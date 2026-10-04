---
name: pr-fix
description: Fix failing CI checks on a pull request
argument-hint: <url> [comments=true|false] [checks=true|false]
---

# Fix Failing PR Checks

Fix failing CI checks on a GitHub pull request, iterating until all checks pass. Uses parallel agents extensively to analyze failures and apply fixes simultaneously.

## Arguments

- `$ARGUMENTS` - PR URL or number (e.g., `https://github.com/owner/repo/pull/123` or `123`)
- `checks` (optional) - Whether to analyze and fix failing checks (default: true)
- `comments` (optional) - Whether to address comments in the PR (default: false)

## Parsing Arguments

Extract from `$ARGUMENTS`:
- **PR reference** — the URL or number (first positional value)
- **checks** — `checks=true` or `checks=false` (default: `true`)
- **comments** — `comments=true` or `comments=false` (default: `false`)

Example: `/pr-fix https://github.com/owner/repo/pull/123 comments=true checks=false`

## Workflow

### 1. Checkout the PR

```bash
gh pr checkout <pr-ref>
```

When checks=true and `gh pr checks <pr-ref>` lists pending checks, follow **Wait for CI** before step 2. If it lists no checks, follow it only when `git ls-files .github/workflows` prints a workflow file, and otherwise handle the PR as on exit 3.

#### Wait for CI

```bash
if [ -z "${PR_URL:-}" ] || [ -z "${REPO:-}" ]; then echo 'set PR_URL and REPO first'; exit 2; fi
HEAD_SHA=$(git -C "$REPO" rev-parse HEAD) || exit 2
PREVIOUS_COUNT=0
for _ in $(seq 1 30); do
  PR_HEAD=$(gh pr view "$PR_URL" --json headRefOid --jq .headRefOid)
  CHECK_COUNT=0
  if [ "$PR_HEAD" = "$HEAD_SHA" ]; then
    CHECK_COUNT=$(gh pr checks "$PR_URL" --json name --jq length 2>/dev/null || echo 0)
  fi
  if [ "$CHECK_COUNT" -gt 0 ] && [ "$CHECK_COUNT" = "$PREVIOUS_COUNT" ]; then break; fi
  PREVIOUS_COUNT=$CHECK_COUNT
  sleep 10
done
if [ "$CHECK_COUNT" -gt 0 ]; then
  exec gh pr checks "$PR_URL" --watch --fail-fast --interval 30
fi
if [ "$PR_HEAD" != "$HEAD_SHA" ]; then
  echo "PR head ${PR_HEAD:-unknown} never matched local HEAD $HEAD_SHA"
  exit 4
fi
echo "No CI checks registered for $HEAD_SHA after 5 minutes"
exit 3
```

Run the block in one Bash call with `run_in_background: true`, with the PR URL and the checkout's absolute path assigned on the line before it, for example `PR_URL=https://github.com/owner/repo/pull/123 REPO=/Users/me/Local/repo`. Both values are required because the Bash tool keeps no variables between calls and a subagent's cwd resets. `REPO` is the absolute path of the checkout from step 1; when the PR reference is a number, `gh pr view <pr-ref> --json url -q .url` prints the URL.

Exit codes: 0 means all checks passed; 1 means a check failed (`--fail-fast`) or `gh` failed during the watch; 3 means no checks registered within 5 minutes (the repo may have no CI); 4 means the PR head never matched the local HEAD: push, or fix the `gh pr view` error it printed, and run again; any other non-zero means the block could not start (unset `PR_URL` or `REPO`, or a path that is not a checkout): fix it and run again. Monitor is the alternative when per-check events are wanted.

On exit 3, skip step 3. With comments=false, report that the PR has no CI checks and stop.

### 2. Gather PR Context (Parallel)

Launch these agents in parallel to collect all PR information simultaneously:

**Agent 1 — PR Details:**
```bash
gh pr view <pr-ref> --json number,headRefName,baseRefName,statusCheckRollup,url,title,body
```

**Agent 2 — Check Status:**
```bash
gh pr checks <pr-ref>
```

**Agent 3 — PR Diff:**
```bash
gh pr diff <pr-ref>
```

**Agent 4 — Review Comments (when comments=true):**
```bash
gh pr view <pr-ref> --json reviews,comments
gh api repos/{owner}/{repo}/pulls/{number}/comments
```

### 3. Fix Failing Checks (when checks=true)

#### 3a. Parallel Failure Analysis

