---
name: evolve-plugin-system
description: Evolve AICP's three extension surfaces — skills (`.claude/skills/*/SKILL.md`, 84 today), MCP tools (`aicp/mcp/server.py`, 64 registered, 21 deprecated per audit), and hooks (`tools/hooks/pretool_safety.py` Layer A + Layer B). Formalize plugin discovery, third-party skill packs, versioning, or backend pluggability (extending `aicp/backends/base.py` contract). Distinct from `evolve-integrate` (NEW external system) — this skill is about evolving the existing extension surfaces themselves. Loads when the operator says "extend the plugin system" / "third-party skill packs" / "formalize backend plugins" / "version skills" / "discover skills dynamically" / "add a new extension type".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# evolve-plugin-system

Evolve AICP's three extension surfaces (skills, MCP tools, hooks) as a
SYSTEM — add new extension types, formalize versioning, introduce plugin
discovery, or establish a third-party contribution protocol.

Distinct from `evolve-integrate` (integrates an external system as a
dependency) — this skill evolves AICP's ability to BE extended.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "extend the plugin system", "add a new extension type",
  "formalize plugins", "third-party skill packs", "discover skills
  dynamically"
- **Versioning**: "version the skills", "skill v1 vs v2", "MCP tool
  deprecation period"
- **Backend pluggability**: "make backends pluggable", "register a backend
  at runtime", "pip-installable backend"
- **Skill pack distribution**: "share skills across projects", "skill
  packs from external repos", "fleet-wide skill sync"

Do NOT load when:

- The concern is adding ONE new skill / MCP tool / hook — that's authoring,
  not system evolution; load the appropriate authoring skill (e.g.,
  `architecture-propose` for a new extension, or just write it inline)
- The concern is integrating with an external system — load `evolve-integrate`
- The concern is the MCP tool audit migration track — that's already
  scoped in `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`

## Operations

### Operation 1 — Inventory the three surfaces before evolving

**When**: start of any plugin-system evolution; ground the work in reality.

**Process**:

1. Count the current state of each surface:
   - **Skills**: `ls .claude/skills/ | wc -l` — currently ~84
   - **MCP tools**: grep `@mcp.tool()` or equivalent in `aicp/mcp/server.py`
     — currently 64 registered (21 deprecated)
   - **Hooks**: `ls tools/hooks/` — currently Layer A (safety) + Layer B
     (stage gate) + `.claude/settings.json` registration
2. Note which surfaces have Extension Standards compliance (per
   `wiki/decisions/00_inbox/skills-audit-2026-04-17.md`) and which are
   boilerplate
3. Identify the specific evolution proposed (new type? versioning?
   discovery? third-party?) — DO NOT treat these as interchangeable

**Quality bar**: never propose plugin-system changes without knowing what
currently exists. The `skills-audit` document is the canonical inventory
for skills; the MCP audit is canonical for MCP tools. Re-use these.

### Operation 2 — Author the plugin-system decision

**When**: evolution scope is concrete; before any code.

**Process**:

1. Per Knowledge Evolution Standards, author a decision page at
   `wiki/decisions/00_inbox/plugin-system-<change>.md`:
   - WHY: what does the evolution enable that current extension surfaces
     can't do?
   - SCOPE: which of the three surfaces (skills / MCP / hooks) — or a
     new fourth surface
   - ALTERNATIVES: at least 2 (e.g., "extend existing surface X" vs
     "introduce new surface Y" vs "punt")
   - VERSIONING: how does the evolution coexist with existing extensions?
     (backward compat / deprecation / breaking)
   - DISCOVERY: how does AICP find plugins — filesystem scan, explicit
     registration, pip metadata, something else?
2. Get operator approval before implementing

**Quality bar**: NEVER evolve the plugin system without a decision page.
Plugin-system changes affect every future extension; the decision is
the contract future contributors rely on.

### Operation 3 — Evolve the skill system

**When**: decision scoped to `.claude/skills/*`.

**Process**:

1. Identify the evolution type:
   - **Versioning**: add `version:` to frontmatter; runtime picks latest
     compatible (requires a resolver — non-trivial)
   - **Third-party packs**: allow skills to live OUTSIDE `.claude/skills/`
     (e.g., pip-installed `aicp-skills-fleet-ops`) with discovery via
     entry points or a registry file
   - **Per-project override**: allow a project to override AICP's skill
     with its own version at same name
   - **New frontmatter field**: add field to Extension Standards, update
     linter, migrate existing skills
2. Update `aicp/core/skills.py` (the loader) to honor the new field/
   discovery path
3. Update Extension Standards documentation in the wiki
4. Backfill tests in `tests/test_skills.py`

**Quality bar**: every evolution of skill system updates BOTH the loader
AND the Extension Standards. Documentation drift is the #1 mode by which
plugin-system evolutions rot.

### Operation 4 — Evolve the MCP tool surface

**When**: decision scoped to MCP.

**Process**:

1. Coordinate with the in-flight MCP audit migration
   (`wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`)
   — DO NOT evolve the surface during active deprecation without a
   conflict check
