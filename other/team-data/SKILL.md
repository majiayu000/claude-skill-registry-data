---
name: team-data
description: "Orchestrate the Database Intelligence team for ProjectAegis.Data: schema design, SQLite migrations, provenance/audit modeling, deterministic data access, DOTS/ECS runtime exports, imports, validation, and database release trains."
argument-hint: "[schema|migration|import|sim-export|release-train|audit|full-scaffold] [scope] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
model: opus
agent: database-intelligence-lead
---

# Team Data — Database Intelligence Orchestration

Use this skill as the entry point for coordinated `ProjectAegis.Data` work. It
routes database architecture, modeling, implementation, and simulation export tasks
through the correct specialists and gates.

## Phase 0: Resolve Mode and Review Level

Modes:

- `schema` — design or review SQLite schema and C# entity mapping.
- `migration` — design/review SQLite migrations and repository changes.
- `import` — route new platform/weapon/sensor data through evidence, diff, rules, and human approval.
- `sim-export` — design deterministic runtime snapshots and DOTS/Burst data layouts.
- `release-train` — validate TL branch, scenario binding, DB versioning, rollback, and diffable drops.
- `audit` — run provenance, schema, deterministic, and release-readiness checks.
- `full-scaffold` — end-to-end plan for creating the `ProjectAegis.Data` assembly.
- No mode — infer from the user's request; if ambiguous, ask one focused question.

Review mode:
1. If `--review [full|lean|solo]` is present, use it.
2. Else read `production/review-mode.txt` if present.
3. Else default to `lean`.

## Team Composition

- **database-intelligence-lead** — orchestration, gates, handoffs, risk tracking.
- **database-architect** — schema boundaries, Data-layer API, write-routing, release trains.
- **database-modeler** — entity-to-table maps, provenance models, C# records, runtime DTOs.
- **database-engineer** — SQLite/.NET 8 implementation, migrations, repositories, tests.
- **sim-data-specialist** — deterministic snapshots, cache strategy, DOTS/Burst export data.
- **determinism-engineer** — replay and deterministic behavior risk review.
- **military-research-specialist** — source evidence and real-world parameter validation when importing content.
- **unity-dots-specialist** — Unity 6.3 DOTS/ECS implementation validation when runtime data crosses into Unity.

## Phase 1: Load Required Context

Read and summarize:

- `docs/architecture/architecture.md` — Data, Simulation, Bridge, Presentation layers; tick pipeline; layer rules.
- `Game-Requirements/requirements/06-Database-Intelligence.md` — provenance, audit, branching, validation, agent workflows.
- `docs/engine-reference/unity/VERSION.md` — Unity 6.3 LTS DOTS package constraints.
- Existing `src/**/*.csproj`, `ProjectAegis.sln`, and any `ProjectAegis.Data` files.
- Relevant ADRs in `docs/architecture/`.

Report whether `ProjectAegis.Data` exists and whether this is design-only,
implementation, or validation work.

## Phase 2: Select Workflow Pipeline

### Schema Pipeline

1. Spawn `database-architect` for assembly/API/schema boundary.
2. Spawn `database-modeler` for entity-to-table and table-to-runtime maps.
3. Run `/sqlite-schema-management` against the proposed schema.
4. Present PASS/CONCERNS/FAIL and ask whether to proceed to implementation planning.

### Migration Pipeline

1. Spawn `database-engineer` for migration/repository implementation plan.
2. Run `/sqlite-schema-management` for audit/provenance/constraint coverage.
3. Run `/deterministic-data-access` for read-path ordering and snapshot impact.
4. Require tests for migrations, rollback, failed transactions, and deterministic ordering.

### Import Pipeline

1. Spawn `military-research-specialist` for evidence/citation package.
2. Spawn `database-modeler` for entity resolution and diff shape.
3. Spawn `database-architect` for schema/rules validation and approval gate.
4. Require human approval before canonical merge.
5. Schedule re-index/relationship refresh after approval.

### Sim Export Pipeline

1. Spawn `database-modeler` for export DTOs and stable keys.
2. Spawn `sim-data-specialist` for snapshot/cache design.
3. Run `/ecs-data-optimization` for Burst/blittable layout.
4. Run `/deterministic-data-access` for snapshot hash and ordering rules.
5. If Unity-specific data structures are proposed, consult `unity-dots-specialist`.

### Release Train Pipeline

1. Spawn `database-architect` for TL branch and release model.
2. Run `/database-branching-release-train`.
3. Spawn `sim-data-specialist` to verify scenario binding and replay snapshot manifest.
4. Produce release/drop readiness verdict.

### Audit Pipeline

Run, in order:

1. `/sqlite-schema-management`
2. `/provenance-audit-modeling`
3. `/deterministic-data-access`
4. `/database-branching-release-train` if release/scenario data is in scope

## Phase 3: Decision Gates

At each gate, present options with trade-offs:

- Proceed to next phase.
- Revise schema/model/export shape.
- Create ADR before implementation.
- Defer implementation until dependencies/packages are approved.
- Stop due to blocking Requirement 06 violation.

Use `AskUserQuestion` for irreversible or costly decisions: schema shape,
dependency/package choice, migration strategy, snapshot format, release-train model,
or human-approval workflow.

## Phase 4: Implementation Handoff

If implementation is requested, hand the approved contract to `database-engineer`.
Before any file writes, confirm explicit paths and package approvals. Required
implementation evidence:

- Migration tests.
- Repository tests.
- Provenance/audit required-field tests.
- Constraint failure tests.
- Deterministic `ORDER BY` / snapshot hash tests.
- No UnityEngine references in `ProjectAegis.Data`.

## Output

Produce a concise orchestration report:

- Mode and scope.
- Agents/skills invoked or recommended.
- Architecture constraints satisfied/violated.
- Requirement 06 coverage table.
- Blocking decisions.
- Next approved action.
