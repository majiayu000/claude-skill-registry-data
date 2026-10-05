---
name: rag
description: RAG pipelines including document chunking, embedding, vector search, retrieval strategies, and reranking
layer: domain
category: ai-ml
triggers:
  - "RAG"
  - "retrieval augmented generation"
  - "vector search"
  - "embeddings"
  - "chunking"
  - "knowledge base"
  - "semantic search"
  - "reranking"
inputs:
  - documents: Source documents to index (PDFs, web pages, databases, etc.)
  - query_patterns: How users will search (natural language, keyword, hybrid)
  - requirements: Accuracy, latency, freshness, cost constraints
  - infrastructure: Vector database choice, embedding model preference
outputs:
  - pipeline_design: End-to-end RAG pipeline architecture
  - chunking_strategy: Document splitting approach with overlap
  - embedding_config: Model selection and dimension settings
  - retrieval_strategy: Search, filter, and reranking configuration
  - evaluation_plan: Metrics and test cases for RAG quality
linksTo:
  - ai-agents
  - prompt-engineering
  - postgresql
  - redis
linkedFrom:
  - ai-agents
  - cook
  - research
preferredNextSkills:
  - ai-agents
  - prompt-engineering
fallbackSkills:
  - research
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects:
  - May create vector store indexes
  - May process and embed documents
  - Consumes embedding API tokens
---

# RAG (Retrieval-Augmented Generation) Skill

## Purpose

Design and implement RAG pipelines that ground LLM responses in relevant, up-to-date knowledge. This skill covers the full pipeline: document ingestion, chunking strategies, embedding model selection, vector storage, retrieval with filtering, reranking for precision, and prompt construction with retrieved context. RAG reduces hallucination by giving the model factual context to work with.

## Key Concepts

### RAG Pipeline Overview

```
INGESTION (offline):
  Documents -> Chunking -> Embedding -> Vector Store

RETRIEVAL (at query time):
  Query -> Embed Query -> Vector Search -> Rerank -> Top-K Context

GENERATION (at query time):
  System Prompt + Retrieved Context + User Query -> LLM -> Response

EVALUATION:
  Context Relevance | Answer Faithfulness | Answer Relevance
```

### Chunking Strategies

```
FIXED SIZE:
  Split at N characters/tokens with M overlap
  Simple but may break mid-sentence
  Good for: Uniform, well-structured documents

RECURSIVE CHARACTER:
  Split on paragraphs, then sentences, then words
  Respects document structure
  Good for: General purpose, articles, documentation

SEMANTIC:
  Split when embedding similarity between sentences drops
  Each chunk is semantically coherent
  Good for: Long documents with topic changes

DOCUMENT-AWARE:
  Split on markdown headers, HTML tags, code blocks
  Preserves structural meaning
  Good for: Technical documentation, code, structured content

RULES OF THUMB:
  Chunk size: 500-1000 tokens (sweet spot for most models)
  Overlap: 50-200 tokens (prevents losing context at boundaries)
  Smaller chunks = more precise retrieval, less context per chunk
  Larger chunks = more context per chunk, less precise retrieval
```

### Embedding Model Selection

```
MODEL                    DIMENSIONS  SPEED    QUALITY  COST
text-embedding-3-small   1536        Fast     Good     Low
text-embedding-3-large   3072        Medium   Best     Medium
voyage-3                 1024        Fast     Great    Medium
cohere-embed-v3          1024        Fast     Great    Medium
BGE-large (open source)  1024        Self-host Good    Free (compute)

GUIDELINES:
  - Start with text-embedding-3-small for prototyping
  - Upgrade to text-embedding-3-large or voyage-3 for production
  - Use the SAME model for document and query embeddings
  - Matryoshka embeddings: can truncate dimensions for speed
```

## Patterns

### Document Ingestion Pipeline

```typescript
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { OpenAIEmbeddings } from '@langchain/openai';

// 1. Load and split documents
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 800,
  chunkOverlap: 200,
  separators: ['\n## ', '\n### ', '\n\n', '\n', '. ', ' '],
});

const chunks = await splitter.splitDocuments(documents);

// 2. Embed chunks
const embeddings = new OpenAIEmbeddings({
  model: 'text-embedding-3-small',
  dimensions: 1536,
});

const vectors = await embeddings.embedDocuments(
  chunks.map((chunk) => chunk.pageContent)
);

// 3. Store in vector database
for (let i = 0; i < chunks.length; i++) {
  await vectorStore.upsert({
    id: `doc_${chunks[i].metadata.source}_chunk_${i}`,
    values: vectors[i],
    metadata: {
      text: chunks[i].pageContent,
      source: chunks[i].metadata.source,
      section: chunks[i].metadata.section,
      chunkIndex: i,
    },
  });
}
```

