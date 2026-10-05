---
name: team-manager
description: |
  Create and maintain TeamMember entities — humans and named AI personas that participate in the project with persistent identity, personality, and tiered memory. Use when adding a new persistent team-member (human or named AI), managing the name pool, scaffolding memory trees, or exporting/importing a team-member bundle. Replaces the deprecated actor-profile skill (DEC-20260422_0233-SpryTulip).
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-team-manager
    version: "1.0.0"
    created: 2026-04-22T00:00:00Z
    category: processkit
    layer: 1
    replaces:
      - SKILL-actor-profile
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
      - skill: role-management
        purpose: Resolve default_role references against the Role catalog.
    provides:
      primitives: [TeamMember]
      mcp_tools:
        - create_team_member
        - get_team_member
        - list_team_members
        - get_active_interlocutor
        - set_active_interlocutor
        - update_team_member
        - deactivate_team_member
        - reactivate_team_member
        - reserve_name
        - release_name
        - list_available_names
        - suggest_name
        - init_memory_tree
        - export_team_member
        - export_claude_subagent
        - export_claude_subagents
        - import_team_member
        - check_consistency
        - check_all_consistency
      templates: [team-member-human, team-member-ai-agent]
---

# Team Manager

## Intro

TeamMembers are the persistent participants in the project — named AI
personas, services, consultants, and explicitly managed human aliases —
that accumulate identity, personality, and tiered memory over time. This
skill owns their lifecycle: creation, memory tree scaffolding, a curated
international name pool, A2A-compatible Agent Cards, export/import
bundles, and consistency checks.

Unlike ephemeral worker invocations (role+seniority dispatches resolved on
the fly and never persisted), TeamMembers live as directory trees on disk:
`persona.md` + `card.json` + `team-member.md` (entity) + tiered memory
subdirectories + optional `private/` (gitignored).

Human TeamMembers are privacy-sensitive. Do not auto-create them from
ambient host, git, or harness identity. `create_team_member(type="human",
...)` stores only the slug as the committed display name by default and
drops `email`/`handle`; pass `allow_committed_pii=true` only after the
human explicitly agrees that their name or contact details may live in
repo-visible files. Store local-only human details under `private/`, not
in `team-member.md`.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable.

## Overview

### Invocation surface

This skill is not a CLI; it is reached entirely via MCP tools served
by `mcp/server.py`. Tools cluster into six capability groups
(lifecycle, session identity, name pool, memory scaffolding,
export/import, consistency). Every write tool logs an `event-log`
entry and updates the SQLite index automatically — callers do not log
or reindex by hand. Read tools (`get_team_member`,
`list_team_members`, `get_active_interlocutor`,
`get_interlocutor_runtime_binding`, `list_available_names`,
`suggest_name`, `get_team_member_runtime`, `list_team_member_runtimes`,
`check_consistency`) are side-effect-free and safe to call from any
agent context.

### Capability groups

| Group | Tools | Use when |
|---|---|---|
| Lifecycle | `create_team_member`, `get_team_member`, `list_team_members`, `update_team_member`, `deactivate_team_member`, `reactivate_team_member` | Adding, editing, retiring or restoring a persistent team-member entity |
| Session identity | `get_active_interlocutor`, `get_interlocutor_runtime_binding`, `set_active_interlocutor` | Showing which persistent TeamMember, if any, is the current harness interlocutor, plus the resolved runtime binding when available |
| Runtime launch | `launch_team_member`, `launch_workitem_assignee`, `get_team_member_runtime`, `list_team_member_runtimes`, `stop_team_member_runtime` | Creating and tracking a harness-consumable TeamMember runtime request with explicit model, status, and write policy |
| Name pool | `reserve_name`, `release_name`, `list_available_names`, `suggest_name` | Choosing or rotating an AI persona name; the pool is the canonical source of truth for AI-agent slugs |
| Memory scaffolding | `init_memory_tree` | Creating the six tier subdirectories + frontmatter-validated headers under `context/team-members/<slug>/` |
| Export / import | `export_team_member`, `export_claude_subagent`, `export_claude_subagents`, `import_team_member` | Moving a TeamMember between projects or generating provider-specific adapter files; tarball export redacts confidential/PII memory |
| Consistency | `check_consistency`, `check_all_consistency` | Pre-release health-check; CI validation; ad-hoc audits, including human committed-PII warnings |

### Common workflows

