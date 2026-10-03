---
name: super-design
description: Use when the user asks you to build, style, theme, refine, audit, or recreate UI — or uploads a screenshot to rebuild. Reads DESIGN.md as a closed token layer, detects the project's framework (Tailwind v4/v3, ShadCN, MUI, Radix, Geist), and enforces production design rules (tokens only, full state matrix, WCAG 2.2 AA, responsive across 320→1920px, reusability, 300 LOC hard limit, 44×44 touch targets, continuous UI memory) via PostToolUse hooks.
allowed-tools: Read, Write, Edit, MultiEdit, Glob, Grep, Bash
---

# Super Design

You enforce a production design system. Read `DESIGN.md` before editing UI. Emit tokens, never literals. Ship full state coverage. **Build every component reusable.** Validate with the bundled scripts.

## The one-paragraph rule

Any UI code you write references `DESIGN.md` tokens by name. No `#hex`, no `rgb()/hsl()`, no raw `px` outside the scale, no inline `style={{ color: ... }}`. Every interactive element defines `hover`, `focus-visible`, `active`, `disabled` — buttons add `loading`, inputs add `error` and `readonly`. Focus rings use `:focus-visible` with a double-layer box-shadow for 3:1 contrast at all offsets. Motion is `transform` and `opacity` only, under 300ms, guarded by `prefers-reduced-motion`. **Files stay under 300 LOC, functions under 80 LOC, JSX depth under 6, hooks per component under 10. Every component declares an exported `Props` interface. Every interactive element has `min-h-11 min-w-11` (44×44 touch target). Every layout has responsive breakpoints or container queries. Layouts pass at 320/375/768/1024/1440/1920.** Run `bash scripts/test.sh <file>` before declaring done — target score ≥ 90.

## Before / after — the discipline in 5 seconds

**❌ Rejected by the hook:**
```tsx
<button
  style={{ background: '#5e6ad2', padding: '17px' }}
  className="rounded-[6px] hover:bg-[#828fff]"
  onClick={submit}
>
  Save
</button>
```
Rejected for: literal hex (×2), off-scale px, arbitrary Tailwind value, no `:focus-visible`, no `:disabled`, no `:active`, no min size, no `type`, no `aria-busy` on async click.

**✓ Accepted:**
```tsx
<Button variant="primary" size="md" loading={isPending} onClick={submit}>
  Save
</Button>
```
With a `Button` that reads:
```tsx
// components/ui/button.tsx — 92 LOC
const buttonVariants = cva(
  [
    "inline-flex items-center justify-center gap-2 whitespace-nowrap",
    "rounded-md font-medium select-none",
    "transition-[background-color,box-shadow,transform] duration-fast ease-out",
    "focus-visible:outline-none",
    "focus-visible:shadow-[0_0_0_2px_var(--color-bg),0_0_0_5px_var(--color-focus-ring)]",
    "active:scale-[0.98]",
    "disabled:opacity-50 disabled:pointer-events-none",
    "aria-busy:opacity-70 aria-busy:cursor-wait",
    "forced-colors:border forced-colors:border-[ButtonText]",
    "min-h-11 min-w-11",
  ].join(" "),
  {
    variants: {
      variant: {
        primary:   "bg-accent text-accent-fg hover:bg-accent-hover",
        secondary: "bg-surface text-fg border border-border hover:bg-surface-raised",
        ghost:     "bg-transparent text-fg hover:bg-surface-raised",
        danger:    "bg-danger text-white hover:brightness-110",
      },
      size: { sm: "h-9 px-3 text-sm", md: "h-11 px-4", lg: "h-12 px-6 text-base" },
    },
    defaultVariants: { variant: "primary", size: "md" },
  }
);
```

Every token resolves through `DESIGN.md`. No magic numbers.

## Workflow: starting a UI task

**Step 1 — Detect.**
```bash
bash "${CLAUDE_SKILL_DIR}/scripts/detect-framework.sh"
```
Returns JSON with `cssFramework`, `tailwindVersion`, `componentLibrary`, `projectFramework`, `designMd`. Branch on `recommendedAdapter`.

**Step 2 — Load DESIGN.md.**
- If it exists → read it completely.
- If it doesn't → ask: *"I don't see DESIGN.md. Do you want me to (a) bootstrap the template, (b) extract one from a reference in the `super-design` collection, or (c) extract one from a screenshot?"* Do not proceed without a closed token layer.

