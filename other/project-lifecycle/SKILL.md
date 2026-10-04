---
name: project-lifecycle
description: "Create, inspect, close, or reopen an iteration or project board using the target project’s own workflow."
metadata:
  category: Planning
---

# Project Lifecycle

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the project, tracker, owner, and requested lifecycle action. Discover current project fields, status options, linked repositories, and the local iteration-document convention, if any. Inspect all relevant items, including paginated results.
2. For creation, use the project's existing template or agreed scope, dates, goals, and workflow. Create an iteration document only if requested or part of the established process. Do not assume a template path or helper script exists.
3. For inspection, compare the live configuration and item states with the documented workflow. Report discrepancies before changing anything. Reuse a project-maintained tool when available and understood; otherwise use supported tracker APIs or UI operations.
4. For closing, summarize delivered outcomes and unfinished items. Close only when authorized and unresolved work has an explicit disposition. Never silently mark unfinished items complete to enable closure.
5. For reopening, preserve existing items and configuration, restore the intended lifecycle state, and update any associated iteration record.
6. Treat deletion of a status field or option as a potentially destructive migration. Identify affected items and reporting dependencies, prepare an explicit mapping, and obtain authorization for that change if the user has not provided it. Do not replace a field merely to reorder labels.
7. Re-read the project after changes. Report any partially applied operation and the remaining recovery action; do not retry destructive operations blindly.

## Deliverable

Provide the project URL, actual lifecycle state, outcomes, unresolved items, and any updated document. This workflow does not require a particular board-column set, reporting script, or repository arrangement.
