---
name: engram-eval
description: Design and maintain engram memory quality evaluations. Use when creating evaluation fixtures, expected recall tests, forbidden recall tests, ranking checks, policy/forgetting checks, belief or hierarchy regression cases, or evaluation harness APIs.
---

# Engram Eval

Use this skill when defining or changing how engram proves memory quality. Evaluations should cover correctness, safety, ranking quality, source grounding, and regression behavior across memory, knowledge, belief, and hierarchy features.

## Required Context

Read these files before eval work:

- `docs/domain-data-model.md`
- `docs/architecture.md`
- `docs/research/synthesis.md`
- `references/evaluation-patterns.md`

## Evaluation Principles

- Every retrieval feature needs a positive recall case and a negative leakage case.
- Policy, forgetting, redaction, and tenant isolation are correctness tests, not optional security tests.
- Ranking tests should assert stable ordering only where the scoring contract is deterministic.
- Belief and hierarchy evaluations should check evidence links and contradiction handling, not just returned text.
- Fixtures must be portable and not tied to a specific database or model provider.

## Required Eval Families

- Contract serialization round trips.
- In-memory write and retrieve.
- Scope and access isolation.
- Forgetting and retention enforcement.
- Knowledge document ingestion and chunk retrieval.
- Code knowledge ingestion and symbol/query retrieval.
- Belief derivation with evidence and contradiction records.
- Hierarchical retrieval with ancestor, descendant, and sibling expansion.
- Fusion and omitted-result explanations.

## Output

Eval work should report:

- Fixture names added or changed.
- Expected and forbidden retrieval behavior.
- Deterministic versus model-dependent assertions.
- Remaining quality gaps.
