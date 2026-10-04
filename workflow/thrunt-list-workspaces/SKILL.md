---
name: thrunt-list-workspaces
description: List active THRUNT workspaces and their status
allowed-tools: Bash, Read
---

<objective>
Scan `~/thrunt-workspaces/` for workspace directories containing `WORKSPACE.md` manifests. Display a summary table with name, path, repo count, strategy, and THRUNT project status.
</objective>

<execution_context>
@.github/thrunt-god/workflows/list-workspaces.md
@.github/thrunt-god/references/ui-brand.md
</execution_context>

<process>
Execute the list-workspaces workflow from @.github/thrunt-god/workflows/list-workspaces.md end-to-end.
</process>
