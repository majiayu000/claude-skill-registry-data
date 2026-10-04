---
name: solar-gateway
description: >
  HTTP webhook and WebSocket entry point for external integrations (n8n, Telegram).
  Delegates to solar-router. Not Solar App UI (`solar-app` on :9000).
---

# Solar Gateway

## Purpose

Provide a reusable local transport layer for Solar:
- receive inbound messages over WebSocket,
- process request/response loop in one place,
- keep channel adapters decoupled from runtime transport,
- manage Telegram webhook operations from this same skill.

## Scope

- Run local WebSocket server for bidirectional messaging.
- Run local HTTP webhook bridge with channel routes (`/webhook/<channel>`).
- Define stable message contract for channel adapters.
- Keep implementation lightweight and deterministic.

## Required MCP

None

## Dependencies

- **solar-router:** This skill depends on `solar-router` for AI provider execution. Ensure `solar-router` is configured first:
  ```bash
  bash core/skills/solar-router/scripts/onboard_router_env.sh
  bash core/skills/solar-router/scripts/diagnose_router.sh
  ```

## Validation commands

```bash
# One-command setup (recommended)
bash core/skills/solar-gateway/scripts/setup_transport_gateway.sh

# Restart after .env changes (stop owned runtime + start; runs preflight first)
bash core/skills/solar-gateway/scripts/setup_transport_gateway.sh --restart

# Dry-run stop (ownership report; no kill)
bash core/skills/solar-gateway/scripts/stop_transport_gateway.sh --dry-run

# Stop owned processes (--force kills foreign blockers; --tunnel-only skips bridges)
bash core/skills/solar-gateway/scripts/stop_transport_gateway.sh
bash core/skills/solar-gateway/scripts/stop_transport_gateway.sh --tunnel-only

# Validate skill quality and structure
python3 core/skills/solar-skill-creator/scripts/package_skill.py core/skills/solar-gateway /tmp

# Bootstrap .env block for this skill
bash core/skills/solar-gateway/scripts/onboard_websocket_env.sh

# Validate runtime prerequisites
bash core/skills/solar-gateway/scripts/validate_websocket_bridge.sh

# Preflight AI providers
bash core/skills/solar-router/scripts/diagnose_router.sh --dry-run
bash core/skills/solar-router/scripts/diagnose_router.sh
bash core/skills/solar-router/scripts/list_supported_providers.sh

# Check runtime health — local HTTP + named-tunnel connector /ready (exit 0/1/2).
# Public hostname curl from the origin host is informational (hairpin).
bash core/skills/solar-gateway/scripts/check_transport_gateway.sh

# Ensure gateway is healthy, recover if not (used by solar-system orchestrator)
# Drift-first: env stamp mismatch → preflight → setup --restart
# Partial without drift → tunnel-only; partial with drift → full restart
bash core/skills/solar-gateway/scripts/ensure_transport_gateway.sh

# Smoke: priority change → ensure → new process env (restores .env afterward)
bash core/tests/skills/solar-gateway/smoke_priority_ensure.sh

# Unit lifecycle tests (OWNER, fingerprint, preflight, rollback)
bash core/tests/skills/solar-gateway/test_gateway_lifecycle.sh

# n8n auth / async poll tests
uv run --project core/tests python -m pytest core/tests/skills/solar-gateway/test_http_n8n_auth.py -q

# Register and verify Telegram webhook (OWNER=solar only; fails if OWNER=external)
bash core/skills/solar-gateway/scripts/set_telegram_webhook.sh
bash core/skills/solar-gateway/scripts/verify_telegram_webhook.sh

# Configure stable named tunnel (recommended for production)
bash core/skills/solar-gateway/scripts/configure_named_tunnel.sh

# Direct runtime check without local .venv
uv run --with websockets==12.0 python3 -c "import websockets; print(websockets.__version__)"

# Sync core changes to local clients
solar client sync
```

## Lifecycle (stop / setup / ensure)

