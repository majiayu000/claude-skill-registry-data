---
name: engram-distill
description: Distill knowledge from docs, transcripts, or code notes into the engram knowledge graph via the engram-mcp tools. Extract entities, relationships, and facts, classify them against the project's configured ontology, and BRIDGE every concept to the code/doc artifact it describes or realizes so the graph stays connected. Trigger after reading a doc worth remembering, after scan_repo, or when building the project knowledge graph. Extraction + bridging are the agent's own reasoning; the server never calls an LLM.
---

# engram-distill

Turn unstructured material (Markdown docs, transcripts, design notes) plus code
into a queryable, multi-layer knowledge graph by writing it through the
**engram-mcp** server. The server is a deterministic store — *you* (the agent)
do the extraction, classification, and **bridging**; the server persists and
retrieves.

> **Bridging is mandatory, not optional.** A concept not linked to the code or doc
> it describes/realizes is an orphan in a disconnected subgraph. The deterministic
> `scan_repo` already links docs to code by **exact name match**; your job is the
> **semantic** links the scan cannot infer — e.g. a doc section titled
> *Authentication* that explains `auth_middleware`, even though the words differ.

## When to run

- You just read a doc / transcript / RFC / README that the project should remember.
- After `scan_repo`, to add the conceptual layer that explains the code.

## Prerequisites

The `engram` MCP server is configured (stdio JSON-RPC). Its launch flags fix the
**project** scope and the **ontology + taxonomy**:

```
engram-mcp --storage <dir> --project <name> --tools full \
           [--ontology <layers.json>] [--taxonomy <concepts.json>]
```

`--tools full` (or `all`) is required: `ontology_read`, `taxonomy_read`,
`graph_neighbors` and `resolve_entity` are not in the default core profile.

All writes land in one fused-per-project workspace; `recall` sees them together.

## Workflow

1. **Read the active ontology + taxonomy** — `ontology_read` then `taxonomy_read`.
   Classify every entity into an ontology class; use only declared predicates. The
   `across` predicates (`describes`, `realized_by`, `governs`, `extracted_from`)
   are the ones that bridge layers — concept → code, business → technical.

2. **Ensure code is indexed** — if the repo has not been scanned, call
   `scan_repo {path}`. This populates the `technical` layer (function/class/struct
   entities + call edges) that your concepts will bridge **to**. Do this before
   bridging so the link targets exist.

3. **Index raw docs** (optional) — for material you want retrievable verbatim,
   `index_docs {content, path, kind}`. The server chunks it into the `docs` lane.

4. **Discover existing code entities** — before bridging, find out what code
   symbols already exist so you link to REAL names, not invented ones. Call
   `search {query}` for each domain/area (e.g. `"auth"`, `"payment"`), or
   `resolve_entity {name}` for a specific symbol. Keep the code entity names you find.

5. **Extract** (your reasoning) — from the material, produce:
   - **facts** — `{ "content": "…" }` free-text observations worth remembering.
   - **entities** — `{ "name", "kind" }` mapped to an ontology class.
   - **relationships** — `{ "subject", "predicate", "object" }` using only the
     ontology's predicates.

6. **Bridge (REQUIRED)** — for every concept/entity you extracted, link it to the
   code or doc artifact it relates to, using an `across` predicate:
   - A domain concept a function/class/module implements →
     `concept -[describes]-> function` (or `-[realized_by]->`).
   - A business capability realized by a module → `capability -[realized_by]-> module`.
   - A doc that governs a process → `doc-concept -[governs]-> …`.
   Use the code entity names you discovered in step 4 as the `object`. If a concept
   genuinely has no code/doc counterpart, record that in a fact instead of
   fabricating an edge — a fabricated link is worse than an honest orphan.

7. **Write the batch** — `store_knowledge {facts, entities, relationships,
   idempotency_key, source_id}`. Include the bridging relationships in the same
   batch. Best-effort, not ACID. The key discipline is **mandatory**:
   - Key = `<doc-id>@<sha256-of-exact-material>[:12]` — the identity of the
     source you distilled, bound to the exact bytes you extracted from.
   - `source_id` = the stable doc identity (e.g. repo path), reused across revisions; omit only for one-off batches.
   - Retries re-send the **same payload** (immutable retry payload). If you
     re-extract and anything changed, that is a *revision*, not a retry.
   - A revision = **new key** + same `source_id`: the engine supersedes the
     prior batch (archives undeclared records, tombstones replaced facts,
     reports per-step counts); keep the supersession fact as the record.
   - **Append-only only when `source_id` is omitted:** unsourced batches are never retracted.
   - `facts` land in the memory lane as source-derived observations (recalled
     by `recall`); entities/relationships land in the knowledge graph.

8. **Verify** — `graph_neighbors {name}` on a bridged concept; confirm it now links
   to the code entity. Then `recall {query}` to confirm retrieval. If the link is
   missing, the batch was malformed — fix and re-send (idempotency makes this safe).

## Rules

- **You classify AND bridge; the server stores.** Decide each entity's ontology
  class and each relationship's predicate from `ontology_read`; do not invent predicates.
- **Semantic bridging is your value-add.** The scan links by exact name; you link by
  meaning (concept ↔ the code that realizes it). Aim for every extracted concept to
  carry at least one `across` edge.
- **One project, one graph.** Writes are scoped to the launch `--project`.
- **Honest orphans.** A concept with no real counterpart gets a fact noting that, not
  a fabricated edge.

## Example call sequence

```
ontology_read, taxonomy_read              → learn layers + declared predicates
scan_repo      {path}                      → index code (technical layer)
search         {query: "auth"}             → discover real code symbols
index_docs     {content, path}             → persist the raw doc (docs lane)
store_knowledge {facts, entities,          → persist KG + REQUIRED bridges
                 relationships,              (concept -[describes]-> function)
                 idempotency_key}
graph_neighbors {name}, recall {query}     → verify the bridge + retrieval
```

## Contract

1. Every write is source-keyed: the idempotency key names the doc and its
   exact bytes (step 7). Session-stable keys are forbidden.
2. Every extracted concept is bridged to a real artifact, or honestly
   recorded as an orphan — never a fabricated edge.
3. Only declared ontology predicates; only discovered link targets.
4. Sourced batches are retractable: a revision reusing the same `source_id`
   supersedes engine-side with reported counts; unsourced batches stay append-only.

## When it fails

- `store_knowledge` reports per-step failures → fix the malformed entries
  and re-send the same batch and key (idempotent).
- Entity won't classify → the ontology doesn't cover it; record it as a
  fact instead of inventing a class.
- `graph_neighbors` shows no across-edge after write → batch was malformed
  or the bridge target didn't exist; re-discover names and re-send.

## Anti-patterns

- Session-keyed idempotency ("my-session-1") — orphans the write from its source.
- Linking to symbol names you never saw in a discovery query.
- Dumping raw prose as facts instead of extracting entities/relationships.
- Treating a revision as a retry (re-used key, changed payload).

## Final check

- Does every sampled concept carry an across-edge or an honest orphan note?
- Does the key name the source doc and its content hash?
- Would a re-run of the same doc converge instead of duplicating?
