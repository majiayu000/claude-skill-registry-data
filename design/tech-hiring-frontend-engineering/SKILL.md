---
name: "tech-hiring-frontend-engineering"
description: "Frontend engineers build the interfaces users interact with: web applications, design systems, client-side performance, accessibility, and the bridge between design and engineering. Full-stack signals are common — look for proficiency on bo"
---

# Frontend Engineering — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Frontend Engineering

### What This Role Does
Frontend engineers build the interfaces users interact with: web applications, design systems, client-side performance, accessibility, and the bridge between design and engineering. Full-stack signals are common — look for proficiency on both sides where required.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Junior Frontend Engineer, Junior UI Developer, Junior Web Developer |
| Mid | Frontend Engineer, UI Engineer, Web Developer, React Developer |
| Senior | Senior Frontend Engineer, Senior UI Engineer, Lead Frontend Engineer |
| Staff+ | Staff Frontend Engineer, Principal Engineer, Frontend Architect |
| Full-stack variant | Full-Stack Engineer, Software Engineer (Next.js / Nuxt / Remix) |
| Specialist | UI Platform Engineer, Design Systems Engineer, Web Performance Engineer |

### Skill Tiers

**Tier 1 — Must-have:**
- JavaScript (ES2020+) — deep understanding, not just "I've used React"
- TypeScript — increasingly non-negotiable for mid and above
- React, Vue, or Angular (one deeply, others surface-level)
- CSS: layout (Flexbox, Grid), responsive design, browser compatibility
- HTTP, REST API consumption, async/await, state management

**Tier 2 — Differentiator:**
- Next.js / Nuxt / SvelteKit (SSR, SSG, ISR)
- State management: Redux, Zustand, Jotai, React Query
- Testing: Jest, Vitest, React Testing Library, Playwright, Cypress
- Accessibility (WCAG 2.1 AA) — increasingly a hiring filter
- Web performance: Core Web Vitals, lazy loading, bundle optimisation
- Build tools: Vite, Webpack, Turbopack

**Tier 3 — Bonus:**
- WebAssembly (WASM)
- WebGL / Three.js / data visualisation (D3.js, Recharts)
- Design system authorship (Storybook)
- Svelte / SolidJS / Qwik
- Open source UI library contributions

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("frontend engineer" OR "UI engineer" OR "React developer" OR "web developer") (React OR Vue OR Angular OR TypeScript OR "Next.js") -recruiter -talent -jobs

# Senior specialist
site:linkedin.com/in/ ("senior frontend" OR "frontend architect" OR "design systems") (TypeScript OR "design system" OR accessibility) -recruiter

# GitHub — active frontend engineers
language:javascript followers:>25 pushed:>2025-01-01
language:typescript followers:>25 pushed:>2025-01-01

# GitHub — React/TypeScript specifically
site:github.com "joined on" (React OR "Next.js" OR TypeScript) (frontend OR UI OR "web developer") -template -jobs
```

### Seniority Signals

- **Junior → Mid:** Stops copying patterns without understanding them; can debug browser quirks independently
- **Mid → Senior:** Proactively raises accessibility, performance, and cross-browser concerns; influences design decisions
- **Senior → Staff:** Owns the frontend platform, establishes patterns for the team, reduces toil through tooling
- **Full-stack signal:** They've shipped production Next.js or Nuxt apps, including auth, API routes, and data fetching strategy — not just "I've done some Node"

### Interview & Assessment Loop

| Stage | Format | What you're assessing |
|---|---|---|
| Technical screen | 45 min, JS/TS fundamentals + small component | Core language understanding, not just framework knowledge |
| Take-home | Build a small feature (2–3 hours) | Code quality, CSS craft, accessibility awareness, test coverage |
| Live review | Walk through their take-home | Decision reasoning, how they handle feedback |
| System design | Frontend architecture (component design, state, data fetching) | Senior+ only — scale thinking for UI |
| Behavioural | STAR questions | Collaboration with designers, handling product ambiguity |

**Watch for:** Candidates who know the framework but not the language. Ask "what does `this` mean in JavaScript?" or "walk me through the event loop" — senior frontend engineers should answer confidently.

### Red Flags
- Can only work in one framework, has no JS fundamentals
- No understanding of accessibility ("the designers handle that")
- Never written a test in any frontend context
- Portfolio is only tutorials or cloned apps
- Dismissive of performance ("modern hardware handles it")
- Resume lists 15 frameworks superficially — depth matters more than breadth

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $85k – $125k |
| Mid | $125k – $165k |
| Senior | $150k – $210k |
| Staff | $190k – $260k |
| Principal | $230k – $310k+ |