**Adding a human contributor.** Prefer an ephemeral Actor/reference unless
the project really needs a persistent human TeamMember. When persistence
is needed, use a privacy-preserving slug such as `human-user` or
`project-owner`: `create_team_member(type="human", name="human-user",
slug="human-user", ...)` → `init_memory_tree(slug)`. No name-pool
interaction; humans use any valid kebab-case slug. Real names, emails,
and handles require `allow_committed_pii=true` and explicit human consent.

**Adding a named AI persona.** `suggest_name(kind="neutral")` →
`create_team_member(type="ai-agent", slug=<name>, ...)` (auto-reserves
the name) → `init_memory_tree(slug)` → write `persona.md` and the
A2A-compliant `card.json`. The name is now drawn from the pool and
must remain in `data/name-pool.yaml` until released.

**Retiring a persona.** `deactivate_team_member(slug, reason)` (sets
`active: false`; preserves history) → optionally
`release_name(name)` to return the slug to the pool. To bring the
persona back, call `reactivate_team_member(slug)`.

**Migrating a persona between projects.**
`export_team_member(slug)` → ship the tarball → at the destination
`import_team_member(tarball_path)`. Schema and Agent Card are
re-validated on import; signature presence is required (crypto
verification is deferred).

**Showing the active interlocutor.**
`set_active_interlocutor(id)` writes
`context/team/session-identity.json` with the TeamMember that should be
presented as the harness's main speaker. `get_active_interlocutor()`
returns a compact label and speaker prefix for status briefings and
session-start UI. This is session identity, not lifecycle state:
`TeamMember.spec.active` continues to mean whether a TeamMember is
eligible to participate at all.

Use `get_interlocutor_runtime_binding(observed_model?,
observed_effort?)` when the caller can supply the harness's actual
runtime. The tool returns the provider-neutral TeamMember identity, the
model-recommender candidate after local provider gates, the negotiated
harness mode, and an informational mismatch report. processkit cannot
hot-swap an already running primary harness session; unsupported
harnesses therefore fall back to identity-only behavior while still
growing memory on the configured TeamMember.

**Launching TeamMember runtimes.**
`launch_team_member(id, harness?, ...)` creates a runtime record under
`context/team/runtime-sessions.json` and returns a harness-specific
dispatch payload. `launch_workitem_assignee(workitem_id, ...)` resolves
the WorkItem's `TEAMMEMBER-*` assignee first and then records the same
runtime contract. Runtime state is separate from WorkItem state:
`queued`, `running`, `failed`, and `stopped` describe the harness
session, not the work lifecycle.

The MCP server does not spawn host harness processes directly. For
Claude, the dispatch payload names the `subagent_type` and refreshes the
`.claude/agents/<slug>.md` adapter by default. For Codex, Aider, and
OpenCode, the payload carries the TeamMember identity, resolved model,
effort, write scope, and MCP/context-write policy for the outer harness
adapter to consume. Use `list_team_member_runtimes(active_only=true)`
and `stop_team_member_runtime(handle)` to report and update status.

