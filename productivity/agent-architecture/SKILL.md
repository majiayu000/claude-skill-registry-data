---
name: agent-architecture
description: "Design agent loops: planning, tool use, subagents, memory, RAG, evals, budgets. Use when building LLM features or multi-step agents. Security review via security/agent-security."
---

# agent-architecture

Plan → act → observe → verify. Every loop needs a budget, a memory policy, and an eval.

## Activate when

- Building tool-calling features, RAG pipelines, subagent workflows, or scheduled agents.
- Debugging agent loops, runaway cost, or stale context.

## Do NOT activate for

- MCP server mechanics (see mcp-engineering) or skill authoring (see skill-design).

## Procedure

1. Loop: define states (plan, act, verify, escalate), max steps, and stop conditions; stream progress for long runs.
2. Tools: narrow schemas, idempotent mutations, confirmation for irreversible actions; treat all tool output as untrusted input to the next step.
3. Context: retrieve-then-read (embeddings + rerank), cite sources, budget tokens per phase; compact with extractive summaries, never silent drops.
4. Memory: short-lived working memory vs persisted facts with TTL and provenance; no secrets in memory stores.
5. Models: route by difficulty with fallbacks; structured outputs with schema validation and repair retries.
6. Eval: task-based evals (success rate, cost, latency) before and after each change; log traces for replay.
7. Verify: replay a failing trace, confirm the fix, and record residual risk + owner.

## References
- `../mcp-engineering/`, `../skill-design/`, `../../security/agent-security/`.
