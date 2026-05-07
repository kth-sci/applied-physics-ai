# Handoff — APHYS AI Initiative

Context for the next agent session. Last updated 2026-05-07.

## What this project is

The internal webpage and operational backbone for the **Applied Physics AI Initiative** at KTH (https://kth-sci.github.io/applied-physics-ai/). Led by Wei Ouyang and Jonas Sellberg. The agent's role is to act as the operational arm: build/maintain the site, monitor Slack and Hypha, send confirmations, prepare materials for events, and execute Jonas's feedback verbatim.

Read `CLAUDE.md` first for the full project context — vision, design philosophy, repo layout, and agent instructions.

## Imminent priority — May 8 Tutorial (TOMORROW)

**Date:** Friday, May 8, 2026, 13:00–17:00 CET
**Location:** FB53, AlbaNova University Center (+ Zoom for 7 attendees)
**Status as of handoff:** 43 attendees registered, of which 36 onsite, 7 Zoom. Claude Team licenses being arranged for everyone.

**Roles for the day:**
- **Wei** — leads intro (13:00–13:30), drives Claude Code in the live demo, runs hands-on
- **Jonas** — leads ChatGPT segment (13:30–14:15), pairs with Wei in live demo as the "domain expert" framing the physics
- **Christian Ohm** — confirmed guest speaker for advanced-user showcase (15:00–15:45). He'll cover Copilot/Cursor (free 1-yr student plan)/Claude Code/OpenCode plus possibly an MCP+CAD demo.

**Detailed agenda:** `docs/may-8-tutorial.html`
**Intro slide deck (scaffolded, not finished):** `docs/slides/may-8-intro.html`
  - Karpathy material lands at slides 4–6 and slide 9 ("you can outsource your thinking, but you cannot outsource your understanding")
**ChatGPT slides (Jonas's segment):** *not yet drafted* — Jonas may draft these himself
**Slide source quotes / framing notes:** `attendees/slide-source-notes.md`

**Open items before May 8:**
1. **Welcome + Claude Team invite email** to all 43 attendees — Jonas will send manually since SMTP is still propagating. Template at `attendees/welcome-email-template.md`. Email list at `attendees/may8-attendees.txt`.
2. **Claude Team monthly seats** — Jonas coordinating with Carlota Canalias (Head of Dept) for the 13+ extra seats beyond their 30-seat annual plan.
3. **SMTP credentials** — Wei + Jonas just set up `kth-aphys-ai@gmail.com` Gmail. Account is <24h old so Google won't allow SMTP yet. As soon as it propagates, drop into `.env`:
   ```
   SMTP_USER=kth-aphys-ai@gmail.com
   SMTP_PASS=<app password>
   SMTP_FROM_NAME=KTH APhys AI
   ```
   Then restart daemon. Confirmation emails will start sending automatically.
4. **Stuart McAndrew talk link** — pending speaker permission (Christian to ask). Once cleared, drop the link into the "Follow-up Resources" section of `docs/may-8-tutorial.html`.
5. **The 4 approved-but-not-registered Claude Team requesters** — Ali Elshaari, Alexander Balatsky, Vaishali Adya, Lukas Müllender. Worth a nudge to attend since they have/will have seats.

## Operational systems

### Hypha collections (`kth-sci` workspace)
| Collection | Purpose |
|---|---|
| `aphys-ai-gallery` | Use case gallery (30 AI + community submissions) |
| `aphys-ai-feedback` | "Is this useful?" widget feedback |
| `aphys-ai-pageviews` | Per-page persistent view counters |
| `aphys-ai-navigation` | Page-to-page transitions for analytics |
| `aphys-ai-registrations` | May 8 tutorial signups (43 unique) |
| `aphys-ai-claude-requests` | Claude Team seat requests (20 unique deduped) |
| `aphys-ai-community` | "Voices from Colleagues" + Tips |
| `aphys-ai-discussions` | Discussion topics with vote/subscribe system |

All have `rw+` permissions for `*` so anonymous edits work from the browser. Token in `.env` for admin operations.

### The daemon (`daemon.py`)
Running continuously (PID in `.daemon.pid`, log at `.daemon.log`). Polls every 30 seconds:
- Slack DMs from Jonas (D0ANKJFED8F) and Wei (D0AESV2LHQD) → relays to Svamp session via `svamp session send` with `--urgency urgent`
- Hypha collections for new gallery items, registrations, Claude requests, action requests from the admin "Send to Agent" button
- Detects status changes on Claude requests (pending → approved/rejected) → sends approval/rejection emails
- Email sending via Gmail SMTP if `SMTP_USER`/`SMTP_PASS` set, otherwise falls back to posting the email content to Wei + Jonas on Slack as "[Email pending — please send manually]"

**Restart command:**
```
kill $(cat .daemon.pid) 2>/dev/null
cd /Users/weio/workspace/applied-physics-ai
nohup python3 daemon.py >> /dev/null 2>&1 &
echo $! > .daemon.pid
```

### Admin dashboard
https://kth-sci.github.io/applied-physics-ai/admin.html — passphrase `aphys2026`. Tabs:
1. Page Views — analytics + navigation flow network
2. Page Feedback — thumbs up/down with comments + "Send to Agent" action button
3. Claude Requests — approve/reject Claude Team seat applications
4. Gallery Submissions — hide/highlight/edit user-submitted use cases
5. Community Messages — edit/delete/highlight community posts
6. Discussion Topics — vote stats + subscriber lists per topic
7. May 8 Attendees — registration table with stats by attendance mode

### Site pages
| File | URL | Owner |
|---|---|---|
| `docs/index.html` | / | landing |
| `docs/getting-started.html` | /getting-started.html | introduction |
| `docs/chatgpt-quickstart.html` | /chatgpt-quickstart.html | ChatGPT guide |
| `docs/ai-agents.html` | /ai-agents.html | Claude Code guide |
| `docs/gallery.html` | /gallery.html | use case gallery |
| `docs/events.html` | /events.html | event schedule |
| `docs/may-8-tutorial.html` | /may-8-tutorial.html | **detailed tutorial agenda** |
| `docs/slides/may-8-intro.html` | /slides/may-8-intro.html | **Wei's intro deck (scaffold)** |
| `docs/community.html` | /community.html | discussions + voices |
| `docs/admin.html` | /admin.html | admin dashboard |
| `docs/workshop-slides.html` | /workshop-slides.html | original Oct workshop proposal |

## Working style with Wei + Jonas

**Critical rules captured in memory** (`~/.claude/projects/-Users-weio-workspace-applied-physics-ai/memory/`):
- Always implement Jonas's Slack feedback immediately, then reply on Slack confirming what was done. Do not ask for clarification unless truly blocked.
- Respect the `feedback_design_preferences` memory — Tailwind CSS, no old-fashioned KTH-blue color schemes, modern indigo/slate, AI disclaimer in every footer, **never** use "Weio" — it's "Wei".
- All Slack message replies need to use `python3 -c` with `urllib.request` and the BCC token in the daemon code; the bot token is the same one used everywhere.

**Channels:**
- Jonas DM: `D0ANKJFED8F` (user `U0AM83MUH6V`)
- Wei DM: `D0AESV2LHQD` (user `U059XQJG518`)

**Github:**
- Repo: `kth-sci/applied-physics-ai`
- CI: `.github/workflows/deploy-pages.yml` builds Tailwind CSS via `@tailwindcss/cli` v4 and deploys `docs/` to GitHub Pages on every push to `main`.

## Recent work timeline (most recent first)

1. **Enrichment script for attendees + Claude requests** — `attendees/build_enriched_lists.py` regenerates `may8-attendees.{csv,txt}` and `claude-requests.{csv,txt}` from Hypha. Cross-check shows 16 of 20 requesters are May 8 attendees; 4 are not (worth nudging).
2. **Karpathy material added** to slide 4–6 + 9 of intro deck.
3. **Intro deck scaffolded** at `docs/slides/may-8-intro.html` (Reveal.js, 12 slides).
4. **May 8 sub-page created** at `docs/may-8-tutorial.html` with full agenda, "before you arrive", and follow-up resources sections.
5. **Welcome email template** at `attendees/welcome-email-template.md`.
6. **AI tutor prompt** at `attendees/chatgpt-tutor-prompt.md` for ChatGPT segment to bootstrap participants through Claude Code install.
7. **Confirmation email system** in daemon (Gmail SMTP w/ Slack fallback). Approval/rejection emails for Claude requests too.
8. **Multiple iterations of polish** on community page, admin dashboard, navigation flow visualization, registration cap (60 onsite), capacity footers per event.

## Things explicitly *not* done yet

- Jonas's ChatGPT segment slides (he may build these himself; or schedule them after he confirms format)
- The actual live demo dataset for the 14:15–14:45 segment (Jonas to pick a real APHYS task; pump-probe was discussed)
- Stuart McAndrew talk link (pending permission)
- The "wake-up demo" image/video for slide 3/4 of intro deck (Wei to pick)
- SMTP credentials in `.env` (waiting on Google's 24h propagation)
- Public attendee/Claude-request lists are gitignored content — `attendees/` is committed but contains personal email addresses; review whether this is appropriate before any wider sharing.

## How to pick up tomorrow

1. Read `CLAUDE.md` first.
2. Check daemon status: `kill -0 $(cat .daemon.pid) 2>/dev/null && echo running || echo stopped`. If stopped, restart per the command above.
3. Check for any unread Slack messages from Jonas — they should show up in the Svamp session via the daemon, but you can also poll directly:
   ```python
   import urllib.request, json
   req = urllib.request.Request('https://slack.com/api/conversations.history?channel=D0ANKJFED8F&limit=10',
       headers={'Authorization': 'Bearer ' + open('.env').read().split('SLACK_BOT_TOKEN=')[1].split('\n')[0]})
   print(urllib.request.urlopen(req).read().decode())
   ```
4. The `attendees/` files are the source of truth for who's coming and which Claude seats are needed.
5. The intro deck is incomplete — slides 3 (where AI is in 2026) and slide 4 still want a real visual demo or screenshot. Wei to pick one.
6. After May 8, debrief content goes into the gallery and community page; expect fresh feedback from attendees within 24h.
