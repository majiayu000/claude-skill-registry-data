---
name: code-semantic-search
description: Design, evaluate, or operate privacy-aware semantic and hybrid search over a large codebase using structural chunks, lexical retrieval, optional embeddings.
license: MIT
---

# Semantic Code Search

Start with repository search, symbol indexes, and targeted reads. An index is justified when the corpus is too large, natural-language concepts do not map to identifiers, or repeated discovery cost exceeds indexing cost.

## Requirements

1. Define queries and relevance judgments before choosing a backend.
2. Inventory languages, generated/vendor/secrets paths, repository size, update rate, data boundary, hardware, and latency target.
3. Chunk on symbols and syntax boundaries when a verified parser exists; preserve file path, symbol, line range, language, commit/hash, and parent context.
4. Use lexical/BM25 and exact identifier matching as a strong baseline. Add embeddings only when evaluation shows a measurable recall gain.
5. Prefer local processing for private code. Any external embedding/vector/reranking service requires explicit authorization, retention/privacy review, and secret filtering.
6. Keep embedding model/backend configurable and record its exact version, dimensions, tokenizer, normalization, and index schema. Do not choose a provider/model automatically.
7. Deduplicate chunks, cap generated/minified content, and exclude secrets before indexing.
8. Incrementally update by content hash; delete stale chunks when files disappear or symbols move.

## Retrieval pipeline

Normalize the query without destroying identifiers, retrieve lexical and semantic candidates, fuse ranks, rerank only a small bounded set, diversify near-duplicates, and return source-linked snippets. Never answer from vector text without reopening the current source file; the index may be stale.

## Evaluation

Create a labeled set of realistic "where/how/what depends on" questions. Measure recall@k, MRR/nDCG, exact-symbol recall, stale-result rate, latency, index size, build time, and privacy failures. Compare lexical-only, semantic-only, and hybrid. Test renamed symbols, cross-language calls, common words, generated code, and deleted files.

## Completion gate

- every result links to a current path/symbol/range and commit/hash;
- direct search fallback remains available;
- private code stayed inside the approved boundary;
- index/update/delete behavior was tested;
- chosen complexity beats the baseline on the evaluation set;
- setup, dependencies, rebuild, and removal steps are documented.
