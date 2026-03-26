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
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime
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


# ── Poll: Slack messages from Jonas ───────────────────────────────────────
def check_slack_messages(state):
    """Check for new DMs from Jonas and relay to session."""
    url = (
        f"https://slack.com/api/conversations.history"
        f"?channel={JONAS_DM_CHANNEL}&limit=5"
        f"&oldest={state['last_slack_ts_jonas']}"
    )
    data = http_get(url, {"Authorization": f"Bearer {SLACK_TOKEN}"})
    if not data or not data.get("ok"):
        return

    messages = data.get("messages", [])
    # Filter to messages FROM Jonas (not from our bot)
    new_msgs = [
        m for m in messages
        if m.get("user") == JONAS_USER_ID
        and float(m.get("ts", "0")) > float(state["last_slack_ts_jonas"])
    ]

    if not new_msgs:
        return

    # Update timestamp to latest
    new_msgs.sort(key=lambda m: float(m["ts"]))
    state["last_slack_ts_jonas"] = new_msgs[-1]["ts"]

    for msg in new_msgs:
        text = msg.get("text", "").strip()
        if not text:
            continue
        log(f"New message from Jonas: {text[:100]}")
        # Relay to session
        send_to_session(
            f"[Slack from Jonas] {text}\n\n"
            f"(Reply via Slack or update the site accordingly.)",
            urgency="urgent",
        )


def check_slack_messages_wei(state):
    """Check for new DMs from Wei and relay to session."""
    url = (
        f"https://slack.com/api/conversations.history"
        f"?channel={WEI_DM_CHANNEL}&limit=5"
        f"&oldest={state['last_slack_ts_wei']}"
    )
    data = http_get(url, {"Authorization": f"Bearer {SLACK_TOKEN}"})
    if not data or not data.get("ok"):
        return

    messages = data.get("messages", [])
    new_msgs = [
        m for m in messages
        if m.get("user") == WEI_USER_ID
        and float(m.get("ts", "0")) > float(state["last_slack_ts_wei"])
    ]

    if not new_msgs:
        return

    new_msgs.sort(key=lambda m: float(m["ts"]))
    state["last_slack_ts_wei"] = new_msgs[-1]["ts"]

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

    save_state(state)
    log("Initialization complete. Entering poll loop.\n")

    while True:
        try:
            logger.debug("Poll cycle start")
            check_slack_messages(state)
            check_slack_messages_wei(state)
            check_gallery_submissions(state)
            check_action_requests(state)
            save_state(state)
            logger.debug("Poll cycle complete")
        except Exception as e:
            logger.exception(f"Error in poll loop: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
