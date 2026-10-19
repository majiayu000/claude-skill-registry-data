---
name: sd-grilling
description: Explore the codebase and relentlessly interview the user about a plan, feature, or idea until shared understanding is reached. Use when user says 'plan this feature step by step', 'help me plan this properly', 'generate a plan for this problem', 'walk through planning this feature', 'grill me about X', or uses any 'grill' trigger phrases.
model: claude-opus-5-5[1m]
---

# Steps

Repeat phases 1 and 2 together, as one loop, until you have a complete understanding of the problem and how it fits into the current codebase. When the loop feels sufficient, ask the user whether they wish to finish or continue refining before stopping — never end the loop on your own judgment alone.

1. **Exploration phase.**
   1. Use `sequentialthinking` to break down the request into sub-issues (scope, constraints, edge cases, dependencies).
   2. Use `/dynamic-programming-analysis` when the breakdown itself is hard (unclear where to start, many interdependent sub-problems).
   3. Use `/context-map` with the sub-issues as the task description to get verified anchors, dependents, tests, reference patterns, and risks. Re-run or extend it on later loop iterations when new sub-issues open unmapped areas.

   Across all of the above: treat the codebase as the absolute source of truth — navigate file-by-file, following the flows that will be modified/adjusted, until you reach the limits of what's there and have a full understanding of current behavior. Search transversally too, not just along linear flows: hunt keywords/terms possibly related but not directly linked, or absent from files already inspected (config, feature flags, error codes, event names, shared constants). If a knowledge gap remains that the codebase and `context7` (library docs) can't cover — market patterns, RFCs, security advisories, precedent for a novel architectural decision — use `WebSearch` to fill it. Skip this when the codebase/context7 already answer the question.

2. **Grilling phase.** Invoke the `/grilling` skill directly (inline, not as a sub-agent) over the open branches surfaced by phase 1 (scope, constraints, edge cases, dependencies). Follow its design-tree/frontier/round format exactly: one numbered round of questions via `AskUserQuestion`, each with a recommended default, waiting for answers before recomputing the frontier. Never ask the user for a fact you can look up yourself — only put genuine decisions to them. Any answer that opens a sub-issue not yet explored sends the loop back to phase 1 for that branch before the next round.
