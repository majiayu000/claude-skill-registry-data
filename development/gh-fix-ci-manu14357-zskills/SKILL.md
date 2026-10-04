---
name: gh-fix-ci
description: Inspect failing GitHub Actions checks on PRs, fetch detailed logs, summarize failures, create a fix plan, and implement fixes after user approval. For external CI systems, report details only.
compatibility:
  use-case: CI/CD debugging, GitHub Actions troubleshooting, workflow fixes
  frameworks: GitHub CLI, GitHub Actions, CI/CD
---

# GitHub PR Checks Fix

## Use This Skill When

- GitHub Actions checks failing on your PR
- Need to understand why CI/CD workflow failed
- Want actionable fix plan for failing tests/builds
- Debugging workflow configuration issues
- Fixing flaky tests or environment problems
- Non-GitHub Actions checks: report details URL only (out of scope)

## When NOT to Use

- External CI systems (Buildkite, CircleCI, Travis)
- Complex approval workflows requiring multiple stakeholders
- Workflow failures in protected branches (needs admin)
- Local debugging (local testing more efficient)

## Context: CI Debugging Maturity

**Undeveloped**: Click through GitHub UI, read raw logs, guess at fixes.

**Target**: Fetch logs via CLI, summarize failure, draft plan, implement after approval.

**Optimized**: Predict root causes, suggest preventive measures, auto-retry flaky tests, integrated remediation.

## Core Principle

**Failed CI should be actionable.** Fetch logs programmatically, surface the actual failure context (not noise), create a concrete plan, and let the developer decide how to fix.

## Instructions

### Step 1: Verify gh CLI Authentication

**Check auth status:**
```bash
gh auth status
```

**If not authenticated:**
```bash
gh auth login
# Select GitHub.com, HTTPS or SSH
# Authorize with scopes: repo, workflow
```

**Verify elevated permissions:**
```bash
gh auth refresh --scopes repo,workflow
```

### Step 2: Resolve the PR

**Find current branch's PR:**
```bash
gh pr view --json number,url,title
```

**Or specify PR explicitly:**
```bash
gh pr view 123  # PR number
# or
gh pr view https://github.com/owner/repo/pull/123  # Full URL
```

### Step 3: Inspect Failing Checks

**List all checks on PR:**
```bash
gh pr checks [PR] --json name,state,conclusion,url,detailsUrl
```

**Filter for failures:**
```bash
gh pr checks [PR] --json name,state,conclusion,url,detailsUrl | \
  jq '.[] | select(.conclusion == "FAILURE" or .state == "FAILURE")'
```

### Step 4: Fetch Detailed Failure Logs

**For GitHub Actions failures:**

```bash
# Get run details
gh run view [RUN_ID] --json name,workflowName,conclusion,status,url,event,headBranch

# Fetch full logs
gh run view [RUN_ID] --log > failure_logs.txt

# Or fetch specific job logs
gh api "/repos/OWNER/REPO/actions/jobs/JOB_ID/logs" > job_logs.txt
```

**For non-GitHub Actions (external):**
```
❌ External CI detected: [System Name]
📋 Details URL: [Link]
⏭️ Out of scope for this skill
👉 Visit the link above to debug manually
```

### Step 5: Summarize Failure Context

**Extract key failure snippet:**

```markdown
## Failed Check Summary

**Check Name**: tests-ubuntu
**Status**: ❌ FAILURE
**Run ID**: [RUN_ID]
**URL**: [GitHub Actions Run URL]

### Error Context

**Last 30 lines of output:**
```
[STDERR snippet from logs showing actual failure]
```

**Likely Root Cause**: 
- Test assertion failed: `expect(result).toBe(true)`
- Expected: true
- Received: false

**Context**:
- Test file: `src/utils.test.ts`
- Test name: "parseConfig returns valid structure"
- Failure appears consistent (not flaky)

**Next Steps**: Needs investigation of config parsing logic
```

### Step 6: Create Fix Plan

**Use plan skill to draft:**

```markdown
# Plan: Fix Test Failure in tests-ubuntu

We need to debug why `parseConfig()` is returning false instead of true.

## Scope

**In:**
- Review parseConfig logic in src/utils.ts
- Check test expectations in src/utils.test.ts
- Verify mock data/fixtures

**Out:**
- Refactoring entire config system
- Upgrading testing framework

## Action Items

- [ ] Run test locally: `npm test -- src/utils.test.ts`
- [ ] Add console.log to see actual parseConfig output
- [ ] Compare expected vs. actual config structure
- [ ] Fix parseConfig or update test expectations
- [ ] Verify test passes locally
- [ ] Push changes and verify CI passes

## Open Questions

- Is the test expectation correct?
- Did a recent code change break parseConfig?
```

### Step 7: Implement After User Approval

**After user approves plan:**

1. **Make code changes**
   ```bash
   # Edit files based on plan
   code src/utils.ts  # Fix the logic
   code src/utils.test.ts  # Or update test expectations
   ```

2. **Test locally**
   ```bash
   npm test -- src/utils.test.ts
   # Or the specific test
   npm test -- src/utils.test.ts -t "parseConfig returns valid"
   ```

3. **Commit changes**
   ```bash
   git add src/
   git commit -m "Fix parseConfig test failure — ensure config validation works correctly"
   git push
   ```

4. **Verify CI recheck**
   ```bash
   # GitHub Actions auto-triggers on push
   # Or manually re-run:
   gh run rerun [RUN_ID]
   
   # Monitor status
   gh pr checks [PR]
   ```

### Step 8: Re-check Status

**After changes, verify fixes:**
```bash
gh pr checks [PR] --json state,conclusion
```

**If still failing:**
- Fetch new logs
- Repeat analysis
- Consider flaky test vs. actual issue

**If passing:**
```bash
✅ All checks passing!
Ready to merge or request review.
```

## Common Failure Patterns

| Pattern | Indicator | Fix |
|---------|-----------|-----|
| **Timeout** | "execution timeout after 300s" | Increase timeout or optimize code |
| **Missing dep** | "Cannot find module 'x'" | Add missing package or import |
| **Flaky test** | "Intermittent failures" | Add retry, improve timing, mock randomness |
| **Env var missing** | "process.env.API_KEY undefined" | Add secret to Actions workflow |
| **Type error** | "Property 'x' does not exist on type 'y'" | Fix TypeScript type annotations |
| **Permission denied** | "Access denied to /path" | Fix file permissions or paths |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Can't fetch logs** | Verify gh auth with `gh auth refresh --scopes repo,workflow` |
| **Run ID not found** | Use `gh pr checks [PR]` to get correct run ID |
| **External CI system** | Report details URL only; out of scope |
| **Still can't debug** | Try running test locally first to narrow scope |

## Output

**Deliver:**

1. **Failure Summary** with logs excerpt
2. **Likely Root Cause** (educated guess from logs)
3. **Fix Plan** (using plan skill)
4. **After approval: Applied changes** with commit link
5. **Re-check results** (passing or still failing)