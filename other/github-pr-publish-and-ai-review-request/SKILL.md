---
name: github-pr-publish-and-ai-review-request
description: Use only when the user explicitly invokes `$github-pr-publish-and-ai-review-request` or names `github-pr-publish-and-ai-review-request` for publishing local GitHub changes as a pull request and requesting AI review.
---

# GitHub PR Publish And AI Review Request

## Scope

Use this orchestration skill to publish one or more local branches or worktrees
as pull requests, then request both Copilot and Codex review through the
existing PR AI review request wrapper.

This skill is not for:
- implementing feature changes before publication
- applying review feedback
- merging pull requests
- deleting branches or worktrees
- force pushing
- cleaning up after merge

## Workflow

1. Resolve targets.
   - Resolve and process targets under `github-pr-publish` step 1, across
     publication and review requests.
2. Use `github-pr-publish` for the target.
   - Delegate repository checks, verification, staging, commit, push, and PR
     creation or reuse to that skill; do not maintain a second publication workflow.
   - Apply its approval model to the requested publication; delegated calls
     follow [Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization).
   - Capture the branch, commit, push target, PR number/URL, and verification result.
   - If publication fails or is blocked, stop before requesting review or moving
     to another target.
3. Use `github-pr-review-request` with provider `both` for that exact PR.
   - An explicit request to run this combined workflow includes requesting both
     reviews, subject to governing approval rules.
   - Let that skill handle both requests and their separate verification.
   - Capture the Copilot and Codex request status for the final report.
   - Report partial success; if either request fails or remains unacknowledged,
     stop before moving to another target. Do not repeat publication or a
     successful review request to recover the other request.

## Guardrails

- Do not force push, merge, delete remote branches, or clean up worktrees.
