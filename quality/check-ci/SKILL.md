---
name: check-ci
description: "Inspect checks on a pull request’s current commit and report a clear CI verdict."
metadata:
  category: Quality
---

# Check Ci

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the PR and its current head commit using the configured hosting service. For GitHub, inspect `gh pr view <number> --repo <owner>/<repo> --json headRefOid` and `gh pr checks <number> --repo <owner>/<repo>`.
2. Distinguish required checks from optional checks using available branch rules and documented policy. Read relevant failure output; do not infer success from the absence of a failing status.
3. If asked to wait, use bounded polling while checks are pending and keep the user informed. Stop waiting when the checks settle, the request is interrupted, or a clear external blocker is established. A one-time status request needs only a snapshot.
4. Recheck the head commit before declaring the result. Checks from an older head do not validate a newer revision.
5. Report one of: green, failing, pending, no checks configured, or unknown. Skipped/cancelled required checks are not an automatic pass. Distinguish unavailable permissions from absent CI.

## Deliverable

Return the PR, evaluated SHA, verdict, failed/pending checks, relevant run URLs, and next action. This inspection does not rerun jobs, modify CI, approve, or merge the PR.
