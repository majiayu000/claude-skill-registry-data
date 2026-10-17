---
name: brokk-memory-curation
description: Distill reviewed findings into Yggdrasil Memory — the persistent, source-cited knowledge base; establish, consolidate, and prune entries.
---

# Memory Curation

## Purpose

Maintain the persistent, project-scoped Yggdrasil Memory by distilling reviewed research findings into durable, source-cited entries; establishing the knowledge base structure in new projects; and executing consolidation and deletion operations when tasked by the requesting agent.

Four tasks route through this skill: establishing the knowledge base structure, and the three entry-mutating operations — promotion, consolidation, and deletion. Every entry is grounded in reviewed sources and carries explicit metadata per the schema below.

## When to Use

- **Promotion (Remember):** When the requesting agent tasks you to distill reviewed research findings into Yggdrasil Memory entries. The requesting agent provides the reviewed Workfile path(s); you extract durable claims, cite their sources, and write them as new or updated entries.
- **Establishment:** When a project lacks a `.yggdrasil-memory/` directory and the requesting agent asks you to scaffold it. You create the directory structure, populate canonical templates, and initialize the manifest.
- **Consolidation (Dream):** When the requesting agent provides a reviewed audit of Yggdrasil Memory and tasks you to apply its findings — merging duplicates, reconciling contradictions, pruning obsolete entries, reorganizing topics, and updating the manifest.
- **Deletion (Forget):** When the requesting agent provides an explicit, confirmed scope of entries to delete and tasks you to remove them. You delete exactly the named entries, update the manifest, and leave changes in the working tree (never commit).

## Workflow

### Establishment Workflow

When tasked to establish `.yggdrasil-memory/` in a project:

1. **Check for existing directory.** If `.yggdrasil-memory/` already exists at the session working directory root, report that it is already established and stop.
2. **Create the directory structure at the session working directory root:**
   ```
   .yggdrasil-memory/
   ├── README.md       (canonical template from this skill)
   └── INDEX.md        (empty manifest with header in place)
   ```
3. **Populate `README.md`** from the canonical template (see Quality Criteria section below for the exact template text).
4. **Initialize `INDEX.md`** with a header and empty-state placeholder (see Quality Criteria section).
5. **Verify the directory is not gitignored.** If a `.gitignore` pattern excludes `.yggdrasil-memory/` (e.g., a broad `.yggdrasil-*` entry), report this to the requesting agent — the knowledge base is intended to be git-tracked.
6. **Report completion** to the requesting agent with the directory path and a note that the knowledge base is ready for entries.

### Promotion Workflow (Remember)

When tasked to promote reviewed findings into Yggdrasil Memory:

1. **Read the reviewed Workfile(s) fully.** The requesting agent provides the path(s) to the reviewed research Workfile(s) and/or original sources. Read them completely before extracting claims.
2. **Extract durable, source-cited claims only.** Identify statements that are:
   - Factual and verifiable against the sources you just read.
   - Durable (not task-specific, not transient state, not reproducible in seconds by reading one file).
   - Worth retaining across multiple tasks (decisions, hard-won findings, project facts).
   - **Never** secrets, credentials, or sensitive data.
3. **Organize by topic.** Group related claims into logical topics (e.g., "ci-pipeline," "database-migrations"). One topic = one entry file.
4. **Write or update entry files.** For each topic:
   - Create a new file `<topic>.md` or update an existing one.
   - Include YAML frontmatter with required fields (see Quality Criteria for the schema).
   - Write the markdown body with the distilled knowledge, organized for clarity.
   - **Cite sources precisely:** in the frontmatter `sources` field, list file paths and line numbers (e.g., `scripts/validate.sh:42-50`, `AGENTS.md:35`).
5. **Update `INDEX.md`.** Add or update one line per entry: topic name, brief summary, updated date. Keep the manifest in sync with the files on disk.
6. **Leave changes in the working tree. Do not commit.** The diff is reviewed downstream; committing is the user's act, never an agent's.
7. **Report completion** to the requesting agent with the list of entries created/updated and the Memory paths.

### Consolidation Workflow (Dream)

When tasked to apply a reviewed audit to the knowledge base:

