---
name: priority-issue-resolution
description: Autonomous issue resolution workflow for processing priority-critical/priority-high issues in TradeStream. Covers claiming, investigation, worktree-based fixes, PR shepherding, and CI monitoring. Activates on "fix issues", "resolve bugs", "claim issue", "priority queue", "issue triage", or "autonomous resolution".
allowed-tools: Bash, Read, Grep, Glob, Task, GitHub, Write, Edit
---

# Priority Issue Resolution Workflow

Autonomous workflow for resolving issues from highest to lowest priority in the TradeStream ecosystem.

## When to Use

- Working through backlog of priority-critical/priority-high issues
- Autonomous issue resolution sessions
- After E2E verification discovers failures
- When cleaning up after feature deployments

## Core Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  PRIORITY ISSUE RESOLUTION LOOP                             │
│                                                             │
│  1. SCAN → Find highest priority unclaimed issue            │
│  2. CLAIM → Post comment with ETA                           │
│  3. INVESTIGATE → Verify relevance, gather context          │
│  4. DECIDE → Close / Add details / Decompose / Fix          │
│  5. FIX → Worktree + PR + Monitor CI + Merge                │
│  6. REPEAT → Return to step 1                               │
│                                                             │
│  STOP when no issues remain                                 │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Scan for Issues

### Priority Scan

```bash
#!/bin/bash
# scan-priority-issues.sh - Find highest priority issues

echo "=== PRIORITY ISSUE SCAN ==="

REPO="tradestreamhq/tradestream"

# Priority-critical first (highest priority)
echo "--- priority-critical ---"
gh issue list --repo $REPO --label priority-critical --state open \
  --json number,title --jq '.[] | "#\(.number): \(.title)"' 2>/dev/null

# Then priority-high
echo "--- priority-high ---"
gh issue list --repo $REPO --label priority-high --state open \
  --json number,title --jq '.[] | "#\(.number): \(.title)"' 2>/dev/null

# Then enhancement
echo "--- enhancement ---"
gh issue list --repo $REPO --label enhancement --state open \
  --json number,title --jq '.[] | "#\(.number): \(.title)"' 2>/dev/null
```

### Priority Order

| Priority         | Label              | Action         |
| ---------------- | ------------------ | -------------- |
| Critical         | `priority-critical`| Fix NOW        |
| High             | `priority-high`    | Fix this cycle |
| Enhancement      | `enhancement`      | Queue or close |

## Step 2: Claim the Issue

### Check Claim Status

Before claiming, verify the issue isn't already claimed:

```bash
# Check for claim tags in recent comments
ISSUE_NUM=1234
REPO="tradestreamhq/tradestream"

LAST_COMMENT=$(gh api repos/$REPO/issues/$ISSUE_NUM/comments \
  --jq '.[(-1)]?.body // ""' 2>/dev/null)

if echo "$LAST_COMMENT" | grep -qE '\[(CLAIMED|AGENT-|ANALYSIS|EDITING)\]'; then
  echo "Issue already claimed - skip"
else
  echo "Issue available - claim it"
fi
```

### Post Claim Comment

```bash
gh issue comment $ISSUE_NUM --repo $REPO --body "[CLAIMED] Claiming this issue. ETA: ~30 minutes.

**Investigation Plan:**
1. Understand the root cause
2. Identify affected files
3. Implement fix with worktree
4. Create PR and monitor CI

Will update with analysis shortly."
```

## Step 3: Investigate

### Investigation Checklist

1. **Read the full issue** - Understand the reported problem
2. **Check for related issues** - May be duplicate or related to other work
3. **Search codebase** - Find relevant files and understand context
4. **Verify reproducibility** - Confirm the issue is real and current

### Investigation Outcomes

| Finding             | Action                           |
| ------------------- | -------------------------------- |
| Issue is irrelevant | Close with explanation           |
| Insufficient detail | Add research findings, keep open |
| Too big             | Decompose into smaller issues    |
| Ready to fix        | Proceed to Step 4                |

