---
name: getting-pr-workflow-results
description: Use when needing workflow job results and log commands from PR - automatically waits for workflows to complete, then returns job summaries with gh commands to retrieve logs without loading large logs into context
---

# Getting PR Workflow Results

## Overview

Get workflow job results and provide commands to retrieve logs, without loading logs into main context.

**Core principle:** Return job summaries + retrieval commands, not actual logs. Let main agent decide what to fetch.

**Automatic dependency:** This skill automatically waits for workflows to complete before fetching results.

## CRITICAL: Scope Guardrails

**This skill reports workflow status with error details. It NEVER fixes issues.**

When you find failures:
- ✅ Report which jobs failed
- ✅ Extract actual error messages and test failures from logs
- ✅ Include context (what operation was in progress when it failed)
- ✅ Provide commands to retrieve full logs for deeper investigation
- ✅ Suggest grep patterns to search logs
- ❌ DO NOT investigate root causes beyond what's in the error messages
- ❌ DO NOT propose fixes
- ❌ DO NOT make any code changes

**Why:** This skill runs in a subagent to save tokens. It extracts actionable error information but
  doesn't try to fix anything. Return the error details and let the caller decide what to do.

## When to Use

Use when you need:
- Summary of which jobs passed/failed
- Commands to retrieve specific job logs
- Suggestions for searching logs (grep patterns)

**When NOT to use:**
- Need to actually read logs (use returned commands in main context)

## Workflow

### Step 0: Wait for Workflows to Complete (Automatic)

Before fetching results, ensure all workflows are complete by following the `awaiting-pr-workflows` skill.

**Skill location:** `~/.claude/skills/awaiting-pr-workflows/SKILL.md`

Read and execute that skill's workflow to:
- Check for unpushed commits
- Verify PR exists and commit correlation
- Wait for workflows to start (up to 30s)
- Wait for workflows to complete (up to 20 minutes)

Once all workflows are complete, proceed to Step 1 below.

### Step 1: Get Workflow Runs for PR Commit

```bash
# Get PR's head commit
PR_COMMIT=$(gh pr view $PR_NUM --json headRefOid -q '.headRefOid')

# List workflow runs for that commit
gh run list --commit $PR_COMMIT --json databaseId,name,status,conclusion,workflowName,createdAt
```

### Step 2: For Each Run, Get Job Details

```bash
RUN_ID=<from step 1>

# Get jobs in this run
gh run view $RUN_ID --json jobs --jq '.jobs[] | {
  name: .name,
  conclusion: .conclusion,
  url: .html_url,
  steps: [.steps[] | select(.conclusion == "failure") | .name]
}'
```

### Step 3: Check for Artifacts

Check if the run has artifacts that might help with debugging:

```bash
# List artifacts for this run
gh run view $RUN_ID --json artifacts --jq '.artifacts[] | {
  name: .name,
  size: .size_in_bytes,
  expired: .expired
}'
```

**Common useful artifacts:**
- Test reports (JUnit XML, HTML reports)
- Screenshots (for UI test failures)
- Crash logs
- Coverage reports
- Build artifacts

### Step 4: Extract Error Messages from Failed Jobs

For failed jobs, retrieve the logs and extract key errors:

```bash
# Get failed logs
LOGS=$(gh run view $RUN_ID --log-failed)

# Extract pertinent errors (examples):
# - Test failures: grep for "FAILED", "✗", test names
# - Build errors: grep for "error:", "fatal:", compiler messages
# - Lint errors: grep for "warning:", "expected", actual vs expected
# - Runtime errors: grep for "Exception", "Error:", stack traces
```

**What to extract:**
- Specific test names that failed
- Error messages (first few lines of stack traces, not full traces)
- What operation was in progress (e.g., "compiling", "running test X")
- Exit codes if non-zero

**What NOT to extract:**
- Full logs (too verbose)
- Debug output
- Passing tests

### Step 5: Build Return Summary

For each job, return:

1. **Job name and result**
2. **Actual error messages/failures** (extracted from logs)
3. **Context** (what was happening when it failed)
4. **Artifacts** (if any exist for the run)
5. **Location in repo** (workflow file path + line if applicable)
6. **gh commands** to retrieve full logs and download artifacts
7. **grep suggestions** for common issues

## Return Format

```markdown
PR #{number} Workflow Results (commit {sha}):

## ✅ Passing Jobs (N)
- Backend Tests
- iOS Lint
- workstation-test-e2e

## ❌ Failing Jobs (N)

### 1. iOS Test (failed after 7m28s)
**Workflow:** `.github/workflows/ci.yml:45`

**Errors found:**
```
testHealthCheckE2E FAILED
  Error: Timeout waiting for health endpoint after 30s
  at HealthCheckTests.swift:142

testSettingsE2E FAILED
  Error: Element not found: settingsButton
  at SettingsTests.swift:87
