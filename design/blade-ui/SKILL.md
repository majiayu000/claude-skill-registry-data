---
model_tier: medium
name: blade-ui
description: "Use when the project's frontend stack is Blade — dispatched by `directives/ui/{apply,review,polish}.ts`. Covers views, components, partials, layouts, and view logic."
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

# blade-ui

> **Grounded stack guidance:** pull idiomatic Do/Don't + docs URLs from the
> adopted stack corpus before improvising — `./scripts-run
> <skills-root>/corpus-grounding/scripts/ground search --manifest
> <skills-root>/design-intelligence/data/manifest.json --stack laravel "<topic>"`
> (the `laravel` stack file is Blade/UI-scoped, not general Laravel). See
> [`design-intelligence`](../design-intelligence/SKILL.md).

## Positioning — dispatched, not standalone

`blade-ui` is the **apply-step executor** for the Blade stack. It is
invoked by [`directives/ui/apply.ts`](../../templates/scripts/work_engine/directives/ui/apply.ts)
once the design brief is locked, and revisited by `review.ts` /
`polish.ts` during the design-review loop. It does **not** own the
flow, does **not** drive the audit, and does **not** lock the design.

| Concern | Owner |
|---|---|
| Audit + token inventory (mandatory pre-step) | [`existing-ui-audit`](../existing-ui-audit/SKILL.md) |
| Design brief (layout / states / microcopy) | [`directives/ui/design.ts`](../../templates/scripts/work_engine/directives/ui/design.ts) |
| Universal design heuristics | [`fe-design`](../fe-design/SKILL.md) |
| Review + polish loop | [`directives/ui/review.ts`](../../templates/scripts/work_engine/directives/ui/review.ts) + [`polish.ts`](../../templates/scripts/work_engine/directives/ui/polish.ts) |

## When to use

Cite this skill when:

- `state.stack.frontend == "blade"` (or the project is clearly Blade-only without Livewire / Flux) and `directives/ui/apply.ts` dispatches to this skill
- Editing or creating Blade views, components, partials, layouts, or forms

Do NOT use when:

- API-only endpoints (use `api-endpoint` skill)
- Livewire components (use `livewire` skill — it composes Blade views internally)
- Flux UI components (use `flux` skill)
- Driving the full UI flow yourself — that is the `directives/ui/` orchestrator

## Procedure: Create Blade view or component

### Step 0: Inspect

1. Confirm Blade is used — check `resources/views`, components, layouts.
2. Inspect existing UI patterns — layouts, partials, component naming, CSS conventions.
3. Check form handling style — old input, validation errors, session flashes, reusable field partials.
4. Inspect neighboring templates — match indentation, directives, slot usage, classes.
5. Determine data flow — what belongs in controller/view model vs. template.

### Step 1: Create the template

1. Use the project's existing layout system.
2. Keep template presentation-focused — no business logic, no DB queries.
3. Extract repeated sections into partials or components.

### Step 2: Handle forms (if applicable)

1. Follow project's form style for labels, inputs, validation messages.
2. Use CSRF protection correctly.
3. Render validation errors consistently.
4. Preserve user input with `old()` or project conventions.
5. Reuse existing field components — don't duplicate.

### Step 3: Validate

1. Check escaping — `{{ }}` by default, `{!! !!}` only when explicitly safe.
2. Check styling — Tailwind utility classes, not inline styles.
3. Check accessibility — labels for form fields, semantic HTML.

## Conventions

→ See guideline `php/blade-ui.md` for full conventions.

## Output format

1. Blade view or component file(s) following project conventions
2. Component class (if applicable) with typed props

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
  dom_dump_path?, error?, skipped?, skip_reason?}`. **Render evidence is
  required, not optional** on a review/polish pass: you MUST drive the
  headless browser (Playwright + axe-core) against the rendered output and
  write `render_ok`. Omitting it now triggers the `preview_render_required`
  halt — a render-capable stack can no longer claim success without
  rendering. `render_ok: false` with `error` populated triggers the
  `preview_render_failed` halt; `render_ok: true` with `screenshot_path`
  threads the screenshot into the delivery report's `artifacts` list. The
  only no-render path is an **explicit, reasoned skip**: set `skipped: true`
  plus a `skip_reason` (e.g. no Playwright runner in this env). Browser
  tooling (Playwright/Cypress/…) is a consumer-project dependency — this
  package does not ship one.

Polish dispatch: when the dispatcher skips `review` because a previous
review pass already returned `SUCCESS`, this skill MUST itself
synthesise the updated `state.ui_review.findings` (including any
remaining `a11y_violation` entries) so the engine's gate sees the
current state on the next polish round.

## Gotcha

- `@include` shares parent scope — components don't. Know the difference.
- Always use Tailwind utility classes — not inline styles.
- Don't put business logic in templates — use view composers or Livewire.

## Taste Dials

When `DESIGN.md` declares `## Taste Dials`, honour them: Variance → layout-family spread + asymmetry tolerance; Motion → animation budget + reduced-motion posture; Density → spacing scale + information-per-viewport. Absent → follow the design brief's inferred dials.

## Do NOT

- Do NOT use `{!! !!}` with user input — XSS risk.
- Do NOT put business logic in Blade templates — use Livewire or view composers.
- Do NOT use inline styles — use Tailwind utility classes.

## Anti-slop

Before shipping a Blade view, pull
[`docs/guidelines/design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md)
and scan Visual / Typography / Layout — the Blade markup is where side-stripe
accents (V1), icon-tile feature cards (T3), and the centered-hero + 3-column
template (L1/L2) concretely land. Stack-specific Tailwind class/hex bans live in
[`tailwind-engineer`](../tailwind-engineer/SKILL.md).

## Auto-trigger keywords

- Blade template
- Blade component
- Laravel view
- partial
- view logic
