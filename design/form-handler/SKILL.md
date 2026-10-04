---
model_tier: medium
name: form-handler
description: "Use when designing or reviewing a form — validation timing, error display, submission lifecycle, optimistic UI, dirty/pristine state, idempotency — even on 'why does submit double-fire?'."
personas:
  - frontend-engineer
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# form-handler

> Pick the validation timing, lay out error placement, sequence the
> submission lifecycle, and decide where (and whether) to use
> optimistic UI. Stack-agnostic — Livewire, Inertia, React Hook Form,
> server-rendered Blade — the lens is the same. Pair with
> [`laravel-validation`](../laravel-validation/SKILL.md) for
> server-side rules and [`accessibility-auditor`](../accessibility-auditor/SKILL.md)
> for label / error a11y.

## When to use

- A new form is being designed (login, signup, settings, multi-step
  wizard) and the validation strategy is unsettled.
- A form bug shows up: double-submission, lost data on validation
  fail, error not announced, optimistic update flicker.
- A wizard or multi-step flow needs state across steps and the
  ownership of dirty / pristine state is unclear.
- German triggers: "Formular bauen", "wann validieren?",
  "Submit feuert doppelt".

Do NOT use when:

- The screen is read-only / display-only — no form, skip.
- The question is purely server-side validation rules — route to
  [`laravel-validation`](../laravel-validation/SKILL.md) (or the
  stack equivalent).
- The question is form *layout* / spacing — route to
  [`fe-design`](../fe-design/SKILL.md) or
  [`tailwind-engineer`](../tailwind-engineer/SKILL.md).

## Procedure

### 1. Identify field types, pick validation timing

Inspect every field on the form (text, password, async-checked,
file, multi-step) before choosing timing. Three knobs, picked per
field:

| Timing | When |
|---|---|
| On submit only | Forms with privacy concerns (passwords); short forms |
| On blur | Default — feedback when the user finishes the field |
| On change (debounced) | Typing-feedback fields (username availability, password strength) |

Avoid validate-on-change for the whole form — premature errors
shame the user. Username-availability is the canonical exception.

### 2. Lock the error display contract

Per field: error message location (below field), text-based
(never colour-only), `aria-describedby` wired, focus moves to
**first** error on submit-fail. Per form: a summary box at top
that lists every error with anchor links — required for forms
> 5 fields and any wizard step.

### 3. Sequence the submission lifecycle

Order matters; bake into one helper:

1. Disable the submit button (idempotency).
2. Run client-side validation; bail on failure with focus to
   first error.
3. Mark optimistic state if applicable (step 5).
4. POST to server.
5. On 2xx: clear dirty state, show success, route or reset.
6. On 4xx: surface field errors per the display contract; restore
   submit button; **do not** lose user input.
7. On 5xx: keep input, show retry CTA, log to error tracker.

A submit handler that skips step 1 is a duplicate-record bug
waiting to fire on slow networks.

### 4. Decide on optimistic UI per action

Optimistic UI is only safe when **rollback is cheap and visible**:
toggling a like, marking read, in-list reorder. It is unsafe for:
multi-field forms, money movements, anything with downstream
notifications. Default to non-optimistic; opt in per action with
a documented rollback path.

### 5. Track dirty state and unsaved-changes guard

Pristine = identical to the server's last-known value. Dirty =
any difference. On route-leave with dirty form, prompt
confirmation (browser `beforeunload` for full nav, in-app modal
for client-side route changes). For wizards, dirty state is
per-step; submit at step N validates only that step's fields,
final submit re-validates the whole payload server-side.

## Output format

Return:

1. Validation contract — per-field timing + error-display rules.
2. Submit lifecycle — the 7-step sequence with any deviations called out.
3. Risk surface — optimistic-UI rollback path, dirty guard, idempotency,
   server contract (endpoint, status codes, error shape).

Concrete shape:

```
Form:               <name / route>
Validation timing:  per field — <field: timing>
Error display:      below field + summary box (≥ 5 fields)
Submit lifecycle:   <list of steps 1–7 with any deviations>
Optimistic UI:      <none | per action — list with rollback path>
Dirty guard:        <yes/no — and the route-leave hook>
Idempotency:        <strategy — disable + token? request id?>
Server contract:    <endpoint, status codes, error shape>
```

## Gotcha

- Disabling the submit button without showing a spinner reads as
  "broken UI"; pair the disable with a visible busy state.
- Validation-on-change for a password creates a bad UX: errors
  appear before the user has finished typing. Validate-on-blur
  with a single re-validate-on-change *after* the first failure.
- Optimistic UI + slow network = the user sees success then a
  rollback; that is worse than waiting. Pick optimistic only when
  the request is < 300 ms p95.
- Wizard "save & continue" buttons that POST per step double the
  failure surface; only do this if the back-end can resume.
  Otherwise hold state client-side and POST once at the end.

## Do NOT

- Do NOT trust client-side validation alone; server-side is the
  contract. Client-side is UX, not safety.
- Do NOT clear the form on validation failure; the user's input
  is sacred until the server says it is safely saved.
- Do NOT use colour as the only error signal; that is both an a11y
  failure and a print / colour-blind regression.
- Do NOT enable optimistic UI by default; the rollback story has
  to fit on one line, or it does not ship optimistic.
