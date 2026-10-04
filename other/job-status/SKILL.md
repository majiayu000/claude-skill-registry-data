---
name: job-status
description: Check executor status and job queue state from the publisher machine.
---

# Job Status

Pull the private repo and display executor state, active jobs, and queue summary.

## Procedure

1. Pull latest:
```bash
cd $AUTOSPEC_ROOT/techniques
git pull --rebase
```

2. Read `sync/status.json` for executor heartbeat.

3. Scan job directories:
- `jobs/queue/`: pending jobs
- `jobs/active/`: currently executing
- `jobs/completed/`: finished (show recent)
- `jobs/failed/`: errored (show recent)

4. If there's an active job with a `run_id`, read `runs/<run_id>/status.json` for autospec progress.

5. Present summary:

```
Executor: <executor_id> | <state> | last heartbeat: <relative time>

Active: <job_id> - <title> (claimed <relative time> ago)
  Run: <run_id> | state: <run_state> | step: <N>

Queue: <count> jobs pending
  - <job_id>: <title> (priority: <p>)

Recent completed: <count>
  - <job_id>: <title> (completed <relative time> ago)

Recent failed: <count>
  - <job_id>: <title> - <error>
```

## Notes

- If `sync/status.json` shows `state: offline` or heartbeat is stale (>15 min), warn the user.
- Show at most 5 recent completed/failed jobs.
