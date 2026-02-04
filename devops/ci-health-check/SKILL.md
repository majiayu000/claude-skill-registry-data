---
name: ci-health-check
description: Check CI/CD workflow status and troubleshoot failing checks in GitHub Actions
group: devops
keywords: [ci-cd, github-actions, troubleshooting, workflows, ci, cd, continuous integration]
version: 1.0.0
author: docent
---

# CI/CD Health Check Runbook

## Overview

This runbook provides procedures for checking the health of CI/CD pipelines running on GitHub Actions. Use this runbook to:

- Check status of workflow runs
- Troubleshoot failing checks
- Re-run failed workflows
- Analyze logs and diagnose issues

**Expected duration:** 5-10 minutes for status check; additional time for troubleshooting

## Prerequisites

### Required Tools

- `gh` CLI (GitHub CLI) - installed and authenticated
- `git` command line tool
- Terminal access

### Required Access

- Read access to the repository
- For fixing issues: Write access to create branches and PRs

### Pre-Flight Checklist

Before starting, ensure:

- [ ] You have `gh` CLI installed (`gh --version`)
- [ ] You are authenticated (`gh auth status`)
- [ ] You are in the project directory

## Procedure

### Step 1: Check Overall CI/CD Status

**Purpose:** Get a quick overview of all workflow runs

**Commands:**

```bash
# Check status of recent workflow runs
gh run list --limit 10

# Check status for a specific branch
gh run list --branch main --limit 10

# Check status for current PR (if in a branch)
gh run list --branch $(git branch --show-current) --limit 5
```

**Validation:**

- Output shows list of workflow runs with status (✓ completed, ✗ failed, * in_progress)
- Recent runs should show "completed" status

**If step fails:**

- Verify `gh` CLI is authenticated: `gh auth status`
- Ensure you're in a git repository: `git status`
- Check network connectivity

---

### Step 2: View Details of Failed Runs

**Purpose:** Identify which specific jobs failed in a workflow run

**Commands:**

```bash
# View the most recent failed run
gh run view $(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId')

# View a specific run by ID
gh run view <RUN_ID>

# Watch a run in progress
gh run watch
```

**Validation:**

- Output shows which jobs passed/failed
- Failed jobs are clearly marked
- Run URL is displayed for browser viewing

**If step fails:**

- If no runs found, check: `gh run list --limit 20`
- Run may have been deleted or archived

---

### Step 3: View Logs for Failed Jobs

**Purpose:** Get detailed logs to understand why a job failed

**Commands:**

```bash
# View logs for the most recent failed run
gh run view $(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId') --log

# View logs for a specific failed job
gh run view <RUN_ID> --log-failed

# Download all logs for offline analysis
gh run download <RUN_ID> --dir ./ci-logs
```

**Validation:**

- Logs show error messages and stack traces
- You can identify the specific step that failed
- Error context is visible

**If step fails:**

- Logs may be too large for terminal display
- Use `--log > output.log` to save to file
- Use GitHub web UI as fallback

---

### Step 4: Check Specific Workflow Status

**Purpose:** Focus on a specific workflow (Test or Lint)

**Commands:**

```bash
# List runs for test workflow
gh run list --workflow=ci.yml --limit 10

# List runs for lint workflow
gh run list --workflow=lint.yml --limit 10

# View status of both workflows for current branch
gh run list --workflow=ci.yml --branch $(git branch --show-current)
gh run list --workflow=lint.yml --branch $(git branch --show-current)
```

**Validation:**

- Shows runs specific to the workflow
- Can identify if one workflow is consistently failing
- Can compare success rates between workflows

**If step fails:**

- Verify workflow file names: `ls .github/workflows/`
- Workflow may not have run yet on current branch

---

### Step 5: Re-run Failed Workflows

**Purpose:** Retry failed workflows after fixing issues or if failure was transient

**Commands:**

```bash
# Re-run the most recent failed workflow
gh run rerun $(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId')

# Re-run only failed jobs
gh run rerun $(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId') --failed

# Watch the re-run
gh run watch
```

**Validation:**

- Command confirms re-run started
- New run appears in `gh run list`
- Can watch progress with `gh run watch`

**If step fails:**

- May not have permissions to re-run
- Workflow may be too old (>30 days)
- Try from GitHub web UI

---

## Validation

After completing all steps, verify:

1. **Overall Health:**

   ```bash
   gh run list --limit 5
   ```

   Expected result: Recent runs show ✓ (completed) status

2. **Both Workflows Passing:**

   ```bash
   gh run list --workflow=ci.yml --status success --limit 1
   gh run list --workflow=lint.yml --status success --limit 1
   ```

   Expected result: Both workflows have recent successful runs

3. **Current Branch Status:**

   ```bash
   gh run list --branch $(git branch --show-current)
   ```

   Expected result: Latest runs on current branch are successful

## Troubleshooting

### Common Issues

