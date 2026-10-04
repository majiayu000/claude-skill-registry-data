---
name: tpl-ai-ml-rag-pipeline
description: Template do pack (ai-ml/03-rag-pipeline.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/03-rag-pipeline.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: RAG Pipeline (Python + LangChain/LlamaIndex + pgvector + FastAPI)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/03-rag-pipeline.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Language:** Python 3.12
- **RAG Framework:** LangChain 0.2+ (primary) / LlamaIndex 0.10+ (alternative)
- **Embeddings:** OpenAI `text-embedding-3-small` (1536 dims)
- **Vector Store:** pgvector (PostgreSQL extension) — prod; Chroma — dev
- **Reranker:** Cohere Rerank / cross-encoder (local)
- **Lexical Search:** BM25 (rank_bm25) for hybrid retrieval
- **API:** FastAPI + Pydantic v2
- **Tracing:** LangSmith

---

## PROJECT STRUCTURE
```
rag/
├── ingestion/
│   ├── loader.py          # Document loaders (PDF, web, DB)
│   ├── chunker.py         # Chunking strategies
│   ├── embedder.py        # Batch embedding + upsert
│   └── pipeline.py        # Full ingest orchestration
├── retrieval/
│   ├── vector_store.py    # pgvector store wrapper
│   ├── bm25_index.py      # Lexical index
│   ├── hybrid.py          # Hybrid retriever (RRF fusion)
│   └── reranker.py        # Cross-encoder reranking
├── generation/
│   ├── chain.py           # RAG chain
│   └── prompts.py         # Prompt templates
├── evaluation/
│   ├── metrics.py         # RAGAS metrics
│   └── eval_dataset.py    # Golden eval set
└── api/
    └── routes.py           # FastAPI endpoints
```

---

## ARCHITECTURE RULES
1. **Chunking strategy drives answer quality** — wrong chunk size is the #1 reason RAG fails. Profile before deploying.
2. **Batch embeddings** — never embed one doc at a time; batch 100-500 at 8K tokens/batch max.
3. **Hybrid search by default** — dense (semantic) + sparse (BM25) via RRF. Semantic-only misses exact keyword matches.
4. **Rerank after retrieval** — retrieve top-20, rerank to top-5. Reranker is 10x cheaper than large LLM but improves accuracy.
5. **Evaluate with RAGAS** — measure faithfulness, answer relevancy, context precision before shipping.
6. **Metadata is non-negotiable** — every chunk stores: `source_id`, `page_num`, `created_at`, `doc_type`. Enables filtering.
7. **pgvector for production** — your app already has Postgres; adding pgvector avoids another managed service.
8. **Incremental ingestion** — hash each document; skip re-embedding unchanged docs.

---

## CHUNKING STRATEGY DECISION TABLE
```
Chunk Size │ Overlap │ Use Case
───────────┤─────────┤─────────────────────────────────────────────
256 tokens │  30     │ FAQ, dense technical docs, precise retrieval
512 tokens │  50     │ General purpose (DEFAULT)
1024 tokens│  100    │ Narrative text, long-form content, summaries
Paragraph  │  0      │ Legal docs, contracts (keep semantic unit)
Semantic   │  auto   │ When sentence boundaries matter (use SpaCy)
Recursive  │  auto   │ Markdown/code — split on headers then chars

Rules:
- Overlap = ~10-20% of chunk size
- Chunk must stand alone: test "does this chunk answer a question on its own?"
- max chunk ≤ 60% of embedding context window (8191 for text-embedding-3)
```

---

## DOCUMENT INGESTION PIPELINE

```python
# rag/ingestion/pipeline.py
import hashlib
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from rag.retrieval.vector_store import PGVectorStore
import logging

logger = logging.getLogger(__name__)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536,
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""],
)

def compute_doc_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]

async def ingest_pdf(file_path: Path, metadata: dict) -> int:
    """Ingest a PDF, skip unchanged documents. Returns chunks added."""
    loader = PyMuPDFLoader(str(file_path))
    pages = loader.load()

    doc_hash = compute_doc_hash("".join(p.page_content for p in pages))

    # Check if document already ingested (by hash)
    store = PGVectorStore()
    if await store.document_exists(doc_hash):
        logger.info(f"Document {file_path.name} unchanged, skipping")
        return 0

    # Chunk
    chunks = splitter.split_documents(pages)

    # Enrich metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            **metadata,
            "doc_hash":   doc_hash,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "source_file": file_path.name,
        })

    # Batch embed + upsert (100 chunks per batch)
    batch_size = 100
    total = 0
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        await store.aadd_documents(batch)
        total += len(batch)
        logger.info(f"Embedded {total}/{len(chunks)} chunks")

    return total
```

---

## PGVECTOR SETUP

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE documents (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content     TEXT NOT NULL,
    embedding   VECTOR(1536),
    metadata    JSONB NOT NULL DEFAULT '{}',
    doc_hash    TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast ANN search (better than IVFFlat for most workloads)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Index for metadata filtering (crucial for performance)
CREATE INDEX ON documents USING gin (metadata);
CREATE INDEX ON documents (doc_hash);
```

---

## HYBRID RETRIEVER (SEMANTIC + BM25)

```python
# rag/retrieval/hybrid.py
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
import numpy as np
from typing import List

class HybridRetriever(BaseRetriever):
    """Combines dense (pgvector) and sparse (BM25) retrieval with RRF fusion."""

    def __init__(
        self,
        vector_store: PGVector,
        all_documents: List[Document],
        k: int = 20,
        final_k: int = 5,
        rrf_k: int = 60,
    ):
        self.vector_store = vector_store
        self.k = k
        self.final_k = final_k
        self.rrf_k = rrf_k

        # Build BM25 index from corpus
        tokenized = [doc.page_content.lower().split() for doc in all_documents]
        self.bm25 = BM25Okapi(tokenized)
        self.corpus_docs = all_documents

    def _reciprocal_rank_fusion(
        self,
        dense_results: List[Document],
        sparse_results: List[Document],
    ) -> List[Document]:
        """RRF: score(d) = Σ 1/(k + rank(d))"""
        scores: dict[str, float] = {}
        doc_map: dict[str, Document] = {}

        for rank, doc in enumerate(dense_results):
            key = doc.page_content[:100]  # Use content prefix as key
            scores[key] = scores.get(key, 0) + 1 / (self.rrf_k + rank + 1)
            doc_map[key] = doc

        for rank, doc in enumerate(sparse_results):
            key = doc.page_content[:100]
            scores[key] = scores.get(key, 0) + 1 / (self.rrf_k + rank + 1)
            doc_map[key] = doc

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_map[k] for k, _ in ranked[:self.final_k]]

    def _get_relevant_documents(self, query: str) -> List[Document]:
        # Dense retrieval
        dense = self.vector_store.similarity_search(query, k=self.k)

        # Sparse retrieval (BM25)
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(bm25_scores)[-self.k:][::-1]
        sparse = [self.corpus_docs[i] for i in top_indices if bm25_scores[i] > 0]

        return self._reciprocal_rank_fusion(dense, sparse)
```

---

## RERANKING

```python
# rag/retrieval/reranker.py
import cohere
from langchain_core.documents import Document
from typing import List
import os

co = cohere.Client(os.environ["COHERE_API_KEY"])

def rerank_documents(
    query: str,
    documents: List[Document],
    top_n: int = 5,
) -> List[Document]:
    """Rerank retrieved docs using Cohere Rerank. Much cheaper than LLM."""
    if not documents:
        return []

    response = co.rerank(
        query=query,
        documents=[doc.page_content for doc in documents],
        top_n=top_n,
        model="rerank-english-v3.0",
    )

    return [documents[r.index] for r in response.results]
```

---

## RAG CHAIN

```python
# rag/generation/chain.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rag.retrieval.hybrid import HybridRetriever
from rag.retrieval.reranker import rerank_documents

SYSTEM_PROMPT = """You are a helpful assistant. Answer questions based ONLY on the provided context.
If the context doesn't contain enough information to answer, say "I don't have enough information."
Never make up facts or rely on training knowledge when context is available.

Context:
{context}
"""

def format_docs(docs) -> str:
    return "\n\n---\n\n".join(
        f"[Source: {d.metadata.get('source_file', 'unknown')}]\n{d.page_content}"
        for d in docs
    )

def build_rag_chain(retriever: HybridRetriever):
    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    def retrieve_and_rerank(question: str):
        docs = retriever.get_relevant_documents(question)
        reranked = rerank_documents(question, docs, top_n=5)
        return format_docs(reranked)

    chain = (
        {"context": retrieve_and_rerank, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
```

---

## RETRIEVAL EVALUATION

```python
# rag/evaluation/metrics.py
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

# Minimum thresholds before production deployment
QUALITY_GATES = {
    "faithfulness":      0.90,   # LLM answer is grounded in context
    "answer_relevancy":  0.85,   # Answer addresses the question
    "context_precision": 0.80,   # Retrieved chunks are relevant
    "context_recall":    0.75,   # Correct chunks are retrieved
}

def evaluate_rag_pipeline(eval_samples: list[dict]) -> dict:
    """
    eval_samples: [{"question": ..., "answer": ..., "contexts": [...], "ground_truth": ...}]
    """
    dataset = Dataset.from_list(eval_samples)
    results = evaluate(dataset, metrics=[
        faithfulness, answer_relevancy, context_precision, context_recall
    ])

    scores = results.to_pandas().mean().to_dict()

    failed = [
        metric for metric, threshold in QUALITY_GATES.items()
        if scores.get(metric, 0) < threshold
    ]

    if failed:
        raise ValueError(f"RAG quality gates failed: {failed}. Scores: {scores}")

    return scores
```
