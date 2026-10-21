---
name: multi-agent-orchestration
description: Execute authorized agent work with explicit ownership and integration checks. Triggers on "parallel agents", "并行 agent".
---

# Multi-Agent Orchestration

## When to use

- Execute authorized agent work with explicit ownership and integration checks.

**Not for:** breakdown for decomposition; implement for single-agent work.

## Steps

1. Confirm delegation is authorized and supported; use it only when isolation or concurrency earns the overhead.

2. Separate dependencies and independent tasks; assign file and state ownership so writers do not collide.

3. Provide goals, inputs, decisions, boundaries and verification targets; describe actual shared context and filesystem capabilities.

4. Inspect returned diffs and rerun checks before integration; reconcile assumptions and verify the whole result.

## Verify

- Ownership and dependencies are explicit; integration is checked independently of agent claims.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/dispatch-patterns.md](references/dispatch-patterns.md) — when to fan out vs sequence, context-construction templates, review-checkpoint patterns, common failure modes (race conditions, context-starved subagents, unverified seams).
