---
name: building-rag-pipelines
description: End-to-end RAG architecture — chunking, embedding, retrieval, reranking, augmentation, grounding, evaluation. Provider- and store-agnostic.
when_to_use: >
  Reach for this when designing or improving a retrieval-augmented generation system end-to-end:
  ingestion → chunking → embedding → storage → retrieval → rerank → augment → answer → eval.
  For the vector store itself use using-weaviate or using-pgvector; for the embedding/completion
  model defer to the provider skill (using-openai-platform / using-anthropic-platform /
  using-perplexity-platform); for graph-based agent orchestration around retrieval use
  building-langgraph-agents; for memory layered on top of retrieval use building-agent-memory;
  for tracing/eval dashboards use using-langfuse. **ALWAYS WebFetch the current docs for your
  chosen embedding provider, vector store, and reranker BEFORE recommending a model name,
  dimension, distance op, or top-k default — embedding catalogs and reranker APIs change faster
  than any training snapshot.**
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Building RAG Pipelines — Architecture Quick Reference

RAG = retrieve relevant context from an external store, then condition the LLM on it.
This skill covers the *architecture* and design choices; defer model names, store APIs, and
client SDKs to the respective provider/store skills.

---

## Stay current — DO NOT rely on training-data knowledge of embeddings, rerankers, or eval frameworks

Embedding catalogs (dimensions, max input, prices), rerankers (Cohere Rerank, Voyage rerank,
open-source cross-encoders), and eval frameworks (Ragas, TruLens, DeepEval) all churn fast.
**Before** you (a) pick an embedding model, (b) pick a reranker, (c) cite a recall@k benchmark,
(d) recommend a chunking default, or (e) wire an eval metric, you **MUST** WebFetch the live
source and cite it:

