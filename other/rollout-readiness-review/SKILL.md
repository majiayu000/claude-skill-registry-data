---
name: rollout-readiness-review
description: Review cross-cutting operational readiness after implementation and before deployment. Use when a concrete change may alter runtime prerequisites, failure visibility, deployment order, rollback, recovery, or production failure modes.
---

# Rollout Readiness Review

Assess repository-local deployment readiness without performing or implying a live rollout.

## Workflow

1. Confirm the concrete change, target environment class, available evidence, and whether the task is repository review or explicitly authorized live verification.
2. Identify the runtime delta, required configuration and permissions, startup and shutdown behavior, background work, migration order, and partial-state risk.
3. Determine how failures appear through existing signals and how an operator verifies success.
4. Check the mixed-version window: during a deploy, old and new versions run side by side, so each must work with the data, messages, and configuration that the other writes. Check that the previous version can still run against the state the new version leaves; if it cannot, rollback is not available, and the result must say so.
5. Define the smallest safe deployment order, rollback conditions, and recovery path.
6. Delegate IaC blast radius to `infra-review`, trust-boundary risk to `security-review`, dependency provenance to `dependency-review`, documentation drift to `docs-drift-review`, and verification gaps to `test-gap-review`.
7. Run only trusted non-mutating repository checks unless the enclosing task separately authorizes implementation or live verification.

Report the runtime delta, prerequisites, failure visibility, success evidence, deployment order, rollback and recovery, blocking findings, residual risk, and confidence limits. State directly when no readiness finding exists.

Keep the review read-only by default. Never apply, deploy, execute migrations, change secrets or permissions, modify external systems, or claim production readiness from unavailable live evidence without explicit authority.

Finish when the required readiness answers are evidenced or explicitly inconclusive.
