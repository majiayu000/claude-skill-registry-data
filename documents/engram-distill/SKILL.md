---
name: engram-distill
description: Distill knowledge from docs, transcripts, or code notes into the engram knowledge graph via the engram-mcp tools. Extract entities, relationships, and facts, classify them against the project's configured ontology, and BRIDGE every concept to the code/doc artifact it describes or realizes so the graph stays connected. Extraction + bridging are the agent's own reasoning; the server never calls an LLM.
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
- You are building up a project's knowledge graph (technical + domain + business).
- After `scan_repo`, to add the conceptual layer that explains the code.

## Prerequisites

The `engram` MCP server is configured (stdio JSON-RPC). Its launch flags fix the
**project** scope and the **ontology + taxonomy**:

```
engram-mcp --storage <dir> --project <name> [--ontology <layers.json>] [--taxonomy <concepts.json>]
```

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
   idempotency_key}`. Include the bridging relationships in the same batch. Supply a
   **stable `idempotency_key`** so re-runs converge, not duplicate. Best-effort, not ACID.

8. **Verify** — `graph_neighbors {name}` on a bridged concept; confirm it now links
   to the code entity. Then `recall {query}` to confirm retrieval. If the link is
   missing, the batch was malformed — fix and re-send (idempotency makes this safe).

## Rules

- **You classify AND bridge; the server stores.** Decide each entity's ontology
  class and each relationship's predicate from `ontology_read`; do not invent predicates.
- **Bridge to real artifacts.** Link only to code/doc names that exist (discovered in
  step 4 or written in this same batch). Never invent a link target.
- **Semantic bridging is your value-add.** The scan links by exact name; you link by
  meaning (concept ↔ the code that realizes it). Aim for every extracted concept to
  carry at least one `across` edge.
- **One project, one graph.** Writes are scoped to the launch `--project`.
- **Idempotency.** Same `idempotency_key` → converge, not duplicate.
- **Honest orphans.** A concept with no real counterpart gets a fact noting that, not
  a fabricated edge.

## Example call sequence

```
ontology_read                              → learn layers + predicates
taxonomy_read                              → learn concept hierarchy
scan_repo      {path}                      → index code (technical layer)
search         {query: "auth"}             → discover auth-related code symbols
index_docs     {content, path}             → persist the raw doc (docs lane)
store_knowledge {facts, entities,          → persist KG + REQUIRED bridges
                 relationships,              (include: concept -[describes]-> function)
                 idempotency_key}
graph_neighbors {name: "Authentication"}   → verify the concept now links to code
recall         {query}                     → confirm retrieval
```

## Bridge coverage (self-check)

After writing, sample 2–3 concepts via `graph_neighbors`. Each should show at least
one `across` edge (`describes`/`realized_by`/`governs`) to a code/doc entity. If a
sampled concept has no across-edge and you did not intentionally mark it an orphan,
go back and add the bridge — an unbridged concept is a disconnected subgraph, which
is the defect this skill exists to prevent.