**Step 3 — Lint the DESIGN.md.**
```bash
bash "${CLAUDE_SKILL_DIR}/scripts/lint-design-md.sh" DESIGN.md
```
If it fails schema, stop and fix it first. A broken token layer poisons everything downstream.

**Step 4 — Generate theme (once per project).**
```bash
node "${CLAUDE_SKILL_DIR}/scripts/generate-theme.mjs" DESIGN.md --target=<adapter>
```
Emits the framework-native theme file (`@theme` block, `tailwind.config.ts`, `theme.ts`, etc.) wired to the tokens in DESIGN.md. Show the user the diff; get approval before writing.

**Step 5 — Build the component.**
- Max 300 LOC per file; extract when you approach it.
- Every required state from `references/state-matrix.md`.
- Use the matching adapter in `references/framework-adapters/`.
- Use `:focus-visible` with the double-ring shadow pattern.
- Touch targets ≥ 44×44.
- Mark interactive text with `select-none`; mark inert overlays with `pointer-events-none`.

**Step 6 — Validate.**
```bash
bash "${CLAUDE_SKILL_DIR}/scripts/test.sh" <file>
```
Runs `validate-tokens`, `validate-component`, `quality-score`, and — if a reference PNG exists — `visual-diff`. Blocks on violations; warns on smells; emits a composite score 0–100.

**Step 7 — Verify contrast.**
```bash
node "${CLAUDE_SKILL_DIR}/scripts/contrast-check.mjs" DESIGN.md
```
Walks every semantic color pair (fg on bg, accent-fg on accent, border on surface) and asserts WCAG 2.2 AA (4.5:1 text, 3:1 large text + UI, 3:1 focus).

**Step 8 — Generate the design system showcase page.**
```bash
node "${CLAUDE_SKILL_DIR}/scripts/generate-design-system-page.mjs" \
  DESIGN.md --out src/pages/DesignSystem.tsx
```
Run this once per project after finalizing `DESIGN.md`, and again whenever the **token structure** changes (not the values). The resulting page is the visual reference both user and agent come back to throughout the development cycle. Keep it in version control and wire it to a route like `/design-system`.

## Workflow: screenshot → code

Follow `references/screenshot-to-code-workflow.md`. The 7-pass loop is encoded as filled prompts with concrete JSON schemas. Do not invent tokens — reconcile against DESIGN.md at pass 5 and get user approval on any NEW tokens.

For dense regions:
```bash
bash "${CLAUDE_SKILL_DIR}/scripts/crop-region.sh" input.png <x> <y> <w> <h> out.png
```
Crops produce measurably better vision-model accuracy. Use them.

For verification:
```bash
node "${CLAUDE_SKILL_DIR}/scripts/screenshot-component.mjs" http://localhost:3000/my-page out.png
node "${CLAUDE_SKILL_DIR}/scripts/visual-diff.mjs" reference.png out.png diff.png 0.1
```
Iterate until `score ≥ 95` (recreation) or `≥ 99` (pixel-perfect port). Cap at 3 iterations — gains plateau.

## Workflow: style audit

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/audit.sh" src/
```
Walks every component file, emits `{file, score, grade, violations[]}`, sorts by worst. Fix in order. Re-run and report the delta.

## Model-specific notes

- **Claude (3.5/4.x)** — strongest at layout + OCR + iteration. Give it crops for dense regions.
- **GPT-4o / GPT-5** — strong on component identification. Weak on exact bbox coords; use the 12-grid overlay prompt.
- **Gemini 1.5+** — native bbox output; can skip grid overlay. Strong on long-context multi-screen flows.
- **All models** — never trust guessed text. Always OCR-ground typography.

## Hard stops (the hook blocks these)

| Violation | Exit |
|---|---|
| Literal `#hex`/`rgb()`/`hsl()` outside token file | block |
| Inline `style={{ color: ... }}` | block |
| `<img>` without `alt` | block |
| **File > 300 LOC** (tightened in v1.2.0, was 500) | block |
| **Longest function > 80 LOC** (new in v1.2.0) | block |
| File with no `focus-visible` but has `onClick`/`<button>` | block |
| **Layout file with no responsive variants** (promoted from warn to block in v1.2.0) | block |
| px outside the allowed scale (> 3 occurrences) | block |
| **Component file with > 10 hooks** (tightened from 12) | block |
| JSX nesting depth > 6 | block |
| **Interactive element with no 44×44 minimum size** (new in v1.2.0) | warn |
| **Component without exported Props interface** (new in v1.2.0) | warn |
| **Component with module-scope hardcoded data > 3 items** (new in v1.2.0) | warn |
| **h1/h2/h3 without clamp() or responsive text-\*** (new in v1.2.0) | warn |
| `outline: none` without replacement shadow/outline | warn |
| Animating `width`/`height`/`top`/`left`/`margin`/`padding` | warn |
| `:focus` used instead of `:focus-visible` | warn |

