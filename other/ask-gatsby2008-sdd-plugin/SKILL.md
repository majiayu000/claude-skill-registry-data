---
name: ask
description: One query over the docs-registry — service catalogs, ADRs, specs and investigations. Loads only the documents that match the question (within a budget), grounds every claim in `raw/`, and navigates the `wiki/` backlinks when that layer exists. Optional `type:` / `service:` filters. Ask "who consumes the LeadCreated event and why did we design it that way?", "which specs have open questions?", "have we seen ReportToken reuse before?".
argument-hint: "free-text question  [type:catalog|adr|spec|investigation]  [service:<name>]"
allowed-tools: Read, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/registry.py:*), Bash(ls:*), Bash(find:*), Bash(grep:*), Bash(cat:*)
---

# Ask — unified knowledge query

One query for the whole registry. `lib/registry.py` picks what to read; you answer
from it, grounding every claim in `raw/`.

## Core rule — wiki is the index, raw is the truth

- **`raw/` (`$CLAUDE_DOC_HOME`) is the source of truth.** The `doc-*` commands write it
  directly, so it is always current. Every claim must cite a `raw/` file.
- **`wiki/` (a sibling of `raw/`, when present) is a compiled navigation index** of
  `[[backlinks]]`, refreshed by `/sdd:doc-ingest`. It can lag `raw/`. Navigate it; never
  answer from it alone.

---

## Step 1 — Retrieve

Run the engine with the arguments **verbatim** — do not add `type:` or `service:`
yourself; without filters it searches everything and ranks by relevance:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/registry.py ask "$ARGUMENTS"
```

It prints, in order:

| Block | What it is |
|---|---|
| `WIKI:` (+ `⚠ The wiki is behind`) | Only when a `wiki/` layer exists: its path, last ingest, and raw docs changed since |
| `INDEX` | Every in-scope doc: path, title, date — always complete |
| `LOADED` | The best-matching docs (large ones trimmed to their matching `##` sections) up to a budget; or every doc when the scope fits; or only unresolved Open Questions for "which specs have open questions?" |
| `ALSO MATCHED` | Other matches by path, not loaded |
| `HINTS` | How to read each registry type that loaded |
| `tip:` | When matches concentrate in one registry, the `type:` that would narrow it |

## Step 2 — Fill gaps

- An `INDEX` title or `ALSO MATCHED` path looks relevant but was not loaded → `cat` it
  (`<Registry>/<path>`). Do this especially when `LOADED` says none matched: term search
  misses synonyms and Spanish questions over English docs; titles don't.
- A section you need was `[omitted …]` from a trimmed doc → read the file.

## Step 3 — Navigate the wiki (only if a `WIKI:` line was printed)

For cross-cutting questions (spanning catalog + ADR + spec + investigation):
1. Read `wiki/wiki.md` and the folder-notes (`entities.md`, `concepts.md`, `sources.md`)
   to find the pages for the question's entities.
2. Read those pages and follow their `[[wikilinks]]` one hop.
3. Their `## Source` links point at `raw/` files — read any that were not loaded.

A missing wiki page means "not compiled yet", not "no data" — `raw/` still decides.

## Step 4 — Answer and cite

Answer `$ARGUMENTS`, citing a `raw/` path for every claim (and the wiki pages you
navigated through, when they added cross-links). If the engine printed
`⚠ The wiki is behind`, relay it in one line and suggest `/sdd:doc-ingest`.

```
Question: Who consumes LeadCreated, and why did we design it that way?

Consumed by (service-catalog/marketing-service.md, service-catalog/consent-service.md):
  marketing-service ← SQS marketing-lead-events-queue
  consent-service   ← SQS consent-lead-events-queue
Design rationale (adr-registry/leads-service/PROJ-12-ADR-002-sns-fanout.md):
  Fan-out via SNS chosen over direct calls to decouple consumers …
```

If the registry does not cover the question, say what you read (the `INDEX` size and
what you opened) and offer to widen — never invent.

---

## Related Skills

- `/sdd:doc-ingest` — builds/refreshes the `wiki/` layer this skill navigates.
- `/sdd:doc-catalog` · `/sdd:doc-adr` · `/sdd:doc-spec` · `/sdd:doc-investigation` — write
  the `raw/` registries answers are grounded in.
