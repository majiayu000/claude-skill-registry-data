---
name: wiki-query
description: Query wiki via RAG collection + direct reads, returning relevant excerpts. Use when Claude can't answer from target files alone, when user says "search wiki", or before opus-deep-audit for technique notes.
---

# wiki-query

## Purpose
Retrieve from the personal knowledge base before resorting to fresh
reasoning. Past findings, target intel, and technique patterns often
have the answer Claude needs.

## Inputs
- `<question>` (free text).

## Steps
1. `docs_query(collection="wiki", query="<question>", k=8)`. Returns
   excerpts with source paths + scores.
2. If top-score < threshold (default 0.55), do a fallback grep across
   `wiki/` (case-insensitive, multi-keyword). Combine the two
   recall sets.
3. Score-rank, deduplicate by source path.
4. If best result clearly answers the question, return it with the
   source path link.
5. If results are weak/partial AND the question is genuinely useful
   for future work, optionally suggest a new wiki page (draft inline,
   ask user to confirm before writing). This is Karpathy's
   "query can create new wiki pages" pattern.

## Outputs
- Returns excerpts inline to Claude's reasoning context (not
  persisted unless step 5 fires and user confirms).
- If a new page was created, append entry to `wiki/_ingest_log.jsonl`
  via `wiki-ingest`.

## Failure modes
- `wiki` collection missing → user hasn't ingested anything yet.
  Suggest seeding via `wiki-ingest` on any past findings.
- `docs_query` errors → fall back to pure grep.

## Notes
This skill is *cheap* — Claude should fire it eagerly. The wiki
exists to be queried.
