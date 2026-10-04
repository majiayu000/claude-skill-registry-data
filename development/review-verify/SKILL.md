---
name: review-verify
user-invocable: false
version: 1.1.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal run-it verification review pass of the agentic-workflow review pack —
  composed in-turn by review-change and product-audit; not a menu entry. Runs
  the project's gate and the changed behavior for real — commands, exit codes,
  observed output — instead of assuming; what cannot be executed goes to the
  manual checklist. Findings only; never edits code.
---

# Review Verify (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The diff or path/glob the caller passes; default the current change vs the
default branch. State the scope at the top of the returned table.

## Checklist (evaluate EVERY item — none is optional; n/a must be stated)

✓ The project's verification gate ran in THIS review (type-check, tests, build
  per the project's declared commands) — paste exit status per command
✓ The change's primary claimed behavior was exercised for real (run the
  CLI/endpoint/function; paste the actual observed output)
✓ At least one failure-mode from the SPEC's dev scenarios was reproduced (bad
  input, missing file, error path) and behaved as specified
✓ New/changed tests actually fail when the implementation is reverted or
  broken (mutate or stash to prove they assert something — restore after)
✓ No test was skipped/disabled to get green (grep for skip/only/todo markers
  in the diff)
✓ The build artifact/dev server starts cleanly (no new warnings that indicate
  breakage)
✓ Anything that can only be confirmed by a human (visual, device, locale,
  load) is listed explicitly under "Manual" — never silently dropped

## Materiality bar

Report a row only when a competent user's outcome changes or a rule the project
explicitly declares is violated — cite the rule it violates beside the evidence.
Not findings: comment/punctuation typos, formatting-only drift, style preference
with no cited rule, hypothetical robustness beyond the SPEC's named scenarios.
An empty table with `Decision: PASS` is the expected result for a well-formed
change — never pad the table.

## Return exactly

```
REVIEW VERIFY — scope: <scope>

| # | Finding | Sev | Evidence | Suggested fix |
|---|---------|-----|----------|---------------|
| 1 | <what>  | critical|major|minor | <file:line> | <smallest action> |

Checklist: <n> evaluated, <n> pass, <n> findings, <n> n/a (<which + why>)
Summary: <1-2 sentences>
Manual (a human must check): <bullet list, or "none">
Decision: PASS | FAIL
```

FAIL if any critical or major finding is open; PASS otherwise. Minor findings
never block — they route to the caller's triage step.

## Done when

- Every checklist item was evaluated with evidence (file:line or command output)
  or explicitly marked n/a with the reason.
- The fixed-format block above is returned — nothing more, nothing less — and
  no code was changed.
