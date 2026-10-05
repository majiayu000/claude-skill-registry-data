---
name: commit-push-pr
description: Full git workflow - creates branch, commits, pushes, and creates or updates a PR with summary and test plan.
user_invocable: true
allowed-tools:
  - Bash(git checkout --branch:*)
  - Bash(git checkout -b:*)
  - Bash(git add:*)
  - Bash(git status:*)
  - Bash(git push:*)
  - Bash(git commit:*)
  - Bash(gh pr create:*)
  - Bash(gh pr edit:*)
  - Bash(gh pr view:*)
  - Bash(gh pr merge:*)
---

# Commit, Push, and Open PR

## Context

Gather this context first:
- `git status`
- `git diff HEAD`
- `git branch --show-current`
- `git diff main...HEAD` (or default branch)
- `gh pr view --json number 2>/dev/null || true`

## Git Safety Protocol

- NEVER update the git config
- NEVER run destructive/irreversible git commands (like push --force, hard reset, etc) unless the user explicitly requests them
- NEVER skip hooks (--no-verify, --no-gpg-sign, etc) unless the user explicitly requests it
- NEVER run force push to main/master, warn the user if they request it
- Do not commit files that likely contain secrets (.env, credentials.json, etc)
- Never use git commands with the -i flag (like git rebase -i or git add -i) since they require interactive input which is not supported

## Task

Analyze ALL changes that will be included in the pull request - look at ALL commits from `git diff main...HEAD`, not just the latest commit.

Based on the changes:

### 1. Create branch (if on main/master)
Use the format `username/feature-name`:
```
git checkout -b username/descriptive-feature-name
```

### 2. Create a single commit
Use heredoc syntax for the message:
```
git commit -m "$(cat <<'EOF'
Commit message here.
EOF
)"
```
- Follow the repo's commit message style (check `git log --oneline -10`)
- Focus on "why" not "what"
- Keep it concise (1-2 sentences)

### 3. Push the branch
```
git push -u origin HEAD
```

### 4. Create or update PR
Check if a PR already exists (from the `gh pr view` output above).

**If PR exists** - update it:
```
gh pr edit --title "Short title" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points>

## Test plan
- [ ] Test item 1
- [ ] Test item 2
EOF
)"
```

**If no PR** - create one:
```
gh pr create --title "Short, descriptive title" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points>

## Test plan
- [ ] Test item 1
- [ ] Test item 2
EOF
)"
```

**Rules:**
- Keep PR titles under 70 characters. Use the body for details.
- Summary should be 1-3 bullet points covering WHAT changed and WHY
- Test plan should be a checklist of verification steps

### 5. Return the PR URL

Do all of the above in a single message using multiple tool calls. Return the PR URL when done.
