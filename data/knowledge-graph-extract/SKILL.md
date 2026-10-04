---
name: knowledge-graph-extract
description: Use when the user wants to extract a knowledge graph, entities and relationships, or subject-relation-object triplets from a folder of documents or a set of files — including resuming an interrupted extraction, or turning extracted triplets into Cypher import scripts for Neo4j/Memgraph.
---

# Knowledge Graph Extraction

Extract subject–relation–object triplets from documents into an append-only JSONL dataset,
with deterministic chunking and a progress manifest so an interrupted run resumes exactly
where it stopped. Optional schema enforcement and Cypher generation via bundled
stdlib-only Python scripts (no pip dependencies, no network, no database connections).

**Core principle: the output directory is the state.** Every step reads its inputs from and
records its result in `<output_dir>` before moving on. If the session dies at any point,
re-invoking this skill on the same directory continues the work.

File formats: see [references/output-format.md](references/output-format.md).
Schema format: see [references/schema-format.md](references/schema-format.md).

## When not to use

- **Very large corpora where token cost dominates.** Every chunk re-reads the entity
  registry; across thousands of documents that adds up. A dedicated pipeline (LangChain,
  LlamaIndex, GraphRAG) may be cheaper when you don't need agent-quality reading of mixed
  formats.
- **When you need measured extraction quality.** There is no evaluation harness here;
  precision/recall rest on the agent's judgment. For benchmarked extraction, use a system
  with a labelled eval set.

## Phase 0 — Inputs