For each failing check, launch a separate analysis agent in parallel:

**Agent per failing check:**
```bash
gh run view <run-id> --log-failed
```

Each agent:
1. Downloads and reads the failure logs for its check
2. Identifies the root cause
3. Determines which files need changes
4. Outputs a structured diagnosis: `{check_name, root_cause, files_to_change, proposed_fix}`

#### 3b. Parallel Fixes (Consolidation Pattern)

Partition diagnosed failures into groups by root cause. Use the **consolidation pattern** — launch each fix group as a parallel agent in its own worktree. Agents can freely edit overlapping files; the consolidator handles merges.

Before launching them, record BASE: the SHA `git rev-parse HEAD` prints in the checkout from step 1 (the PR head). Give each group's `architect` agent that checkout's absolute path as the repo, BASE, its own branch and an absolute worktree path (explicit worktree mode: the architect follows its Worktree BASE protocol). Prompt the consolidator with that checkout as the integration worktree, BASE, and merge as the integration mode.

**Per worktree agent:**
1. Apply the proposed fix from the analysis
2. Verify the fix makes sense in context (read surrounding code)
3. Make minimal, focused changes
4. Commit before finishing

**After all worktree agents complete**, launch the **consolidator** agent (`subagent_type: "consolidator"`) to merge all branches. Then launch a **verifier** agent (`subagent_type: "verifier"`) to confirm tests pass.

#### 3c. Commit and Push

After all fix agents complete, delegate to the `skills:commit` command with a descriptive message, then push:

```
Skill(skill="skills:commit", args="fix(<scope>): <description of what was fixed>")
```

```bash
git push
```

#### 3d. Monitor Checks

Follow **Wait for CI** (step 1) for the pushed commit. If checks still fail, repeat from 3a. Escalate to the user only if the same failure persists after a fix attempt.

### 4. Address PR Comments (when comments=true)

#### 4a. Parallel Comment Analysis

Group review comments by file. Launch a separate agent per file (or per independent comment group) in parallel:

**Agent per file/group:**
1. Read the referenced code and the reviewer's feedback
2. Determine what change is needed
3. Output a structured plan: `{file, line, comment_summary, proposed_change}`

#### 4b. Parallel Comment Fixes (Consolidation Pattern)

Launch each comment group as a parallel agent in its own worktree. Agents can freely edit overlapping files; the consolidator handles merges.

Before launching them, record BASE: the SHA `git rev-parse HEAD` prints in the checkout from step 1 (the PR head). Give each group's `architect` agent that checkout's absolute path as the repo, BASE, its own branch and an absolute worktree path (explicit worktree mode: the architect follows its Worktree BASE protocol). Prompt the consolidator with that checkout as the integration worktree, BASE, and merge as the integration mode.

**Per worktree agent:**
1. Apply the requested change (or closest reasonable interpretation)
2. Respect the reviewer's intent — don't make superficial changes
3. Verify the fix is consistent with surrounding code
4. Commit before finishing

**After all worktree agents complete**, launch the **consolidator** agent (`subagent_type: "consolidator"`) to merge all branches. Then launch a **verifier** agent (`subagent_type: "verifier"`) to confirm tests pass.

#### 4c. Commit and Push

Delegate to the `skills:commit` command, then push:

```
Skill(skill="skills:commit", args="fix(<scope>): address review comments")
```

```bash
git push
```

#### 4d. Monitor Checks

Follow **Wait for CI** (step 1) for the pushed commit. If fixing comments introduces new check failures, loop back to step 3.

### 5. Iterate If Needed

Continue iterating until:
- All enabled checks pass
- All comments are addressed (if comments=true)
- Or the same failure persists after a fix attempt (escalate to user)

## Important Notes

- Read failure logs carefully — the error message usually contains the fix
- Common check failures:
  - **tests**: Check test output, fix code or test
  - **build**: Check compilation errors
- When addressing comments, respect the reviewer's intent — don't just make superficial changes
- After each fix, commit with: `fix(<scope>): <description of what was fixed>`

## Test Failure Policy

**IMPORTANT:** There is no such thing as a "pre-existing" test failure. If any test fails - whether it appears related to the PR changes or not - you must fix it. The task always completes with completely passing tests. Do not dismiss failures as "unrelated to this PR."

## Exit Conditions

Stop iterating when:
- All checks pass (required - no exceptions)
- The same failure persists after a fix attempt (escalate to user)
