---
name: logging
description: Structured logging conventions for DraftForge backend (Django/Celery/Daphne) and frontend (React). This skill should be used when adding log statements, creating new modules, debugging with logs, or reviewing logging patterns. Covers structlog usage, system/subsystem taxonomy, required fields, log levels, and Grafana query patterns.
---

# Structured Logging

DraftForge uses **structlog** (backend) for structured JSON logging exported to Grafana Cloud via OpenTelemetry. All logs use a `system`/`subsystem` taxonomy for filtering.

## Backend: Quick Start

```python
from telemetry.logging import get_logger
log = get_logger(__name__)

# Structured log — event name first, then kwargs
log.info("order_created", system="tournament", subsystem="registration", draft_id=5, user_id=42)
```

**Never use f-strings or `%` formatting in log messages.** The first argument is always an event name (snake_case). All context goes in kwargs.

## System / Subsystem Taxonomy

Every log MUST include `system` and `subsystem` kwargs. These are the primary Grafana filter dimensions.

> **Two-axis taxonomy:** `system` / `subsystem` answer *where the code lives* (single value, label-friendly). `tags: list[str]` is an optional secondary axis answering *what domains this log concerns* (multi-value, for cross-cutting queries like "show me everything related to signups"). When tags are set, also set `tags_csv` (comma-joined string) for clean LogQL `=~` filtering (Loki's `| json` flattens lists as `tags_0`, `tags_1` which is awkward to filter). Bind tags via `discord_log_context` for interaction-flow logs, or pass explicitly for one-off cross-cutting logs.

| system | subsystem | tags | Where | What |
|--------|-----------|------|-------|------|
| `herodraft` | `connection` | — | `consumers.py` | WS connect/disconnect, captain state, kicks |
| `herodraft` | `heartbeat` | — | `herodraft_tick.py` | Heartbeat staleness checks, heartbeat-triggered pauses |
| `herodraft` | `timer` | — | `herodraft_tick.py` | Tick loop lifecycle, tick broadcast, timeout auto-pick, resume |
| `websocket` | `heartbeat` | — | `consumers_base.py` | Heartbeat receive, captain register/unregister (generic WS infra) |
| `websocket` | `connection` | — | `telemetry/websocket.py` | Generic WS connect/disconnect/receive instrumentation |
| `herodraft` | `view` | — | `app/functions/herodraft_views.py` | HeroDraft HTTP actions: create, roll, choice/pick submit, abandon, reset |
| `celery` | `task` | — | `telemetry/celery.py` | Generic Celery task lifecycle bookends (started/completed/failed) |
| `events` | `discord` | — | `events/tasks.py` (cron sync, non-interaction tasks like `sync_discord_events`) | Cron-driven event sync to Discord that isn't triggered by an interaction |
| `events` | `scheduling` | — | `events/tasks.py` | Event generation, signup opening, repeaters |
| `tournament` | `discord` | — | `discordbot/tasks.py` | Tournament DMs, bracket notifications |
| `avatars` | `endpoint` | — | `user/internal/avatar.py` | Internal endpoints: list-linked-users, list-guild-ids, bulk-update + invalidate |
| `avatars` | `refresh` | — | `app/tasks/avatar_refresh.py::refresh_avatars_batched` | Daily Celery beat: read guild-member cache, diff against DB, POST bulk-update |
| `avatars` | `single` | — | `app/tasks/avatar_refresh.py::refresh_single_user_avatar` + helpers | Single-user refresh: Discord API fetch + per-user `update_user_avatar` |
| `avatars` | `legacy` | — | `app/tasks/avatar_refresh.py::refresh_discord_avatars` / `refresh_all_discord_data` | Older per-user fanout tasks (predates the batched path) |
| `discord` | `lease` | — | `discordbot/tasks.py`, `app/views/internal.py` | DiscordMessageLog stale-lease sweep (pending NULL >5min, failed >1h) |
| `discord` | `interaction` | `["events","signup"]` | `discordbot/components.py`, `discordbot/signup_responses.py`, `discordbot/log_context.py` | Discord-bot UI plumbing + response delivery: button/modal/select callbacks |
| `discord` | `dispatch` | `["events","signup"]` | `events/discord/dispatch.py` | `notify_*` dispatch visibility (queued vs skipped); threads `interaction_id` to Celery |
| `discord` | `celery` | `["events","signup"]` | `events/tasks.py` (Discord-dispatching tasks) | `celery_task_started/finished/failed` bookend logs |
| `cache` | `invalidate` | — | `app/cache_utils.py` | Per-object cacheops invalidation fired from `transaction.on_commit` |
| `websocket` | `broadcast` | — | `app/broadcast.py` | Draft / herodraft event + state broadcast to channel groups (`kind` field distinguishes draft/herodraft/herodraft_state) |
| `auth` | `internal` | — | `app/auth.py` | Internal-service auth (X-Internal-Token): IP-allowlist rejects, invalid-token failures |
| `auth` | `social` | — | `app/pipelines.py` | Discord OAuth social-auth pipeline: account reclaim/merge, username matching |
| `auth` | `merge` | — | `app/discord_accounts.py` | Discord account de-dup / merge |
| `tournament` | `draft`, `registration`, `user` | — | `app/models.py`, `app/functions/tournament.py` | Draft build/pick/rebuild, captain/team registration, per-user avatar refresh |
| `api` | `serializer`, `routing`, `main`, `csv_import`, `joke` | — | `app/serializers.py`, `app/views*.py`, `app/views/csv_import.py`, `backend/urls.py` | DRF serializer mutations, view cache-miss, CSV import, env/routing |
| `user` | `functions` | — | `app/functions/user.py` | Profile-update request/validate/apply |
| `app` | `signals` | — | `app/signals.py` | Model signal handlers (org/league user create, herodraft cleanup) |
| `internal_client` | `http` | — | `app/internal_client/__init__.py` | Internal HTTP client JSON-parse failures |
| `discord` | `bot`, `utils`, `views`, `channels`, `roles`, `users` | — | `discordbot/**` | Bot lifecycle, message utils, slash views, channel/role/user services |
| `events` | `tasks`, `services`, `views`, `dispatch` | — | `events/**` | Event task lifecycle, signup services, manual fire, tournament-link dispatch |
| `steam` | `api`, `game_linking`, `match`, `mmr`, `stats`, `model`, `league_sync`, `retry` | — | `steam/**` | Steam API, account/game linking, match fetch/store, MMR/stats, league sync, retry |
| `bracket` | `generate`, `model` | — | `bracket/**` | Bracket generation + model-level cache logging |
| `org` | `views` | — | `org/views.py` | Org admin actions (user delete/merge) |
| `common` | `utils` | — | `common/utils.py` | Shared utility warnings (CI/IP detection) |

Add new systems/subsystems as features grow. Keep systems coarse (feature area), subsystems functional (what role the code plays).

## Cross-System Correlation

Logs that span multiple systems carry an `interaction_id` (Discord interaction) or `request_id` (web request) so a single user action can be traced across processes.

For Discord interactions, the `discord_log_context` async CM in `discordbot/log_context.py` binds:
- `interaction_id` — primary correlation key (Discord-generated, unique per click)
- `discord_user_id`, `discord_username`, `channel_id`, `guild_id`
- `custom_id`, `event_id`, `interaction_type`
- `tags=["events","signup"]` (or other prefix-derived tags)
- `tags_csv="events,signup"` (flat string for clean LogQL filtering)

These propagate via `structlog.contextvars.merge_contextvars` through `await` and `sync_to_async`. They also propagate across Celery `.delay()` calls when the dispatch site passes `interaction_id` as a kwarg and the task calls `bind_contextvars(interaction_id=...)` at entry.

OTel `trace_id` and `span_id` are injected automatically by the `_add_otel_trace_context` processor in `telemetry/logging.py`. At a 10% sample rate, the `trace_id` is in every log line for that 10%; for the other 90%, rely on `interaction_id` for log-side correlation.

### Grafana query patterns

```logql
# Single user click
{service_name="backend"} | json | interaction_id="<id>"

# Cross-cutting: anything signup-related
{service_name="backend"} | json | tags_csv=~".*signup.*"

# Discord code that touches events
{service_name="backend"} | json | system="discord" | tags_csv=~".*events.*"
```

## Log Levels

| Level | When | Exported to Grafana? |
|-------|------|---------------------|
| `DEBUG` | Per-request/per-tick detail, heartbeat received | No (prod=INFO) |
| `INFO` | State transitions, lifecycle events, periodic health | Yes |
| `WARNING` | Anomalies that self-recover (stale heartbeat, slow tick) | Yes |
| `ERROR` | Failures requiring attention (broadcast failed, API error) | Yes |

## Required Fields

Beyond `system` and `subsystem`, include relevant entity IDs:

- `draft_id` — for anything draft-related
- `user_id` / `username` — for user-scoped actions
- `event_id` — for event system logs
- `duration_s` / `elapsed_ms` — for timing-sensitive operations
- `reason` — for skipped/stopped/failed actions
- `error` — for exception context (`str(e)`, never the full traceback)

## References

- Backend patterns (structlog config, OTel export, Celery/Daphne logging, middleware): [references/backend.md](references/backend.md)
- Frontend console logging conventions: [references/frontend.md](references/frontend.md)
- Querying/parsing logs from the CLI with `gcx` (error breakdown, mixed JSON+plain-text, silence detection, request/trace correlation): [references/grafana-loki.md](references/grafana-loki.md)

## Grafana Queries

```logql
# All herodraft heartbeat logs
{service_name="backend"} | json | system="herodraft" | subsystem="heartbeat"

# Slow ticks
{service_name="backend"} | json | event="tick_slow"

# All errors across systems
{service_name="backend"} | json | level="error"

# Filter by draft
{service_name="backend"} | json | draft_id="42"
```

Run these from the CLI with `gcx` (context `draftforge` → kettle.grafana.net). **Pass
`--agent=false`** or Claude Code's auto agent-mode suppresses the output:

```bash
gcx logs query '{service_name="backend"} | json | level="error"' --since 24h -o raw --agent=false
```

The `discord` service mixes structlog JSON with plain-text `discord.py` lines, so `| json`
drops half of them — use line filters (`|= "ERROR"`) there. Full examples (error breakdown,
silence detection, request/trace correlation): [references/grafana-loki.md](references/grafana-loki.md).
