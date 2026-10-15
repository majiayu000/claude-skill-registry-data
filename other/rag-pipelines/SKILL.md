---
name: rag-pipelines
description: RAG systems with embeddings, vector stores, retrieval.
version: 1.0.0
author: Hermes Agent
platforms: [windows, linux, macos]
---

# RAG Pipelines

Build, optimize, and debug Retrieval-Augmented Generation systems: document ingestion, chunking, embeddings, vector storage, retrieval, and LLM answer synthesis. Directly supports Harsh's AI roadmap (Zoho CRM AI Assistant, Multi-Document RAG, LangGraph agents).

## Trigger Conditions
- User asks to build a RAG system, knowledge base, or Q&A bot over documents
- Need chunking, embedding, vector DB, or retrieval strategies
- Debugging poor retrieval results (missed context, hallucinated answers)
- Integrating RAG with Zoho CRM/Creator data or LLM APIs

## 1. Architecture (standard pipeline)

```
Documents → Split/Chunk → Embed → Vector Store → Retrieve (query) → Augment → LLM → Answer
```

Choose components:
| Stage | Options |
|---|---|
| Embeddings | OpenAI text-embedding-3-small, Gemini embedding-001, local all-MiniLM-L6-v2 (sentence-transformers) |
| Vector store | ChromaDB (local, zero-config), FAISS (fast, in-memory), Qdrant/Milvus (scalable), pgvector (SQL) |
| Chunking | RecursiveCharacterTextSplitter (default 500-1000 chars, 10-20% overlap) |
| Retrieval | Top-k (default k=4-8), hybrid (BM25 + vector), MMR for diversity |
| LLM | Any chat API (OpenAI, Gemini, local Ollama) |

## 2. Chunking rules (biggest quality lever)

- Split on semantic boundaries: headers, paragraphs, code blocks. Never mid-sentence.
- Recursive splitter: `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150, separators=["\n\n", "\n", ". ", " "])`
- Tables/JSON: keep as atomic chunks; don't split across rows
- Metadata: attach source, page, section header to every chunk. Retrieval returns citations from it.
- 400-1000 chars per chunk works for most business docs

## 3. Vector store pattern (ChromaDB, local, no keys)

```python
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # local, free
client = chromadb.PersistentClient(path="./kb")
col = client.get_or_create_collection("docs", metadata={"hnsw:space": "cosine"})

# upsert chunks with embeddings + metadata
col.add(ids=[f"chunk-{i}"], embeddings=model.encode(chunks).tolist(),
        documents=chunks, metadatas=[{"source": src} for src in sources])

# query
hits = col.query(query_embeddings=model.encode([q]).tolist(), n_results=5)
```

## 4. Retrieval + answer synthesis (LLM API)

```python
import openai  # or requests to any chat-completions endpoint

context = "\n---\n".join(hits["documents"][0])
prompt = f"""Answer using ONLY the context below. Cite source per claim.
If the answer is not in the context, say so.

CONTEXT:
{context}

QUESTION: {q}"""

resp = openai.chat.completions.create(model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}])
```

Hybrid retrieval (better precision): combine vector top-k with BM25 (rank_bm25 lib) and merge scores.

## 5. RAG on Zoho data (Harsh's pattern)

- Zoho CRM/Creator records are structured: convert each record to a text block (`"Deal: X | Amount: Y | Stage: Z"`) then embed
- Rebuild the index on a schedule (cron) or after record changes via webhook
- Multi-document RAG: one collection per client/app, filter by metadata on query (`where={"client": "acme"}`)
- Works inside Deluge too: call your RAG API endpoint via `invokeurl`

## 6. Debugging checklist (when answers are bad)

| Symptom | Fix |
|---|---|
| Answer not in docs | k too small (raise to 8), chunks too big, wrong collection |
| Irrelevant hits | Better embeddings (OpenAI/Gemini), add reranker (cross-encoder), filter by metadata |
| Hallucination | Grounding prompt (answer only from context), cite sources, lower temperature (0.1-0.2) |
| Slow | Cache embeddings, use smaller model, limit context to top-k |
| Missing recent data | Rebuild index, add incremental ingestion, check chunk overlap |

## 7. Pitfalls

- ❌ Do not embed the whole document as one vector - retrieval fails on long docs
- ❌ Do not skip metadata - you lose source citations and filtering
- ❌ Do not use temperature >0.3 for grounded answers
- ✅ Always test retrieval first (query the store directly) before blaming the LLM
- ✅ Keep embeddings model consistent between index time and query time (must match)
- ✅ Store the model name + chunk config in the collection metadata for reproducibility

## References
- OpenAI embeddings docs: https://platform.openai.com/docs/guides/embeddings
- ChromaDB: https://docs.trychroma.com
- LangChain text splitters: https://python.langchain.com/docs/concepts/text_splitters/
