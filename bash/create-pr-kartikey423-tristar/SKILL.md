---
name: create-pr
description: Create GitHub pull requests for TriStar features. Runs pre-flight checks, security scan, generates PR description from SDLC artifacts, and manages PR lifecycle.
allowed-tools: Bash, Read
---

# Create PR Skill

## Prime Directive

**"Every PR tells a story. Make it complete."**

Create well-documented pull requests with security scans, artifact references, and clear descriptions. Manage the full PR lifecycle from creation through merge.

## Arguments

- Default: create a new PR for the current branch
- `--status`: check existing PR status
- `--reviewers=<list>`: assign reviewers
- `--merge`: merge the PR (after checks pass)

## Pre-Flight Checks

Before creating a PR, verify:

1. **GitHub CLI authenticated**: `gh auth status`
2. **Not on main/master branch**: refuse to create PR from protected branches
3. **No uncommitted changes**: `git status` shows clean working tree
4. **Branch has commits ahead of base**: `git log main..HEAD` shows commits
5. **Remote branch exists or push first**: ensure branch is pushed with `-u` flag

## Process

### Step 1: Pre-Flight

Run all pre-flight checks. If any fail, report the failure and stop.

### Step 2: Security Scan

Run `bash scripts/security-scan.sh` if the script exists. If it fails, warn the user but do not block (they may choose to proceed).

### Step 3: Gather Context

1. Read `git log main..HEAD --oneline` for commit history
2. Read `git diff main...HEAD --stat` for changed files summary
3. Check for SDLC artifacts in `docs/artifacts/` relevant to this branch
4. Read any available artifacts (problem_spec.md, design_spec.md, verification_report.md, risk_assessment.md)

### Step 4: Generate PR Title

Use conventional commit format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `refactor`: Code restructure
- `test`: Add/update tests
- `chore`: Tooling, dependencies

Determine type from commit messages and changed files. Keep title under 70 characters.

### Step 5: Generate PR Description

Use the template from `templates/pr-description.md`. Fill in:
- Summary from commit messages and changed files
- Layers affected (from artifact or file analysis)
- Type of change
- Test plan
- Security status
- SDLC artifact references (if available)

### Step 6: Create PR

Use `gh pr create` with the generated title and body.

```bash
gh pr create --title "<title>" --body "<body>"
```

### Step 7: Report

Output the PR URL and a summary of what was created.

## Branch Naming Convention

- `feature/<description>` - New feature development
- `bugfix/<description>` - Bug fix
- `docs/<description>` - Documentation changes
- `refactor/<description>` - Code restructuring
- `test/<description>` - Test additions

## PR Lifecycle Operations

### Status Check
```bash
gh pr status
gh pr checks
```

### Assign Reviewers
```bash
gh pr edit --add-reviewer <username>
```

### Merge (after approval)
```bash
gh pr merge --squash --delete-branch
```

## Important Rules

1. Do NOT add Co-Authored-By lines to PR descriptions
2. Do NOT push to main/master directly
3. Do NOT create PRs from main/master branch
4. Always run security scan before creating PR
5. Always include SDLC artifact references when available
6. Use conventional commit format for PR titles

## Templates

- `templates/pr-description.md` - PR body template
