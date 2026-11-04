---
name: file-swarm
description: Use file-swarm to run Codex-controlled, OpenAI-compatible, file-level coding swarms. Trigger when a coding task should be split into guarded patch workers, when the user asks for multi-model or multi-slot cooperation, when Codex should generate hard_constraints.yaml/interface_contract.yaml, run file-swarm auto/preflight/smoke-test/summary/apply/repair, or inspect which model handled which task.
---

# file-swarm

Use `file-swarm` as a patch-only coding swarm controlled by Codex.

Core principle:

```text
Codex sets rules.
Workers produce patches.
file-swarm enforces guardrails.
Tests validate.
Codex decides whether to apply.
```

Do not bypass Patch Guard by editing target repo files directly unless the user explicitly asks for manual implementation.

## Integrated Skill Pair

Use this skill together with `$file-swarm-agent` when the request mixes coding and structured actions.

- Use `$file-swarm` for guarded file-level coding patches.
- Use `$file-swarm-agent` for non-patch actions such as shell diagnostics, browser fetches, screenshot plans, mouse/keyboard dry-runs, and MCP-style tool calls.
- Keep coding work in patch workers unless the user explicitly asks for real action execution.
- Keep action work in dry-run mode unless the user explicitly approves side effects.

Decision rule:

```text
Coding task that should change repository files -> file-swarm patch worker
System/browser/mouse/MCP task that should execute or simulate actions -> file-swarm-agent
Mixed request -> run patch workflow first, then action dry-run/benchmark/report as supporting evidence
```

## Quick Start

Run from the target repository root:

```bash
file-swarm init --repo .
file-swarm preflight --repo .
file-swarm codex-contract "<user task>" --repo .
file-swarm auto "<user task>" --repo . --parallel 2 --dry-merge
file-swarm summary --run <run_id> --for-codex
```

Apply only when `codex_summary.md` recommends it and guard reports passed:

```bash
file-swarm apply --run <run_id> --allow-dirty
```

Repair failed or rejected tasks:

```bash
file-swarm repair --run <run_id>
```

## Live Checks

Never call a live slot without a configured environment variable API key.

```bash
file-swarm preflight --repo . --live
file-swarm smoke-test --repo . --live
```

Rules:

- `preflight --live` sends `Reply with OK.` to enabled keyed slots.
- `smoke-test --live` must receive a real unified diff patch from the provider.
- Live smoke-test must fail if the model returns prose or non-diff text.
- Never print or write full API keys; use fingerprints only.

## Task Allocation

Let `file-swarm` split tasks when possible. Prefer file-level task boundaries:

- One task owns one coherent file or tightly coupled file group.
- Keep `allowed_files` as small as possible.
- Tests can be a separate task when they touch a dedicated test file.
- UI/design text can be a separate task from domain logic.
- Never let workers edit config, lockfiles, `.env`, dependencies, or unrelated files unless hard constraints explicitly allow it.

Good task split:

```text
task_001 -> src/clicker_core.py       -> domain logic and safety rules
task_002 -> src/clicker_ui.py         -> designed presentation helpers
task_003 -> tests/test_clicker_*.py   -> behavior and integration tests
```

Avoid:

```text
task_001 -> entire repository
task_002 -> package manager files
task_003 -> duplicate ownership of task_001 files
```

## Model And Slot Assignment

Model slots live in:

```text
.swarm/config/model_slots.yaml
```

Each enabled slot has:

- `id`
- `provider`
- `base_url` or `base_url_env`
- `api_key_env`
- `allowed_models`
- `default_model`

Dispatch behavior:

- `--parallel N` limits global worker concurrency.
- A slot is leased before worker start.
- Busy slots are skipped during selection.
- One slot cannot serve two workers at the same time.
- If no slot is free, tasks wait instead of reusing a busy slot.

## NVIDIA To Mimo Failover

Default live coding route:

```text
1. NVIDIA GLM primary: z-ai/glm-5.1
2. NVIDIA auxiliary models: Kimi, Qwen, DeepSeek when configured
3. Mimo Pro super-brain: mimo-v2.5-pro on /anthropic
4. Mimo multimodal worker: mimo-v2.5 on /anthropic
5. Mimo /v1 compatibility slot, only if it returns non-empty text
```

Use these endpoints in `model_slots.yaml`:

```text
NVIDIA: https://integrate.api.nvidia.com/v1
Mimo preferred: https://token-plan-cn.xiaomimimo.com/anthropic
Mimo compatibility: https://token-plan-cn.xiaomimimo.com/v1
```

