---
name: manus
description: Create and manage AI agent tasks via Manus API. Manus is an autonomous AI agent that can browse the web, use tools, and deliver complete work products.
homepage: https://manus.im
user-invocable: true
disable-model-invocation: true
metadata:
  clawdbot:
    emoji: "🤖"
    primaryEnv: MANUS_API_KEY
    requires:
      bins: [curl, jq]
      env: [MANUS_API_KEY]
---

# Manus AI Agent

Create tasks for Manus, an autonomous AI agent, and retrieve completed work products.

## Authentication

Set `MANUS_API_KEY` env var with your key from [manus.im](https://manus.im).

---

## Commands

All commands use `scripts/manus.sh`.

### Create a Task

```bash
{baseDir}/scripts/manus.sh create "Your task description here"
{baseDir}/scripts/manus.sh create "Deep research on topic" manus-1.6-max
```

Profiles: `manus-1.6` (default), `manus-1.6-lite` (fast), `manus-1.6-max` (thorough).

### Check Status

```bash
{baseDir}/scripts/manus.sh status <task_id>
```

Returns: `pending`, `running`, `completed`, or `failed`.

### Wait for Completion

```bash
{baseDir}/scripts/manus.sh wait <task_id>
{baseDir}/scripts/manus.sh wait <task_id> 300  # custom timeout in seconds
```

Polls until task completes or times out (default: 600s).

### Get Task Details

```bash
{baseDir}/scripts/manus.sh get <task_id>
```

Returns full task JSON including status and output.

### List Output Files

```bash
{baseDir}/scripts/manus.sh files <task_id>
```

Shows filename and download URL for each output file.

### Download Output Files

```bash
{baseDir}/scripts/manus.sh download <task_id>
{baseDir}/scripts/manus.sh download <task_id> ./output-folder
```

Downloads all output files to the specified directory (default: current directory).

### List Tasks

```bash
{baseDir}/scripts/manus.sh list
```

---

## Typical Workflow

1. **Create task**: `manus.sh create "your prompt"`
2. **Wait for completion**: `manus.sh wait <task_id>`
3. **Download results**: `manus.sh download <task_id>`

---

## Advanced API Features

For file attachments, webhooks, connectors, projects, multi-turn conversations, and interactive mode, see the full Manus API documentation:

- API Reference: https://open.manus.ai/docs
- Main Docs: https://manus.im/docs

---

## Security & Permissions

**What this skill does:**
- Sends task prompts to the Manus API at `api.manus.ai`
- Polls for task completion and downloads output files from Manus CDN
- API key is sent only in the `API_KEY` header to `api.manus.ai`

**What this skill does NOT do:**
- Does not upload local files (file upload is an advanced API feature not implemented in the bundled script)
- Does not register webhooks or connect external accounts
- Does not send your API key to any endpoint other than `api.manus.ai`
- Does not modify local system configuration
- Cannot be invoked autonomously by the agent (`disable-model-invocation: true`)
- You must explicitly trigger every Manus task

**Bundled scripts:** `scripts/manus.sh` (Bash — uses `curl` and `jq`)

Review `scripts/manus.sh` before first use to verify behavior.
