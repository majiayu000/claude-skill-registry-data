---
name: pr-ready
description: Get a branch ready for review and keep its pull request green. Use before opening a PR and whenever CI or a review reports something on it.
---

Before opening:

1. Run the `check` skill. Push only after every command passes.
2. Read your own diff as a reviewer would: unused code, a leftover debug line, a secret, a comment that justifies instead of describes, a missing doc or registry entry (see `new-module`).
3. Commit subject in the imperative, at most 72 characters. The body says why.

PR body:

- A "Before:" paragraph and an "After:" paragraph in plain language.
- A short "How" list naming the files and decisions a reviewer needs.
- New migration IDs, new environment variables, new org secrets and anything a deployer must do.

On CI failure: reproduce locally, find the cause, fix it, and push. A flaky test is not a cause. Never skip or disable a test, and never force-push someone else's branch.

On review comments: fix small, local requests in the next push. Reply on the thread with the reason when you do not.
