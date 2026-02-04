---
name: git-pr-workflow
description: "Complete GitHub workflow from commit to PR including conventional commits, branch management, pre-push quality checks, PR creation with gh CLI, and wiki synchronization. Use when creating commits, ..."
---

# Git Pull Request Workflow for @j0kz/mcp-agents

Complete workflow from committing changes to creating pull requests with quality gates.

## When to Use This Skill

- Creating feature branches and commits
- Preparing code for pull request
- Running pre-push quality checks
- Creating PRs with gh CLI
- Synchronizing wiki documentation
- Following conventional commit standards

## Evidence Base

**Current State:**
- 25+ version releases with extensive PR history in CHANGELOG
- Conventional commits used throughout (feat:, fix:, docs:, refactor:, test:, chore:)
- GitHub Actions CI/CD (.github/workflows/)
- Wiki publishing workflow (publish-wiki.ps1)
- Code review patterns visible in release notes

---

## Core Workflow

### 1. Feature Branch Creation

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feat/your-feature-name

# Or for fixes
git checkout -b fix/issue-description
```

### 2. Conventional Commits

```bash
cat .claude/skills/git-pr-workflow/references/conventional-commits-guide.md
```

### 3. Pre-Push Quality Checks

Run ALL checks before pushing:

```bash
# 1. Build everything
npm run build

# 2. Run all tests (632+ tests)
npm test

# 3. Smart code review
npx @j0kz/smart-reviewer@latest review *.ts --severity=moderate

# 4. Security scan
npx @j0kz/security-scanner@latest scan . --severity=medium

# 5. Check for circular dependencies
npx @j0kz/architecture-analyzer@latest analyze . --detect-circular
```

### 4. Push & Create PR

```bash
# Push branch
git push -u origin feat/your-feature-name

# Create PR with gh CLI
gh pr create \
  --title "feat: add your feature description" \
  --body "$(cat <<'EOF'
## Summary
- Implement feature X that does Y
- Add comprehensive tests (+15 tests)
- Update documentation

## Changes
- Added new component in `src/components/`
- Updated API endpoints in `src/api/`
- Added 15 new test cases

## Test Plan
- [x] Unit tests pass (632/632)
- [x] Build succeeds
- [x] Security scan clean
- [x] No circular dependencies

## Screenshots
(if applicable)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)" \
  --base main
```

### 5. Conflict Resolution

```bash
cat .claude/skills/git-pr-workflow/references/conflict-resolution-guide.md
```

### 6. PR Review Process

```bash
cat .claude/skills/git-pr-workflow/references/pr-review-checklist.md
```

### 7. GitHub CLI Advanced Usage

```bash
cat .claude/skills/git-pr-workflow/references/github-cli-guide.md
```

---

## Quick Commands Reference

```bash
# View PR status
gh pr status

# List PRs
gh pr list

# View specific PR
gh pr view 123

# Check CI status
gh pr checks

# Merge PR (after approval)
gh pr merge --squash --delete-branch
```

---

## Wiki Synchronization

After PR merge, update wiki if docs changed:

```bash
# Run from Windows PowerShell
powershell.exe -File publish-wiki.ps1

# Or manually
cd wiki
git add .
git commit -m "docs: sync wiki with main branch updates"
git push
```

---

## Common Issues & Solutions

### Issue: Push Rejected

```bash
# If push rejected, pull and rebase
git pull --rebase origin main
git push --force-with-lease
```

### Issue: PR Checks Failing

```bash
# Check specific failures
gh pr checks

# Re-run failed checks
gh pr checks --watch
```

### Issue: Merge Conflicts

Follow the comprehensive guide:
```bash
cat .claude/skills/git-pr-workflow/references/conflict-resolution-guide.md
```

---

## Best Practices

1. **Always run full quality checks before pushing**
2. **Use conventional commits for clear history**
3. **Keep PRs focused (one feature/fix per PR)**
4. **Update tests for any logic changes**
5. **Synchronize wiki after documentation changes**
6. **Request reviews from relevant maintainers**
7. **Address review feedback promptly**

---

## Complete Example Workflow

```bash
# 1. Start fresh
git checkout main && git pull

# 2. Create feature branch
git checkout -b feat/add-bilingual-support

# 3. Make changes
# ... edit files ...

# 4. Stage and commit
git add -A
git commit -m "feat(orchestrator): add bilingual support for ES/EN

- Add language detection logic
- Create BilingualText interface
- Add 15 bilingual tests
- Update documentation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 5. Run quality checks
npm run build && npm test
npx @j0kz/smart-reviewer@latest review src/**/*.ts

# 6. Push and create PR
git push -u origin feat/add-bilingual-support
gh pr create --title "feat: add bilingual support" --body "..."

# 7. After approval, merge
gh pr merge --squash --delete-branch
```

---

**Verification:** Run `gh pr --help` to confirm GitHub CLI is installed.