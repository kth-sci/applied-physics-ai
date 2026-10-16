# Handoff — APHYS AI Initiative

Context for the next agent session. **Last updated 2026-10-16.**

Read `CLAUDE.md` first for project vision, design philosophy, repo layout, and
standing agent instructions. This file covers current state and open threads.

---

## Imminent — APHYS AI Retreat, Oct 21–22 (five days out)

Two-day residential retreat at Skytteholm Hotell & Konferens, Ekerö. Bus from
Brommaplan 08:30 on 21 Oct, returning 13:30 on 22 Oct. ~30 APHYS faculty.
Organisers: Jonas Sellberg + Wei Ouyang.

- **Agenda:** published on `docs/events.html` (featured block + full schedule
  card) and in `EVENTS.md`. Source PDF: `planning/APHYS-AI-Retreat-2026-Agenda260914.pdf`.
- **Planning repo:** https://github.com/kth-sci/aphys-ai-retreat-2026
  (`PLAN.md`, `LOGISTICS.md`, `TASKS.md`).

### Flagged: the agenda is still labelled a draft

The circulated PDF says *"the final agenda will be published in early October."*
It is 16 October and both the site and `EVENTS.md` still carry the
"Draft agenda — for review" badge and the amber "circulated for comment" notice.
Either the final agenda needs publishing or the wording needs changing before
participants arrive. **Ask Wei or Jonas which.**

### Retreat deliverables named in the agenda, status unknown

None of these were tracked in this session — verify before assuming they exist:

1. **Printed cheat sheet** for Session 1, to be sent as a pre-read (GitHub
   basics, how to get AI access at APHYS, anatomy of a skill, worked tutorial).
   The AI-access part can be lifted from `docs/ai-agents.html`.
2. **Pre-work ask for Session 2** — every participant brings one concrete case,
   including things that did not work. Needs to go out before the 21st.
3. **Hackathon groups** — five topics, ~six people each, deliberately mixing
   newcomers with experienced users.
4. **$3,000 API token budget**, allocated per group.
5. **DGX Spark** brought on site for the local-model track.
6. **Keynote speaker** — external, industrial perspective. "To be announced
   once confirmed"; no name on file here.
7. **Shared repository** for the `SKILLS.md` commits each group must make.
   Which repo this is has not been decided — `aphys-ai-retreat-2026` is the
   obvious candidate but nothing has been set up.
8. **Skeleton guidelines document** drafted in advance, so Session 4 edits a
   real draft rather than a blank page.

---

## Repositories

| Repo | Purpose | State |
|------|---------|-------|
| `kth-sci/applied-physics-ai` | Initiative hub + public site (this repo) | Active |
| `kth-sci/aphys-ai-retreat-2026` | Retreat planning (created 2026-09-04) | 2 commits, in sync |
| `kth-sci/ai-workshop-2026` | March 2026 scoping for the same retreat | Stale since Mar 26 |
| `kth-sci/applied-physics-ai-internal` | Budget, participants, internal docs | Private |

**Unresolved:** `ai-workshop-2026` holds the original planning for this retreat
(`plan.md`, `workshop-plan.md`, `jonas-proposal.md`, Gantt figure) and predates
the May and June events. Wei was asked whether to migrate the still-valid parts
and archive it; no decision yet.

---

## Infrastructure state

### Community daemon (`daemon.py`)

Running under svamp as `aphys-daemon` (`svamp process list`). Polls Slack and
Hypha every 30 s; sends confirmation emails; relays to a session.

Three things were fixed in August and are worth knowing about:

- **Single-instance lock.** Four daemons were once running in the same
  directory, racing on the shared state file — one test request produced four
  emails. `daemon.py` now takes an exclusive `flock` on `.daemon.lock`; a second
  instance logs and exits. Do not work around this.
- **Send-once ledger.** Every email goes through `send_email_once(state, key, …)`
  with keys like `claude:<alias>:approved`, persisted in `.daemon_state.json`.
- **Organizers are always Bcc'd** (Jonas, Wei), deduped against the To line.

### Two known breakages — neither fixed

