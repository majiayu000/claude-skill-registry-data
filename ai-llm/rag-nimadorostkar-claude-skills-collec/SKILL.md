---
name: rag
description: Use when building retrieval-augmented generation. Covers chunking, embedding and hybrid search, reranking, grounding and citation, and diagnosing whether a bad answer is a retrieval failure or a generation failure.
metadata:
  category: ai
  version: 1.0.0
  tags: [rag, retrieval, embeddings, vector-search, grounding]
---

# Retrieval-Augmented Generation

## Purpose

Build a RAG system whose answers are grounded in retrieved evidence, and be able to tell — when an answer is wrong — whether the retriever failed to find the right document or the generator failed to use it.

## When to Use

- Building question answering over a document corpus.
- A RAG system that returns confident, wrong answers.
- Choosing chunking, embedding, and retrieval strategy.
- Adding citation and grounding to a generative feature.

## Capabilities

- Chunking strategies and their trade-offs.
- Embedding selection and hybrid (dense + sparse) retrieval.
- Reranking and query rewriting.
- Grounding, citation, and refusal when evidence is absent.
- Component-wise evaluation.

## Inputs

- The corpus: its size, structure, and update frequency.
- The query patterns: factual lookup, comparison, summarization, multi-hop.
- Accuracy requirements and the cost of a wrong answer.

## Outputs

- A retrieval pipeline with a measured recall figure.
- Answers with citations to the retrieved passages.
- Separate evaluation of retrieval quality and generation quality.

## Workflow

1. **Evaluate retrieval separately** — Before touching the prompt. If the correct passage is not in the top-k, no amount of prompt engineering will produce a correct answer. Measure recall@k first.
2. **Chunk on semantic boundaries** — Sections, paragraphs, or logical units. Fixed-size chunking splits a table in half and produces two useless chunks. Add overlap so a fact spanning a boundary is not lost.
3. **Retrieve hybrid** — Dense embeddings find semantic matches; BM25 finds exact terms, product codes, and names. Neither alone is sufficient; the combination materially outperforms both.
4. **Rerank the candidates** — Retrieve 50, rerank with a cross-encoder, pass the top 5. Reranking is the single highest-value addition to a naive RAG pipeline.
5. **Ground the generation** — Instruct the model to answer *only* from the provided context, to cite the passage for each claim, and to say it does not know when the context does not contain the answer.
6. **Diagnose failures by component** — For each wrong answer: was the right passage retrieved? If no, it is a retrieval problem. If yes, it is a generation problem. These have completely different fixes.

## Best Practices

- Most "the LLM hallucinated" complaints in RAG systems are retrieval failures. The model answered from its parameters because the context did not contain the answer. Check recall before blaming the model.
- Chunk size is a trade-off: small chunks retrieve precisely and lose context; large chunks carry context and dilute the embedding. Around 500-1,000 tokens with 10-15% overlap is a reasonable starting point, then measure.
- Embed the chunk with its context — the document title and the section heading prepended. A chunk that reads "It expires after 30 days" is unretrievable without knowing what "it" is.
- The model must be permitted to say "the provided documents do not answer this". Without an explicit escape, it will invent something.
- Metadata filtering before vector search (by tenant, date, or document type) is both a correctness and a performance requirement in any multi-tenant system.
- Re-embed when you change the embedding model. Mixing vectors from two models in one index produces nonsense.

## Examples

**Hybrid retrieval with reranking:**

```python
async def retrieve(query: str, tenant_id: str, k: int = 5) -> list[Chunk]:
    # 1. Rewrite the query: user questions are often poor search queries.
    search_query = await rewrite_for_retrieval(query)

    # 2. Dense and sparse, in parallel. They fail in different ways.
    dense, sparse = await asyncio.gather(
        vector_store.search(
            embed(search_query),
            k=50,
            filter={"tenant_id": tenant_id},     # a filter, not a post-hoc check
        ),
        bm25.search(search_query, k=50, filter={"tenant_id": tenant_id}),
    )

    # 3. Fuse the two rankings.
    candidates = reciprocal_rank_fusion(dense, sparse)[:50]

    # 4. Rerank with a cross-encoder: it sees the query and the passage together,
    #    which a bi-encoder embedding cannot. This is the biggest single win.
    scored = await reranker.score(query, candidates)
    return [c for c, score in scored if score > 0.35][:k]
```

**Grounded generation that is allowed to refuse:**

```python
GROUNDED_PROMPT = """\
Answer the question using only the passages provided below. 

- Cite the passage number for every factual claim, like this: [2]
- If the passages do not contain the answer, respond exactly:
  "The provided documents do not answer this question."
- Do not use knowledge from outside the passages, even if you are confident.

Passages:
{passages}

Question: {question}"""
```

**Diagnosing failures by component — the step that most teams skip:**

```python
for case in eval_set:
    retrieved = await retrieve(case.question, case.tenant_id)
    retrieved_ids = {c.id for c in retrieved}

    if not (case.gold_chunk_ids & retrieved_ids):
        record("RETRIEVAL_FAILURE", case)   # the answer was never in the context
    else:
        answer = await generate(case.question, retrieved)
        if not matches(answer, case.gold_answer):
            record("GENERATION_FAILURE", case)  # it was there and the model missed it

# Typical first result on a naive pipeline:
#   RETRIEVAL_FAILURE:  31 / 100     <- fix chunking and add a reranker
#   GENERATION_FAILURE:  6 / 100     <- fix the prompt
# Effort spent on the prompt would have addressed 6% of the problem.
```

## Notes

- Reciprocal rank fusion is a simple, parameter-free way to combine two ranked lists and works remarkably well. It requires no tuning and no score normalization.
- Contextual retrieval — prepending a model-generated summary of the chunk's place in the document before embedding it — substantially reduces retrieval failures on chunks that are ambiguous in isolation.
- If the corpus is small (under a few hundred documents) and the model's context window is large, consider skipping retrieval entirely and putting the whole corpus in the prompt. It is simpler and often more accurate.
