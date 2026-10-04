---
name: idea-loop
description: >
  Autonomous idea-to-complete-app loop. Give it any seed — one sentence, a vague concept, a complex app idea — and it iterates through brainstorm → think → spec → plan → build phases without stopping until a complete, production-ready deliverable is produced. Trigger on phrases like "loop this", "run the full loop", "take this idea all the way", "build this from scratch", "make a complete app from", or any idea given without further instruction when the user wants autonomous end-to-end execution. Works for any domain: landing pages, SaaS, Three.js apps, dashboards, mobile apps, CLI tools, etc.
---

# Idea Loop

**One command. Any idea. Complete result.**

Idea Loop is a fully autonomous, self-driving workflow that takes a raw seed — one sentence to a complex brief — and iterates through every phase needed to produce a finished, tested, production-ready output. It does not stop between phases to ask permission. It runs, self-evaluates, improves, and only surfaces when done or when it hits a genuine blocker it cannot resolve alone.

---

## The Core Promise

```
SEED → BRAINSTORM → THINK → SPEC → PHASE PLAN → BUILD → QA → DONE
         ↑___________↓ (loop until quality gate passes)
```

Each phase has an **exit condition**. If the condition is not met, the loop re-runs that phase with the lessons from the previous attempt. The loop only advances when the gate is cleared.

---

## Trigger

Run this skill when the user gives any of:
- A one-liner idea: *"landing page about birds"*
- A vague concept: *"something like Airbnb but for boats"*
- A specific technical brief: *"Three.js app with scroll-triggered animations and parallax"*
- An explicit loop call: *"run the full loop on this"*, *"take this all the way"*

Do **not** run this skill for:
- Tasks that are clearly scoped one-step jobs (just write a button, just fix this bug)
- When the user explicitly wants to stay in one phase (e.g. "just brainstorm, don't build yet")

---

## The Seven Phases

### PHASE 0 — SEED INTAKE

Read the input. Classify it:

| Seed type | Example | Loop strategy |
|-----------|---------|---------------|
| Nano | "birds landing page" | Expand aggressively; fill every gap |
| Vague | "an app like X but for Y" | Map to known patterns; infer users + goals |
| Structured | Full brief with tech stack | Follow it precisely; brainstorm enhancements |
| Technical | "Three.js app with scroll animations" | Treat tech as constraint; brainstorm content + UX |

Extract from the seed:
- **Domain** (web, mobile, CLI, data, 3D, marketing, etc.)
- **Technology signals** (if named: Three.js, Flutter, Go, React, etc.)
- **Target user** (if implied)
- **Core goal** (what success looks like)

Fill in everything not provided with the best available inference. State all inferences clearly at the start so the user can redirect if needed.

---

### PHASE 1 — BRAINSTORM

**Skills: `brainstorming` (primary) + `what-if-oracle` (provoke step) + `consciousness-council` (converge/select when the call is genuinely hard)**

Run a full brainstorm session autonomously:

1. **Frame** — define the problem space, target user, and what "great" looks like
2. **Diverge** — generate ≥7 distinct directions or feature concepts; vary by scope, approach, and ambition
3. **Provoke** — challenge each concept: who would hate it? what's the riskiest assumption? what's the 10x version?
4. **Converge** — score each direction on: user impact / feasibility / differentiation / scope fit
5. **Select** — pick the 1 strongest direction + note 2 runners-up as v-next candidates

**Brainstorm exit gate:** A single clear product direction with a defined user, a core mechanic, and a scope boundary. If not reached → re-brainstorm with tighter framing.

Output of this phase:
```
BRAINSTORM RESULT
─────────────────
Direction: [chosen direction in 2 sentences]
Core user: [who]
Core mechanic: [the one thing it must do well]
Key additions identified: [2-4 enhancements brainstorm surfaced]
Parked ideas (v-next): [list]
```

---

### PHASE 2 — THINK

**Skills: `thinker` (Phases 1–3 of its own flow, non-interactively) + `doubt-driven-development` (adversarial review of every non-trivial decision before it stands)**

