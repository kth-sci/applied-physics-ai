# Applied Physics AI — Project Instructions

## Project Overview

This repository is the central hub for the **Applied Physics Department AI Initiative** at the School of Engineering Sciences, KTH Royal Institute of Technology. The initiative is led by **Wei Ouyang** and **Jonas Sellberg**.

### Vision

Empower faculty, researchers, and staff within the Department of Applied Physics (and across the School of Engineering Sciences) to adopt AI — specifically **AI agents** — as tools for research, teaching, productivity, and everyday academic work. The initiative promotes critical understanding alongside practical fluency: knowing when and how to use AI, and equally when not to.

### Primary Goals

1. **AI Agent Adoption** — Guide faculty to use AI agents (Claude, ChatGPT, coding assistants) for research workflows, data analysis, literature review, grant writing, and daily productivity.
2. **Teaching & Education** — Address the urgent disruption AI poses to traditional assessment and teaching. Help educators redesign courses, assignments, and pedagogy for the AI era.
3. **Training Series** — Deliver a structured sequence of events (tutorials, hackathons, workshops) that build competence progressively across the department and school.
4. **Internal AI Webpage** — Build and maintain a department-facing webpage (GitHub Pages) that serves as a resource hub: guides, tutorials, event information, tools, and ethical discussion materials.
5. **Ethical & Societal Awareness** — Foster open discussion about AI's impact on education, junior career paths, scientific integrity, and society.

### Design Philosophy

- **Agent-first**: AI agents are the primary interface for learning and doing — not traditional lectures or textbooks.
- **Physics-grounded**: All examples and exercises use Applied Physics contexts (spectroscopy, microscopy, materials, time-resolved measurements).
- **Personalized**: The AI Tutor Prompt adapts to each participant's research area, background, and level.
- **Action-oriented**: Every event produces concrete outputs — working prototypes, redesigned assignments, personal action commitments.
- **Critical**: Always show both capabilities and limitations. Domain knowledge > black-box tools.

## Repository Structure

```
applied-physics-ai/
  CLAUDE.md              # This file — project context and agent instructions
  .gitignore             # Git ignore rules
  docs/                  # GitHub Pages source (internal webpage)
    index.html           # Landing page
    ...
  ai-workshop-2026/      # Submodule/subfolder — workshop planning materials
    CLAUDE.md            # Workshop-specific context
    context.md           # Background and origin story
    key-ideas.md         # Design rationale
    jonas-proposal.md    # Jonas's pedagogical framework
    plan.md              # Detailed workshop plan
    workshop-plan.md     # Session-by-session blueprint
    schedule.md          # Timeline of all 2026 events
    tasks.md             # Preparation checklist
    slides/              # Reveal.js presentation
    figures/             # Gantt chart and visuals
  AI-slides-v2.html      # Standalone workshop proposal slides
```

## Key Context

### Origin Story

The Engineering Mechanics department at KTH organized a successful 3-day AI/ML retreat. A handover meeting on Feb 18, 2025 (Wei, Jonas, Fredrik, Artem, Marco) identified that Applied Physics needs a different approach:
- Faculty already have strong quantitative backgrounds — less need for ML math derivations
- The biggest gap is **practical AI tool usage**, not theory
- AI agents have changed everything since the original retreat
- The urgent crisis is AI's **impact on teaching and learning**

### 2026 Event Timeline (Tentative)

| Date | Event | Leads |
|------|-------|-------|
| May 8, 2026 | APHYS AI Agent Tutorial (faculty, 4h) | Wei + Jonas |
| May 26, 2026 | SCI AI Agent Hackathon (faculty, full day) | Fredrik + Wei + Jonas |
| June 15, 2026 | APHYS Teachers' Meeting — AI in Teaching | Wei + Jonas |
| October 2026 | APHYS 2-Day Workshop (deep technical) | Wei + Jonas |

### Key Stakeholders

