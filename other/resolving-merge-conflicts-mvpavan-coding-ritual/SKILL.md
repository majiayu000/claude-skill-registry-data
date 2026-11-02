---
name: resolving-merge-conflicts
description: Use when a git merge, rebase, or cherry-pick is already in a conflicted state and the conflicts need resolving. Trigger on merge-conflict / rebase-conflict phrases.
---

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files — capture the conflict set now: `git diff --name-only --diff-filter=U`.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Use commit messages and relevant requirements first; expand to PRs/issues only
   when a disputed hunk needs that history.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Resolve rather than reflexively aborting; if the two intents cannot be reconciled, or the merge/rebase itself turns out to be the wrong operation, stop and ask the user before `--abort`.

4. Discover the project's **automated checks** and run them — typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage only the resolved conflict files, explicitly by path — the list captured in step 1, never `git add .` / `-A`. Commit (or `rebase --continue`) only if the user or the active workstream granted commit authority; otherwise stop with the resolution staged and report what would be committed.
