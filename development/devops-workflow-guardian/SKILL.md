---
name: devops-workflow-guardian
description: "Enforces DevOps best practices for commits, merges, and PRs. Use when user requests a commit, merge, or pull request. Analyzes changes, validates quality, composes conventional commit messages, and ensures user approval before any git operations."
---

# DevOps Workflow Guardian

## Purpose

Ensure all git operations follow best practices: conventional commits, proper branching, clean merges, and user-confirmed actions. This skill orchestrates with `test-driven-development` and `using-git-worktrees` skills when appropriate.

## Quick Reference

| Operation | Key Steps |
|-----------|-----------|
| **Commit** | Analyze → Validate → Compose message → Confirm → Execute |
| **Merge** | Check sync → Identify conflicts → Resolve → Confirm → Execute |
| **PR** | Analyze all commits → Generate description → Confirm → Create |

**Iron Rule:** Never execute git operations without user confirmation.

---

## Commit Workflow

### 1. Analyze Changes

```bash
# Check current state
git status
git diff --staged
git diff  # unstaged changes
```

**Identify:**
- What files changed and why
- Logical grouping (single concern per commit)
- Sensitive files that should NOT be committed

**Red flags - STOP and warn user:**
- `.env`, `.env.local`, `credentials.json`, `*.pem`, `*.key`
- Files containing API keys, passwords, tokens
- Large binary files (>10MB)
- Node_modules, build artifacts, cache directories

### 2. Validate Before Commit

**Run checks (if configured in project):**
```bash
# Check for test command
npm test 2>/dev/null || yarn test 2>/dev/null || pytest 2>/dev/null
```

**If tests fail:**
> "Tests are failing. Would you like to:
> 1. Fix the tests first (recommended)
> 2. Commit anyway with a note about failing tests
> 3. Skip tests for this commit"

**If no test command found:** Proceed, but note in commit if significant changes.

### 3. Compose Commit Message

Follow [Conventional Commits](reference/conventional-commits.md) format:

```
type(scope): description

[optional body]

[optional footer]
```

**Determine type from changes:**

| Change Type | Commit Type |
|-------------|-------------|
| New feature | `feat` |
| Bug fix | `fix` |
| Documentation | `docs` |
| Refactoring (no behavior change) | `refactor` |
| Performance improvement | `perf` |
| Tests | `test` |
| Build/dependencies | `build` |
| CI/CD changes | `ci` |
| Formatting/style | `style` |
| Maintenance/chores | `chore` |

**Breaking changes:** Add an exclamation mark (!) after the type and include a `BREAKING CHANGE:` footer.

### 4. Confirm with User

Present for approval:

```
Proposed commit:
─────────────────────────────────────
feat(auth): add JWT token validation

Add middleware to validate JWT tokens on protected routes.
Includes token expiry checking and refresh logic.
─────────────────────────────────────

Files to commit:
  M src/middleware/auth.ts
  A src/utils/jwt.ts
  M src/routes/protected.ts

Proceed with commit? [y/n/edit]
```

**Wait for explicit approval.** Never auto-commit.

### 5. Execute Commit

```bash
git add <files>
git commit -m "$(cat <<'EOF'
type(scope): description

Body text here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Merge Workflow

### 1. Check Branch Status

```bash
# Ensure we're on the right branch
git branch --show-current

# Check if up to date with remote
git fetch origin
git status -uno

# Check relationship with target branch
git log --oneline main..HEAD  # commits to merge
git log --oneline HEAD..main  # commits we're behind
```

### 2. Identify Conflicts

```bash
# Dry-run merge to check for conflicts
git merge --no-commit --no-ff main
git merge --abort  # if conflicts, abort and report
```

**If conflicts exist:** See [Conflict Resolution](reference/conflict-resolution.md)

### 3. Choose Strategy

Based on situation, recommend:

| Situation | Strategy |
|-----------|----------|
| Local unpushed commits | Rebase onto target |
| Shared/pushed branch | Merge (preserve history) |
| Many small commits | Squash merge |
| Long-running feature | Merge (avoid repeated rebasing) |

See [Branching Strategies](reference/branching-strategies.md) for details.

### 4. Confirm and Execute

```
Merge plan:
─────────────────────────────────────
Source: feature/auth (3 commits ahead)
Target: main (2 commits behind)
Strategy: Rebase then merge (recommended)

