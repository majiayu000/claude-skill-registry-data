---
name: ci-fix-loop
description: Autonomous CI fix loop with background monitoring and retry logic. Runs up to 10 fix-commit-push-wait cycles until CI passes or max retries reached.
---

# CI Fix Loop Skill

Orchestrates autonomous CI repair: analyze → fix → commit → push → monitor → repeat until success.

## When to Use

This skill is invoked when:
- User runs `/fix-ci --loop` or `/fix-ci --auto`
- Multiple CI fix iterations are needed
- User wants hands-off CI repair

## Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| max_attempts | 10 | Maximum fix iterations |
| poll_interval | 60 | Seconds between CI status checks |
| ci_start_timeout | 120 | Seconds to wait for CI run to start |
| ci_run_timeout | 1800 | Max seconds to wait for CI completion (30 min) |

## Workflow

### Phase 1: Initialize

Get context and validate:

```bash
BRANCH=$(git branch --show-current)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown")
```

**Safety checks:**

1. Block on protected branches:
```bash
if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "Cannot run autonomous fixes on $BRANCH"
  echo "Create a feature branch: git checkout -b fix/ci-errors"
  # STOP - do not proceed
fi
```

2. Handle uncommitted changes:
```bash
if [[ -n $(git status --porcelain) ]]; then
  echo "Stashing uncommitted changes..."
  git stash push -m "pre-ci-fix-loop-$(date +%Y%m%d_%H%M%S)"
fi
```

Initialize state:
```
attempt = 1
max_attempts = 10
last_errors = []
history = []
started_at = now
```

### Phase 2: Fix Loop

For each attempt from 1 to 10:

#### Step 2.1: Display Progress

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CI Fix Loop - Attempt ${attempt}/${max_attempts}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Branch: ${branch}
Repository: ${repo}
```

#### Step 2.2: Fetch CI Logs

Get most recent failed run:
```bash
RUN_ID=$(gh run list --branch "$BRANCH" --limit 5 --json databaseId,conclusion \
  --jq '[.[] | select(.conclusion == "failure")][0].databaseId')

if [ -z "$RUN_ID" ]; then
  echo "No failed runs found - checking if CI is passing..."
  # May already be fixed, verify
fi
```

Fetch logs for failed jobs:
```bash
FAILED_JOBS=$(gh run view $RUN_ID --json jobs --jq '.jobs[] | select(.conclusion == "failure") | .databaseId')

for JOB_ID in $FAILED_JOBS; do
  gh api repos/${REPO}/actions/jobs/${JOB_ID}/logs > /tmp/ci-logs-${JOB_ID}.txt 2>/dev/null || true
done
```

#### Step 2.3: Analyze Errors

Invoke the `ci-log-analyzer` agent:
- Parse CI logs from /tmp/ci-logs-*.txt
- Extract structured error list with type, file, line, message
- Returns JSON with errors categorized by type (lint/test/type/build)

#### Step 2.4: Check for Progress

Compare current errors with previous attempt:

```
if current_errors == last_errors AND attempt > 1:
  # Same errors after fix attempt = likely unfixable
  consecutive_same_errors += 1

  if consecutive_same_errors >= 2:
    echo "Same errors detected after 2 fix attempts - aborting"
    echo "These errors may require manual intervention"
    # STOP - exit loop with failure report
fi

if current_errors is empty:
  # No errors found - CI might be passing
  # Skip to monitoring phase
```

#### Step 2.5: Apply Fixes

Invoke the `ci-error-fixer` agent with error list:
- Applies targeted fixes based on error type
- Shows diffs for each change
- Reports fixed vs flagged-for-manual-review counts

Track results:
```
errors_fixed = count of successfully fixed errors
errors_flagged = count of errors needing manual review
```

#### Step 2.6: Commit & Push

Stage and commit changes:
```bash
git add .

# Create descriptive commit message
git commit -m "fix(ci): automated fix attempt ${attempt}

Errors addressed:
- ${error_summary_list}

Attempt ${attempt} of ${max_attempts} (ci-fix-loop)"
```

Push to trigger CI:
```bash
PUSH_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
git push origin ${BRANCH}
```

#### Step 2.7: Wait for CI Run to Start

Poll until new run appears (max 2 minutes):
```bash
TIMEOUT=120
START=$(date +%s)

