---
name: "Roadmap: Create"
description: "Create a project roadmap in the rich phase-array format: roadmaps.json as source of truth plus a PHASE task list and prose overview"
when_to_use: "When a project has no roadmap yet, or an existing simple-style one needs superseding with a new phase built from scratch (for converting an old roadmap, use roadmap:migrate instead)."
model: fable
effort: high
metadata:
  glyph: ᚠ
  family: roadmap
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(python3:*)"]
arguments: ["phase"]
argument-hint: "[phase name (optional, e.g. PHASE_1)]"
---

Create a roadmap as three synchronised artefacts:

- `.claude/roadmaps.json`: machine-readable **source of truth**, an **array of phase objects** each `{name, path, archived?, externalGates, milestones}`. The active phase is the entry without `archived: true`; archived entries are retained as historical record.
- `docs/roadmaps/{PHASE}.md`: human-readable task list and dependency diagram (a projection).
- `docs/reports/ROADMAP_OVERVIEW.md`: prose overview (a projection).

When creating a new phase alongside existing ones, append a new element and mark the superseded phase `"archived": true`.

Shared conventions (status vocabulary, colour table, graph rules, formatting) live in `${CLAUDE_PLUGIN_ROOT}/references/roadmap-conventions.md`; read it before writing anything. The CLI is `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py`.

## Behaviour

| Codebase Context  | Arguments Passed | Action |
|-------------------|------------------|--------|
| No other roadmaps | 0                | Propose a phase name drawn from the project's goal and confirm it |
| N/A               | 1                | Create the roadmap/phase named in the argument |
| Roadmaps exist    | 0                | Ask the user which phase to create or if starting a new phase |

## Steps

### 1. Determine scope, context and format

- Check if `docs/roadmaps/` exists and contains roadmaps; check if `.claude/roadmaps.json` exists.
- If `$ARGUMENTS` is given, use it as the phase name (e.g. `PHASE_2`). If no arguments and no existing roadmap, propose a phase name drawn from the project's goal and confirm it; never default to a bare `PHASE_1`. If no arguments but roadmaps exist, ask the user to clarify intent.
- **If a roadmap already exists, check its format first**: run `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py detect`. Exit **3** = old simple format: **stop and tell the user to run the `roadmap:migrate` skill first**, so the new phase is appended to a consistent phase array. Exit **2** = could not locate/parse: ask the user for the path. Only proceed on exit 0 (or when no roadmap exists yet).

### 2. Gather project context

Read what is available to understand the project: `README.md`, `CLAUDE.md`, `docs/` (architecture, proposals, ADRs) and any existing roadmaps in `docs/roadmaps/`.

### 3. Elicit the work; let the structure emerge

Feature first, structure second: milestones reveal themselves as the conversation groups the work, so never open with "how many milestones?". Ask targeted questions (2–3 per round, not a long form):

- **The work:** what must exist by the end of this phase? What's frustrating enough to fix, and what does each piece unlock?
- **Grouping (proposed, not demanded):** once the features are on the table, propose a milestone grouping (typically 3–5, each with a goal and completion criterion) and 2–3 letter category prefixes (e.g. `EV` = evaluation, `IN` = ingestion). The user corrects a concrete proposal rather than designing structure cold.
- **Dependencies:** which groups are sequential vs parallel; any known external blockers or prerequisites.
- **Assignees (optional):** if the user wants to attribute tasks to people up front, ask who owns what. Never infer an assignee from category, milestone or anything else; leave it unset for any task the user doesn't name an owner for.

For a big batch of half-formed ideas, `roadmap:create-interview` is the deeper feature interview; its approved proposal can seed this step's grouping.

### 4. Assign task IDs

Format: `{MilestoneNum}{Category}.{Seq}`, e.g. `1EV.1`, `3IN.6`. Sub-tasks use an alpha suffix: `3IN.2a`. Never reuse an ID; number sequentially within each category; new tasks append (never renumber).

### 5. Compute initial statuses (mechanical)

The mechanical status rule from the conventions reference applies: empty `dependsOn` → `todo`; any non-`done` dependency → at least `blocked`, escalating under `deferred > paused > blocked > todo` when a dependency is itself parked. No task starts `done` unless the user says the work is already complete. A root-seeded `paused`/`deferred` (empty `dependsOn`) is only for tasks parked behind a gate or a later phase from the outset. `softDependsOn` never feeds this rule.

### 6. Generate `.claude/roadmaps.json`

The top level is an **array of phase objects**. Append + archive the superseded phase if others exist; otherwise write a one-element array. Tabs for indentation, British spelling.

```json
[
  {
    "name": "{Phase Name}",
    "path": "docs/roadmaps/{PHASE}.md",
    "archived": false,
    "externalGates": [],
    "milestones": [
      {
        "id": "M{N}",
        "name": "{Milestone Name}",
        "goal": "{One-sentence objective}",
        "tasks": [
          { "id": "{ID}", "description": "{Task description}", "status": "todo", "dependsOn": [] }
        ]
      }
    ]
  }
]
```

