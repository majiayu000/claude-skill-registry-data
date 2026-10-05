---
name: flow-plan
description: Decompose an approved PWDEV Flow specification into dependency-aware waves and atomic executable tasks. Use when design is approved and the user needs exact file scope, test-first actions, verification commands, and an execution gate.
---

# Plan executable work

Read [planning](../../references/planning.md), [specification](../../references/specification.md), [artifacts](../../references/artifacts.md), [memory](../../references/memory.md), and [safety](../../references/safety.md).

## Entry gate

Require an approved `spec.md`. Stop if the design gate is absent, rejected, or stale relative to requirements.

## Procedure

1. Read the full specification, decisions, repository governance, relevant code and tests, and selected conventions or lessons.
2. Map specification clauses to concrete components and file ownership.
3. Build the dependency graph and wave map before writing tasks.
4. Split work into atomic tasks using the exact contract in [planning](../../references/planning.md): at most five implementation files per task and three tasks per wave.
5. Include a failing-test step for each behavior change and exact focused and broader verification commands.
6. Mark `Parallel-safe: yes` only for disjoint files and side effects. This metadata does not authorize worker creation.
7. Check every objective, rule, quality criterion, prohibition, and definition-of-done item maps to at least one task or integration checkpoint.
8. Present wave order, dependencies, file scope, risks, and verification strategy for approval.
9. On approval, mark state `PLANNED`; otherwise revise the plans without editing production code.

## Output

Return `STATUS`, phase slug, wave count, task count, plan paths, gate result, and `NEXT`. Recommend `$flow-execute` only after explicit plan approval.