- **No listener reuse:** setup fails if WS/HTTP ports are busy unless `--restart`.
- **Stop** is the only kill path: ownership via bridge cmdline signatures + port/pid file; tunnel via `cloudflared.pid` + cmdline (no global cloudflared scan).
- **Env stamp** lives at `$SOLAR_WORKSPACE/<runtime root>/gateway/env.stamp` (fingerprint of an allowlisted key set — not `.env` mtime). Missing stamp with live Solar bridges counts as drift.
- Fingerprint includes `SOLAR_GATEWAY_CLAIM_TELEGRAM` and a derived `SOLAR_N8N_WEBHOOK_SECRET_SHA256` (never the secret in plaintext). Rotating the secret or changing the claim flag triggers drift → `ensure` restart.
- **HTTP channels** (`SOLAR_HTTP_WEBHOOK_BASE/<channel>`): `n8n` always; `telegram` when `TELEGRAM_BOT_TOKEN` is set. Distinct from Bot API claim.
- **Telegram claim** (`SOLAR_GATEWAY_CLAIM_TELEGRAM=true|false`, absent = do not claim):
  - `false` or absent: setup/ensure skip `setWebhook` (exit 0). Outbound `sendMessage` is still allowed.
  - `true`: register Solar's URL only when `getWebhookInfo` is empty or already Solar. A foreign URL is never claimed; setup continues (no rollback).
  - No `SOLAR_TELEGRAM_WEBHOOK` / `OWNER` fallback.
- **n8n auth** (`SOLAR_N8N_WEBHOOK_SECRET`): required. `POST /webhook/n8n` uses `Authorization: Bearer`. Unset secret → fail-closed `401`. Missing header → `401`; wrong token → `403` (constant-time compare). Generate with `openssl rand -base64 32`. HTTP 202 / `GET /webhook/n8n/result` are not part of the production contract.
- **Drift / restart** runs a **non-destructive preflight** before stopping a healthy runtime. Preflight failure writes `env.fail` and leaves processes running. Provider tokens are validated against solar-router `PROVIDERS` (via `list_supported_providers.sh`), not a duplicated list. Invalid `SOLAR_GATEWAY_CLAIM_TELEGRAM` (not `true|false` or absent) fails preflight.
- **Backoff:** repeated failures with the same fingerprint are throttled via `env.fail` (exponential, capped at `GATEWAY_BACKOFF_CAP_SEC`, default 15 min). Configuration failures (`preflight_failed*`, `setup_failed`, `stop_failed`, `ports_busy_after_stop`) count toward `GATEWAY_FAIL_ATTEMPTS_CAP` (default 5). After that many with the same fingerprint, ensure **stops retrying** until the fingerprint changes (fix `.env` or remove `env.fail`). A fingerprint change resets that backoff. `tunnel_recovery_failed` does not count toward the cap and never takes that hard stop: it only uses the capped backoff. An older `env.fail` already exhausted with that reason is retried on the next ensure when preflight passes, without deleting the file by hand.
- **Tunnel grace:** while `cloudflared` is still running and only the connector is down, ensure leaves it to reconnect for `GATEWAY_TUNNEL_RESTART_GRACE_SEC` (default 300 s) before restarting it. A healthy check clears that clock, so the next outage of the same process gets a fresh grace.
- **mkdir-lock** (portable, no `flock`) at `<runtime root>/gateway/lock/` serializes ensure/setup/stamp writes. Distinct from the solar-system orchestrator lock. Dead or recycled lock PIDs are reclaimed.

## Runtime requirements

- `uv`
- Python dependency resolved at runtime by `uv`: `websockets==12.0`
- At least one AI client CLI in `PATH`:
  - `codex`, `claude`, `agy`, or `agent`
- Local runtime write access for conversation memory (default: `<runtime root>/router/`)

## System activation (via solar-system)

For host-level orchestration through one LaunchAgent, enable this feature in:

```dotenv
# [solar-system] required environment
SOLAR_SYSTEM_FEATURES=transport-gateway
```

Telegram / n8n gateway (examples):

```dotenv
# n8n owns the Telegram webhook (this host). Absent or false: do not claim.
# SOLAR_GATEWAY_CLAIM_TELEGRAM=false
SOLAR_N8N_WEBHOOK_SECRET=<openssl rand -base64 32>
# Solar registers /webhook/telegram only when getWebhookInfo is empty or already Solar:
# SOLAR_GATEWAY_CLAIM_TELEGRAM=true
```

Or combined with async tasks:

```dotenv
SOLAR_SYSTEM_FEATURES=async-tasks,transport-gateway
```

Then install/update Solar LaunchAgent:

