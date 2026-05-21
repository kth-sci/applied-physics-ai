# Handoff — Claude Seat Request Email Agent

**Purpose:** another agent running in `/Users/weio/workspace/applied-physics-ai/` takes over the email side of the Claude Team seat request workflow. This other agent has **SMTP email access but no Slack access** — so it sends confirmation / approval / rejection emails directly via Gmail SMTP.

Today is 2026-05-21. The APHYS AI initiative is live; the May 8 tutorial happened (48 participants); the May 26 SCI Hackathon is the next event. ~20 Claude Team seat requests so far.

---

## What this agent owns

Continuously monitor two Hypha collections and send the right email for each event. The infrastructure already exists — this agent's job is to keep `daemon.py` running with SMTP enabled, and to use `send_email.py` for manual approvals/rejections when needed.

| Event | Trigger | Email |
|---|---|---|
| New May 8 registration | new artifact in `kth-sci/aphys-ai-registrations` | Confirmation to attendee |
| New Claude seat request | new artifact in `kth-sci/aphys-ai-claude-requests` | "Received: your Claude Team seat request" |
| Request approved | `status` flips `pending` → `approved` in the admin UI | Approval + next steps |
| Request rejected | `status` flips `pending` → `rejected` | Polite rejection with alternatives |

All templates and the polling loop already exist in `daemon.py`. The `send_email.py` CLI exists for one-off sends.

---

## Quick start

### 1. Read the project context

```bash
cd /Users/weio/workspace/applied-physics-ai
cat CLAUDE.md          # full project overview — read the "Email setup" + "Email CLI" sections
cat HANDOFF.md         # broader handoff (slightly older but still accurate)
```

### 2. Stop the previous daemon (if running)

```bash
[ -f .daemon.pid ] && kill $(cat .daemon.pid) 2>/dev/null
rm -f .daemon.pid
```

**Leave `.daemon_state.json` in place.** It tracks which registrations / Claude requests have already been seen; deleting it would re-send confirmation emails for every existing entry (40+ duplicates).

### 3. Confirm SMTP credentials are in `.env`

```bash
grep -E "^SMTP_(USER|PASS|FROM_NAME)" .env
```

Expected:
```
SMTP_USER=kth.aphys.ai@gmail.com
SMTP_PASS=<gmail app password, 16 chars no spaces>
SMTP_FROM_NAME=APHYS AI Initiative
```

