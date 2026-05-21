# Handoff — Claude Seat Request Email Agent

**Purpose:** another agent running in `/Users/weio/workspace/applied-physics-ai/` takes over the email side of the Claude Team seat request workflow. This other agent has **SMTP email access but no Slack access** — so it sends confirmation / approval / rejection emails directly, while this session's daemon (which had only Slack fallback) is being retired.

Today is 2026-05-21. The APHYS AI initiative is live; the May 8 tutorial happened; the May 26 SCI Hackathon is the next event. ~48 May 8 attendees, ~20 Claude Team seat requests so far.

---

## What this agent needs to do

Continuously monitor two Hypha collections and send the right email for each event:

| Event | Trigger | Email to send |
|---|---|---|
| New May 8 tutorial registration | new artifact in `kth-sci/aphys-ai-registrations` | Confirmation to attendee |
| New Claude Team seat request | new artifact in `kth-sci/aphys-ai-claude-requests` | "Received: your Claude Team seat request" |
| Claude request approved | `status` flips to `approved` on an existing request | Approval email with next steps + Claude Team invite reminder |
| Claude request rejected | `status` flips to `rejected` | Polite rejection with alternatives |

All four email templates already exist in `daemon.py` (functions named `email_registration_confirmation`, `email_claude_request_received`, `email_claude_request_approved`, `email_claude_request_rejected`). **Do not rewrite them** — they are content-reviewed and consistent with the rest of the site.

The expiration auto-computation (Faculty std=1yr, Researcher std=6mo, Postdoc/PhD std=3mo, any Premium=3mo) is handled client-side in the admin UI when a status flips to approved. The agent does not need to touch expiration — it just sends the emails when status changes.

---

## Quick start (do these, in order)

### 1. Read the project context

```bash
cd /Users/weio/workspace/applied-physics-ai
cat CLAUDE.md          # project overview
cat HANDOFF.md         # broader handoff doc (slightly older)
```

### 2. Stop the previous daemon (it's running with Slack fallback only)

```bash
[ -f .daemon.pid ] && kill $(cat .daemon.pid) 2>/dev/null
rm -f .daemon.pid
```

The state file `.daemon_state.json` should be left in place — it tracks which registrations / Claude requests have already been seen, so the new daemon does not re-send confirmation emails for old entries.

### 3. Add SMTP credentials to `.env`

```bash
# Open .env (do NOT commit it — it is gitignored)
nano .env
```

Add these three lines (replace with real values):

```
SMTP_USER=kth-aphys-ai@gmail.com
SMTP_PASS=<gmail app password — 16 chars, no spaces>
SMTP_FROM_NAME=APHYS AI Initiative
```

The Gmail app password is generated at https://myaccount.google.com/apppasswords (requires 2FA on the Gmail account). The address `kth-aphys-ai@gmail.com` was set up by Wei + Jonas on 2026-05-07 — the password is whatever Jonas saved.

If SMTP credentials are missing, the daemon falls back to posting "[Email pending — please send manually]" to Slack — which we do **not** want any more. Setting these vars is what flips the daemon into autonomous-email mode.

### 4. Start the daemon

```bash
cd /Users/weio/workspace/applied-physics-ai
nohup python3 daemon.py >> /dev/null 2>&1 &
echo $! > .daemon.pid
sleep 4
grep -v DEBUG .daemon.log | tail -10
```

You should see a line like:

```
SMTP email: enabled (kth-aphys-ai@gmail.com)
```

If it instead says `SMTP email: NOT configured — using Slack fallback`, the credentials in `.env` were not loaded. Restart after fixing.

### 5. Verify by sending a test

The cleanest test is to submit a fake Claude request via the public form and watch the daemon send the email:

- Go to https://kth-sci.github.io/applied-physics-ai/ai-agents.html
- Click the "Request a Claude Team Seat" button
- Submit with your own email (so you can verify the message arrives)
- Within 30s, daemon should log `Email sent to <you>: Received: your Claude Team seat request (Standard)` and your inbox gets the confirmation

If something fails, the daemon will log the SMTP error (typically auth error if the app password is wrong, or "Less Secure Apps" if 2FA is not on).

---

## How the daemon is structured

`daemon.py` has these polling functions, called every 30 seconds:

- `check_slack_messages` / `check_slack_messages_wei` — relays Jonas/Wei Slack DMs to the Svamp session. **You can ignore these** if you have no Slack token; they will fail silently and not affect email sending.
- `check_registrations` — sees new May 8 tutorial registrations and sends confirmation emails.
- `check_claude_requests` — sees new Claude Team requests (→ received-confirmation email) and status changes on existing ones (→ approval / rejection email). Tracks per-request status in `.daemon_state.json` so it does not re-send.
- `check_gallery_submissions` — notifies organizers when someone submits a use case to the public gallery. Not email-related.
- `check_action_requests` — admin-dashboard "Send to Agent" hook. Not email-related.

The email sending is `send_email(to_email, subject, body, cc_organizers=False)` at the top of the file. It uses Gmail SMTP over SSL on port 465.

If you only want the email pieces and nothing else, you can:

