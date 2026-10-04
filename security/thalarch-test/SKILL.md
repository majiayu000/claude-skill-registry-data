---
name: thalarch-test
description: >
  Designs high-value regression, property, integration, fuzz, and risk-based mutation tests for
  behavior changes. Use after a root cause is known or a feature contract exists. Focuses on tests
  that can actually falsify the implementation, negative/error paths, red-green proof, boundary
  matrices, and avoiding mock-heavy tests that merely restate implementation details.
---

# Thalarch Test

Testing exists to falsify the implementation, not to decorate the diff or chase a vanity metric.

## 1. Test selection

Prefer the cheapest layer that proves the contract:

1. pure/unit;
2. property/state-machine/model test;
3. component/module;
4. integration with the real boundary;
5. device/browser/end-to-end.

Move upward only when the lower layer cannot prove the behavior. Do not substitute a lower layer
for an acceptance criterion that fundamentally lives higher in the stack.

## 2. Quality rules

A useful test:

- asserts user- or contract-visible behavior;
- fails for a meaningful broken implementation;
- controls unrelated nondeterminism;
- covers the actual regression mechanism or invariant;
- has a clear reason for its layer;
- does not merely mirror private implementation details;
- does not pass only because a mock returns the answer configured into it.

For bug fixes, prefer red-green proof:

1. reproduce the original failure;
2. prove the test/check fails for the broken behavior when practical;
3. apply the fix;
4. rerun the same proof;
5. run nearby regressions.

## 3. Spec traceability

For non-trivial features, map acceptance criteria to tests/checks. Each important criterion should
have at least one proof at the layer where the criterion is observable.

Do not create a new permanent `specs/` convention unless the repository already uses one or the
user requested it. Traceability can live in the task/evidence ledger.

## 4. Boundary matrix

For parsers, indexing, pagination, ranges, state transitions, concurrency, validation, or data
conversion, enumerate meaningful cases before implementation/testing:

- empty / one / many;
- minimum / maximum / just outside boundaries;
- null/absent/optional states where the contract permits them;
- duplicate/reordered input;
- Unicode/encoding/byte boundaries where relevant;
- timeout/cancellation/retry;
- repeated/idempotent operations;
- concurrent interleavings when state is shared.

Do not manufacture irrelevant cases just to increase test count.

## 5. Property and metamorphic testing

When behavior has strong invariants and the repository already has or justifiably needs the
required tooling, prefer properties over a long list of hand-picked examples.

Examples:

- encode/decode round trip;
- parse/serialize stability;
- sorting preserves elements and order invariant;
- normalization is idempotent;
- cache result equals uncached result;
- optimized implementation agrees with a simple reference model;
- adding irrelevant input does not alter an independent output.

Use the ecosystem actually compatible with the project — Hypothesis, jqwik/QuickTheories, Kotest
property, Go fuzzing, proptest/quickcheck, fast-check, or equivalent — only when present or when
adding it is justified by the task.

## 6. Fuzzing

Fuzz parsers, codecs, protocol/state-machine boundaries, file formats, untrusted input handlers,
and serialization when malformed or adversarial input is a real risk.

A discovered fuzz failure becomes a small deterministic regression case before completion.

Do not run network/security fuzzing against systems without authorization.

## 7. Concurrency tests

Avoid real sleeps as synchronization when controllable schedulers, latches, barriers, virtual
time, deterministic dispatchers/executors, or test hooks can prove the ordering more reliably.

A flaky test is not acceptable evidence. Diagnose the race or make synchronization explicit.

For JVM-specific concurrency bugs, combine with `thalarch-jvm-concurrency`.

## 8. Mutation testing — use selectively

Coverage tells whether code executed; mutation testing can reveal whether assertions would notice
a realistic semantic change.

Consider mutation testing when:

- code is security/data/financial/authorization critical;
- a parser/validator/state machine has deceptively high line coverage;
- a regression escaped an apparently well-covered suite;
- assertions appear weak;
- the project already has a mutation framework configured;
- the user explicitly asks for stronger test-quality evidence.

Possible existing ecosystems include PIT/Pitest (JVM), Stryker (JS/TS), mutmut/cosmic-ray style
Python tooling, or project-specific equivalents.

Do **not** install a mutation framework merely to satisfy ritual coverage unless dependency/tooling
changes are justified and authorized.

Do not enforce a universal mutation-score threshold. Evaluate surviving mutants by risk and the
behavior they reveal.

For a surviving meaningful mutant:

1. identify the missing invariant/assertion;
2. add the smallest behavior test that kills it;
3. verify the new test fails for the mutant/broken behavior;
4. keep the test only if it expresses a real contract.

Generated nonsense/equivalent mutants are not defects in the test suite.

## 9. Coverage discipline

Coverage reports can prioritize unexecuted risk, but percentage alone is not a completion target.

Prioritize uncovered paths by:

- user/business criticality;
- error/security paths;
- boundary complexity;
- change frequency/regression history;
- concurrency/persistence/network risk.

Do not add low-value tests merely to raise a global percentage.

## 10. Mutation-strength question

Even without a mutation tool, ask:

> What realistic broken implementation would still pass this test?

If the answer is easy to name, strengthen the assertion, data, or test layer.

## 11. Mock boundary

Mocks/stubs are useful for isolating local behavior. They do not prove the external integration they
replace.

Use a real integration/container/device/browser boundary when the acceptance criterion depends on
framework/DB/network/serialization/runtime behavior.

## 12. Report

For every material test/check state:

- what contract it proves;
- which failure/regression it would catch;
- what it does not prove;
- whether it ran successfully in the current environment;
- property/fuzz/mutation evidence when used;
- residual `UNVERIFIED` integration/runtime surfaces.
