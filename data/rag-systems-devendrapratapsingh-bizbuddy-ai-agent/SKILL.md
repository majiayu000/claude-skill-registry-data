---
name: rag-systems
description: Retrieval-Augmented Generation (RAG) implementation - vector databases, embedding models, chunking strategies, retrieval optimization, hybrid search, reranking, evaluation metrics, and production patterns for AI knowledge systems.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# RAG Systems Skill

You are a RAG (Retrieval-Augmented Generation) Specialist. You design and implement production-grade RAG systems that combine vector search with LLMs to provide accurate, context-aware responses based on custom knowledge bases.

## Core Capabilities

### 1. Architecture Overview

**Basic RAG Flow:**
```
User Query → Embedding → Vector Search → Retrieve Context → LLM → Response
                ↑                                      ↓
           Documents → Chunk → Embed → Vector DB ← Relevance Check
```

### 2. Document Chunking Strategies

**Fixed Size Chunking:**
```python
def fixed_chunk(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
```

**Semantic Chunking:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_documents(documents)
```

**Markdown-Aware:**
```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
chunks = splitter.split_text(markdown_text)
```

### 3. Embedding Models

**OpenAI:**
```python
from openai import OpenAI
client = OpenAI()

def get_embedding(text: str, model="text-embedding-3-small"):
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
```

**Sentence Transformers (Local):**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["Text to embed"])
```

### 4. Vector Databases

**Pinecone:**
```python
from pinecone import Pinecone
pc = Pinecone(api_key="key")

index = pc.Index("rag-index")
index.upsert(vectors=[
    {"id": "doc1", "values": embedding, "metadata": {"source": "file.pdf"}}
])

results = index.query(vector=query_embedding, top_k=5)
```

**ChromaDB (Open Source):**
```python
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.create_collection("documents")

collection.add(
    embeddings=embeddings,
    documents=chunks,
    ids=[f"id_{i}" for i in range(len(chunks))]
)

results = collection.query(query_embeddings=[query_embedding], n_results=5)
```

**pgvector (PostgreSQL):**
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)
);

CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);

SELECT content, 1 - (embedding <=> query_embedding) AS similarity
FROM documents ORDER BY embedding <=> query_embedding LIMIT 5;
```

### 5. Retrieval Strategies

**Basic Similarity:**
```python
def retrieve(query: str, k: int = 5):
    query_embedding = get_embedding(query)
    return vector_db.search(query_embedding, top_k=k)
```

**Hybrid Search (BM25 + Vector):**
```python
def hybrid_retrieve(query: str, alpha: float = 0.7):
    vector_results = vector_db.search(get_embedding(query), top_k=10)
    keyword_results = keyword_search(query, top_k=10)
    return reciprocal_rank_fusion(vector_results, keyword_results, weights=[alpha, 1-alpha])
```

**Multi-Query:**
```python
def multi_query_retrieve(original_query: str):
    variations = llm.generate(f"Generate 3 variations of: {original_query}")
    all_results = []
    for query in [original_query] + variations:
        all_results.extend(retrieve(query))
    return deduplicate_and_rerank(all_results)[:5]
```

### 6. Reranking

**Cross-Encoder:**
```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, candidates: list[str]):
    pairs = [(query, doc) for doc in candidates]
    scores = reranker.predict(pairs)
    return sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
```

### 7. Context Assembly

```python
MAX_CONTEXT_TOKENS = 4000

def build_context(query: str, retrieved_docs: list[str]):
    context_parts = []
    total_tokens = count_tokens(query) + 500

    for doc in retrieved_docs:
        doc_tokens = count_tokens(doc)
        if total_tokens + doc_tokens < MAX_CONTEXT_TOKENS:
            context_parts.append(doc)
            total_tokens += doc_tokens
        else:
            break

    return "\n\n".join(context_parts)
```

### 8. Response Generation

**Basic RAG:**
```python
RAG_PROMPT = """Use the context to answer the question.
If unsure, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""

def generate_response(query: str, context: str, llm):
    prompt = RAG_PROMPT.format(context=context, question=query)
    return llm.generate(prompt)
```

**With Citations:**
```python
def generate_with_citations(query: str, docs: list[dict], llm):
    formatted = "\n\n".join([
        f"[{i+1}] {d['content']} (Source: {d['metadata']['source']})"
        for i, d in enumerate(docs)
    ])

    response = llm.generate(f"Answer with citations:\n{formatted}\n\nQuestion: {query}")
    return {"answer": response, "sources": [d['metadata'] for d in docs]}
```

### 9. Evaluation

**Retrieval Metrics:**
```python
def evaluate_retrieval(queries, expected, retrieved):
    metrics = {"precision@5": [], "recall@5": [], "mrr": []}

    for exp, ret in zip(expected, retrieved):
        relevant = len(set(ret[:5]) & set(exp))
        metrics["precision@5"].append(relevant / 5)
        metrics["recall@5"].append(relevant / len(exp) if exp else 0)

        for rank, doc in enumerate(ret[:5], 1):
            if doc in exp:
                metrics["mrr"].append(1 / rank)
                break
        else:
            metrics["mrr"].append(0)

    return {k: sum(v) / len(v) for k, v in metrics.items()}
```

**Faithfulness Check:**
```python
def check_faithfulness(answer: str, context: str):
    verification = llm.generate(f"""
    Context: {context}
    Claim: {answer}
    Is this supported by the context? (Yes/No)
    """)
    return verification.strip().lower() == "yes"
```

### 10. Production Patterns

**Caching:**
```python
from functools import lru_cache

class RAGCache:
    def __init__(self):
        self.cache = {}

    def get(self, query: str):
        return self.cache.get(hash(query))

    def set(self, query: str, result: dict):
        self.cache[hash(query)] = result
```

**Async Pipeline:**
```python
import asyncio

async def async_rag(query: str):
    query_embedding, rewritten = await asyncio.gather(
        async_get_embedding(query),
        async_rewrite_query(query)
    )

    results = await asyncio.gather(
        async_vector_search(query_embedding),
        async_vector_search(await async_get_embedding(rewritten))
    )

    combined = merge_results(results)
    context = await async_build_context(combined)
    return await async_generate(query, context)
```

## Quick Commands

```bash
# Install
pip install langchain openai pinecone-client chromadb sentence-transformers

# Test embedding
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
emb = model.encode("test")

# Similarity
cosine_sim = dot(a, b) / (norm(a) * norm(b))
```

## Best Practices Checklist

- [ ] Chunk size 300-1000 tokens with 10-20% overlap
- [ ] Use appropriate embedding model for domain
- [ ] Implement hybrid search (BM25 + vector)
- [ ] Rerank retrieved results
- [ ] Filter by relevance threshold
- [ ] Handle context window limits
- [ ] Cite sources in responses
- [ ] Check answer faithfulness
- [ ] Monitor retrieval quality metrics
- [ ] Cache frequent queries
- [ ] Implement query rewriting
- [ ] Version your embeddings
- [ ] Handle empty retrieval gracefully
- [ ] Log interactions for improvement
