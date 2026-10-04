---
name: retune
description: Rebuild and re-optimize the llmwiki vault's retrieval pipeline (corpus index + AutoRAG hybrid trial). Use when the user says /retune, after any /ingest adds pages, when `llmwiki ask` can't retrieve a page that `llmwiki search` finds, after editing .rag/config.yaml, or on suspicion the deployed pipeline is stale. Not for answering questions (/query) or adding content (/ingest).
---

# Retune the llmwiki retrieval pipeline

CLI: `llmwiki` (vault `/mnt/c/Users/emmaj/llmwiki`, engines in `.rag/`). Retuning = `llmwiki index` (rebuild corpus parquet from vault markdown) then `llmwiki tune` (AutoRAG trial: BM25 + vector + hybrid-RRF race, scored on auto-generated QA, winner deployed).

## When to call

- After /ingest lands new pages — until then they are `search`-visible but `ask`-invisible (ask retrieves from trial-time indexes).
- **Staleness tell:** `llmwiki search X` finds a page but `llmwiki ask` about it refuses — that's the signature; retune, don't debug retrieval.
- After changing `.rag/config.yaml` (nodes, prompt, models).
- NOT after mere page edits to already-indexed topics — BM25/embeddings tolerate content drift; batch retunes instead.

## Procedure

1. `llmwiki index` — seconds; prints page count. Extra roots: `llmwiki index wiki Clippings`.
2. Corpus grew a lot or QA set should refresh? Delete `.rag/data/qa.parquet` first — tune reuses an existing QA set otherwise.
3. `llmwiki tune` — run backgrounded, 10–40 min on the 3090 (QA gen if needed + embed corpus + trial). Tell the user it's running.
4. On completion, sanity-check the leaderboard: read `.rag/data/project/<latest>/*/*/summary.csv` — expect hybrid ≥ BM25 ≥ vector on retrieval_recall, ROUGE ≈ 0.6. A collapsed metric (0.0) means a broken stage, not a bad corpus.
5. Verify end-to-end with one `llmwiki ask` about a recently added page.

## Known failure modes (all hit in practice, all guarded — do not re-diagnose from scratch)

- **QA gen crashes on batch 2** (`Event ... bound to a different event loop`): AutoRAG's legacy QA creator opens a new loop per cache batch while the Ollama client stays bound to the first. Guard: `cache_batch` ≥ `content_size` in `.rag/engines/tune.py`. If it recurs, that guard was lowered.
- **`doc_id ... not found in corpus_data` from ask after tune**: stale project-level corpus copy. `tune.py` deletes `data/project/data/{corpus,qa}.parquet` before each trial for exactly this; if seen, the deletion was removed.
- **`ollama is not a valid llm name`**: this AutoRAG build needs `autorag.generator_models["ollama"] = Ollama` registered before Evaluator/Runner — present in both `tune.py` and `autorag_ask.py`.
- **`node ... is not supported`**: this build uses `lexical_retrieval`/`semantic_retrieval`/`hybrid_retrieval` node types (docs still show the retired `retrieval`).
- Trials accumulate as `data/project/0,1,2…`; `ask` uses the highest. Old trials are safe to delete except the newest.