### Close Irrelevant Issues

```bash
gh issue close $ISSUE_NUM --repo $REPO --reason "not_planned" \
  --comment "[ANALYSIS] Closing as not relevant.

**Reason:** [Explain why the issue is no longer valid]

Examples:
- Feature already removed
- Duplicate of #XXX
- Working as intended
- Cannot reproduce"
```

### Add Missing Details

```bash
gh issue comment $ISSUE_NUM --repo $REPO --body "[ANALYSIS] Investigation findings:

## Root Cause
[Describe what you found]

## Affected Files
- \`path/to/file1.java\`
- \`path/to/file2.kt\`

## Proposed Fix
[Describe the solution approach]

## Complexity
[Low/Medium/High] - [Time estimate]"
```

### Decompose Large Issues

```bash
# Create sub-issues for complex work
gh issue create --repo $REPO \
  --title "[Sub] Part 1: Implement X" \
  --label "priority-high" \
  --body "Parent issue: #$ISSUE_NUM

## Scope
[Describe this sub-task]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2"

# Update parent issue
gh issue comment $ISSUE_NUM --repo $REPO \
  --body "[DECOMPOSED] Split into smaller issues:
- #XXX - Part 1: Implement X
- #YYY - Part 2: Implement Y"
```

## Step 4: Fix with Worktree

### Create Worktree

```bash
ISSUE_ID=1234
REPO_PATH="/home/pselamy/repositories/direnv/pselamy/tradestream"

# Navigate to repo
cd $REPO_PATH

# Fetch latest and create worktree
git fetch origin
git worktree add -b fix/${ISSUE_ID} \
  /home/pselamy/repositories/worktrees/tradestream-${ISSUE_ID} \
  origin/main

# Work in worktree
cd /home/pselamy/repositories/worktrees/tradestream-${ISSUE_ID}
```

### Make the Fix

1. **Edit files** - Apply the minimal fix
2. **Run tests locally** - Verify the fix works
3. **Check formatting** - Run linters

```bash
# Build and test with Bazel
bazel build //...
bazel test //...

# Format code (if needed)
# Java formatting
bazel run //:format-java

# Kotlin formatting
bazel run //:format-kotlin

# Python formatting
bazel run //:format-python
```

### Create PR

```bash
git add -A
git commit -m "fix: [description] (#$ISSUE_ID)"
git push -u origin fix/${ISSUE_ID}

gh pr create --title "fix: [description] (#$ISSUE_ID)" \
  --body "## Summary
- [Describe the fix]

## Root Cause
- [Explain what was wrong]

## Test plan
- [ ] Bazel tests pass
- [ ] Verified locally

Closes #$ISSUE_ID"
```

## Step 5: Monitor CI and Merge

### CI Monitoring Loop

```bash
PR_NUMBER=1234
REPO="tradestreamhq/tradestream"

while true; do
  STATUS=$(gh pr checks $PR_NUMBER --repo $REPO 2>&1)

  if echo "$STATUS" | grep -q "fail"; then
    echo "CI FAILED - investigating..."
    gh pr checks $PR_NUMBER --repo $REPO 2>&1
    # Fix the failure, commit, push
    break
  elif ! echo "$STATUS" | grep -q "pending"; then
    echo "All checks passed - merging"
    gh pr merge $PR_NUMBER --repo $REPO --merge --delete-branch
    break
  else
    echo "CI still running..."
    sleep 60
  fi
done
```

### Fix CI Failures

Common CI failures and fixes:

| Failure Type | Fix                                    |
| ------------ | -------------------------------------- |
| Bazel Build  | Fix compilation errors                 |
| Bazel Test   | Fix failing tests or update assertions |
| Format       | Run `bazel run //:format-*`            |
| Coverage     | Add missing test coverage              |

```bash
# After fixing, amend and push
git add -A
git commit --amend --no-edit
git push --force-with-lease
```

### Post Victory Comment

