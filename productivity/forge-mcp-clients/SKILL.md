---
name: forge-mcp-clients
description: Forge doctrine for using MCP servers as a client — opt-in, tiered, least-privilege. Use when a Boss needs an external tool grant or when installing/discussing an MCP server.
---

# Forge playbook — MCP-as-client doctrine (dormant, opt-in)

**Do not duplicate the config — defer to:** `config/orchestration/mcp-registry.json` (the server catalog)
and `config/orchestration/mcp-grants.json` (the per-Boss least-privilege matrix) as the single source of
truth for tiers, servers, and grants. This file is doctrine/orchestration only — it explains *how* to use
those configs correctly, it does not re-list every server or re-derive the matrix.

## Hard rules
- **Nothing here installs, connects to, or activates any MCP server.** The zero-dependency Forge default
  (fs/path only, no live network client) stays 100% intact until the owner explicitly opts a server in.
- A server is usable **only** when both are true: (1) the owner has opted it in (a marker naming the
  server id — see "Opt-in flow" below), **and** (2) the requesting Boss's grant covers it (tier + server
  id, per `mcp-grants.json`). Either condition failing means dormant → honest native fallback.
- **Tier 3 (WRITE-PRIMITIVE) is never auto-used.** Every tier-3 call routes through the existing
  `forge-actiongate.cjs` hard-gate classifier (the same one used for deploy/push/spend/DNS/etc.) — it is
  never bypassed and never reimplemented in parallel.
- Never claim an MCP tool ran, was available, or was opted in when it wasn't. Absence is reported as a
  labeled native fallback, not silently skipped.

## What "MCP-as-client" means here
Forge already ships one MCP artifact: `forge-bin/forge-mcp.cjs`, a **read-only server** that exposes this
project's own Forge run state (runs/events/reports/memory) to an external MCP host. That is Forge acting
as a *server* — unrelated to this skill.

This skill is the opposite direction: Forge (its Bosses) acting as an MCP **client**, consuming *external*
MCP servers (docs lookup, web search, browser automation, GitHub, etc.) as extra tools during a task. The
client side is deliberately **dormant by default** — a catalog and a validator, not a running connection.

## The 4 capability tiers (least-privilege)
| Tier | Class | Examples | Notes |
|------|-------|----------|-------|
| 0 | Read-only LOCAL | LSP/code-intelligence read (`serena-lsp`), local docs | No network call at all. |
| 1 | Read-only REMOTE | web search (`exa`), docs fetch (`context7`), scrape (`firecrawl`), GitHub read (`github-read`) | Network read, no writes; a credential (if any) is a read-scoped key only. |
| 2 | SANDBOXED action | browser-QA drive (`playwright`, `chrome-devtools`) | Can click/type/screenshot a page it navigates to — ephemeral browser state, never a project or repo write. |
| 3 | WRITE-PRIMITIVE | any MCP write (`github-write`, file write, deploy, publish) | Always routes through `forge-actiongate.cjs`; never granted by default to any Boss. |

Tiers and the full server catalog live in `config/orchestration/mcp-registry.json`. Every entry there
starts (and stays, until opted in) at `"status": "not-installed"` — `"active"` in that file is forbidden.

Two newer catalog entries (beginner-sweep vetting, 2026-09-24, both dormant/opt-in like everything else
here): `n8n-mcp` (czlonkowski/n8n-mcp, MIT) is tier 1 — read-only n8n node docs + `validate_workflow` for
forge-n8n, never a live n8n connection (that stays the separate, tier-3, owner-gated `n8n` entry).
`playwright` (microsoft/playwright-mcp, Apache-2.0) stays tier 2 — navigate/click/type/screenshot in a
sandboxed browser session is exactly the doctrine's tier-2 definition; an action with a real external
effect (a live form submission, a publish, a payment) is write-shaped and must be routed through
`forge-actiongate.cjs` like any other tier-3 write, never assumed covered by the tier-2 grant.

## Per-Boss least-privilege model
Each of the 12 permanent Bosses (`config/agents/agent-registry.json`) has a **max tier** and an explicit
**allow-list** of server ids in `config/orchestration/mcp-grants.json`. Both conditions are checked
independently — a Boss can never get a tool above its max tier, and never a server outside its allow-list,
even if one side alone would technically allow it. A Boss with no entry in that file defaults to
`max_tier: 0, allow_servers: []` (no grant at all — native fallback only); there is no implicit wide grant.

