---
name: ingest-pipeline
description: >
  The ingest pipeline's topic-tree plan format and confirmation gate, the opt-in
  destructive optimize (restructure) procedure, and the final-report template
  for claude-wiki-pages. Documents the plan/approval and restructure steps so the
  ingest agent can drive them without inlining the detail. Trigger when an agent
  or user asks "how does ingest plan the topic tree", "how does the optimize
  restructure work", or invokes /claude-wiki-pages:ingest-pipeline. Reference,
  not action.
allowed-tools: Read
disable-model-invocation: true
---

# Wiki Ingest Pipeline — Plan & Optimize Procedures (reference)

The Step 1.4 topic-tree plan + confirmation gate, the Step 3 optimize
(destructive restructure) procedure, and the final-report template for
`claude-wiki-pages-ingest-agent`. The agent reads this skill at the start of
Step 1.4 and Step 3, and when composing the final report. Schema authority
remains `vault/CLAUDE.md`; the contract, preflight, page-write steps, auto-heal
delegation, synthesis, model selection, and hard rules live in the agent body.
Every page the pipeline produces follows the house voice —
see [`skills/voice`](../voice/SKILL.md): a one-line plain-language definition
first, then typed content in the engineer register, no marketing inside the vault.

## Step 1.4 — Plan the topic tree (externalize, then confirm)

The topic-tree shape is the most consequential decision of the run. Errors here
cascade into every page's `parent:` and `path:`, and into the Obsidian graph
structure. Externalize the plan so the user can review or edit before any page
is written.

> **PDF sources (`source_format: pdf`):** when a source is a PDF under
> `raw/assets/`, apply the PDF ingest path documented in
> `skills/ingest/SKILL.md` — "PDF sources (I4): `source_format: pdf`" — before
> planning the topic tree. The required fields (`source_format: pdf`,
> `attachment_path`, `extracted_at`) must appear in the source note, and the
> PDF remains immutable in `raw/assets/` throughout. Classification and dedup
> proceed identically to text sources.

### 1.4a — Write the plan

Write to `vault/output/_pipeline-plan-YYYY-MM-DD.md` (git-ignored; no frontmatter required). Structure:

```
# Ingest plan — YYYY-MM-DD

## Sources in this run
- <source-1.md> — N entities, M concepts
- <source-2.md> — N entities, M concepts
...

## Entities and concepts extracted

> For each extracted item, apply the **classification checklist** in
> `skills/ingest/SKILL.md` — assign exactly one `type` (and, for entities,
> one `entity_type`) drawn from `ontology-profile-v1` in `vault/CLAUDE.md`.
> Never invent out-of-enum values; flag ambiguous cases for human review.
>
> Also apply the **two-pass alias-aware dedup** from `skills/ingest/SKILL.md`
> before marking any item as `new`. Pass 1 = exact title match; pass 2 =
> alias-aware match against existing pages' `aliases` fields. Mark items as
> `existing` if either pass matches, and plan an additive extension (never a
> duplicate). See "Dedup: two-pass existence check (I2)" in
> `skills/ingest/SKILL.md` for the full procedure.

- [<new|existing>] <Entity/Concept name> — `type: <type>` (entity: `entity_type: <value>`) — from <source(s)>
...

## Proposed topic tree

wiki/<existing-or-new-topic>/
├── <topic>.md                   [new | existing]   # folder note (legacy _index.md if already present)
├── <page>.md                    [new | update]
├── <subtopic>/                  [new | existing]
│   ├── <subtopic>.md            [new | existing]   # folder note
│   └── <page>.md                [new | update]
...

## Folder size check
- <topic>/: N direct children (target ≤ 12)
- <topic>/<subtopic>/: N direct children (target ≤ 12)

## Graph color groups needed
- <new-top-level-topic> → next palette color
- (or: none)

## Open decisions
- <any ambiguities the model resolved — e.g., "placed X under Y instead of Z because …">
```

The plan must obey `vault/CLAUDE.md` folder-hierarchy rules (max depth 4, grouped by semantic domain, every folder gets a folder note `<folder>/<folder>.md`) and ingest-specific sizing:

- **Target ≤ 12 pages per folder.** Plan subtopic folders up front if exceeded.
- Entities cluster into `roles/`, `tools/`, or named subtopic folders.
- Deliverables/build items/templates cluster into `deliverables/` or `templates/`.
- Blockers/decisions/project-tracking cluster into `blockers/` or `project/`.
- Process concepts (flows, tiers, triggers) stay in the parent topic folder.

### 1.4b — Confirmation gate

Report to the user:

```
Ingest plan written to vault/output/_pipeline-plan-YYYY-MM-DD.md.

Summary:
- N new sources, M total entities/concepts
- N new folders, N updated folders
- N pages will be created, M pages will be updated
- Graph color groups to add: N

Review the plan. Options:
  (a) Approve — proceed to write pages
  (b) Edit the plan file, then approve — I'll re-read before proceeding
  (c) Abort — no pages will be written
```

**Stop. Wait for explicit approval before continuing.** If the user edits the plan file, re-read it before 1.5. If the user aborts, log the abort to `wiki/log.md` and exit:

```
## [YYYY-MM-DD] ingest-aborted | Plan declined
Plan at vault/output/_pipeline-plan-YYYY-MM-DD.md. N sources left unprocessed.
```

## Parallel-extract fan-out and EXTRACT envelope (P1-A2, P1-A3, P1-A4)

This section documents the map-only parallel-extract design for the
`claude-wiki-pages-ingest-agent`. The ingest-agent reads this section at
Step 1.2b. All invariants below are gate-tested by
`tests/scripts/extract-worker-frontmatter.bats` and the determinism replay
gate (P1-A8).

### Typed EXTRACT envelope

An extract worker returns a fenced YAML block (`extract_envelope:`) in its
text response. The envelope carries:

- **`source_path`** — the assigned raw source path (relative to vault).
- **`items[]`** — extracted entities, concepts, topics, projects, and
  synthesis candidates, each carrying:
  - `slug_candidate` — kebab-case hint; the writer canonicalizes via the
    two-pass alias-aware dedup (I2, `skills/ingest/SKILL.md`).
  - `type` — legal value from `ontology-profile-v1` in `vault/CLAUDE.md`.
  - `entity_type` — required when `type: entity`; legal value from the same
    profile.
  - `title`, `summary`, `source_quotes[]`, `confidence`, `derived`.
  - `out_of_enum: true` + `review_reason` when no legal type fits (the
    writer routes these to `_proposed/`).
- **`predicates[]`** — typed relationships (`subject_candidate`,
  `predicate`, `object_candidate`).
- **`implied_folders[]`** — folder/index nodes implied by new topics.
- **`source_note`** — title, author, publisher, date, url, summary, key
  claims for the source summary page.
- **`error`** — empty on success; non-empty signals worker failure
  (SKIP-AND-BACKLOG).

Workers return `{slug_candidate, extracted content}` only — **never a
create/update verdict** and **never a final slug**. Create vs update and
slug canonicalization are the single writer's exclusive responsibilities.

### Closed-vocabulary enforcement

Every `type` and `entity_type` in the envelope must be a legal value drawn
from `ontology-profile-v1` in `vault/CLAUDE.md`. Workers must not invent
out-of-enum values. When an item has no legal type, workers set
`out_of_enum: true` + `review_reason`; the writer routes those items to
`_proposed/` with the reason logged, and they are never written directly to
`wiki/` with a guessed heading.

### Single-writer dedup and coalesce contract

The ingest-agent (the single writer) is the only entity that creates or
updates wiki pages. It receives N envelopes (one per source) and:

1. **Two-pass alias-aware dedup (I2).** For each `slug_candidate` in the
   envelopes, run the two-pass existence check defined in
   `skills/ingest/SKILL.md` ("Dedup: two-pass existence check"):
   - Pass 1: exact title match (case-insensitive) against existing pages.
   - Pass 2: alias match against existing pages' `aliases` fields.
   If either pass matches, this is an **update** (additive merge);
   otherwise it is a **create**.

