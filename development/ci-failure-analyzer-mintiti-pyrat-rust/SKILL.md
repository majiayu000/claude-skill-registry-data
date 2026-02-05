---
name: ci-failure-analyzer
description: Analyze GitHub Actions CI failures for the current branch. Use when the user asks about CI status, test failures, build errors, GitHub Actions problems, or mentions checking CI, workflow failures, or pipeline status.
allowed-tools: Bash, Grep
---

# CI Failure Analyzer

Analyzes GitHub Actions CI failures for the current git branch and provides detailed failure reports.

## Instructions

When the user asks about CI status, failures, or test errors, follow these steps:

### 1. Get the current branch name

```bash
git rev-parse --abbrev-ref HEAD
```

### 2. List recent CI runs for the current branch

```bash
gh run list --branch <branch-name> --limit 5
```

This shows the most recent workflow runs with their status (completed/success/failure).

### 3. Identify the most recent failed run

Look for runs with `failure` status in the output. Get the run ID (first column).

### 4. Get detailed failure logs

```bash
gh run view <run-id> --log-failed
```

This shows only the failed job logs, filtering out successful steps.

### 5. Extract key failure information

Parse the logs to find:
- Which test(s) failed
- The actual error messages and stack traces
- Which Python version or environment had the failure
- The root cause of the failure

Use grep to find error patterns:
```bash
gh run view <run-id> --log | grep -A 20 "FAILED"
gh run view <run-id> --log | grep -B 5 -A 30 "ERRORS\|FAILURES"
gh run view <run-id> --log | grep -A 100 "ModuleNotFoundError\|ImportError\|AssertionError"
```

### 6. Present a clear failure report

Format the report as:

```markdown
## CI Status for branch: <branch-name>

**Most recent run:** <status> (run ID: <run-id>)

### Failure Summary

- **Failed tests:** List of failed test names
- **Total results:** X failed, Y passed, Z skipped
- **Error type:** ModuleNotFoundError / AssertionError / etc.

### Root Cause

Clear explanation of what went wrong

### Failed Test Details

For each failed test:
- Test file and function name
- Error message
- Relevant stack trace excerpt
```

## Tips

- Always start with `gh run list --branch` to get the current branch status
- Use `--log-failed` first for concise output
- If more context is needed, use full `--log` with grep
- Look for patterns like "FAILED", "ERROR", "ModuleNotFoundError", "AssertionError"
- CI logs can be very long - focus on the actual failure messages
- Check multiple test environments (different Python versions) if failures occur

## Example Usage

**User asks:** "Check the CI status"

**You should:**
1. Get current branch: `git rev-parse --abbrev-ref HEAD`
2. List runs: `gh run list --branch <branch> --limit 5`
3. If failed, analyze: `gh run view <run-id> --log-failed`
4. Present failure report with root cause and failed tests

**User asks:** "Why did the tests fail?"

**You should:**
1. Follow same process as above
2. Deep dive into error messages with grep
3. Explain the root cause clearly
4. Suggest potential fixes if obvious from the error
