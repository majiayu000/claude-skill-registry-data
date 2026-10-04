---
name: review-design
user-invocable: false
version: 1.1.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal UI/UX design review pass of the agentic-workflow review pack —
  composed in-turn by review-change and product-audit; not a menu entry.
  Checks the changed UI against the project's design doc: consistency, states,
  responsiveness, and reuse — applies only when the project has a UI and the
  change touches it. Findings only; never edits code.
---

# Review Design (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The diff or path/glob the caller passes; default the current change vs the
default branch. State the scope at the top of the returned table.

## Checklist (evaluate EVERY item — none is optional; n/a must be stated)

✓ Read the project's design doc first (e.g. docs/frontend/DESIGN.md) — cite the rule for every finding
✓ Changed components reuse the design system (no one-off styles/colors/spacing duplicating existing tokens or components)
✓ Every new/changed view handles ALL states: loading, empty, error, success (cite each)
✓ Responsive behavior stated and honored at the project's breakpoints (n/a if the platform has none)
✓ No hardcoded user-facing strings where the project declares i18n (cite the i18n doc)
✓ Visual hierarchy: primary action distinguishable, one primary action per view
✓ Consistency with sibling screens (same patterns for the same interactions — cite the diverging sibling)
✓ Destructive actions require confirmation and are visually distinct
✓ Feedback on every user action (submit, save, fail) — no silent operations

## Materiality bar

Report a row only when a competent user's outcome changes or a rule the project
explicitly declares is violated — cite the rule it violates beside the evidence.
Not findings: comment/punctuation typos, formatting-only drift, style preference
with no cited rule, hypothetical robustness beyond the SPEC's named scenarios.
An empty table with `Decision: PASS` is the expected result for a well-formed
change — never pad the table.

## Return exactly

```
REVIEW DESIGN — scope: <scope>

| # | Finding | Sev | Evidence | Suggested fix |
|---|---------|-----|----------|---------------|
| 1 | <what>  | critical|major|minor | <file:line> | <smallest action> |

Checklist: <n> evaluated, <n> pass, <n> findings, <n> n/a (<which + why>)
Summary: <1-2 sentences>
Decision: PASS | FAIL
```

FAIL if any critical or major finding is open; PASS otherwise. Minor findings
never block — they route to the caller's triage step.

## Done when

- Every checklist item was evaluated with evidence (file:line or command output)
  or explicitly marked n/a with the reason.
- The fixed-format block above is returned — nothing more, nothing less — and
  no code was changed.
