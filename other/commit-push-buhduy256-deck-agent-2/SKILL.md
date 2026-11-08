---
name: commit-push
description: Commit staged or unstaged changes with a conventional commit message, then push to the remote. Use when the user wants to commit and push in one step, ship changes, or send work to the remote.
allowed-tools: Bash(git:*), Read, Grep, Edit
user-invocable: true
---

# Git Commit & Push Skill

## Overview

Create a well-structured git commit with a conventional commit message, then push it to the remote — one workflow, no extra steps.

## Instructions

### 1. Check the current state

Run these commands in parallel:
- `git status` to see staged and unstaged changes
- `git diff --cached` to see what's staged
- `git diff` to see unstaged changes
- `git log --oneline -5` to see recent commit style
- `git remote -v` to confirm a remote exists

If no remote is configured, stop and tell the user — there's nowhere to push.

### 2. Check the branch

- Note the current branch name.
- If the branch is `main` or `master`, warn the user that they're about to push directly to the primary branch and ask whether to continue.

### 3. Stage changes if needed

If there are unstaged changes the user wants to commit, stage them with `git add`.

### 4. Analyze the changes

Review what's being committed:
- What files are affected?
- What's the nature of the change (fix, feature, refactor, docs, etc.)?
- What's the primary purpose?

### 5. Update CHANGELOG.md

Add a description of the changes under the `## [Unreleased]` section:
- Read the top of `CHANGELOG.md` to see the current format
- If there's no `## [Unreleased]` section, create one at the top (after the header)
- Add entries under the appropriate category header:
  - `### Added` — New features or capabilities
  - `### Changed` — Changes to existing functionality
  - `### Fixed` — Bug fixes
  - `### Removed` — Removed features or code
  - `### Security` — Security-related changes
- Each entry should be a bullet point with a clear description
- Stage the CHANGELOG.md changes with `git add CHANGELOG.md`

### 6. Generate a commit message

Follow this format:
```
<type>: <short description>

<optional body explaining what and why>
```

Never add a `Co-Authored-By` trailer or any attribution to Claude or any other AI agent or model (AGENTS.md "GitHub conventions").

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation changes
- `style`: Formatting, whitespace
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependencies

### 7. Create the commit

Use a HEREDOC for proper formatting:
```bash
git commit -m "$(cat <<'EOF'
type: short description

Optional longer description.
EOF
)"
```

### 8. Push to the remote

- If the branch already tracks an upstream, run `git push`.
- If no upstream is set, run `git push -u origin <branch>` to set tracking.

If the push is rejected (e.g. the remote has newer commits), report the error to the user. Do not force-push or rebase automatically.

### 9. Verify success

Run `git status` and confirm:
- The working tree is clean (or only has intentionally uncommitted files)
- The branch is up to date with the remote

Report the commit hash and the remote URL the changes were pushed to.

## Guidelines

- Keep the first line under 72 characters
- Use imperative mood ("add feature" not "added feature")
- Focus on WHY the change was made, not just WHAT changed
- Don't include file lists in the message — git tracks that
- Match the style of recent commits in the repo when possible

## Safety

- Never use `--force` or `--force-with-lease` on push
- Never skip hooks with `--no-verify` unless explicitly asked
- Never amend commits that have been pushed
- If there are no changes to commit, inform the user
- If push fails, report the error — never force-push or rebase to work around it
