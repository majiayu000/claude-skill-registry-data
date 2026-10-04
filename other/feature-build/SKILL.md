---
name: feature-build
description: Use for a bounded product feature or vertical slice; convert acceptance criteria into a smallest complete implementation that is verified across applicable UX, correctness, security, runtime, and operations boundaries.
---
# Feature Build

1. Start from the user outcome and task contract, not a component list.
2. Inspect existing patterns and choose the smallest compatible architecture.
3. Define happy path plus loading, validation, empty, error, permission, retry, and degraded states that apply.
4. Map data/auth/external-provider boundaries before editing.
5. Implement one vertical slice end to end.
6. Add deterministic regression/contract tests for important rules.
7. If user-facing web, invoke `runtime-verification` before completion.
8. If AI-backed, invoke `ai-provider-routing` and `ai-integration-verification`.
9. Record required checks and pass `evidence_gate.py` before declaring completion.