Allowed px scale: `0, 1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80, 96, 112, 128, 160, 192, 224, 256`, plus viewport breakpoints `320, 375, 768, 1024, 1280, 1440, 1536, 1920`.

## Responsive guardrails (v1.2.0 — promoted to hard enforcement)

Every layout component must pass at **320, 375, 428, 768, 1024, 1280, 1440, 1920** pixels wide — the full device range from iPhone SE to ultra-wide desktop. The `validate-component.sh` hook blocks layout files that have:

- No Tailwind breakpoint prefixes (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`)
- No `@container` / container queries
- No intrinsic responsive primitives (`auto-fit`, `minmax()`, `clamp()`, `fr` units)

"Layout file" means any file containing `<main>`, `<section>`, `<article>`, `<aside>`, `<nav>`, or className variants of `grid`, `flex-col`, `flex-row`, `container`, or `Layout`. Buttons and small primitives are exempt — they inherit responsive behavior from their parents, and forcing breakpoint variants on every button would add noise without value.

**Content-first beats breakpoint-first.** Start narrow (320px), let content drive breakpoints. Add a breakpoint only when the layout visibly breaks. Prefer container queries over media queries for reusable components (a Card in a sidebar adapts to its container, not the viewport).

For the full responsive playbook — fluid type formulas, container query patterns, intrinsic grid primitives, touch targets, safe-area insets, `dvh`/`svh`/`lvh`, and a self-validation checklist — see `references/responsive-patterns.md`.

## Reusability rules (v1.2.0 — new validator)

Every component you create must be **reusable** — droppable into a different context and parameterizable via props. `validate-reusability.sh` runs on every edit and warns on:

- **`NO_PROPS_INTERFACE`** — TSX file with no named `Props` interface/type. Declare one: `export interface ButtonProps { ... }`.
- **`PROPS_NOT_EXPORTED`** — Props interface exists but isn't exported. Consumers need to import it for type safety.
- **`HARDCODED_CONTENT`** — JSX children contain string literals > 60 characters. Extract long copy into props or children.
- **`MODULE_DATA`** — Top-level `const` array with > 3 object items. Accept the data as a prop so the component works for other datasets.
- **`COMPONENT_FETCHES`** — Component calls `fetch()`, `axios.*`, `useQuery()`, `useSWR()`, or `useMutation()` directly. Move data fetching into a container or hook and pass data via props. Files under `/containers/`, `/hooks/`, `/pages/`, `/routes/`, or `/app/` are exempt.
- **`MULTI_PRIMARY`** — More than 2 component-like exports in one file. Split into separate files (one component per file).
- **`NO_PARAMETERIZATION`** — Component has no `{children}` usage and no destructured props, but is > 30 LOC. It hardcodes its own content and can't be reused.

Pages are exempt: files matching `pages/`, `app/*/page.tsx`, `app/*/layout.tsx`, `routes/`, `App.tsx`, `index.tsx`, `*.stories.tsx`, `*.test.tsx`, and `DesignSystem.tsx` / `design-system/` are skipped — hardcoded content is correct in those files by design.

## LOC limits (v1.2.0 — tightened)

| Metric | Hard (block) | Soft (warn) | Old (v1.1.0) |
|---|---|---|---|
| File LOC | **300** | 150 | 500 / 300 |
| Function LOC (longest) | **80** | 40 | — (no check) |
| Hooks per component | **10** | 6 | 12 / 8 |
| JSX nesting depth | 6 | 4 | 6 / 4 |

Function LOC is tracked with a proper brace-counting awk parser, not a naive line-count — it finds the longest top-level function in a file and reports its LOC. A single 120-LOC function in a 200-LOC file still blocks the edit.

## UI memory (v1.2.0 — new hook)

`update-ui-memory.sh` runs after every component write and appends a structured entry to `.claude/super-design/ui-memory.md`:

```markdown
## 2026-04-10T14:22:07Z — src/components/Button.tsx
- LOC: 42
- Tokens: --color-accent, --color-fg, --color-border, --radius-md, --inset-sm
- States: hover, focus-visible, disabled, active, loading
- Responsive: sm, md
- Touch targets: compliant (44×44 min)
- Props interface: ButtonProps (exported)
- Forced-colors: compliant
```

The log is **bounded to the last 200 entries** (older ones are pruned automatically) and loaded into session context by `inject-design-context.sh`. This means across a long development cycle you can see your own past decisions — which tokens you used, which states you covered, what your last Button looked like — without re-reading every file. The agent uses this log to stay **consistent** across the entire project.

## Design system showcase (v1.2.0 — new generator)

`generate-design-system-page.mjs` emits a single-file React route that renders **every token in DESIGN.md** live:

- Primitive palette (color.neutral / color.brand / color.status) as swatch grids
- Semantic color table with live contrast ratios against light and dark backgrounds
- Typography scale (each size rendered with sample text)
- Spacing scales (inset / stack / inline) visualized as rulers
- Radius scale (boxes with each radius applied)
- Shadow / elevation scale (boxes at each level)
- Motion (buttons animating at each duration)
- Responsive breakpoint table
- Live viewport indicator (bottom-right, shows current width + active breakpoint)

Run it with:
```bash
node "${CLAUDE_SKILL_DIR}/scripts/generate-design-system-page.mjs" \
  DESIGN.md --out src/pages/DesignSystem.tsx
```

The generated file references CSS variables via `var(--color-*)` etc., so **it auto-updates when the theme is regenerated** without needing to re-run this script. Re-run only when the token STRUCTURE changes (tokens added or removed), not when VALUES change.

The design system page is the single source of truth the user and agent can reference throughout the development cycle. It is **exempt from the 300 LOC rule** (it's a page, not a component) and from reusability checks (pages are allowed to hardcode content).

## Bundled files — progressive disclosure

Load on demand; each reference is ~400–900 words:

- `DESIGN.md` — the enhanced template (blank slate)
- `references/tokens-schema.md` — DTCG format, naming, primitive vs semantic vs component layers
- `references/state-matrix.md` — required states per component + ARIA + keyboard + `STATE_MATRIX.yaml`
- `references/animation-tokens.md` — duration/easing/recipes + reduced-motion
- `references/responsive-patterns.md` — breakpoints, clamp(), container queries, touch targets, safe-area
- `references/component-quality-gates.md` — LOC/complexity/scoring rubric + regex patterns
- `references/screenshot-to-code-workflow.md` — 7-pass extraction loop with filled prompts
- `references/framework-adapters/*.md` — concrete theme codegen per framework

### Scripts (runnable)

- `scripts/validate-tokens.sh` — blocks literal colors, inline styles, off-scale px (PostToolUse hook)
- `scripts/validate-component.sh` — blocks oversized files/functions, missing focus-visible, bad responsive, weak touch targets (PostToolUse hook)
- `scripts/validate-reusability.sh` — warns on missing Props interface, hardcoded content, module-scope data (PostToolUse hook, **new in v1.2.0**)
- `scripts/update-ui-memory.sh` — maintains `.claude/super-design/ui-memory.md`, a running log of every component write (PostToolUse hook, **new in v1.2.0**)
- `scripts/generate-theme.mjs` — emits framework-native theme code from DESIGN.md
- `scripts/generate-design-system-page.mjs` — emits a live React showcase page from DESIGN.md (**new in v1.2.0**)
- `scripts/contrast-check.mjs` — WCAG 2.2 AA contrast validator for DESIGN.md
- `scripts/lint-design-md.sh` — schema linter for DESIGN.md
- `scripts/quality-score.sh` — 0–100 per-file quality grade
- `scripts/audit.sh` — batch audit walker for `src/`
- `scripts/test.sh` — 13-test self-test suite

Only load what you need. SKILL.md + the single matching adapter is typically enough for one session.

## Do not

- Do not invent tokens. Propose a diff to DESIGN.md and wait for approval.
- Do not reference primitive tokens (`--color-neutral-900`) from components. Reference the semantic layer (`--color-fg`).
- Do not use `:focus` — always `:focus-visible` with a double-ring.
- Do not use `outline: none` without a same-or-greater-visibility replacement.
- Do not ship without a `forced-colors: active` fallback on interactive surfaces.
- Do not generate theme files if DESIGN.md is failing the linter.
- Do not skip `lint-design-md.sh` at session start.
- Do not write > 300 LOC/component without splitting.
- Do not animate layout properties.
- Do not auto-loop visual-diff more than 3 times without surfacing to the user.
