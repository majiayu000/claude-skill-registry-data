---
name: resolving-merge-conflicts
description: Resolve an in-progress git merge or rebase conflict while preserving both sides' intent. Use when a merge/rebase is blocked on conflicts, or the user asks to finish a conflicted merge or rebase.
---

# Resolving Merge Conflicts

1. **See the current state** of the merge/rebase. Check git history and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where the two intents truly cannot both be kept, ask the user to choose instead of picking silently (`AskUserQuestion` where available: ours and theirs as options, plus a combined one if it makes sense, each hunk in its option's `preview`, the one matching the merge's stated goal first and marked recommended; otherwise quote both hunks in chat and ask). Do **not** invent new behaviour. Always resolve; never `--abort` unless the user explicitly asks to abort.

4. **Check what the merge touched; leave the suite to CI.** The conflict is resolved when both intents are in the file, the conflict markers are gone, and the resolved files still parse. Run one quick check scoped to the resolved files: the project's static analysis or linter on those paths, or a syntax check (`php -l`, `tsc --noEmit`) when none is configured. Then search the tree for every symbol either side renamed or removed (`rg <old name>`), because a merge with no textual conflict can still call what the other side deleted. Fix what the merge broke. The full test suite and formatter run in CI.

5. **Finish the merge/rebase.** Stage everything and commit. If rebasing, continue the rebase process until all commits are rebased.
