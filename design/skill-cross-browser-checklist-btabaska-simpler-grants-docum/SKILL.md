---
name: Cross-Browser Checklist
description: "Produce a targeted manual cross-browser test checklist for a changed frontend feature, covering Chrome, Firefox, Safari (macOS + iOS), and Edge against the feature's user flows. Triggers on 'cross-browser check', 'browser matrix', 'pre-release QA'. Outputs a Markdown checklist scoped to the diff."
model: inherit
---

## Purpose

Turn an open-ended "test it in all browsers" ask into a deterministic, diff-scoped checklist. The output lists the specific flows, widgets, and interactions touched by the change so QA is focused rather than exhaustive.

## When to Invoke

- Before promoting a feature branch to staging.
- When a PR touches form controls, modals, or USWDS overrides.
- As part of a release readiness review.

## When NOT to Invoke

- Backend-only changes.
- Content-only changes (copy, translations).
- Changes already covered by a Playwright suite across browsers.

## Inputs

- **diff**: git ref range (default `origin/main...HEAD`).
- **browsers** (optional): subset, default `chrome,firefox,safari-macos,safari-ios,edge`.

## Procedure

1. Collect changed `.tsx|.ts|.scss` files from the diff.
2. Identify affected user flows by tracing route files and component usage.
3. Inspect each changed component for browser-sensitive constructs: `input[type=date]`, `<dialog>`, `position: sticky`, custom focus rings, CSS logical properties, clipboard/file APIs.
4. For each browser, emit a checklist item tailored to the flow plus any sensitive construct.
5. Flag known Safari quirks (iOS viewport units, `:has()` support floor, date input UI).
6. Output a Markdown checklist the tester can paste into the PR.

## Outputs

```markdown
Cross-Browser Checklist — PR #4321 (Opportunity Search filters)

### Chrome 120
- [ ] Filter panel opens and closes via button and Esc
- [ ] Date range picker accepts mm/dd/yyyy and keyboard entry
- [ ] Results count updates on filter change

### Safari macOS 17
- [ ] Date input falls back to native picker; value round-trips
- [ ] Sticky filter sidebar stays in viewport on scroll
- [ ] Focus ring visible on filter chips

### Safari iOS 17
- [ ] Tap target >= 44px on filter chips
- [ ] Keyboard does not obscure filter submit button
...
```

## Safety

- Read-only; produces a checklist, not test code.
- Never assumes a flow works — everything is a tester action.
- Flags PII-adjacent flows (login, application) with a reminder to use the staging fixture user only.

## Examples

**Example 1 — Filter feature.** Output scoped to filter open/close, date picker, sticky sidebar.

**Example 2 — Form refactor.** Output adds iOS keyboard and autofill checks.

**Example 3 — Modal introduction.** Output adds focus trap, backdrop click, Esc handling per browser.

## Related

- `.cursor/agents/visual-regression.md` — paired screenshot check.
- `.cursor/skills/skill-accessibility-check/` — run together for release QA.
- `.cursor/skills/skill-uat-checklist/` — business-level acceptance flow.
