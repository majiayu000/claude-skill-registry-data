---
name: resolving-merge-conflicts
description: Resolve existing conflict hunks during an in-progress Git merge or rebase. Use when Git reports unresolved merge/rebase conflicts; do not use for ordinary branch integration or speculative cleanup.
---

1. **Inspect the exact Git state.** Determine whether a merge or rebase is in progress, read the history and status, and list the paths and hunks that are currently conflicted.

2. **Find the primary intent sources.** Use the relevant commits, messages, pull requests, issues, accepted plans, and surrounding code to understand why each side changed.

3. **Resolve only existing conflict hunks.** Preserve both intents where compatible. Where they conflict, follow the stated integration goal and report the trade-off. Do not invent new behavior or broaden the change.

4. **Verify and report.** Stage only verified conflict-resolution paths when staging is needed to mark them resolved, and report the exact staged set. Run the relevant repository checks and fix only failures caused by the resolution.

5. **Respect the exact lifecycle authorization.** Do not continue or abort the merge/rebase, commit, push, force-push, reset, discard with checkout, or clean up unless that exact action is already authorized. Do not repeat an approval request for an action the user has explicitly approved.
