---
name: local-rag
description: Use when building retrieval-augmented generation that runs entirely on one machine — chunking Markdown and documents, multilingual embeddings (for example bge-m3), a vector index in SQLite (sqlite-vec) with keyword search alongside, scoped search, evaluation with hit@k and MRR, and answering with citations through a local model. Also use when retrieval returns irrelevant chunks, the index is polluted by generated files, or private documents must never leave the machine.
---

# Local RAG (embeddings + SQLite + local LLM)

Default: Markdown-aware chunking, a multilingual embedding model served locally, `sqlite-vec` for vectors plus SQLite FTS5 for keywords in one database file, a small evaluation set, answers that cite chunk sources.

## Pipeline

1. **Collect** files from an explicit allow-list of directories. Exclude generated files, dictionaries, queues, logs and anything marked local-only — they swamp results.
2. **Chunk** by headings (keep the heading path as context), 300–800 tokens, small overlap. Store source path, heading path and a content hash per chunk.
3. **Embed** with a local model; batch requests; skip chunks whose hash is unchanged (incremental indexing).
4. **Index:** `CREATE VIRTUAL TABLE vec USING vec0(embedding float[1024])` (dimension must match the model) and an FTS5 table over the same chunk IDs.
5. **Search:** run vector and keyword search, merge with reciprocal rank fusion, optionally restrict to a scope (a directory prefix).
6. **Answer:** pass the top chunks with their source labels; instruct the model to answer only from them and cite labels; reply "not found" otherwise.

## Evaluate before tuning

- Write 20–50 questions with the file (or heading) that should be retrieved.
- Report hit@1, hit@k and MRR, plus median search latency.
- Change one thing at a time (chunk size, excluded paths, fusion weights, scope) and keep the change only if the numbers improve.
- Removing noise from the index often beats a better embedding model.

## Privacy by structure

- Mark private sources at index time (a flag per chunk) and filter them out structurally in any path that sends context to a remote model. Do not rely on prompts for this.
- Keep the database file out of version control.

## Verification loop

1. Rebuild the index from scratch; chunk counts match expectations.
2. Run the evaluation set; compare with the previous numbers.
3. Ask a question whose answer is absent; the system must say so.

## Pitfalls

- **Dimension mismatch** between model and table fails silently in some setups; assert it at start-up.
- **Mixed languages:** use a multilingual embedding model; keyword search needs a tokenizer that handles CJK (trigram tokenizer in FTS5 or character n-grams).
- **Huge chunks** dilute similarity; tiny chunks lose context. Measure.
- **Stale entries** after files are deleted: remove chunks whose source no longer exists on each run.
- **Citations that do not match** the retrieved labels indicate the model is answering from memory; reject such answers.
