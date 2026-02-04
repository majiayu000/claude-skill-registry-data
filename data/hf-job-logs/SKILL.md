---
name: hf-job-logs
description: View logs from a Hugging Face training job
---

# HF Job Logs

View the training logs from a job running on Hugging Face cloud GPUs.

## How to Use

```bash
$CLAUDE_CONFIG_DIR/skills/hf-job-logs/scripts/hf-job-logs.sh <job_id> [tail_lines]
```

## Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `job_id` | The job ID from hf-job-submit | required | `job_abc123` |
| `tail_lines` | Number of lines to show | 50 | `100` |

## Prerequisites

- `HF_TOKEN` environment variable must be set

## Output

Returns the training logs, including:
- Training progress (loss, learning rate)
- Epoch/step information
- Errors and warnings
- Final results

## Example

```bash
# Show last 50 lines (default)
$CLAUDE_CONFIG_DIR/skills/hf-job-logs/scripts/hf-job-logs.sh job_abc123

# Show last 100 lines
$CLAUDE_CONFIG_DIR/skills/hf-job-logs/scripts/hf-job-logs.sh job_abc123 100
```

Output:
```
[2024-01-15 10:30:15] Starting training...
[2024-01-15 10:30:20] Epoch 1/3, Step 10/100, Loss: 2.345
[2024-01-15 10:30:25] Epoch 1/3, Step 20/100, Loss: 2.123
...
```