2. Identify the evolution:
   - **Versioning**: `aicp_chat` → `aicp_chat_v2` coexistence pattern
     (per `evolve-api-version` skill)
   - **Dynamic registration**: allow tools to be registered at startup
     via a config file (enables third-party MCP packs)
   - **Per-profile tool subset**: expose different tools per AICP profile
     (e.g., `reliable` profile gets `aicp_deep_health`, `fast` doesn't)
3. Coordinate with `infra-api` skill (MCP is one of AICP's API surfaces)

**Quality bar**: MCP evolutions MUST honor the CLI-beats-MCP lesson
(`wiki/lessons/00_inbox/aicp-mcp-server-tool-surface-drift-from-claude-md.md`).
New MCP tools justify their schema overhead or go to CLI + Skills instead.

### Operation 5 — Evolve the hook system

**When**: decision scoped to `tools/hooks/`.

**Process**:

1. Identify the evolution:
   - **New layer**: Layer C beyond A (safety) + B (stage gate) — e.g.,
     Layer C for per-project custom rules
   - **Hook pack distribution**: allow hooks to ship as pip packages
     discovered via `.claude/settings.json` extensions
   - **Per-task hook customization**: different hook behavior based on
     `.aicp/state.yaml` active task type
2. Update `.claude/settings.json` registration pattern (document in
   CLAUDE.md or AGENTS.md)
3. Coordinate with `infra-security` — hooks are a security surface

**Quality bar**: hook evolutions MUST preserve fail-closed semantics.
A layer that fails open (default allow on error) is a regression from
current safety baseline.

### Operation 6 — Document and migrate

**When**: evolution is implemented; existing extensions need to adapt.

**Process**:

1. Write a migration guide in `wiki/patterns/00_inbox/` or
   `docs/migrations/` explaining how existing extensions adapt
2. Update CLAUDE.md's `## Project Structure` table if a new top-level
   extension surface was added
3. Update AGENTS.md reading order for new contributors
4. Run the linter (`python3 -m tools.lint`) on existing extensions; fix
   compatibility issues
5. Add a CHANGELOG entry

**Quality bar**: evolutions that don't document migration paths leave
existing contributors stranded. Every breaking change gets a migration
guide.

## Gotchas

- **Detection**: agent evolves plugin surface without inventorying what
  exists.
  **Rule**: always run the surface-count step (Operation 1) first.
  **Reasoning**: without grounding in current state, proposed evolutions
  often duplicate existing capability or miss compatibility constraints.

- **Detection**: agent adds new MCP tools during active MCP audit
  deprecation period.
  **Rule**: check `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md`
  status first; coordinate or defer.
  **Reasoning**: adding tools while removing others muddies the schema
  reduction measurement and confuses operators.

- **Detection**: agent updates the skill loader but forgets to update
  Extension Standards.
  **Rule**: loader + Standards + linter evolve together, always.
  **Reasoning**: drift between the three produces skills that pass the
  linter but crash the loader (or vice versa).

- **Detection**: agent introduces a hook layer that fails open on error.
  **Rule**: hooks MUST fail closed (deny on error). See
  `tools/hooks/pretool_safety.py` for the canonical pattern.
  **Reasoning**: the safety baseline depends on fail-closed semantics;
  a new layer that fails open silently regresses it.

- **Detection**: agent proposes plugin-system evolution without naming
  the concrete use case.
  **Rule**: plugin-system evolutions are expensive; require a named
  operator + named extension they want to build.
  **Reasoning**: speculative plugin evolution is dead code. AICP's
  extension surfaces are already plural (3); a 4th without a real
  consumer is cost without return.

- **Detection**: agent adds per-task / per-profile conditional extension
  loading without measuring the schema cost.
  **Rule**: measure MCP schema size before/after; conditional loading
  often doesn't save tokens because the model still sees the full
  registration code path.
  **Reasoning**: conditional-loading for MCP has been a dead-end
  optimization historically; verify actual token savings before
  committing.

## Reference exemplars

- `aicp/core/skills.py` — the canonical skill loader; all skill-system
  evolutions update this module
- `aicp/mcp/server.py` — the MCP tool registration surface; line 1 is the
  `@mcp.tool()` decoration pattern
- `aicp/backends/base.py` — the backend contract (for backend-pluggability
  evolutions)
- `tools/hooks/pretool_safety.py` — Layer A hook canonical pattern
  (fail-closed, return exit 2 to block)
- `wiki/decisions/00_inbox/skills-audit-2026-04-17.md` — canonical skill
  inventory
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` —
  canonical MCP inventory
- `wiki/decisions/01_drafts/pretooluse-hooks-layered-approach-layer-a-vs-layer-b.md` —
  canonical hook architecture

## Domain context

AICP has three extension surfaces intentionally: skills for just-in-time
loaded documentation + process knowledge, MCP tools for external-bridge
inference capability, hooks for runtime safety + stage gating. The
distinction matters — an evolution that blurs them (e.g., "make skills
callable as MCP tools") degrades operator mental model. Per the
`cli-tools-beat-mcp-for-token-efficiency` lesson, the default answer to
"should this be an MCP tool?" is "probably CLI + skill instead" — that
bias applies to plugin-system evolutions too.

## Related skills

| Skill | When to use |
|-------|-------------|
| `architecture-propose` | For the design of a significant plugin-system change |
| `evolve-integrate` | When the evolution is about adding a NEW external system, not evolving the extension surfaces |
| `evolve-api-version` | When evolving MCP tool versioning specifically |
| `infra-api` | Design of API surfaces (MCP included) |
| `infra-security` | When hook system changes affect security posture |
| `refactor-architecture` | When the evolution restructures how extensions live in the package layout |
| `feature-document` | For scoping the evolution's requirements |
