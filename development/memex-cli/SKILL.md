---
name: memex-cli
description: "Execute AI-powered command-line tasks with memory, replay, and resume capabilities using memex-cli. Use when (1) Running AI backend tasks (codex, claude, gemini), (2) Replaying recorded events from JSONL files, (3) Resuming interrupted runs by run_id, (4) Executing prompts with streaming output in jsonl or text format."
---

# Memex CLI

A CLI wrapper for AI backends with built-in memory, replay, and resume support.

## Core Commands

### Run a Task

```bash
memex-cli run \
  --backend <backend> \
  --prompt "<prompt>" \
  --stream-format <format>
```

**Parameters:**
- `--backend`: AI backend (`codex`, `claude`, `gemini`)
- `--prompt`: Task prompt
- `--stream-format`: Output format (`jsonl` or `text`)
- `--model`: Model name (optional, for codex backend)
- `--model-provider`: Model provider (optional, for codex backend)

### Replay Events

```bash
memex-cli replay --events ./run.events.jsonl --format text
```

Replays a previously recorded run from its event log.

### Resume a Run

```bash
memex-cli resume \
  --run-id <RUN_ID> \
  --backend <backend> \
  --prompt "<prompt>" \
  --stream-format <format>
```

Continues a previous run using its `run_id`.

## Backend Examples

### Codex

```bash
memex-cli run --backend "codex" --model "deepseek-reasoner" --model-provider "aduib_ai" --prompt "任务描述" --stream-format "jsonl"
```

### Claude

```bash
memex-cli run --backend "claude" --prompt "任务描述" --stream-format "jsonl"
```

### Gemini

```bash
memex-cli run --backend "gemini" --prompt "任务描述" --stream-format "jsonl"
```

## Output

Each run generates `run.events.jsonl` for auditing and replay.