```

**Artifacts available:**
- `ios-test-results` (2.4 MB) - Test result bundle with screenshots
- `test-logs` (156 KB) - Detailed test logs

**Download artifacts:**
```bash
# Download all artifacts from this run:
gh run download 19727163744

# Download specific artifact:
gh run download 19727163744 -n ios-test-results

# Or view/download from web:
# https://github.com/{owner}/{repo}/actions/runs/19727163744
```

**Retrieve full logs:**
```bash
gh run view 19727163744 --log-failed
# OR specific job:
gh run view 19727163744 --job 56520688201 --log
```

**Search suggestions:**
```bash
# Find all errors:
gh run view 19727163744 --log | grep -i error

# Find test failures:
gh run view 19727163744 --log | grep -E "(FAILED|failed|✗)"

# Find specific test:
gh run view 19727163744 --log | grep "testHealthCheckE2E"
```

### 2. workstation-lint (failed after 35s)
**Workflow:** `.github/workflows/workstation-ci.yml:12`

**Errors found:**
```
error: unused import in src/simulator.rs
  --> src/simulator.rs:5:5
   |
 5 | use std::collections::HashMap;
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^

warning: variable does not need to be mutable
  --> src/main.rs:42:9
```

**Artifacts available:**
None

**Retrieve full logs:**
```bash
gh run view 19727163743 --log-failed
```

**Search suggestions:**
```bash
# Find linting errors:
gh run view 19727163743 --log | grep -E "(error|warning)"

# Find formatting issues:
gh run view 19727163743 --log | grep "Diff in"
```

---

**Summary:** 2 failures, 7 passing
**All results:** https://github.com/{owner}/{repo}/pull/{number}/checks
```

## Finding Workflow File Locations

**Method 1: Via gh API**
```bash
gh api repos/{owner}/{repo}/actions/workflows \
  --jq '.workflows[] | {name: .name, path: .path}'
```

**Method 2: Local search**
```bash
find .github/workflows -name "*.yml" -o -name "*.yaml"
```

**Method 3: From run metadata**
```bash
gh run view $RUN_ID --json workflowName,workflowDatabaseId
# Then map to file using gh api
```

## Common Log Search Patterns

### For Test Failures
```bash
grep -E "(FAILED|✗|Error:|Exception)"
grep -B 5 -A 10 "test.*failed"  # Context around failures
grep "exit code [1-9]"           # Non-zero exits
```

### For Build Failures
```bash
grep -i "error:"
grep "fatal:"
grep "npm ERR!"
grep "cargo.*error"
```

### For Lint Failures
```bash
grep "warning:"
grep "Diff in"
grep "expected.*found"
```

## Example Implementation

```bash
#!/bin/bash
# Run in subagent

PR_NUM=$1
PR_COMMIT=$(gh pr view $PR_NUM --json headRefOid -q '.headRefOid')

# Get all runs for this commit
RUNS=$(gh run list --commit $PR_COMMIT --json databaseId,conclusion,name)

# For each run, get job details
echo "$RUNS" | jq -r '.[] | .databaseId' | while read RUN_ID; do
  gh run view $RUN_ID --json jobs --jq '.jobs[] | {
    name: .name,
    conclusion: .conclusion,
    url: .html_url
  }'
done

# Format and return (pseudo-code)
# - Group by passing/failing
# - Add gh commands for each
# - Add grep suggestions based on job type
```

## Common Mistakes

**Loading full logs into context**
- **Problem:** Full logs can be 100k+ tokens
- **Fix:** Extract only pertinent errors/failures, provide commands for full logs

**Not extracting actual error messages**
- **Problem:** User gets "test failed" without knowing what failed or why
- **Fix:** Extract specific test names, error messages, and context from logs

**Extracting too much log content**
- **Problem:** Including full stack traces or debug output bloats the response
- **Fix:** First few lines of errors only, not full traces

**Not providing grep patterns**
- **Problem:** User has to figure out how to search full logs
- **Fix:** Include job-type-specific grep examples

**Checking runs without commit correlation**
- **Problem:** May return results for old commits
- **Fix:** Always use `--commit $SHA` flag

## Quick Reference

| Task | Command |
|------|---------|
| List runs for commit | `gh run list --commit $SHA` |
| Get run details | `gh run view $RUN_ID --json jobs` |
| Get failed logs only | `gh run view $RUN_ID --log-failed` |
| Get specific job log | `gh run view $RUN_ID --job $JOB_ID --log` |
| List artifacts | `gh run view $RUN_ID --json artifacts` |
| Download all artifacts | `gh run download $RUN_ID` |
| Download specific artifact | `gh run download $RUN_ID -n $ARTIFACT_NAME` |
| List workflows | `gh api repos/{owner}/{repo}/actions/workflows` |

## Use Subagents

**CRITICAL:** Always run in subagent.

```
Use Task tool with subagent_type='general-purpose'.
Give them this skill and the PR number.
They return job summaries + commands.
```

**Why:** Prevents loading massive logs into main context. Main agent gets actionable commands instead.