- Task and gate field order follows the conventions reference (a new task never carries `started`: claims come from starting work). Include `softDependsOn`/`softMilestone`/`notes`/`iterative`/`assignee` only when meaningful; `assignee` is free-text with no roster, and must never be guessed.
- **External gates** (`externalGates`, per phase, beside `milestones`) model things outside the team's control that block work: `{id, name, status:"external", imposes?, blocks[], notes?}`. `imposes` (default `blocked`; may be `paused` or `deferred`) is the status the gate forces on its blocked children; `blocks[]` is the reverse edge: every task ID that lists this gate in its `dependsOn`. A gate ID can appear in a task's `dependsOn`.
- A `dependsOn` entry may be a **milestone ID** (`M1`, `MP`…): it resolves `done` only when every task in that milestone is `done`.
- The `iterative: true` flag marks a task that loops to convergence: descriptive only, never a cyclic `dependsOn`.
- A `softDependsOn` entry authors an optional, best-effort link that renders dotted in the diagram (`X -.-> Y`) but imposes no status, no cycle constraint and no sink effect (full semantics in the conventions reference). Use it for relationships worth showing but not worth blocking on; never hand-draw a dotted line into the generated diagram instead.

### 7. Generate `docs/roadmaps/{PHASE}.md`

````markdown
# {Project Name} {Phase} Roadmap

{1–3 sentence intro.}

**Critical path:** `{key IDs in sequence}`; {brief explanation}.

---

## Milestone 1: {Name}

**Goal:** {Milestone objective}

- [ ] **{ID}**: {description}
- [ ] **{ID}**: {description} _(depends on {ID})_
- [ ] **{ID}**: {description} _(blocked: depends on {ID}, {ID})_
  - Note: {optional note}

---

## Dependency Diagram

```mermaid
{output of roadmap.py graph --mermaid}
```
````

Task line annotations follow the conventions reference (none / `_(depends on {IDs})_` / `_(blocked: depends on {IDs})_` / `_(paused: reconvene {gateId})_` / `_(deferred to a later phase)_` / the tier-gated `_(deferred: {gateId}, and every {tier} milestone)_` and `_(deferred: follows {ID})_` forms — see Tiers in the conventions reference).

**The diagram is generated, never hand-written.** Once the JSON is written, run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py graph --mermaid --direction LR
```

and paste the output verbatim into the fenced `mermaid` block. It emits the classDefs (canonical status colours), nodes, edges (terminal milestone convention) and `class` statements in the right order. Do not add, remove or recolour lines by hand.

### 8. Generate `docs/reports/ROADMAP_OVERVIEW.md`

```markdown
# {Project} {Phase}: Roadmap Overview

**{N} tasks across {M} milestones.** Files: `.claude/roadmaps.json` (machine-readable), `docs/roadmaps/{PHASE}.md` (full task list with Mermaid dependency diagram).

> {Rescope/context note if relevant}

---

## What we're building
{2–3 paragraphs on the key deliverables and the reasoning behind the phase structure.}

## Milestone sequence and the reasoning behind it
{One paragraph per milestone.}

## Decisions that shaped the structure
{Key decisions that explain non-obvious choices.}

## External blockers (flag early)
{Dependencies on external parties, unconfirmed decisions, etc.}
```

The header task count must match `roadmaps.json`. Get it from `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py stats` rather than counting by hand.

### 9. Validate, confirm and report

1. Run `python3 "${CLAUDE_PLUGIN_ROOT}"/scripts/roadmap.py validate`; it must report clean (dependsOn/blocks parity, acyclicity, status recompute). Fix any discrepancy before finishing.
2. Report the three paths created, the milestone and task counts (from `roadmap.py stats`), and the status breakdown.
3. Note any assumptions or areas needing user refinement.

---

## Conventions

- ID format `{MilestoneNum}{Category}.{Seq}`; never reuse IDs.
- roadmaps.json is the source of truth; the PHASE file and overview are projections.
- Everything else (statuses, colours, graph rules, formatting): `${CLAUDE_PLUGIN_ROOT}/references/roadmap-conventions.md`.

These roadmaps are maintained by `roadmap:maintain` (status synchronisation) and `roadmap:update-tasks` (adding tasks, or a single new milestone via its `m` mode). Old simple-format roadmaps are upgraded by `roadmap:migrate`; the HTML dashboard comes from `roadmap:dashboard` (`roadmap.py render`).

The two skills split by scope, not by capability overlap: this skill (`roadmap:create`) builds an entire phase from scratch, multiple milestones at once, when none exists yet or an old one is being superseded wholesale. `roadmap:update-tasks m` appends exactly one milestone to a phase that already exists. Reach for this skill only in the "no roadmap yet" / "starting a new phase" cases in the Behaviour table above; a single new milestone inside a live phase is the other skill's job.
