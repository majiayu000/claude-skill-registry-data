---
name: install-git-hooks
description: Install pre-commit hooks to automatically lint markdown files before commits
group: git
author: "@tnez"
version: 1.0.0
keywords: [git, hooks, automation, linting]
---

# Runbook: Install Git Hooks

**Purpose:** Install pre-commit hooks to automatically lint markdown files before commits
**Owner:** Development Team
**Last Updated:** 2025-10-20
**Frequency:** One-time setup per developer environment

## Overview

This runbook provides the procedure for installing git hooks in your local docent repository. Git hooks automatically run quality checks before committing, helping catch markdown linting errors early in the development process.

**Script Reference:** `../../scripts/install-git-hooks.sh`

**Expected duration:** 1-2 minutes

What this accomplishes:

- Installs pre-commit hook that runs markdown linting on staged `.md` files
- Prevents commits with markdown linting errors
- Provides early feedback before CI/CD runs

**Note:** This is **optional but recommended** for all developers.

## Prerequisites

### Required Tools

- `git` - Version control system
- `npm` - Node.js package manager
- Project dependencies installed (`npm install`)

### Required Access

- Write access to local `.git/hooks` directory (standard for any git repository)

### Pre-Flight Checklist

Before starting, ensure:

- [ ] You are in the docent project root directory
- [ ] Git repository is initialized (`.git` directory exists)
- [ ] Project dependencies are installed: `ls node_modules/markdownlint-cli2`
- [ ] You can write to `.git/hooks`: `ls -ld .git/hooks`

## Procedure

### Step 1: Verify Location

**Purpose:** Ensure you're in the correct directory

**Commands:**

```bash
# Verify you're in the docent project root
pwd
# Expected: /Users/tnez/Code/tnez/docent (or your path to docent)

# Verify git repository exists
ls -d .git
# Expected: .git

# Verify hooks directory exists
ls -d .git/hooks
# Expected: .git/hooks
```

**Validation:**

- You're in the project root
- `.git` directory exists
- `.git/hooks` directory exists

**If step fails:**

- Navigate to project root: `cd /path/to/docent`
- If `.git` doesn't exist: `git init` or clone the repository again

---

### Step 2: Run Installation Script

**Purpose:** Install the pre-commit hook

**Commands:**

```bash
# Run the installation script
scripts/install-git-hooks.sh

# Expected output:
# Installing pre-commit hook...
# ✓ Git hooks installed successfully
#
# The pre-commit hook will now run markdown linting on staged .md files.
# To bypass the hook, use: git commit --no-verify
#
# To uninstall, run: rm .git/hooks/pre-commit
```

**Validation:**

- Script completes successfully with ✓ message
- No error messages displayed
- Exit code is 0

**If step fails:**

- **Error: "Not in a git repository root directory"**
  - Navigate to project root and retry
  - Verify `.git` directory exists

- **Error: "Permission denied"**
  - Check file permissions: `ls -l scripts/install-git-hooks.sh`
  - Make executable if needed: `chmod +x scripts/install-git-hooks.sh`

- **Error: "No such file or directory"**
  - Verify hook source exists: `ls scripts/hooks/pre-commit`
  - Pull latest changes from repository

---

### Step 3: Verify Hook Installation

**Purpose:** Confirm the hook is properly installed and executable

**Commands:**

```bash
# Check hook file exists
ls -l .git/hooks/pre-commit
# Expected: -rwxr-xr-x ... .git/hooks/pre-commit

# View hook contents (first few lines)
head -5 .git/hooks/pre-commit
# Expected: Should show shell script starting with #!/bin/sh
```

**Validation:**

- File `.git/hooks/pre-commit` exists
- File is executable (permissions include `x`)
- File contains shell script code

**If step fails:**

- Hook file missing: Re-run installation script
- Not executable: `chmod +x .git/hooks/pre-commit`

---

### Step 4: Test Hook

**Purpose:** Verify the hook runs on commit

**Commands:**

```bash
# Create a test markdown file with linting errors
echo "# Test" > test-lint.md
echo "No blank line before list:" >> test-lint.md
echo "- item 1" >> test-lint.md

# Stage the file
git add test-lint.md

# Try to commit (hook should run and may fail if linting errors)
git commit -m "test: verify pre-commit hook"

# Expected: Hook runs markdown linting
# If there are errors, commit will be blocked

# Clean up test file
git reset HEAD test-lint.md
rm test-lint.md
```