1. **Read the reviewed audit Workfile fully.** The requesting agent provides the path to the reviewed audit (an analysis of Yggdrasil Memory for duplicates, contradictions, staleness, and reorganization opportunities). Read it completely.
2. **Execute the audit's findings faithfully.** Do not re-decide what the audit already decided. Apply its guidance exactly:
   - **Merge/deduplicate:** Combine overlapping entries into one authoritative entry; union their source citations.
   - **Reconcile contradictions:** Where the audit identified conflicting claims, follow its guidance on which entry to keep (mark the loser `superseded` or delete it).
   - **Prune:** Delete entries the audit marked as obsolete, trivially re-derivable, or below the value bar. Downgrade `confidence` on aging unverified entries per the audit's guidance.
   - **Reorganize:** Split bloated topic files, rename topics, or restructure as the audit recommends.
3. **Update `INDEX.md`.** Rebuild the manifest to reflect all changes (deletions, merges, renames, confidence downgrades).
4. **Leave changes in the working tree. Do not commit.** The diff is reviewed downstream; committing is the user's act, never an agent's.
5. **Report completion** to the requesting agent with a summary of changes (entries merged, deleted, reorganized, confidence adjusted) and the Memory paths.

### Deletion Workflow (Forget)

When tasked to delete entries from the knowledge base:

1. **Verify the scope.** The requesting agent provides an explicit, confirmed list of entry names/topics to delete. This list has already been presented to the user and confirmed. Do not infer, expand, or interpret the scope — delete exactly what you are given.
2. **Delete entry files.** Remove the named `.md` files from `.yggdrasil-memory/`.
3. **Update `INDEX.md`.** Remove the corresponding lines from the manifest. Ensure the manifest remains valid and consistent.
4. **Leave changes in the working tree. Do not commit.** The diff is reviewed downstream; committing is the user's act, never an agent's.
5. **Report completion** to the requesting agent with the list of deleted entries and confirmation that the manifest is consistent.

## Quality Criteria

### Entry Frontmatter Schema

Every entry must include the following YAML frontmatter (in this order):

> **Maintainer note:** Any future schema change must also update the copy embedded in the README canonical template (§ README.md Canonical Template → Frontmatter Schema, below).

```yaml
---
topic: <kebab-case-topic-name>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources:
  - <file-path>:<line-range>  # e.g., scripts/validate.sh:42-50
  - <file-path>               # e.g., AGENTS.md
confidence: <high|medium|low>
status: <active|stale|superseded>
---
```

**Field definitions:**
- `topic`: Unique identifier for the entry, kebab-case, matching the filename (without `.md`).
- `created`: ISO date when the entry was first written.
- `updated`: ISO date of the most recent modification.
- `sources`: List of file paths and/or line ranges where the claims in this entry are sourced. Always cite verifiable sources; never leave this empty.
- `confidence`: `high` (verified recently), `medium` (verified but aging), `low` (unverified or contradicted by newer sources).
- `status`: `active` (current and in use), `stale` (unverified for a long time; consider re-verifying or deleting), `superseded` (replaced by a newer entry; kept for history).

### INDEX.md Manifest Format

The manifest lists all entries in the knowledge base. Format:

```markdown
# Yggdrasil Memory Index

| Topic | Summary | Updated |
|-------|---------|---------|
| ci-pipeline | CI requires Node 20; builds fail on older versions | 2026-07-23 |
| database-migrations | Migrations run in CI, not at app startup | 2026-07-23 |
```

**Empty state** (as scaffolded at establishment; remove the placeholder line when the first entry row is added):

```markdown
# Yggdrasil Memory Index

| Topic | Summary | Updated |
|-------|---------|---------|

_No entries yet._
```

**Rules:**
- One row per entry file.
- Columns: topic name, one-line summary, updated date (ISO format).
- Keep the manifest in sync with the files on disk — every `.md` file in the directory (except `README.md` and `INDEX.md` itself) must have a corresponding row.
- When entries are added, merged, deleted, or renamed, update the manifest immediately.

### README.md Canonical Template

Every project's `.yggdrasil-memory/README.md` is generated from this canonical template (stored in this skill). The template is:

````markdown
# Yggdrasil Memory

This directory contains the project's persistent Yggdrasil Memory — distilled, source-cited findings that persist across task lifecycles.

## What Goes Here

- **Facts about the project** (e.g., "the CI pipeline requires Node 20; builds fail on older versions") — with file/line citations.
- **Decisions and rationale** (e.g., "database migrations run in CI, not at app startup, because…").
- **Hard-won findings** (root causes from debugging tasks, dependency quirks, performance characteristics).
- **NOT**: task narratives, review verdicts, transient state, anything reproducible in seconds by reading one file.

## Entry Format

