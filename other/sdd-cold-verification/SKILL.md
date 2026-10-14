---
name: sdd-cold-verification
description: "Trigger: cold verification, verify run.md, SDD verification, behavior acceptance. Verify scoped implementation independently against every source scenario and required check."
license: MIT
metadata:
  author: andresnator
  version: "3.0.0"
  status: testing
---

# SDD Cold Verification

## Activation Contract

Load for independent, read-only acceptance of exact SDD run scenarios and required checks. Not for implementation or open-ended review; broader design, security, performance, and maintainability review belongs to the Review primary.

## Required Brief

- Exact `.ai/orchestration/runs/<slug>/` root and its `run.md`.
- Exact immutable plan path and the SHA-256 recorded in `run.md` when it references one.
- Complete source scenario list, including every id and `WHEN`/`THEN` pair.
- Complete source `Files:` scope.
- Complete source `Verify` checklist.
- Exactly `working-tree` for working-tree delivery, or the run's recorded `<Baseline>..HEAD` for commit-per-unit delivery.

Missing or contradictory input blocks verification. Never infer a run root, plan, hash, scope, scenario, check, or baseline.

## Method

1. Read `run.md`. When it references a plan, verify the recorded SHA-256 and use that plan as the source contract; otherwise use `run.md`.
2. Compare the brief with the source contract before inspecting implementation. Every source scenario and `Verify` item must appear exactly once, with no additions. The `Files:` scope must match exactly. Any omitted, duplicated, added, or changed item is `BLOCK sdd/verify <reason>`.
3. Build separate scenario and check ledgers. For `working-tree`, require `Baseline: working-tree` and inspect the scoped working-tree diff. For `commit-per-unit`, require the left side of the range to equal the full SHA on `Baseline:`, require the right side to be literal `HEAD`, and inspect only that range and the `Files:` scope. Never substitute an inferred merge base, first commit, or working-tree diff.
4. Trace each `WHEN` through its stimulus to the observable `THEN`; cite scoped `path:line` evidence or a focused check.
5. Run every applicable read-only `Verify` item fresh. A check is read-only when it does not edit tracked files, the plan, run state, or Git. Count unavailable, unauthorized, or non-read-only items as failed checks; never omit them. Additional probes may narrow a failure but never replace a required check.
6. For hardening or characterization, setup, stimulus, and assertion must independently detect the named regression. A green but tautological test is a failed scenario. Run mutation or coverage only when the source contract names an available command.
7. Recheck the plan hash when present. Count every scenario and every `Verify` item separately. One unsupported, contradicted, or failed item makes the result fail.

## Boundaries

- Ignore unrelated working-tree changes and paths outside the brief.
- Ignore `.ai/` state because it is outside the implementation `Files:` scope and must never appear in a delivery commit.
- Do not turn conventions, security, performance, or design preferences into acceptance failures unless an assigned scenario or check requires them.
- Never edit, write state, ask, delegate, stage, commit, push, or mutate graph lifecycle.

## Output Contract

Return each failed scenario or check with evidence, then exactly one final line:

```text
PASS scenarios=<passed>/<total> checks=<passed>/<total> evidence=<pointer>
FAIL scenarios=<passed>/<total> checks=<passed>/<total> evidence=<pointer>
```

Use `PASS` only when both ledgers pass completely. Never return logs, code, diffs, or praise.
