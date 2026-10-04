---
name: "Branch: Rename If Needed"
description: "Check the current branch name against convention (type/short-description) and rename it if it drifted."
when_to_use: "Before opening a PR, when work started on a misnamed or default branch, or whenever the branch name no longer reflects what the branch actually contains."
model: sonnet
effort: low
metadata:
  glyph: ᛊ
  family: branch
disable-model-invocation: false # invocable by Claude so it can flag a drifted branch name before PR creation; the rename still awaits approval
allowed-tools: ["Bash(git:*)", "Bash(gh pr list:*)", "Bash(~/.claude/library/scripts/branch-facts.sh:*)"]
arguments: ["desired-name"]
argument-hint: "[desired name (optional; omit and a name is suggested from the branch's contents)]"
---

## Assess and Rename Current Branch

1. Gather the facts in one call: `"$HOME"/.claude/library/scripts/branch-facts.sh`; it emits JSON including the current branch name, its convention compliance and the commit/diff shape. Judge from that; only run `git log main..HEAD --oneline` / `git diff main..HEAD --name-only` when the facts alone can't tell you what the branch *is about*.
2. **`$desired-name` given**: treat it as the target: check it against convention (Step 3's format rules), flag any mismatch, then proceed to Step 5 with it.
3. **No argument**: derive the right name yourself from what the branch actually contains:
   - Format: `<prefix>/<short-description>`, all lowercase, hyphens, imperative mood (`add-feature`, never `adds-feature` or `adding-feature`)
   - Prefix from the canonical set: `feat`, `fix`, `enhance`, `refactor`, `test`, `docs`, `config`, `chore`, `ci`, `deps`, `hotfix`, `spike`, `agents`, chosen from the dominant nature of the commits, not the first commit
   - Description from the work's effect, not its file list
4. If the current name already satisfies convention **and** accurately describes the work, say so and stop; no rename for renaming's sake.
5. Otherwise present the suggested (or user-supplied) name against the current one, with one line of reasoning, and **await approval**. On approval:
   - Rename locally: `git branch -m <new-name>`
   - If the old branch was pushed: first run `gh pr list --head <old-name>` **and** `gh pr list --base <old-name>`. An open PR on either means **stop and rename nothing**: deleting a head branch closes its PR permanently (GitHub does not follow renames), and deleting a branch that is the *base* of an open PR orphans a stacked child. Report that; a branch inside a stack is renamed safely only via `gh stack modify` (its rename operation retargets the stack for you), which is a full-screen interactive editor Claude cannot drive: ask the user to run it, otherwise the rename waits until the PRs merge or close. With no open PR either way: `git push origin HEAD:<new-name>`, then `git push origin --delete <old-name>`, then `git branch --set-upstream-to=origin/<new-name>`
   - Never touch the remote when the branch was never pushed; the facts output shows whether an upstream exists.

<raw-arguments value="$ARGUMENTS" />