2. **Cross-envelope coalesce.** Multiple envelopes may propose the same
   entity (different sources, different alias forms). Before deciding
   create vs update, group all envelope items by canonical title (after
   applying the string-identity resolver from PR #29). For each group:
   - **Union `sources`** — every contributing source appears in the
     final page's `sources` list.
   - **Union `related`** — all cross-references are preserved.
   - **`max()` confidence** — take the highest confidence value from
     contributing items (the reinforce rule: more sources = more
     confident).
   - **`derived: true` only if ALL contributors are derived** — if any
     contributor is non-derived, the merged page is non-derived.
   - **Stable sort by canonical title** — ensures byte-identical output
     regardless of envelope arrival order.

3. **Execute in stable canonical-title order.** Apply creates and updates
   in this fixed order. The result is byte-identical at `maxParallelExtract=1`
   vs N with shuffled worker returns because the sort is stable over the
   canonical title key, which does not depend on arrival order.

4. **Log once per source.** The single writer appends to `wiki/log.md`
   and is the only appender (ordered `wiki/log.md` invariant from TEAM-BRIEF §5).

### Byte-identical guarantee

At `maxParallelExtract=1`, no Task fan-out occurs; the agent reads and
extracts inline — output is byte-identical to the pre-feature baseline. At
`maxParallelExtract>1` with shuffled worker return order, the stable-sort
coalesce ensures the written pages and `log.md` source order are
byte-identical to the `=1` run. This is the mechanical determinism
guarantee required by D5/D8.

### SKIP-AND-BACKLOG on worker failure (OQ-5)

When an extract worker fails (missing envelope block, non-empty `error`
field, or timeout), the ingest-agent:

1. Records that source as unprocessed backlog (not as a processed source in
   `wiki/log.md`).
2. Continues applying all successfully validated envelopes.
3. The single `snapshot.sh post` at Step 1.9 covers exactly the applied
   subset — it is a single revertible unit.
4. The final report lists failed sources under "Worker failures" with the
   error reason.

This matches the existing 25-cap-then-backlog semantics: forward progress
is preserved and the snapshot range remains revertible.

## Structured record sources — fan-out mode (ADR-0036 #57)

When a raw source is a **JSON, YAML, or CSV array** (a glossary, catalogue, or
dataset where every row is an independent page), skip the normal single-source
extraction path and use `expand-records.ts` instead. This mode is a first-class
fan-out: one page per record, hub folder-notes per category, and a `parent:`
spine all born tree-shaped — no `strict-tree-reduce` pass needed afterwards.

### When to trigger

- Source file extension is `.json`, `.yaml`, `.yml`, or `.csv`.
- Top-level value is an array (confirmed by reading the first 5 lines).
- Records share a common id/name/category structure (a glossary, taxonomy, or
  entity catalogue).

### How to invoke

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/expand-records.sh" \
  --target <vault> \
  --source raw/<file.json> \
  --topic <target-topic-folder> \
  [--id-field id] \
  [--title-field name] \
  [--hub-field category] \
  [--tag-fields "family,severity,principle"] \
  [--type concept] \
  --json
```

Dry-run first (omit `--apply`) to review the page plan. Then pass `--apply` and
run inside a git checkpoint (`bash scripts/snapshot.sh pre --target <vault>`).

### Output shape

For a record `{id:"srp", name:"Single Responsibility Principle", category:"solid-principles", family:"oop", severity:"high"}` with `--topic principles`:

```
wiki/_sources/glossary.md                              ← source note (type: source, auto-created)
wiki/principles/solid-principles/solid-principles.md   ← hub folder-note (type: index)
wiki/principles/solid-principles/srp.md                ← record page
  tags: ["family/oop", "severity/high"]
  parent: "[[solid-principles|Solid Principles]]"
  sources: ["[[glossary|Glossary]]"]
```

The hub folder-note has `parent: "[[principles|Principles]]"`, closing the
spine to the topic root. The source summary note (`wiki/_sources/<file>.md`) is
auto-created when absent so every record page's `sources:` link resolves —
provenance is born intact, not just the tree shape. An existing source note
(e.g. one a prior ingest already wrote with richer metadata) is never
overwritten. All cross-record associations are expressed as `family/<x>`,
`severity/<x>`, `principle/<x>` nested tags — no wikilinks — so the graph draws
clean topic islands from day one.

### Confirmation gate

After the dry-run, report to the user:

```
expand-records plan for raw/<file>:
- N records → N pages in wiki/<topic>/
- N hub folder-notes: <list>
- Tag fields: <fields>
- Pages already existing (will skip): N

Review the plan. Options:
  (a) Approve — run with --apply
  (b) Adjust (change --hub-field, --tag-fields, --topic) — re-plan
  (c) Abort
```

Stop and wait for explicit approval before passing `--apply`.

---

## Step 3 — Optimize (opt-in, destructive)

**This step restructures folders with `git mv` and rewrites `parent:`/`path:` across many pages. It requires explicit user confirmation.**

### 3.1 Audit

Count pages per folder. Identify folders with > 12 direct `.md` children (excluding the folder's own index note). If none, skip Step 3 entirely and report "no optimization needed".

### 3.2 Plan and confirm

Write the restructure plan to `vault/output/_restructure-plan-YYYY-MM-DD.md`
(git-ignored; no frontmatter required). Structure:

```
# Restructure plan — YYYY-MM-DD

## Proposed restructure

<folder-a>/ (18 pages) → split into:
  <folder-a>/subtopic-x/  (<count> pages: <list>)
  <folder-a>/subtopic-y/  (<count> pages: <list>)

<folder-b>/ (14 pages) → split into:
  ...

## Summary
- Cross-links to add: N
- Files to move: N (git mv)
- Frontmatter rewrites: N (parent/path fields)
```

Report to the user:

```
Restructure plan written to vault/output/_restructure-plan-YYYY-MM-DD.md.

Options:
  (a) Approve — execute the restructure
  (b) Edit the plan file, then approve — I'll re-read before executing
  (c) Decline — skip Step 3, proceed to Step 4
```

**Stop. Wait for explicit approval before continuing.** If the user edits the plan file, re-read it before 3.3. If the user declines, skip to Step 4.

### 3.3 Execute

Only after explicit confirmation:

1. Create subtopic folders, each with its folder note (`<subtopic>/<subtopic>.md`).
2. Move each page into the correct subtopic — try the backlink-safe path first:
   `bash ${CLAUDE_PLUGIN_ROOT}/scripts/obsidian-rename.sh --target <vault> --from <old-rel.md> --to <new-rel.md>`.
   On exit 3 (`[skip] cli-rename: …`), fall back to `git mv`. Exit 0 means
   Obsidian also updated any path-form backlinks; title-form `[[wikilinks]]`
   are unaffected by moves in either branch.
3. Update each moved page's `parent:` and `path:` (both branches — Obsidian
   does not know our frontmatter schema).
4. Update the parent folder note: remove moved children from `children:`, add subfolder entries to `child_indexes:` (quoted `"[[wikilink]]"` entries).
5. Update `wiki/index.md` to reflect new locations.
6. Add obvious `related:` cross-links (pages sharing 2+ sources, pages in the same new subtopic, pages referenced in body text).

### 3.4 One re-run of lint-fix

Invoke the `Task` tool with `subagent_type: claude-wiki-pages-curator-agent` and the
following prompt verbatim:

```
Run a post-restructure lint and fix pass. Pages were moved and new
folder notes were created. Verify parent/path, children arrays, and
index entries are consistent. This is the final pass.
```

Do not spawn a third run. Unresolved errors go into the final report.

### 3.5 Log

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] optimize | Tree restructure
Moved N pages into subtopic folders. Created N new folder notes.
Current tree: <summary>.
```

## Final report template

```
## Pipeline complete

### Step 1 — Ingest
- Plan: approved | edited-then-approved | aborted
- Plan file: vault/output/_pipeline-plan-YYYY-MM-DD.md
- Sources processed: N / N unprocessed  (backlog: N, if any)
- Source summaries created: N
- Entity pages created/updated: N / N
- Concept pages created/updated: N / N
- Divergences from plan: N  (list if any)

### Step 2 — Fix
- Issues found / fixed / unresolved: N / N / N

### Step 3 — Optimize
- Status: skipped | declined | executed
- Folders created: N
- Pages moved: N
- Wikilinks added: N

### Step 4 — Synthesize
- Synthesis notes created: N
- Pages scoped: N
- Gaps identified: N

### Current tree
<folder listing with page counts>

### Unresolved
<list anything still failing verify-ingest.sh>
```
