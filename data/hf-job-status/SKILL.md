---
name: hf-job-status
description: Check the status of a Hugging Face training job
---

# HF Job Status

Check the current status of a training job running on Hugging Face cloud GPUs.

## How to Use

```bash
$CLAUDE_CONFIG_DIR/skills/hf-job-status/scripts/hf-job-status.sh <job_id>
```

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `job_id` | The job ID returned from hf-job-submit | `job_abc123` |

## Prerequisites

- `HF_TOKEN` environment variable must be set

## Output

Returns job status information:
- `pending` - Job is queued
- `running` - Job is actively training
- `completed` - Job finished successfully
- `failed` - Job encountered an error

## Example

```bash
$CLAUDE_CONFIG_DIR/skills/hf-job-status/scripts/hf-job-status.sh job_abc123
```

Output:
```
Job ID: job_abc123
Status: running
Progress: 45%
Runtime: 12m 34s
```
