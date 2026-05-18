#!/usr/bin/env python3
"""
APHYS AI Community Daemon
=========================
Continuously monitors:
1. Slack DMs from Jonas (feedback/site updates)
2. New gallery submissions on Hypha
3. Community interactions

Relays relevant events to the current Svamp session and notifies Wei+Jonas on Slack.
"""

import json
import logging
import logging.handlers
import os
import smtplib
import ssl
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

# ── Load .env file ─────────────────────────────────────────────────────────
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# ── Configuration ──────────────────────────────────────────────────────────
SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
JONAS_DM_CHANNEL = "D0ANKJFED8F"  # DM channel with Jonas
WEI_DM_CHANNEL = "D0AESV2LHQD"    # DM channel with Wei
JONAS_USER_ID = "U0AM83MUH6V"
WEI_USER_ID = "U059XQJG518"

HYPHA_URL = "https://hypha.aicell.io"
GALLERY_CHILDREN_URL = f"{HYPHA_URL}/kth-sci/artifacts/aphys-ai-gallery/children"
REGISTRATION_URL = f"{HYPHA_URL}/kth-sci/artifacts/aphys-ai-registrations/children"
CLAUDE_REQUEST_URL = f"{HYPHA_URL}/kth-sci/artifacts/aphys-ai-claude-requests/children"

# Email config (Gmail SMTP)
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "APHYS AI Initiative")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
ORGANIZER_EMAILS = ["wei.ouyang@scilifelab.se", "jonassel@kth.se"]

SESSION_ID = os.environ.get("SVAMP_SESSION_ID", "53be87cd-3c5a-4899-b792-b78821590dee")

POLL_INTERVAL = 30  # seconds between checks
BASE_DIR = Path(__file__).parent.resolve()
STATE_FILE = str(BASE_DIR / ".daemon_state.json")
LOG_FILE = str(BASE_DIR / ".daemon.log")

# ── Logging setup ──────────────────────────────────────────────────────────
logger = logging.getLogger("aphys-daemon")
logger.setLevel(logging.DEBUG)

# Console handler (INFO+)
_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
_ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(_ch)

# Rotating file handler (DEBUG+, 2MB max, 5 backups)
_fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=5, encoding="utf-8")
_fh.setLevel(logging.DEBUG)
_fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(_fh)

# ── State management ───────────────────────────────────────────────────────
def load_state():
    """Load persisted state (last seen timestamps, artifact counts)."""
    defaults = {
        "last_slack_ts_jonas": "0",
        "last_slack_ts_wei": "0",
        "known_gallery_count": 0,
        "known_gallery_aliases": [],
        "known_registration_aliases": [],
        "known_claude_request_aliases": [],
        "claude_request_statuses": {},  # alias -> status (for detecting status changes)
        "last_check": None,
    }
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                saved = json.load(f)
            defaults.update(saved)
        except Exception:
            pass
    return defaults


def save_state(state):
    """Persist state to disk."""
    state["last_check"] = datetime.utcnow().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── HTTP helpers ───────────────────────────────────────────────────────────
def http_get(url, headers=None):
    """Simple GET request returning parsed JSON."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        log(f"HTTP GET failed: {url} -> {e}")
        return None


def http_post(url, data, headers=None):
    """Simple POST request returning parsed JSON."""
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        log(f"HTTP POST failed: {url} -> {e}")
        return None


# ── Logging shorthand ──────────────────────────────────────────────────────
def log(msg, level="info"):
    getattr(logger, level)(msg)


# ── Svamp session messaging ───────────────────────────────────────────────
def send_to_session(message, urgency="normal"):
    """Send a message to the current Svamp session."""
    try:
        result = subprocess.run(
            ["svamp", "session", "send", SESSION_ID, message,
             "--urgency", urgency],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            log(f"Sent to session: {message[:80]}...")
        else:
            log(f"svamp send failed: {result.stderr[:200]}")
    except Exception as e:
        log(f"svamp send error: {e}")


# ── Slack messaging ───────────────────────────────────────────────────────
def slack_post(channel, text):
    """Post a message to a Slack channel/DM."""
    return http_post(
        "https://slack.com/api/chat.postMessage",
        {"channel": channel, "text": text},
        {"Authorization": f"Bearer {SLACK_TOKEN}"},
    )


def notify_organizers(text):
    """Notify both Wei and Jonas on Slack."""
    slack_post(WEI_DM_CHANNEL, text)
    slack_post(JONAS_DM_CHANNEL, text)
    log(f"Notified organizers: {text[:80]}...")


# ── Email sending ─────────────────────────────────────────────────────────
def send_email(to_email, subject, body, cc_organizers=False):
    """Send an email via Gmail SMTP. Falls back to Slack notification if SMTP not configured.
    Returns True if sent, False if logged-only fallback."""
    if not SMTP_USER or not SMTP_PASS:
        # Fallback: notify organizers on Slack with the email content
        log(f"SMTP not configured — Slack-fallback for email to {to_email}: {subject}")
        notify_organizers(
            f"[Email pending — please send manually]\n"
            f"To: {to_email}\nSubject: {subject}\n\n{body}"
        )
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"
        msg["To"] = to_email
        if cc_organizers:
            msg["Cc"] = ", ".join(ORGANIZER_EMAILS)
        msg["Reply-To"] = ", ".join(ORGANIZER_EMAILS)
        msg.set_content(body)

        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=20) as s:
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        log(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        log(f"Email send failed: {e}", "error")
        notify_organizers(f"[Email failed — please send manually]\nTo: {to_email}\nSubject: {subject}\nError: {e}\n\n{body}")
        return False


# ── Email templates ───────────────────────────────────────────────────────
def email_registration_confirmation(reg):
    """Confirmation email for May 8 tutorial registration."""
    name = reg.get("name", "there")
    attendance = reg.get("attendance", "AlbaNova")
    body = f"""Hi {name},