Each entry is a markdown file with YAML frontmatter. See the schema below.

### Frontmatter Schema

```yaml
---
topic: <kebab-case-topic-name>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources:
  - <file-path>:<line-range>  # e.g., scripts/validate.sh:42-50
  - <file-path>               # e.g., AGENTS.md
confidence: <high|medium|low>
status: <active|stale|superseded>
---
```

**Fields:**
- `topic`: Unique identifier, kebab-case, matching the filename (without `.md`).
- `created`: ISO date when the entry was first written.
- `updated`: ISO date of the most recent modification.
- `sources`: File paths and/or line ranges where the claims are sourced. Always cite verifiable sources.
- `confidence`: `high` (verified recently), `medium` (verified but aging), `low` (unverified or contradicted).
- `status`: `active` (current), `stale` (unverified for a long time), `superseded` (replaced by a newer entry).

## INDEX.md

The `INDEX.md` file is a manifest listing all entries in the knowledge base. It is kept in sync with the files on disk — every entry file must have a corresponding row in the manifest.

## Maintenance

The knowledge base is maintained through three operations:

- **Remember (promotion)** — via `/yggdrasil/remember`: Distill reviewed research findings into new or updated entries. Only reviewed research is eligible.
- **Dream (consolidation)** — via `/yggdrasil/dream`: Audit the knowledge base for duplicates, contradictions, and staleness; consolidate and prune per a reviewed audit.
- **Forget (deletion)** — via `/yggdrasil/forget`: Delete entries by explicit user instruction and confirmation.

All mutations are reviewed before they are final. Changes are left in the working tree (never committed by agents) — committing is the user's act.

## Git History as Recovery Net

By default, this directory is git-tracked. Git history provides an audit trail of all changes and serves as a recovery net for destructive operations (Forget, Dream pruning). A mistaken deletion is `git checkout` away.

## Canonical Source

This README is generated from the canonical template in the `brokk-memory-curation` skill. If you are reading this in a target project, the schema and conventions are authoritative in the skill; this file documents them for your reference.
````

### Quality Criteria for Entries

- **Every entry must cite verifiable sources.** The `sources` field must list file paths and/or line numbers where the claims are grounded. Never cite a source you have not read.
- **No entry created or modified without a distinct upstream reviewed Workfile backing it.** Promotion requires a reviewed research Workfile. Consolidation requires a reviewed audit. Deletion requires explicit user confirmation. Never write to Yggdrasil Memory based on your own reasoning or inference.
- **INDEX.md always kept in sync.** Every entry file on disk must have a corresponding row in the manifest. Every row in the manifest must correspond to a file on disk.
- **Never promote secrets or credentials.** Entries are git-tracked by default and visible in diffs.
- **Never commit Yggdrasil Memory changes.** All mutations — promotion, consolidation, deletion — are left in the working tree; committing is the user's act.
- **Confidence and status fields are honest.** Mark entries `low` confidence if sources are old or unverified. Mark entries `stale` if they have not been re-verified in a long time. Never overstate certainty.

## Anti-Patterns

- **Fabricating knowledge not present in sources.** Every claim must be extractable from the reviewed Workfile or original sources you read. Never extrapolate, infer, or add reasoning beyond what the sources support.
- **Skipping INDEX.md updates.** Update the manifest every time you modify entry files; an out-of-sync manifest defeats its purpose.
- **Expanding a Forget scope beyond what was confirmed.** The requesting agent provides an explicit list of entries to delete. Delete exactly that list, nothing more. Never infer "related" entries or "probably stale" entries to delete alongside the confirmed scope.
- **Treating Yggdrasil Memory entries as a place for raw or unreviewed notes.** Yggdrasil Memory is not a scratch pad. Every entry is a durable claim backed by reviewed sources. If you are tempted to write something without a reviewed source, it does not belong in Yggdrasil Memory yet.
- **Promoting task narratives or transient state.** Yggdrasil Memory is for durable knowledge, not "what happened in this task" or "the current state of X." If a claim is only true for this task or only true right now, it is not durable enough for Yggdrasil Memory.
- **Deleting beyond the task's named scope.** A consolidation task deletes only what its reviewed audit names; a deletion task deletes only the confirmed list. Never remove entries as an unrequested side effect of any operation.
- **Creating or mutating a knowledge base anywhere other than the session working directory.** The knowledge base must be rooted at the session working directory — never in a global or configuration location, and never in another project's tree. Always establish and work with `.yggdrasil-memory/` at the session working directory root.
