---
name: breakdown
description: Turn agreed requirements into executable dependency-aware tasks. Triggers on "break into tickets", "拆解任务".
---

# Breakdown

## When to use

- Turn agreed requirements into executable dependency-aware tasks.

**Not for:** spec for defining scope; multi-agent-orchestration for execution.

## Steps

1. Read scope, design, current implementation and acceptance criteria.

2. Create tasks around observable outcomes or necessary structural steps.

3. Specify inputs, deliverables, dependencies, risks and concrete checks; identify critical path and safe parallelism.

4. Use available planning facilities or an inline plan; create PLAN only when persistent coordination is useful and the path is agreed.

**Output:** Suggested paths, subject to [human audit](../../../references/human-audit.md): `docs/PLAN.md`; optionally `docs/vX.Y/plan.md` for separate release planning.

## Verify

- Tasks cover acceptance without speculative additions; dependencies are acyclic and checks are concrete.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [human-audit.md](../../../references/human-audit.md) — document consent, readability and human review.
- [references/ticket-format.md](references/ticket-format.md) — local-ticket and issue templates, the staleness rule, and ticket-type routing.
