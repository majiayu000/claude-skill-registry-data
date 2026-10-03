---
name: github-pr
description: Safely upsert, inspect, review, or explicitly merge the pull request for an issue-backed work branch
type: operations
version: v0.1
argument-hint: "<upsert|review|merge|status> [pr-number] [--draft|--ready]"
---

# GitHub Pull Request

Use this low-freedom subskill to own pull-request reuse, creation, readiness, review status, and explicit merge. Follow the canonical `docs/github-delivery-contract.md` when available.

## Commands

- `upsert`: reuse the pull request for the resolved head branch or create one.
- `status`: report identity, head/base, draft state, mergeability, checks, approvals, unresolved threads, and linked issue.
- `review`: inspect review feedback and gates without merging.
- `merge`: merge only after all strict gates and immediate explicit user confirmation.

## Prompt History Termination

Prompt history is metadata, not work that initiates this lifecycle. Never create or reuse a pull request solely to ship a prompt-history record. Status, review, and merge commands create no prompt file when it would be their only tracked mutation; when another user-invoked skill produces substantive tracked changes, its prompt record travels with that same work.

## Upsert

1. Require a resolved issue and a published, non-primary branch from `$github-issue` and `$github-branch`.
2. Search open and closed pull requests by exact head repository and branch. Reuse the one compatible open pull request. Stop on multiple candidates, a conflicting base, or an already-merged/closed candidate rather than creating a duplicate.
3. Create only when no pull request exists for the head. Base it on the detected primary branch. Include a concise summary, validation evidence, risks or follow-ups, and `Closes #N` for the resolved issue.
4. Mark ready only when intended changes are committed and pushed, proportionate validation passed, and no known blocking finding remains. Otherwise preserve or create a draft and explain the blockers.
5. Ordinary shipping ends after the ready pull request is published or updated. Do not merge it.

## Merge Gate

Before requesting confirmation, fetch fresh GitHub state and prove all of the following:

- the exact pull request is open, non-draft, and targets the detected primary branch;
- its head matches the reviewed commit and is current enough for repository policy;
- GitHub reports no conflicts and an allowed merge method is selected;
- every required check has passed, with no pending, skipped-required, cancelled, or failed check;
- required approvals are present and no change request remains;
- no unresolved review thread, accepted Critical/High finding, or other documented blocker remains;
- the linked issue is correct and will close through merge, not before it.

Show repository, pull-request number and URL, exact head SHA, base, merge method, check/approval/thread summary, and issue disposition. Obtain explicit user confirmation immediately before the merge mutation. A prior request to ship, publish, finish, or create a pull request is not merge confirmation.

After merge, verify the merged SHA and linked issue state. Branch cleanup is separate and routes to `$github-branch cleanup`; do not delete branches implicitly.

## Safety

- Never enable auto-merge, bypass branch protection, dismiss reviews, resolve threads without addressing them, admin-merge, or merge with failing/unknown gates.
- Never treat local test success as a substitute for required remote checks.
- Authentication or API uncertainty blocks mutation and never authorizes a direct-primary fallback.

## Output

Report pull-request identity, reuse/create decision, readiness, exact gate status, linked issue behavior, and the next substantive review or remediation action. Never route next work to a prompt-history-only pull request.
