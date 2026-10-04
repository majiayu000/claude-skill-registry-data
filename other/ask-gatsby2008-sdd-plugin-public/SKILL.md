---
name: ask
description: Unified cross-service knowledge query over the docs-registry. Answers ANY question about services, decisions, specs, or investigations — grounding every claim in the `raw/` registries (the source of truth) and, when a `wiki/` layer exists, navigating its `[[backlink]]` graph to answer cross-cutting questions. Warns when the wiki is stale. Optional `type:` filter to scope. Supersedes the per-registry doc-*-query commands. Ask "who consumes the LeadCreated event and why did we design it that way?", "what breaks if leads-service goes down?", "have we seen ReportToken reuse before?".
argument-hint: "free-text question  [type:catalog|adr|spec|investigation]"
allowed-tools: Read, Bash(ls:*), Bash(find:*), Bash(grep:*), Bash(cat:*), Bash(test:*), Bash(dirname:*), Bash(stat:*)
---

# Ask — unified knowledge query

One query for the whole registry. It answers cross-cutting questions that used to need
picking the right `doc-*-query` — spanning service catalogs, ADRs, specs, and
investigations — by **navigating the `wiki/` backlink graph** (when present) and
**grounding every answer in `raw/`** (always the source of truth).

---

## Core rule — wiki is the index, raw is the truth

- **`raw/` (`$CLAUDE_DOC_HOME`) is the source of truth.** The `doc-*` commands write it
  directly, so it is always current. Every claim in an answer must be grounded in `raw/`.
- **`wiki/` (if it exists) is a compiled navigation index** — `[[backlinks]]` that make
  cross-cutting answers cheap. It can lag `raw/` (it's refreshed by `/sdd:doc-ingest`).

So: **navigate the wiki, but land on raw.** Never answer from the wiki alone — a stale
wiki must never silently drop `raw/` content. When the wiki is absent or behind, fall
back to reading `raw/` directly (this degrades gracefully to "the typed queries, merged").

```bash
RAW="$CLAUDE_DOC_HOME"
WIKI="$(dirname "$RAW")/wiki"   # present only in a two-layer vault
```

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Parse an optional `type:` scope; check `raw/` exists |
| 2 | If `wiki/` exists → use it to **navigate** (find pages, follow `[[backlinks]]`, collect the `raw/` sources they cite) |
| 3 | **Read the actual `raw/` files** (source of truth); fall back to grep across `raw/` when the wiki has no page or is absent |
| 4 | **Staleness check** — if `raw/` has un-ingested material bearing on the question, warn |
| 5 | Answer, citing `raw/` paths (and wiki pages when used) |

---

## Step 1 — Scope

If `$ARGUMENTS` contains `type:catalog` / `type:adr` / `type:spec` / `type:investigation`,
restrict the read to that registry (`service-catalog/`, `adr-registry/`, `spec-registry/`,
`investigation-registry/`). Strip the token from the question text. No `type:` → all four.

```bash
[ -d "$RAW" ] || { echo "No registry at \$CLAUDE_DOC_HOME ($RAW)."; exit 0; }
```

If `raw/` is empty, say so (as the typed queries do) — don't invent.

---

## Step 2 — Navigate (only if a wiki layer exists)

```bash
[ -d "$WIKI" ] && cat "$WIKI/wiki.md" "$WIKI"/*/*.md 2>/dev/null | head -1   # wiki present?
```

If present:
1. Read `wiki/wiki.md` and the folder-notes (`entities.md`, `concepts.md`, `sources.md`)
   to find the pages relevant to the question.
2. Read those pages and **follow their `[[wikilinks]]`** one hop — this is how a single
   question reaches across catalog + adr + spec + investigation.
3. Note the `## Source` links on each page — they point at the `raw/` files to read next.

If **no** wiki layer, skip to Step 3 and search `raw/` directly.

---

## Step 3 — Ground in raw/ (the source of truth)

Read the actual `raw/` files the wiki pointed to. When the wiki had no page for the
topic (or there is no wiki), search `raw/` directly — this is the reliable fallback:

```bash
grep -rilE '<terms from the question>' "$RAW"/{service-catalog,adr-registry,spec-registry,investigation-registry} 2>/dev/null
```

Then read the matched files. **The answer's facts come from these `raw/` files**, not
from the wiki summary — the wiki only told you where to look.

---

## Step 4 — Staleness check (don't answer from a stale index)

If a wiki layer exists, compare `raw/` against the last ingest so you never present a
wiki-shaped answer that silently omits new `raw/` material:

```bash
WATERMARK="$(grep -oE '^## \[[0-9-]+\]' "$WIKI/log.md" 2>/dev/null | head -1)"
find "$RAW" -name '*.md' -newermt "<watermark date>" -not -path '*/templates/*'
```

If un-ingested `raw/` files bear on the question, **warn** (then still answer from `raw/`):

```
⚠ The wiki is behind: N raw/ source(s) added since the last ingest may bear on this
  (e.g. raw/service-catalog/foo.md). This answer is grounded in raw/ so it's current,
  but the wiki's cross-links may miss them — run /sdd:doc-ingest to refresh.
```

A missing/empty wiki result means "not compiled yet," **not** "no data" — always fall
back to `raw/`.

---

## Step 5 — Answer & cite

Answer `$ARGUMENTS`, citing `raw/` files for every claim (and wiki pages when they added
cross-links). Query shapes it handles (the specialization the typed queries had):

- **Event flow** — who publishes/consumes X → catalog `Publishes`/`Consumes` sections, chained.
- **Decision** — why was X decided → ADR Context + Decision; supersede chains.
- **Feature / spec** — what does feature X do, Open Questions → spec sections.
- **Recurrence** — have we seen X before → investigations, oldest first.
- **Cross-cutting** — spans types (who consumes X *and* why we designed it that way) →
  this is where the wiki backlinks earn their place; without a wiki, read each registry.

```
Question: Who consumes LeadCreated, and why did we design it that way?

Consumed by (raw/service-catalog/marketing-service.md, consent-service.md):
  marketing-service ← SQS marketing-lead-events-queue
  consent-service   ← SQS consent-lead-events-queue
Design rationale (raw/adr-registry/leads-service/…-ADR-002-…md):
  Fan-out via SNS chosen over direct calls to decouple consumers …

Sources: service-catalog/marketing-service.md, service-catalog/consent-service.md,
         adr-registry/leads-service/PROJ-…-ADR-002-….md
         (navigated via wiki/entities/leads-service.md)
```

If the answer isn't in scope: say what you read and offer to widen (`type:` off, or run
`/sdd:doc-ingest` if the wiki looked thin) — never fabricate.

---

## Relationship to the typed queries

`/sdd:ask` **subsumes** `/sdd:doc-catalog-query`, `/sdd:doc-adr-query`, `/sdd:doc-spec-query`,
and `/sdd:doc-investigation-query`: those each read one registry; `ask` reads across all
of them (via the wiki when present, via `raw/` always) and takes an optional `type:`
filter to reproduce a single-registry query when you want it.

## Related Skills

- `/sdd:doc-ingest` — builds/refreshes the `wiki/` layer `ask` navigates.
- `/sdd:doc-catalog` · `/sdd:doc-adr` · `/sdd:doc-spec` · `/sdd:doc-investigation` — write the
  `raw/` registries `ask` grounds its answers in.
