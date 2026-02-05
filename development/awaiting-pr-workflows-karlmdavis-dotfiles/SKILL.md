---
name: awaiting-pr-workflows
description: Use when needing to check PR workflow status, especially under time pressure or after pushing commits - ensures verification of unpushed changes, commit correlation, and patient waiting for workflows to complete (up to 20 minutes)
---

# Awaiting PR Workflows

## Overview

Wait for GitHub PR workflows to complete while correctly handling unpushed changes, commit correlation, and timing issues.

**Core principle:** Always verify local state before checking remote workflows. Under pressure, agents skip critical checks.

## When to Use

Use this skill when you need to:
- Check if PR workflows have finished
- Verify CI status for recent changes
- Wait for workflows to complete before proceeding
- Handle requests like "are the tests passing?" or "wait for CI"

**When NOT to use:**
- PR doesn't exist and user hasn't asked to create one
- Just viewing PR status without concern for latest commits

## Critical Checks (Always Perform These FIRST)

### 1. Check for Unpushed Local Changes

**BEFORE** checking workflow status, verify local/remote sync:

```bash
# Check if local branch has unpushed commits
git status
```

**If unpushed commits exist:**
```
Your branch is ahead of 'origin/branch-name' by N commits
```

**Then ask user:**
```
I found N unpushed commits on your local branch.
The PR workflows won't include these changes yet.

Would you like me to push them now? (y/n)
```

**Never skip this check, even under time pressure.**

### 2. Verify PR Exists

```bash
# Get current branch name
BRANCH=$(git branch --show-current)

# Search for PR by branch
gh pr list --head "$BRANCH" --json number,title
```

**If no PR found, ask user:**
```
No PR found for branch '$BRANCH'.

Would you like me to create one? (y/n)
```

### 3. Verify Commit Correlation

**Always check which commits the workflows are testing:**

```bash
# Get PR head commit
PR_COMMIT=$(gh pr view "$PR_NUMBER" --json headRefOid -q '.headRefOid')

# Get local HEAD commit
LOCAL_COMMIT=$(git rev-parse HEAD)

# Compare (show short SHAs for readability)
PR_SHORT=$(echo $PR_COMMIT | cut -c1-7)
LOCAL_SHORT=$(echo $LOCAL_COMMIT | cut -c1-7)
```

**If commits don't match:**
```
⚠️  Commit mismatch detected:
- PR is testing: $PR_SHORT
- Your local HEAD: $LOCAL_SHORT

The workflows are not testing your latest local changes.
[Proceed with step 1 - check for unpushed changes]
```

## Waiting for Workflows

### Step 1: Check if Workflows Have Started

```bash
# List recent workflow runs for the PR's head commit
gh run list --commit $PR_COMMIT --limit 5 --json status,conclusion,createdAt
```

**If no runs found:**

Wait up to 30 seconds (workflows may be queuing):

```bash
for i in {1..6}; do
  sleep 5
  RUNS=$(gh run list --commit $PR_COMMIT --limit 1 --json databaseId -q '.[0].databaseId')
  if [ -n "$RUNS" ]; then
    echo "Workflows started!"
    break
  fi
  echo "Waiting for workflows to start... ($((i*5))s elapsed)"
done
```

**If still no runs after 30s:**
```
⚠️  Workflows haven't started after 30 seconds.

This could mean:
- GitHub Actions is experiencing delays
- Workflows are disabled for this repo
- The commit hasn't triggered workflows

Would you like me to:
1. Wait longer (recommended if GitHub is slow)
2. Check workflow configuration
3. Stop waiting
```

### Step 2: Wait for Workflows to Complete

**First check if already complete, then poll with exponential backoff up to 20 minutes:**

