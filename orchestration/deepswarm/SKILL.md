---
name: deepswarm
description: Use when running parallel AI workers for any long-running or multi-turn batch API task. Auto-calculates optimal workers + stagger. Supports tiered delegation (V4 Pro orchestrator → V4 Flash workers). 99.95% API success rate at scale.
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [orchestration, parallel, workers, api-generation, swarm, batch, multi-turn, delegation, tiered-models]
    related_skills: [tmux-agent-orchestrator, hermes-agent]
---

# DeepSwarm — Task-Agnostic Parallel Worker Orchestration

Spawn N parallel API workers for **any** long-running or multi-turn batch task. Auto-calculates optimal worker count and stagger delay. Supports tiered model delegation: orchestrator plans with a frontier model (V4 Pro), workers execute with a cheaper model (V4 Flash).

## Overview

DeepSwarm 2.0 generalizes the proven orchestration pattern from the 19,331-trace generation project to any batch API task. You define a task — translations, reasoning traces, code reviews, summarization — and DeepSwarm parallelizes it across optimal workers with the right stagger for your API.

**The core insight:** API rate limits are a function of simultaneous connections, not total volume. Auto-calculated stagger + worker count = 99.95% success.

## When to Use

- **Any** batch API task: generation, translation, summarization, extraction, classification
- Long-running individual calls (30s+) that benefit from parallelization
- Multi-turn tasks where each worker loops through conversation turns
- Cost optimization via tiered delegation (orchestrator ≠ worker model)
- Crash-resilient batch processing (checkpointed, idempotent)

**Don't use for:**
- Quick calls under 10s (overhead not worth it — just loop)
- Tasks requiring inter-worker coordination (use `delegate_task`)
- Real-time interactive sessions (use tmux-agent-orchestrator)

## Quick Start

```bash
# Install
hermes skills tap add amanning3390/deepswarm

# Define your task (task.yaml)
# Generate seeds
python3 scripts/seed.py --task task.yaml

# Launch — auto-optimizes workers, stagger, model routing
python3 scripts/swarm.py --task task.yaml --total 1000

# Filter — repair JSON, validate structure, apply length thresholds
python3 scripts/filter.py --input-dir output/ --output clean.jsonl --errors errors.jsonl
```

## Task Definition (task.yaml)

```yaml
# What to do
task_type: generation              # generation | translation | summarization | custom
prompt_template: |
  You are an AI assistant. {{seed}}

# Model routing (tiered delegation)
orchestrator_model: deepseek-v4-pro  # Plans, monitors, handles errors
worker_model: deepseek-v4-flash      # Executes batches (cheaper!)
worker_api_base: https://api.deepseek.com/v1/chat/completions
worker_max_tokens: 4096

# Execution control
multi_turn: true                    # Workers loop through conversation turns
max_turns: 20                       # Max turns per worker conversation
seeds_file: seeds.jsonl             # Pre-generated task seeds

# Worker optimization (auto-calculated if omitted)
workers: auto                       # auto | N
stagger: auto                       # auto | seconds
batch_size: auto                    # auto | tasks per worker

# Output
output_dir: output/
output_format: jsonl               # jsonl | json | parquet
checkpoint_every: 10                # Save progress every N tasks

# Optional: custom worker logic
worker_script: custom_worker.py     # Override default worker behavior
```

## Tiered Model Delegation

Orchestrator (V4 Pro) and workers (V4 Flash) can use different models:

```
User Task → V4 Pro (plans, monitors)
              ├─ V4 Flash Worker 0 → API → output/
              ├─ V4 Flash Worker 1 → API → output/
              ├─ V4 Flash Worker 2 → API → output/
              └─ ...
```

**Why tiered delegation matters:**
- V4 Pro costs ~3× V4 Flash per token
- Orchestrator only plans + monitors (few calls)
- Workers make thousands of calls — use the cheapest model that works
- Typical savings: 60-70% vs using V4 Pro for everything

**When to use same model for both:**
- Task quality requires frontier reasoning at every step
- Worker model doesn't support the required format
- Budget allows it and quality is paramount

## Auto-Optimization

When `workers: auto` and `stagger: auto`:

1. DeepSwarm runs a single calibration call to measure call duration
2. Calculates optimal workers: `min(8, floor(rate_limit / call_duration))`
3. Sets stagger: `call_duration / workers × 2`
4. Adjusts batch_size: `total / workers`

**Calibration table (pre-computed):**

| Call Duration | Workers | Stagger | Success | Throughput |
|--------------|---------|---------|---------|------------|
| <10s | 16 | 1s | 99.9% | ~5,760/hr |
| 10-30s | 12 | 2s | 99.9% | ~1,440/hr |
| 30-60s | 8 | 5s | 99.95% | ~440/hr |
| 60-90s | 6 | 10s | 99.9% | ~240/hr |
| >90s | 4 | 15s | 99.9% | ~96/hr |

## Multi-Turn Task Support

For tasks requiring conversation loops (generation, debugging, interactive work):

```
Worker loop:
  for each seed:
    messages = [system_prompt, user_task]
    for turn in range(max_turns):
      response = api_call(messages, model=worker_model)
      messages.append({"role": "assistant", "content": response})
      if task_complete(response):
        break
      if needs_tool_call(response):
        messages.append(simulate_tool_response(response))
```

Each turn is an independent API call. Multi-turn tasks benefit most from parallelization because per-task latency is high.

## Task-Agnostic Worker Design

The worker (`worker.py`) accepts a YAML task definition and executes any pipeline:

```python
def run_task(seed, config):
    messages = build_messages(seed, config)
    for turn in range(config["max_turns"]):
        response = call_api(messages, config)
        if is_complete(response, config):
            return finish(response, messages)
        if needs_continuation(response, config):
            messages = append_turn(messages, response, config)
    return messages
```

Built-in task types:
- `generation` — Generate content from seed (the trace generation pattern)
- `translation` — Translate each seed text
- `summarization` — Summarize each seed document
- `classification` — Classify each seed input
- `custom` — Uses `worker_script` for completely custom logic

## Common Pitfalls

1. **`workers: auto` choosing too many.** If calibration call was fast but actual calls are slow, override manually.
2. **Forgetting to stagger between workers.** Even 2 workers at same millisecond can trigger rate limits on slow APIs.
3. **Mixing models without checking format compatibility.** Worker model must support the same prompt format as orchestrator.
4. **Not checkpointing.** Worker dies at 120/125 = lost work. Checkpoint every 10.
5. **Shell `&` without `wait`.** Without `wait`, shell exits early and kills child workers.
6. **Using V4 Pro for workers when V4 Flash would work.** Check quality on 10-sample test before committing to expensive model.
7. **Not deleting error outputs before restarting.** Error files consume indices and inflate disk.

## Verification Checklist

- [ ] Task YAML has valid model names and API base URL
- [ ] API key exported for both orchestrator and worker models
- [ ] `workers: auto` or manual count ≤ 8 per batch
- [ ] `stagger: auto` or manual ≥ call_duration / workers × 2
- [ ] Worker model tested on 5-sample run before full batch
- [ ] Output directory exists and is writable
- [ ] Seeds file exists with correct format
- [ ] Checkpointing enabled for runs >100 tasks
- [ ] Orchestrator model is V4 Pro (or equivalent frontier) for planning
- [ ] Worker model is V4 Flash (or cheapest model that handles the task)
