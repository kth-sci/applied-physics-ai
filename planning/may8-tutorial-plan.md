# May 8 Tutorial Plan — APHYS AI Agent Tutorial
**Date:** Thursday, May 8, 2026 | **Duration:** 4 hours  
**Venue:** AlbaNova (+ Zoom for 6 remote participants)  
**Leads:** Wei Ouyang + Jonas Sellberg  
**Audience:** 26 onsite, 6 Zoom — 32 total (12 beginners, 16 regular, 3 advanced)

---

## Goals

By the end, every participant should have:
- [ ] Held a productive back-and-forth conversation with Claude or ChatGPT on a real research task
- [ ] Produced one concrete output (synthesized literature, improved writing, generated code or a teaching idea)
- [ ] Made a personal commitment to one AI task in the next 2 weeks
- [ ] Understood the critical risks and limitations, not just the hype

---

## Audience Map

| Group | Who | Count | Strategy |
|-------|-----|-------|----------|
| Beginners | Senior profs: Vogt, Canalias, Pasiskevicius, Dutta, Lundström, Andersson, Burvall, Dendzik, Strandberg, Holmgren, Srambickal, Cao | 12 | Step-by-step, template prompts, no setup friction |
| Regular | Researchers/postdocs + Jonas Sellberg, Mats Persson, Martin Viklund | 16 | Hands-on autonomy, intermediate tracks |
| Advanced | Christian Ohm, Qichen Xu, Renan Maciel | 3 | Pair with beginners as table mentors; offer harder challenges |
| Remote | Yaqun Liu, Kritika Vijay, Stefan Wennmalm, Simone Mariani, Alexander Edström, Mariia Mohylna | 6 | Zoom-friendly tasks only; no group breakouts; shared doc for async participation |

---

## Timetable

### 09:00–09:30 — Welcome & Setup (30 min)
**Owner: Wei**

**Purpose:** Break the ice, verify everyone has working accounts, set expectations.

**Run of show:**
1. **09:00–09:05** — Welcome slide: "Today you will build something real."
2. **09:05–09:15** — Setup check (show of hands / Zoom poll):
   - Who has Claude.ai? ChatGPT? Claude Code?
   - Helpers (Christian Ohm, Qichen Xu, Renan Maciel) circulate for laptop fixes
   - Fallback: use claude.ai in browser — no install needed
3. **09:15–09:25** — 5-min live demo by Wei: "Watch what I can do in 3 minutes"
   - Take one real spectroscopy abstract → ask Claude to identify 3 knowledge gaps → ask it to suggest one experiment to fill the biggest gap
   - Goal: show the *pace* and *quality* possible, not just that it works
4. **09:25–09:30** — **Icebreaker exercise (Exercise 0):** Everyone types this prompt:
   > "I am [name], a [role] working on [one-sentence research description]. What are 3 specific ways AI agents could help me this month? Be concrete."
   - Share with neighbor; 2 Zoom participants read theirs aloud
   - **Output:** Personal relevance established

**Room setup needs:** Projector mirroring Zoom, helpers stationed at sides

---

### 09:30–10:30 — Module 1: Core AI Agent Skills (60 min)
**Owner: Wei (with Jonas supporting)**

**Purpose:** Teach the mental model of prompting — task, context, format, iteration.

#### 09:30–09:45 — Mini-lecture: "How to talk to an AI agent" (15 min)
Key concepts (keep slides minimal):
- **Task** = what you want done
- **Context** = background knowledge the AI doesn't have
- **Format** = how you want the output (table, bullet list, Python code, etc.)
- **Iteration** = the real skill — treating it as a conversation, not a search

Common mistakes to show live:
- Vague prompt → mediocre output → how to fix it
- Missing context → hallucination risk → how to mitigate

#### 09:45–10:10 — **Exercise 1: Literature Synthesis** (25 min)
*Works for all levels, all research domains*

