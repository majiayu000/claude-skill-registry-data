---
name: publish-job
description: Create a job for the remote executor and push it to the private repo queue.
---

# Publish Job

Create a job file and push it to the executor queue via the private git repo.

## Input

The user describes what they want the executor to do. This can be:
- An autospec run (provide spec path, properties, trust model)
- An arbitrary task (freeform instructions)

## Procedure

1. Generate a job ID: `job_<unix_timestamp>`
2. Determine job type: `autospec` if the user references a spec/properties/trust-model, otherwise `arbitrary`
3. If the job references local files that the executor needs, copy them to `$AUTOSPEC_ROOT/techniques/context/<job_id>/` (or a descriptive name if the user provides one)
4. Create the job file at `$AUTOSPEC_ROOT/techniques/jobs/queue/<job_id>.md` with this format:

```markdown
---
id: <job_id>
title: "<short description>"
type: autospec | arbitrary
priority: normal
created: <ISO 8601 timestamp>
status: queued
context_dir: context/<name>
timeout_hours: 24
---

# Instructions

<instructions for the executor, written as markdown>
```

For autospec jobs, the instructions should specify:
- Path to spec file (relative to techniques/)
- Path to properties file
- Path to trust model
- Any `--techniques` flags
- Any config overrides

5. Commit the new files to the private repo:
```bash
cd $AUTOSPEC_ROOT/techniques
git add jobs/queue/<job_id>.md
git add context/  # if new context files were added
git commit -m "queue job: <title>"
git push
```

6. Confirm to the user: job ID, what was queued, and that it was pushed.

## Notes

- The `context_dir` field is optional. Only set it if files were copied to context/.
- The executor will pick this up on its next poll cycle.
- Use `/job-status` to check progress after publishing.
