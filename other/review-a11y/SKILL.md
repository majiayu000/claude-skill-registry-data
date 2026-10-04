---
name: review-a11y
user-invocable: false
version: 1.1.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal accessibility review pass of the agentic-workflow review pack —
  composed in-turn by review-change and product-audit; not a menu entry.
  Checks the changed user-facing surface for accessibility: semantics,
  keyboard, focus, contrast, and ARIA correctness — applies only to
  user-facing surfaces. Findings only; never edits code.
---

# Review Accessibility (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The diff or path/glob the caller passes; default the current change vs the
default branch. State the scope at the top of the returned table.

## Checklist (evaluate EVERY item — none is optional; n/a must be stated)

✓ Semantic elements over generic ones (button not clickable div; headings in order; landmarks present)
✓ Every input has an associated label; every image an alt (empty alt only when decorative)
✓ Full keyboard operability of the changed surface (tab order, Enter/Space activation, Escape to dismiss)
✓ Focus management on dynamic changes (modals trap + restore focus; route changes move focus)
✓ Contrast of changed text/UI meets the project's declared level (default WCAG AA) — cite computed values where checkable
✓ ARIA used correctly and only when semantics can't do it (wrong ARIA is a major finding)
✓ No information conveyed by color alone
✓ Motion/animation respects reduced-motion preferences (n/a if no motion added)
✓ Error messages programmatically associated with their fields

## Materiality bar

Report a row only when a competent user's outcome changes or a rule the project
explicitly declares is violated — cite the rule it violates beside the evidence.
Not findings: comment/punctuation typos, formatting-only drift, style preference
with no cited rule, hypothetical robustness beyond the SPEC's named scenarios.
An empty table with `Decision: PASS` is the expected result for a well-formed
change — never pad the table.

## Return exactly

```
REVIEW ACCESSIBILITY — scope: <scope>

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
