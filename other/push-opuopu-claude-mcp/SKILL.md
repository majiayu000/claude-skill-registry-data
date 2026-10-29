---
name: push
description: Review the latest changes, commit with an appropriate message, and push to GitHub
disable-model-invocation: true
allowed-tools: Bash(git *)
---

# Push Skill

When this skill runs, review the current codebase state, commit it, and push to the remote.

1. **Inspect the latest state** (run in parallel):
   - `git status` (never use `-uall`)
   - `git diff` and `git diff --staged`
   - `git log --oneline -10` to match the repo's commit message style
   - `git branch --show-current` and `git remote -v`
2. **Stop and report** if there is nothing to commit, there is no remote, or HEAD is detached.
3. **Choose what to stage.** Stage files by name, never `git add -A` or `git add .`. Do not stage:
   - secrets or likely-secret files (`.env`, credentials, keys); if unsure, read the file first
   - `input.md` (the UserPromptSubmit hook's prompt log) unless the user explicitly asks
   - large binaries or generated output
     Mention anything you skipped and why.
4. **Write the commit message** from the actual diff: one concise subject line (match the existing style, e.g. `feat: ...`, `fix: ...`, `docs: ...`) that explains why, plus a short body only if needed. Split unrelated changes into separate commits. Pass the message via a HEREDOC and end it with:

5. **Commit**, then run `git status` to confirm. If a hook fails, fix the issue and create a NEW commit; never use `--no-verify` or `--amend`.
6. **Push** the current branch with `git push` (use `git push -u origin <branch>` if it has no upstream). If the push is rejected because the remote is ahead, run `git pull --rebase` and retry once; if that conflicts, stop and ask. Never force push.
7. **Report** the commit hash(es), the branch, and the remote URL in one or two sentences.