Take the brainstorm output and develop it independently into a buildable plan. Run thinker's internal DEVELOP phase:

- **Problem & user** — sharpen the definition from brainstorm output
- **Core mechanic** — name the essential loop; strip to minimum
- **Approach** — concrete methods. If Three.js: name which Three.js primitives (ScrollTrigger + GSAP, OrbitControls, custom geometry). If Go backend: name packages. Never hand-wave.
- **What it needs** — all inputs, data, integrations, content
- **Unknowns & risks** — what could make this harder than it looks
- **Scope cut** — MVP vs v-next, with clear line

**Think exit gate:** Every section has a concrete answer (no "TBD" where a decision can be made). If an unknown cannot be resolved without user input → surface it; otherwise resolve it with the best available inference.

Output of this phase:
```
THINK RESULT
────────────
MVP scope: [bullet list of what's in]
v-next: [what's out]
Tech approach: [concrete methods, libraries, patterns]
Data/content: [what's needed and where it comes from]
Top risk: [the single biggest thing that could go wrong]
```

---

### PHASE 3 — SPEC

**Skills: `thinker` (Phase 4) + `writing-plans` + `api-and-interface-design` (endpoint/type contracts) + `database-schema-designer` (data model) + `docx` (final spec doc)**

Produce a full Technical Specification following the structure in `thinker/references/tech-spec-template.md`:

1. Overview
2. Problem & Users
3. Goals & Non-Goals
4. Scope (MVP / v-next)
5. Core Mechanic & Approach (with concrete methods)
6. Architecture (stack, components, data model)
7. User Flows
8. Acceptance Criteria (verifiable checklist)
9. Testing & Safety
10. Risks, Assumptions & Open Questions
11. Milestones

Save as `.docx` using the `docx` skill. Present the file.

**Spec exit gate:** All 11 sections populated. No placeholder text. Acceptance criteria are objectively verifiable. If a section cannot be written without information only the user has → flag it and continue with best inference; note it as an open question.

---

### PHASE 4 — PHASE PLAN

**Skills: `writing-plans` + `decider` (per-phase skill routing) + `sys-design` (architecture graphs) + `dispatching-parallel-agents` & `using-git-worktrees` (when the plan has independent build tracks)**

Break the spec into **build phases** — ordered chunks of work that each produce a runnable increment:

```
Phase 1: Foundation (scaffolding, routing, data model)
Phase 2: Core mechanic (the one thing it must do well)
Phase 3: Full feature set (everything in MVP scope)
Phase 4: Polish & QA (design pass, edge cases, error states)
Phase 5: Production readiness (deploy, docs, performance)
```

For each phase, define:
- **Goal** — what is runnable at the end of this phase
- **Tasks** — concrete list of what to build
- **Done condition** — how we know this phase is complete

**Plan exit gate:** Every task in every phase maps to a specific acceptance criterion from the spec. No phase is "figure it out". If a task is ambiguous → decompose it until it is concrete.

---

### PHASE 5 — BUILD

**Core build skills:** `frontend-ui-engineering`, `frontend-design`, `sys-design`, `documentation-and-adrs`, `test-driven-development`, plus domain skills picked by `decider` (see `domain-overrides.md`):
- **Web/UI:** `frontend-ui-engineering` + `frontend-design` + `framer-motion` (motion) + `zustand` (client state) + `api-communication` (data layer) + `localization` (if multi-locale)
- **3D:** `threejs`
- **Backend/data:** `api-and-interface-design` + `database-schema-designer`
- **Mobile:** `flutter` / `swiftui-pro`
- **Payments:** `stripe-integration-expert`
- **Assets:** `generate-image` (real images, never placeholders) + `infographics`
- **Always-on guardrails:** `security-and-hardening` + `env-secrets-manager` (secure-by-default, no committed secrets)

Execute each build phase in sequence. For each phase:

1. Read the phase's task list from the plan
2. Select the right skill(s) via `decider`
3. Build, following each skill's own `SKILL.md`
4. Self-check against the phase's done condition
5. If done condition not met → fix before advancing

