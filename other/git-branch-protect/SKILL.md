---
name: git-branch-protect
version: "1.0.0"
user-invocable: true
description: "Use when checking or changing who can push or merge release/*, an exact release branch, or main/master. Read the live rule with glab or gh, then whitelist the active release, freeze a finished release, set trunk protection, or roll a release branch back to a chosen commit. Also use when git-release-start or git-release-finish needs that check. Triggers — 「分支权限」「保护分支」「冻结 release」「release 白名单」「回退保护分支」 / branch protection, freeze release branch, release whitelist, protected branch permission. Do NOT use for creating the release branch, tagging and merging the release, or merging an ordinary change. A protection write waits for the user to confirm that command."
---

# Git Branch Protect

## Overview

Keep one active `release/X.Y.Z` mergeable, keep every other release branch closed, and keep trunk push closed. GitLab and GitHub combine overlapping rules differently, so the host procedure lives in one reference file. Read that file before any API call.

The condition is the live protection rule on the host. Read it with `glab` or `gh` and compare it with the operation's effect. There is no committed config file.

**Pairing**: after the remote branch exists, `git-release-start` asks this skill to read the default and the new branch. After the tag and the trunk merge have both succeeded, `git-release-finish` asks it to read whether that branch is frozen, and it reads trunk during fingerprinting. A release skill naming an operation is a request to compare the live rule. The write itself waits for the user. Neither release skill calls `rollback`.

## Use when / Do not use for

**Use when**:

- The user asks to freeze a release branch, open one release branch for merge, set `main` or `master` protection, or roll a release branch back to an older commit
- `git-release-start` or `git-release-finish` needs the live rule compared with the expected push and merge result

**Do not use for**:

- Creating the release branch (`git-release-start`)
- Tagging and merging the release into trunk (`git-release-finish`)
- Deciding whether an ordinary merge request may land (`merge-discipline`)

## Judge from the remote rule

From the repo's `origin` URL, choose one reference and do not mix procedures:

| Origin | Reference | Read command |
|--------|-----------|--------------|
| GitLab host | [references/gitlab.md](references/gitlab.md) | `glab api` |
| GitHub host | [references/github.md](references/github.md) | `gh api` |
| Anything else | Stop. Say this skill covers GitLab and GitHub only | — |

Run the reference's read first. When the live push and merge results already match the operation, print the report and stop. When they differ, print the live rule and the target rule.

## Confirm a write

Creating, updating, or deleting a protection rule is a high-risk change. Show the branch, the operation, the live rule, the target rule, and the exact command, then wait.

Acceptance is an explicit yes to that branch and that operation. Workflow auto-advance is not acceptance. A release skill naming the operation is not acceptance. A yes for a different branch or a different operation is not acceptance.

After acceptance, run that one command, read the rule again, and print the report. When the user declines, leave the rules as they are and set `confirmation` to `declined`.

`check-trunk` and every other read run immediately.

## Operations

Run the matching section in the host reference. After a write the user accepted, verify with that file's permission check. `merge_status`, `mergeable`, and `mergeable_state` are not the verdict.

| Operation | Effect |
|-----------|--------|
| `ensure-default` | Unmatched `release/*` branches deny push and deny merge. Leave an existing default that already does this unchanged. List every exact rule that still allows merge |
| `allow-merge <branch>` | That exact branch denies push and allows maintainer merge. Other allow entries stay |
| `freeze <branch>` | When a wider rule already denies merge, remove only that branch's allow entry. When no matching rule denies merge, set the exact rule to deny push and deny merge. If a wider rule still allows merge, report the branch as not frozen and name the rule |
| `check-trunk [name]` | Compare trunk with "push denied, maintainer merge allowed". Report a mismatch. Do not write |
| `rollback <branch> <sha>` | Only when the user invoked this operation and confirmed the sha, the force-push, and the temporary protection change. Backup, move the branch, restore the frozen policy |

For a new release, compare `ensure-default` first, then `allow-merge`. Each write waits for its own acceptance. `freeze` is offered only after the tag exists and the trunk merge has succeeded, and it runs only after acceptance.

Trunk writes happen only when the user asks this skill directly to set trunk policy and then accepts `set-trunk`. Use the same push-denied, maintainer-merge policy. A release skill reports trunk drift and does not run `set-trunk`.

## Report

Print this after every operation:

```text
branch: <name>
operation: <ensure-default|allow-merge|freeze|check-trunk|rollback|set-trunk>
push: denied | allowed
merge: denied | maintainers
confirmation: already-met | accepted | declined | read-only
evidence: <permission field or rule computation>
observed-mr: <iid or none>
still-open: <exact branches that remain mergeable, or none>
blocked-layer: <group or organization rule the caller cannot edit, or none>
```

When `blocked-layer` is set, stop. Do not claim the branch is frozen or whitelisted.

## Examples

Input: "冻结 release/1.2.3"

Output: read the live rule. When the branch is already frozen, the report says `confirmation: already-met`. When it is not, show the command that removes only that allow entry and wait. After the user accepts, run it and print the report. On GitLab, when `release/*` already denies merge, the accepted write deletes the exact allow rule. When no matching rule denies merge, the accepted write sets the exact rule to deny push and deny merge. On GitHub it removes the exception for that branch on every layer that targets it, or locks the exact rule when no wildcard is in use.
