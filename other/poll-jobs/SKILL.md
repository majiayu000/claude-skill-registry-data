---
name: poll-jobs
description: Poll the job queue, claim and execute a pending job. Each invocation is a fresh ephemeral session spawned by executor/run.sh.
---

# Poll Jobs

Single iteration of the executor. Claim one queued job, execute it, mark complete or failed.

## Architecture

The executor runs via cron, not `/loop`. Every 5 minutes, `executor/run.sh` checks for queued jobs and spawns a fresh `claude` session per job (up to MAX_SESSIONS in parallel). Each session runs this skill, then exits. No context bloat, no process management.

## Procedure

### 1. Pull latest

```bash
cd $REPO_ROOT/techniques
git pull --rebase
```

If rebase fails due to conflicts, abort and report. Do not force-push.

### 2. Check queue

List files in `jobs/queue/`. If no `.md` files exist, go to step 6 (heartbeat-only).

### 3. Claim job

Pick the oldest job file (by filename sort). Claim it:

```bash
git mv jobs/queue/<job>.md jobs/active/<job>.md
```

Update the file's YAML frontmatter:
- Set `status: active`
- Add `claimed_at: <ISO timestamp>`
- Add `executor: <hostname>`

Commit and push immediately so the publisher sees the claim:
```bash
git add jobs/active/<job>.md
git commit -m "claim job: <job_id>"
git push
```

If the push fails because another session claimed a job concurrently, pull --rebase and check if YOUR job was already claimed by someone else. If so, pick the next queued job or exit.

### 4. Execute job

Read the job's `type` field. Look up `job-types/<type>.md` in this repo for type-specific execution instructions. If the file exists, follow it. If not, interpret the job's markdown instructions directly.

Commit and push results at natural breakpoints during execution.

### 5. Complete or fail

**On success:**
```bash
git mv jobs/active/<job>.md jobs/completed/<job>.md
```
Update frontmatter:
- Set `status: completed`
- Add `completed_at: <ISO timestamp>`
- Add `run_id: <run_id>` (if applicable, per job-type instructions)

**On failure:**
```bash
git mv jobs/active/<job>.md jobs/failed/<job>.md
```
Update frontmatter:
- Set `status: failed`
- Add `failed_at: <ISO timestamp>`
- Add `error: "<description>"`

Commit and push:
```bash
git add jobs/
git commit -m "<completed|failed> job: <job_id>"
git push
```

### 6. Heartbeat

Update `sync/status.json`:
```json
{
  "executor_id": "<hostname>",
  "heartbeat": "<ISO timestamp>",
  "state": "idle",
  "current_job": null,
  "history": ["<last 10 job IDs>"]
}
```

During execution, set `state: "executing"` and `current_job: "<job_id>"`.

Commit and push:
```bash
git add sync/status.json
git commit -m "heartbeat"
git push
```

## Notes

- Each session claims exactly one job. Parallelism comes from cron spawning multiple sessions, not from one session handling multiple jobs.
- The git mv claim mechanism prevents double-claiming. If two sessions race for the same job, one will fail the push and should pick another.
- If `git push` fails (remote ahead), pull --rebase and retry once. If still failing, log and continue.