Build rules:
- Follow the spec. Resist scope creep. New ideas → log as v-next, do not build.
- Build incrementally. Every phase produces working, runnable code.
- For Three.js / animation work: read `threejs/SKILL.md` and follow its library selection and pattern guidance.
- For UI work: read `frontend-ui-engineering/SKILL.md` for style choices, color systems, component patterns.
- For frontend aesthetics: read `frontend-design/SKILL.md` for typography and visual direction.

**Build exit gate:** All acceptance criteria from the spec are met. Every feature in MVP scope is working. No placeholder UI. No console errors.

---

### PHASE 6 — QA

**Skills: `qa-tester` (primary) + `browser-testing-with-devtools` (live runtime — DOM, console, network, Core Web Vitals) + `code-review` (correctness) + `a11y-audit` (WCAG 2.2 AA) + `performance-optimization` (Lighthouse / LCP·INP·CLS) + `security-review` & `cybersec-web-security` (web vulns) + `verification-before-completion` (final gate)**

Run a multi-lens QA pass across the completed build:
- **Functional** (`qa-tester`): detect new/changed features, static analysis, visual inspection of every page/modal/state, check every acceptance criterion
- **Runtime** (`browser-testing-with-devtools`): real-browser console errors, network failures, runtime exceptions
- **Correctness** (`code-review`): bug hunt on the diff
- **Accessibility** (`a11y-audit`): WCAG 2.2 A + AA — contrast, ARIA, keyboard nav *(enforces your global accessibility rule)*
- **Performance** (`performance-optimization`): Lighthouse ≥ 95, Core Web Vitals *(enforces your global Lighthouse rule)*
- **Security** (`security-review` + `cybersec-web-security`): XSS, secrets, OWASP basics

If QA finds issues:
- Minor (styling, copy, missing empty state) → fix in-loop, re-check
- Moderate (broken feature, logic error, a11y/perf miss) → return to BUILD phase for that component, then re-QA
- Blocker (fundamental design issue) → surface to user with options

**QA exit gate:** All acceptance criteria pass. No P0/P1 bugs. WCAG 2.2 AA clean. Lighthouse ≥ 95. No exposed secrets. QA report produced via `verification-before-completion`.

---

### PHASE 6.5 — SHIP (optional — runs when seed implies a deployable product, skipped for throwaway/demo)

**Skills: `git-workflow-and-versioning` + `ci-cd-and-automation` + `shipping-and-launch` + `documentation-and-adrs` + `finishing-a-development-branch`**

- **Version control** (`git-workflow-and-versioning`): conventional commits, clean history
- **Pipeline** (`ci-cd-and-automation`): CI with the QA gates above wired in as quality gates
- **Launch readiness** (`shipping-and-launch`): pre-launch checklist, rollout plan, monitoring, rollback
- **Docs** (`documentation-and-adrs`): README + ADRs for non-obvious tech choices
- **Branch finish** (`finishing-a-development-branch`): merge / PR / cleanup

**Ship exit gate:** Builds in CI, deploy path documented, rollback plan exists. (Skip entirely for one-off demos — note the skip.)

---

### PHASE 7 — DONE

Deliver the complete output:
- All files in `/mnt/user-data/outputs/`
- Technical Specification `.docx`
- QA report
- README with setup instructions
- Summary of what was built, what was deferred to v-next, and what open questions remain

Final message format:
```
✅ LOOP COMPLETE
────────────────
Built: [what was built in 1 sentence]
Phases run: [N]
Iterations: [total loop-backs]
Spec: [filename]
QA: [pass/issues resolved]
v-next: [top 3 deferred ideas]
Open questions for you: [if any]
```

---

## Loop-Back Rules

The loop self-corrects. When a phase's exit gate is not met:

| Situation | Action |
|-----------|--------|
| Brainstorm direction is weak | Re-run BRAINSTORM with tighter framing |
| Think has unresolvable unknowns | Surface 1 question to user, then continue |
| Spec has a gap that appeared during build | Amend spec, note the change, continue |
| Build phase done condition not met | Re-build that phase; do not advance |
| QA finds P0 bug | Return to BUILD for that component, then re-QA |
| QA finds the spec was wrong | Amend spec + fix build + re-QA |

