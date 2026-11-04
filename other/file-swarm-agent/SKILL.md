---
name: file-swarm-agent
description: Use the enhanced file-swarm agent subsystem for non-patch structured action tasks, including shell, browser, mouse, keyboard, screenshot, wait, and MCP-style tool actions. Trigger when the user asks file-swarm to execute agent tasks, benchmark models for action quality, route non-coding tasks to an agent worker, use NVIDIA rate limiting, or inspect cross-model agent benchmark results.
---

# file-swarm-agent

Use this skill when `file-swarm` is being used as more than a patch worker and must execute model-planned structured actions.

This skill is separate from `$file-swarm`:

- `$file-swarm` controls guarded code patch workflows.
- `$file-swarm-agent` controls structured action workflows such as shell/browser/mouse/MCP dry-run tasks.

## Core Modules

The latest implementation is in:

```text
src/file_swarm/agent_executor.py
src/file_swarm/rate_limiter.py
src/file_swarm/providers/openai_compatible_provider.py
src/file_swarm/providers/anthropic_provider.py
src/file_swarm/task_planner.py
tests/benchmark_nvidia_v2.py
tests/test_enhanced_agent_benchmark.py
```

Benchmark outputs are currently stored in:

```text
benchmark_report.md
benchmark_results.json
```

## AgentExecutor

`AgentExecutor` asks a model to return a JSON array of typed actions, validates the action structure, applies safety checks, and executes or dry-runs actions sequentially.

Supported action types:

```text
shell
browser_open
browser_fetch
mouse_click
mouse_move
mouse_drag
key_type
key_press
key_hotkey
screenshot
mcp_call
wait
```

Use dry-run mode for benchmark and safety validation. Do not run real mouse, keyboard, browser, or shell actions unless the user explicitly asks for real execution and the target environment is safe.

## Safety Rules

Always preserve these guardrails:

- Block destructive commands such as `rm -rf`, `format`, `shutdown`, `reboot`, fork bombs, and pipe-to-shell installers.
- Keep shell commands inside the configured working directory.
- Cap command output.
- Use per-command timeouts.
- For browser actions, allow only `http://` or `https://` URLs.
- For MCP `env_get`, never expose secrets, API keys, tokens, passwords, or credentials.
- Prefer `dry_run=True` in tests and benchmarks.

## Model Prompt Contract

When asking a model for actions, require:

```json
[
  {"type": "shell", "command": "dir"},
  {"type": "mcp_call", "tool": "datetime_now", "args": {}}
]
```

Rules:

- Return JSON only.
- Include a `type` field on every action.
- Use at most 10 actions.
- Use Windows-compatible shell commands on Windows.
- Prefer typed actions over prose.
- Increase `max_tokens` and retry once if the model returns an empty response.

## Task Routing

Use `split_agent_tasks()` when a request is not primarily a coding patch task and mentions actions such as:

- run/check/list system commands
- open or fetch a web page
- click/move/type/screenshot
- call MCP tools
- inspect environment safely
- produce a system report

Do not route normal coding requests to `agent_worker`. Coding work should stay with patch workers under `$file-swarm`.

## Rate Limiting

`src/file_swarm/rate_limiter.py` provides async rate limiting and retry behavior.

Important behavior:

- NVIDIA endpoints get conservative limiting.
- Mimo and relaxed endpoints are not throttled by default.
- The limiter releases its lock before sleeping, avoiding deadlocks.
- Retry only rate-limit or transient server-busy failures such as 429, 502, and 503.

Use rate limiting in provider calls, not in task planning.

## Provider Notes

`OpenAICompatibleProvider` integrates rate limiting and retry behavior.

`AnthropicProvider` supports Anthropic-style Messages API endpoints and returns the shared `ProviderResult` shape.

Provider failures must return:

```text
ProviderResult(ok=False, error="...")
```

Do not raise raw provider exceptions to the CLI top level.

Never log API keys. Only log key fingerprints.

## Benchmark Workflow

Run benchmark code only when explicitly requested:

```bash
python tests/benchmark_nvidia_v2.py
```

The benchmark is designed to be dry-run and side-effect safe.

Inspect:

```text
benchmark_report.md
benchmark_results.json
```

Report results in this shape:

```text
Model | Pass Rate | Best Category | Avg Latency | Notes
```

If a model returns 403, timeout, or empty response, report the error clearly and do not fabricate a pass.

## Current Benchmark Interpretation

The current benchmark report says:

- Mimo-v2.5 passed the most categories.
- Mimo-v2.5-Pro passed multiple categories but timed out on some tasks.
- Several NVIDIA-hosted model IDs returned 403 in the tested environment.
- Dry-run action execution was used, so no real shell/browser/mouse effects were required for benchmark scoring.

Treat benchmark results as environment-specific, not universal truth.

## User-Facing Summary

When this skill is used, summarize:

```text
Agent subsystem: enabled
Task category: shell/browser/mouse/mcp/mixed
Provider/model: <provider> / <model>
Dry run: yes/no
Actions planned: <count>
Actions executed: <count>
Blocked actions: <count>
Rate limiter: enabled/disabled
Result: passed/failed
Evidence files: benchmark_report.md, benchmark_results.json, or run artifacts
```

Never include raw secrets, bearer tokens, or API key values.
