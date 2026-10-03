---
name: anthropic-routines
last_updated: 2026-05-17
description: "How to write a Beamix Routine .md file: required frontmatter fields (schedule, routine_id_env_key, budget, trust-spec parsing), body conventions, and MCP grant patterns. Use when authoring or refining any file under .claude/agents/_routines/."
tags: [orchestration, beamix-specific, agents, routines]
source: beamix-authored 2026-05-16
risk: low
---

# Anthropic Routines

## Quick reference

> Routines are triggers, not durable executors. Inngest owns durability. Always include `budget` + `routine_id_env_key` in frontmatter.

## When to use

- Authoring a new Routine .md file under `.claude/agents/_routines/`
- Refining an existing Routine's frontmatter or operating procedure
- Debugging why a Routine did not fire on its cron schedule
- Understanding how a Routine receives and validates a trust spec

## When NOT to use

- For interactive C-suite agents (they use the standard agent schema, not Routine schema)
- For worker agents (workers are spawned via Task, not via `/fire`)

## What a Routine is

A Routine is an agent that runs on a cron schedule OR is fired on-demand via Anthropic's `/fire` endpoint. It starts a fresh main thread each invocation. It has no persistent state between runs — state lives in Mem0, DECISIONS.md, and Supabase.

Routines are triggers + orchestrators. They are NOT durable executors. Inngest owns durability.

## Required frontmatter

```yaml
---
name: cto-daily-plan
description: "Reads open Linear tickets + overnight code activity, drafts a prioritized engineering plan, posts to war-room project. Fires daily at 10:30 UTC."
when_to_use: |
  - Fires automatically at 10:30 UTC via cron schedule
  - Can be manually fired via /fire for an on-demand engineering plan
  - Triggered by Inngest timeout-watcher if previous run timed out
schedule: "30 10 * * *"           # cron expression (UTC)
routine_id_env_key: ROUTINE_CTO_DAILY_PLAN_ID
routine_token_env_key: ROUTINE_CTO_DAILY_PLAN_TOKEN
model: claude-sonnet-4-6           # or claude-opus-4-7 for depth Routines
tools: [Read, Write, Edit, Bash, Glob, Grep, Task]
maxTurns: 25
color: blue                        # matches CTO color
isolation: none                    # Routines share no worktrees
mcpServers:
  - linear
  - github
  - supabase
  - mem0
skills:
  - war-room-orchestration
  - linear-mvp-recipe
  - writing-plans
budget:
  max_cost_usd: 2.0
  max_runtime_minutes: 20
  max_tool_calls: 100
delivery:
  channel: linear-comment
  project: war-room
  ticket_prefix: BMX-W              # war-room tickets use W prefix
trust_spec_parsing: true            # this Routine accepts inbound trust specs
escalates_to: ceo                   # on BLOCKED or over-budget
---
```

## Fields reference

| Field | Required | Notes |
|-------|----------|-------|
| `schedule` | Yes (for cron Routines) | Standard cron expression, UTC |
| `routine_id_env_key` | Yes | Env var name storing the Routine ID. Value set via Wrangler secrets. |
| `routine_token_env_key` | Yes | Env var name storing the per-Routine bearer token. |
| `model` | Yes | `claude-sonnet-4-6` default. `claude-opus-4-7` for advisor/synthesis Routines. |
| `budget.max_cost_usd` | Yes | Hard ceiling. Inngest runaway-watcher enforces this. |
| `budget.max_runtime_minutes` | Yes | Inngest timeout-watcher fires Auto-Unblock if exceeded. |
| `trust_spec_parsing` | Conditional | Set `true` if this Routine can receive an inbound trust spec via `/fire`. Must validate HMAC. |
| `delivery.channel` | Yes | Where the Routine posts its output: `linear-comment`, `slack`, `telegram`. |

## Routine body structure

All Routines follow the same 6-section body:

```markdown
# <Routine Name> — <Tagline>

## Identity & mission
## Schedule & triggers
## Pre-flight reads      (files to read at the start of every run)
## Operating procedure   (numbered steps)
## Trust spec handling   (if trust_spec_parsing: true)
## Return format         (what the Routine posts and where)
```

## Trust spec handling section (mandatory if trust_spec_parsing: true)

```markdown
## Trust spec handling

When fired via `/fire` with a trust spec in the payload:

1. Extract spec from `---BEAMIX-SPEC-V1-START---` / `---BEAMIX-SPEC-V1-END---` sentinels
2. Verify HMAC signature against `BRIDGE_HMAC_SECRET` env var
3. Verify `nonce` not seen before (read KV or fail-open with audit_log row)
4. Verify `expires_at > now()`
5. Verify `issued_by.linear_user_id` ∈ `ALLOWED_ISSUERS` env list
6. Write `audit_log` row: status=accepted
7. Execute the scoped task from `scope.intent` + `scope.constraints`
8. Write `audit_log` row: status=complete (or blocked)

If any verification step fails: write audit_log row status=rejected, post Linear comment with reason, exit.
```

## Standing Routines roster

| Routine | Schedule (UTC) | Model |
|---------|---------------|-------|
| `advisor-daily-thinking` | 05:30 daily | Opus |
| `morning-digest` | 05:30 daily | Sonnet |
| `competitor-pulse` | 05:30 daily | Sonnet |
| `geo-algorithm-signal` | 05:30 Sundays | Opus |
| `cto-daily-plan` | 10:30 daily | Sonnet (Opus for plan depth) |
| `content-idea-generator` | 10:30 daily | Sonnet |
| `monday-standup` | 10:30 Mondays | Sonnet |
| `friday-retro` | 15:30 Fridays | Sonnet |
| `eod-sync` | 20:30 daily | Sonnet |
| `auto-unblock` | Event-triggered (timeout) | Sonnet |
| `synthesizer` | Event-triggered (board R3) | Opus |

## See also

- `war-room-orchestration` — [[war-room-orchestration]]
- `trust-spec-contracts` — [[trust-spec-contracts]]
- `linear-mvp-recipe` — [[linear-mvp-recipe]]
- `board-meeting-protocol` — [[board-meeting-protocol]]

## Anti-patterns

- Hardcoding the Routine ID or token in the .md file (use env var name, not value)
- Omitting `budget` fields — Inngest runaway-watcher cannot enforce without them
- Setting `trust_spec_parsing: true` without implementing the HMAC verification steps
- Posting output to main product Linear project (Routines post to war-room or strategy projects)
- Using `schedule` in local timezone — always UTC
- Awaiting a downstream Routine's completion inline (fire-and-forget only; completion via Inngest fan-in)
