---
name: swap-embeddings
description: Change the embedding model used to index and search documents (OpenAI, Cohere, Voyage, a local server). Use when the user decides on a different or cheaper embedding model, or asks about vector dimensions. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the embedding model

- **Interface:** `Embedder` (`name`, `min_score`, `embed(texts)`) in
  `apps/ai/app/embeddings.py`.
- **Today:** `HashingEmbedder` locally (lexical, no model; refused in production) and
  `ProviderEmbedder` for any Pydantic AI embedding model, asked for
  `EMBEDDING_DIMENSIONS` (1536, `apps/ai/app/db/models.py`). `create_embedder` picks one.
- **Env:** `AI_EMBEDDINGS` (`hashing` or a model name such as
  `openai:text-embedding-3-small`), `AI_MIN_RELEVANCE` (cosine floor), and the provider's
  key (e.g. `OPENAI_API_KEY`).

## Swap

1. Same dimension (1536): set `AI_EMBEDDINGS` and the key, then re-index every document
   (vectors from different models aren't comparable; documents keep their text).
2. A different dimension: a migration changing `ai.chunk`'s vector column and its HNSW
   index (db-change skill), `EMBEDDING_DIMENSIONS` in `apps/ai/app/db/models.py`, and a
   re-index.
3. A model Pydantic AI can't reach: a class with the `Embedder` shape, chosen in
   `create_embedder`.
4. Calibrate `AI_MIN_RELEVANCE` for the new model with `bun run --cwd apps/ai evals`.

## Tests

`apps/ai/tests/test_units.py` (embedders), `apps/ai/tests/test_service.py` (indexing and
retrieval against Postgres), `apps/ai/tests/test_models_match_db.py` after a migration.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too. The change is in apps/ai, so the
   `python-reviewer` agent as well.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
