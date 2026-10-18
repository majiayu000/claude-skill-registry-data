---
name: context-hygiene
agent: none
description: Nightly context trim for ACTIVE_PRIORITIES and the dated SESSION_LOG schema. Archives before removal, uses content-hash compare-and-swap, and refuses unknown shapes.
allowed-tools: Read, Write, Bash
user-invocable: true
status: PRODUCTION - bounded archive writer
triggers:
  - context hygiene
  - trim session log
  - archive old session entries
  - clean active priorities
---

# /context-hygiene

This is the sole bounded compaction exception to the Session Log chronicle. It
runs only when invoked, never while the framework is being installed or tested
against a real vault.

## Precondition

1. Read `vault/memory/SESSION_LOG.md` and
   `vault/memory/ACTIVE_PRIORITIES.md`.
2. Hash both exact byte streams with SHA-256.
3. Run:

```text
node daemons/nightly-context-hygiene.mjs --root <aigent-root>
```

Green means no edit is needed. Red permits only the bounded archive below.
Unreadable or unfamiliar content is a failure, not permission to rewrite.

## Session Log archive

The executable target schema uses newest-first dated H2 blocks. A canonical
block starts with `## YYYY-MM-DD - title` and contains one nonempty occurrence
of each field:

- `Objective`
- `Completed`
- `Decisions`
- `Open threads`
- `Next action`

Archival rules:

- Keep the newest five live dated blocks.
- Move older whole blocks to
  `vault/memory/SESSION_LOG_ARCHIVE_<YYYY-MM-DD>.md`.
- Preserve source text and order.
- Preserve frontmatter, title, schema guidance, and archive links.
- Dedupe by exact dated heading plus block hash.
- Refuse a block whose boundary cannot be determined without judgment.

## Active Priorities archive

The mechanically checkable live shape contains:

- exactly one `## Operating Mode: <mode>` heading;
- one to five live bullet priorities under `## Tier 1`, `## Tier 2`, or
  `## Tier 3` headings;
- no placeholder priority;
- one valid `Last reviewed: YYYY-MM-DD` line; and
- no embedded `## Archived` section.

Move only content explicitly marked stale, superseded, or archived to
`vault/memory/ACTIVE_PRIORITIES_ARCHIVE_<YYYY-MM-DD>.md`. If removal requires a
human decision, preserve it and report the gate.

## Compare-and-swap

Immediately before each write, hash the live source again. If either hash
differs from the precondition hash, abort with `CONTEXT_HYGIENE_RACE`. Archive
must be durable before the source is trimmed.

After writing, re-run the checker. Only its literal
`CONTEXT_HYGIENE PASS` receipt may record the checkpoint green. Return archive
paths and before/after hashes in bounded detail. Never touch another memory
file.