```bash
gh issue comment $ISSUE_NUM --repo $REPO \
  --body "[VICTORY] Fixed in PR #$PR_NUMBER (merged).

**Root Cause:** [Brief explanation]

**Fix:** [What was changed]"
```

## Step 6: Cleanup and Repeat

### Cleanup Worktree

```bash
cd /home/pselamy/repositories/direnv/pselamy/tradestream
git worktree remove /home/pselamy/repositories/worktrees/tradestream-${ISSUE_ID}
git branch -d fix/${ISSUE_ID}  # Local branch cleanup
```

### Return to Step 1

Continue scanning for the next highest priority issue until none remain.

## Creating New Issues

When you discover bugs or missing features while working:

1. **DO NOT fix them in the current PR** - Stay focused
2. **Create a new issue** with appropriate priority
3. **Comment in current issue** referencing the new discovery

```bash
# Create new issue for discovered problem
NEW_ISSUE=$(gh issue create --repo $REPO \
  --title "[Discovery] [Brief description]" \
  --label "priority-high,bug" \
  --body "Discovered while fixing #$ISSUE_NUM.

## Problem
[Describe the issue]

## Where Found
\`path/to/file.java:line\`

## Impact
[Severity/Impact]" \
  --json number --jq '.number')

# Comment in current issue
gh issue comment $ISSUE_NUM --repo $REPO \
  --body "[DISCOVERY] Found unrelated issue while investigating.
Created #$NEW_ISSUE to track. Staying focused on current fix."
```

## Quick Reference

### Common Commands

```bash
# Scan all priority-critical issues
gh issue list --repo tradestreamhq/tradestream --label priority-critical --state open

# Check if issue is claimed
gh api repos/tradestreamhq/tradestream/issues/1234/comments \
  --jq '.[(-1)]?.body // ""' | grep -q '\[CLAIMED\]'

# Monitor PR CI
gh pr checks 1234 --repo tradestreamhq/tradestream

# Merge when ready
gh pr merge 1234 --repo tradestreamhq/tradestream --merge --delete-branch

# Close with reason
gh issue close 1234 --repo tradestreamhq/tradestream --reason completed
```

### TradeStream Project Structure

| Directory       | Purpose                          |
| --------------- | -------------------------------- |
| `src/main/java` | Core Java implementation         |
| `services/`     | Microservices                    |
| `charts/`       | Helm deployment charts           |
| `protos/`       | Protocol Buffer definitions      |
| `platforms/`    | Platform configurations          |
| `.github/`      | CI/CD workflows                  |

## Anti-Patterns

| Anti-Pattern           | Problem                          | Prevention                        |
| ---------------------- | -------------------------------- | --------------------------------- |
| Fix without claiming   | Duplicate work with other agents | Always claim first                |
| Scope creep during fix | PR becomes too large             | Create new issues for discoveries |
| Skip CI monitoring     | Failed PRs left unmerged         | Monitor until green and merged    |
| Develop on main        | Messy git history                | Always use worktree               |
| Abandon failing CI     | Stale PRs                        | Fix failures, don't abandon       |

## Related Skills

- `@agent-claim-verification` - Claim checking patterns
- `@worktree-lifecycle` - Full worktree patterns
- `@sre-sniper-pattern` - CI monitoring and shepherding
- `@creating-issues-and-prs` - PR creation conventions

---

## Session Log Template

**Context:** Document workflow progress during issue resolution sessions.

### Issues Resolved This Session

1. **#XXXX** - [Issue title]
   - Root cause: [Brief description]
   - Fix: [What was changed]
   - PR #XXXX merged successfully

### Key Learnings Captured

1. **Always verify claim status** before starting work to avoid duplicating effort
2. **Use worktrees for every fix** - never develop on main
3. **Monitor CI actively** - don't abandon PRs with failing checks
4. **Create issues for discoveries** - stay focused on current fix
5. **Post victory comments** - document root cause for future reference

### Metrics

- Issues scanned: X
- Issues resolved: X (Y fixes, Z investigations)
- PRs created: X (merged)
- Time spent: ~XX minutes