Current defaults (see `mcp-grants.json` for the authoritative, evolving list and the "why" per Boss):
search-boss and integration-boss get tier-1 docs/search; review-boss gets tier-1 read-only GitHub/docs;
test-boss and ui-boss get tier-2 sandboxed browser-QA; build-boss gets tier-0 local LSP only. No Boss gets
tier 3 by default — Boss, head-chef, seo-boss, security-boss, skill-boss, and docs-boss have no default
MCP grant at all in the current matrix.

## "mcp-write is a write-primitive" → hard-gate
A tier-3 MCP tool call (e.g. `github-write` creating a commit/PR, or any MCP tool that writes files,
deploys, or publishes) is treated exactly like `deploy`, `git-push`, `spend`, or `credential-rotate` in
`config/orchestration/hard-gates.json`. It is classified through the existing
`forge-actiongate.cjs::classify()` — **reuse that hard-gate, never duplicate its regex/logic** — and
requires an explicit per-use `owner_confirmed: true` before proceeding, regardless of autonomy level.
There is no separate "MCP write" bypass path; write is write.

## Defer-loading (token discipline)
Never pre-load every MCP tool schema for a task. A Boss that has a valid grant requests only the specific
tool(s) it needs for the current step via `ToolSearch` (or the equivalent narrow lookup), the same
discipline this project already applies to ECC/Codex/MCP loading generally (see the project's Token
Efficiency governance: "load only the tools needed for the current task; fetch deferred tool schemas on
demand"). A planner-style `planLoad()` step returns only the relevant tool(s) for the task at hand — never
the full catalog.

## Opt-in flow (dormant until the owner acts)
1. Nothing is active out of the box. `config/orchestration/mcp-registry.json` is a catalog, not a
   connection — every entry starts at `"status": "not-installed"`.
2. The owner opts a specific server in explicitly (naming its registry `id`). Until that marker exists for
   a given server id, that server stays dormant for every Boss, no matter what its grant would allow.
3. See `config/mcp/.mcp.json.example` in this project for a worked, DORMANT example of what opting one
   server in looks like end-to-end (host wiring + the explicit opt-in marker) — copy and adapt it, do not
   activate it by editing this skill.
4. Opting in a server does **not** widen any Boss's grant. Opt-in only makes a server *reachable*;
   `mcp-grants.json` still decides *who* may use it and at what tier.

## Requesting + validating a grant
Before a Boss calls any MCP tool it must validate, not assume, that it may:
1. Confirm the server id has been opted in (step 2 above) — if not, stop here and use the native fallback.
2. Look up its own entry in `config/orchestration/mcp-grants.json`: is the server id in its
   `allow_servers`, and is the server's tier (from `mcp-registry.json`) `<= max_tier`? Both must hold.
3. If the server is tier 3, additionally run it through `forge-actiongate.cjs::classify()` and require
   `owner_confirmed: true` before the call — no exception, even if steps 1–2 passed.
4. Only after all applicable checks pass does the Boss call the tool, and only the specific tool it needs
   (defer-loading, above) — never the server's full toolset just because access exists.
5. Log the outcome honestly: a real MCP call is reported as used; a denied/ungranted/not-opted-in request
   is reported as a labeled native fallback (see below), never silently absorbed into "it worked."

## Honest native fallback
When a server is absent, not opted in, or the requesting Boss's grant does not cover it, the Boss does
**not** stall the task — it falls back to its existing native capability (repo read, Claude's own
reasoning, WebSearch/WebFetch if separately available, manual QA, etc.) and **says so explicitly** in its
report: which server/tool was wanted, why it wasn't available (not opted in / grant denied / tier too
low), and what native path was used instead. Never claim an MCP tool ran, or imply a capability gap didn't
exist, when a fallback was actually used.

## Skills / commands / MCP
`config/orchestration/mcp-registry.json` (catalog), `config/orchestration/mcp-grants.json` (per-Boss
matrix), `forge-bin/forge-actiongate.cjs` (tier-3 hard-gate, reused not duplicated),
`config/mcp/.mcp.json.example` (dormant worked example — never a live `.mcp.json`).

## Fan-out & flow
No dedicated team — this is a cross-cutting doctrine every Boss consults inline before attempting an MCP
call. No fan-out of its own; it does not spawn agents.

## Ship-readiness (unique)
Zero-dep default provably unbroken (no new runtime dependency, no auto-started connection); every tier-3
attempt is provably routed through `forge-actiongate.cjs`; no Boss ever exceeds its `max_tier` or
`allow_servers`; every MCP absence is reported as a labeled native fallback, never silently dropped or
falsely claimed as success.
