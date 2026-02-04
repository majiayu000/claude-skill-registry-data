---
name: git-commit-standards
description: "Use when creating git commits or pull requests. Enforces conventional commit format and atomic change principles. Verified on Git 2.30+"
author: "Claude Code Learning Flywheel Team"
allowed-tools: ["Bash", "Read", "Grep"]
version: 1.2.0
last_verified: "2025-12-31"
tags: ["git", "workflow", "team-standards"]
related-skills: []
verification:
  test_script: "tests/skills/test_git_commit_standards.py"
  command: "python3 tests/skills/test_git_commit_standards.py"
  frequency: "on-change"
---

# Git Commit Standards

## 1. Context & Scope

This skill defines the team's git commit and pull request standards, ensuring consistent history and easy rollback/debugging.

**Trigger Conditions:**
- When user asks to "commit changes"
- When user asks to "create a pull request"
- Before running `git commit` or `gh pr create`

**Environment:**
- Git: 2.30+
- GitHub CLI (optional): 2.20+
- Pre-commit hooks: Enabled (validates format)

**Out of Scope:**
- Branching strategy (see `git-workflow` skill)
- Code review guidelines (see `code-review-process` skill)

---

## 2. Negative Knowledge (Read First)

*Common mistakes that have caused problems in the past.*

### Failed Attempts Table

| # | Attempted Strategy | Error/Symptom | Root Cause | Fix/Prevention |
|---|-------------------|---------------|------------|----------------|
| 1 | Used generic "fix bug" messages | Unable to identify which commit caused production issue | No context about WHAT was fixed | Use format: `fix(component): specific issue description` |
| 2 | Committed multiple unrelated changes together | Had to revert feature A but it also reverted unrelated fix B | Atomic commit principle violated | One logical change per commit, use `git add -p` |
| 3 | Used past tense "Added feature X" | Inconsistent with team convention, hard to scan history | Team uses imperative mood | Use "Add feature X" not "Added feature X" |
| 4 | Forgot to reference issue number | PM couldn't track which commits belonged to which feature | No traceability to project management | Add `Refs: #123` footer to all commits |

### Common Pitfalls

- **❌ Don't:** Write vague messages like "updates", "fixes", "changes"
  - **Why it fails:** 6 months later, impossible to understand intent
  - **✅ Do instead:** "fix(auth): prevent token expiry race condition"

- **❌ Don't:** Commit WIP code directly to main branch
  - **Why it fails:** Breaks CI/CD, blocks other developers
  - **✅ Do instead:** Use feature branches, squash before merge

- **❌ Don't:** Include passwords, API keys, or secrets in commits
  - **Why it fails:** Git history is permanent, secrets are exposed forever
  - **✅ Do instead:** Use .env files (gitignored), run `scripts/check_secrets.sh` pre-commit

---

## 3. Verified Procedure

> **IMPORTANT:** This skill is a "Tool Wrapper" - DO NOT analyze commit message format yourself.
> Use the deterministic validation script for accuracy and speed.

### Prerequisites Check

```bash
# Run automated pre-commit validator
python scripts/validate_commit_msg.py --check-setup

# Expected output: "✅ Git hooks installed, conventional commit format enabled"
```

### Step 1: Stage Changes Atomically

**Description:** Group related changes together, exclude unrelated changes

```bash
# Review what changed
git status
git diff

# Stage specific files (atomic changes)
git add path/to/changed/file.py

# OR stage interactively (parts of files)
git add -p path/to/file.py
# Press 'y' to stage hunks that belong together
# Press 'n' to skip unrelated changes
```

**Validation:**
```bash
# Verify only intended changes are staged
git diff --cached

# Expected: Only logically related changes visible
```

### Step 2: Write Conventional Commit Message

**Description:** Format message according to team standards

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types (choose one):**
- `feat`: New feature for the user
- `fix`: Bug fix for the user
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, tooling

**Example:**
```bash
git commit -m "$(cat <<'EOF'
feat(api): add rate limiting to /users endpoint

Implements token bucket algorithm with 100 req/min limit.
Prevents abuse observed in incident #456.

Refs: #123
Breaking Change: Clients must handle 429 status codes
EOF
)"
```

**Validation:**
```bash
# DO NOT validate commit message text manually
# Use the deterministic script instead:
python scripts/validate_commit_msg.py HEAD

# Expected output: "✅ Commit message follows conventional format"
# If errors returned, fix them based ONLY on script output
```

### Step 3: Verify Before Push

**Description:** Run final checks before pushing to remote

```bash
# Run tests (if applicable)
npm test  # or: pytest, cargo test, etc.

# Check commit message format
python scripts/validate_commit_msg.py HEAD

# Push to remote
git push -u origin <branch-name>
```

**Success Criteria:**
- [ ] Commit message follows conventional format
- [ ] Only one logical change per commit
- [ ] Tests pass locally
- [ ] No secrets or sensitive data included
- [ ] Issue number referenced (if applicable)

---

## 4. Configuration Reference

### Conventional Commit Format

**Regex Pattern:**
```regex
^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,72}$
```

**Scope Examples:**
- `api` - Backend API changes
- `ui` - Frontend user interface
- `db` - Database schema/migrations
- `auth` - Authentication/authorization
- `ci` - CI/CD pipeline changes

### Git Hooks Configuration

Create `.git/hooks/commit-msg`:
```bash
#!/bin/bash
# Validate commit message format
python scripts/validate_commit_msg.py "$1"
exit $?
```

Make executable:
```bash
chmod +x .git/hooks/commit-msg
```

---

## 5. Troubleshooting

### Error Pattern Recognition

| Error Message | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| `pre-commit hook failed` | Commit message doesn't match format | Amend with `git commit --amend` using correct format |
| `secret detected in commit` | API key or password in staged files | `git reset HEAD <file>`, add to `.gitignore`, use env vars |
| `diverged branches` | Remote has commits you don't have | `git pull --rebase origin main` then re-push |

### Diagnostic Commands

```bash
# Check recent commit history
git log --oneline -10

# See what would be committed
git diff --cached --stat

# Check for secrets (before committing)
python scripts/check_secrets.sh

# View commit message of last commit
git log -1 --pretty=%B
```

---

## 6. Reference Links

**Internal Documentation:**
- Full commit message examples: See `examples/commit-messages.md`
- Branching strategy: See `.claude/skills/git-workflow/SKILL.md`

**External Resources:**
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)

---

## 7. Maintenance Log

| Date | Version | Change Summary | Trigger |
|------|---------|----------------|---------|
| 2026-01-01 | 1.2.0 | Added executable verification framework integration | Agent Ops framework enhancement |
| 2025-12-31 | 1.1.0 | Refactored to Tool Wrapper pattern, verified skill still accurate | Architectural audit remediation |
| 2025-01-01 | 1.0.0 | Initial skill creation | Setup learning flywheel scaffold |

---

## 8. Metrics & Success Indicators

**How to measure if this skill is working:**

- **Consistency:** 95%+ of commits follow conventional format (checked in CI)
- **Traceability:** Every commit links to an issue or requirement
- **Revert Safety:** Can revert individual features without side effects

**When to update this skill:**
- When a commit causes a problem (add to Negative Knowledge)
- When team adopts new commit type or scope
- When git version changes behavior
