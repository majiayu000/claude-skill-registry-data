---
name: patpat-interrogate
description: Challenge architecture, designs, and changes from adversarial independent perspectives without editing.
disable-model-invocation: true
---

# Patpat Interrogate

Run adversarial multi-perspective review to stress-test designs, code changes, and unstated assumptions before delivery.

## Process

1. State Intent: Explicitly formulate the objective, target invariant, and non-goals from commit messages, task briefs, and changed contracts.
2. Determine Scope: Bind evidence to the exact candidate revision or reproducible working-tree snapshot; require a committed head only for commit- or delivery-bound claims. Never review an ambiguous or undefined scope.
3. Multi-Angle Skepticism:
   - Boundary & Security angle: Look for unsanitized inputs, unmasked credentials, missing permission gates, and denial-of-service paths.
   - Concurrency & State angle: Look for race conditions, cache incoherence, re-entrancy, and non-idempotent side effects.
   - Epistemic & Evidence angle: Look for proxy testing, mock theater, unverified assertions, and missing failure-mode tests.
   - Maintainability & Anti-Slop angle: Look for commentary replacing design clarity, duplicate abstractions, and unnecessary complexity.
4. Synthesize Findings: Order findings strictly by severity (`blocker`, `high`, `medium`, `low`). State `no findings` only when all skeptical angles are demonstrably cleared. Do not auto-apply edits.

## Mutation boundary

Remain read-only with respect to repository implementation and external delivery. Limit incidental verifier artifacts to the declared proof contract, clean them up, and hand any authorized mutation back to `patpat-loop`.
