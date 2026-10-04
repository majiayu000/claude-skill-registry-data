---
name: "Roadmap: Migrate"
description: "Convert an old simple-style roadmap (single Markdown, four statuses, <a name> anchors, roadmaps.json pointer registry) into the rich phase-array format (roadmaps.json source of truth + PHASE task list + prose overview)."
when_to_use: "When a project still has the old single-Markdown-file roadmap format and needs upgrading to the rich phase-array format before roadmap-create or roadmap-update-tasks can be used on it."
model: sonnet
effort: high
metadata:
  glyph: ᛊ
  family: roadmap
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(python3:*)", "Bash(git status:*)", "Bash(git stash:*)"]
arguments: ["roadmap"]
argument-hint: "[roadmap path or name (optional)]"
---

Upgrade an old **simple-format** roadmap to the **rich phase-array format** the other `roadmap-*` skills expect. This is a one-way structural rewrite of the source of truth, so it is user-initiated only (never model-triggered); the other skills detect the old format and point the user here.

**Old (simple) format:** a single `docs/roadmaps/{name}.md` is the source of truth, with `<a name="m{N}">` anchors, four sections (In Progress / To Do / Blocked / Completed), `- [ ]`/`- [x]` checkboxes, prose `— **depends on {IDs}**`, a `graph TD` diagram; `.claude/roadmaps.json` is a `{"roadmaps":[{name,path}]}` pointer registry.

**Rich format:** `.claude/roadmaps.json` is the source of truth: an **array of phase objects** `{name, path, archived?, externalGates, milestones}` with six statuses (`todo, blocked, paused, deferred, done, out_of_scope`), external gates, milestone/gate dependencies and a mechanical status recompute. `docs/roadmaps/{PHASE}.md` and `docs/reports/ROADMAP_OVERVIEW.md` are projections.

Shared conventions: `~/.claude/library/references/roadmap-conventions.md`. The CLI is `python3 "$HOME"/.claude/library/scripts/roadmap.py`.

## Steps

### 1. Locate and confirm it is old format

Resolve the roadmap: `$ARGUMENTS` path/name → `.claude/roadmaps.json` → `docs/roadmaps/` scan. Run `python3 "$HOME"/.claude/library/scripts/roadmap.py detect`:

- Exit **3**: old format, proceed.
- Exit **0**: already rich; tell the user there is nothing to migrate and stop.
- Exit **2**: could not locate; ask for the path.

Show `git status` and advise the user to commit or stash first: this overwrites the source of truth. Do not proceed with a dirty tree unless the user says so.

### 2. Parse the old Markdown

Read the `.md`. For each `<a name="m{N}">` milestone block, capture:

- Milestone number and name; the goal (`> **Goal:**` / `> [!IMPORTANT]` block).
- Tasks in each section (`m{N}-doing`, `m{N}-todo`, `m{N}-blocked`, `m{N}-done`): the ID, the description and any `— **depends on {IDs}**` clause. Note which section each came from (`doing`/`todo`/`blocked`/`done`).

Also parse the aggregated `graph TD` diagram for `{A} --> {B}` edges; merge these into each task's dependency set, so a dependency drawn only in the diagram (not written in prose) is not lost.

### 3. Derive milestones, tasks and dependencies

Build milestone objects `{id: "M{N}", name, goal, tasks:[…]}`. Each task: `{id, description, dependsOn:[…]}` with `dependsOn` the union of its prose depends-clause and its incoming Mermaid edges. The old format has no external gates → `externalGates: []`. Preserve any `- Note:` sub-bullets as a task `notes` field.

### 4. Assign statuses (seed, then recompute)

Seed each task's status from its old section, then let the recompute derive the rest:

- **Completed** (`- [x]`) → `done` (terminal seed, kept).
- **In Progress** → in the rich format, in progress is a **claim** (a `started` date), never a status, and the old format never said who or since when. Seed as `todo` (the recompute promotes it to `blocked` if it has non-`done` deps). **Record every task remapped this way** for the report: the user may want to re-seed one deliberately (e.g. `paused`).
- **To Do / Blocked** → leave unseeded; the recompute sets `todo` (empty/all-done deps) or `blocked` (any non-done dep).

Write the seeded JSON, then run `python3 "$HOME"/.claude/library/scripts/roadmap.py recompute` so every non-terminal status is *derived*, not carried over. This guarantees the migrated file passes validation immediately.

### 5. Write the phase-array `roadmaps.json`

Write a single phase object (or, if migrating one roadmap among several pointer-registry entries, an array; append this phase and mark others as needed). Structure, tabs, field order, British spelling exactly as `roadmap-create` Step 6. Set the phase `name` from the old roadmap name (or `$ARGUMENTS`), `path` to the `.md` it will regenerate (reuse the old path so existing links hold), `archived: false`, `externalGates: []`.

### 6. Regenerate the `.md` as a rich projection

Overwrite the old `.md` at the same path with the rich layout (see `roadmap-create` Step 7): milestone headings, `- [ ] **{ID}**: {description}` lines with status annotations, and a generated `graph LR` diagram; no `<a name>` anchors, no four-section structure, no `graph TD`. The diagram is the verbatim output of `python3 "$HOME"/.claude/library/scripts/roadmap.py graph --mermaid --direction LR` (terminal milestone edges, canonical colours, correct classDef placement; nothing hand-computed).

### 7. Generate `ROADMAP_OVERVIEW.md`

The old format had no prose overview. Synthesise a minimal one (see `roadmap-create` Step 8) from the milestone goals, with the header count from `python3 "$HOME"/.claude/library/scripts/roadmap.py stats`. **Flag the narrative sections as stubs** for the user to flesh out; do not invent decisions or rationale that weren't in the source.

### 8. Validate and report

Run `python3 "$HOME"/.claude/library/scripts/roadmap.py validate`: it must report clean; fix any discrepancy. Then report:

- Milestones and tasks migrated; the status distribution (`roadmap.py stats`).
- **In-Progress remaps**: every task that lost its in-progress state, so the user can claim any still under way (`roadmap.py claim <ID> --assignee <name>`, asking who) or re-seed one deliberately.
- Any dependency edges recovered **only** from the Mermaid diagram (not written in prose); worth a glance in case the diagram was stale.
- The three artefact paths written, and a note that `ROADMAP_OVERVIEW.md`'s narrative is a stub.

---

## Notes

- One-way: the old single-file model cannot be reconstructed from the rich format, hence the git-checkpoint advice. `disable-model-invocation` keeps it explicit.
- Statuses end up **derived**, not copied: the recompute is the source of truth for everything except `done`/`out_of_scope` seeds.
- Tabs not spaces; British spelling throughout. After migration, the roadmap is maintained by `roadmap-maintain`, extended by `roadmap-update-tasks`, and rendered by `artefact-roadmap`.
