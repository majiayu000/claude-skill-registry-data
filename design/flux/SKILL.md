---
model_tier: medium
name: flux
description: "Use when the project uses `livewire/flux` — dispatched by `directives/ui/{apply,review,polish}.ts`. Covers Flux components, slots, variants, and form primitives."
domain: engineering
workspaces:
  - engineering
packs:
  - laravel
trust:
  level: professional
install:
  default: false
  removable: true
---

# flux

> **Grounded stack guidance:** Tailwind-layer Do/Don't + docs URLs via
> `./scripts-run <skills-root>/corpus-grounding/scripts/ground search
> --manifest <skills-root>/design-intelligence/data/manifest.json
> --stack html-tailwind "<topic>"`. See
> [`design-intelligence`](../design-intelligence/SKILL.md).

## Positioning — dispatched, not standalone

`flux` is the **primitive-library executor** for projects on the
Livewire + Flux stack. It is invoked by
[`directives/ui/apply.ts`](../../templates/scripts/work_engine/directives/ui/apply.ts)
once the design brief is locked, and revisited by `review.ts` /
`polish.ts` during the design-review loop. It does **not** own the
flow, does **not** drive the audit, and does **not** lock the design.

| Concern | Owner |
|---|---|
| Audit + token inventory (mandatory pre-step) | [`existing-ui-audit`](../existing-ui-audit/SKILL.md) |
| Design brief (layout / states / microcopy) | [`directives/ui/design.ts`](../../templates/scripts/work_engine/directives/ui/design.ts) |
| Universal design heuristics | [`fe-design`](../fe-design/SKILL.md) |
| Component logic / state / actions | [`livewire`](../livewire/SKILL.md) |
| Static Blade partials | [`blade-ui`](../blade-ui/SKILL.md) |

## When to use

Cite this skill when:

- The project depends on `livewire/flux` and `directives/ui/apply.ts` dispatches Flux primitives
- Building forms, modals, dropdowns, toasts, or other standard UI elements that Flux already provides

Do NOT use when:

- Raw Blade templates without Flux (use `blade-ui` skill)
- Livewire component logic / state (use `livewire` skill)
- React + shadcn (use `react-shadcn-ui` skill)
- Driving the full UI flow yourself — that is the `directives/ui/` orchestrator

## Procedure: Create a Flux view

### Step 0: Inspect

1. Confirm Flux is installed — check `composer.json` for `livewire/flux`.
2. Check existing views — match Flux component usage patterns.
3. Check Flux docs — https://fluxui.dev/docs for latest API.

### Step 1: Build the view

1. Use `<flux:*>` components instead of raw HTML.
2. Use `variant` prop for styling (not custom Tailwind for standard styles).
3. Use `wire:model` for Livewire binding.
4. Use `label` prop on form fields (accessibility).

### Step 2: Validate

1. No raw HTML form elements where Flux equivalents exist.
2. No manual error rendering (Flux has built-in validation display).
3. No conflicting Tailwind classes overriding Flux styles.

## Conventions

→ See guideline `php/flux.md` for component reference, variants, forms, icons.

## Output format

1. Blade view using Flux components with correct props and slots
2. Livewire component class if interactive behavior is needed

### Review pass — a11y findings + preview envelope

When this skill is dispatched by `directives/ui/review.ts` (test slot)
or `directives/ui/polish.ts` (verify slot) — i.e. a review/polish run,
not the initial apply — it also emits:

- `state.ui_review.a11y` — `{violations: [{rule, selector, severity}, ...],
  severity_floor?, accepted_violations?}`. Use the same `(rule, selector)`
  shape as `state.ui_audit.a11y_baseline` so the engine's de-dup matches
  pre-existing entries on replay. Omit the envelope on apply passes; the
  engine's `_apply_a11y_gate` only fires when a baseline is present.
- `state.ui_review.preview` — `{render_ok: bool, screenshot_path?,
  dom_dump_path?, error?, skipped?}`. `render_ok: false` with `error`
  populated triggers the `preview_render_failed` halt; `render_ok: true`
  with `screenshot_path` threads the screenshot into the delivery
  report's `artifacts` list. Browser tooling (Playwright/Cypress/…) is
  a consumer-project dependency — this package does not ship one.

Polish dispatch: when the dispatcher skips `review` because a previous
review pass already returned `SUCCESS`, this skill MUST itself
synthesise the updated `state.ui_review.findings` (including any
remaining `a11y_violation` entries) so the engine's gate sees the
current state on the next polish round.

## Gotcha

- The model tends to use old Flux API syntax — always check latest docs.
- Flux has built-in validation display — don't add manual error rendering alongside it.
- Don't mix Flux with raw HTML form elements in the same form.

## Taste Dials

When `DESIGN.md` declares `## Taste Dials`, honour them: Variance → layout-family spread + asymmetry tolerance; Motion → animation budget + reduced-motion posture; Density → spacing scale + information-per-viewport. Absent → follow the design brief's inferred dials.

## Do NOT

- Do NOT use raw `<input>`, `<select>`, `<button>` when Flux equivalents exist.
- Do NOT override Flux styles with conflicting Tailwind — use variants or slots.
- Do NOT skip the `label` prop on form fields — accessibility.

## Anti-slop

Flux primitives carry sane defaults, but composition still drifts into slop —
pull [`docs/guidelines/design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md)
and check Layout (L1/L2 hero-metric + identical-card grids) and Color
(C1 gradient defaults) before shipping. Tailwind-level bans:
[`tailwind-engineer`](../tailwind-engineer/SKILL.md).

## Auto-trigger keywords

- Flux UI
- Livewire components
- Flux component
- Laravel Flux
