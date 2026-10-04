---
name: hotfix
description: Emergency hotfix workflow for production issues
argument-hint: "<issue-description>"
---

# Emergency Hotfix

Rapid response workflow for critical production issues.

**PRIORITY: Fix the issue with minimal changes. Speed matters. Use parallel agents aggressively.**

## Arguments

- `$ARGUMENTS` - Description of the production issue

## Phase 0: Triage

### 0.1 Understand Severity

Ask if not clear:
- Is this blocking users?
- Is data being corrupted?
- Is there a security vulnerability?
- What's the blast radius?

### 0.2 Gather Context (Parallel)

Launch **three agents in parallel** to gather all context simultaneously:

**Agent A: Fetch and inspect git state**
```
git fetch origin
git log origin/main --oneline -10
git diff origin/main..HEAD --stat
```

**Agent B: Check recent deploys**
```
gh run list --limit 5
```
Report which workflows ran, their status, and when they completed.

**Agent C: Check recent CI failures**
```
gh run list --status failure --limit 5
```
Report any recent failures and whether they relate to the reported issue.

Wait for all three agents to complete. Synthesize their findings before proceeding.

## Phase 1: Create Hotfix Branch

```bash
git checkout main
git pull origin main
git checkout -b hotfix/$(date +%Y%m%d)-brief-description
```

## Phase 2: Reproduce and Diagnose (Parallel)

Launch **two agents in parallel** to reproduce and search for root cause simultaneously:

**Agent A: Reproduce locally**
- Replicate the exact conditions described in `$ARGUMENTS`
- Capture error logs and stack traces
- Identify the failing code path
- Write findings to a temporary summary

**Agent B: Search for root cause**
- Check recent commits that could have caused this:
  ```
  git log --oneline -20 -- path/to/affected/code
  ```
- Read the stack trace and trace back through call sites
- Identify candidate commits with `git log --all --oneline --since='3 days ago'`
- Use `git diff` on suspect commits to find the breaking change
- Write findings to a temporary summary

Wait for both agents. Combine their findings to confirm the root cause and identify the minimal fix.

## Phase 3: Fix, Test, and Review (Parallel After Fix)

### 3.1 Implement Fix

**RULES:**
- Smallest possible change
- No refactoring
- No "while we're here" improvements
- Just fix the bug

### 3.2 Add Regression Test

Write ONE test that:
- Reproduces the exact bug
- Verifies the fix works
- Prevents regression

### 3.3 Verify and Review (Parallel)

After the fix and regression test are written, launch **two agents in parallel**:

**Agent A: Run full test suite**
- Run all tests locally
- Report pass/fail status for every suite
- If any test fails, report the failure details (there are no "pre-existing" failures; all must pass)

**Agent B: Review the fix** (`reviewer`)
- Use **reviewer** for focused review of the fix:
  - Is the fix correct?
  - Could it cause other issues?
  - Is it the minimal change needed?
- Report any critical issues found (skip suggestions, this is a hotfix)

Wait for both agents. If either agent found issues:
- Fix test failures
- Fix critical review findings
- Re-run both agents in parallel again until both pass clean

## Phase 4: Commit and Ship

### 4.1 Commit

Delegate to the `skills:commit` command:

```
Skill(skill="skills:commit", args="fix(<scope>): <brief description>")
```

### 4.2 Open the PR

Delegate to the `skills:pr` command with a `fix(<scope>)` title:

```
Skill(skill="skills:pr", args="fix(<scope>): <description>")
```

The `skills:pr` command will push the branch and open the PR. After it returns, update the PR body with hotfix-specific context (issue / root cause / fix / rollback) using `gh pr edit`:

```bash
gh pr edit <pr-number> --body-file - <<'EOF'
## Emergency Hotfix

### Issue
[What was broken in production]

### Root Cause
[Why it broke]

### Fix
[What this PR changes]

### Testing
- [x] Regression test added
- [x] All tests pass
- [x] Minimal change verified

### Rollback Plan
[How to rollback if needed]
EOF
```

## Phase 5: Deployment Checklist

Provide deployment instructions:

```markdown
## Deployment Steps

1. [ ] PR approved
2. [ ] Merge to main
3. [ ] Monitor CI/CD pipeline
4. [ ] Verify deployment successful
5. [ ] Monitor for 15 minutes post-deploy
6. [ ] Confirm issue resolved in production

## Rollback Command
[Specific rollback instructions]

## Post-Mortem
Schedule follow-up to:
- [ ] Investigate root cause fully
- [ ] Add more comprehensive fix if needed
- [ ] Update monitoring/alerting
```

## Test Failure Policy

**IMPORTANT:** There is no such thing as a "pre-existing" test failure. If any test fails - whether it appears related to the hotfix or not - you must fix it. The task always completes with completely passing tests.

## Completion Criteria

- [ ] Issue reproduced and understood
- [ ] Minimal fix implemented
- [ ] Regression test added
- [ ] ALL tests pass (no exceptions for "pre-existing" failures)
- [ ] PR created with context
- [ ] Deployment instructions provided
