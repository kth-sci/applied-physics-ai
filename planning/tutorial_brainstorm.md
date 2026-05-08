# May 8 Tutorial — Planning Brainstorm
**Captured from:** Voice conversation between Wei Ouyang and Jonas Sellberg  
**Date:** May 4, 2026  
**Status:** Working document — questions marked ❓ need follow-up from Wei/Jonas

---

## Event Basics (confirmed)

| Field | Value |
|-------|-------|
| Date | Thursday, May 8, 2026 |
| Time | 13:00–17:00 (4 hours) |
| Room | FB53, AlbaNova University Center |
| Capacity | 60 onsite + Zoom hybrid |
| AV | Projector confirmed, Zoom accessible |
| Attendees | ~32 registered (26 onsite, 6 Zoom); more PhD students expected once registration opens |
| Tools | ChatGPT (personal accounts) + Claude Code (team seats distributed before event) |

---

## Full Schedule
**⚠️ Updated May 5 — reverted to original split structure; coffee break at 14:30 confirmed**

| Time | Duration | Session | Owner | Format |
|------|----------|---------|-------|--------|
| 13:00 | 15 min | Arrival, setup, welcome | Wei + Jonas | Informal |
| 13:15 | 15 min | **Tutorial intro + general AI context** — labor market research, participant stats, why this matters | Wei + Jonas | Slides |
| 13:30 | 15 min | **ChatGPT intro** — prompting fundamentals, use cases | Jonas | Slides |
| 13:45 | 15 min | **ChatGPT hands-on** — groups try literature synthesis exercise | All | Group work |
| 14:00 | 15 min | **Claude Code intro** — what an AI agent is, surface-level | Wei | Slides |
| 14:15 | 15 min | **Claude Code hands-on** — groups explore a project folder or analyse data | All | Group work |
| 14:30 | 30 min | ☕ **Coffee break** — pastries, discussions | — | Fika |
| 15:00 | 15 min | **Jonas showcase** — building this event with AI: webpage, repo, first-time journey | Jonas | Live demo |
| 15:15 | 15 min | **Wei showcase** — AI agents in the lab: SVAMP, hardware control, research workflows | Wei | Live demo |
| 15:30 | 30 min | **Advanced user showcases** — Christian Ohm, Qichen Xu, Renan Maciel (~10 min each) | Ohm, Xu, Maciel | Demos + Q&A |
| 16:00 | 45 min | **Group work** — AI-generated mini-project task; coffee refill available | All | Group work |
| 16:45 | 15 min | **Presentations + wrap-up** — groups share results, closing words | Jonas + Wei | Short presentations |

---

## Session Details

### Opening Context Intro (Wei + Jonas, 15 min)
**Goal:** Set the stage. Not just "this is a useful tool" — this is a real structural shift.  
**Content:**
- The Anthropic labor market research (94% theoretical vs 33% actual coverage)
- Who is in this room: participant stats — experience levels, research areas (bar/pie chart, shown visually)
- "We're co-creating the learning environment for the future"
- Relevant to both students/postdocs (job market) AND faculty (teaching, research output)
- Frame: you have a window of advantage while adoption gap is still open
- Brief: who are Wei and Jonas, what is this tutorial about

**Tone:** Motivating but grounded. Not doom, not hype. Evidence-based.  
**Transition:** Seamless handoff between Wei and Jonas — no formal "now Jonas will speak"  
❓ **Q1:** Who opens — Wei or Jonas? Who covers which part of the research slide?

---

### ChatGPT Intro (Jonas, 15 min)
**Goal:** Practical prompting fundamentals — even beginners leave with 2–3 concrete techniques.  
**Content ideas (Jonas to finalize):**
- What ChatGPT is good at (and not good at)
- The prompting mental model: task + context + format
- Show 2–3 live examples (research-relevant, not generic)
- Frame: use ChatGPT as a thinking partner, not a search engine
- Mention: free accounts work; team seats also give Claude which we'll use next

**Exercise at end of slide deck:** specify exactly what participants should try  
❓ **Q2:** Jonas to specify the exercise prompt and example topic for the 15-min hands-on

---

### ChatGPT Hands-On (15 min, groups)
**Format:** Pre-specified exercise that works at beginner level, browser only, no install  
**Group size:** ~4–5 people per table (self-organized)  
**Zoom participants:** Do same exercise individually, type results in chat  
**Exercise (to be finalized):** Literature synthesis task using 3 provided abstracts — paste prompt into ChatGPT, iterate  
**Guided by:** Template prompt provided on tutorial webpage (so they can copy-paste)  
❓ **Q3:** Should Jonas pre-select 3 abstracts from an Applied Physics field, or let them use their own?

