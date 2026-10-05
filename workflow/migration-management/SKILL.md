---
name: migration-management
description: |
  Manage Migration entities — pending, in-progress, and applied transitions between upstream source versions. Use when an upstream source bumps version (processkit, a host installer, or a community package), when a user wants to draft a migration plan, when an agent needs to reason about pending migrations, or when working through an in-progress migration.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-migration-management
    version: "1.0.0"
    created: 2026-04-07T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: decision-record
        purpose: Record consequential decisions made during this skill's workflow.
      - skill: index-management
        purpose: Query existing entities and keep the SQLite index fresh after writes.
      - skill: id-management
        purpose: Allocate unique entity identifiers via central ID generation.
    provides:
      primitives: [Migration]
      templates: [migration]
---

# Migration Management

## Intro

A Migration is processkit's tracked representation of an upstream version
bump. When a host installer/sync tool notices a new processkit,
host-installer, or community-package version, it writes a Migration
entity into `context/migrations/pending/`.
The agent and the user work through it together over one or more sessions —
drafting a plan, applying changes, then archiving the result. This skill is
how the agent navigates that lifecycle.

Migration is also the upstream-source-version transition primitive. Use it for
every upstream Schema change, every adopted third-party spec version change
(A2A, ACP, Cilium CRDs, kagent CRDs if adopted), and every auditable data-fix.
The Migration records the exact source version transition through
`source_api_version`, `source_processkit_version`, `target_api_version`, and
`target_processkit_version`; `pk-doctor` treats missing version metadata as a
schema vocabulary error for v2 content.

Two subtype patterns are canonical:

- `Migration{kind=schema-extension}` documents an extension to a Schema
  vocabulary such as `Artifact.spec.known_kinds` or
  `Binding.spec.known_types`.
- `Migration{kind=data-fix}` documents a correction to already-emitted data.
  For LogEntry repair, the original event is superseded by reference and never
  deleted; this preserves the append-only event-log invariant.

## Overview

### The migration directory layout

```
context/migrations/
├── INDEX.md                    ← always-loaded summary of all migrations
│
├── pending/                    ← briefings waiting for human review
│   └── MIG-<id>.md
│
├── in-progress/                ← migrations being worked on
│   └── MIG-<id>.md
│
└── applied/                    ← completed migrations (historical record)
    └── MIG-<id>.md
```

The directory the file lives in **mirrors** the entity's `spec.state`. Moving
the file is part of the state transition — `transition_migration` does both
the file move and the spec update atomically.

### The lifecycle

```
                ┌──────────────┐
                │   pending    │ ← host sync writes new migrations here
                └──────┬───────┘
                       │ user reviews briefing, approves a plan
                       ▼
                ┌──────────────┐
                │ in-progress  │ ← agent works through plan, updates progress_notes
                └──────┬───────┘
                       │ all plan items done, user accepts
                       ▼
                ┌──────────────┐
                │   applied    │ ← terminal, kept as history
                └──────────────┘

      Either pending or in-progress can transition to `rejected`
      (terminal side branch — "we looked at this and decided not to take it")
```

### Always-loaded INDEX.md

`context/migrations/INDEX.md` is a small file the agent loads at session start.
It summarizes every migration's state and the next action. Update it whenever
you transition a migration. Sample shape:

```markdown
# Migrations Index

## Pending (2)

- **MIG-bright-owl** — processkit v0.3.0 → v0.4.0 (generated 2026-04-15)
  4 affected skills, 2 affected processes, 8 new entities, 1 removal
- **MIG-calm-river** — aibox 0.14.4 → 0.15.0 (generated 2026-04-12)

## In progress (1)

- **MIG-quick-hawk** — processkit v0.2.0 → v0.3.0 (started 2026-04-08)
  Plan: 6 items, 4 done. Next: migrate workitem-management overrides.

## Applied (4)

| Date       | Migration                                |
|------------|------------------------------------------|
| 2026-04-15 | MIG-... — processkit v0.1.0 → v0.2.0     |
| 2026-03-20 | MIG-... — aibox 0.13.0 → 0.14.0          |
```

### Workflow when starting a session

1. Read `context/migrations/INDEX.md` — get the migration state at a glance.
2. If anything is in `pending/` and the user hasn't asked about something
   else, surface it: "There's a pending migration MIG-bright-owl from
   processkit v0.3.0 to v0.4.0. Do you want to review it now?"
