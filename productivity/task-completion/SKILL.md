---
name: task-completion
description: >
  Shared task lifecycle protocol for swarm subagents. Covers executing
  assigned tasks, posting results, and completing tasks with summaries.
---

# Task Completion Skill

## Task Lifecycle

Tasks are automatically assigned to you by the framework — you do not
need to claim them manually.

1. **Execute the task** — follow your domain skill's workflow.
2. **Complete the task** — use `complete_task` with a comprehensive summary
   of what you found. Include exact numbers, methodology details, and
   caveats. The summary is automatically shared with the orchestrator and
   peers — no separate sharing step is needed.

## Rules

- Focus on YOUR assigned task — don't try to do everything.
- You CANNOT create tasks for other agents. Only execute tasks assigned
  by the orchestrator.
- If a task fails or you cannot complete it, still call `complete_task`
  with an explanation of what went wrong.

## Completion Summary Hints

When writing the `complete_task` summary, include (when relevant):

- **What you found**: the concrete answer, value, or artifact.
- **How you found it**: methodology, queries, sources, or tools used.
- **Evidence**: data, URLs, query outputs — whatever the recipient needs
  to verify.
- **Caveats**: assumptions, data gaps, or edge cases.
- **Confidence**: high / medium / low, and why.
- **Response to feedback**: if you changed your approach based on DMs
  or BBS posts from other agents, briefly explain what changed and why.
  This helps the orchestrator understand how your analysis evolved.