---

### Claude Code Intro (Wei, 15 min)
**Goal:** What is an AI agent, how Claude Code works at surface level. Not deep — just enough to try it.  
**Source material:** Stuart McAlpin's presentation from Stockholm/Oscar Klein Center (already pulled and adapted)  
**Key points:**
- Difference between chat and agent (already in slides)
- Agentic loop
- What it can see (files, terminal, web)
- Safety / permissions / Esc Esc to rewind
- ChatGPT stays useful: participants can use it to solve technical issues when Claude Code confuses them

**Exercise at end:** Added to slide deck  
❓ **Q4:** Should the Claude Code hands-on exercise be: (a) open-ended "try it on your own data" or (b) a specified shared task everyone does?

---

### Claude Code Hands-On (15 min, groups)
**Format:** Pre-specified exercise, Claude Code on laptop (or Claude.ai code artifacts as fallback)  
**Suggested exercise:** Give participants a small CSV dataset (provided), ask Claude Code to analyze it and generate a figure  
**Key point:** ChatGPT can help if they get stuck ("paste your error into ChatGPT")  
❓ **Q5:** Provide sample dataset from Applied Physics (spectra? image metadata?), or let them use their own?

---

### Jonas Showcase (15 min)
**Perspective:** First-time user — "this is how I experienced building the tutorial using AI"  
**Content:**
- Show the department AI webpage (live)
- Show the GitHub repository for this project
- Walk through how the page was built with AI assistance
- Frame: what surprised me, what was harder than expected, what I'd do differently
- Show organization structure for how they can set up their own projects

**Jonas's note:** "I will phrase it in a way because this is my first time... I will say any technical questions redirect to Wei"  
❓ **Q6:** Jonas — are there specific demos or moments from your experience you want to highlight?

---

### Wei Showcase (15 min)
**Content:**
- Agent management with SVAMP
- Lab hardware/instrument control via AI agent
- How Wei uses agents in research (writing papers, analyzing data, managing workflows)
- Show more advanced: what a fully-integrated AI workstation looks like
- Frame as: "here's what's possible when you go further"

❓ **Q7:** Wei — what specific hardware demos are feasible live? What SVAMP features to show?

---

### Advanced User Showcases (~30 min total)
**Who:** Jonas to email Christian Ohm, Qichen Xu, Renan Maciel  
**Ask:** "You registered as advanced. Would you like to showcase something for up to 15 min?"  
**Christian Ohm (priority):**
- Has built web pages with AI agents
- Has used local/free LLMs (not just commercial)
- Can demo local LLM setup on laptop → very interesting for many participants
- Suggested slot: ~15 min

**Others (Xu, Maciel):** If willing, ~5 min each to speak about their experience  
❓ **Q8:** Jonas — when will you send this email? (Ideally by May 5 to give them time to prepare)

---

### Advanced Hands-On — Mini-Projects (30–45 min, groups)
**Format:** Groups brainstorm and start building a small project using AI  
**How to start:**
- Provide a **brainstorming prompt** on the tutorial webpage — participants paste it into ChatGPT or Claude Code
- The prompt guides them to define a mini-project that is:
  - Achievable in 30 min
  - Related to their actual research, teaching, or admin work
  - Uses either ChatGPT or Claude Code (their choice)
- AI asks them: "What do you want to build? What data do you have? What's your goal?"

**Example starting ideas the agent can suggest:**
- Analyze a small dataset they brought
- Write a script that automates a repetitive task in their workflow
- Design a new assignment for a course they teach
- Draft an abstract or grant paragraph for a project they're working on

❓ **Q9:** Wei — should the brainstorming prompt enforce a specific output format for the wrap-up? (e.g., "produce 2 slides showing what you built and what you learned")

---

### Wrap-Up / Show-Off (15 min)
**Format:**
- 2–3 groups present voluntarily (not forced): 1–2 slides, ~5 min each
- Share GitHub link or Claude.ai conversation link in Zoom chat / Slack
- Wei moderates, Jonas facilitates discussion
- Collect submissions to use-case gallery (optional, via prompt they can run in Claude Code)

**Gallery submission:** Agent prompt provided on tutorial page → Claude Code submits to `aphys-ai-gallery` with tag `may8-tutorial`  
**Follow-up:** "More info will be added to the tutorial webpage after the event"  
❓ **Q10:** Should we ask them to email links, or post to a shared Google Doc, or just Zoom chat?

