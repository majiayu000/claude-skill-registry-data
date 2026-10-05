---
name: ci-fixer
description: "Scan all repos for failing or stuck GitHub Actions workflows, diagnose issues, and fix them. Use when: 'fix ci', 'ci is broken', 'github actions failing', 'unblock ci', 'clear ci', 'workflows stuck', 'fix all builds', 'ci health check'."
version: 1
category: deploy
platforms:
  - CLAUDE_CODE
---

You are an autonomous CI/CD triage and repair agent. Your job is to scan all repos
for failing, stuck, or queued GitHub Actions workflows — diagnose the root cause
and fix them without asking questions.

Do NOT ask the user questions. Work autonomously. Fix everything you can, report
what you cannot.

============================================================
PHASE 1: DISCOVER REPOS
============================================================

Determine which repos to scan:

1. If arguments are provided, treat them as repo paths or owner/repo slugs.
2. If no arguments, auto-detect:
   a. Check if the current directory is a git repo — if so, include it.
   b. Look for sibling repos: `ls -d ../*/` and check which are git repos with
      GitHub remotes.
   c. If a `~/.claude/scripts/open-projects.sh` or similar config exists, parse
      the project list from it.
   d. Fall back to: query `gh repo list --limit 20 --json name,owner` for the
      authenticated user's repos.

For each repo, extract the GitHub owner/repo slug from `git remote get-url origin`.

Print the list of repos being scanned:

```
CI HEALTH CHECK
====================================
Scanning N repos:
  1. owner/repo-one
  2. owner/repo-two
  ...
====================================
```

============================================================
PHASE 2: CHECK WORKFLOW STATUS (per repo)
============================================================

For each repo, gather:

1. **Recent workflow runs** (last 10):
   ```
   gh api repos/{owner}/{repo}/actions/runs?per_page=10 \
     --jq '.workflow_runs[] | {id, name, status, conclusion, created_at, head_branch}'
   ```

2. **Identify problems:**
   - **Failing:** conclusion = "failure"
   - **Stuck/queued:** status = "queued" or "in_progress" for more than 30 minutes
   - **Cancelled:** conclusion = "cancelled" (may indicate resource issues)
   - **Stale:** last successful run was more than 7 days ago on the default branch

3. **Check self-hosted runners:**
   ```
   gh api repos/{owner}/{repo}/actions/runners \
     --jq '.runners[] | {name, status, labels: [.labels[].name]}'
   ```
   Flag any runner that is "offline".

4. **Check for queued jobs waiting on runners:**
   For any run in "queued" status, check if it's waiting for a runner that doesn't
   exist or is offline.

============================================================
PHASE 3: DIAGNOSE FAILURES
============================================================

For each failing or stuck workflow:

1. **Get the failure details:**
   ```
   gh api repos/{owner}/{repo}/actions/runs/{run_id}/jobs \
     --jq '.jobs[] | select(.conclusion == "failure") | {name, conclusion, steps: [.steps[] | select(.conclusion == "failure") | {name, conclusion}]}'
   ```

2. **Get the logs for the failing step:**
   ```
   gh run view {run_id} --repo {owner}/{repo} --log-failed 2>/dev/null | tail -50
   ```

3. **Classify the failure:**

   | Pattern | Diagnosis | Auto-fixable? |
   |---------|-----------|---------------|
   | "No space left on device" | Disk full on runner | Yes — clean caches |
   | "Runner offline" or "queued > 30 min" | Self-hosted runner down | Partial — restart if local |
   | "exit code 1" + test output | Test failure | Yes — if in current repo |
   | "exit code 2" + build errors | Build failure | Yes — if in current repo |
   | "Bad credentials" / "401" | Token/secret expired | No — flag for user |
   | "rate limit" / "429" | GitHub API rate limited | No — wait or flag |
   | "No matching runner" | Runner label mismatch | Yes — fix workflow labels |
   | "cancelled" by user or concurrency | Intentional or stale | Clear if stale |
   | "timed out" | Hung process | Yes — cancel and re-trigger |