#### Issue 1: Test Workflow Failing - Installation Tests

**Symptoms:**

- Test workflow shows failure
- Error in "Run test suite" step
- Message about installation failure

**Resolution:**

```bash
# View the specific test failure
gh run view --log-failed

# Run tests locally to reproduce
npm test

# Common fixes:
# 1. Check if TypeScript compilation works
npm run build

# 2. Verify all test files are valid
npm test -- --reporter spec
```

---

#### Issue 2: ShellCheck Failures

**Symptoms:**

- Lint workflow fails at "ShellCheck" step
- Output shows shell script warnings/errors
- Specific scripts in `./scripts` or `./test` have issues

**Resolution:**

```bash
# View the specific shellcheck errors
gh run view --log-failed | grep -A 5 "ShellCheck"

# Install shellcheck (see Contributing Guide for other platforms)
brew install shellcheck  # macOS

# Run shellcheck locally
shellcheck ./scripts/*.sh ./test/*.sh

# Fix common issues:
# - Quote variables: "$var" instead of $var
# - Check for undefined variables
# - Fix array handling
# - Address exit code handling

# See Contributing Guide for detailed setup and troubleshooting
```

---

#### Issue 3: Markdown Lint Failures

**Symptoms:**

- Lint workflow fails at "Markdown Lint" step
- Markdown formatting issues in `*.md` files

**Resolution:**

```bash
# View the specific markdown errors
gh run view --log-failed | grep -A 10 "Markdown Lint"

# Install project dependencies (includes markdownlint-cli2)
npm install

# Run markdown lint locally
npx markdownlint-cli2 "**/*.md" "!node_modules"

# Common fixes:
# - Fix line length (MD013) - keep lines under 80 characters
# - Add blank lines around headers and lists (MD022, MD031, MD032)
# - Fix trailing spaces (MD009)
# - Consistent list styling (MD004, MD007)
# - Add language specifiers to code blocks (MD040)

# See Contributing Guide for more details on fixing markdown issues
```

---

#### Issue 4: Matrix Build Failures (Ubuntu vs macOS)

**Symptoms:**

- Test workflow fails on one OS but not the other
- Usually Ubuntu succeeds, macOS fails (or vice versa)

**Resolution:**

```bash
# View logs for specific OS
gh run view <RUN_ID> --log | grep -A 20 "Test on macos-latest"
gh run view <RUN_ID> --log | grep -A 20 "Test on ubuntu-latest"

# Common issues:
# - Path differences (/tmp vs /private/tmp on macOS)
# - Command availability (brew vs apt)
# - File permission differences
# - Line ending differences (CRLF vs LF)

# Test locally on both platforms if possible:
npm test
npm run build
```

---

#### Issue 5: Workflow Not Running

**Symptoms:**

- No workflow runs appear for recent commits
- PR doesn't show CI/CD checks

**Resolution:**

```bash
# Check workflow configuration
cat .github/workflows/ci.yml | grep -A 5 "on:"
cat .github/workflows/lint.yml | grep -A 5 "on:"

# Verify branch is configured to trigger workflows
gh run list --branch $(git branch --show-current) --limit 5

# Common causes:
# - Branch not pushed to remote: git push origin $(git branch --show-current)
# - Workflow only runs on main/specific branches
# - Workflow file has syntax errors
# - Repository settings disabled Actions
```

---

### When to Escalate

Escalate if:

- Workflows consistently fail across all branches
- Infrastructure issues (GitHub Actions down)
- Permissions issues preventing access to logs
- Repeated transient failures
- Security scanning alerts

**Escalation Contact:**

- Check GitHub status: https://www.githubstatus.com/
- Repository maintainer
- DevOps team lead

## Post-Procedure

After completion:

- [ ] Document any recurring issues encountered
- [ ] Update this runbook if new failure patterns emerge
- [ ] File issues for systematic problems
- [ ] Update workflow files if improvements identified

## Quick Reference

### Most Useful Commands

```bash
# Quick health check
gh run list --limit 5

# View latest failure
gh run view $(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId') --log-failed

# Re-run failed jobs
gh run rerun $(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId') --failed

# Watch current run
gh run watch

# Test locally (see Contributing Guide for setup)
./test/test-install.sh
shellcheck ./scripts/*.sh ./test/*.sh
npx markdownlint-cli2 "**/*.md"
```

## Notes

**Important Notes:**

- Always check logs before re-running - transient failures are rare
- Matrix builds can have OS-specific issues
- ShellCheck severity is set to "warning" - all warnings must be fixed
- Markdown linting is strict - follow conventions consistently

**Gotchas:**

- macOS test failures often relate to `/tmp` vs `/private/tmp` paths
- Workflow runs older than 30 days cannot be re-run
- Log downloads create nested directories by job name

**Related Procedures:**

- [Contributing Guide](../guides/contributing.md) - for development workflow and local checks

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-10-14 | @tnez | Initial creation |
