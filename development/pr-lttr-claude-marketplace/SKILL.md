---
name: pr
description: Azure DevOps pull requests, for repos whose git remote is on dev.azure.com or *.visualstudio.com. Covers comment threads, which `az repos pr` cannot read or post. Use to create a PR for the current branch, check out, list or complete PRs, post code comments on a PR, reply to threads, and assess whether review feedback was addressed. Trigger on "create PR", "checkout PR 123", "list PRs", "complete PR", "comment on the PR", "post these review findings", "check PR feedback", "/dev-azdo:pr".
argument-hint: <create|checkout|list|complete|comments> …
---

# PR (Azure DevOps)

Multi-op skill. Pick the op from the intent of the request, read its reference, run the steps,
report the result.

Shared rules (org/project resolution, default branch, approval gate, writing, request bodies)
live in `${CLAUDE_PLUGIN_ROOT}/references/conventions.md`. Read it before the first op.

## Pre-flight

Run `git remote get-url origin`. If it is not an Azure DevOps remote (see the conventions),
stop and say so. This skill does not handle GitHub or other hosts.

## Dispatch

| Op           | Intent                                                   | Reference                                    |
| ------------ | -------------------------------------------------------- | -------------------------------------------- |
| **create**   | open a PR for the current branch                         | `${CLAUDE_SKILL_DIR}/references/create.md`   |
| **checkout** | switch to a PR's source branch, by id or URL             | `${CLAUDE_SKILL_DIR}/references/checkout.md` |
| **list**     | active PRs, mine (default) or all                        | `${CLAUDE_SKILL_DIR}/references/list.md`     |
| **complete** | merge the current branch's PR                            | `${CLAUDE_SKILL_DIR}/references/complete.md` |
| **comments** | post code comments, reply to threads, assess PR feedback | `${CLAUDE_SKILL_DIR}/references/comments.md` |

Ambiguous intent: ask.

`create`, `complete` and posting in `comments` write under the user's name. Each goes through
the approval gate. Do not skip it.

## Notes

- `create` stops on the repo's default branch and tells the user to run `feature-branch` first.
- `create` stops if no commits are ahead of the default branch and tells the user to commit
  first. Commit logic is intentionally not bundled.
- Work-item state changes go through the `ticket` skill (`state` op). `create` offers Code
  Review, `complete` offers the next state after merge. Neither transitions on its own.
- For reviewing the diff, `aiwork:code-review-diff` does it if the `aiwork` plugin is installed.
  Not required. This skill never invokes it. Its findings can be posted with the `comments` op.
