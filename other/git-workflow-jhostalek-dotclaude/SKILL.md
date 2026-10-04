---
name: git-workflow
description: Apply personal Git conventions when committing, creating or updating PRs, merging, rebasing, or explicitly shipping work end to end.
disable-model-invocation: false
---

Use the mode requested by the user or calling skill. A request for a commit message only produces a message; an ordinary commit or PR request does not authorize merging. Honor narrower instructions already given.

Read the relevant reference before acting:

| Mode | Reference |
| --- | --- |
| Commit or commit message | [commit.md](references/commit.md) |
| Create or update a PR/MR | [pr.md](references/pr.md) |
| Merge a branch, rebase, or resolve conflicts | [integration.md](references/integration.md) |
| Explicit end-to-end shipping, including `/yeet` | [ship.md](references/ship.md) |

Use the intended repository, current branch, and remote. Preserve unrelated work and staged changes. One PR per repository; update an existing PR for the branch.

Ordinary commit mode commits locally. PR mode includes pushing the relevant commits. Explicit branch-merge and rebase modes include publishing the result, using a lease for a rewritten remote branch. End-to-end mode includes implementation, verification, commit, push, PR creation/update, merge, and remote source-branch deletion.

Report the completed operation, relevant commit or PR, verification, and any unresolved blocker. Publishing and merging are complete only when the remote confirms them.