```python
# Quick test of just the email path:
python3 -c "
import daemon
daemon.send_email('your.email@kth.se', 'Test', 'This is a test from the daemon.')
"
```

(Run from `/Users/weio/workspace/applied-physics-ai/` so `.env` loads.)

---

## Coordinating with the human team (Jonas + Wei)

- **Do not send approval emails until Jonas (or Wei) explicitly approves a request via the admin dashboard.** The approval/rejection emails fire when `status` flips from `pending` → `approved` or `rejected`. Status flips are controlled by the admin UI at https://kth-sci.github.io/applied-physics-ai/admin.html (passphrase `aphys2026`).
- **Confirmation emails on new submissions are automatic** — send them as soon as a new artifact appears in the collection. The template already says "we will review it and contact you" so users know an approval email is coming separately.
- **CC the organizers on approval/rejection only** (not on the initial confirmation). This is already wired in `send_email(..., cc_organizers=True)` for status-change emails. `ORGANIZER_EMAILS = ["wei.ouyang@scilifelab.se", "jonassel@kth.se"]` at the top of `daemon.py`.
- **Reply-To on every email** is set to both Wei and Jonas, so when an attendee replies it lands in both inboxes.

---

## Things you should NOT do

- Do not edit the email templates' content — they are reviewed copy. If text needs to change, ask Wei or Jonas first.
- Do not change the cron / poll interval below ~15 s (Hypha rate-limits and we get 503s).
- Do not delete `.daemon_state.json` — that would re-send confirmation emails for every existing registration / request (40+ duplicate emails).
- Do not commit `.env` to git. It's in `.gitignore` already but double-check before any `git add`.
- Do not approve/reject Claude requests from the agent side. Only the admin dashboard (a human) does that.

---

## When something goes wrong

- **Daemon stopped:** `cat .daemon.pid | xargs kill -0 2>/dev/null && echo running || echo stopped`. Restart with the command in §4.
- **No emails being sent (but logs show "SMTP not configured"):** `.env` did not load. Check the file exists at `/Users/weio/workspace/applied-physics-ai/.env`, contains all three SMTP vars, no quotes around values.
- **No emails (SMTP enabled but errors):** the most common errors are auth failures (wrong app password) or "username and password not accepted" (need to regenerate app password). Check `tail -30 .daemon.log`.
- **Duplicate emails being sent:** check `.daemon_state.json` is being written. If `last_check` is updating but `known_*_aliases` lists are not growing, there's a state-save bug.
- **Hypha returning 503s for long stretches:** that happens. Daemon retries every 30s; just wait. Logs will show `HTTP GET failed: ... 503`.

---

## Quick reference — files and URLs

| Thing | Where |
|---|---|
| Daemon script | `/Users/weio/workspace/applied-physics-ai/daemon.py` |
| Persisted state | `/Users/weio/workspace/applied-physics-ai/.daemon_state.json` |
| Log (rotating, 2 MB × 5) | `/Users/weio/workspace/applied-physics-ai/.daemon.log` |
| PID file | `/Users/weio/workspace/applied-physics-ai/.daemon.pid` |
| Credentials | `/Users/weio/workspace/applied-physics-ai/.env` (gitignored) |
| Hypha API base | https://hypha.aicell.io |
| Hypha workspace | `kth-sci` |
| Claude requests collection | https://hypha.aicell.io/kth-sci/artifacts/aphys-ai-claude-requests/children |
| Registrations collection | https://hypha.aicell.io/kth-sci/artifacts/aphys-ai-registrations/children |
| Admin dashboard | https://kth-sci.github.io/applied-physics-ai/admin.html (passphrase `aphys2026`) |
| Public site | https://kth-sci.github.io/applied-physics-ai/ |

---

## Verifying you have everything

Run this once after setup to sanity-check:

```bash
cd /Users/weio/workspace/applied-physics-ai
echo "=== Daemon ==="
kill -0 $(cat .daemon.pid 2>/dev/null) 2>/dev/null && echo "  running (PID $(cat .daemon.pid))" || echo "  STOPPED"
echo "=== SMTP enabled? ==="
grep -E "^SMTP_(USER|PASS)=" .env | sed 's/=.*/=set/' || echo "  not configured"
echo "=== Last log lines ==="
grep -v DEBUG .daemon.log | tail -8
echo "=== Claude requests in Hypha ==="
curl -s "https://hypha.aicell.io/kth-sci/artifacts/aphys-ai-claude-requests/children?pagination=true&limit=1&silent=true" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  total: {d.get(\"total\",\"?\")}')"
```

Expected output:

```
=== Daemon ===
  running (PID 12345)
=== SMTP enabled? ===
SMTP_USER=set
SMTP_PASS=set
=== Last log lines ===
2026-05-21 ... [INFO] aphys-daemon: SMTP email: enabled (kth-aphys-ai@gmail.com)
2026-05-21 ... [INFO] aphys-daemon: Initialization complete. Entering poll loop.
=== Claude requests in Hypha ===
  total: 20
```

If all four sections look healthy, you are good. The agent does not need to do anything else — the daemon runs itself.