3. If anything is in `in-progress/`, surface it: "We're 4/6 of the way
   through MIG-quick-hawk. Want to continue?"
4. Otherwise proceed with the user's request.

### Workflow for a pending migration

1. **Read the briefing** — open the file in `pending/`. The body has a
   summary, list of affected files (with classification), new additions,
   removals.
2. **Draft a plan** — propose a project-specific migration plan to the
   user. Keep it small: each item is one concrete action ("update the
   release process to call the new gate", "rename `foo` references in
   our overrides", etc.). Prefer many small items over a few big ones.
3. **Get approval** — show the plan, ask for explicit approval. Do NOT
   start changing files until approved.
4. **Transition** — when approved, set `spec.state: in-progress`, set
   `spec.plan: <approved plan>`, and **move the file** from `pending/`
   to `in-progress/`.
5. **Update INDEX.md**.

### Workflow for an in-progress migration

1. Read `spec.plan` and `spec.progress_notes` — figure out where you are.
2. Pick the next plan item, do the work, get user confirmation per item
   if non-trivial.
3. Append a `progress_note` to `spec.progress_notes` after each completed
   item — date, actor, what was done.
4. When all items are done, ask the user to accept. On acceptance:
   - Set `spec.state: applied`, set `spec.applied_at` and `spec.applied_by`
   - Move the file from `in-progress/` to `applied/`
   - Update INDEX.md
   - Optionally write a `LogEntry` (`event_type: migration.applied`)

### Rejecting a migration

If the user decides not to take an upstream change:
- Set `spec.state: rejected`, `spec.rejected_reason: "..."`
- Move the file from `pending/` (or `in-progress/`) to `applied/`
  (rejected migrations live in `applied/` because that's their terminal home —
  "applied" here means "decision finalized", not "code applied")
- Future host sync runs see this migration in `applied/` and do NOT
  re-propose the same transition.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Drafting a Migration without a rollback plan.** Every Migration
  must answer "what happens if this fails halfway through". A
  Migration without rollback is a one-way door — and one-way
  doors deserve much more scrutiny than the typical Migration
  flow allows. State the rollback explicitly even when it's
  "manual restore from backup".
- **Running a Migration without a dry-run pass.** Always preview
  the changes before applying. A dry-run that shows the diff
  surfaces typos, ordering issues, and unintended scope before
  they hit the live tree.
- **Forgetting to log `migration.applied` (and `migration.failed`).**
  The audit trail is how the next Migration knows where the last
  one stopped. Skipping the log strands future maintainers.
- **Sequencing dependent Migrations wrong.** If Migration B
  assumes the state Migration A produced, applying B before A is
  guaranteed corruption. Use the `depends_on` field and verify
  the dependency graph before scheduling.
- **Migration markers without actual diffs.** Don't create a
  Migration entity for "fix the thing" if there's no concrete
  before/after state. Migrations are records of mechanical
  transitions, not aspirational notes.
- **Treating "no-op migrations" as harmless.** A Migration that
  does nothing should not exist — delete it. Otherwise it
  pollutes the audit trail with phantom transitions.
- **Editing an applied Migration after the fact.** Migrations are
  immutable history. If the Migration was wrong, write a NEW
  Migration that corrects it (`migration.corrected`), don't
  rewrite the old one.

## Full reference

### Migration entity shape

See `src/primitives/schemas/migration.yaml` for the authoritative schema.
Frequently-used fields:

| Field | Type | Notes |
|---|---|---|
| `source` | string | `aibox`, `processkit`, `processkit-acme`, ... |
| `from_version` | string | semver tag |
| `to_version` | string | semver tag |
| `state` | enum | `pending` / `in-progress` / `applied` / `rejected` |
| `summary` | string | one-line for INDEX.md |
| `affected_files` | list[object] | path + classification per file |
| `affected_groups` | list[string] | logical groups touched |
| `plan` | string | the approved migration plan (markdown) |
| `progress_notes` | list[object] | append-only progress log |

### Data-fix migrations are required for legacy shapes

Compatibility shims are temporary aids for discovering drift, not a
terminal state. When pk-doctor reports legacy vocabulary, non-canonical
IDs, filename-policy drift, wrong directory layouts, placeholder
timestamps, or stale references, record a `kind: data-fix` Migration
that names every affected file and the canonical target shape. Apply
the migration through migration-management MCP tools so indexes,
schemas, state-machine transitions, and event logs stay consistent.

Do not resolve strict schema/storage drift by adding project-local
`legacy_known_*` allowlists or by documenting a permanent policy
exception. If a legacy value should become current vocabulary, ship an
explicit schema migration that adds it to the authoritative
`known_*` field before new entities use it.

### The five file classifications

| Classification | Meaning |
|---|---|
| `changed-upstream-only` | Upstream changed it, the user has not touched it. Safe to take the new version with one approval. |
| `changed-locally-only` | The user has edited it, upstream is unchanged. No-op for this migration — but worth flagging that the file diverges. |
| `conflict` | Both have changed. Must be resolved by hand (or by agent + user). Highest priority. |
| `new-upstream` | Upstream added a new file. Decide whether to take it. |
| `removed-upstream` | Upstream removed a file the project still uses. Decide whether to remove locally or keep as a project-local fork. |

### Why migrations are tracked entities, not just markdown files

Three reasons:
1. **Queryable.** The `index-management` MCP server indexes them. An agent can
   ask "what migrations are pending?" without filesystem walking.
2. **State machine validation.** Transitions are validated by the migration
   state machine — you cannot accidentally move a file from `applied/` back
   to `pending/`.
3. **Cross-referenceable.** A `WorkItem` can reference a `Migration`
   (`spec.related_migrations: [MIG-bright-owl]`), so if a migration spawns
   work, the agent can find the linkage. Same for `DecisionRecord`.

### Interaction with PROVENANCE.toml

When a host sync tool generates a Migration, it diffs the
`PROVENANCE.toml` files of the old and new upstream versions. This gives
the change set without having to walk every file. The diff script
(`scripts/processkit-diff.sh`) is the canonical implementation; host
installers can call it or reimplement its logic.

### Interaction with the upstream reference templates

The project's `context/templates/processkit/<version>/` directory holds
a verbatim copy of every file shipped by the pinned processkit release
(installed and refreshed by the host installer). The migration's
`affected_files` classification is computed by comparing three SHAs on
the fly:

- **template SHA** — read from
  `context/templates/processkit/<version>/<file>` (the as-installed
  reference)
- **cache SHA** — what upstream NOW says (from the host installer's
  runtime cache, fetched from the pinned processkit tag)
- **live SHA** — what's in the project right now

Three SHAs → five classifications. See the host installer migration
generation logic for the truth table. The pinned source URL + version +
resolved commit live in the project lockfile at the project root
(Cargo-style), not in a separate manifest file.

### Agent-facing MCP tools

This skill ships an MCP server — see
[`mcp/SERVER.md`](mcp/SERVER.md) for the contract. The server exposes
six tools that together cover the full lifecycle: `list_migrations`
and `get_migration` for discovery, `start_migration` for the
`pending → in-progress` edge, `apply_migration` for the terminal
`in-progress → applied` edge (with implicit-start support from a
pending file), and `reject_migration` for the
`{pending, in-progress} → rejected` branch. Every write-side tool
stamps the appropriate timestamp (`started_at` / `applied_at` /
`rejected_at`), moves the file between the `pending/`, `in-progress/`,
and `applied/` directories, refreshes `context/migrations/INDEX.md`
(preserving the hand-written Notes column and the trailing
`## CLI Migrations` section), and writes a `migration.*` event via the
side-effect log helper.

`normalize_migration_filename(id, target_id)` is the narrowly-scoped,
audited repair path for a Migration that violates the canonical
`MIG-YYYYMMDD_HHMM-WordPair` policy. It is safe for applied/rejected history:
the tool writes the corrected record before removing the old path, rewrites
exact ID references only in mutable canonical files, regenerates the migration
index, rebuilds SQLite, and emits `migration.filename-normalized`. It never
rewrites LogEntries or other terminal Migration records; that event preserves
the old-to-new ID bridge.

In gateway deployments, these tools are available only when
migration-management is present in the installed/merged MCP
configuration. The gateway must not infer or expose unrelated
processkit servers from this skill's documentation.

`list_migrations()` without arguments is intentionally an active-work
view: it returns only `pending` and `in-progress` migrations. Historical
`applied` and `rejected` migrations accumulate for the life of a project
and must be requested explicitly with `state="applied"` or
`state="rejected"` to avoid filling status/resume context.

### What this skill does NOT do (yet)

- **Generate** migrations — that's the host installer/sync tool's job.
- **Apply file changes** — the agent does the actual edits as part of
  walking the plan. This skill describes the workflow but doesn't ship a
  tool that auto-edits.
