---
name: review-code
user-invocable: false
version: 1.2.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal correctness + simplification review pass of the agentic-workflow
  review pack — composed in-turn by review-change and product-audit; not a menu
  entry. Checks correctness, error handling, duplication, dead code, and
  simplification opportunities against the project's own conventions. Findings
  only; never edits code.
---

# Review Code (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The diff or path/glob the caller passes; default the current change vs the
default branch. State the scope at the top of the returned table.

## Checklist (evaluate EVERY item — none is optional; n/a must be stated)

✓ No logic errors on the changed paths (trace each modified function's inputs →
  outputs, including boundary values)
✓ Every error path is handled — no swallowed exceptions, no empty catch, no
  silently-ignored return codes
✓ No duplicated logic (a changed block does not re-implement an existing
  helper — cite the existing one if it does)
✓ No dead code introduced (unused functions, params, imports, unreachable
  branches)
✓ No leftover TODO/FIXME/HACK markers in the diff
✓ Naming and file conventions match the project's docs (read them first; cite
  the convention violated)
✓ No new abstraction beyond what the SPEC requires (an interface/base class
  with one implementation is a finding)
✓ No new dependency not justified in the SPEC
✓ Simplification: any changed block that can lose lines without losing
  behavior (cite before/after)
✓ Reference trace: every changed symbol/API got a reference search —
  un-updated callers are findings
✓ Edge cases the SPEC's dev scenarios name are actually handled in code, not
  just in tests

## Materiality bar

Report a row only when a competent user's outcome changes or a rule the project
explicitly declares is violated — cite the rule it violates beside the evidence.
Not findings: comment/punctuation typos, formatting-only drift, style preference
with no cited rule, hypothetical robustness beyond the SPEC's named scenarios.
An empty table with `Decision: PASS` is the expected result for a well-formed
change — never pad the table.

## Return exactly

```
REVIEW CODE — scope: <scope>

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
