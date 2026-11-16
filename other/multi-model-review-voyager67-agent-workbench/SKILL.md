---
name: multi-model-review
description: Use independent agents or models to challenge a design or diff. Use when the change is high-risk or a second perspective is worth the cost and the harness supports independent reviewers.
---

# Independent Multi-Model Review

Seek genuinely independent criticism, not agreement theater.

1. Freeze a review point: share the same spec, diff, and relevant context with each reviewer.
2. Assign distinct review lenses such as correctness, security, performance, API compatibility, or test coverage.
3. Ask reviewers to return concrete findings with file/line, scenario, impact, and evidence. Ask them to distinguish facts from speculation.
4. Deduplicate findings and resolve disagreements against the code, tests, documentation, and requirements.
5. Reproduce high-severity findings where safe. Record false positives with the reason.
6. Fix only validated issues, then rerun review or targeted checks on the final diff.

Do not use model consensus as proof of correctness; correlated models can share blind spots. Do not disclose secrets or private data to external model providers. If the harness cannot route to independent models/subagents, perform separate review passes and state that they were not independent. No reviewer may merge or publish on the user's behalf without authorization.
