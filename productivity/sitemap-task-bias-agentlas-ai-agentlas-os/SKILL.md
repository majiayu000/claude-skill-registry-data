---
name: sitemap-task-bias
description: "Use when creating or auditing an agent-team sitemap, Task Bias ledger, concept coverage, product surface map, validation chain, or missing-concept check."
---

# Sitemap Task Bias

## Procedure

1. List the user-facing surfaces, workflows, agent roles, skills, memory scopes,
   runtime adapters, policy gates, and verification lanes.
2. Compare the request against required concept coverage:
   - sitemap;
   - PM Soul;
   - memory architecture;
   - all-LLM runtime architecture;
   - public/private boundary;
   - install and verification path.
3. Add task biases that protect the build from dropping important concerns.
4. Record skipped or blocked concepts in `.agentlas/validation-ledger.jsonl`.

## Output

Return `covered`, `missing`, `task_biases`, and `evidence_files`.
