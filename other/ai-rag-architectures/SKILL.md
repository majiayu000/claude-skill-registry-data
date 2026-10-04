---
name: ai-rag-architectures
description: Patterns for RAG pipelines, vector databases, embedding strategies, context-window management, and LLM orchestration. Use when building retrieval-augmented generation systems, semantic search, or AI-powered knowledge bases.
version: "1.0.0"
verified_date: 2026-04-30
category: ai
---

# AI RAG Architectures

## Purpose
Provide specialized architectural patterns for building Retrieval-Augmented Generation (RAG) systems. This skill codifies the engineering decisions around vector stores, embedding pipelines, chunking strategies, and context assembly that the `ai-engineer` agent needs but currently lacks as formalized guidance.

## When to Use This Skill
Use when:
- Building a RAG pipeline (document ingestion → embedding → retrieval → generation)
- Integrating vector databases (Pinecone, Weaviate, Qdrant, pgvector, ChromaDB)
- Designing chunking and embedding strategies for documents
- Optimizing context window usage for LLM calls
- Building semantic search or AI-powered knowledge bases
- Evaluating retrieval quality (precision, recall, relevance)

Do NOT use when:
- Building simple LLM chat completions without retrieval (use `ai-engineer` agent directly)
- Working on frontend or UI components
- The task has no AI/ML component

## Phase 1: RAG Pipeline Architecture

### Standard Pipeline
```
Documents → Chunking → Embedding → Vector Store → Retrieval → Context Assembly → LLM → Response
```

### Component Selection

| Component | Options | Default Recommendation |
|-----------|---------|----------------------|
| Embedding | OpenAI `text-embedding-3-small`, Cohere `embed-v3` | OpenAI for simplicity |
| Vector DB | Pinecone, Qdrant, pgvector, ChromaDB | pgvector for Postgres stacks |
| LLM | GPT-4o, Claude 3.5, Gemini 2.0 | Project-dependent |
| Chunking | Fixed-size, semantic, recursive | Recursive text splitter |

## Phase 2: Document Chunking

### Chunking Strategies
1. **Fixed-size** (simple): Split by character/token count with overlap
2. **Recursive** (recommended): Split by structure (paragraphs → sentences → words)
3. **Semantic** (advanced): Split by topic/meaning boundaries using embeddings

### Chunking Rules
- **Chunk size**: 500-1000 tokens for most use cases
- **Overlap**: 10-20% overlap between chunks to preserve context
- **Metadata**: Always attach source document ID, page number, and section title
- **Never split mid-sentence** — use sentence boundaries as minimum split points

## Phase 3: Embedding & Storage

### Embedding Rules
1. Use the **same embedding model** for indexing and querying — mismatched models produce garbage
2. **Normalize embeddings** if using cosine similarity
3. **Batch embedding calls** — never embed one document at a time
4. **Cache embeddings** — re-embedding unchanged documents wastes money

### Vector Store Schema
```sql
-- pgvector example
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  embedding vector(1536),  -- match your model's dimension
  metadata JSONB DEFAULT '{}',
  source_id TEXT NOT NULL,
  chunk_index INTEGER NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

## Phase 4: Retrieval & Context Assembly

### Retrieval Strategy
1. **Semantic search** (default): Query embedding → cosine similarity → top-K
2. **Hybrid search**: Combine semantic search with keyword (BM25) search
3. **Re-ranking**: Use a cross-encoder model to re-rank top-K results

### Context Assembly Rules
1. **Token budget**: Reserve 30-40% of context window for the system prompt + user query + response
2. **Order matters**: Place most relevant chunks first (recency bias in LLMs)
3. **Deduplication**: Remove near-duplicate chunks before assembly
4. **Source attribution**: Always include chunk metadata for citation

### Context Window Management
```
Model context window:  128K tokens (example)
├── System prompt:      ~2K tokens
├── Retrieved context:  ~50K tokens (max)
├── User query:         ~1K tokens
├── Response budget:    ~4K tokens
└── Safety margin:      ~10% buffer
```

## Phase 5: Evaluation

### Retrieval Metrics
- **Precision@K**: What fraction of retrieved chunks are relevant?
- **Recall@K**: What fraction of relevant chunks were retrieved?
- **MRR**: Mean Reciprocal Rank of the first relevant result

### Generation Metrics
- **Faithfulness**: Does the response only use information from retrieved context?
- **Relevance**: Does the response answer the actual question?
- **Groundedness**: Can every claim be traced to a source chunk?

### Evaluation Rules
1. Build a **golden test set** of 50+ question-answer pairs with expected source documents
2. Measure retrieval quality **separately** from generation quality
3. Track metrics over time — RAG quality degrades as the document corpus grows
4. **Hallucination detection**: Flag responses that contain claims not present in any retrieved chunk

## Behavior Rules
1. **Embedding model is a locked decision.** Changing it requires re-indexing the entire corpus.
2. **Chunk size is tunable.** Start with 500 tokens and adjust based on retrieval precision.
3. **Never skip evaluation.** A RAG system without metrics is a hallucination machine.
4. **Cost awareness.** Embedding and LLM calls cost money — log token usage per query.

## Safety Guardrails
1. **Data Privacy Patch**: Never embed or store PII in vector databases without explicit user consent and encryption at rest.
2. **Prompt Injection Patch**: Retrieved chunks are untrusted input — always sandbox them within the prompt template with clear delimiters.
3. **Cost Runaway Patch**: Set hard limits on document corpus size and per-query token budgets. Alert when approaching limits.
4. **Self-Rejection Clause**: If the embedding model dimension or vector DB type cannot be determined, **ABORT OUTPUT** and emit: *"REJECTED: Cannot design RAG pipeline without knowing the embedding model and vector store."*

## Output Format / Delivery
- Output should be a structured architectural spec or pipeline components.

## Maintenance Notes
- Created 2026-04-30 as part of the Strategic Gap analysis.
- Complements the `ai-engineer` agent (which orchestrates AI features) with specialized RAG architecture patterns.
- Does NOT overlap with `backend-dev-guidelines` — this skill is exclusively for AI retrieval systems.