- **Embedding providers (defer to provider skill's Stay-current):**
  - OpenAI embeddings: https://platform.openai.com/docs/guides/embeddings
  - Anthropic (no first-party embeddings yet — verify): https://docs.claude.com/en/docs/build-with-claude/embeddings
  - Cohere embeddings: https://docs.cohere.com/docs/embeddings
  - Voyage AI: https://docs.voyageai.com/docs/embeddings
- **Vector stores (defer to store skill):** using-weaviate, using-pgvector.
- **Rerankers:** https://docs.cohere.com/docs/rerank-overview ;
  https://docs.voyageai.com/docs/reranker
- **Ragas (eval):** https://docs.ragas.io/en/stable/
- **TruLens:** https://www.trulens.org/

Cite source URL + fetch date for every model / dimension / metric assertion. For *provider*
calls (embed, complete, structured output), the provider skill's Stay-current rules apply —
this skill defers to them.

---

## When to Use

Load this skill when:
- Designing a new RAG feature ("answer from our docs", "search our knowledge base")
- Re-architecting an existing retrieval pipeline (recall complaints, hallucinations, latency)
- Choosing between chunking strategies, retrieval modes, or rerankers
- Adding evaluation/observability to an existing RAG system
- Files like `ingest.py`, `retriever.ts`, `chunker.py`, `rerank.py` are present

---

## Pipeline Stages

```
┌─────────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐   ┌────────┐   ┌────────┐
│  INGESTION  │──▶│ CHUNKING │──▶│  EMBED  │──▶│  STORE  │──▶│RETRIEVE│──▶│ RERANK │
└─────────────┘   └──────────┘   └─────────┘   └─────────┘   └────────┘   └────────┘
                                                                              │
                                                                              ▼
                                  ┌──────────┐   ┌─────────┐   ┌─────────────┐
                                  │   EVAL   │◀──│ ANSWER  │◀──│   AUGMENT   │
                                  └──────────┘   └─────────┘   └─────────────┘
```

---

## 1. Ingestion

- **Source connectors**: filesystems, S3, Confluence, Notion, Slack, GitHub, RSS, CRMs.
- **Normalize to text**: strip boilerplate, preserve structure markers (headings, tables, code).
- **Preserve metadata**: source URL, title, author, mtime, tenant, ACL, doc type.
- **Idempotency**: hash content → skip re-embed if unchanged. Critical for cost control.
- **Versioning**: keep doc_id + version + supersedes pointer; soft-delete old versions.

```python
def doc_hash(content: str, metadata: dict) -> str:
    import hashlib, json
    payload = content + json.dumps(metadata, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()
```

---

## 2. Chunking Strategies

| Strategy | When to use | Tradeoffs |
|----------|-------------|-----------|
| **Fixed-size (tokens)** | Default starting point; uniform docs | Cuts mid-sentence; lose context |
| **Sentence / paragraph** | Prose docs, transcripts | Variable size; boundaries make sense |
| **Structural** (heading-aware) | Markdown, HTML, RST | Best context preservation; needs parser |
| **Semantic** (embedding-based splits) | Long unstructured docs | Compute overhead at ingest |
| **Late chunking** | Long-context embedding models | Embed whole doc once, pool per chunk |
| **Code-aware** (AST split) | Source code corpora | Requires per-language parser |

### Defaults to start from (then measure)

- Chunk size: **300–800 tokens**
- Overlap: **10–20%** of chunk size
- Always store: `chunk_text`, `chunk_index`, `doc_id`, `parent_section`, source metadata.

### Parent-document / small-to-big

Index small chunks (precision); return the *parent* section (recall) to the LLM:

```python
# Embed small (~256 tok) chunks but store parent (~2k tok) section id alongside
chunk = {"text": small, "parent_id": section_id, "embedding": embed(small)}
# At retrieval: fetch top-k chunks, dedupe to parent_ids, fetch full parents
```

---

## 3. Embedding

Choose the model from the **provider skill** (`using-openai-platform`,
`using-anthropic-platform`, etc.). Decisions this skill cares about:

- **Dimension**: drives storage cost and index size (1536 / 1024 / 768 / 384 common).
- **Max input tokens**: must exceed your chunk size + overlap.
- **Asymmetric vs symmetric**: some models have separate `query` vs `passage` instructions —
  honor them; ~5-10pp recall on the table.
- **Multilingual**: pick a multilingual model if corpus is mixed-language.
- **Batching**: embed in batches of 64–256 at ingest; respect provider rate limits.
- **Quantization**: store as `halfvec` (pgvector) or float16 (Weaviate) at scale.

```python
def embed_batch(texts: list[str], batch_size: int = 96) -> list[list[float]]:
    out = []
    for i in range(0, len(texts), batch_size):
        out.extend(provider.embed(texts[i:i+batch_size]))
    return out
```

---

## 4. Storage

Defer to the vector-store skill:
- **`using-pgvector`** — Postgres-native, hybrid SQL filters, no second datastore.
- **`using-weaviate`** — dedicated, scales further, multi-tenant native.

Both support: filter metadata, hybrid (vector+keyword), and top-k. The retrieval *strategy*
below is store-agnostic.

---

## 5. Retrieval

### Top-k pure vector

Start at **k = 10–20** for downstream reranking; **k = 3–5** if no reranker.

### Hybrid (dense + sparse)

Combine vector similarity with BM25/keyword. Most stores expose a hybrid mode; otherwise use
**Reciprocal Rank Fusion (RRF)**:

```python
def rrf(rankings: list[list[str]], k: int = 60) -> dict[str, float]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return scores
```

### MMR (Maximal Marginal Relevance)

Diversify top-k to avoid redundant near-duplicates:

```
selected = []
while len(selected) < k:
    best = argmax over candidates of: λ * sim(q, d) - (1-λ) * max_{s in selected} sim(d, s)
    selected.append(best)
```

`λ` typical = 0.5–0.7. Use when corpus has many near-duplicates.

### Metadata filtering

Filter BEFORE similarity (where the store supports it):
- `tenant_id` (security; never optional in multi-tenant)
- `doc_type`, `language`, `created_at` (recency)
- ACL labels (security; defense in depth)

### Recency / freshness

Decay similarity by age:
```
adjusted = similarity * exp(-age_days / half_life_days)
```

---

## 6. Reranking

Rerankers (cross-encoders) score `(query, candidate)` pairs jointly — much more accurate than
bi-encoder similarity but slower. Apply to top-k = 20–100 from retrieval to get top-n = 3–10.

Options (verify currency):
- **Cohere Rerank** (`rerank-v3.5` family) — managed API
- **Voyage Rerank** — managed API
- **Open-source cross-encoders** — BGE, Jina rerank (self-host)
- **LLM-as-reranker** — Claude/GPT scoring each pair (expensive; high quality; useful for eval)

```python
ranked = cohere.rerank(query=q, documents=candidates, top_n=5, model="rerank-v3.5")
top = [candidates[r.index] for r in ranked.results]
```

---

## 7. Prompt Augmentation & Grounding

### Context block layout

```
You are a helpful assistant. Answer ONLY from the provided context. If the context does not
contain the answer, say "I don't know based on the provided context."

# Context
[1] {source_title} ({source_url})
{chunk_1_text}

[2] {source_title} ({source_url})
{chunk_2_text}

# Question
{user_question}

# Answer
Cite sources inline like [1], [2].
```

- **Number every chunk** so the model can cite by id.
- **Include source URL/title** in each chunk header so citations are traceable.
- **Refuse-out-of-context** instruction reduces hallucinations measurably.
- **Order matters**: put highest-rank chunks at the *end* (recency bias of attention) or both
  ends (lost-in-the-middle). Measure on your data.

### Citation format

Force inline numeric citations; post-process to resolve `[1]` → URL.

```python
import re
def resolve_citations(answer: str, chunks: list[dict]) -> str:
    return re.sub(r"\[(\d+)\]",
                  lambda m: f"[{m.group(1)}]({chunks[int(m.group(1))-1]['url']})",
                  answer)
```

---

## 8. Evaluation

Don't ship RAG without metrics. Minimum viable eval:

| Metric | What it measures | Tooling |
|--------|-------------------|---------|
| **Recall@k / NDCG@k** | Did retrieval surface the right chunks? | Custom + golden set |
| **Context precision** | Of retrieved chunks, how many were relevant? | Ragas / LLM-as-judge |
| **Faithfulness** | Is the answer grounded in the context? | Ragas, TruLens |
| **Answer relevance** | Does the answer address the question? | Ragas, LLM-as-judge |
| **Latency p50/p95** | End-to-end + per-stage | OpenTelemetry / Langfuse |
| **Cost / query** | $ per answer | Provider usage + Langfuse |

### Golden set

Build a small (50–200) `(question, ideal_chunk_ids, ideal_answer)` set. Run on every change.
Even a tiny set catches regressions LLM-as-judge will miss.

### Ragas snippet

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

result = evaluate(
    dataset,                         # HF dataset with question/answer/contexts/ground_truth
    metrics=[faithfulness, answer_relevancy, context_precision],
)
print(result)
```

Pipe traces to `using-langfuse` for production observability and dataset-driven A/B.

---

## Common Patterns

- **Hybrid > pure vector** on real-world queries (acronyms, product names, IDs). Always.
- **Rerank top-50 → top-5** beats bigger embedding model on most use cases for a fraction of
  the cost.
- **Small-chunk index, big-chunk context** — precision in retrieval, recall in the LLM context.
- **Query rewriting** — for short/ambiguous queries, have the LLM expand to 3 variants and
  fuse with RRF.
- **Multi-vector per doc** — embed `title`, `summary`, and `body` separately; fuse.
- **Cite or refuse** — system prompt enforces "answer from context only".

---

## Anti-Patterns

- **Shipping without an eval set.** "Looks good on a few queries" ≠ working.
- **One giant chunk per doc.** Wastes context, hides relevance signal.
- **Re-embedding entire corpus on every change.** Use content hashes; only re-embed deltas.
- **Mixing embedding models in one index.** Distances are not comparable. Re-embed on switch.
- **Filtering after retrieval.** Top-k of irrelevant tenant → empty results. Filter first.
- **No metadata.** You'll regret it the first time you need to debug "why did this come back?"
- **Trusting LLM-as-judge alone.** Pair it with a golden-set recall metric.

---

## See Also

- `using-pgvector` — Postgres-native vector store (default for "we already have Postgres").
- `using-weaviate` — dedicated vector DB; large-scale / multi-tenant SaaS.
- `using-openai-platform`, `using-anthropic-platform`, `using-perplexity-platform` —
  embedding + completion models (own their Stay-current).
- `building-agent-memory` — long-term memory layered on top of a vector store.
- `building-langgraph-agents` — orchestrate retrieve→rerank→answer as graph nodes.
- `building-tool-orchestration` — expose retrieval as a tool the LLM can call.
- `using-langfuse` — production tracing, prompt versioning, dataset eval.