**Max loops per phase:** 3 attempts before surfacing to user. If a phase fails 3 times, report what's blocking and ask for direction.

---

## Skill Selection per Phase

Decider is called at the start of PHASE 5 (BUILD) and re-called at the start of each build sub-phase. Pass it:

```
Situation: Building [product type] — [tech stack]. 
Stage: Build, Phase [N] of [total]. 
Needs: [what this build phase requires — UI, backend, 3D, data, docs, etc.]
```

Decider returns the skill(s). Loop announces them, reads each skill's SKILL.md, then proceeds.

---

## Domain-Specific Overrides

### Three.js / WebGL apps
- Always read `threejs/SKILL.md` before touching any 3D code
- Use ScrollTrigger + GSAP for scroll animations (not custom scroll listeners)
- OrbitControls for camera when applicable
- Draco compression for any imported models
- Test at 60fps target; flag if below on first render

### Landing pages / marketing sites
- Read `frontend-ui-engineering/SKILL.md` for layout patterns
- Read `frontend-design/SKILL.md` for typography and color direction
- Use `framer-motion` for scroll reveals; `generate-image` for real assets
- Mobile-first. Every section responsive.
- Performance: images optimized, no render-blocking scripts

### Full-stack apps (Go/Flutter/React etc.)
- Read `sys-design/SKILL.md` for architecture; record choices via `documentation-and-adrs`
- Define data model with `database-schema-designer` before any code
- API-first: spec endpoints with `api-and-interface-design`, then build them; wire the client with `api-communication`

### Complex multi-module apps
- Use `writing-plans` + `decider` to chunk phases
- Use `documentation-and-adrs` for ADRs on non-obvious tech choices
- Use `documentation-and-adrs` + `markdown-mermaid-writing` for README and API docs
- Use `dispatching-parallel-agents` + `using-git-worktrees` for concurrent build tracks

---

## What Loop Does NOT Do

- Ask unnecessary questions between phases (only surfaces genuine blockers)
- Skip the spec to "just start building"
- Drift from the spec during build (new ideas go to v-next)
- Call QA before the build phase's done condition is met
- Produce a partial deliverable and call it done

---

## Example: "landing page about birds"

```
PHASE 0 — SEED INTAKE
Seed type: Nano
Domain: Web / marketing landing page
Tech: HTML/CSS/JS (inferred — no stack specified)
Target user: Bird enthusiasts, nature lovers, potential community members
Core goal: Beautiful, engaging landing page that communicates a bird-related product/brand

PHASE 1 — BRAINSTORM
Directions explored:
1. Bird watching app promo page
2. Bird species guide/encyclopedia
3. Community for bird photographers
4. Bird sound library
5. Migration tracking visualisation
6. Bird feeder product landing page
7. "Birds of [region]" educational site

Selected: Bird photography community — strongest differentiation, rich visual potential
Key additions: hero with parallax feathers, species gallery, community CTA, sound clips

PHASE 2 — THINK
MVP: Hero section, about section, gallery grid, CTA, footer
Tech: HTML/CSS/JS, CSS Grid, Intersection Observer for scroll animations
No backend needed for v0

PHASE 3 — SPEC → .docx produced

PHASE 4 — PLAN
Phase 1: HTML scaffold + design system (colors, fonts, spacing)
Phase 2: Hero with parallax
Phase 3: Gallery + about sections
Phase 4: Animations + mobile responsive
Phase 5: QA pass

PHASE 5-6 — BUILD + QA → complete files delivered

PHASE 7 — DONE ✅
```

---

## How to Invoke

In Claude Code, run:

```
/idea-loop "your seed here"
```

Or use the built-in `/loop` equivalent with this SKILL.md as the driver:

```
/loop [run idea-loop on: "Three.js app with scroll-triggered section animations, each section reveals a new geometric shape"]
```

Or just describe the idea naturally and Claude Code will route it here via `decider`.
