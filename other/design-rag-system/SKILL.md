---
name: design-rag-system
description: Use when building LLM applications that need to answer questions about proprietary, recent, or domain-specific knowledge that is not in the model's training data
source: Lewis et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" NeurIPS (2020); LlamaIndex/LangChain architectural patterns; Anthropic RAG best practices
tags: [ai, llm, rag, architecture]
related: [apply-bm25-ranking, design-rag-pipeline]
verified: true
---

# Design RAG System

Build a Retrieval-Augmented Generation system that grounds LLM responses in retrieved documents to reduce hallucination and enable knowledge updates without retraining.

## Why This Is Best Practice

**Adopted by:** Microsoft (Azure AI Search + OpenAI), Anthropic (Claude with document retrieval), Google (Vertex AI Search), Salesforce Einstein GPT — all major enterprise AI platforms use RAG
**Impact:** RAG reduces hallucination rates by 38-68% compared to LLM-only generation (RAGAS benchmarks); enables knowledge updates in hours vs. months required for fine-tuning; reduces LLM costs by limiting context size
**Why best:** LLMs cannot know proprietary or post-training data; fine-tuning is expensive and doesn't generalize; RAG provides fresh, attributable, updatable knowledge

Sources: Lewis et al. NeurIPS 2020; Gao et al. "Retrieval-Augmented Generation for Large Language Models: A Survey" (2023); LlamaIndex documentation

## Steps

1. **Define the knowledge corpus** — Identify the documents the system must retrieve from: internal wikis, PDFs, databases, code repositories, API documentation. Define update frequency (hourly, daily, real-time). Update frequency determines whether you need batch indexing or streaming indexing.

2. **Design document ingestion pipeline** — Build an automated pipeline: fetch documents → parse (PDF, HTML, DOCX) → extract text → chunk → embed → index. Handle incremental updates: new documents, modified documents, and deletions. Use checksums to detect changes and avoid re-indexing unchanged documents.

3. **Choose a chunking strategy** — Chunking strategy is the most impactful RAG design decision. Fixed-size chunks (512-1024 tokens with 10-20% overlap) work for uniform documents. Semantic chunking (split at paragraph/section boundaries) works better for structured documents. Smaller chunks improve precision; larger chunks improve context. Test empirically.

4. **Select an embedding model** — Choose based on: domain (general vs. domain-specific), multilingual requirement, dimension size (768 vs. 1536), and retrieval benchmarks (MTEB leaderboard). OpenAI text-embedding-3-small is cost-effective for general use. Domain-specific embeddings outperform general embeddings for technical corpora.

5. **Build the vector index** — Use a vector database (Pinecone, Weaviate, pgvector, Qdrant, ChromaDB) or a managed service (Azure AI Search, Vertex AI Matching Engine). Configure: distance metric (cosine similarity for normalized embeddings), index type (HNSW for approximate nearest neighbor), and metadata filtering support.

6. **Implement hybrid retrieval** — Combine dense (vector) retrieval with sparse (BM25/keyword) retrieval. Dense retrieval handles semantic similarity; sparse handles exact term matching. Re-rank results using a cross-encoder (Cohere Rerank, BGE Reranker) after hybrid retrieval. Hybrid consistently outperforms either method alone.

7. **Design the retrieval query** — Don't use the raw user question as the retrieval query. Expand queries: hypothetical document embeddings (HyDE), query rewriting, multi-query generation. For conversational systems: include conversation history in query construction to handle coreference ("what about the second option?").

8. **Construct the generation prompt** — Format retrieved context with clear delimiters: `<document source="..." chunk_id="...">{{text}}</document>`. Instruct the model to: answer only from provided documents, cite sources, and state when the answer is not in the documents. Place context before the question in the prompt.

9. **Implement faithfulness validation** — For high-stakes applications: add a faithfulness check that verifies the generated answer is grounded in retrieved documents (NLI classifier or LLM-as-judge). Reject or flag responses that make claims not supported by the retrieved context.

10. **Evaluate with RAG-specific metrics** — Use RAGAS or TruLens: retrieval precision (are retrieved docs relevant?), retrieval recall (are all relevant docs retrieved?), answer faithfulness (is the answer grounded in retrieved docs?), and answer relevance (does the answer address the question?). Establish baselines and track metrics on every pipeline change.

## Rules

- Never send raw retrieved chunks to the LLM without source metadata — attribution requires knowing which document each chunk came from.
- The retrieval quality ceiling caps generation quality; invest in retrieval evaluation before tuning the generation prompt.
- Chunk size and retrieval top-k must be balanced against the LLM context window; retrieved context that exceeds the context window requires summarization or re-ranking to select the most relevant chunks.
- Always include a graceful "I don't know" path when retrieved documents don't contain the answer; hallucination is worse than abstention.

## Common Mistakes

- **No chunking overlap** — chunks with no overlap lose context at boundaries; a sentence split across two chunks retrieves half the context from each; 10-20% overlap prevents boundary artifacts.
- **Single-strategy retrieval** — pure vector search misses exact terminology (product names, error codes); hybrid retrieval is almost always better.
- **Ignoring metadata filtering** — retrieving from the entire corpus when a user asks about a specific product version returns irrelevant chunks; filter by metadata (date, category, product) before vector search.
- **No evaluation harness** — RAG systems have many tunable parameters (chunk size, top-k, embedding model, reranker); without systematic evaluation, parameter tuning is guesswork.

## When NOT to Use

- Questions answerable from the LLM's training data where hallucination risk is acceptable
- Real-time data needs where document latency (indexing lag) makes retrieved information stale at query time
- Structured data queries where SQL or a database API is more precise and reliable than semantic retrieval