Steps:
1. git fetch origin main
2. git rebase origin/main
3. git checkout main
4. git merge feature/auth
─────────────────────────────────────

Proceed? [y/n]
```

---

## Pull Request Workflow

### 1. Analyze All Commits

```bash
# Get full commit history for this branch
git log --oneline main..HEAD

# Get full diff against target
git diff main...HEAD --stat
```

**Review ALL commits, not just the latest.** PR description must reflect complete changes.

### 2. Check PR Readiness

- [ ] All tests passing
- [ ] Branch up to date with target (or conflicts identified)
- [ ] No WIP commits (or squash them)
- [ ] No sensitive files included

### 3. Generate PR Description

```markdown
## Summary
<2-3 bullet points describing what this PR does>

## Changes
<List of significant changes by area>

## Test Plan
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Edge cases considered

## Related Issues
Closes #<issue-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 4. Create PR

```bash
# Push branch if needed
git push -u origin $(git branch --show-current)

# Create PR
gh pr create --title "type(scope): description" --body "$(cat <<'EOF'
## Summary
...

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Return PR URL to user.**

---

## Orchestration

### When to Invoke Other Skills

**Before implementation work:**
> "This looks like a feature implementation. Invoking `test-driven-development` skill to ensure TDD practices."

**When workspace isolation needed:**
> "This work could benefit from an isolated workspace. Invoking `using-git-worktrees` skill."

**This skill handles:**
- All git commit operations
- Branch management
- Merge/rebase operations
- PR creation and updates
- Conflict resolution guidance

---

## Safety Rules

1. **Never force push to main/master** without explicit user request and warning
2. **Never commit sensitive files** - always warn and exclude
3. **Never auto-commit** - always show and confirm
4. **Never amend pushed commits** without checking authorship first
5. **Never skip hooks** (--no-verify) unless user explicitly requests

### Before Amending

```bash
# Check authorship
git log -1 --format='%an %ae'

# Check if pushed
git status  # "Your branch is ahead of..."
```

Only amend if:
- You are the author, AND
- Commit is not pushed, OR
- User explicitly confirms

---

## Common Patterns

### Atomic Commits

One logical change per commit. If you find yourself writing "and" in the commit message, split it.

**Bad:** `feat: add login page and fix header styling and update deps`

**Good:** Three separate commits:
1. `feat(auth): add login page`
2. `fix(ui): correct header styling on mobile`
3. `build: update dependencies`

### Commit Frequency

- Commit when a logical unit of work is complete
- Commit before switching context
- Commit before risky operations (refactoring, rebasing)

### Branch Naming

```
type/description-in-kebab-case

Examples:
feature/user-authentication
fix/login-redirect-loop
refactor/extract-validation-utils
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Committed sensitive file | `git reset HEAD~1`, remove file, recommit |
| Wrong commit message | `git commit --amend` (if not pushed) |
| Committed to wrong branch | `git reset HEAD~1`, stash, checkout correct branch, apply |
| Merge conflict hell | Abort, try rebase with smaller steps, or see conflict resolution guide |
| Tests failing in CI but not locally | Check environment differences, run with `--verbose` |

---

## Verification Checklist

Before finalizing any git operation:

- [ ] Changes analyzed and understood
- [ ] Sensitive files excluded
- [ ] Tests passing (or user acknowledged)
- [ ] Commit message follows conventional format
- [ ] User explicitly confirmed action
- [ ] No force operations on shared branches
