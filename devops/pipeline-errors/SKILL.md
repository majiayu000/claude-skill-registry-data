---
name: pipeline-errors
description: Fetch and analyze GitHub Actions pipeline errors. Use when the user wants to debug CI/CD failures, check workflow runs, or troubleshoot test failures.
---

# Pipeline Errors Fetcher

This skill automatically fetches GitHub Actions pipeline errors and displays them for debugging. It eliminates the need to manually copy/paste errors from GitHub.

## When to Use This Skill

Invoke this skill when:
- User mentions pipeline failures, CI/CD errors, or test failures
- User asks about GitHub Actions errors
- User wants to check the status of workflow runs
- User says "the tests are failing" or "the build is broken"
- User asks "what's wrong with the pipeline?"
- Starting work on a feature branch to check if tests are passing

## How It Works

The skill uses the `fetch-pipeline-errors.sh` script which:
1. Detects the current git branch
2. Fetches failed workflow runs from GitHub API
3. Downloads logs from failed jobs
4. Displays the last 50 lines of logs (where errors typically appear)
5. Provides direct links to view full details on GitHub

## Prerequisites

Before the skill can work, verify the user has set up their GitHub token:

1. Check if `.env` file exists with `GITHUB_TOKEN`
2. If not, guide them through setup:
   - Get token at: https://github.com/settings/tokens/new
   - Required permissions: `repo` and `actions:read`
   - Create `.env` file: `cp .env.example .env`
   - Add token to `.env`: `GITHUB_TOKEN=ghp_xxxxx`

## Running the Skill

### Default: Current Branch Errors

```bash
./fetch-pipeline-errors.sh
```

This shows failed workflow runs for the current git branch.

### All Branches

```bash
./fetch-pipeline-errors.sh --all
```

This shows recent failures across all branches.

### Show More Results

```bash
./fetch-pipeline-errors.sh --limit 10
```

This shows more than the default 5 workflow runs.

## Analyzing the Output

When you receive the output, analyze it to:

1. **Identify the failure type:**
   - Build errors (compilation, syntax)
   - Test failures (which tests, why they failed)
   - Environment issues (missing dependencies, config problems)
   - Timeout issues
   - Database/service connection errors

2. **Extract key information:**
   - Which workflow failed (e.g., "E2E Tests", "Build")
   - Which job failed within the workflow
   - Which step failed within the job
   - The actual error message
   - Stack traces if available

3. **Present findings to user:**
   - Summarize what failed
   - Quote the relevant error message
   - Suggest likely causes
   - Propose solutions

## Example Workflow

**User says:** "The tests are failing on my branch"

**Your response:**
1. Check if `.env` exists and has `GITHUB_TOKEN`
   - If not: Guide through setup
   - If yes: Proceed to fetch errors
2. Run: `./fetch-pipeline-errors.sh`
3. Analyze the output
4. Present findings:
   ```
   The E2E Tests workflow failed on step "Run E2E tests".

   Error found:
   ```
   Error: Timeout of 30000ms exceeded waiting for backend to be ready
   ```

   This indicates the backend server didn't start in time. Possible causes:
   - Port 3002 already in use
   - Database connection issues
   - Missing environment variables

   Would you like me to check the backend startup configuration?
   ```

## Common Error Patterns

### Build Errors
```
Error: Cannot find module 'xyz'
```
**Action:** Check if dependency is in package.json, suggest `npm install`

### Test Failures
```
Error: expect(received).toBe(expected)
Expected: 200
Received: 404
```
**Action:** Analyze test failure, check endpoint implementation

### Timeout Errors
```
timeout 30 bash -c 'until curl -f http://localhost:3002/health; do sleep 2; done'
```
**Action:** Check if service is starting correctly, review logs

### Database Errors
```
Error: connect ECONNREFUSED 127.0.0.1:5433
```
**Action:** Check database service configuration in workflow

### Environment Variable Errors
```
Error: JWT_SECRET is not defined
```
**Action:** Check workflow env vars, compare with .env.example

## Tips for Using This Skill

1. **Always fetch latest errors** - Run the script before starting debugging
2. **Check context** - Look at recent commits that might have caused the failure
3. **Read the full logs** - The last 50 lines usually contain the error, but check GitHub link if needed
4. **Compare with successful runs** - Use `--all` to see if other branches pass
5. **Proactive checking** - Run this when switching to a branch to check CI status

## Troubleshooting

### Script fails with "GITHUB_TOKEN not found"
- User needs to set up `.env` file with token
- Guide them through token creation process

### API rate limit exceeded
```json
{
  "message": "API rate limit exceeded"
}
```
- GitHub has rate limits for API calls
- Authenticated requests get higher limits (5000/hour)
- Suggest waiting or using fewer `--limit` requests

### No failed runs found
```
No failed workflow runs found!
```
- Good news! Tests are passing
- Inform user their pipeline is green

### Invalid JSON response
- Check if GitHub token has correct permissions
- Verify token is valid (not expired)
- Check network connectivity

## Integration with Development Workflow

Use this skill as part of the development cycle:

1. **Before starting work:**
   - Check if current branch has failures
   - Fix any existing issues before adding new code

2. **After pushing changes:**
   - Wait for workflow to complete
   - Fetch errors if build fails
   - Debug and fix immediately

3. **Before creating PR:**
   - Ensure all workflows pass
   - Clean up any test failures

4. **During code review:**
   - Check if reviewer's comments relate to pipeline failures
   - Verify fixes resolve the errors

## Quick Reference

```bash
# Current branch failures
./fetch-pipeline-errors.sh

# All branches
./fetch-pipeline-errors.sh --all

# Show 10 most recent
./fetch-pipeline-errors.sh --limit 10

# Combine options
./fetch-pipeline-errors.sh --all --limit 20
```

## Remember

- **Be proactive:** Check pipeline status without being asked
- **Be specific:** Quote exact error messages
- **Be helpful:** Suggest concrete fixes, not just identifying problems
- **Be contextual:** Consider what the user is working on
- **Save time:** This eliminates manual copy/paste of errors from GitHub UI

Use this skill to streamline CI/CD debugging and keep the development process flowing smoothly.
