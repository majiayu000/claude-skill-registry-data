---
name: tzurot-git-workflow
description: Git workflow for Tzurot v3 - Rebase-only strategy, PR creation against develop, commit message format, and safety checks. Use when creating commits, PRs, or performing git operations.
lastUpdated: '2025-12-31'
---

# Tzurot v3 Git Workflow

**Use this skill when:** Creating commits, pushing changes, creating PRs, or performing any git operations.

## Quick Reference

```bash
# Start feature
git checkout develop && git pull origin develop
git checkout -b feat/your-feature

# Test before commit
pnpm test

# Create PR to develop
gh pr create --base develop --title "feat: description"
```

## 🚨 Critical Rules

### Rebase-Only Workflow

**NO SQUASH. NO MERGE. ONLY REBASE.**

GitHub settings enforce this - rebase and merge is the only option enabled.

### Always Target `develop` for PRs

```bash
# ✅ CORRECT
gh pr create --base develop --title "feat: your feature"

# ❌ WRONG - Never create feature PRs to main!
gh pr create --base main --title "feat: your feature"
```

### Test Before Push

```bash
pnpm test && git push origin <branch>
```

## Standard Workflow

### 1. Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feat/your-feature-name
```

**Branch prefixes:** `feat/`, `fix/`, `docs/`, `refactor/`, `chore/`, `test/`

### 2. Commit Changes

```bash
git commit -m "$(cat <<'EOF'
feat(ai-worker): add pgvector memory retrieval

Brief description of what and why.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`
**Scopes:** `ai-worker`, `api-gateway`, `bot-client`, `common-types`, `ci`, `deps`

### 3. Push and Create PR

```bash
git push -u origin feat/your-feature
gh pr create --base develop --title "feat: description"
```

### 4. After PR Merged

```bash
git checkout develop
git pull origin develop
git branch -d feat/your-feature
```

## Git Safety Protocol

### 🚨 NEVER Run Without Permission:

| Command            | Risk                       |
| ------------------ | -------------------------- |
| `git restore`      | Discards uncommitted work  |
| `git reset --hard` | Undoes commits permanently |
| `git clean -fd`    | Deletes untracked files    |
| `git push --force` | Rewrites history           |

### Golden Rules

1. **Uncommitted changes = HOURS OF WORK** - Never discard without confirmation
2. **Use safe alternatives:** `--force-with-lease`, `git branch -d` (not -D)
3. **When user says "get changes"** → They mean COMMIT, not DISCARD

## Git Hooks

**Source-controlled in `./hooks/`** (not `.git/hooks/`)

| Hook       | When         | What                        | Speed |
| ---------- | ------------ | --------------------------- | ----- |
| pre-commit | Every commit | Prettier + migration safety | ~5s   |
| pre-push   | Before push  | Lint, typecheck, tests      | ~60s  |

**Install:** `./scripts/git/install-hooks.sh`

**Never skip:** Don't use `--no-verify`

## Handling Rebase Conflicts

```bash
git checkout develop && git pull origin develop
git checkout feat/your-feature
git rebase develop

# If conflicts:
# 1. Resolve files
# 2. git add <resolved>
# 3. git rebase --continue
# Repeat until done

git push --force-with-lease origin feat/your-feature
```

## Release Workflow

### Version Bump (ALL package.json files!)

```bash
# Use the bump-version script - handles all 9 package.json files
pnpm bump-version 3.0.0-beta.31

# Review changes
git diff

# Commit
git commit -am "chore: bump version to 3.0.0-beta.31"
git push origin develop
```

**Script location:** `scripts/utils/bump-version.sh`

### Create Release PR

```bash
gh pr create --base main --head develop \
  --title "Release v3.0.0-beta.31: Description"
```

## Anti-Patterns

| ❌ Don't                      | ✅ Do                            |
| ----------------------------- | -------------------------------- |
| PRs to main (except releases) | PRs to develop                   |
| Push without testing          | `pnpm test && git push`          |
| Vague commits ("fix stuff")   | Descriptive commits              |
| Skip hooks (`--no-verify`)    | Fix the issues                   |
| Force push to main/develop    | Only force-push feature branches |

## Related Skills

- **tzurot-code-quality** - When lint fails, refactoring patterns
- **tzurot-docs** - Session handoff and CURRENT_WORK.md
- **tzurot-testing** - Run tests before committing
- **tzurot-security** - Pre-commit security checks

## GitHub CLI Quirks

**⚠️ ALWAYS check `docs/reference/GITHUB_CLI_REFERENCE.md` before running `gh` commands!**

### Known Broken Commands

```bash
# ❌ BROKEN - "Projects (classic) deprecation" error
gh pr edit 123 --body "new body"
gh pr edit 123 --title "new title"

# ✅ WORKAROUND - Use REST API directly
gh api -X PATCH repos/{owner}/{repo}/pulls/123 -f body="new body"
gh api -X PATCH repos/{owner}/{repo}/pulls/123 -f title="new title"

# ✅ Multiline body with HEREDOC
gh api -X PATCH repos/{owner}/{repo}/pulls/123 -f body="$(cat <<'EOF'
## Summary
- Changes here

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Comment Types

PRs have THREE different comment types with different endpoints:

- **Issue comments** (general): `gh pr view --json comments` or `/issues/{pr}/comments`
- **Review comments** (line-specific): `/pulls/{pr}/comments`
- **Reviews** (APPROVE, etc.): `gh pr view --json reviews`

## References

- **GitHub CLI Reference**: `docs/reference/GITHUB_CLI_REFERENCE.md` ← **CHECK THIS FIRST!**
- Full workflow: `CLAUDE.md#git-workflow`
- Post-mortems: `docs/postmortems/PROJECT_POSTMORTEMS.md`
