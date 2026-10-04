---
name: review-brand
user-invocable: false
version: 1.1.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal brand & copy review pass of the agentic-workflow review pack — composed
  in-turn by review-change and product-audit; not a menu entry. Checks changed
  user-facing copy against the project's brand doc: voice, terminology, and
  honesty of claims — applies only to surfaces with user-facing text. Findings
  only; never edits code.
---

# Review Brand & Copy (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The diff or path/glob the caller passes; default the current change vs the
default branch. State the scope at the top of the returned table.

## Checklist (evaluate EVERY item — none is optional; n/a must be stated)

- ✓ Read the project's brand doc first (e.g. `docs/brand/BRAND.md`) — cite the
  rule for every finding; n/a all items if the project has none and say so
- ✓ Tone of changed copy matches the declared voice (cite the guideline violated)
- ✓ Product/domain terms used consistently with the declared glossary (same
  concept, same word, same capitalization)
- ✓ No forbidden/deprecated phrases from the brand doc
- ✓ Claims are honest: limits, restrictions, and reductions the code enforces
  are disclosed in the copy (an undisclosed limitation is a major finding —
  repo hard rule)
- ✓ Error/empty-state copy is actionable (says what happened and what to do),
  not blame-y
- ✓ Consistency across the changed surface and its siblings (same action
  labeled the same way everywhere)
- ✓ Placeholder/lorem text absent from the diff

## Materiality bar

Report a row only when a competent user's outcome changes or a rule the project
explicitly declares is violated — cite the rule it violates beside the evidence.
Not findings: comment/punctuation typos, formatting-only drift, style preference
with no cited rule, hypothetical robustness beyond the SPEC's named scenarios.
An empty table with `Decision: PASS` is the expected result for a well-formed
change — never pad the table.

## Return exactly

```
REVIEW BRAND — scope: <scope>

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
