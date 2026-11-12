---
name: index
description: >
  Generate or refresh the vault MOC at vault/wiki/index.md — the top-level
  catalog of every topic folder and synthesis note in the vault. Trigger when
  the user says "refresh the index", "rebuild the vault MOC", "update the
  catalog", or after adding a new top-level topic or synthesis. Per-folder
  folder notes are owned by the ingest workflow, not by this skill.
allowed-tools: Read Write Edit Glob Grep
disable-model-invocation: true
---

# LLM Wiki — Index

Refresh `vault/wiki/index.md` — the vault MOC.

Per-folder folder notes (`wiki/<topic>/<topic>.md`, `type: index`; legacy
`_index.md` where still present) are maintained by
`/claude-wiki-pages:ingest` during ingest. This skill does not touch
them.

## When to invoke

- A new top-level topic folder has been created.
- A synthesis note has been added under `wiki/_synthesis/`.
- `/claude-wiki-pages:lint` reports vault-MOC drift.
- The user asks for an index refresh.

## Reading contract

- `vault/CLAUDE.md` — the schema.
- `vault/wiki/` — the full tree, specifically:
  - Top-level topic folders (children of `wiki/`).
  - `wiki/_synthesis/*.md` — the synthesis notes.
  - Each top-level folder's folder note (or legacy `_index.md`) — to pull its
    topic `title` and the aliases the vault MOC should expose.

## Writing contract

Exactly one write target:

```
vault/wiki/index.md
```

With frontmatter matching the `index` type schema, and a body that:

- Lists every top-level topic folder under a `## Topics` heading, one line
  per folder, format `- [[<folder>]] — <one-line summary from the folder note>`
  (filename wikilink to the folder note, matching the quoted `"[[<folder>]]"`
  form the schema requires in the root `child_indexes:`).
- Lists every synthesis note under `## Syntheses`, one line per file, format
  `- [[<file-basename>|<Title>]] — <synthesis_type>` (piped basename target —
  a bare `[[<Title>]]` does not resolve to the kebab-case filename and renders
  as a ghost node).
- Ends with an auto-generated timestamp: `_Generated <YYYY-MM-DD>._`

Plus one log append:

```
## [YYYY-MM-DD] index | refreshed vault MOC (<N> topics, <M> syntheses)
```

This skill MUST NOT:

- Touch per-folder folder notes (`wiki/<topic>/<topic>.md`, or legacy `_index.md`). Ever.
- Write any page other than `wiki/index.md` and `wiki/log.md`.
- Reorder entries non-deterministically — ordering must be stable, so
  repeated runs on an unchanged tree produce no diff.

## Ordering

- Topics: alphabetical by folder name. Underscore-prefixed folders
  (`_synthesis`, `_sources`) are excluded from the topic list.
- Syntheses: chronological by `created:` ascending, ties broken alphabetically.

These are the conventions; document any project-specific override in
`vault/CLAUDE.md` and respect it here.

## Workflow

1. **Schema.** Read `vault/CLAUDE.md`.
2. **Enumerate.** List top-level folders under `wiki/` (excluding
   underscore-prefixed). List files under `wiki/_synthesis/`.
3. **Summarize.** For each topic folder, read its folder note's frontmatter
   `title:` and first-line summary (fall back to a legacy `_index.md` when no
   folder note exists). For each synthesis, read `title:` and
   `synthesis_type:`.
4. **Render.** Build `wiki/index.md` per the frontmatter schema and the body
   format above.
5. **Verify idempotency.** If the current `wiki/index.md` is byte-identical
   to what would be written, skip the write (avoid a noop commit) but still
   log the refresh.
6. **Write.** Overwrite `wiki/index.md`.
7. **Log.** Append to `wiki/log.md`.

## Hook enforcement

`PreToolUse` `validate-frontmatter.sh` rejects an `index`-type page missing
any required field (`title`, `type`, `aliases`, `children`,
`child_indexes`). For the vault MOC, `children` and `child_indexes` at the
top level are the full lists built in step 4.

## Completion signal

```
READY: wrote wiki/index.md (<N> topics, <M> syntheses).
```

or, on a noop:

```
UNCHANGED: wiki/index.md already reflects the current tree.

## Context contract

Machine-readable read/write contract for the `engine context` verb.

| role           | globs                                     |
| -------------- | ----------------------------------------- |
| inputs (L4)    | wiki/**                                   |
| reference (L3) | vault/CLAUDE.md                           |
| outputs        | wiki/index.md                             |
```