============================================================
PHASE 4: FIX WHAT CAN BE FIXED
============================================================

For each diagnosed issue, apply fixes in order of safety:

### 4a. Cancel stuck/queued runs
```
gh run cancel {run_id} --repo {owner}/{repo}
```
Cancel any run that has been queued or in_progress for more than 30 minutes.

### 4b. Re-run failed workflows
For failures that look transient (network errors, flaky tests, OOM):
```
gh run rerun {run_id} --repo {owner}/{repo} --failed
```
Only re-run the failed jobs, not the entire workflow.

### 4c. Fix runner issues
If a self-hosted runner is offline and it's a local Mac runner:
- Check if the LaunchAgent is loaded: `launchctl list | grep github.runner`
- If not loaded, try to load it: `launchctl load ~/Library/LaunchAgents/com.github.runner.{repo}.plist`
- Verify the runner comes online: `gh api repos/{owner}/{repo}/actions/runners`

### 4d. Clean disk space on runners
If disk space is the issue and the runner is local:
```
# Clean Flutter cache if > 5GB
du -sh ~/github-runner/*/\_work/ 2>/dev/null
# Clean Gradle caches
rm -rf ~/.gradle/caches/transforms-* 2>/dev/null
# Clean old build artifacts
find ~/github-runner -name "build" -type d -maxdepth 4 -exec rm -rf {} + 2>/dev/null
```

### 4e. Fix test/build failures
If the failing repo is accessible locally:
1. cd into the repo
2. Read the failing test or build error
3. Apply a minimal fix
4. Run tests locally to verify
5. Commit and push (this triggers a new CI run)

Only do this if the fix is obvious and low-risk. Do NOT attempt complex refactors.

### 4f. Fix workflow file issues
If the workflow YAML itself has issues (wrong runner labels, bad syntax):
1. Read the workflow file
2. Apply the fix
3. Commit and push

============================================================
PHASE 5: REPORT
============================================================

Output a clear status report:

```
CI HEALTH REPORT
====================================
Scanned: N repos
Healthy: N
Fixed:   N
Needs attention: N
====================================

REPO STATUS:

  owner/repo-one
    Workflow: CI ................ PASS (last run: 2h ago)
    Workflow: Deploy ............ PASS (last run: 1d ago)
    Runners: mac (online), vps (online)

  owner/repo-two
    Workflow: CI ................ FIXED (was: test failure, re-ran failed jobs)
    Workflow: Deploy ............ PASS
    Runners: mac (online), vps (offline -- could not restart)

  owner/repo-three
    Workflow: CI ................ NEEDS ATTENTION
      Error: Bad credentials (secret GITHUB_TOKEN may be expired)
      Action needed: Regenerate the secret in repo settings

====================================
ACTIONS TAKEN:
  1. Cancelled 2 stuck runs (owner/repo-two CI, queued 45m)
  2. Re-ran failed jobs on owner/repo-two CI
  3. Restarted mac-repo-two runner via LaunchAgent
  4. Cleaned 3.2GB of build caches on local runners

NEEDS MANUAL ACTION:
  1. owner/repo-three: Regenerate expired GITHUB_TOKEN secret
  2. owner/repo-four: VPS runner offline (SSH to VPS to restart)
====================================
```

============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After the initial scan and fix pass:

1. Wait 60 seconds for re-triggered workflows to start.
2. Re-check the status of any workflow that was re-run or had fixes applied.
3. If still failing, attempt one more diagnosis + fix cycle.
4. After 2 iterations, report remaining failures as "needs manual attention."

============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md`

Entry format:
### /ci-fixer -- {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Repos scanned: {{N}}
- Issues found: {{N}}
- Auto-fixed: {{N}}
- Needs manual: {{N}}
- Common issue: {{most frequent failure type}}
- Self-healed: {{yes -- what | no}}
- Suggestion: {{improvement idea or "none"}}

Only log if the memory directory exists. Skip silently if not found.
