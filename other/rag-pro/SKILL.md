---
name: rag-pro
description: RAG guidance — chunking, retrieval tuning, hybrid search, reranking, citations, evaluation, and production RAG.
category: development
---

## Overview

RAG (Retrieval-Augmented Generation) grounds LLMs in your data: retrieve relevant chunks, stuff them into the prompt, generate answers with citations. It's the highest-ROI LLM pattern — and the one where "it works in the demo" most often collapses in production. The unglamorous truth: chunking, retrieval quality, and evaluation matter far more than model choice.

This skill covers production RAG end to end: ingestion and chunking, retrieval tuning (hybrid, reranking, filters), synthesis with citations, evaluation, and the operational concerns of a live system.

## When to use

- Building question-answering over documents.
- Improving RAG answer quality.
- Tuning chunking and retrieval.
- Adding citations to generated answers.
- Evaluating RAG systems.
- Operating RAG in production (updates, access control, monitoring).

## Core concepts

- **The pipeline.** Ingest → chunk → embed → index → retrieve → rerank → synthesize → cite. Every stage has quality levers; failures compound — debug stage by stage, not end-to-end.
- **Chunking.** The highest-leverage decision: semantic boundaries (sections, paragraphs) over fixed sizes; 300-800 tokens typical with overlap; hierarchical (small chunks + parent context); metadata per chunk (source, section, date). Bad chunks cap everything downstream.
- **Embeddings.** Domain-appropriate model, fixed for the index; chunk text + metadata strategies (what gets embedded vs filtered). Re-embed everything on model change.
- **Retrieval.** Top-k similarity as the baseline; `similarity_top_k` tuning (more ≠ better — noise dilutes); metadata pre-filtering (tenant, date, source) before similarity.
- **Hybrid search.** Dense + BM25 fused (RRF) — semantic for paraphrases, keyword for exact terms (names, codes, SKUs). Usually the single biggest retrieval win after chunking.
- **Reranking.** Cross-encoder or LLM rerank over top-20→top-5 — the cheapest quality improvement in the pipeline; slower but applied to few candidates.
- **Query transformations.** HyDE (hypothetical answer embedding), query rewriting, multi-query expansion — bridging the vocabulary gap between questions and documents. Useful when queries and docs speak different languages.
- **Context assembly.** Order (best first? best last — "lost in the middle"), deduplication, token budgeting, `LongContextReorder`. More context isn't better — relevant context is.
- **Synthesis.** The generation prompt: "answer ONLY from context," citation requirements, refusal behavior for unanswerable questions. The prompt is a reliability control, not decoration.
- **Citations.** Chunk IDs → source references in answers — verifiability is the feature; users must be able to check. Citation format designed for the UI (inline, footnotes, side panel).
- **Refusal.** "I don't know" as a designed behavior — unanswerable questions answered confidently are the worst failure mode. Thresholds on retrieval scores + explicit instructions.
- **Evaluation.** Two layers: retrieval (hit rate, MRR@k on labeled Q&A) and answer (faithfulness — grounded in context? relevancy — answers the question?). RAGAS-style metrics automate the answer layer; human review on samples.
- **Incremental updates.** Document changes → re-chunk/re-embed affected docs → upsert; deletions as tombstones; versioned corpora. Stale RAG lies with confidence.
- **Access control.** Metadata-based filtering (user's clearance ≥ chunk's classification) — enforced at retrieval, tested adversarially. RAG over mixed-sensitivity corpora without ACLs is a breach waiting.
- **Monitoring.** Retrieval scores distribution, refusal rates, citation click-through, user feedback (thumbs up/down per answer) — quality signals from production, feeding the eval set.
- **Graph RAG.** Knowledge-graph-augmented retrieval for multi-hop questions — entities and relationships as the retrieval structure; powerful for connected data, heavy to build.
- **Agentic RAG.** The retriever as an agent tool — the LLM decides what to search, iteratively; flexible for complex research, costlier and less predictable than fixed pipelines.

## Practical workflow

1. **Build the eval set first.** 50-100 real questions with known-good answers and source chunks — before tuning anything. This set judges every later decision.
2. **Ingest and chunk deliberately.** Semantic boundaries, overlap, rich metadata; inspect chunks manually — read 50 random chunks before indexing:
   ```python
   chunks = semantic_chunk(documents, target_tokens=512, overlap=50,
                           metadata=["source", "section", "date"])
   ```
3. **Baseline retrieval.** Dense top-k; measure hit rate/MRR on the eval set. This number anchors all improvements.
   ```python
   # retrieval eval: hit rate on labeled Q&A
   hits = sum(gold_chunk in [c.id for c in retrieve(q, k=5)]
              for q, gold_chunk in eval_set)
   print(f"hit@5: {hits / len(eval_set):.2f}")
   ```

4. **Add hybrid + rerank.** BM25 fusion (RRF), then cross-encoder rerank top-20→5; measure each addition independently — keep what moves the metric.
5. **Tune assembly.** Token budgets, ordering, dedup; verify the context actually fits and the best chunks aren't buried.
6. **Write the synthesis prompt.** Grounded-only instructions, citation format, refusal behavior:
   ```
   Answer ONLY from the provided context. Cite sources as [1], [2].
   If the context doesn't contain the answer, say "I don't have information on this."
   Never invent details not present in the context.
   ```
7. **Evaluate both layers.** Retrieval metrics + faithfulness/relevancy; human spot-checks on failures; grow the eval set from production misses.
8. **Operate.** Incremental update pipelines, ACL filtering, monitoring (refusal rate, feedback, drift), scheduled re-evaluation — RAG is a living system.

## Common pitfalls

- **Blaming the LLM** — generation is rarely the problem; chunking and retrieval are.
- **No eval set** — tuning by vibes; labeled Q&A before any optimization.
- **Arbitrary chunking** — fixed 1000-char splits mid-sentence; semantic boundaries.
- **Pure dense retrieval** — missing exact terms; hybrid search.
- **Skipping reranking** — cheapest win ignored; rerank top candidates.
- **Context stuffing** — 50 chunks hoping for coverage; top-n discipline.
- **No citations** — unverifiable answers; cite by design.
- **Confident hallucination on gaps** — no refusal behavior; design "I don't know."
- **Stale indexes** — updated docs, old chunks; incremental update pipelines.
- **No access control** — sensitive chunks to everyone; metadata ACLs, tested.
- **Evaluating end-to-end only** — can't separate retrieval vs synthesis failures; two layers.
- **Production without monitoring** — quality decay invisible; feedback loops + re-evaluation.
- **Ignoring query-document mismatch** — jargon gaps; query rewriting/HyDE where needed.
- **Agentic RAG by default** — unpredictable cost/latency; fixed pipelines first, agentic where complexity demands it.