---

## Key Design Principles (from discussion)

1. **Surface level first, depth later** — the Claude Code intro should not go deep. Leave detail for them to explore themselves. "There's always more to talk about, just give the basic idea."
2. **ChatGPT as scaffold for Claude Code** — frame ChatGPT in Part 1 so participants use it to debug their Claude Code issues in Part 2.
3. **Show AI used to build the event itself** — meta-demonstration: participants see the workflow that created this tutorial. Connects motivation to practice.
4. **Co-creation, not execution** — second half shows AI as brainstorming partner, not just tool. "It's part of the co-creation process."
5. **Community building** — show participant stats at opening, let them see they're on a shared journey.
6. **No forced GitHub org setup during event** — too much friction with invitations and permissions. After event: ask participants to share links; optionally fork to org later.
7. **Tutorial webpage as single source of truth** — all exercise prompts, prep instructions, links, and follow-up resources live there. Email just links to it.

---

## Deliverables Needed

### Pre-event (by May 5–6)
- [ ] **Preparation email** — markdown template, send 1–2 days before; links to tutorial page
- [ ] **Tutorial webpage** (`docs/may8-tutorial.html`) — prep instructions, exercise prompts, brainstorming prompt, gallery submission prompt
- [ ] **Email to advanced users** — Jonas sends to Christian Ohm, Qichen Xu, Renan Maciel

### Slide decks
- [ ] **Opening context intro** (`may8-ai-context-intro.html`) — add participant stats slide (pie chart: experience, attendance)
- [ ] **ChatGPT intro** (`may8-chatgpt-intro.html`) — Jonas's 15-min deck + exercise slide ❓ Jonas to specify content
- [ ] **Claude Code intro** (`may8-claude-code-intro.html`) — add exercise slide at end ✓ already exists, just needs exercise
- [ ] **Jonas showcase** — slides for his 15-min second-half presentation ❓ Jonas to specify
- [ ] **Wei showcase** — slides for his 15-min agent/hardware demo ❓ Wei to specify
- [ ] **Wrap-up slide** — simple closing slide with follow-up info

### Exercise materials
- [ ] **ChatGPT exercise prompt** — template for 15-min hands-on (copy-paste into ChatGPT)
- [ ] **Claude Code exercise prompt** — template for 15-min hands-on
- [ ] **Brainstorming prompt** — for advanced hands-on mini-project session
- [ ] **Gallery submission prompt** — agent prompt that submits to `aphys-ai-gallery` via API

---

## Task Split Summary

| Task | Owner |
|------|-------|
| Opening context intro slides | Wei + Jonas jointly |
| ChatGPT intro slides + exercise | Jonas |
| Claude Code intro slides + exercise | Wei |
| Jonas showcase slides | Jonas |
| Wei showcase slides | Wei |
| Email to advanced users | Jonas |
| Tutorial webpage | Wei (+ agent) |
| Prep email template | Wei (+ agent) |
| Brainstorming prompt design | Wei (+ agent) |
| Gallery submission prompt | Wei (+ agent) |
| Sample datasets for exercises | Wei |

---

## Open Questions for Wei & Jonas

| # | Question | For |
|---|----------|-----|
| Q1 | Who opens the 13:00 session — Wei or Jonas? How do you want to split the 15-min context intro? | Both |
| Q2 | Jonas: What exactly should participants do in the 15-min ChatGPT hands-on? Which exercise topic? | Jonas |
| Q3 | Should Jonas pre-select 3 Applied Physics abstracts for the ChatGPT exercise, or let participants use their own? | Jonas |
| Q4 | Claude Code hands-on: open-ended (their own data) or specified shared task? | Both |
| Q5 | Sample dataset for Claude Code exercise: which field? (spectra, microscopy images, time-series?) | Wei |
| Q6 | Jonas: What specific moments from your AI journey with this project do you want to highlight in your showcase? | Jonas |
| Q7 | Wei: What hardware demos are feasible live? What SVAMP features will you show? | Wei |
| Q8 | Jonas: When will you email Christian Ohm, Qichen Xu, and Renan Maciel? | Jonas |
| Q9 | Should the brainstorming prompt enforce a specific output format for the wrap-up presentation? | Both |
| Q10 | How should participants share their wrap-up: email links, Google Doc, Zoom chat, or something else? | Both |
| Q11 | Tutorial webpage: does this replace the current events page entry for May 8, or is it a new separate page? | Both |
| Q12 | Should we open PhD student registration before May 8, or after? | Both |
