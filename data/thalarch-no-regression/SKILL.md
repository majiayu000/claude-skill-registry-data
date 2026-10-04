---
name: thalarch-no-regression
description: >
  Defines a compact preservation contract before risky changes to working systems. Use for cache,
  playback, persistence, sync, migrations, concurrency, networking, UI state machines, or any task
  where a narrow improvement could accidentally break adjacent behavior that currently works.
---

# Thalarch No-Regression

A working subsystem is evidence. Treat preservation of its important behavior as an explicit
contract before optimizing or refactoring it.

## 1. Write the preservation contract first

Before mutation, record a compact contract:

```text
SURFACE: <subsystem>

Must preserve:
- <observable behavior/invariant>
- <observable behavior/invariant>

Suspected problem:
- <specific hypothesis>

Evidence:
- PROVEN / SUPPORTED / INFERENCE / UNKNOWN / UNVERIFIED

Action:
- AUDIT ONLY / TARGETED MUTATION

Verification:
- <tests/runtime/profiling required>
```

Keep it task-local. Do not create bureaucracy or a permanent spec file unless the repository already
uses one.

## 2. Unknown problem means audit first

If the suspected defect/inefficiency is `UNKNOWN` or only weak inference:

- inspect the actual implementation;
- trace lifecycle/state/data flow;
- measure or reproduce when feasible;
- search for the concrete failure mechanism;
- do not rewrite the subsystem merely because another project solved a similar issue differently.

When the audit does not demonstrate the suspected problem, **preserve the implementation** and
report the negative finding. A no-change outcome can be the correct engineering result.

## 3. Define blast radius

List adjacent behavior that shares the changed state, data, or lifecycle.

Examples:

- cache change → cached/uncached reads, eviction, offline mode, downloads, prefetch, seek, recovery;
- queue change → current item, duplicates, next/previous, shuffle/repeat, persistence;
- database paging → ordering, empty/partial pages, counts, search, refresh;
- UI state change → rotation, process recreation, accessibility, disabled states;
- retry change → cancellation, rate limits, idempotency, duplicate side effects.

Do not use a generic checklist when the repository proves a more specific one.

## 4. Minimal mutation rule

Once the problem is demonstrated:

- change the smallest causal surface;
- preserve existing interfaces and semantics when possible;
- avoid unrelated cleanup in the same diff;
- avoid new abstractions unless they reduce actual complexity in the changed path;
- do not upgrade dependencies/toolchains unless required by the fix;
- keep rollback/review easy.

If the proposed fix changes more behavior than the failure mechanism requires, challenge it before
implementation grows.

## 5. Falsification-first tests

Use `thalarch-test` to select proofs that would catch a realistic regression.

For a bug/performance fix, prefer:

1. reproduce or characterize the original issue;
2. capture the relevant invariant/baseline;
3. apply the narrow change;
4. rerun the same evidence;
5. exercise adjacent must-preserve behaviors.

A test that only confirms the new implementation's private structure is weak regression evidence.

## 6. Performance changes

For optimization combine with `thalarch-performance`.

Do not claim improvement from source appearance alone. Use comparable workload evidence when runtime
performance is part of the claim.

If measurement is unavailable, the optimization claim remains `UNVERIFIED` and the change should be
more conservative, not less.

## 7. Migration/deprecation changes

When changing APIs or schemas, preserve behavior separately from modernization.

- prove the exact old contract;
- prove the supported replacement/migration for the installed version;
- migrate minimally;
- verify the same observable behavior;
- avoid combining modernization with unrelated redesign.

## 8. Stop conditions

Stop expanding the change when:

- the original problem is fixed/proven absent;
- acceptance invariants pass;
- further cleanup is unrelated;
- additional refactoring would increase blast radius without evidence-backed benefit.

Finding nearby imperfections is not automatic authorization to fix them.

## 9. Completion format

Report:

```text
Preserved: <key invariants verified>
Changed: <narrow causal surface>
Not changed: <working adjacent systems intentionally preserved>
Evidence: <tests/runtime/profiling actually observed>
Residual: <remaining UNVERIFIED risks>
```

The goal is not "zero code change". The goal is **maximum demonstrated benefit per unit of regression
risk**.
