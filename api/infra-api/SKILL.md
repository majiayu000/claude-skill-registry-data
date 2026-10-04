---
name: infra-api
description: Manage AICP's API surfaces — LocalAI's OpenAI-compatible REST API (proxied at `localhost:8090/v1/*`), AICP's MCP tool surface (~64 tools, 21 deprecated per audit), AICP CLI commands (~100 flags), agent server REST API (when activated via `--agent <port>`), planned fleet RPC. Includes contract design, versioning, deprecation, OpenAPI schema generation. Loads when the operator says "design a new API endpoint" / "version the API" / "deprecate API X" / "OpenAPI schema" / "contract change for fleet integration".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# infra-api

Manage AICP's API surface design + lifecycle. AICP exposes 4 distinct
API surfaces:

1. **LocalAI REST API** — OpenAI-compatible `/v1/chat/completions`, `/v1/embeddings`,
   `/v1/audio/*`, etc., on `localhost:8090`. AICP proxies but doesn't define
   this contract — LocalAI does.
2. **MCP tool surface** — currently 64 tools (21 deprecated per audit), accessed
   via stdio transport. Per the MCP audit, the surface is being trimmed to
   inference + KB + fleet (47 KEEP) with operational ones moving to CLI.
3. **AICP CLI** — ~100 flags (per `aicp --help`), the operator-facing command surface
   that follows the Gateway Output Contract per the contract-adoption decision.
4. **Agent server REST API** — activated by `aicp --agent <port>`, exposes task
   submission/status for fleet coordination.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "design a new API endpoint", "version the API", "deprecate
  API X", "OpenAPI schema", "contract change for fleet integration"
- **MCP tool design**: adding/modifying an MCP tool — engage this skill
  alongside the MCP-vs-CLI decision criteria
- **CLI flag design**: adding a new top-level CLI flag — engage with
  Gateway Output Contract awareness
- **Fleet RPC design**: planning agent-to-agent or controller-agent
  protocols (load `infra-networking` for transport too)

Do NOT load when:

- The concern is RUNTIME state of the API (load `aicp-ops-runtime`)
- The concern is MCP MIGRATION specifically (the audit decision is the
  source of truth — load it directly)
- The concern is HOW to invoke a CLI flag (load the relevant ops skill —
  `aicp-ops-*`)

## Operations

### Operation 1 — Design a new MCP tool (and decide if it should be CLI instead)

**When**: a new capability needs to be exposed.

**Process**:

1. Apply the `cli-tools-beat-mcp-for-token-efficiency` lesson criteria:
   - Cross-conversation discoverability needed? → MCP
   - External service bridge? → MCP
   - Project-internal operational? → CLI+Skills (preferred)
   - High-frequency inference? → MCP (Category A in audit)
2. If CLI: extend `aicp/cli/main.py`, follow Gateway Output Contract
   (NEXT lines). Author companion SKILL.md.
3. If MCP: add to `aicp/mcp/server.py` with `@mcp.tool()` decorator,
   minimal docstring (concise schema reduces consumer overhead)
4. Document the decision (especially if this is a borderline case) in
   `wiki/decisions/00_inbox/<tool-name>-mcp-or-cli.md`

**Quality bar**: NEW MCP tools default to "should be CLI" unless they
clearly meet MCP-win criteria. Per the audit, AICP has too many MCP tools
already — adding more without rigor compounds the problem.

### Operation 2 — Version an API surface

**When**: backward-incompatible change is unavoidable.

**Process**:

1. Choose versioning style:
   - URL path: `/v1/...` → `/v2/...` (LocalAI-style; visible)
   - Header: `Accept-Version: 2` (less visible; harder for operators)
   - Tool name: `aicp_chat` → `aicp_chat_v2` (MCP-style; clear)
2. Implement v2 alongside v1; mark v1 deprecated with warning
3. Per `config-migrations` skill, give a deprecation window (1-2 releases)
4. Document: CHANGELOG + decision page

**Quality bar**: v1/v2 cohabitate during deprecation; cutting v1 same
release as v2 is a hard break that breaks consumers without warning.

### Operation 3 — Deprecate an API endpoint or tool

**When**: removing something from the public surface.

**Process**:

1. Mark deprecated: docstring `[DEPRECATED]` prefix + return-payload
   `warning:` field (per the MCP audit pattern — see deprecated MCP
   tools in `aicp/mcp/server.py`)
2. Wait 1-2 release cycles for consumers to migrate
3. Remove the registration; runtime returns 404 or NoSuchTool
4. Document the timeline in CHANGELOG

**Quality bar**: NEVER skip the deprecation period. Removing without
warning breaks consumers silently.

### Operation 4 — Generate or audit an OpenAPI schema

**When**: documenting AICP's REST surface for external consumers.

**Process**:

1. AICP itself doesn't have a REST API beyond LocalAI's (which has
   OpenAPI from upstream) and the agent server (which is small)
2. For the agent server: the REST surface is in `aicp/agent/server.py`;
   generate OpenAPI via FastAPI's built-in `/openapi.json` endpoint
3. For the LocalAI proxied surface: refer to LocalAI's own OpenAPI spec
   at `localhost:8090/swagger/index.html` (when LocalAI runs)
4. For the MCP tool surface: MCP doesn't use OpenAPI — the tool list is
   the schema (visible via the MCP client's `tools/list` request)

**Quality bar**: don't claim AICP has an OpenAPI surface it doesn't have
(only the agent server does). Setting expectations correctly avoids
operator confusion.

## Gotchas

- **Detection**: agent adds a new MCP tool without applying CLI-vs-MCP criteria.
  **Rule**: every new MCP tool gets evaluated against the `cli-tools-beat-mcp`
  lesson criteria first. Default is CLI.
  **Reasoning**: per the audit, AICP already has 64 MCP tools; adding
  more without justification compounds the schema overhead per consumer.

- **Detection**: agent versions via header instead of URL path.
  **Rule**: prefer URL path versioning (`/v1/`) — visible, debuggable,
  cacheable.
  **Reasoning**: header versioning is invisible in logs, breaks naive
  caching, and produces hard-to-debug version mismatches.

- **Detection**: agent removes a deprecated tool same release as deprecation.
  **Rule**: deprecation needs 1-2 release cycles before removal.
  **Reasoning**: consumers need a window to migrate; same-release
  removal is a hard break.

- **Detection**: agent claims AICP has an OpenAPI spec for the MCP surface.
  **Rule**: MCP doesn't use OpenAPI — the tool list IS the schema.
  **Reasoning**: misnaming the contract type leads to confusion;
  OpenAPI applies to REST, not MCP stdio.

- **Detection**: agent designs a fleet RPC without considering the audit's MCP-as-bridge guidance.
  **Rule**: fleet agent-to-agent protocols are exactly the case MCP
  serves well (cross-conversation discoverability + external bridge).
  Don't reinvent in CLI.
  **Reasoning**: the audit categorizes fleet/P2P tools as Category C
  KEEP MCP for this reason.

## Reference exemplars

- `aicp/mcp/server.py` — MCP tool definitions; deprecated tools show
  the warning-payload pattern
- `aicp/cli/main.py` — CLI flag dispatcher; `_print_next()` helper for
  Gateway Output Contract
- `aicp/agent/server.py` — agent REST API (the only AICP-defined REST surface)
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` —
  the audit decision (MCP-vs-CLI categorization criteria)
- `wiki/decisions/00_inbox/aicp-cli-mcp-outputs-adopt-gateway-output-contract.md` —
  the contract for CLI/MCP outputs
- `~/devops-solutions-research-wiki/wiki/lessons/03_validated/tools-architecture/cli-tools-beat-mcp-for-token-efficiency.md` —
  the underlying lesson

## Domain context

AICP's API surface is intentionally bifurcated: LocalAI's REST for
inference (proxied), MCP for cross-conversation tools, CLI for
operator/skill-driven workflows. The active migration is reducing MCP
surface (per audit) while maintaining LocalAI proxy + adding CLI flags
for migrated capabilities. Future fleet API design lives in this skill's
scope.

## Related skills

| Skill | When to use |
|-------|-------------|
| `infra-networking` | When the concern is transport (port, MCP stdio, etc.) |
| `infra-security` | When the concern is auth/access for the API surface |
| `config-migrations` | When the API change includes config schema migration |
| `architecture-propose` | When proposing a major NEW API surface |
| `aicp-ops-runtime` | When diagnosing live API behavior |