Thank you for registering for the APHYS AI Agent Tutorial!

Event details:
  Date:       May 8, 2026
  Time:       13:00-17:00 CET
  Location:   FB53, AlbaNova University Center
  Attendance: {attendance}

What to bring:
  - Your laptop
  - Curiosity — no AI experience required

What you'll get:
  - Hands-on intro to ChatGPT and Claude Code
  - A Claude Team license (standard seat) at no cost
  - Practical examples for research, teaching, and productivity

If you have any questions before the event, just reply to this email.

See you on May 8!

Wei Ouyang & Jonas Sellberg
Department of Applied Physics, KTH
https://kth-sci.github.io/applied-physics-ai/
"""
    return ("Confirmed: APHYS AI Agent Tutorial — May 8, 2026", body)


def email_claude_request_received(req):
    """Confirmation email when someone submits a Claude Team seat request."""
    name = req.get("name", "there")
    seat = req.get("seat", "standard").capitalize()
    body = f"""Hi {name},

Thank you for requesting a {seat} seat in the APHYS Claude Team license.

We have received your application and will review it shortly. You will hear back from us by email within a few days.

Your request summary:
  Name:     {req.get("name","?")}
  Position: {req.get("position","?")}
  Seat:     {seat}
  Motivation: {req.get("motivation","")[:200]}

If you have questions in the meantime, just reply to this email.

Wei Ouyang & Jonas Sellberg
Department of Applied Physics, KTH
https://kth-sci.github.io/applied-physics-ai/
"""
    return (f"Received: your Claude Team seat request ({seat})", body)


def email_claude_request_approved(req):
    """Email when a Claude Team request is approved."""
    name = req.get("name", "there")
    seat = req.get("seat", "standard").capitalize()
    body = f"""Hi {name},

Good news — your request for a {seat} seat in the APHYS Claude Team license has been APPROVED.

Next steps:
  1. We will send you a Claude Team invitation email shortly (separate message from Anthropic).
  2. Accept the invitation and create or link your Claude account.
  3. Install Claude Code if you haven't yet:
     - Mac/Linux: curl -fsSL https://claude.ai/install.sh | bash
     - Windows / Desktop / Web: see https://kth-sci.github.io/applied-physics-ai/ai-agents.html

Reminder of your consent:
  - Projects driven by Claude under this license will be documented in the APHYS AI Gallery
    https://kth-sci.github.io/applied-physics-ai/gallery.html
  - Code repositories will be made available under https://github.com/kth-sci

Welcome to the team — looking forward to seeing what you build!

Wei Ouyang & Jonas Sellberg
Department of Applied Physics, KTH
"""
    return (f"Approved: your Claude Team {seat} seat request", body)


def email_claude_request_rejected(req):
    """Email when a Claude Team request is rejected."""
    name = req.get("name", "there")
    seat = req.get("seat", "standard").capitalize()
    body = f"""Hi {name},

Thank you for your interest in the APHYS Claude Team license.

After review, we are unable to grant your request for a {seat} seat at this time. Common reasons include limited seat availability or eligibility scope.

