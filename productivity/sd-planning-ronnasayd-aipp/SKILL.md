---
name: sd-planning
description: Generate a feature plan through iterative problem breakdown, codebase research, and clarifying questions before handing off to tlc-spec-driven and requirements-table generation. Use when user says 'plan this feature step by step', 'help me plan this properly', 'generate a plan for this problem', or 'walk through planning this feature'.
model: claude-opus-5-5[1m]
---

# Steps

See [diagram](references/diagram.md) for a visual flow overview.

Add the following steps as tasks using the `TaskCreate`, `TaskUpdate`, `TaskGet`, and `TaskList` tools. Update the status as you progress through each step to keep the user informed.

1. Repeat these steps until you have a complete understanding of the problem and how it fits into the current context. When you feel the loop should end because you have sufficient context, ask the user if they wish to finish or continue refining issues before creating the plan.
   1. Use `sequentialthinking` in `mcp-manager` to break down the feature request into sub-issues (scope, constraints, edge cases, dependencies). Use `/dynamic-programming-analysis` when the breakdown itself is hard (unclear where to start, many interdependent sub-problems).
   2. Next, run `/context-map` with the sub-issues as the task description to get verified anchors, dependents, tests, reference patterns, and risks (it runs `rag-rat`, `codebase-memory-mcp`, `serena` itself). Re-run or extend it on later loop iterations when new sub-issues open unmapped areas. Then use `grep`, `Read`, or any other available tool to go deeper where the map's "Not Checked" or uncertain anchors leave gaps.
      1. Treat codebase as absolute source of truth. Navigate file-by-file, following flows that will be modified/adjusted, until you reach limits and have total understanding of current behavior.
      2. Don't trust linear flows alone — search transversally: hunt keywords/terms possibly related but not directly linked, or absent from files already inspected (config, feature flags, error codes, event names, shared constants).
      3. Use every available tool to reach this understanding: semantic search, sub-agents for parallel/deep search, CLI commands, MCP tools, skills, or anything else that helps.
      4. If a knowledge gap remains that the codebase and `context7` (library docs) can't cover — market patterns, RFCs, security advisories, precedent for a novel architectural decision — use `WebSearch` to fill it. Skip this when the codebase/context7 already answer the question.
   3. Run `/prd-get-implicit-requirements` against the gathered problem description to surface gaps across its 14 universal categories (error handling, data persistence, security, accessibility, etc.) before grilling the user — this narrows what still needs asking.
   4. Conduct a `/grilling` session until you have obtained all necessary information and clarified any doubts with the user, including the gaps surfaced above. Check for unlisted implicit requirements and potential undefined issues.

2. Execute the `/tlc-spec-driven` skill to generate a plan/spec based on the described problem.
3. Execute the `/spec-to-requirements-table` skill to generate a `requirements.md` file.
4. Once planning is complete, ask the user if they wish to register the feature in _taskmaster_. If the answer is "yes," use the `/sd-insert-taskmaster` skill.
5. Check the definitions in [docs-adr](./references/docs-adr.md) and consider offering to create an ADR when the criteria are met.
6. At the end of the session, evaluate whether there is anything worth saving as permanent memory. Save as permanent memory only what the next session will need and cannot rediscover by reading the code, Git, or CLAUDE.md—such as the _reason_ behind a decision, a non-obvious invariant, or a user preference; if it is already in the repo or only matters for this specific conversation, do not save it. Use the `ai-memory-durable-pages` skill to persist it.
