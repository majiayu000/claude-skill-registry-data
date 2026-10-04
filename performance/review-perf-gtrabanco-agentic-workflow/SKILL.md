---
name: review-perf
user-invocable: false
version: 1.2.0
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Internal performance review pass of the agentic-workflow review pack — composed
  in-turn by review-change and product-audit; not a menu entry. Checks the
  changed paths for algorithmic and resource regressions: N+1s, hot-path
  allocations, asset weight, and leaks. Findings only; never edits code.
---

# Review Performance (internal)

Composed by `review-change` / `product-audit` within their conversation — on any
agent, follow this file inline as the routed step. **Findings only; never edits,
never refactors.**

## Scope

The diff or path/glob the caller passes; default the current change vs the
default branch. State the scope at the top of the returned table.

## Checklist (evaluate EVERY item — none is optional; n/a must be stated)

- ✓ No N+1 query/IO pattern on changed data-access paths (loop bodies issuing
  queries/requests — cite)
- ✓ Algorithmic complexity of new code paths stated where input can grow (an
  unbounded O(n²) on user data is a major finding)
- ✓ No blocking IO/sync work added on hot/request paths where the platform is
  async
- ✓ Resources opened by the change are closed/released on ALL paths including
  errors (files, connections, subscriptions, timers)
- ✓ No unbounded growth introduced (caches without eviction, arrays that only
  append, listeners never removed)
- ✓ Web only: bundle/asset impact of the change stated (new dep size, image
  weight, lazy-loading where the project uses it) — n/a otherwise
- ✓ Repeated computation hoisted where a loop recomputes an invariant (cite)
- ✓ Pagination/limits on any new listing that reads user-scaled data
- ✓ No premature optimization either: complexity added for speed without a
  cited measurement is a finding (the repo forbids overengineering)
- ✓ **Measured evidence when declared** — the project's agent guide declares a
  `Performance commands` block with a `bench` command AND the diff touches
  paths its benchmarks cover: RUN the benchmark on the base branch and on the
  change, and cite both numbers in Evidence as
  `<cmd> → base <x> / change <y> (<±z%>)`. A regression beyond the noise band
  (the project's declared band, else ±5%) is a **major** finding; a delta
  inside the band is no finding. The declared command failing (non-zero exit)
  is itself a finding (the gate can't measure) — never silently skipped.
- ✓ **No declared perf commands** → state exactly
  `n/a — no declared perf commands` for the item above (never skip it
  silently), and if the diff adds algorithmic code on input that can grow,
  add a **minor** finding recommending the project adopt the tooling via
  `init-workspace`'s Performance tooling round.

## Materiality bar

Report a row only when a competent user's outcome changes or a rule the project
explicitly declares is violated — cite the rule it violates beside the evidence.
Not findings: comment/punctuation typos, formatting-only drift, style preference
with no cited rule, hypothetical robustness beyond the SPEC's named scenarios.
An empty table with `Decision: PASS` is the expected result for a well-formed
change — never pad the table.

## Return exactly

```
REVIEW PERF — scope: <scope>

| # | Finding | Sev | Evidence | Suggested fix |
|---|---------|-----|----------|---------------|
| 1 | <what>  | critical|major|minor | <file:line — or, for measured findings, `<cmd> → base <x> / change <y> (<±z%>)`> | <smallest action> |

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