Collect from the user (ask only for what's missing):

1. **Documents**: a folder (recurse; skip hidden files and files you cannot read) or an explicit file list. Any format you can Read works — never parse documents with scripts. Line-addressable text (txt, md, code) is chunked by line; page-addressable documents (pdf) by page (see Phase 2).
2. **Output directory**: where all state lives. Required — ask if not given.
3. **Schema** — three modes (format: references/schema-format.md):
   - **Given**: a file path (copy it to `<output_dir>/schema.json`) or inline types in the
     prompt (write the equivalent `schema.json` and show it to the user).
   - **Inferred**: if the user provides no schema, offer to generate one. Skim a bounded
     sample — the first ~200 lines of up to 3–5 representative documents, no more — and
     propose entity and relation types. Present the proposed schema and **wait for explicit
     confirmation before any extraction**: the schema is effectively frozen once triplets
     exist (recovery path: edit schema.json later and re-run validation). Write it with
     `"generated_by": "agent"` so a resumed session knows it was inferred.
   - **Explicitly open**: only if the user declines a schema. Warn that validation weakens
     to structure/duplicate checks and relation vocabulary tends to drift across chunks
     (WORKS_AT vs EMPLOYED_BY); keep relation names consistent with ones already in
     `triples.jsonl`'s vocabulary as you go.
4. **Max triplets per document** (optional): a salience budget — divide it across a document's chunks (minimum 5 per chunk) and extract only the most important facts up to the per-chunk budget. Never stop reading a document early because of the cap.

## Phase 1 — Resume check

If `<output_dir>/manifest.json` exists, this is a resume:

```bash
python3 scripts/kg_status.py <output_dir>
```

Report progress to the user, then continue at Phase 3 from the chunk `kg_status.py` names.
An `in_progress` chunk is re-extracted from scratch — its earlier triplets may partially
exist; the validator's duplicate check cleans exact repeats later. Never edit the chunk plan
of an existing manifest.

## Phase 2 — Chunk plan (before any extraction)

Chunk boundaries must be deterministic — decided once, recorded, never recomputed.
Record a `unit` per document (`"line"` or `"page"`) so resume and status reporting know
how to address each chunk.

1. **Line-addressable text** (txt, md, code, ...) → `unit: "line"`:
   - Count lines with `awk 'END{print NR}' <file>` (counts a final line that has no
     trailing newline, which `wc -l` silently drops).
   - ≤ 1500 lines → one chunk covering the whole file. Larger → ~1200-line chunks, moving
     each boundary forward to the nearest blank line (≤ 50 lines ahead) so chunks end on
     paragraph breaks. Record exact `start_line`/`end_line`.
   - A file that is one giant line (minified/single-line JSON) has no usable line
     structure — make it one chunk and extract in a single pass.
2. **Page-addressable documents** (pdf, ...) → `unit: "page"`:
   - Get the page count with one Read of the whole PDF (no `pages` arg): a PDF of ≤ 10
     pages reads in full (make it one chunk — done), and a larger one errors with the exact
     total ("This PDF has N pages…") — use that N.
   - Larger than 10 pages → ~10-page chunks (the Read tool caps one PDF read at 20 pages, so
     ~10 keeps a chunk to a single read). Record exact `start_page`/`end_page`.
3. Write the complete `manifest.json` (format: references/output-format.md) with every
   chunk `pending`. The chunk plan is now immutable; only `status`/`triplets` fields change.

## Phase 3 — Extraction loop

For each pending chunk, in manifest order:

1. Mark the chunk `in_progress`:
   `python3 scripts/kg_mark.py <output_dir> <doc> <chunk_id> in_progress`
2. Read **only** that chunk of the document: `unit: "line"` → Read with offset/limit over
   `start_line`..`end_line`; `unit: "page"` → Read with the `pages` parameter set to
   `start_page`-`end_page`.
3. Read the entity registry compactly, e.g.
   `cut -c1-160 <output_dir>/entities.jsonl` — you need names, types, and aliases,
   not the full records.
4. Extract the most salient triplets up to the per-chunk budget:
   - Prefer specific facts stated in the text; subject and object must be named entities,
     not pronouns or vague noun phrases. Don't invent facts the chunk doesn't support.
   - Reuse canonical names from the registry for entities already seen ("IBM", not
     "International Business Machines", if "IBM" is registered). Record new surface forms
     of known entities as aliases, not new entities.
   - Conform to schema.json if present: only listed entity/relation types, respect
     subject/object constraints. A true fact that doesn't fit the schema is skipped, not
     shoehorned into a wrong type.
   - Relations in UPPER_SNAKE_CASE; entity names as they'd appear as graph node names.
5. Append triplets to `triples.jsonl` and new entities/aliases to `entities.jsonl`
   (one JSON object per line; append with `>>`, never rewrite these files).
6. Mark the chunk `done` with its triplet count (this also flips the document to `done`
   once its last chunk finishes):
   `python3 scripts/kg_mark.py <output_dir> <doc> <chunk_id> done --triplets <n>`

**Context discipline** (what makes long runs survive):

- Never read `triples.jsonl` back — it is write-only for you.
- Never hand-edit `manifest.json` — change status only through `kg_mark.py`, which
  rewrites it atomically so an interrupted write cannot corrupt the resume anchor.
- If context is running low mid-run: finish the current chunk (through step 6), tell the
  user extraction is partial and re-invoking the skill on the same output directory
  resumes automatically, and stop cleanly. Do not start a chunk you cannot finish.

## Phase 4 — Validation

```bash
python3 scripts/validate_triples.py <output_dir>            # report only
python3 scripts/validate_triples.py <output_dir> --apply    # quarantine violations
```

Checks structure, schema conformance (types, relation domain/range), and exact duplicates.
`--apply` moves violations to `rejected.jsonl` (quarantined, never deleted) and rewrites
`triples.jsonl` atomically. Run report mode first and show the user the summary before
applying.

## Phase 5 — Cypher generation (optional, on request)

```bash
python3 scripts/generate_cypher.py <output_dir>
```

Writes `cypher/00_constraints_neo4j.cypher` **and** `cypher/00_constraints_memgraph.cypher`
(one indexes the MERGE key per label; load only the one matching the target DB — the DDL
syntax differs), then `cypher/01_entities.cypher` and `cypher/02_relations.cypher` — batched
`UNWIND … MERGE` statements with escaped literals grouped by label/relation type (portable
openCypher). Load order: the matching `00_constraints_*` file → `01_entities` → `02_relations`.
The user loads them themselves (cypher-shell, Neo4j Browser, Memgraph); never connect to a
database on their behalf.

## Quick reference

| Task | How |
|---|---|
| Show progress / find next chunk | `python3 scripts/kg_status.py <output_dir>` |
| Update chunk status (atomic) | `python3 scripts/kg_mark.py <output_dir> <doc> <chunk_id> <status> [--triplets N]` |
| Validate against schema | `python3 scripts/validate_triples.py <output_dir> [--apply]` |
| Generate Cypher | `python3 scripts/generate_cypher.py <output_dir>` |
| Resume interrupted run | Re-invoke skill with same output dir — Phase 1 handles it |
| Add triples/entities | Append (`>>`) to the `.jsonl` files, never rewrite |

## Common mistakes

- **Re-chunking on resume** — chunk boundaries come from the manifest, never from re-reading document sizes. A changed plan orphans already-extracted chunks.
- **Extracting before the manifest exists** — an interruption then loses everything; Phase 2 always completes first.
- **Loading the whole document or whole triples file into context** — read only the current chunk's line range and the compact registry view.
- **Inventing entity duplicates** — check the registry before naming an entity; "Dr. Smith" and "Jane Smith" in the same corpus are usually one node with an alias.
- **Treating the cap as a hard stop** — it's a per-chunk salience budget; every chunk is always processed.
- **Writing Cypher by hand** — always use `generate_cypher.py`; hand-written Cypher with interpolated names breaks on quotes and backslashes.