Failover is automatic for patch workers when a slot returns:

```text
rate_limit
timeout
connection_error
empty_response
api_error_status_429
api_error_status_502
api_error_status_503
```

When this happens:

- Release the failed slot immediately.
- Exclude that slot from the current task retry.
- Acquire the next eligible, keyed, preflight-ready slot.
- Record `slot_failover` in `timeline.jsonl`.
- Prefer Mimo `/anthropic` over Mimo `/v1`.
- Treat Mimo `/v1` empty chat text as `empty_response`, not success.

Do not retry side-effecting `agent_worker` tasks on another slot automatically.

## Showing Which Model Did What

After `auto`, inspect these files:

```text
.swarm/runs/<run_id>/dispatch_report.json
.swarm/runs/<run_id>/dispatch_report.md
.swarm/runs/<run_id>/timeline.jsonl
.swarm/runs/<run_id>/transcripts/task_xxx.meta.json
.swarm/runs/<run_id>/codex_summary.md
```

Report model/task mapping to the user in this shape:

```text
task_001: src/clicker_core.py
  slot: mock1
  model: mock-model
  provider: mock
  status: passed

task_002: src/clicker_ui.py
  slot: nvidia_glm_slot
  model: glm-...
  provider: openai_compatible
  status: passed
```

Use `dispatch_report.json` as source of truth for:

- `task_id`
- `slot_id`
- `model`
- `provider`
- `is_mock`
- `status`
- `modified_files`
- `provider_ok`
- `provider_error`

Use `timeline.jsonl` to verify:

- `slot_acquired`
- `worker_started`
- `worker_finished`
- `slot_released`

## Worker Input Requirements

Every worker input must include:

- user request
- task id and task type
- assigned files
- allowed files
- read-only context files
- `hard_constraints.yaml`
- `interface_contract.yaml`
- repo map
- instruction to return unified diff only

Workers must not write files directly. They only return patches.

## Patch Guard Rules

Patch Guard must reject:

- empty patches
- patches outside `allowed_files`
- `.env` or `.env.local`
- `package.json`
- `pyproject.toml`
- `requirements.txt`
- lockfiles
- absolute paths
- file deletions unless explicitly allowed
- suspected secrets or API keys

Only guard-passed patches can enter `final.patch`.

## Codex Decision Checklist

Before applying:

- Read `.swarm/runs/<run_id>/codex_summary.md`.
- Confirm `hard_constraints_loaded: yes`.
- Confirm `interface_contract_loaded: yes`.
- Confirm `guard_rejected_tasks: 0`.
- Confirm `final_patch_generated: yes`.
- Confirm `final_patch_empty: no`.
- Confirm `recommend_apply: yes` or `yes_with_caution`.
- Read `validation_report.md` if present.

Do not apply when:

- `recommend_apply: no`
- guard rejected any task
- final patch is empty
- contracts were missing
- merge conflict occurred
- critical worker failed

## Apply Safety

Default apply requires a clean git worktree.

```bash
file-swarm apply --run <run_id>
```

Use `--allow-dirty` only when the user expects local changes:

```bash
file-swarm apply --run <run_id> --allow-dirty
```

`git apply` is the default method. Do not use fallback apply unless explicitly requested:

```bash
file-swarm apply --run <run_id> --allow-fallback-apply
```

After apply, inspect:

```text
.swarm/runs/<run_id>/apply_report.md
.swarm/runs/<run_id>/validation_report.md
```

## Repair Loop

Use repair when guard or validation failed:

```bash
file-swarm repair --run <run_id>
file-swarm summary --run <run_id> --for-codex
```

Repair input must include:

- original task
- original patch
- guard violation
- validation error summary
- hard constraints
- interface contract

If repair cannot run, it must write:

```text
repair_status: skipped
reason: ...
```

or:

```text
repair_status: failed
reason: ...
```

## Recommended User-Facing Report

After a run, summarize:

```text
Run: <run_id>
Mode: mock/live/mixed
Tasks: <completed>/<total>
Guard: <passed> passed, <rejected> rejected
Models used: <model list>
Slots used: <slot list>
Modified files: <file list>
Recommend apply: <yes/no/yes_with_caution>
Reason: <summary reason>
Next command: <apply/repair/summary command>
```

Then include a compact task table:

```text
task_id | file(s) | slot | model | provider | status
```

Never include API keys, bearer tokens, or raw provider credentials.