If `SMTP_PASS` is missing, get the app password from Jonas (or regenerate at https://myaccount.google.com/apppasswords — requires 2FA on the Gmail account). The account is `kth.aphys.ai@gmail.com`, owned jointly by Wei + Jonas.

### 4. Test the SMTP CLI without sending

```bash
python3 send_email.py --to "Your Name <you@kth.se>" --template claude-approved --dry-run
```

Should preview the email body. If you see "SMTP_PASS not set" the `.env` is not loading — check the file path.

### 5. Send a real test to yourself

```bash
python3 send_email.py --to "Your Name <you@kth.se>" --template claude-approved
```

Check your inbox. If it arrives, SMTP is working end-to-end.

### 6. Start the daemon

```bash
cd /Users/weio/workspace/applied-physics-ai
nohup python3 daemon.py >> /dev/null 2>&1 &
echo $! > .daemon.pid
sleep 4
grep -v DEBUG .daemon.log | tail -10
```

Confirm you see:
```
SMTP email: enabled (kth.aphys.ai@gmail.com)
```

If it says `NOT configured — using Slack fallback`, the `.env` did not load. Restart the daemon after fixing.

---

## Two ways to send emails

### A. Automatic — via the daemon

The daemon polls Hypha every 30 s and auto-sends confirmation emails on new registrations / Claude requests, and approval/rejection emails when an admin flips a status in the dashboard. Once it's running with SMTP enabled, you don't have to do anything for the common case.

### B. Manual one-off — via `send_email.py`

For ad-hoc cases (e.g. resending an approval email someone missed, or rejecting a request that was created before the daemon was started):

```bash
# Approve a Claude Team seat request
python3 send_email.py --to "Ada Lovelace <ada@kth.se>" --template claude-approved

# Reject a Claude seat request
python3 send_email.py --to "Ada Lovelace <ada@kth.se>" --template claude-rejected

# Send a free-form custom message
python3 send_email.py --to "Name <email@kth.se>" \
    --subject "Subject line" \
    --body "Body text on multiple lines is fine"

# Send to multiple recipients
python3 send_email.py \
    --to "A <a@kth.se>" --to "B <b@kth.se>" \
    --subject "Hi everyone" --body "..."

# Preview before sending
python3 send_email.py --to "..." --template claude-approved --dry-run
```

---

## How the daemon decides what to send

`daemon.py` keeps `.daemon_state.json` with three things relevant here:

- `known_registration_aliases`: list of registration artifacts already processed → no duplicate confirmations
- `known_claude_request_aliases`: same for Claude requests
- `claude_request_statuses`: dict of `alias → status` so the daemon can detect when an admin changes status (`pending` → `approved` / `rejected`) and trigger the corresponding email

When the daemon starts fresh with an empty state, it seeds these baselines from the current Hypha state (no emails sent for existing items). Then it only acts on new items / status changes that happen after start-up. This is why **never delete `.daemon_state.json`** — that would re-seed and miss any change you already processed.

The expiration date (Faculty std=1yr, Researcher std=6mo, Postdoc/PhD std=3mo, any Premium=3mo) is auto-computed in the admin UI when status flips to approved. The agent does not need to touch expiration — but the approval email body references it.

---

## Coordination rules

- **Confirmation emails on new submissions are fully automatic.** No human input needed.
- **Approval / rejection emails only fire when a human flips the status** in the admin UI: https://kth-sci.github.io/applied-physics-ai/admin.html (passphrase `aphys2026`). Do not approve/reject requests from the agent side.
- **Both Wei and Jonas are CCed on approval/rejection emails.** Set in `daemon.py` as `ORGANIZER_EMAILS = ["wei.ouyang@scilifelab.se", "jonassel@kth.se"]`. Confirmation emails are sent to the user only, not CCed.
- **Reply-To is set to both organizers on every email**, so user replies land in both inboxes.
- This agent has no Slack. If something needs human attention (e.g. SMTP auth keeps failing), email Wei or Jonas directly using `send_email.py` — do not try to reach Slack.

---

## Things to NEVER do

- Don't edit the email template content in `daemon.py` or `send_email.py` — they're reviewed copy. If text needs to change, ask Wei or Jonas via email first.
- Don't delete `.daemon_state.json`.
- Don't commit `.env` to git. It's in `.gitignore` already; double-check before any `git add -A`.
- Don't approve / reject Claude requests from the agent side. Humans-only via admin UI.
- Don't reduce the poll interval below ~15 s — Hypha rate-limits and starts returning 503s.

---

## When things go wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Daemon stopped | crash or system restart | Restart per §6 above |
| "SMTP NOT configured" in logs | `.env` did not load | Check file exists at repo root with all three SMTP vars, no quotes |
| "Username and Password not accepted" | wrong/expired app password | Regenerate at https://myaccount.google.com/apppasswords |
| Duplicate emails sent | state file not being written | Check `.daemon_state.json` mtime — should update every 30 s |
| Hypha 503s | service temporarily unavailable | Daemon retries every 30 s. Wait it out. |
| No new emails despite new submissions | daemon stuck on a stale Slack timestamp | Look at `last_slack_ts_jonas` in `.daemon_state.json` vs latest Slack ts — fixed in May, but watch for regressions |

---

## File map

| File | Role |
|---|---|
| `daemon.py` | Long-running poller. Send-email logic + email templates inside. |
| `send_email.py` | CLI for manual sends. Uses same SMTP creds. |
| `.env` | SMTP_USER / SMTP_PASS / SMTP_FROM_NAME. Gitignored. |
| `.daemon.pid` | Current daemon process ID. Gitignored. |
| `.daemon.log` | Rotating log (2 MB × 5). Gitignored. |
| `.daemon_state.json` | Per-collection seen-aliases + per-request statuses. Gitignored. |
| `CLAUDE.md` | Full project context — read sections "Community Daemon", "Email setup", "Email CLI". |
| `HANDOFF.md` | Earlier session handoff doc — broader project context. |

---

## Sanity-check command bundle

Run this once after setup to verify everything is healthy:

```bash
cd /Users/weio/workspace/applied-physics-ai
echo "=== Daemon process ==="
kill -0 $(cat .daemon.pid 2>/dev/null) 2>/dev/null && echo "  running (PID $(cat .daemon.pid))" || echo "  STOPPED"
echo "=== SMTP config in .env ==="
grep -E "^SMTP_(USER|PASS|FROM_NAME)=" .env | sed 's/PASS=.*/PASS=<set>/'
echo "=== Daemon recent log (non-debug) ==="
grep -v DEBUG .daemon.log 2>/dev/null | tail -8
echo "=== State file ==="
[ -f .daemon_state.json ] && stat -f "  %Sm: .daemon_state.json" .daemon_state.json 2>/dev/null || echo "  missing"
echo "=== Claude Team requests on Hypha ==="
curl -s "https://hypha.aicell.io/kth-sci/artifacts/aphys-ai-claude-requests/children?pagination=true&limit=1&silent=true" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  total: {d.get(\"total\",\"?\")}')"
echo "=== Registrations on Hypha ==="
curl -s "https://hypha.aicell.io/kth-sci/artifacts/aphys-ai-registrations/children?pagination=true&limit=1&silent=true" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  total: {d.get(\"total\",\"?\")}')"
```

A healthy setup looks like:

```
=== Daemon process ===
  running (PID 12345)
=== SMTP config in .env ===
SMTP_USER=kth.aphys.ai@gmail.com
SMTP_PASS=<set>
SMTP_FROM_NAME=APHYS AI Initiative
=== Daemon recent log (non-debug) ===
2026-05-21 ... [INFO] aphys-daemon: SMTP email: enabled (kth.aphys.ai@gmail.com)
2026-05-21 ... [INFO] aphys-daemon: Initialization complete. Entering poll loop.
=== State file ===
  May 21 16:50:33 2026: .daemon_state.json
=== Claude Team requests on Hypha ===
  total: 20
=== Registrations on Hypha ===
  total: 48
```

If all five blocks look like that, the handoff is complete. The daemon will run itself; you only need to act if logs start showing errors.
