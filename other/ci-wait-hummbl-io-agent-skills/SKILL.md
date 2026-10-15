---
name: ci-wait
description: Watch a CI run until completion and report pass/fail.
version: 0.1.0
execution-mode: advisory
argument-hint: "[run-id | --last]"
category: backend-infra
status: candidate
---
# CI Wait Command

Monitor a GitHub Actions workflow run until it completes, then report results.

## Usage

```bash
[ci-wait]               # Watch the most recent run
[ci-wait] --last        # Watch the most recent run (explicit)
[ci-wait] 12345678      # Watch a specific run ID
```

## Execution

### 1. Find the run
If no run ID provided:
```bash
gh run list --limit 5 --json databaseId,displayTitle,status,conclusion,headBranch,createdAt
```
Pick the most recent non-completed run. If all are completed, report the latest result.

### 2. Watch the run
```bash
gh run watch <RUN_ID>
```
This blocks until the run completes.

### 3. Report results
```bash
gh run view <RUN_ID> --json conclusion,status,jobs
```
For each job, report name + conclusion.

### 4. On failure, fetch logs
```bash
gh run view <RUN_ID> --log-failed 2>&1 | tail -50
```
Extract the key error lines.

## Output Format

```
CI Watch | <run-id> | <branch>
══════════════════════════════

Status: PASS / FAIL / CANCELLED
Duration: Xm Ys
Commit: <sha> (<message>)

| Job | Status |
|-----|--------|
| job-name | pass/fail |

<if failed>
## Failure Details
<relevant error lines from --log-failed>
</if>
```

## Constraints

- This is READ-ONLY. Do not modify code or re-trigger runs.
- If the run takes more than 10 minutes, report current status and let the user decide whether to keep waiting.
- Do not fabricate CI results -- always run the actual `gh` commands.
- If `gh` is not authenticated, suggest `[gh-auth-recovery]`.
