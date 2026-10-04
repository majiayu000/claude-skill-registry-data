---
name: commit-and-track
description: Create a git commit AND update the vault changelog/timeline so history stays in sync. Use after any meaningful change instead of plain git commit. Use when the user says "commit this", "save the work", or "ship it".
---

# commit-and-track

Commit + propagate to the History section of the vault in one move. This is the project-specific replacement for the bare `/commit` command.

## Steps

1. **Check user authorization** — has the user explicitly asked to commit? If not, **do not** commit. The vault still gets updated, but commit is held until they say so.
2. **Run `git status` and `git diff --staged`** in parallel to see what's in scope.
3. **Group changes by intent** (feat / fix / refactor / chore / style / docs / test / milestone). If they're mixed, ask the user whether to split commits — don't bundle unrelated work.
4. **Draft a commit message** in the project's style:
   - Single line ≤ 72 chars
   - Conventional prefix (`feat:`, `fix:`, etc.)
   - Em-dash `—` for sub-clauses (matches project history)
5. **Stage explicit files** (no `git add -A`). Skip `.env`, `node_modules`, `dist`, `xlsx` lock files, unrelated changes.
6. **Create the commit** via HEREDOC, ending with the project's `Co-Authored-By` line.
7. **After commit succeeds**:
   - Update `Aqarkom_Knowledge/History/Changelog/{current-month}.md` — append a new bullet under the right category
   - Update `Aqarkom_Knowledge/History/Timeline.md` — bump the highlights list if this is a `feat:` or `milestone:`
   - If the commit changed something architectural, run `/track-change` to update Architecture/Features notes too
8. **Report** the short hash and what was committed.

## Verification

- [ ] User explicitly authorized the commit
- [ ] Commit landed (verified by `git log -1`)
- [ ] Changelog month note updated
- [ ] Timeline updated if commit was a feat/milestone
- [ ] No secrets, lock files, or unrelated changes in the commit

## Anti-patterns

- Don't `git add -A` — it sweeps in `.env`, xlsx lock files, and dev junk
- Don't amend a published commit
- Don't skip the changelog update — that's the whole point of this skill
- Don't use `--no-verify` to bypass hooks
