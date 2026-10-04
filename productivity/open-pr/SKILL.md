---
name: open-pr
description: "Open a pull request with a focused description, the correct base branch, and relevant validation evidence."
metadata:
  category: Delivery
---

# Open Pr

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the target repository, working branch, discovered default or explicitly requested base branch, and related issue. Do not open a PR from the base branch to itself.
2. Inspect the full branch diff against the base and check whether a PR already exists. Update an existing matching PR when appropriate instead of creating duplicates.
3. Review local task changes, commit and push as needed for the requested PR, and preserve unrelated work. Use the repository's commit and branch conventions; inspect the remote destination before pushing.
4. Write a title and body for a reviewer unfamiliar with the conversation. Explain the problem, final behavior, scope, tests, and meaningful limitations. Use the repository template if present. Link issues accurately; use an automatic closing reference only when the PR actually completes that issue.
5. Create the PR in the requested draft/ready state, reflecting unfinished work honestly. If authorized and configured, update the issue's board status using the project's real field values.
6. Verify the PR URL, head and base, body, and tracker linkage. A newly opened PR with pending checks is not a verified green build.

## Deliverable

Return the PR URL, summary, validation evidence, and remaining review/check steps. Opening a PR does not authorize merging it.