while true; do
  RUN_JSON=$(gh run list --branch "$BRANCH" --limit 1 --json databaseId,status,createdAt)
  CREATED=$(echo "$RUN_JSON" | jq -r '.[0].createdAt')

  # Check if this run was created after our push
  if [[ "$CREATED" > "$PUSH_TIME" ]]; then
    NEW_RUN_ID=$(echo "$RUN_JSON" | jq -r '.[0].databaseId')
    echo "CI run started: $NEW_RUN_ID"
    break
  fi

  ELAPSED=$(($(date +%s) - START))
  if [ $ELAPSED -gt $TIMEOUT ]; then
    echo "Warning: No CI run started after ${TIMEOUT}s"
    echo "Check if workflows are enabled for this branch"
    break
  fi

  sleep 5
done
```

#### Step 2.8: Monitor CI (Background)

Spawn the `ci-monitor` agent with `run_in_background: true`:

The monitor will:
- Poll `gh run list` every 60 seconds
- Return when CI reaches terminal state
- Output: `SUCCESS|RUN_ID`, `FAILURE|RUN_ID`, `CANCELLED|RUN_ID`, or `TIMEOUT|RUN_ID`

Wait for monitor result using `TaskOutput` tool.

#### Step 2.9: Handle Result

Parse monitor output:
```
case "$RESULT" in
  SUCCESS*)
    # CI passed! Exit loop with success
    ;;
  FAILURE*)
    # CI still failing - continue to next attempt
    ;;
  CANCELLED*)
    # Run was cancelled - warn and exit
    echo "CI run was cancelled externally"
    # EXIT with warning
    ;;
  TIMEOUT*)
    # Exceeded 30 min wait
    echo "CI run timed out after 30 minutes"
    # Ask if should continue waiting or abort
    ;;
esac
```

#### Step 2.10: Record History

```
history.append({
  attempt: attempt,
  errors_found: len(current_errors),
  errors_fixed: errors_fixed,
  errors_flagged: errors_flagged,
  run_id: run_id,
  result: conclusion,
  duration: attempt_duration
})

last_errors = current_errors
attempt += 1
```

### Phase 3: Final Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CI Fix Loop Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Result: [SUCCESS|FAILURE] after ${attempts} attempt(s)

Summary:
  Total time: ${total_duration}
  Commits created: ${commit_count}
  Errors fixed: ${total_errors_fixed}

History:
```

For each entry in history:
```
  Attempt ${n}: Found ${errors_found} errors, fixed ${fixed} → ${result}
```

If FAILURE:
```
Remaining Issues (require manual intervention):
  - ${file}:${line} - ${message}
    Type: ${type}

Suggested next steps:
  1. Review errors above
  2. Check CI logs: gh run view ${last_run_id} --log-failed
  3. Fix manually and push
```

If SUCCESS:
```
CI is now passing!

Next steps:
  1. Review automated commits: git log --oneline -${commit_count}
  2. Squash if desired: git rebase -i HEAD~${commit_count}
  3. Create PR: /github:create-pr
```

## Error Handling

### Network/API Failures
- Retry `gh` commands 3 times with 5s backoff
- If persistent, abort and report

### Git Conflicts
- If push fails due to upstream changes:
```
echo "Upstream changes detected"
echo "Pull and retry: git pull --rebase && /fix-ci --loop"
```
- Abort loop

### Unfixable Errors
- Track errors persisting across 2+ attempts
- Mark as "unfixable" in final report
- Continue attempting other errors

### Timeout
- CI run timeout (30 min): report and suggest `gh run watch`
- CI start timeout (2 min): check workflow configuration

## Safety Mechanisms

1. **Branch protection**: Never run on main/master
2. **Max attempts**: Hard limit of 10 iterations
3. **Stash protection**: Uncommitted changes are preserved
4. **Progress detection**: Abort if same errors repeat twice
5. **Timeout limits**: 30 min max CI wait per attempt
6. **Commit tracking**: Report all commits for easy revert

## Token Efficiency

Estimated per iteration:
- Analysis (sonnet): ~2000 tokens
- Fix application (sonnet): ~3000 tokens
- CI monitoring (haiku): ~500 tokens
- State/reporting: ~500 tokens
- **Total: ~6000 tokens/iteration**
- **10 iterations max: ~60,000 tokens**

Key optimizations:
- Haiku model for CI polling (10x cheaper than sonnet)
- No context accumulation between iterations
- Minimal state tracking
- Background execution frees terminal
