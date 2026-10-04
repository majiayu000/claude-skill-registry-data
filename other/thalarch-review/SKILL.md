---
name: thalarch-review
description: >
  Runs risk-sized, evidence-first review of code changes. Use before completion, PR creation, or
  after meaningful implementation. Separates requirement compliance from engineering quality,
  uses independent reviewer contexts and perspective shifts to break self-review blind spots,
  confirms findings before fixing them, and supports lite, standard, and deep review depth.
---

# Thalarch Review

Review exists to find **real** defects and risk, not to manufacture criticism.

## 1. Review depth

### Lite

Small/low-risk diff: one independent general reviewer.

### Standard

Meaningful code change:

- requirement/spec compliance;
- correctness/regression/maintainability.

### Deep

Add only the lenses justified by the changed surface:

- security;
- performance/concurrency;
- persistence/data;
- API/compatibility;
- language/platform specialist;
- UI/design/vision;
- CI/release.

Do not invoke a council for ceremonial thoroughness.

## 2. Lens — specification compliance

For every acceptance item mark:

- `PASS`;
- `FAIL`;
- `UNVERIFIED`;
- `OUT OF SCOPE`.

Check for missing behavior and unrequested changes.

## 3. Lens — correctness/regression

Inspect as relevant:

- lifecycle/state ownership;
- boundaries and edge cases;
- async/concurrency/cancellation;
- resource cleanup;
- persistence/migrations;
- network timeout/retry/idempotency;
- API/ABI/wire compatibility;
- dependency/version assumptions;
- test validity;
- consumer/caller behavior.

## 4. Blind-spot breakers

When the reviewer may share the author's mental model, deliberately change perspective. Use only
what helps the current diff.

### Contract-before-body

For an important changed function/class/interface, state its expected contract **before** reading
the implementation in detail. Then compare implementation to that contract.

### Consumer-first

Inspect at least one real caller/consumer for public or cross-module changes. Ask what assumptions
the consumer makes that the implementation may have broken.

### Failure-first

For external I/O/framework/database/process calls ask what happens on failure, timeout,
cancellation, duplicate execution, malformed response, partial completion, or unavailable
resource — then check only the cases the contract actually needs to handle.

### Production-breaker perspective

Try to construct a concrete input/interleaving/state transition that breaks the changed behavior.
A concern without a plausible path remains a question, not a defect.

### New-maintainer perspective

Ask whether a future maintainer can recover the invariant from names, types, tests and nearby
structure, and whether the change introduced a second competing pattern.

### Bottom-up pass

For tricky diffs, optionally read from low-level helpers/callees back toward the entry point. This
can expose assumptions hidden by the author's top-down narrative.

### Removal test

Ask: if this changed block/file were removed or reverted, which acceptance criterion would fail?
This can expose dead/speculative code or tests that do not actually depend on the implementation.

These techniques **must not force a finding**. A clean review is valid.

## 5. Security lens

When relevant use `thalarch-security` or a stronger installed security specialist selected by
skill intelligence.

Security findings require a credible trust-boundary/source-to-sink or authorization failure path.

## 6. Performance/concurrency lens

When relevant use `thalarch-performance`, `thalarch-jvm-concurrency`, or the matching platform
specialist.

Look for repeated/unbounded work, blocking I/O, hot-path allocation/copying, N+1/fan-out,
contention/race/lifecycle problems, cache growth/invalidation, or expensive rendering.

A “performance smell” is a lead until a hot path/workload or concrete resource risk is established.

## 7. Finding contract

A confirmed finding must include:

- severity proportional to impact;
- path/location;
- violated requirement/invariant;
- concrete failure mode/counterexample;
- evidence;
- minimal remediation;
- verification that would prove the remediation.

Low-confidence speculation is labeled `QUESTION`/`RISK`, not promoted to a defect.

Do not inflate severity because multiple reviewers repeated the same unsupported assumption.
Independent agreement increases confidence only when they identify the same evidence-backed path.

## 8. Review mechanical evidence

Use deterministic project tools when available:

- compiler/type checker;
- linter/static analyzer;
- test runner;
- dependency/build analysis;
- code-quality/risk scripts;
- architecture/dependency graph tools.

Script output is a queue of leads, not a verdict. Confirm material findings in source/runtime.

Do not invent universal complexity/line-count scores when the repository has no such policy.

## 9. Test review

For new/changed tests ask:

- which contract does this prove?
- what realistic broken implementation would still pass?
- does a mock replace the exact boundary the acceptance criterion needs to prove?
- was an assertion weakened/deleted merely to accommodate the implementation?
- are negative/boundary/concurrency cases appropriate to the risk?

Coverage percentage alone is not evidence of assertion quality.

## 10. Fix loop

Only confirmed findings enter the fix queue.

- batch compatible issues;
- apply the smallest corrections;
- rerun invalidated checks;
- re-review affected surface;
- expand review only if the fix changes architecture/contract/risk.

Do not enter an infinite “review until a reviewer invents nothing else” loop.

## Final review output

Report:

- acceptance matrix status;
- confirmed findings by severity;
- questions/risks separately;
- checks executed;
- affected specialist lenses used;
- residual `UNVERIFIED` areas.

`CLEAN` is an acceptable result when no evidence-backed defect remains.
