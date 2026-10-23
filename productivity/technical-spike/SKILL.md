---
name: technical-spike
description: Resolve one correctness-blocking external or version-specific technical uncertainty through bounded investigation. Use when cheap local inspection cannot establish framework, library, tool, runtime, protocol, or platform behavior needed by the current task.
---

# Technical Spike

Own extended technical investigation while the calling workflow retains its planning, implementation, or validation decision.

## Workflow

1. State the exact question, applicable versions, decision it blocks, and stopping condition.
2. Check local manifests, lockfiles, configuration, code, tests, installed versions, and command help first.
3. When local evidence is insufficient, use the most authoritative relevant primary source: official documentation, specifications, upstream source, release notes, or a bounded reproduction.
4. Read public documentation and upstream source when the host allows network access, and never put private repository or customer data in a query. Require explicit authority before dependency changes, repository edits, external writes, or experiments with side effects. Keep temporary reproductions outside the repository unless the task authorizes a durable test.
5. Separate observed facts from inference and record only conclusions that affect the current task.
6. Translate evidence into concrete design, compatibility, implementation, or verification implications.

Report the question, applicable versions, local and external source references, observed facts, inference, conclusion, task impact, remaining uncertainty, and stopping decision.

Do not research adjacent features, upgrade dependencies, add abstractions to hide uncertainty, or present unresolved behavior as confirmed. Return unresolved uncertainty as a blocker or explicit risk.

Finish when the current task has a supported path forward or further evidence requires new authority or unavailable state.
