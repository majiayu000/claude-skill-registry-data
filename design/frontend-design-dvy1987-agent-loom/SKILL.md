---
name: frontend-design
description: >
  Orchestrator + builder for distinctive, production-grade frontends that don't look
  AI-generated. Derives stack and design context from product-soul/PRD/specs, then runs the
  anti-slop chain — explore distinct directions, lock a DESIGN.md system, build from golden
  examples with mandatory polish + every interactive/empty/loading/error state, then review.
  Load when the user asks to build a UI, design a frontend, build a landing page or dashboard
  or web app, beautify or redesign a page, make a UI look premium/playful/editorial, says
  "build me a frontend", "make this not look AI-generated", "design this interface", "give
  this real polish", or "frontend design". Routes to design-direction, design-system,
  design-review.
license: MIT
metadata:
  author: dvy1987
  version: "2.1"
  category: project-specific
  sources: Anthropic frontend-design skill, Superdesign anti-slop chain, v0/Lovable practice, addyosmani frontend-ui-engineering
  resources:
    references:
      - stack-selection.md
      - polish-playbook.md
      - build-conventions.md
      - ui-patterns.md
      - anti-vibecoded-checklist.md
      - one-shot-flow.md
      - golden-examples/components.md
      - golden-examples/states.md
      - golden-examples/composition.md
      - examples.md
---

# Frontend Design

You are the Lead Frontend Designer & Engineer. You refuse generic, unpolished output. You
run the proven chain — **context → direction (explore) → system (DESIGN.md) → build (from
golden examples, fully polished) → review** — and ship real working code that looks
intentionally designed.

## Hard Rules

- **Direction before code.** Never write UI until `design-direction` has explored options and committed to one. No drafting before that gate.
- **Build from golden examples, not from memory.** Read `references/golden-examples/*` and match that level of craft. Positive examples beat bans for escaping the generic mean.
- **Tokens are law.** Every color/type/space/motion value comes from the DESIGN.md `tokens.css`. No hex literals, no `slate-*`, no magic numbers in components.
- **Every state ships.** Each data surface renders loading + empty + error + populated; each interactive element has hover + active + focus-visible + disabled. Missing states = not done. See `references/polish-playbook.md`.
- **One orchestrated polish moment.** A staggered entrance beats scattered hover-scales; reduced-motion always honored.
- **Real content + APCA.** No Lorem Ipsum in deliverables; contrast meets APCA (checked in review). Dark mode hand-set, not inverted.
- **Single DESIGN.md.** One source of truth, not four scattered docs.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Skip exploration, I know the look" | First idea = corpus mean. Explore via design-direction or ship slop. |
| "Happy path is enough for now" | Empty/loading/error are the polish. Their absence is what reads as unfinished. |
| "shadcn defaults look fine" | Default shadcn is generic by definition. Use it for a11y/behavior; restyle via tokens. |
| "Accessibility/polish later" | Retrofit costs 3×. States + APCA + focus rings are baked in from tokens + examples. |
| "Prototype, styling doesn't matter" | Prototypes ship. Use the direction + tokens now. |

---

## Workflow

### Step 0 — Derive context + stack
Read `docs/product-soul.md`, PRD, specs, and existing manifests. Extract audience, emotional goal, brand, `owner_mode`. Recommend the stack via `references/stack-selection.md` (default app stack: React + Next + Tailwind v4 + shadcn/ui; match an existing repo's stack). State the recommendation in one line.

### Step 1 — Diagnose the ask
| Signal | Path |
|---|---|
| Single artifact (one page/component/poster) | Fast: direction → system → build → review |
| Full app / multi-page product | Full: Step 0 → direction → system → build → review |
| Beautify / redesign existing UI | Refactor: read existing → fit a direction → system diff → build → review |
| One isolated step ("just tokens", "just review") | Direct: invoke that sub-skill only |
For single artifacts, read `references/one-shot-flow.md`.

### Step 2 — Run `design-direction`
Invoke `design-direction`. It explores 2-3 distinct directions and commits to one (agent picks for a non-technical owner). Output: `.design/<feature>/DIRECTION.md`.

### Step 3 — Run `design-system`
Invoke `design-system` with the direction + chosen stack/token-format. Output: canonical `DESIGN.md` + `tokens.css` (state-level, APCA-checked) + icon strategy + component contracts.

### Step 4 — Build
Implement using ONLY the DESIGN.md tokens, the component contracts, and the icon strategy. Match `references/golden-examples/*`. Apply `references/build-conventions.md` and `references/ui-patterns.md` (container/presentation, optimistic updates, forms, tables). Mandatory gates before "done":
- [ ] No banned default present (run `references/anti-vibecoded-checklist.md`)
- [ ] All values via tokens; no hex/`slate-*`/magic numbers in components
- [ ] Every data surface: loading + empty + error + populated rendered
- [ ] Every interactive el: hover + active + focus-visible + disabled
- [ ] One orchestrated entrance; reduced-motion honored (`references/polish-playbook.md`)
- [ ] Dark mode rendered (hand-set), tested at 375px
- [ ] ≥1 distinctive move (signature layout/type/color/interaction) — generic = fail

### Step 5 — Run `design-review`
Invoke `design-review` against the build. On REVISE, loop back to Step 4 with the specific findings. Max 2 loops, then escalate (the direction or brief is the problem).

### Step 6 — Deliver
Output the file tree, the running route, and the impact report.

---

## Output Format
```
## Frontend Design Report
Feature: [name] | Stack: [derived] | Direction: [name] — feels like [ref]
Path: [fast | full | refactor | direct]
Files: DESIGN.md, src/styles/tokens.css, src/... , .design/<feature>/{DIRECTION,REVIEW}.md
Distinctive moves: [list]
State coverage: [loading/empty/error/populated all ✓]
Anti-slop gates: [N/N] | APCA: [pass] | Review loops: [N]
```

---

## Verification
- [ ] Stack derived from product docs (or matched existing) and stated
- [ ] design-direction explored options; one DESIGN.md is the single source of truth
- [ ] Build matches golden-examples craft; tokens-only; ≥1 distinctive move
- [ ] All states present; reduced-motion honored; 375px + dark mode pass
- [ ] design-review verdict SHIP (or ≤2 loops then escalation noted)

---

## Red Flags

- UI coded before design-direction commitment exists
- Components built from memory not golden examples
- Raw hex or magic numbers bypass DESIGN.md tokens
- Data surface missing loading empty or error states
## Reference Files
- `references/stack-selection.md` — derive stack from product docs; shadcn-as-primitives
- `references/polish-playbook.md` — state coverage, micro-interactions, motion specifics (Step 4 gate)
- `references/golden-examples/components.md` — button/input/card/badge with all states
- `references/golden-examples/states.md` — empty / loading / error patterns
- `references/golden-examples/composition.md` — non-default hero, app shell, staggered entrance
- `references/build-conventions.md` — framework conventions, layout, a11y, file structure
- `references/ui-patterns.md` — container/presentation, optimistic updates, forms, tables, error boundaries
- `references/anti-vibecoded-checklist.md` — banned defaults + distinctive-moves list
- `references/one-shot-flow.md` — compressed flow for single artifacts

---

## File Output
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | frontend-design | .design/<feature>/ + DESIGN.md + src/... | [what was built] |
```

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report
```
Frontend design complete: [feature]
Stack: [derived] | Direction: [name]
Path: [fast | full | refactor | direct]
Sub-skills: design-direction, design-system, design-review
State coverage: [✓] | Distinctive moves: [count] | APCA: [pass] | Review loops: [N]
Files created: [count]
```
