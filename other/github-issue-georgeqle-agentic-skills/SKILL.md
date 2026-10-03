---
name: github-issue
description: Safely reuse, create, update, or explicitly close the single GitHub Issue that tracks repository work
type: operations
version: v0.1
argument-hint: "<ensure|update|close|status> [issue-number] [--title <title>]"
---

# GitHub Issue

Use this low-freedom subskill to own the issue/ticket boundary for tracked repository mutations. Follow `docs/github-delivery-contract.md` when it exists in a source checkout; packaged use follows the same contract embedded here.

## Commands

- `ensure`: find one unambiguous open issue for the current task or create one.
- `update`: add material status or acceptance-criteria context to the resolved issue.
- `status`: report the resolved issue and its relationship to the current branch or pull request without mutation.
- `close`: close only the explicitly resolved issue after separate user confirmation. Normal delivery uses a pull-request closing keyword instead.

## Prompt History Termination

Prompt history is metadata, not work that initiates this lifecycle. Never create or reuse an issue solely to ship a prompt-history record. These lifecycle commands create no prompt file when it would be their only tracked mutation; when another user-invoked skill produces substantive tracked changes, its prompt record travels with that same work.

## Resolution

1. Verify this is a Git repository with one unambiguous GitHub repository and authenticated `gh` access. Read repository issue templates and contribution instructions when present.
2. Resolve explicit issue numbers or URLs first. Otherwise inspect the current branch, pull-request metadata, task artifacts, and open issues for exact task identity, distinctive title terms, and linked paths.
3. Reuse one issue only when the evidence is unambiguous and its scope is compatible. Stop when multiple plausible issues exist, a candidate is closed, or its scope conflicts.
4. For `ensure`, create an issue only after the search finds no compatible issue. Use a specific title and body containing the goal, scoped acceptance criteria, and known constraints. Do not create placeholder, umbrella, or duplicate issues.
5. Return the repository, issue number, URL, title, state, and whether it was reused or created. Pass that stable issue identity to `github-branch` and `github-pr`.

## Safety

- A GitHub Issue is the canonical ticket abstraction; do not create a second ticket record for the same work.
- Do not close an issue when a branch or pull request opens. Prefer `Closes #N` in the pull-request body so closure occurs only after merge.
- `close` requires the exact issue, current state, closure reason, linked pull-request state, and explicit user confirmation immediately before mutation.
- Never close an issue with an open or unmerged linked pull request, unresolved acceptance criteria, or ambiguous ownership.
- Authentication or remote failure is a blocker, not permission to invent identifiers or weaken delivery safety.

## Output

Report the exact issue identity, evidence used for reuse or creation, any blocker, and the next operation. Do not expose tokens or credential output.
