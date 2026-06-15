# Source notes — APHYS Teachers' Meeting, June 2026

Material backing the slide deck at `docs/slides/teachers-meeting-jun-2026.html`. Keep this file the canonical source of truth so handouts stay consistent.

## Programme context (from Uli's emails)

Week 24, June 8-12, 2026. Programme:
- Hour 1: general GRU info (Uli)
- Hour 2: AI resilience questionnaire results (Uli)
- Hour 3: SCI AI Hackathon teaching outcomes (Jonas + Wei)
- Last 30 min: Olle Bälter (invited speaker)

So Wei + Jonas share ~30 min before Olle. Wei runs intro/framing; Jonas covers his autograder from the Agenthathon + Canvas / LearnWise + other initiatives. Plan to meet ~30 min before to align.

## Slide-by-slide sources

### Slide 2 — Inflection point
- **Karpathy 80% / December 2025 step change** — Sequoia AI Ascent 2026 (March 2026); summary at karpathy.bearblog.dev/sequoia-ascent-2026. Paraphrased.
- **SWE-bench Verified 1.96% → ~78%** — public leaderboard timeline; Anthropic's "Measuring AI Agent Autonomy in Practice" (2026).
- **~2× autonomous turn duration** — same Anthropic paper, Oct 2025 → Jan 2026 99.9th-percentile.
- **80% of Anthropic production code authored by Claude** — VentureBeat, 2026.

### Slide 3 — The new engineering
- All three concepts (context engineering, loop engineering, aligned understanding) from the SCI Agenthon Track C reading: https://kth-sci.github.io/sci-agenthon-2026/advanced.html
- Pull-quote "what should Claude know?" — verbatim from that page.

### Slide 4 — Concrete demos
- **AlphaEvolve / Strassen** — DeepMind blog, "AlphaEvolve: a Gemini-powered coding agent for designing advanced algorithms", May 2025. 4×4 complex matrix multiply in 48 scalar multiplications; first improvement on Strassen since 1969.
- **Plummer / PDP-11 transformer** — Tom's Hardware, 2025. Mini-transformer in PDP-11 assembly on a 1978 6 MHz / 64 KB machine. Dave Plummer = ex-Microsoft, Windows Task Manager creator, "Dave's Garage" YouTube channel.

### Slide 5 — Empirical teaching picture
- **Wang et al., Nature Humanities & Social Sciences Communications 2026** — 35 experimental studies meta-analysis, g = 0.67.
- **Liu et al., Journal of Computer Assisted Learning 2025** — large positive performance effect on student outcomes (Wiley).
- **HEPI Student Generative AI Survey 2026** — Higher Education Policy Institute, UK undergraduate AI use data.
- **"No real learning gains" framing** — paraphrased from 2026 systematic-review literature. (Hedge: I do not have a single canonical citation; treat as a frame, not a quote.)
- **Retracted Nature HSSC meta-analysis** — one earlier high-profile meta was retracted in 2025; useful to mention as evidence the field is messy.

### Slide 6 — Institutional positions
- **ASU** — tech.asu.edu/node/1232406, ChatGPT Edu with GPT-5 site-wide, Oct 2025.
- **Cal State $13M** — CalMatters and NPR (May 2026); 22 campuses; documented organized faculty + student refusal.
- **OECD Digital Education Outlook 2026** — OECD, June 2026; paraphrased framing.
- **Nature "AI university" column** — Nature d41586-025-03950-4, Dec 2025.

### Slide 7 — Junior career squeeze
- Entry-level hiring at 15 largest tech firms down 25% from 2023 to 2024 — Stack Overflow Blog (Dec 2025).
- Junior dev postings down ~40-50% since early 2024 — Stack Overflow Blog (Dec 2025).
- Devs aged 22-25 employment down ~20% from late-2022 peak — SSRN paper by Zachary Adam (2026).
- LeadDev 2025 survey, 54% will hire fewer juniors — LeadDev annual engineering leaders survey.
- IBM tripling US entry-level hiring in 2026 — IBM press release / Bloomberg coverage. (Counter-data point.)

### Slide 8 — Inequality + skills
- "Student < AI alone < Student + AI" — Wei's framing; consistent with the existing community page voices on the APHYS AI site.
- Pull-quote "outsource your thinking but not your understanding" — Karpathy, late 2025, attributing to a conversation. Already used on the May 8 deck and the community page.

### Slide 9 — Discussion seeds
- Five open questions, no answers. Designed to seed a 15-20 min open discussion. Wei to facilitate.

## Tone / framing notes

- Senior faculty audience &mdash; they will tune out hype on the first overstatement. Cite by name, with year, and only the claims I would defend under push-back.
- Wei's specific concern (from the Slack request): students need to be better than AI, not equivalent to it. The whole arc lands at the "Student + AI > AI alone" inequality.
- Discussion is the goal, not advocacy. Slide 9 must feel like "here are the questions" not "here is what we should do."
- Hand-off slide 10 puts Jonas on for the operational details (autograder, Canvas, May 8 / hackathon outcomes). Don't pre-empt that material.

## Pull-quotes I considered but did not use

- "Code is free as in puppies." (advanced.html) — too inside-baseball for this audience.
- "Demo is works.any(), product is works.all()." (advanced.html) — same.
- "2025 is the year of agents. This is the decade of agents." — true but borderline hype-y.
- The Spotify CTO "haven't written a line of code since December 2025" — flagged in research as anecdotal. Kept out of the slides; mention only if the audience pushes for an industry quote.
