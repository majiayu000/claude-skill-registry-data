---
name: jmo-ship
description: "Rebase on main, commit, push, and optionally create a PR in one command. Use when the user says 'ship', 'ship it', 'send it', or wants to commit + push + PR in one step."
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Ship

Rebase on main, commit all changes, push to remote, and create a PR if on a feature branch. Do everything in one smooth flow.

## Process

### Step 1: Check state

Run these in parallel:
- `git status` (no `-uall` flag)
- `git diff` and `git diff --staged`
- `git branch --show-current`
- `git log --oneline -5`

### Step 2: Rebase on main

- Fetch the latest from origin: `git fetch origin main`
- Rebase the current branch onto the updated main: `git rebase origin/main`
- If the rebase has conflicts, stop and tell the user. Do NOT force-resolve or abort without asking.
- If the rebase succeeds cleanly, continue to the next step.

### Step 3: Stage and commit

- If there are no changes (no untracked files, no modifications), tell the user there's nothing to ship and stop.
- Stage all relevant files. Prefer `git add` with specific file paths over `git add -A`. Never stage files that look like secrets (.env, credentials, API keys).
- Write a concise commit message (1-2 sentences) that focuses on the "why" not the "what". Follow the repo's existing commit message style from git log.
- Always end the commit message with:
  ```
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
  ```
- Use a HEREDOC to pass the commit message:
  ```bash
  git commit -m "$(cat <<'EOF'
  Commit message here.

  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
  EOF
  )"
  ```

### Step 4: Push

- Push to the remote. If the branch has no upstream, use `git push -u origin <branch>`.
- If the branch already tracks a remote, use `git push`.

### Step 5: PR (if applicable)

- Determine if the current branch is `main` or `master`. If so, skip PR creation — just commit and push.
- If on a feature branch, check if a PR already exists for this branch: `gh pr view --json url 2>/dev/null`
  - If a PR already exists, skip creation and show the existing PR URL.
  - If no PR exists, create one using `gh pr create`:
    - Title: short, under 70 characters
    - Body: use this format with a HEREDOC:
      ```bash
      gh pr create --title "the pr title" --body "$(cat <<'EOF'
      ## Summary
      <1-3 bullet points summarizing changes>

      ## Test plan
      - [ ] Manual testing steps

      🤖 Generated with [Claude Code](https://claude.com/claude-code)
      EOF
      )"
      ```
- Print the PR URL at the end.

## Important rules

- Do NOT ask the user for confirmation at each step. Just do it all in one flow.
- If a pre-commit hook fails, fix the issue, re-stage, and create a NEW commit (never amend).
- Never use `--no-verify` or `--force`.
- If something goes wrong, stop and explain rather than retrying blindly.
