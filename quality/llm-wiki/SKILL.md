---
name: llm-wiki
description: Use when designing, building, or maintaining a persistent Obsidian-compatible knowledge base that an LLM updates over time, including wiki schema design, ingest/query/lint workflows, index and log conventions, source traceability, and wiki health checks.
---

# LLM Wiki

Use this skill to turn a collection of raw sources into a maintained wiki that compounds over time, instead of re-deriving the same knowledge from scratch on every query.

## Core Model

Maintain three layers:

- raw sources: immutable documents, notes, images, or transcripts
- wiki pages: LLM-authored markdown that summarizes and cross-links the knowledge
- schema instructions: `CLAUDE.md`, `AGENTS.md`, or a similar file that defines the wiki rules and workflows

Keep the human and LLM roles separate:

- Human curates sources, priorities, and questions.
- LLM summarizes, cross-references, updates pages, and performs bookkeeping.

## Essential Files

- `index.md`: content-oriented catalog and first stop for navigation
- `log.md`: append-only record of ingests, queries, and lint passes
- `purpose.md` optional: goals, scope, key questions, and evolving thesis
- YAML frontmatter optional: page type, dates, source links, tags, or counters when that metadata helps navigation

## Ingest Workflow

1. Read one new source or a small batch.
2. Extract the main claims, entities, concepts, evidence, and contradictions.
3. Create or update:
   - a source summary page
   - related entity or concept pages
   - overview or synthesis pages
   - `index.md`
   - `log.md`
4. Record provenance so claims can be traced back to the source material.
5. Prefer incremental edits to the existing wiki over rewriting everything from scratch.

## Query Workflow

- Start from `index.md` to find the relevant neighborhood of pages.
- Read the smallest set of pages that can answer the question well.
- Answer with citations to wiki pages or raw sources.
- If the answer creates durable knowledge, file it back into the wiki as a new page, comparison, memo, or checklist.

## Lint Workflow

Run periodic health checks for:

- contradictions or superseded claims
- orphan pages and weak cross-links
- concepts that are mentioned but still lack their own page
- stale summaries after new evidence arrives
- obvious research gaps that should become new source requests

## Structural Conventions

- Keep raw sources immutable.
- Prefer many small linked pages over giant monolith notes.
- Use stable wikilinks and consistent page types.
- Make logs parseable with consistent headings and timestamps.
- Store important images locally if future sessions may need to inspect them again.

## Scale-Up Guidance

- At moderate scale, a strong `index.md` may be enough.
- Add local search or embeddings only when the wiki outgrows simple navigation.
- Treat the wiki as the primary artifact even if additional retrieval layers are added later.

## Reference Material

- Read `references/llm-wiki-pattern.md` for a concrete folder layout and maintenance checklist.
- Read `references/provenance.md` for source review and packaging notes.
