---
name: doc-ingest
description: Compile new or changed material from the docs-registry `raw/` layer into the `wiki/` knowledge layer — extract entities & concepts, write typed markdown pages with [[backlinks]], update the indexes, and append to the log. This is the "raw → wiki" step of the two-layer (Karpathy) knowledge base, and the producer that keeps `/sdd:ask` sharp. Only runs where `$CLAUDE_DOC_HOME` is a two-layer vault (a `wiki/` sibling of `raw/`).
argument-hint: "[path under raw/ | 'session' | omit to compile what's un-ingested]"
allowed-tools: Read, Write, Bash(ls:*), Bash(find:*), Bash(grep:*), Bash(cat:*), Bash(test:*), Bash(dirname:*), Bash(date:*), Bash(stat:*)
---

# Ingest — compile raw → wiki

Turns append-only `raw/` material (the SDD registries + hand-added sources) into the
**compiled `wiki/` layer**: typed pages (`entities/`, `concepts/`, `sources/`) with
`[[backlinks]]`, kept indexes, and a log entry. It is the missing *producer* — the SDD
`doc-*` commands write `raw/`; **`doc-ingest` weaves `raw/` into the interconnected wiki**
that `/sdd:ask` navigates.

---

## Vault layout

```bash
RAW="$CLAUDE_DOC_HOME"                 # the registries live here (point it at .../raw)
VAULT="$(dirname "$RAW")"
WIKI="$VAULT/wiki"                     # compiled knowledge (sibling of raw/)
SCHEMA="$VAULT/CLAUDE.md"              # the vault schema — authoritative, co-evolving
```

**This skill only applies to a two-layer vault.** If `$WIKI` does not exist (e.g. the
default `~/.claude` registry with no wiki layer), stop with:

```
No wiki layer found next to $CLAUDE_DOC_HOME.
doc-ingest compiles raw/ into a wiki/ knowledge layer — it needs a two-layer vault
(a `wiki/` sibling of `raw/`, per the Karpathy model). Nothing to do here.
```

---

## Step 1 — Read the schema (authoritative)

**Read `$SCHEMA` first and follow it.** It owns the conventions and can change without
this skill changing:

```bash
cat "$SCHEMA"
```

It defines: the three layers; page frontmatter (`type: entity|concept|source`, controlled
`subtype`, tags; H1 = title; a `## Source` section linking back to `raw/`); the navigation
files (`wiki/wiki.md`, folder-notes, `wiki/log.md`); and the Compile / Lint / Log
operations. **Do not hardcode or drift from it — this skill just enforces running it.**

If the schema and this skill ever disagree, the schema wins.

---

## Step 2 — Choose what to compile

| `$ARGUMENTS` | Source |
|--------------|--------|
| a path under `raw/` (e.g. `raw/service-catalog/leads-service.md`) | compile that document |
| `session` | distill reusable entities/concepts from the **current session** (like `/sdd:doc-investigation`, but into the wiki) |
| *(empty)* | **auto** — compile whatever in `raw/` is newer than the last ingest |

**Auto detection** — find `raw/` files changed since the last compile, using the log's
newest timestamp as the watermark:

```bash
grep -oE '^## \[[0-9-]+\]' "$WIKI/log.md" | head -1     # newest log date = watermark
find "$RAW" -name '*.md' -newermt "<watermark>" -not -path '*/templates/*'
```

Announce the source(s) before compiling. Prefer **incremental** compiles (a few files)
over a giant pass. Skip purely narrative / project-log material — only distill reusable
entities and concepts (per the schema).

---

## Step 3 — Compile (per the schema's Compile operation)

For each source, follow `$SCHEMA` → *Operations → Compile*:

1. Read the source in `raw/`.
2. Extract the **entities** and **concepts** it introduces. For each, **create or update
   in place** its page under `wiki/entities/<subtype>` or `wiki/concepts/<subtype>` —
   **never duplicate an existing page**; grep first:
   ```bash
   grep -rli "<entity or concept name>" "$WIKI/entities" "$WIKI/concepts"
   ```
3. Write each page in **your own words** (never copy raw verbatim), with the required
   frontmatter, `[[wikilinks]]` to related pages, and a `## Source` section linking back
   to the `raw/` file(s).
4. Update the affected folder-notes (`entities.md`, `concepts.md`, `sources.md`) and
   `wiki/wiki.md`.
5. **Append** an entry to `wiki/log.md` in the schema's format:
   `## [YYYY-MM-DD] compile | <title>` (or `ingest` when driven from a session), listing
   pages created vs. updated.

---

## Step 4 — Verify & report

- **Confirm 0 broken links** — every `[[wikilink]]` must resolve to a page (create the
  missing target, or fix the name). Do not finish with dangling links.
- Report: pages **created** vs. **updated**, and the log line appended.

```
Compiled raw/service-catalog/leads-service.md → wiki/
  Created (3):  entities/leads-service, concepts/lead-dedupe, concepts/savings-id-pool
  Updated (1):  entities/storefront-api (now notes it owns the lifecycle spine)
  Indexes:      entities.md, concepts.md, wiki.md · log.md appended · 0 broken links
```

---

## Rules

- **Never hand-edit or delete existing `raw/` files** — `raw/` is append-only and the
  source of truth. This skill only writes `wiki/`.
- **Never duplicate a wiki page** — update it in place.
- Keep `subtype` within the controlled vocabulary; keep names consistent so `[[links]]` resolve.
- Distill reusable entities/concepts only — skip narrative/log material.
- Always finish with a `wiki/log.md` entry and a 0-broken-links check.

---

## Related Skills

- `/sdd:ask` — the consumer: navigates the `wiki/` this skill builds, grounded in `raw/`.
- `/sdd:doc-catalog` · `/sdd:doc-adr` · `/sdd:doc-spec` · `/sdd:doc-investigation` — write the
  `raw/` registries that this skill compiles into the wiki.