### Retrieval with Hybrid Search

```typescript
async function retrieve(query: string, options: {
  topK?: number;
  filter?: Record<string, unknown>;
  minScore?: number;
} = {}): Promise<RetrievedChunk[]> {
  const { topK = 10, filter, minScore = 0.7 } = options;

  // 1. Embed the query
  const queryVector = await embeddings.embedQuery(query);

  // 2. Vector search
  const vectorResults = await vectorStore.query({
    vector: queryVector,
    topK: topK * 2,  // Fetch more for reranking
    filter,
    includeMetadata: true,
  });

  // 3. Filter by minimum score
  const filtered = vectorResults.matches.filter(
    (match) => match.score >= minScore
  );

  // 4. Rerank for precision
  const reranked = await reranker.rerank(query, filtered.map(m => m.metadata.text));

  // 5. Return top-K after reranking
  return reranked.slice(0, topK).map((result) => ({
    text: result.text,
    score: result.relevanceScore,
    source: result.metadata.source,
  }));
}
```

### RAG Prompt Construction

```typescript
async function generateWithRAG(userQuery: string): Promise<string> {
  // 1. Retrieve relevant context
  const chunks = await retrieve(userQuery, { topK: 5 });

  // 2. Build context block
  const context = chunks
    .map((chunk, i) => `[Source ${i + 1}: ${chunk.source}]\n${chunk.text}`)
    .join('\n\n---\n\n');

  // 3. Generate response with context
  const response = await llm.create({
    model: 'claude-sonnet-4-20250514',
    system: `You are a helpful assistant. Answer the user's question based on the provided context.

Rules:
- Base your answer ONLY on the provided context
- If the context does not contain enough information, say so
- Cite sources using [Source N] notation
- Do not make up information not present in the context`,
    messages: [
      {
        role: 'user',
        content: `Context:\n${context}\n\n---\n\nQuestion: ${userQuery}`,
      },
    ],
  });

  return response;
}
```

### PostgreSQL pgvector (Self-Hosted Vector Search)

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table
CREATE TABLE document_chunks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  embedding vector(1536),
  metadata JSONB DEFAULT '{}',
  source TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON document_chunks
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- Similarity search query
SELECT id, content, source, metadata,
       1 - (embedding <=> $1::vector) AS similarity
FROM document_chunks
WHERE metadata->>'category' = $2  -- optional filter
ORDER BY embedding <=> $1::vector
LIMIT 10;
```

## Evaluation

### RAG Quality Metrics

```
CONTEXT RELEVANCE:
  Are the retrieved chunks relevant to the query?
  Measure: LLM-as-judge or human annotation

ANSWER FAITHFULNESS:
  Is the answer grounded in the retrieved context (no hallucination)?
  Measure: Check if every claim maps to a context chunk

ANSWER RELEVANCE:
  Does the answer actually address the user's question?
  Measure: LLM-as-judge on query-answer alignment

CONTEXT PRECISION:
  Are the top-ranked chunks the most relevant?
  Measure: Precision@K with ground truth labels

CONTEXT RECALL:
  Did retrieval find all relevant chunks?
  Measure: Recall against known relevant documents
```

## Best Practices

1. **Chunk size matters** -- 500-1000 tokens is the sweet spot; too small loses context, too large dilutes relevance
2. **Always use overlap** -- 10-20% overlap prevents losing information at chunk boundaries
3. **Preserve metadata** -- source, section headers, and document type enable filtering
4. **Rerank after vector search** -- vector similarity is approximate; reranking improves precision
5. **Use hybrid search** -- combine vector similarity with keyword matching for best results
6. **Test with real queries** -- build a test set of questions with known answers
7. **Monitor retrieval quality** -- log what gets retrieved; poor retrieval causes poor generation
8. **Keep embeddings fresh** -- re-embed when source documents change
9. **Use the same embedding model** -- query and document embeddings must use the same model
10. **Cite sources** -- always attribute retrieved information to its source

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Chunks too large | Retrieval returns irrelevant content | Reduce chunk size to 500-800 tokens |
| No overlap between chunks | Context lost at boundaries | Add 100-200 token overlap |
| Different embed models for docs vs queries | Terrible retrieval quality | Use the SAME model for both |
| No metadata filtering | Irrelevant results from wrong documents | Store and filter on source, category, date |
| Trusting vector search alone | Low precision for some queries | Add reranking step |
| No evaluation | No idea if RAG is working well | Build a test set, measure faithfulness |
| Stale embeddings | Answers based on outdated information | Re-embed on document updates |
