---
name: manage-rag-default
description: Analyze a RAG task and produce guidance for choosing exactly one available Agentic RAG Skill using evidence dependencies, retrieval routes, corpus characteristics, and execution budget. Use as the first and only Skill loaded during the Manage selection stage.
---

# Default RAG Manager

Analyze the query and execution state before any Agentic or Component Skill body is loaded.

## Selection procedure

1. Determine whether the task needs retrieval and identify the evidence required for a grounded answer.
2. Classify the task as a single ordered route, a bounded iterative evidence search, or multiple independent retrieval routes.
3. Distinguish sequential evidence dependencies from query views that can be retrieved in parallel.
4. Consider corpus size, lexical specificity, semantic mismatch, expected retrieval noise, latency budget, and token budget.
5. Produce guidance for selecting exactly one advertised Agentic Skill. Refer only to currently available package names and never invent a candidate.

## Baseline guidance

- Prefer `agentic-sequential-skill` when one retrieval route should be sufficient and the task can proceed directly through optional rewriting, retrieval, optional reranking, and grounded generation. Use it as the lowest-cost default for ordinary questions.
- Prefer `agentic-iterative-rag` when later retrieval should depend on evidence or missing-information feedback from an earlier round, when evidence sufficiency is uncertain, or when a bounded Critic-guided retrieve-generate loop is needed.
- Prefer `agentic-parallel-rag` when independent query decompositions, multiple query views, or complementary lexical and semantic retrieval routes can run concurrently and should be fused before generation. This includes comparison tasks whose evidence branches can be identified up front.
- Prefer the simpler sequential workflow when the expected evidence benefit of iteration or parallel fan-out does not justify additional latency and model calls.
- Reject any candidate that is not an Agentic Skill.
- Do not select Component Skills directly.

## Output

Return strict JSON without selecting a Component Skill:

```json
{"agentic_selection_guidance": "selection guidance", "reason": "short reason"}
```

The framework will expose Agentic advertisements in the next stage and perform the actual selection.