**Validation:**

- Hook runs when you attempt to commit
- You see markdown linting output
- Commit is blocked if there are linting errors (expected behavior)

**If step fails:**

- Hook doesn't run: Verify installation in Step 3
- Hook runs but always passes: Check hook script contents
- Permission errors: Verify hook is executable

---

## Validation

After completing all steps, verify:

1. **Hook Installed:**

   ```bash
   ls -l .git/hooks/pre-commit
   # Expected: File exists and is executable
   ```

2. **Hook Runs on Commit:**

   - Create and stage a markdown file
   - Run `git commit`
   - Observe hook output

3. **Can Bypass if Needed:**

   ```bash
   git commit --no-verify -m "test"
   # Expected: Commit succeeds without running hook
   git reset HEAD~1  # Undo test commit
   ```

## Uninstall

If you need to remove the git hooks:

### Remove Pre-Commit Hook

```bash
# Remove the hook
rm .git/hooks/pre-commit

# Verify removal
ls .git/hooks/pre-commit
# Expected: No such file or directory
```

**When to uninstall:**

- You prefer to run linting manually
- Hook is causing issues
- Switching to a different linting workflow

**Note:** You can always reinstall by running the installation script again.

## Troubleshooting

### Common Issues

#### Issue 1: Hook Blocks All Commits

**Symptoms:**

- Every commit attempt is blocked
- Linting errors on files you didn't change

**Resolution:**

```bash
# Check what files have linting errors
npm run lint:md

# Fix errors
scripts/lint-markdown.sh --fix

# Or bypass for urgent commits
git commit --no-verify -m "message"

# Then fix linting separately
```

---

#### Issue 2: Hook Doesn't Run

**Symptoms:**

- Commits succeed without any hook output
- No linting checks performed

**Resolution:**

```bash
# Verify hook exists and is executable
ls -l .git/hooks/pre-commit

# If missing, reinstall
scripts/install-git-hooks.sh

# If not executable
chmod +x .git/hooks/pre-commit

# Test with verbose output
git commit --dry-run -m "test"
```

---

#### Issue 3: markdownlint-cli2 Not Found

**Symptoms:**

- Hook runs but fails with "command not found"
- Error about missing markdownlint-cli2

**Resolution:**

```bash
# Install project dependencies
npm install

# Verify markdownlint-cli2 is available
npx markdownlint-cli2 --version

# If still failing, check hook script
cat .git/hooks/pre-commit
```

---

### When to Escalate

Escalate if:

- Hook installation script fails consistently
- Hook causes git to hang or crash
- Hook blocks valid commits repeatedly
- Need to modify hook behavior

**Escalation Contact:**

- Repository maintainer
- Development team lead

## Post-Procedure

After installation:

- [ ] Hook successfully runs on commit attempts
- [ ] You understand how to bypass with `--no-verify`
- [ ] You know how to uninstall if needed
- [ ] Team members are notified (if setting up for entire team)

## Quick Reference

### Essential Commands

```bash
# Install hooks
scripts/install-git-hooks.sh

# Verify installation
ls -l .git/hooks/pre-commit

# Bypass hook for one commit
git commit --no-verify -m "message"

# Uninstall hook
rm .git/hooks/pre-commit

# Test linting manually
npm run lint:md
scripts/lint-markdown.sh
```

## Notes

**Important Notes:**

- Hook is local to your repository - not committed or shared via git
- Each developer must install hooks separately
- Hook only runs on `git commit`, not on `git push` or other commands
- Bypassing with `--no-verify` should be rare - prefer fixing linting errors

**Gotchas:**

- Hook only lints **staged** markdown files, not all files
- If you have unstaged changes in markdown files, those won't be linted
- Journal files in `docs/.journal/` are gitignored and won't be linted
- Hook runs before commit message editor opens

**Related Procedures:**

- [Fix Markdown Linting](./fix-markdown-lint.md) - for fixing linting errors the hook finds
- [Contributing Guide](../guides/contributing.md) - general development workflow

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-10-20 | @tnez | Initial creation |
