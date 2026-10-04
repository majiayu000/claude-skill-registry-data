---
name: parallel-pr-review
description: "Review multiple pull requests in isolated checkouts and combine findings into a ranked report."
metadata:
  category: Review
---

# Parallel Pr Review

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the requested PR set and each owning repository. With no explicit set, use the selected repository's open non-draft PRs; do not expand into unrelated repositories. Confirm access before starting workers.
2. Record each PR's head SHA, base, linked issue, diff, and check status. Use a separate detached worktree at the reviewed SHA for each PR; never switch a shared working checkout underneath another task.
3. If the runtime supports delegated agents and the session permits them, assign one PR per worker up to available concurrency. Otherwise review sequentially in the same isolated structure and state that choice. Do not require a particular agent API or model.
4. Give each worker the exact checkout, SHA, issue criteria, local review conventions, and read-only scope. Review changed code through its callers, acceptance coverage, error paths, and relevant tests. Use an installed code-review skill when appropriate; otherwise perform this evidence-based review directly.
5. Report concrete defects with severity, file/line, trigger, impact, and evidence. Distinguish blocking findings, optional improvements, and unreviewed areas. Check status is evidence alongside review, not a substitute for review.
6. Combine results into a per-PR table and a severity-ranked findings list. Identify conflicting changes, shared files, and merge-order dependencies. Missing access or failed workers must appear as unreviewed, never as a clean result.
7. Recheck heads before presenting results; mark changed heads stale. Remove only clean temporary worktrees and refs created for this review.

## Boundaries and output

Workers do not edit code, commit, push, approve, merge, or post comments. The coordinator posts findings or updates a configured board only when those actions were authorized; verify the head and resulting state before recording a pass. Return the evaluated SHA, review verdict, CI state, issue fit, and evidence for every PR. A clean recommendation is not a formal approval or merge authorization.