**Task:** Each participant picks 3–5 abstracts from their own recent reading (or use provided examples if they don't have any ready).

**Template prompt to paste:**
```
Here are [N] abstracts from my research field.

[Paste abstracts here]

Please:
1. Identify the 3 main themes across these papers
2. Point out any contradictions or unresolved tensions
3. Suggest one research question that these papers don't yet answer
Keep your answer concise — one paragraph per point.
```

**Advanced variant (for Christian/Qichen/Renan):** Add a 4th step — "Draft a 150-word introduction paragraph that motivates a study addressing the gap you identified."

**Debrief (5 min):** 2 volunteers share their result. What was good? What was wrong or missing? → introduces the critical lens immediately.

#### 10:10–10:30 — **Exercise 2: Writing Assistant** (20 min)
*Choose one of three tracks — participants self-select*

**Track A — Grant / impact writing (beginners + professors):**
```
Here is a description of my research:
[2–3 sentences about their work]

Write a 200-word impact paragraph for a grant application. 
The audience is a funding panel with general science background, not specialists.
Emphasise societal relevance and novelty. Avoid jargon.
```

**Track B — Abstract improvement (regulars):**
> Paste your actual paper abstract → ask Claude to identify weak sentences, improve clarity, tighten to 150 words, then ask it to explain every change it made.

**Track C — Structured thinking (advanced):**
> "I'm designing a study to [goal]. Help me build a 5-step experimental plan. For each step, list: what could go wrong, what data I need, and one alternative approach."

**Key takeaway to say out loud:** "You didn't just get text — you got a thinking partner who never gets tired and never judges your draft."

---

### 10:30–10:45 — Break (15 min)

---

### 10:45–11:45 — Module 2: AI for Your Research Domain (60 min)
**Owner: Wei (Jonas circulates)**

**Purpose:** Apply AI to domain-specific tasks — data, code, figures, analysis.

#### 10:45–11:00 — Demo: Claude Code in 10 minutes (15 min)
Wei does a live walkthrough, screen-shared to Zoom:
1. Open Claude Code in terminal (or show via browser tool)
2. Drop in a small CSV dataset (spectroscopy or microscopy data)
3. Ask: "Analyze this data: find peaks, plot them, write a summary"
4. Show the output file/figure appearing — emphasize **no manual coding required**

*Zoom participants: share screen if possible, or follow on their own laptops*

#### 11:00–11:35 — **Exercise 3: Domain Task** (35 min)
Three parallel tracks — participants choose based on comfort level.

**Track A — "The AI Research Assistant" (beginners, browser only)**
Pick one task:
- Ask Claude to explain a concept from their field that a new PhD student always struggles with → use the output to draft a tutorial blurb
- Ask Claude to generate 5 peer review questions they would ask about a paper in their area
- Ask Claude to write a 3-email sequence for onboarding a new lab member

**Track B — "Code & Data" (regular, Claude.ai code artifacts)**
Using Claude.ai's built-in code tool (no install):
```
I have [describe your data: e.g. "time-resolved fluorescence decay curves as a CSV 
with columns: time_ns, intensity"]. 
Write Python code that:
1. Loads the data
2. Fits an exponential decay (or relevant model for your data)
3. Plots the result with axis labels and a legend
4. Prints the fit parameters with uncertainties
```
Participants use their own data description or pick from provided sample datasets.

**Track C — "Claude Code Workflow" (advanced)**
On their own laptops with Claude Code installed:
- Design a multi-step agent workflow for a real analysis task in their lab
- Alternatively: use the MCP file tools to let Claude read and modify a Jupyter notebook

#### 11:35–11:45 — Share-out (10 min)
- 3 volunteers (one per track) show their screen for 2 minutes each
- Jonas facilitates: "What surprised you? What didn't work?"
- Zoom: one remote participant shares theirs

---

### 11:45–12:15 — Module 3: AI and Teaching (30 min)
**Owner: Jonas Sellberg**

**Purpose:** Address the urgent disruption AI creates for assessment and pedagogy.

#### 11:45–11:55 — Framing: The Assessment Crisis (10 min)
Jonas presents (no more than 5 slides):
- What a student can do today with ChatGPT/Claude on a standard physics exam
- The three traps: detection, banning, ignoring
- The shift: from testing recall → testing judgment, design, reflection
- One inspiring example: an assignment that AI makes *better*, not easier to cheat

#### 11:55–12:10 — **Exercise 4: Assignment Redesign** (15 min)
*Even Zoom participants can do this fully*

**Part 1 — AI audit (5 min):** Each person thinks of one assignment they give. Type:
```
Here is one of my course assignments:
[Describe the assignment in 2–3 sentences]

How would a student use Claude or ChatGPT to complete this with minimal effort?
What would be easy to do with AI? What would still require genuine understanding?
```

**Part 2 — Redesign (10 min):**
```
Now suggest 3 ways I could modify this assignment so that:
- AI use becomes a tool the student must use *critically*, not a shortcut
- The assignment still tests deep understanding of [topic]
- It could work for a class of [N] students with limited TA support
```

Share: Jonas picks 2–3 to discuss briefly with the group.

#### 12:10–12:15 — Discussion point (5 min)
One provocation Jonas puts to the room:
> "If your PhD students can use AI for 80% of their routine tasks, what is the remaining 20% that defines their scientific contribution?"

No need to resolve — plant the seed for the October workshop.

---

### 12:15–12:30 — Wrap-up & Action Commitments (15 min)
**Owner: Wei + Jonas**

#### 12:15–12:22 — Resources & next steps (7 min)
- Show the department AI webpage (live, on projector)
- Highlight: use-case gallery, getting-started guides, Claude Team seat request
- Next event: May 26 hackathon (call for sign-ups)
- Point to the AI Tutor Prompt for self-directed learning after today

#### 12:22–12:30 — Personal commitments (8 min)
Each person (or table group of 4) writes down:
> "In the next 2 weeks, I will use AI to [specific task] in my [research/teaching/admin] work."

Collect via a shared Google Doc or typed into a Zoom chat (remote participants post in chat).  
Wei reads 3–4 aloud. Close with energy — this is day 1 of a longer journey.

---

## Logistics Checklist

### Before May 8
- [ ] Send setup email (by May 5) — accounts + Claude Code install instructions
- [ ] Prepare sample datasets: one spectroscopy CSV, one image metadata CSV, one time-series CSV
- [ ] Prepare "starter abstracts" pack (5 Applied Physics abstracts) for participants who don't have their own
- [ ] Brief the 3 advanced participants (Ohm, Xu, Maciel) as table mentors
- [ ] Set up Zoom with screen share for live demos
- [ ] Print prompt templates as handout (optional but useful for beginners)
- [ ] Prepare shared Google Doc for commitments

### Day-of Setup
- [ ] Test Claude.ai, ChatGPT in the room browser
- [ ] Test projector + Zoom screen share
- [ ] Have helpers arrive 20 min early to assist with account setup
- [ ] Ensure AlbaNova wifi password is posted visibly

### Fallback Plans
- If Claude.ai is slow: switch to ChatGPT (same exercises work)
- If someone has no account: pair them with neighbor, have pre-loaded conversation examples to demo
- If Zoom audio fails: type exercises shared in Zoom chat

---

## Key Design Choices

**Why no pure lecture?** This audience learns by doing, not by watching slides. Every 15-minute block has a hands-on component.

**Why self-selected tracks?** Forcing beginners to do Claude Code and advanced users to do basic prompting wastes both groups. Self-selection maintains energy.

**Why physics examples throughout?** Builds credibility that AI is genuinely useful in their domain — not just for writing or coding in general.

**Why teaching module?** This is the most urgent pain point for senior faculty — they need to address AI in their courses NOW, and they came partly for this.

**Why written commitments at end?** Research on behavior change shows that specific, written plans dramatically increase follow-through compared to general intent.

---

## Materials Needed

| Item | Who prepares | Status |
|------|-------------|--------|
| Setup email | Wei | TODO |
| Slide deck (5 modules) | Wei + Jonas | TODO |
| Sample datasets (3x CSV) | Wei | TODO |
| Starter abstracts pack | Jonas | TODO |
| Prompt template handout | Wei | TODO |
| Shared commitment doc | Wei | TODO |
| Zoom link | Admin | TODO |
| AlbaNova room booking | Admin | Confirmed |
