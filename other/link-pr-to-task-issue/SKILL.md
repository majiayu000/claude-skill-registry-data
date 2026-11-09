---
name: link-pr-to-task-issue
description: Ensure pull requests are explicitly associated with the task issue, reserving closing keywords for the PR that should actually complete it.
engines: [AGNOSTIC]
---

## When to use
Use when preparing, updating, or reviewing a pull request for task-backed work.

## Output
- PR body updated with the correct closing or non-closing issue reference for its delivery mode
- explicit traceability from issue to implementation PR

## Notes
- Prefer `Closes #<issue-number>` in a normal task PR, Goal task PR, or final Gauntlet promotion PR that should complete the linked issue.
- A Gauntlet progress or remediation PR must use a non-closing reference such as `Refs #<issue-number>` so its human merge cannot close the parent deliverable before promotion. Put that reference in the initial PR body beside the required publication-checkpoint marker; do not run the closing-only command below for a progress PR.
- If the link is missing, add it before final review.
- This skill runs only after the applicable mode-aware readiness gate authorizes publication. Human confirmation is required for normal task and Gauntlet promotion PRs; explicit Goal flow and approved Gauntlet progress publication use their recorded scoped exceptions. Do not use issue linkage itself as permission to push or create a PR.
- For PR body reads/updates, prefer `gh` first, then an available `github` CLI executable or repository-provided GitHub CLI wrapper, then GitHub MCP/app connector tools only when both CLI options are unavailable or unsuitable.

## Command
../commands/link-pr-to-task-issue.sh "<issue_url_or_number>" [pr_number_or_url]