- **Wei Ouyang** — Project lead, AI agent focus, teaching disruption, internal webpage
- **Jonas Sellberg** — Pedagogical framework, physics-grounded examples, cross-division design
- **Fredrik** — School-level coordination, hackathon co-lead
- **Artem, Marco** — Advisory, handover meeting participants

### Department Divisions (for cross-cutting examples)

- **BON** — Biomedical and X-ray Physics (X-ray/optical imaging, visual optics, nanochemistry)
- **Biophysics** — Cell morphology, microscopy, protein modeling
- **LAMP** — Light and Matter Physics (ultrafast spectroscopy, optical communication, spintronics)
- **Quantum and Nano Physics** — Nanostructures, nonlinear/quantum photonics

## Hypha Integration

The use case gallery connects to the Hypha artifact manager for dynamic content.

- **Server:** `https://hypha.aicell.io`
- **Workspace:** `kth-sci`
- **Collection alias:** `aphys-ai-gallery`
- **Credentials:** stored in `.env` file (never commit this)
- **API pattern:** `https://hypha.aicell.io/kth-sci/artifacts/aphys-ai-gallery/children?pagination=true`

## Tech Stack

- **CSS framework:** Tailwind CSS v4 (pre-built via `@tailwindcss/cli`, NOT CDN)
- **Fonts:** Inter (Google Fonts)
- **Icons:** Inline SVG
- **Interactivity:** Vanilla JavaScript
- **Backend:** Hypha artifact manager (REST API)
- **Deployment:** GitHub Pages via GitHub Actions (builds CSS + deploys `docs/`)

## Community Daemon (`daemon.py`)

A continuously-running Python process that monitors external events and relays them to the active session.

### What It Monitors

| Source | What | Action |
|--------|------|--------|
| Slack DMs from Jonas | Feedback, site update requests | Relay to session via `svamp session send` |
| Slack DMs from Wei | Instructions, requests | Relay to session via `svamp session send` |
| Hypha gallery | New use case submissions | Notify Wei+Jonas on Slack + relay to session |

### How It Works

- Polls Slack conversations API every 30 seconds for new messages
- Polls Hypha artifact children endpoint for new gallery items
- Tracks state in `.daemon_state.json` (last seen timestamps, known artifacts)
- Sends alerts to session via `svamp session send <session-id> <message>`
- Notifies organizers on Slack when new submissions arrive

### Management

```bash
# Start the daemon
cd /Users/weio/workspace/applied-physics-ai
nohup python3 daemon.py >> .daemon.log 2>&1 &
echo $! > .daemon.pid

# Check status
cat .daemon.pid | xargs kill -0 2>/dev/null && echo "Running" || echo "Stopped"

# View logs
tail -30 .daemon.log

# Stop
kill $(cat .daemon.pid)

# Restart
kill $(cat .daemon.pid) 2>/dev/null; nohup python3 daemon.py >> .daemon.log 2>&1 & echo $! > .daemon.pid
```

### Files
- `daemon.py` — The daemon script
- `.daemon.log` — Stdout/stderr log (gitignored)
- `.daemon.pid` — PID file (gitignored)
- `.daemon_state.json` — Persisted state (gitignored)

## Agent Instructions

When working on this project:

1. **Treat all plans and schedules as tentative** — dates, formats, and content are evolving. Do not assume anything is final.
2. **The internal webpage (docs/) is the current primary deliverable** — focus effort here when asked about the webpage.
3. **Maintain consistency** with the design philosophy above: agent-first, physics-grounded, personalized, action-oriented, critical.
4. **Use modern design:** Tailwind CSS, clean typography, good contrast, subtle animations only.
5. **Content should serve faculty and researchers** — the audience is senior academics, not students.
6. **Respect the dual focus**: practical AI fluency AND critical awareness of AI's societal impact.
7. **All pages include disclaimer** that the site is AI-generated and may contain errors.
