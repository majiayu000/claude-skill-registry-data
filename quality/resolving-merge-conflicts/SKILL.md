---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

Source: [mattpocock/skills — engineering/resolving-merge-conflicts](https://github.com/mattpocock/skills/blob/main/skills/engineering/resolving-merge-conflicts/SKILL.md), imported verbatim 2026-08-26.

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. **Check for subtle semantic conflicts.** Even when git resolves hunks cleanly without conflict markers, semantic collisions can occur (e.g. both sides added an import with the same name, both modified the same configuration key differently, or both registered routes with the same URL path).
   - Review incoming additions with `git diff MERGE_HEAD...HEAD` (or the rebase upstream diff).
   - Grep for duplicate route definitions, conflicting config keys, or duplicate symbols across modified files.
   - Run the project's **automated checks**: compiler/typecheck, test suite, and linter. Fix anything the combined changes broke.

5. **Finish the merge/rebase.** Stage everything and commit. If rebasing, continue the rebase process until all commits are rebased.
