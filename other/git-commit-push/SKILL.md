---
name: git-commit-push
description: Commit current changes with conventional commits format and push to remote repository. Use when committing and pushing changes to the upstream remote.
allowed-tools:
  - Bash(git add:*)
  - Bash(git commit:*)
  - Bash(git push:*)
  - Bash(.agents/skills/git-commit-push/scripts/push.sh:*)
models:
  claude: sonnet      # medium-complexity; branch rename logic and upstream tracking require broader reasoning
  copilot: auto
  codex: gpt-5.4
---

# Git Commit and Push

Commit current changes using conventional commits format and push to remote repository.

## Workflow Steps

1. Check if there are any changes to commit using `git status --porcelain`
2. If there are changes, invoke the **git-commit** skill as a sub-agent (low-complexity task):
   - Claude Code: `Task(subagent_type: "general-purpose", model: "haiku", prompt: "invoke git-commit skill" + args)`
   - Copilot: invoke `git-commit` skill with model `gpt-5.4-mini`
   - Codex: invoke git-commit agent (model: `gpt-5.4-mini`)
   - If commit message provided, pass it to git-commit
   - If `--mansplain` was passed, forward it to git-commit
   - This handles change analysis, staging, and committing with conventional format
   - Respects logical units of work
3. If there are no changes to commit, skip to step 4
4. **If `--issue <number>` was passed** — derive a conforming branch name (see Branch Rename below), then push via `scripts/push.sh --rename <new-branch-name>`
5. Otherwise push via `scripts/push.sh` (handles upstream tracking and the nothing-to-push case)
6. If there's nothing to commit or push, report this to the user and continue gracefully (this is not an error)

**Note**: This command ONLY commits and pushes. For PR creation/updates, use **git-commit-push-pr** instead.

## Branch Rename (when `--issue <number>` is passed)

This step enforces the branch naming convention from `.agents/rules/git/git-policy.instructions.md`:

```
<type>/<issue>-short-description
```

**How to derive the new branch name:**

1. **`<type>`** — take the type from the conventional commit just made (e.g. `feat`, `fix`, `chore`). If the branch already has a conforming name with the correct type, use that type.
2. **`<issue>`** — the number passed via `--issue`.
3. **`short-description`** — generate a concise, lowercase, hyphen-separated description (3–6 words) that summarises what was changed. Derive it from the commit message subject or the staged diff — do not reuse the current branch name verbatim.

**Execution:** `scripts/push.sh --rename <new-branch-name>` (renames the local branch and pushes with upstream tracking in one step).

**Constraints:**
- Only rename if the current branch name does NOT already conform to `<type>/<issue>-*` for the given issue number.
- If the current branch already matches (e.g. `feat/42-add-auth`), skip the rename and push normally.
- Tell the user the old and new branch names when a rename happens.

## Arguments

- Optional: pre-defined commit message (if not provided, will analyze changes and generate appropriate conventional commit message)
- `--issue <number>` — renames the local branch to `<type>/<number>-short-description` before pushing, ensuring branch naming consistency
- `--mansplain` — suppress all interactive questions; passed through to the **git-commit** sub-agent so it uses its best judgment without asking

## Usage Examples

```
/git-commit-push
/git-commit-push feat: add user authentication system
/git-commit-push --issue 42
/git-commit-push --issue 42 feat: add user authentication system
/git-commit-push --mansplain
/git-commit-push --mansplain --issue 42
```