```bash
# Check if workflows are already complete
INCOMPLETE=$(gh run list --commit "$PR_COMMIT" --status in_progress,queued --json databaseId | jq 'length')

if [ "$INCOMPLETE" -eq 0 ]; then
  echo "✅ All workflows already complete!"
else
  # Wait with exponential backoff
  MAX_WAIT=1200  # 20 minutes in seconds
  INTERVAL=5     # Start with 5 seconds
  elapsed=0

  while [ $elapsed -lt $MAX_WAIT ]; do
    INCOMPLETE=$(gh run list --commit "$PR_COMMIT" --status in_progress,queued --json databaseId | jq 'length')

    if [ "$INCOMPLETE" -eq 0 ]; then
      echo "✅ All workflows complete!"
      break
    fi

    echo "⏳ $INCOMPLETE workflow(s) still running... (${elapsed}s elapsed, max ${MAX_WAIT}s)"
    sleep $INTERVAL
    elapsed=$((elapsed + INTERVAL))

    # Exponential backoff: 5s, 10s, 20s, 40s, then cap at 60s
    INTERVAL=$((INTERVAL * 2))
    if [ $INTERVAL -gt 60 ]; then
      INTERVAL=60
    fi
  done

  if [ $elapsed -ge $MAX_WAIT ]; then
    echo "⚠️  Workflows still running after 20 minutes."
    # Report current state and let caller decide what to do
  fi
fi
```

**If timeout reached (20 min):**
```
⚠️  Some workflows are still running after 20 minutes:

[List incomplete workflows with gh run list]

This is unusually long. Caller should decide whether to:
1. Wait longer
2. Proceed with current results
3. Check workflow logs for stuck jobs
```

## Quick Reference

| Step | Command | Purpose |
|------|---------|---------|
| Check local changes | `git status` | Find unpushed commits |
| Find PR | `gh pr list --head $BRANCH` | Verify PR exists |
| Get PR commit | `gh pr view --json headRefOid` | What commit is PR testing |
| Get local commit | `git rev-parse HEAD` | What commit is local HEAD |
| List workflow runs | `gh run list --commit $SHA` | Find runs for specific commit |
| Check run status | `gh run list --json status,conclusion` | See if runs complete |

## Common Mistakes

**Skipping unpushed check under time pressure**
- **Problem:** Reports stale workflow status, user confusion
- **Fix:** ALWAYS check `git status` first, even if "urgent"

**Not correlating commits**
- **Problem:** Report workflows for old commit as if they're current
- **Fix:** Always compare `PR_COMMIT` vs `LOCAL_COMMIT`

**Giving up too early**
- **Problem:** Reports "workflows not started" when they're just queuing
- **Fix:** Wait at least 30s for startup, 20min for completion

**Not asking about push/PR creation**
- **Problem:** Leaves user without next steps
- **Fix:** Always offer to push or create PR when needed

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "They need results ASAP, skip git status" | Takes 1 second. Wrong results waste minutes. |
| "The PR probably has latest commits" | Probably ≠ definitely. Verify with SHAs. |
| "No runs found, must be disabled" | GitHub queues workflows. Wait 30s. |
| "Been 2 minutes, that's long enough" | Workflows take 5-15 min normally. Max is 20. |
| "I'll just check current status quickly" | Quick check = wrong answer if commits don't match. |
| "User wants answer now, not questions" | Wrong answer now < right answer in 2 seconds. |

## Red Flags - STOP and Check

**If you catch yourself thinking:**
- "They need results quickly, I'll skip git status" → NO. Always check.
- "The PR probably has the latest commits" → NO. Verify with commit SHAs.
- "No runs found, workflows must be disabled" → NO. Wait 30s first.
- "It's been 2 minutes, that's long enough" → NO. Max wait is 20 minutes.
- "I'll answer quickly without all the steps" → NO. Fast wrong answer helps nobody.

**These are rationalizations. Follow the process.**

## Use Subagents to Save Context

**IMPORTANT:** This workflow involves waiting (up to 20 minutes) and produces minimal output.

**Run in subagent using Task tool:**
- Subagent does the waiting/polling
- Returns concise summary to main context
- Saves 150k+ tokens vs running in main session

```
Use the Task tool with subagent_type='general-purpose' and give them this skill.
They'll handle the polling and report back results.
```

## Example Workflow

```
User: "Check if CI is passing for my PR"

[Run git status]
→ Found 2 unpushed commits

Me: "I found 2 unpushed commits. The PR workflows won't include
     these yet. Would you like me to push them now?"

User: "Yes"

[Run git push]
[Wait for workflows to start - 15 seconds]
→ Workflows started

[Poll every 30s for completion]
→ 3 minutes elapsed, workflows still running
→ 6 minutes elapsed, workflows complete

Me: "✅ All workflows complete for commit a1b2c3d:
     - Backend tests: PASSED
     - iOS tests: PASSED
     - Lint: PASSED"
```