**Exporting Claude Code subagents.**
`export_claude_subagent(slug)` writes one generated adapter to
`.claude/agents/<slug>.md`; `export_claude_subagents()` exports all
active non-human TeamMembers by default. The generated file uses
Claude Code's Markdown + YAML frontmatter format, sets `model:
inherit`, and omits `tools` so Claude Code inherits the main session's
model and permissions. Pass `model_policy="resolved"` to emit a Claude
model and effort only when processkit routing resolves to an Anthropic
candidate. TeamMember remains the canonical, provider-neutral identity;
`.claude/agents/*.md` is only an adapter.

**Pre-release audit.** `check_all_consistency()` → triage findings by
severity. Errors block release; warnings are advisory. Treat
`team.privacy.committed_pii` as release-blocking for derived-project
templates and installer output: rotate the TeamMember to an alias or move
the personal data into `private/`.

### Mental model

A TeamMember is **a directory tree on disk**, not a row in a database.
The entity file (`team-member.md` / `team-member.yaml` frontmatter)
is the SQLite-indexed object; `persona.md`, `card.json`, and the six
tier subdirectories live alongside it as durable, human-editable
context. Humans/services have no name-pool requirement; AI personas
do. TeamMembers are distinct from **ephemeral worker invocations** —
those are resolved on the fly by `task-router` against role+seniority
and never persist as TeamMembers.

### Pointers to the full reference

The `## Full reference` section below covers the MCP tool contract,
the SQLite-index schema fields, the `data/name-pool.yaml` document
format, the consistency check codes in greater detail, the export
bundle layout, the migration path from `actor-profile`
(DEC-20260422_0233-SpryTulip), and the corner cases for memory
sensitivity tagging. Read it before extending the skill or changing
any tool's contract.

## ID convention

TeamMember IDs follow a single shape:

    TEAMMEMBER-<slug>

where `<slug>` is the team-member's canonical kebab-case name (e.g.
`atlas`, `alice-chen`, `thrifty-otter`). The slug starts with a letter and
uses only `[a-z0-9-]`. It is also the directory name under
`context/team-members/<slug>/`.

For `type=ai-agent`, the slug must be drawn from the team-manager name
pool (see **Name pool** below). For `type=human` and `type=service`, any
valid kebab-case slug is accepted.

## TeamMember types

| type         | Example                                     | When to create |
|--------------|---------------------------------------------|----------------|
| `human`      | Project owner, contributors, reviewers      | The first time the person is assigned work, makes a decision, or gets a Binding |
| `ai-agent`   | Atlas, Aria, Kai (named personas)           | A persistent AI persona you want to grow over time — with memory, personality, and accumulated lessons |
| `service`    | GitHub Actions, CI bots, deploy pipelines   | Automated agents that perform repeat actions and need a stable identity for audit trails |

Do **not** promote every mention of a person into a TeamMember. And do
**not** create a named AI persona for a one-off dispatch — use an
ephemeral role+seniority invocation instead.

## Memory tiers

Every team-member directory contains six tier subdirectories under
`context/team-members/<slug>/`:

| Tier       | What lives here | Cadence |
|------------|-----------------|---------|
| `working/` | Task-local scratchpad, active session context | Ephemeral |
| `journal/` | Daily journal, episodic entries | Daily consolidation |
| `knowledge/` | Semantic knowledge, stable facts, domain notes | Weekly promotion from journal |
| `skills/`  | Procedural recipes, working style, patterns | As learned |
| `relations/` | Per-teammate relationship notes (one file per known teammate) | On interaction |
| `lessons/` | Reflected lessons; A-MemGuard-style consensus defense against memory poisoning | Per-task |

Plus `private/` (optional, developer-local, gitignored) and three
top-level files: `persona.md` (identity + personality prompt),
`card.json` (A2A Agent Card), `team-member.md` (the entity itself).

Every memory file under a tier subdirectory must carry a frontmatter
block validated against `assets/memory-file-header.schema.json` —
required keys: `tier`, `source`, `sensitivity`, `created`.

## Name pool & international naming policy

The name pool lives at `data/name-pool.yaml` (managed by this skill).
It contains three gender-bucket lists (feminine, masculine, neutral) of
international, short, human-friendly first names — ~60 total. Names
from the pool are the canonical identifier source for AI personas.

**Reservation lifecycle**

- `suggest_name(kind?)` — pick a random available name, optionally
  filtered by gender bucket. Does not reserve.
- `reserve_name(name, team_member_slug)` — mark a name taken by a
  specific slug. Writes to `data/name-pool.yaml` atomically.
- `release_name(name)` — remove the reservation (e.g. on team-member
  deletion or re-export).
- `list_available_names(kind?)` — enumerate non-reserved names.

For `create_team_member(type="ai-agent", ...)`, the `slug` must
correspond to a name currently in the pool. The tool auto-reserves on
success.

## Consistency checks

`check_consistency(slug)` returns findings for a single team-member;
`check_all_consistency()` aggregates across every team-member.

Each finding is `{severity, code, team_member, path, message}`. Codes:

| Code | Severity | What it checks |
|------|----------|----------------|
| `team.drift.schema` | error | `team-member.yaml` frontmatter validates against `SCHEMA-team-member` |
| `team.drift.tier_missing` | error | Expected subdirs (knowledge, journal, skills, relations, lessons) exist |
| `team.drift.dangling_ref` | error | `default_role` resolves to an existing Role; `relationships[].with` resolves to known slugs/IDs |
| `team.name_collision` | error | No two active team-members share `name` or `slug` |
| `team.name.off_pool` | warning | For `type=ai-agent`, the name must be in the name pool |
| `team.drift.orphan_file` | warning | No files outside expected tier subdirs / persona.md / card.json / team-member.md / private/ |
| `team.sensitivity.leak_risk` | warning | Memory files with `sensitivity: confidential` or `pii` must live under `private/` |
| `team.private.not_ignored` | warning | Each `private/` directory is covered by a `.gitignore` rule |
| `team.memory.bad_header` | warning | Memory files under tier subdirs carry required frontmatter keys |
| `team.card.stale` | warning | `card.json` name/role/seniority match `team-member.yaml` |

## Export / import

`export_team_member(slug, output_path?)` builds a tar.gz bundle at
`<slug>-export-<YYYY-MM-DD>.tar.gz` containing:

- `persona.md`
- `card.json` (A2A Agent Card, conforms to `assets/agent-card.schema.json`)
- `team-member.md` (the entity)
- `knowledge/`, `skills/`, `lessons/`

Excludes `journal/`, `relations/`, `private/` by default. During the
memory-file walk, any file whose frontmatter declares
`sensitivity: confidential` or `sensitivity: pii` is redacted (skipped).

`import_team_member(tarball_path)` extracts to a temp dir, validates the
`team-member.yaml` against `SCHEMA-team-member`, validates `card.json`
against the A2A Agent Card schema, and checks that a `signature` field
is present on the card (crypto verification is deferred — signature
field presence is a hand-off marker for future work). On success it
copies the tree into `context/team-members/<slug>/` and logs
`team_member.imported`.

## Deprecation note

This skill **replaces** `actor-profile` (DEC-20260422_0233-SpryTulip).
The `ACTOR-<slug>` ID class and the `create_actor`/`get_actor`/etc.
tools are deprecated in v0.19.0. A migration on `context/actors/` runs
in a separate phase; do not modify actor-profile from here.

## Gotchas

- **Creating a TeamMember for every mention.** Reserved for persistent
  participants — the same rule as Actor. If they have no upcoming
  WorkItem/Binding/decision, don't promote them.
- **Drawing an AI persona name outside the pool.** `team.name.off_pool`
  will warn. Use `suggest_name` or `list_available_names` first.
- **Putting confidential info outside `private/`.** `team.sensitivity.leak_risk`
  catches it. The tier subdirectories are git-tracked; only `private/`
  is safe for developer-local sensitive context.
- **Hand-editing `data/name-pool.yaml`.** Use `reserve_name`/
  `release_name` — the tool preserves the document frontmatter and
  writes atomically.
- **Forgetting `init_memory_tree` after create.** `create_team_member`
  writes the entity but does not scaffold the tier subdirectories.
  Call `init_memory_tree(slug)` right after (or pass
  `init_memory=True` at create time, if implemented).
- **Putting role+seniority dispatches here.** Ephemeral worker
  invocations are NOT TeamMembers — they are resolved on the fly via
  `task-router`. Only persistent personas live in `team-members/`.

## Full reference

### MCP tool contract

All fifteen tools are served by `mcp/server.py`. Their tool
annotations follow the processkit convention checked by
`release-audit.mcp_annotations`:

| Tool | readOnlyHint | destructiveHint | idempotentHint | openWorldHint |
|---|---|---|---|---|
| `create_team_member` | false | false | false | false |
| `get_team_member` | true | false | true | false |
| `list_team_members` | true | false | true | false |
| `update_team_member` | false | false | false | false |
| `deactivate_team_member` | false | true | true | false |
| `reactivate_team_member` | false | false | true | false |
| `reserve_name` | false | false | false | false |
| `release_name` | false | true | true | false |
| `list_available_names` | true | false | true | false |
| `suggest_name` | true | false | false | false |
| `init_memory_tree` | false | false | true | false |
| `export_team_member` | true | false | true | false |
| `import_team_member` | false | false | false | false |
| `check_consistency` | true | false | true | false |
| `check_all_consistency` | true | false | true | false |

`mcp/SERVER.md` documents each tool's full input/output schema
including the JSON shape of `create_team_member` (slug, type,
default_role, name, gender_kind, …) and the `Finding` schema for
consistency checks (`{severity, code, team_member, path, message}`).

### Entity schema

The TeamMember frontmatter is validated against
`SCHEMA-team-member` (registered in `context/schemas/`). Required
fields:

| Field | Type | Notes |
|---|---|---|
| `id` | string | Must match `TEAMMEMBER-<slug>` |
| `slug` | string | `[a-z][a-z0-9-]*`; equals directory name |
| `name` | string | Display name; uniqueness enforced by `team.name_collision` |
| `type` | enum | `human` \| `ai-agent` \| `service` |
| `active` | bool | `false` after `deactivate_team_member` |
| `default_role` | string \| null | Resolved against the Role catalog by `team.drift.dangling_ref` |
| `created` | ISO8601 | Stamped by `create_team_member` |
| `relationships` | list | `[{with: <slug-or-id>, kind: <string>, since: <ISO>}]`; references resolved by drift check |

Optional fields used by templates: `card_path` (relative path to
`card.json`), `persona_path` (relative path to `persona.md`),
`memory_root` (relative path; defaults to the directory itself).

### `data/name-pool.yaml` document format

```yaml
---
schema: name-pool.v1
managed_by: SKILL-team-manager
updated: <ISO8601>
---
feminine:
  - name: aria
    reserved_by: TEAMMEMBER-aria   # null if available
    reserved_at: <ISO8601>         # null if available
masculine:
  - name: atlas
    reserved_by: null
    reserved_at: null
neutral:
  - name: kai
    reserved_by: null
    reserved_at: null
```

Atomic writes are produced by `scripts/name_pool.py` using a
write-then-rename pattern; the document frontmatter (`schema`,
`managed_by`, `updated`) is always preserved on round-trip. Hand
edits silently break atomicity guarantees and are caught only by
the next consistency check.

### Memory tier directory layout

```
context/team-members/<slug>/
├── persona.md                   # Identity + personality prompt
├── card.json                    # A2A Agent Card (assets/agent-card.schema.json)
├── team-member.md               # Entity file (frontmatter is the schema target)
├── working/                     # Ephemeral, task-local
├── journal/                     # Daily entries; consolidated weekly → knowledge/
├── knowledge/                   # Stable semantic facts
├── skills/                      # Procedural recipes / patterns
├── relations/                   # One file per known teammate slug
├── lessons/                     # A-MemGuard-style consensus lessons
└── private/                     # Optional, gitignored, developer-local
```

Every memory file under `journal/`, `knowledge/`, `skills/`,
`relations/`, `lessons/`, or `private/` carries a frontmatter block
validated by `assets/memory-file-header.schema.json`. Required keys:
`tier`, `source`, `sensitivity`, `created`. Allowed `sensitivity`
values: `public`, `internal`, `confidential`, `pii`. Files tagged
`confidential` or `pii` outside `private/` raise
`team.sensitivity.leak_risk`.

### Consistency check matrix (recap)

The 10 codes are split between hard errors (block release) and
warnings (advisory). The corresponding implementation lives in
`scripts/consistency.py`:

| Code | Severity | Implementation function |
|---|---|---|
| `team.drift.schema` | error | `check_schema(slug)` |
| `team.drift.tier_missing` | error | `check_tier_dirs(slug)` |
| `team.drift.dangling_ref` | error | `check_refs(slug)` |
| `team.name_collision` | error | `check_collisions()` (cross-slug) |
| `team.name.off_pool` | warning | `check_pool_membership(slug)` |
| `team.drift.orphan_file` | warning | `check_orphans(slug)` |
| `team.sensitivity.leak_risk` | warning | `check_sensitivity(slug)` |
| `team.private.not_ignored` | warning | `check_gitignore(slug)` |
| `team.memory.bad_header` | warning | `check_memory_headers(slug)` |
| `team.card.stale` | warning | `check_card(slug)` |

`check_all_consistency()` aggregates over `list_team_members(active=true)`
and returns `{summary: {errors, warnings}, findings: [...]}`. Use the
summary for CI gating; iterate findings for human-readable triage.

### Export bundle layout

```
<slug>-export-<YYYY-MM-DD>.tar.gz
└── <slug>/
    ├── persona.md
    ├── card.json
    ├── team-member.md
    ├── knowledge/
    ├── skills/
    └── lessons/
```

Excludes `working/`, `journal/`, `relations/`, `private/`. During
the memory walk, any file with frontmatter `sensitivity:
confidential` or `sensitivity: pii` is skipped (redacted) regardless
of which exported tier it lives in. Implementation:
`scripts/export_import.py::export_bundle()`.

### Import contract

`import_team_member(tarball_path)`:

1. Extract to a temp dir (cleaned on failure).
2. Validate `team-member.yaml` against `SCHEMA-team-member`.
3. Validate `card.json` against `assets/agent-card.schema.json`.
4. Require a `signature` field on the card (presence-only;
   cryptographic verification is a future-work hand-off marker).
5. Require the slug to be free locally (no collision with an
   existing TeamMember entity or active name-pool reservation).
6. Copy the tree to `context/team-members/<slug>/`.
7. For `type=ai-agent`, `reserve_name(name, slug)` is called as
   part of step 6.
8. Log `team_member.imported` via `event-log`.

Failures at any step abort cleanly — the temp dir is removed and no
target-side state is mutated.

### Migration from `actor-profile` (DEC-20260422_0233-SpryTulip)

`actor-profile` is deprecated as of v0.19.0; it is replaced by this
skill. Do NOT modify `actor-profile` from here. The migration
strategy is:

1. New write traffic targets `create_team_member` exclusively.
2. Existing `ACTOR-<slug>` IDs continue to be readable via the
   `actor-profile` MCP tools through the deprecation window.
3. A separate migration phase (tracked by its own MIG-* entity)
   converts each Actor under `context/actors/` into a TeamMember
   under `context/team-members/<slug>/`, preserving ID history via
   `replaces` cross-references.
4. After the migration completes, the `actor-profile` skill is
   removed entirely; release-audit will then start flagging any
   remaining `ACTOR-*` references as dangling.

The frontmatter `replaces: [SKILL-actor-profile]` records the
relationship; downstream skills should depend on `team-manager`,
not `actor-profile`, in their `uses:` blocks.

### Referenced source files

| Path | Purpose |
|---|---|
| `mcp/server.py` | MCP server entry point (PEP 723) |
| `mcp/SERVER.md` | Per-tool input/output schema reference |
| `mcp/mcp-config.json` | Harness merge block for stdio launch |
| `scripts/consistency.py` | All 10 consistency check implementations |
| `scripts/export_import.py` | Tarball build + import validation pipeline |
| `scripts/memory_tree.py` | `init_memory_tree` scaffolding logic |
| `scripts/name_pool.py` | Atomic reserve/release/list/suggest |
| `scripts/test_team_manager.py` | Pytest suite covering tools + scripts |
| `data/name-pool.yaml` | The canonical name pool document |
| `assets/agent-card.schema.json` | A2A Agent Card schema |
| `assets/memory-file-header.schema.json` | Memory file frontmatter schema |
| `assets/team-member-human.yaml` | Template for `type=human` |
| `assets/team-member-ai-agent.yaml` | Template for `type=ai-agent` |

### Extension points

- **New TeamMember type.** Add a new value to the `type` enum in
  `SCHEMA-team-member`, ship a template under `assets/`, extend the
  name-pool policy if a curated slug source is needed, and update
  the `team.name.off_pool` check to skip the new type if no curated
  pool applies.
- **New memory tier.** Add the directory to `init_memory_tree`,
  document it in the Memory tiers table, and extend
  `check_orphans` to recognise it. Decide whether export should
  include or redact it.
- **New consistency check.** Add a function in
  `scripts/consistency.py` returning `list[Finding]`, register it
  in the dispatcher, and document the code + severity in the
  matrix above. CI surfaces it on the next release-audit run.

### Corner cases

- **Slug collision on import.** Hard error; the importer never
  overwrites an existing TeamMember directory or reservation. To
  re-key a persona on import, rename the export tarball's inner
  directory + `team-member.md` slug field before importing.
- **Name reserved with no TeamMember.** Possible if a previous
  `create_team_member` failed after `reserve_name` but before
  entity write. Surfaced by `check_all_consistency()` as
  `team.drift.dangling_ref` against the pool. Resolve by
  `release_name` (manual triage, not auto-cleanup).
- **`private/` not gitignored.** `team.private.not_ignored`
  warning. Add `context/team-members/<slug>/private/` (or a glob
  parent) to `.gitignore`. The skill never writes `.gitignore`
  automatically — the warning is the action prompt.
- **Card / entity drift.** `team.card.stale` warning when
  `card.json`'s `name` / `role` / `seniority` no longer match
  `team-member.md` frontmatter. Re-export and re-import is the
  blunt fix; targeted re-write of `card.json` is the surgical fix.
- **Reactivating a deactivated member whose name was released.**
  `reactivate_team_member` will re-reserve the name if it is still
  free; if another persona has taken it, the call errors and the
  caller must pick a new slug (or wait for the colliding persona
  to be deactivated).
