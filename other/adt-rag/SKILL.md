---
name: rag
description: Build and debug Retrieval-Augmented Generation pipelines — chunking, embedding, retrieval, reranking
triggers:
  - rag
  - retrieval
  - build a rag
  - semantic search
  - document retrieval
  - vector search
---

# RAG

Build production-ready Retrieval-Augmented Generation pipelines. Don't retrieve blindly — curate what reaches the model.

## Pipeline Stages

```
Documents → Chunk → Embed → Index → [Query] → Retrieve → Rerank → Augment → Generate
```

## 1. Chunking Strategy

Choose based on document structure:

| Strategy        | Use when                         | Chunk size                    |
| --------------- | -------------------------------- | ----------------------------- |
| Fixed-size      | Uniform docs (logs, transcripts) | 256–512 tokens, 10% overlap   |
| Semantic        | Articles, manuals, code          | Split on headings/paragraphs  |
| Hierarchical    | Nested content (books, wikis)    | Parent + child chunks         |
| Sentence-window | QA over dense text               | 3–5 sentences, sliding window |

Rules:

- Always include metadata (source, section, page, timestamp)
- Overlap prevents context being split at chunk boundaries
- Smaller chunks → better precision; larger chunks → better context

## 2. Embedding

```text
embed(chunk) → vector[dim]
```

- Use the same model for indexing AND querying — mismatches break retrieval
- Normalize vectors before indexing (cosine similarity requires unit vectors)
- Re-embed when switching models — old vectors are incompatible

Common models: `text-embedding-3-small`, `text-embedding-ada-002`, `all-MiniLM-L6-v2`

## 3. Retrieval

**Dense retrieval** (semantic): cosine similarity over embeddings — good for paraphrase matching
**Sparse retrieval** (BM25): keyword overlap — good for exact terms, names, codes
**Hybrid**: combine both with RRF (Reciprocal Rank Fusion) — best for production

```text
Top-K candidates: start with K=20, rerank to top 3–5
```

**Query expansion**: generate 2–3 query variants before retrieval to improve coverage

## 4. Reranking

Never trust retrieval order alone — rerank before passing to LLM:

1. Cross-encoder reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) — slow but accurate
2. LLM reranker: ask the model to score relevance (1–5) for each candidate
3. Reciprocal Rank Fusion: no reranker needed — combine multiple retrieval passes

## 5. Context Augmentation

```text
System: You are a helpful assistant. Use only the provided context.
Context:
[1] <most relevant chunk>
[2] <second chunk>
...
User: <original query>
```

Rules:

- Most relevant first — LLMs attend more to the beginning
- Include source citations in chunks (`[Source: doc.pdf, p.12]`)
- Set a hard token budget for context (e.g., 2000 tokens) — trim from the bottom

## Debugging Checklist

- [ ] Retrieval: are the right chunks being found? Log top-K before reranking
- [ ] Embedding mismatch: same model for index and query?
- [ ] Chunk quality: are chunks coherent? No mid-sentence splits?
- [ ] Hallucination: is the model ignoring retrieved context? Add grounding instruction
- [ ] Latency: which stage is slowest? Profile chunk → embed → retrieve → rerank

## Output

```text
RAG Report
──────────
Stage:     <pipeline stage>
Chunks:    <total chunks indexed>
Retrieved: <K candidates>
Reranked:  <N passed to LLM>
Latency:   <ms per stage>
Issue:     <root cause if failing>
```
