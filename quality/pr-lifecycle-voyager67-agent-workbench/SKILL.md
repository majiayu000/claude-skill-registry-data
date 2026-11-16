---
name: pr-lifecycle
description: Take a verified change from local branch through pull-request readiness, with optional merge only when the user explicitly authorizes it. Use for end-to-end GitHub PR work.
---

# Pull Request Lifecycle

Choose the requested stopping point first: local verification, PR opened, PR ready for human merge, or merged. Never assume merge authorization.

1. Inspect branch, diff, base, working-tree state, and original request. Preserve unrelated changes.
2. Run targeted tests and review the full diff. Resolve concrete issues before publication.
3. Confirm the intended repository, branch, visibility, title, and target. Create commits or push only when authorized.
4. Open or update a PR with a problem-first summary, behavior changes, tests actually run, and known limitations.
5. Monitor CI and review feedback only when requested or within the approved task. Use the PR watcher for check-state changes, but inspect review threads separately.
6. Fix validated findings, rerun relevant checks, and keep the PR description accurate.
7. Stop at the requested gate. Merge only with explicit authorization and after verifying required approvals, checks, mergeability, and target branch.

Never auto-merge because a check turned green. Do not force-push, dismiss reviews, or change repository settings without approval. Report the exact state observed from GitHub.
