---
name: opencode-v2-migration-skill
description: >-
  Detect OpenCode v1 installs and triage migration to v2 — version probe,
  V1 config/plugin/agent-shape detection, native-v2 field mapping, then
  delegate execution to opencode-v2-migration-subagent. Triggers: migrate
  opencode to v2, v1 to v2, opencode v2 upgrade, still on v1, tui.json
  cleanup, v1 config check.
license: Apache-2.0
compatibility: opencode
metadata:
  harness: "opencode"
  protocol: opencode-migrate-v1-to-v2
  pattern: detect-then-delegate
category: OpenCode Meta
---

# OpenCode v1 → v2 Migration

Frontend for migrating an end user's OpenCode v1 setup to v2: detect what is
V1, decide the migration scope, then delegate execution to
`opencode-v2-migration-subagent` (which carries the full field-mapping tables).

**Source of truth:** <https://opencode.ai/v2/docs/migrate-v1/> — re-fetch
before acting; v2 is evolving. Never use `opencode.ai/docs/...` (V1 docs).

## Phase 1 — Detection

### Version + migration-state probes (v2 HTTP API)

```bash
opencode --version                                   # v1.x = V1 client; v2.x = V2
opencode service status                              # v2-only command; failing ⇒ no v2 service
opencode api get /api/status                         # v2 server status (v1 clients lack `api`)
opencode api get /api/experimental/migration/v1      # v2's built-in V1-migration status report
```

`/api/experimental/migration/v1` is the authoritative in-product probe — it
reports what the v2 server still detects as V1-shaped. Full API surface:
<https://opencode.ai/v2/docs/api/> (OpenAPI at `/openapi.json` on any running
server); TypeScript client: `@opencode/client`.

### V1 artifact signals

Check each; every hit is a migration item:

| Signal | Where | v2 destination |
|---|---|---|
| `tui.json(c)` | `~/.config/opencode/`, project | `~/.config/opencode/cli.json` (auto-migrated on first v2 TUI start; verify) |
| `permission` map, legacy top-level `tools` (deprecated) | any config JSON | ordered `permissions` array (`bash`→`shell`, `task`→`subagent`, `write`/`patch`→`edit`) |
| `agent` / `provider` / `command` / `plugin` / `reference` (singular) | config JSON | `agents` / `providers` / `commands` / `plugins` / `references` |
| `prompt`, `disable`, `variant`, top-level `temperature` | agent entries + `.md` frontmatter | `system`, `disabled`, `model#variant`, `request.body.temperature` (auto-translated — optional) |
| `mcp` direct server map, `enabled` | config JSON | `mcp.servers` + inverse `disabled`. **Two stub traps:** (1) V1 enable-only stubs (`{"<name>": {"enabled": true}}`, no `type`) are silently **omitted** by v2; (2) project-level "enable the global one" overrides must be **full entries** — v2 replaces `mcp.servers.<name>` atomically, so a bare `{"disabled": false}` stub yields an inert server. Copy the transport (type/command/env) from the global entry and set `disabled: false` |
| V1 TUI plugin in `cli.json` (`tui:` async-function export) | `~/.config/opencode/cli.json` | v2 CLI plugins need `Plugin.define({id, setup})` via `@opencode/plugin/tui` (or a `./tui` package export) — see the [CLI plugin guide](https://opencode.ai/v2/docs/build/plugins/cli/). Remove V1-only entries (watch-list) until upstream ports |
| `agent/`, `mode/`, `command/`, `skill/`, `plugin/` dirs | `.opencode/` | `agents/`, `agents/` + `mode: primary`, `commands/`, `skills/`, `plugins/` (old dirs still discovered) |
| V1 plugin code | `plugins` array entries | **does not run on v2** — port per the [plugin migration guide](https://opencode.ai/v2/docs/build/plugins/migrate-v1/) or drop |
| `autoupdate`, `small_model`, `enabled_providers` | config JSON | `update`, `agents.title.model`, internal policies (normalized silently) |
| `lsp` config expecting diagnostics | config JSON | **v2 accepts but never runs language servers** — use lint/typecheck commands |
| `instructions` field | config JSON | accepted but **not loaded** — move content to `AGENTS.md` |
| Global config named `config.json` | `~/.config/opencode/` | rename to `opencode.json` — v2 only reads `opencode.json(c)` |
| `/global/health` healthchecks | scripts, compose files | `/api/health` |
| Scripts/integrations calling the V1 server API (curl, SDK) | scripts, CI, apps | v2 HTTP API (`/api/*`, breaking) — port to `opencode api`, `@opencode/client`, or the new endpoints; see the [API reference](https://opencode.ai/v2/docs/api/) |

### Also probe

- `~/.local/share/opencode/log/opencode.log` for `failed to load plugin`
  (every V1-API plugin logs this on v2) — classify each: native-v2 replacement
  exists / port locally / drop.
- Ancestor configs (`~/opencode.json` etc.) — v2 merges every
  `opencode.json(c)` from cwd up to `/`; forgotten layers cause "phantom" MCP
  entries. Surface them in the report.

## Phase 2 — Triage

| Finding | Action |
|---|---|
| Already v2, all-v2 shapes | Report clean; optionally convert remaining V1-syntax fields to native v2 (behavior-preserving; coexistence is supported) |
| v2 client, V1-shaped files | In-place migration of config + agent/command frontmatter (mostly optional — v2 auto-translates); **plugins must be ported or dropped**; run the verification gate |
| v1 client | Install v2 (V2 installer replaces the V1 binary), then migrate files, then verify |

## Delegation

Delegate execution to `opencode-v2-migration-subagent` with a detection
payload (extract-then-delegate — do not paste this skill into the prompt):

```
version: <v1.x|v2.x>
findings: <the Phase 1 signal table, filled in>
plugins_failed: <names from the log probe, with disposition candidates>
user_intent: <convert-to-native-v2 | keep-v1-syntax | full-migrate>
constraints: <shared/global config? Docker mode? CI?>
```

The subagent owns the mapping tables, plugin triage rubric, and the
Return Contract report.

## Verification gate (post-migration, non-negotiable)

1. `opencode service restart` — the running service caches config; stale
   services lie.
2. `opencode mcp list` — every expected server connected or intentionally
   disabled; zero unexplained failures.
3. Log grep for `failed to load plugin` — remaining entries must each have a
   documented keep/drop rationale (exact-version pins do NOT auto-upgrade —
   a pinned V1 plugin stays broken even after its author ships v2).
4. Smoke one agent prompt + one MCP tool call.

## References

- Migration guide: <https://opencode.ai/v2/docs/migrate-v1/>
- Plugin migration: <https://opencode.ai/v2/docs/build/plugins/migrate-v1/>
- v2 config: <https://opencode.ai/v2/docs/config/>
- CLI config (cli.json): <https://opencode.ai/v2/docs/cli/config/>
- Troubleshooting: <https://opencode.ai/v2/docs/troubleshooting/>
- HTTP API reference: <https://opencode.ai/v2/docs/api/> (OpenAPI: `/openapi.json`; V1-migration status: `/api/experimental/migration/v1`)
- Client SDK: <https://opencode.ai/v2/docs/build/client/>
- Docs index: <https://opencode.ai/v2/llms.txt>
