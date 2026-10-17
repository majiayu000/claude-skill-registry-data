---
name: property-testing-current
description: Design, review, or debug property-based tests for parsers, codecs, normalization, numeric algorithms, collections, or controlled stateful workflows. Use when generated inputs and independent behavioral contracts can expose meaningful defects; preserve the project's existing library and runner.
license: CC-BY-SA-4.0
compatibility: Python controls are qualified with Python 3.14.8 and Hypothesis 6.168.3. Other languages, libraries and external-system state machines require their own API and runtime checks.
metadata:
  source: trailofbits/skills
  revision-status: experimental-unbenchmarked
---

# Properties that distinguish correct behavior

Read the relevant contract, implementation and existing tests. Choose properties
from external format rules, independently specified behavior or a simpler
reference model. State the valid domain and expected error behavior separately.
Use example tests for known regressions and exact format vectors alongside
generated tests. Do not add a dependency, inverse API or production refactor
solely to satisfy a testing template; make changes justified by the task.

## Check the oracle before increasing the budget

Ask which plausible wrong implementation each assertion rejects. Exercise
representative mutants or explicit wrong-outcome fixtures when valuable. An
independent simple expression can be a valid oracle even when it resembles the
implementation; comparing an expression with itself cannot constrain it.

Property strength depends on the contract. Roundtrips can hide defects shared
by both directions; add independently known encodings or an external decoder
when interoperability matters. Idempotence accepts constant output; add content
preservation or semantic examples. Sorting needs order and multiset preservation,
including duplicate counts. Do not rank every roundtrip above every invariant.

Check reference independence and supported input semantics. A reference can
share a bug, omit overflow or normalization rules, or disagree intentionally
with the target. Record those limits rather than scoring either implementation
as correct by default.

## Generate the relevant domain

Use direct constraints and compositional strategies for valid inputs; generate
invalid inputs separately for validation/error contracts. Reserve filtering or
assumptions for conditions difficult to construct directly. Keep health checks
enabled and report exhausted or unsatisfiable generation as failure, not a pass
or a low-priority warning.

Match numeric bounds, Unicode/surrogate rules, collection types, duplicate
semantics and size/depth limits to the contract. Use full-match regex generation
when the entire value must match. Include boundary and regression examples.
Avoid restricting inputs merely because they reproduce a real defect.

For controlled stateful systems, generate operation sequences against a small
independent model. Reset the implementation and model between examples. In-place
APIs can be tested using a captured pre-state without changing the public API.
Isolate network, filesystem and database effects in owned fixtures.

## Reproduce and report

Pin library and runtime identities. Choose example counts, sequence lengths and
external time/resource bounds based on the actual workload. A seed controls
generation; it does not request more examples. Removing an example deadline
does not provide process-level protection against hangs.

Retain minimized inputs and regression tests. Control clocks, randomness and
shared state; investigate flaky outcomes. Classify a failure as implementation,
oracle/strategy, infrastructure or unresolved contract, with evidence. Respect
supported platform contracts when a failure is platform-specific.

Report executed domain and budget, failed/skipped/not-run work, actual versions
and retained counterexamples. Finite generated examples and mutation scores do
not prove exhaustive correctness or an agent efficacy gain. See
[qualified controls](references/controls.md).