1. **`SLACK_BOT_TOKEN` is not set anywhere** — not in `.env` (which holds only
   SMTP credentials), not in the environment, not in the running process. Every
   `slack_post` returns `not_authed`, so Slack monitoring and organizer
   notifications are silently inert. Email is unaffected.
2. **`SESSION_ID` in `daemon.py` is hardcoded to `53be87cd-…`, which no longer
   exists.** Session relays go nowhere. Update it to the live session ID, or
   better, read it from the environment.

Together these mean the daemon's Slack relay path is entirely dead. Jonas and
Wei have been reaching the agent through the Svamp participants channel instead,
which is why it went unnoticed for months.

### Email

Gmail SMTP from `kth.aphys.ai@gmail.com`; credentials in `.env` (never commit).
`send_email.py` is the general-purpose CLI — see `HANDOFF-EMAIL-AGENT.md` and
`CLAUDE.md` for templates and usage. `--dry-run` works and shows the Bcc list.

`send_tutorial_email.py` is a one-off blast for May 8 with 43 hardcoded
addresses. It now refuses to run after its event date; override only
deliberately with `--i-know-this-event-has-passed`.

The registration confirmation email in `daemon.py` is specific to May 8 and is
**skipped automatically** once `TUTORIAL_DATE` has passed. If retreat
registration ever runs through Hypha, rewrite that template and bump
`TUTORIAL_DATE` — note its "Claude Team seat at no cost" promise no longer
matches the eligibility rules.

---

## Site state

Deployed from `docs/` by GitHub Actions, which rebuilds Tailwind CSS on push —
new utility classes are fine, no local build needed (but `npx @tailwindcss/cli
--input docs/assets/input.css --output docs/assets/style.css --minify` works
locally for checking).

Recent substantive changes, newest first:

- **2026-10-14** — model, plan and system-requirement facts refreshed sitewide
  against `code.claude.com/docs/en/setup`, `claude.com/pricing` and the OpenAI
  model docs. Corrected a wrong claim that Claude Code needs a plan above Pro
  (every paid plan includes it); GPT-5.4 → GPT-6 Sol; added a system
  requirements block; desktop app is on Linux; Git for Windows is optional.
- **2026-09-14** — Oct 21–22 retreat set as the Next Event at the top of
  `events.html` and `index.html`; all earlier 2026 events greyed and flagged
  Past Event.
- **2026-09-01** — group-leader Claude Team license (Claude for Science) added
  as the primary route to Claude Code, with a request button to the Google Form
  and a note about the KTH-email workaround.
- **2026-08-19** — Claude Team seat requests restricted to permanent staff
  (≥50 % FTE); non-permanent staff directed to their group leader.

### Deliberately left alone

- **Past-event material** (`may-8-tutorial.html`, `workshop-slides.html`,
  `docs/slides/`, `docs/may-8th-tutorial/`) is a record of what was taught on
  the day. Do not "update" model names there — it falsifies the record.
- **Unverified local claims:** "ChatGPT Plus included in KTH procurement" and
  "GitHub Copilot free for academics" on `getting-started.html`. These are
  procurement facts no vendor doc can confirm; check with the license admin
  (`licensadmin-sci@kth.se`) before relying on them.
- `computeExpiration()` in `docs/admin.html` still has post-doc/PhD branches so
  previously approved seat requests keep computing correctly.

---

## Uncommitted / loose ends

- `planning/APHYS-AI-Retreat-2026-Agenda260914.pdf` is **untracked**. Its
  content is already summarised on the public site. Committing it would publish
  the PDF in a public repo — ask before doing so.

---

## Working with Jonas and Wei

- Jonas sends requests through the Svamp participants channel. Execute them
  closely; he gives precise wording and expects it preserved. When copy-editing
  his text for the page's voice, say so.
- Both are senior academics with strong quantitative backgrounds. Cite by name
  and year; only claims that survive push-back.
- Treat plans and dates as tentative unless confirmed — except the retreat
  dates, which are fixed.
- Every page carries the AI-generated disclaimer. Keep it.
