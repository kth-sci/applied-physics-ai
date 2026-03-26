# Website Architecture

## Tech Stack
- **CSS Framework:** Tailwind CSS via CDN (`cdn.tailwindcss.com`)
- **Fonts:** Inter (body), JetBrains Mono (code) via Google Fonts
- **Icons:** Inline SVG throughout
- **Interactivity:** Vanilla JavaScript (no framework)
- **Backend for Gallery:** Hypha Artifact Manager REST API
- **Deployment:** GitHub Pages via GitHub Actions (deploys `docs/` folder)

## Color Palette
- KTH Blue: `#004791` (rarely used, kept for brand reference)
- Accent (primary): `#6366f1` (indigo-500) — used for nav, buttons, highlights
- Fire (secondary): `#f97316` (orange-500) — used for event highlights, agent badges
- Backgrounds: slate-900 (nav/footer), white (body), slate-50 (alt sections)

## Pages
| File | Purpose |
|------|---------|
| `index.html` | Landing page with overview, tools, gallery preview, events timeline |
| `getting-started.html` | Faculty intro, tool comparison, subscription guide, learning paths |
| `chatgpt-quickstart.html` | Prompt engineering guide, cheat sheet, interactive exercises |
| `ai-agents.html` | Claude Code intro, concepts, installation, examples, quiz |
| `gallery.html` | Dynamic use case gallery (fetches from Hypha collection) |
| `events.html` | Event schedule with countdown, May 8 featured, workshop slides link |
| `community.html` | Discussion topics, colleague tips, comment form |
| `workshop-slides.html` | Reveal.js presentation for October workshop proposal |

## Shared Components
- **Navigation:** Consistent across all pages, sticky top, slate-900 bg, mobile hamburger
- **Logo:** Atom + neural network SVG (science + AI fusion)
- **Footer:** Department info, organizer credits, AI-generated disclaimer
- **JS:** `assets/main.js` handles nav toggle, accordions, tabs, quiz, scroll reveal, code copy

## Hypha Integration
- **Server:** https://hypha.aicell.io
- **Workspace:** kth-sci
- **Collection:** `kth-sci/aphys-ai-gallery` (type: collection, public read, authenticated write)
- **Gallery fetch:** `GET /kth-sci/artifacts/aphys-ai-gallery/children?pagination=true`
- **Submission:** `POST /public/services/artifact-manager/create` with `parent_id`
- Credentials stored in `.env` (never committed)

## Key Design Decisions
1. Tailwind CDN (not build) for simplicity — no build step needed for static hosting
2. Inline styles for dynamically-generated cards (Tailwind CDN can't detect JS template classes)
3. Hypha for gallery backend — allows community submissions without a custom server
4. No framework (React/Vue) — keeps deployment trivial and pages fast
5. All content faculty-level — avoids beginner explanations, uses physics analogies
