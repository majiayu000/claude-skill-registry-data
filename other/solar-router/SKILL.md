---
name: solar-router
description: >
  Shared router that runs AI providers (Codex, Claude, Agy/Antigravity, Agent, Ollama) with Solar repo context.
  Single source of truth for provider selection, fallback, and async routing policy.
  Use when solar-gateway, solar-app (channel=app), async-tasks, or other runtimes need to invoke an AI with
  cwd = SOLAR_WORKSPACE and paths resolved against the active workspace.
---

# Solar Router

## Purpose

Single source of truth for all AI execution in Solar:
- **Provider selection and fallback** live only here.
- **Async routing policy** (`direct_reply` vs `async_draft_created`) lives only here.
- Used by solar-gateway (WebSocket/bridge) and solar-async-tasks (task execution).

## Operational boundary

Use this skill as infrastructure for Solar runtimes and controlled diagnostics. Do not use `solar-router` or provider CLIs as the normal path for work that is deferred, multiprovider, browser/MCP-dependent, network/auth/keychain-dependent, long-running, or likely to block the conversation.

For that work, create or propose a task through `solar-async-tasks`. When `solar-system` supervises `async-tasks`, approve/queue the task and let the system runtime execute it.

## Scope

- Accept JSON payload (router contract v3) on stdin; output structured JSON on stdout.
- Run the selected provider with `cwd=SOLAR_WORKSPACE` so all providers see `sun/`, `planets/`, and workspace `AGENTS.md`.
- Resolve `SOLAR_ROUTER_SYSTEM_PROMPT_FILE` and `SOLAR_ROUTER_RUNTIME_DIR` against `SOLAR_WORKSPACE` when relative.
- Codex default command includes `-C <repo-root>` and `--add-dir ~/.codex`.
- Persist conversation turns in runtime dir (JSONL) and inject continuity into each prompt: rolling `*-summary.txt` from `<solar_summary>` plus recent turns (`SOLAR_ROUTER_CONTEXT_TURNS`).
- Inject the cross-channel intention from the continuity row in `state.sqlite`. See `references/continuity.md`.
- Own the A3 mandate CLI (`scripts/delegation_ctl.py`). The YAML in `sun/delegations/` is opened by `solar-state`. Any caller gates mutating routines through `check` and fails closed. See `references/a3-mandates.md`. Unrelated to JIT agent/skill delegation.
- Answer "where are we" on demand with `scripts/work_status.sh` (intention, machine queue, today's blockers, mandates). Read-only, no cadence: periodic briefings are recurring async tasks. Behaviour layer in `references/signal-orchestration.md`.
- Implement `DecisionEngine`: decide `decision.kind` based on `mode`, `channel`, and AI semantic output. On telegram/n8n/app, `async_draft_created` queues work + `notify_when: completed` and returns a short ACK.
- Resolve JIT context from `metadata`: lookup agent/skills in planet → fallback to core → generate role inline if not found.
- Append `start`/`end` audit rows through `solar-state` for each execution (including failed early-exit paths).

## Internal architecture

```
scripts/
  run_router.py        — thin entrypoint: stdin → route() → stdout + exit
  router.py            — all provider-agnostic logic (parse, validate, JIT, prompt, decision engine)
  providers/
    __init__.py        — PROVIDERS dict, exports all adapters
    base.py            — BaseProvider: resolve_binary, get_cmd, prepare_env, clean_output, run
    claude.py          — static default_cmd
    codex.py           — build_default_cmd() with SOLAR_WORKSPACE + CODEX_STATE_DIR
    agy.py             — Antigravity CLI (`agy -p`)
    agent.py           — build_default_cmd() with SOLAR_WORKSPACE

Automated tests live under `core/tests/skills/solar-router/` (framework-wide layout; see `core/AGENTS.md`).
```

**Layer contract:**
- `router.py` decides (context, prompt, policy, response shape).
- `providers/` executes (subprocess, env, normalization). No routing logic.
- `run_router.py` does I/O only. No logic.

## Required MCP

None

## Setup

```bash
# Configure router environment variables (SOLAR_ROUTER_*, timeouts, etc.)
bash core/skills/solar-router/scripts/onboard_router_env.sh
```

**Key environment variables:**
- `SOLAR_ROUTER_PROVIDER_PRIORITY` — Comma-separated provider list (e.g., `codex,claude,agy,agent,ollama`)
- `SOLAR_ROUTER_RUNTIME_DIR` — Where conversation history is stored (default: `<runtime root>/router`)
- `SOLAR_ROUTER_SYSTEM_PROMPT_FILE` — System prompt file path (default: `core/skills/solar-router/assets/system_prompt.md`)
- `SOLAR_ROUTER_CONTEXT_TURNS` — Number of conversation turns to include (default: `12`)
- `SOLAR_ROUTER_TIMEOUT_SEC` — End-to-end router timeout, including provider execution (default: `300`)

Optional command overrides:
- `SOLAR_ROUTER_CODEX_CMD`
- `SOLAR_ROUTER_CLAUDE_CMD`
- `SOLAR_ROUTER_AGY_CMD`
- `SOLAR_ROUTER_OLLAMA_CMD`

Ollama setup:
- `provider=ollama` always targets the local model named `solar`
- Build or refresh it with `bash core/skills/solar-router/scripts/setup_ollama.sh`

## Validation commands

```bash
# Validate skill structure
python3 core/skills/solar-skill-creator/scripts/package_skill.py core/skills/solar-router /tmp

# List configured providers (reads SOLAR_ROUTER_PROVIDER_PRIORITY)
bash core/skills/solar-router/scripts/list_providers.sh
bash core/skills/solar-router/scripts/list_providers.sh --exclude claude
bash core/skills/solar-router/scripts/list_providers.sh --exclude claude --format csv

# Diagnose router / preflight providers (native helper in this skill)
bash core/skills/solar-router/scripts/diagnose_router.sh --dry-run
bash core/skills/solar-router/scripts/diagnose_router.sh

# Full error output when a provider fails (e.g. 401, binary not found)
bash core/skills/solar-router/scripts/diagnose_router.sh --verbose

# Unit tests: router logic + provider adapters (centralized under core/tests; pytest runs unittest-style tests; no real AI calls)
uv run --project core/tests pytest core/tests/skills/solar-router -q
# Without uv: PYTHONPATH=core/skills/solar-router/scripts python3 -m unittest discover -s core/tests/skills/solar-router -p "test_*.py" -v

# Smoke tests: validate router contract v3, bridge delegation, execute_active.py JSON parsing
bash core/skills/solar-router/scripts/check_router.sh

# Live status: provider health, in-flight processes, last executions
bash core/skills/solar-router/scripts/status_router.sh
bash core/skills/solar-router/scripts/status_router.sh --last 20

# Close historical orphan audit records (append reconciled end events)
bash core/skills/solar-router/scripts/reconcile_router_audit.sh --dry-run
bash core/skills/solar-router/scripts/reconcile_router_audit.sh
```

## Router contract v3

### Input (stdin JSON)

```json
{
  "request_id": "string",
  "session_id": "string",
  "user_id": "string",
  "text": "string",
  "channel": "telegram|n8n|async-task|other",
  "mode": "auto|direct_only|async_only",
  "provider": "codex|claude|agy|agent|ollama|null",
  "metadata": {
    "agent": "agent-name|null",
    "skills": ["planet:skill-name", "core-skill-name"],
    "planet": "planet-name|null"
  }
}
```

- `provider`: optional. If set, strict mode — no fallback. If fails → `error_code: provider_locked_failed`.
- `mode`: defaults to `auto`. `direct_only` always returns `direct_reply`. `async_only` requires `async-tasks` feature enabled.
- `channel`: used by `DecisionEngine` for semantic routing in `mode=auto`.
- `metadata.agent`: existing agent name from planet's `agents/`, or `null` for JIT role generation.
- `metadata.skills`: skill name format — `planet:skill` resolves to `planets/<planet>/skills/<skill>/SKILL.md`; unprefixed `skill` resolves to `planets/<metadata.planet>/skills/<skill>/SKILL.md` first (if `metadata.planet` is set), then falls back to `core/skills/<skill>/SKILL.md`. Only description is injected (on-demand).
- `metadata.planet`: planet that owns the task domain. Used for agent/skill lookup.

## Secure Invocation Protocol (Required)

To prevent JSON parsing errors (invalid control characters, unescaped newlines), always use one of these two methods when calling the router from an AI agent or shell:

### Method A: Temporary JSON File (Recommended for Agents)

1. Use `write_file` to create a temporary JSON file (e.g., `<runtime root>/router/request_<id>.json`).
2. Ensure the `text` field contains explicit `\n` for newlines.
3. Execute the router piping the file: `python3 core/skills/solar-router/scripts/run_router.py < <runtime root>/router/request_<id>.json`.

### Method B: Heredoc with Single Quotes (Shell)

Use a heredoc with `'EOF'` (single quotes) to prevent the shell from interpreting backslashes or special characters:

```bash
cat << 'EOF' | python3 core/skills/solar-router/scripts/run_router.py
{
  "request_id": "my-id",
  "text": "Line 1\nLine 2",
  "channel": "other",
  "mode": "direct_only"
}
EOF
```

### Critical Rules:
- **Prefer escaped newlines** (`\n`) inside JSON strings for portability.
- **Escape double quotes** inside the `text` string as `\"`.
- **Validate JSON** before sending if using a custom script.

### Output (stdout JSON)

```json
{
  "status": "success|failed",
  "request_id": "string",
  "provider_used": "codex|claude|agy|agent|ollama",
  "reply_text": "string",
  "decision": {
    "kind": "direct_reply|async_draft_proposal|async_draft_created|async_activation_needed",
    "task_id": "string|null",
    "priority_suggested": "high|normal|low|null"
  },
  "error_code": "string|null",
  "error": "string|null"
}
```

## DecisionEngine rules

1. `mode=direct_only` → `decision.kind=direct_reply` always.
2. `mode=async_only` + `async-tasks` enabled → `decision.kind=async_draft_created`.
3. `mode=async_only` + `async-tasks` disabled → `status=failed` + explicit error.
4. `mode=auto` + `channel=async-task` → `decision.kind=direct_reply` (already in queue).
5. `mode=auto` + `channel=telegram|n8n|other` → AI decides semantically via structured JSON output.

## Consumers

- **solar-gateway:** `run_websocket_bridge.py` and HTTP webhook bridge call the router with full v3 contract.
- **solar-async-tasks:** `execute_active.py` (via `execute_active.sh`) calls the router with `channel=async-task`, `mode=direct_only`.

## Runtime files

- `<runtime root>/router/conversations/<user_id>.jsonl` — conversation history per user (for context continuity).
- Router audit rows in `state.sqlite` — one `start`/`end` pair per execution. Fields: `router_id` (internal UUID), `request_id` (caller ref), `user_id`, `metadata`, `provider`, `status`, `jit_generated`, `duration_ms`.

## References

- `references/routing-policy.md` — provider priority, env keys, repo-context policy, v3 contract rules.

## Managed execution

`managed_process.py` is an internal helper used by app and async executors to bound and cancel router process groups; it is not a separate provider entrypoint.