Alternatives that may work for you:
  - Claude Pro ($20/month) — entry-level Claude Code access
  - Claude Max ($100/month) — full Claude Code access without the team license
  - Join the May 8 Tutorial — Claude Team standard seats available to all attendees:
    https://kth-sci.github.io/applied-physics-ai/events.html

If you have questions about the decision, please reply to this email and we will get back to you.

Wei Ouyang & Jonas Sellberg
Department of Applied Physics, KTH
"""
    return (f"Update on your Claude Team seat request", body)


# ── Poll: Slack messages from Jonas ───────────────────────────────────────
def check_slack_messages(state):
    """Check for new DMs from Jonas and relay to session."""
    url = (
        f"https://slack.com/api/conversations.history"
        f"?channel={JONAS_DM_CHANNEL}&limit=100"
        f"&oldest={state['last_slack_ts_jonas']}"
    )
    data = http_get(url, {"Authorization": f"Bearer {SLACK_TOKEN}"})
    if not data or not data.get("ok"):
        return

    messages = data.get("messages", [])
    last_seen = float(state["last_slack_ts_jonas"])
    # Always advance the cursor past every message we just fetched, so we don't
    # loop forever on bot/non-Jonas messages that don't trigger the timestamp bump.
    for m in messages:
        try:
            t = float(m.get("ts", "0"))
        except (TypeError, ValueError):
            continue
        if t > last_seen:
            last_seen = t
    if last_seen > float(state["last_slack_ts_jonas"]):
        state["last_slack_ts_jonas"] = f"{last_seen:.6f}"

    # Filter to messages FROM Jonas (not from our bot)
    new_msgs = sorted(
        [m for m in messages
         if m.get("user") == JONAS_USER_ID
         and float(m.get("ts", "0")) > float("0")],  # filter happens via `oldest` already
        key=lambda m: float(m["ts"]),
    )
    if not new_msgs:
        return

    for msg in new_msgs:
        text = msg.get("text", "").strip()
        if not text:
            continue
        log(f"New message from Jonas: {text[:100]}")
        send_to_session(
            f"[Slack from Jonas] {text}\n\n"
            f"(Reply via Slack or update the site accordingly.)",
            urgency="urgent",
        )


def check_slack_messages_wei(state):
    """Check for new DMs from Wei and relay to session."""
    url = (
        f"https://slack.com/api/conversations.history"
        f"?channel={WEI_DM_CHANNEL}&limit=100"
        f"&oldest={state['last_slack_ts_wei']}"
    )
    data = http_get(url, {"Authorization": f"Bearer {SLACK_TOKEN}"})
    if not data or not data.get("ok"):
        return

    messages = data.get("messages", [])
    last_seen = float(state["last_slack_ts_wei"])
    for m in messages:
        try:
            t = float(m.get("ts", "0"))
        except (TypeError, ValueError):
            continue
        if t > last_seen:
            last_seen = t
    if last_seen > float(state["last_slack_ts_wei"]):
        state["last_slack_ts_wei"] = f"{last_seen:.6f}"

    new_msgs = sorted(
        [m for m in messages if m.get("user") == WEI_USER_ID],
        key=lambda m: float(m["ts"]),
    )

    if not new_msgs:
        return

    for msg in new_msgs:
        text = msg.get("text", "").strip()
        if not text:
            continue
        log(f"New message from Wei: {text[:100]}")
        send_to_session(
            f"[Slack from Wei] {text}",
            urgency="urgent",
        )


# ── Poll: New gallery submissions ─────────────────────────────────────────
def check_gallery_submissions(state):
    """Check for new use case submissions on Hypha."""
    data = http_get(f"{GALLERY_CHILDREN_URL}?pagination=true&limit=100&silent=true")
    if not data or "items" not in data:
        return

    current_count = data["total"]
    current_aliases = {item["alias"] for item in data["items"]}
    known_aliases = set(state.get("known_gallery_aliases", []))

    new_aliases = current_aliases - known_aliases

    if new_aliases and known_aliases:  # Only alert if we had a baseline
        for alias in new_aliases:
            item = next((i for i in data["items"] if i["alias"] == alias), None)
            if not item:
                continue
            m = item.get("manifest", {})
            name = m.get("name", alias)
            tool = m.get("tool", "Unknown")
            author = m.get("author", "Anonymous")
            desc = (m.get("description", "")[:150] + "...") if len(m.get("description", "")) > 150 else m.get("description", "")

            log(f"New gallery submission: {name} by {author}")

            # Notify session
            send_to_session(
                f"[New Gallery Submission]\n"
                f"Title: {name}\n"
                f"Tool: {tool}\n"
                f"Author: {author}\n"
                f"Description: {desc}\n\n"
                f"Gallery: https://kth-sci.github.io/applied-physics-ai/gallery.html#{alias}",
            )

            # Notify organizers on Slack
            notify_organizers(
                f"New use case submitted to the APHYS AI Gallery!\n"
                f"*{name}* ({tool}) by {author}\n"
                f"View: https://kth-sci.github.io/applied-physics-ai/gallery.html#{alias}"
            )

    # Update state
    state["known_gallery_count"] = current_count
    state["known_gallery_aliases"] = list(current_aliases)


# ── Poll: New event registrations ─────────────────────────────────────────
def check_registrations(state):
    """Check for new May 8 tutorial registrations and send confirmation emails."""
    data = http_get(f"{REGISTRATION_URL}?pagination=true&limit=200&silent=true")
    if not data or "items" not in data:
        return
    known = set(state.get("known_registration_aliases", []))
    current = {item["alias"] for item in data["items"]}
    new_aliases = current - known
    if new_aliases and known:
        for alias in new_aliases:
            item = next((i for i in data["items"] if i["alias"] == alias), None)
            if not item:
                continue
            m = item.get("manifest", {})
            email = m.get("email")
            if not email or "@" not in email:
                continue
            log(f"New registration: {m.get('name','?')} <{email}>")
            subject, body = email_registration_confirmation(m)
            send_email(email, subject, body, cc_organizers=False)
            notify_organizers(
                f"New May 8 registration: *{m.get('name','?')}* <{email}> "
                f"({m.get('attendance','?')}, {m.get('experience','?')})"
            )
    state["known_registration_aliases"] = list(current)


# ── Poll: New / status-changed Claude Team requests ──────────────────────
def check_claude_requests(state):
    """Check for new Claude Team requests + status changes (approved/rejected)."""
    data = http_get(f"{CLAUDE_REQUEST_URL}?pagination=true&limit=200&silent=true")
    if not data or "items" not in data:
        return
    known = set(state.get("known_claude_request_aliases", []))
    statuses = dict(state.get("claude_request_statuses", {}))
    current = {item["alias"] for item in data["items"]}
    new_aliases = current - known

    # New requests → confirmation email
    if new_aliases and known:
        for alias in new_aliases:
            item = next((i for i in data["items"] if i["alias"] == alias), None)
            if not item:
                continue
            m = item.get("manifest", {})
            email = m.get("email")
            if not email or "@" not in email:
                continue
            log(f"New Claude request: {m.get('name','?')} <{email}> ({m.get('seat','standard')})")
            subject, body = email_claude_request_received(m)
            send_email(email, subject, body, cc_organizers=False)
            notify_organizers(
                f"New Claude Team request: *{m.get('name','?')}* <{email}>\n"
                f"Position: {m.get('position','?')} | Seat: {m.get('seat','standard')}\n"
                f"Motivation: {(m.get('motivation','') or '')[:200]}"
            )

    # Status changes → approval/rejection email
    for item in data["items"]:
        alias = item["alias"]
        m = item.get("manifest", {})
        cur_status = m.get("status", "pending")
        prev_status = statuses.get(alias)
        if prev_status is None:
            statuses[alias] = cur_status
            continue
        if prev_status == cur_status:
            continue
        # Status changed
        statuses[alias] = cur_status
        email = m.get("email")
        if not email or "@" not in email:
            continue
        if cur_status == "approved":
            log(f"Claude request approved: {m.get('name','?')} <{email}>")
            subject, body = email_claude_request_approved(m)
            send_email(email, subject, body, cc_organizers=True)
        elif cur_status == "rejected":
            log(f"Claude request rejected: {m.get('name','?')} <{email}>")
            subject, body = email_claude_request_rejected(m)
            send_email(email, subject, body, cc_organizers=True)
        # 'pending' (reset) — no email

    state["known_claude_request_aliases"] = list(current)
    state["claude_request_statuses"] = statuses


# ── Poll: Action requests from admin dashboard ────────────────────────────
FEEDBACK_CHILDREN_URL = f"{HYPHA_URL}/kth-sci/artifacts/aphys-ai-feedback/children"

def check_action_requests(state):
    """Check for pending action requests submitted from the admin dashboard."""
    data = http_get(f"{FEEDBACK_CHILDREN_URL}?pagination=true&limit=100&silent=true")
    if not data or "items" not in data:
        return

    known = set(state.get("known_feedback_aliases", []))
    current = {item["alias"] for item in data["items"]}
    new_aliases = current - known

    if new_aliases and known:
        for alias in new_aliases:
            item = next((i for i in data["items"] if i["alias"] == alias), None)
            if not item:
                continue
            m = item.get("manifest", {})

            # Action requests from admin "Send to Agent" button
            if m.get("type") == "action-request" and m.get("status") == "pending":
                prompt = m.get("prompt", "")
                page = m.get("page", "unknown")
                log(f"Action request for {page}: {m.get('comment','')[:80]}")
                send_to_session(
                    f"[Admin Action Request] Implement feedback for {page}:\n\n"
                    f"\"{m.get('comment', '')}\"\n\n"
                    f"Please make the improvement and confirm on Slack.",
                    urgency="urgent",
                )
                notify_organizers(
                    f"Action request sent to AI agent for *{page}*:\n\"{m.get('comment', '')[:150]}\""
                )

            # Regular feedback (just notify, don't action)
            elif m.get("vote") == "down" and m.get("comment"):
                log(f"New negative feedback on {m.get('page','?')}: {m.get('comment','')[:80]}")
                notify_organizers(
                    f"New feedback on *{m.get('page', '?')}* (thumbs down):\n\"{m.get('comment', '')[:200]}\""
                )

    state["known_feedback_aliases"] = list(current)


# ── Main loop ─────────────────────────────────────────────────────────────
def main():
    log("=" * 60)
    log("APHYS AI Community Daemon starting")
    log(f"Session: {SESSION_ID}")
    log(f"Poll interval: {POLL_INTERVAL}s")
    log(f"Monitoring: Slack (Jonas+Wei), Hypha gallery")
    log("=" * 60)

    state = load_state()

    # Initialize: set current slack timestamps to "now" so we don't replay old messages
    if state["last_slack_ts_jonas"] == "0":
        # Fetch latest message to get current timestamp
        for channel, key in [(JONAS_DM_CHANNEL, "last_slack_ts_jonas"), (WEI_DM_CHANNEL, "last_slack_ts_wei")]:
            data = http_get(
                f"https://slack.com/api/conversations.history?channel={channel}&limit=1",
                {"Authorization": f"Bearer {SLACK_TOKEN}"},
            )
            if data and data.get("ok") and data.get("messages"):
                state[key] = data["messages"][0]["ts"]
                log(f"Initialized {key} = {state[key]}")

    # Initialize feedback baseline
    if not state.get("known_feedback_aliases"):
        data = http_get(f"{FEEDBACK_CHILDREN_URL}?pagination=true&limit=100&silent=true")
        if data and "items" in data:
            state["known_feedback_aliases"] = [i["alias"] for i in data["items"]]
            log(f"Feedback baseline: {data['total']} items")

    # Initialize gallery baseline
    if not state.get("known_gallery_aliases"):
        data = http_get(f"{GALLERY_CHILDREN_URL}?pagination=true&limit=100&silent=true")
        if data and "items" in data:
            state["known_gallery_count"] = data["total"]
            state["known_gallery_aliases"] = [i["alias"] for i in data["items"]]
            log(f"Gallery baseline: {data['total']} items")

    # Initialize registration baseline
    if not state.get("known_registration_aliases"):
        data = http_get(f"{REGISTRATION_URL}?pagination=true&limit=200&silent=true")
        if data and "items" in data:
            state["known_registration_aliases"] = [i["alias"] for i in data["items"]]
            log(f"Registration baseline: {data.get('total', 0)} items")

    # Initialize Claude requests baseline (also seed status map)
    if not state.get("known_claude_request_aliases"):
        data = http_get(f"{CLAUDE_REQUEST_URL}?pagination=true&limit=200&silent=true")
        if data and "items" in data:
            state["known_claude_request_aliases"] = [i["alias"] for i in data["items"]]
            state["claude_request_statuses"] = {
                i["alias"]: (i.get("manifest", {}).get("status") or "pending") for i in data["items"]
            }
            log(f"Claude requests baseline: {data.get('total', 0)} items")

    log(f"SMTP email: {'enabled (' + SMTP_USER + ')' if SMTP_USER and SMTP_PASS else 'NOT configured — using Slack fallback'}")

    save_state(state)
    log("Initialization complete. Entering poll loop.\n")

    while True:
        try:
            logger.debug("Poll cycle start")
            check_slack_messages(state)
            check_slack_messages_wei(state)
            check_gallery_submissions(state)
            check_action_requests(state)
            check_registrations(state)
            check_claude_requests(state)
            save_state(state)
            logger.debug("Poll cycle complete")
        except Exception as e:
            logger.exception(f"Error in poll loop: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