```bash
bash core/skills/solar-system/scripts/install_launchagent_macos.sh
```

## Laptop runtime note (optional)

- This skill can expose long-running local runtime endpoints (webhook/bridge/server/tunnel).
- If the active host is a laptop, host sleep can stop the runtime and break reachability.
- This is a host operations concern, not a mandatory dependency of the skill.
- If multiple laptops are used, only one active host should serve the same public webhook route at a time.

## Workflow

1. Run `setup_transport_gateway.sh` as default end-to-end flow (writes `env.stamp` on success; prints `http_channels=` and `telegram_claim=`).
2. After editing watched `.env` keys (including `SOLAR_GATEWAY_CLAIM_TELEGRAM` or n8n secret), either wait for the next `ensure_transport_gateway.sh` tick or run `setup_transport_gateway.sh --restart`.
3. Preview stop candidates with `stop_transport_gateway.sh --dry-run` before a manual restart.
4. If needed, run `setup_transport_gateway.sh --prepare-only` to stop before long-running services.
5. For stable DNS, configure named tunnel with `configure_named_tunnel.sh` and set `SOLAR_TUNNEL_MODE=named`.
6. With `SOLAR_GATEWAY_CLAIM_TELEGRAM` absent/`false` (or a foreign URL already present), setup does **not** register the Telegram webhook.
7. All AI execution and routing policy is delegated to **solar-router** (`core/skills/solar-router/scripts/run_router.py`). This skill does not select providers or implement fallback.
8. Use individual scripts only for troubleshooting or partial reconfiguration.

## Dependency policy

- This skill must not create or rely on an in-repo `.venv`.
- Runtime Python dependencies are executed directly with `uv run --with ...`.
- Install `uv` once on the host, for example `brew install uv`.

## Conversation continuity

Managed entirely by `solar-router`. See skill `solar-router` for details.

## Message contract (v3)

This skill is a **pure delegate** to `solar-router`. No provider selection, no fallback, no async policy here.

Inbound `request` (WS bridge):
- `type`: `request`
- `request_id`: unique id (`channel:conversation_id:message_id` when composed by the HTTP bridge)
- `session_id`: continuity key (`channel:conversation_id`); the router keys history by it, falling back to `user_id` only when empty
- `user_id`: user identifier
- `text`: user message
- `channel`: `telegram|n8n|async-task|other` (set by HTTP bridge before forwarding)
- `mode`: `auto|direct_only|async_only` (set by HTTP bridge based on caller)
- `provider`: optional — if set, strict mode in router (no fallback)

Outbound `response` (WS bridge — router v3 JSON + envelope):
- `type`: `response`
- `request_id`: mirrors inbound id
- `status`: `success|failed`
- `provider_used`: provider that responded
- `reply_text`: generated reply text
- `decision.kind`: `direct_reply|async_draft_created|async_activation_needed|async_draft_proposal`
- `decision.task_id`: task id if async draft was created
- `error_code`: optional, for consumer routing
- `error`: human-readable error detail

HTTP bridge channel mapping:
- Telegram inbound → `channel=telegram`, `mode=auto` (only when Solar registered the webhook)
- n8n inbound → `channel=n8n`, `mode=auto`; require `Authorization: Bearer` (`SOLAR_N8N_WEBHOOK_SECRET`). Unset secret → fail-closed `401`
- n8n message identity: n8n sends `channel` (platform, e.g. `telegram`), `conversation_id` and `message_id`; the bridge composes `session_id` and `request_id` and never splits them. Partial parts, a malformed `channel` or a conflicting `session_id` are rejected before the replay ledger and not stored. The legacy body (`request_id`, `session_id`, optional `chat_id`) is still accepted. See `references/message-contract.md`
- Telegram direct inbound composes `request_id = telegram:<chat>:<message_id>`
- n8n production contract: one synchronous `POST /webhook/n8n`. HTTP 202, `SOLAR_N8N_DEFAULT_ASYNC`, and `GET /webhook/n8n/result` return `status: failed` (no poll)
- n8n response: router v3 JSON exposed directly (no legacy double-wrapper). Replay uses `$SOLAR_GATEWAY_RUN_DIR/n8n-jobs/`

## References

- `references/message-contract.md`
- Routing policy: `core/skills/solar-router/references/routing-policy.md`
- `references/telegram-webhook-flow.md`
