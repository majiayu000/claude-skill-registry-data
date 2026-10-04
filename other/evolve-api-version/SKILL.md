---
name: evolve-api-version
description: Evolve AICP's API surfaces across versions — bump LocalAI proxy paths (`/v1` → `/v2`), version MCP tools (`aicp_chat` → `aicp_chat_v2`), version CLI flag schemas (e.g., new `--task-cmd` action breaking old call shape), version agent server REST. Coordinated with `infra-api` (design) and `config-migrations` (config schema). Loads when the operator says "version the API" / "ship a v2" / "breaking API change" / "evolve the MCP surface" / "deprecate v1 endpoint".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# evolve-api-version

Manage AICP API version transitions across the surfaces enumerated by
`infra-api`. This skill is the EVOLUTION lifecycle: how to introduce v2
alongside v1, when to deprecate, when to remove. Distinct from
`infra-api` (design) and `config-migrations` (config schema only).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "version the API", "ship a v2", "breaking API change",
  "evolve the MCP surface", "deprecate v1 endpoint"
- **Cross-version coordination**: an API change requires synchronized
  bumps across CLI + MCP + agent server
- **Migration timing**: planning the deprecation window between v1 and
  v2 cutover

Do NOT load when:

- The concern is API DESIGN (load `infra-api`)
- The concern is config schema migration (load `config-migrations`)
- The concern is consumer-side migration (the consumer's repo, not AICP)

## Operations

### Operation 1 — Plan a versioned API change

**When**: a backward-incompatible API change is required.

**Process**:

1. Identify ALL affected surfaces:
   - LocalAI proxy paths (typically not AICP's call to evolve — LocalAI does)
   - MCP tools (rename suffix `_v2`, deprecate the v1)
   - CLI flag (rename `--cmd` → `--cmd-v2`, accept both during deprecation)
   - Agent server REST (URL path version)
2. Author a decision page in `wiki/decisions/00_inbox/<change>-v2.md`
   per Knowledge Evolution Standards: alternatives + reversibility +
   migration plan
3. Choose deprecation timeline:
   - Aggressive: v2 ships, v1 deprecation warning, v1 removed next release
     (2 cycles)
   - Conservative: v2 ships, v1 deprecation warning for 2-3 cycles, then remove
4. Document in CHANGELOG and CLAUDE.md

**Quality bar**: NEVER ship v2 without a v1 deprecation period. Same-release
removal is a hard break.

### Operation 2 — Implement v2 alongside v1

**When**: Operation 1 is approved; build the v2 implementation.

**Process**:

1. For MCP: add `@mcp.tool() def aicp_thing_v2(...)` adjacent to the
   existing `aicp_thing` (don't replace yet)
2. For CLI: add the new flag/handler in `aicp/cli/main.py`; keep old
   flag working with deprecation warning
3. For agent server: add new route at `/v2/...`, keep `/v1/...` working
4. Test: BOTH v1 and v2 must work during deprecation
5. Per the MCP audit deprecation pattern (see `aicp/mcp/server.py`
   deprecated tools), add `warning:` field to v1 returns pointing
   consumers to v2

**Quality bar**: a release containing v2 must NOT break v1. Verify by
running the test suite for both APIs.

### Operation 3 — Deprecate v1

**When**: v2 is shipped + validated; v1 is end-of-life-marked.

**Process**:

1. Update v1 docstring with `[DEPRECATED]` prefix + clear migration
   instructions to v2
2. Add `warning:` payload field (MCP) or stderr deprecation print (CLI)
3. Document the removal date in CHANGELOG and decision page
4. Consider adding a per-call deprecation warning rate-limited (so it
   doesn't spam noisy on high-frequency calls)

**Quality bar**: deprecation must be VISIBLE to consumers. Silent
deprecation is the same as no deprecation.

### Operation 4 — Remove v1 after the deprecation window

**When**: 1-2 release cycles after Operation 3.

**Process**:

1. Per the MCP migration removal pattern, remove the `@mcp.tool()`
   registration / CLI flag / route handler
2. Keep a stub that returns a clear error: "v1 was removed in release X;
   migrate to v2 per <link>"
3. After 1 more release cycle, remove even the stub
4. Update CHANGELOG with the removal

**Quality bar**: the error stub gives the LAST set of consumers a clear
error rather than a 404; it lasts one release cycle then goes away too.

## Gotchas

- **Detection**: agent versions a CLI flag without coordinating with MCP / agent server.
  **Rule**: cross-surface API changes need coordinated versioning.
  Identify ALL affected surfaces in Operation 1.
  **Reasoning**: consumers may use multiple surfaces (e.g., CLI for
  operator + MCP for fleet); partial versioning produces confusion.

- **Detection**: agent removes v1 in the same release as v2 ships.
  **Rule**: ALWAYS deprecation period between ship-v2 and remove-v1.
  Minimum 1 release; 2+ is safer.
  **Reasoning**: consumers can't migrate instantly; same-release removal
  is a hard break that breaks dependent projects.

- **Detection**: agent uses URL header versioning for an MCP tool.
  **Rule**: MCP tools version via NAME suffix (`_v2`); URL/header
  versioning is REST-specific.
  **Reasoning**: MCP doesn't have URLs or headers in the conventional
  REST sense; the tool name IS the contract.

- **Detection**: agent skips the per-call deprecation warning ("just trust the docs").
  **Rule**: in-band deprecation warnings are visible to consumers AT CALL
  TIME; doc-only deprecation gets missed.
  **Reasoning**: consumers don't routinely re-read docs for tools they
  use; they re-read when the tool errors. In-band warning bridges that gap.

- **Detection**: agent treats config schema changes as API versioning.
  **Rule**: config schema is `config-migrations` scope; API versioning
  is THIS skill. Different surfaces, different lifecycles.
  **Reasoning**: config schema operators tune YAML; API consumers call
  endpoints. Conflating produces wrong-tier migration plans.

## Reference exemplars

- `aicp/mcp/server.py` — deprecated tools (21 of them) show the
  warning-payload pattern
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` —
  example versioning decision (deprecation + removal phases)
- `aicp/cli/main.py` — CLI flag handler shape (relevant for new --v2 flags)
- `~/devops-solutions-research-wiki/wiki/spine/standards/...` — second brain
  versioning standards (if a dedicated one exists)

## Domain context

AICP's API surfaces evolve on different cadences: LocalAI's REST is
upstream-controlled; MCP tools evolve per AICP's audit + design;
CLI flags evolve per Gateway Output Contract; agent server evolves per
fleet integration needs. This skill handles the cross-surface
coordination required for breaking changes.

## Related skills

| Skill | When to use |
|-------|-------------|
| `infra-api` | When the concern is API DESIGN (not version transition) |
| `config-migrations` | When the change includes config schema migration |
| `pm-changelog` | When documenting version changes for release notes |
| `evolve-migrate` | When the migration is broader than just API (data + code) |
