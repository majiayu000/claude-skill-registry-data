---
name: gh
description: Commit, push, and open a PR using the cheap low-token git-ops agent. Use for git/github wrap-up — git commit, git push, gh pr create, "ship it", "open a PR", "create the PR", "push and PR", end-of-task git handoff.
disable-model-invocation: true
context: fork
agent: git-ops
---

# gh: git handoff

Commit the relevant changes, push, and open a PR (follow user instructions exactly):

1. Stage what belongs together, commit with a Conventional Commits message.
2. Push the current branch (create one off the default branch first if needed).
3. Open a PR with `gh pr create` — concise title, short what/why body.
4. Print the PR URL.

Keep output minimal: the PR URL on success, the exact error on failure.
