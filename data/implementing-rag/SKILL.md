---
name: implementing-rag
description: Set up RAG pipelines with document chunking, embedding generation, and retrieval strategies using LlamaIndex. Use when building new RAG systems, choosing chunking approaches, selecting embedding models, or implementing vector/hybrid retrieval for src/ or src-iLand/ pipelines.
---

# Implementing RAG Systems

Quick-start guide for building production-grade RAG pipelines with LlamaIndex. This skill helps you set up the foundational components: document processing, embedding generation, and retrieval.

## When to Use This Skill

- Building a new RAG pipeline from scratch
- Choosing optimal chunking strategy for your documents
- Selecting and configuring embedding models
- Implementing retrieval (vector, BM25, or hybrid search)
- Optimizing for specific use cases (Thai language, legal documents, product catalogs)
- Integrating with existing pipelines in `src/` or `src-iLand/`

## Quick Decision Guide

### Chunking Strategy
- **Legal/Technical docs** (like Thai land deeds) → 512-1024 tokens
- **Narrative content** → 1024-2048 tokens
- **Q&A pairs** → 256-512 tokens
- **Rule of thumb**: When halving chunk size, double `similarity_top_k`

### Embedding Model Selection
- **Cost-sensitive** → HuggingFace bge-base-en-v1.5 with ONNX (3-7x faster, free)
- **Quality-first** → OpenAI text-embedding-3-small or JinaAI-base
- **Multi-language (Thai)** → Cohere embed-multilingual-v3.0
- **Balanced** → OpenAI or bge-large (open-source)

### Retrieval Strategy
- **Simple queries** → Vector search
- **Keyword-heavy** → BM25
- **Production systems** → Hybrid (vector + BM25)
- **Structured data** → Metadata filtering
- **Large doc sets (100+)** → Document summary or recursive retrieval

## Quick Start Patterns

### Pattern 1: Standard RAG Setup (Vector Search)

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure chunking
Settings.chunk_size = 1024
Settings.chunk_overlap = 20

# Configure embeddings
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    embed_batch_size=100
)

# Load and index documents
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# Create query engine
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("Your question here")
```

### Pattern 2: Multi-Language Setup (Thai Support)

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core.node_parser import SentenceSplitter

# Use multilingual embeddings
embed_model = CohereEmbedding(
    model_name="embed-multilingual-v3.0",
    api_key="YOUR_COHERE_API_KEY"
)

# Configure chunking for Thai text
node_parser = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=50
)

# Load Thai documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index with multilingual support
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=embed_model,
    transformations=[node_parser]
)

query_engine = index.as_query_engine(similarity_top_k=5)
```

### Pattern 3: Hybrid Search (Production-Ready)

```python
from llama_index.core import VectorStoreIndex
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever
import Stemmer

# Create vector index
index = VectorStoreIndex.from_documents(documents)
vector_retriever = index.as_retriever(similarity_top_k=10)

# Create BM25 retriever
bm25_retriever = BM25Retriever.from_defaults(
    docstore=index.docstore,
    similarity_top_k=10,
    stemmer=Stemmer.Stemmer("english")
)

# Combine with query fusion
hybrid_retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    similarity_top_k=5,
    mode="reciprocal_rerank",
    use_async=True
)

# Use in query engine
from llama_index.core.query_engine import RetrieverQueryEngine
query_engine = RetrieverQueryEngine.from_args(hybrid_retriever)
```

### Pattern 4: Cost-Optimized Local Embeddings

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

# Use local model with ONNX acceleration (3-7x faster)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-base-en-v1.5",
    backend="onnx"  # Requires: pip install optimum[onnxruntime]
)

# Rest of the pipeline remains the same
index = VectorStoreIndex.from_documents(documents)
```

## Your Codebase Integration

### For `src/` Pipeline

**Document Preprocessing** (`src/02_prep_doc_for_embedding.py`):
- Add configurable chunking strategy
- Support multiple node parser types

**Batch Embeddings** (`src/09_enhanced_batch_embeddings.py`):
- Increase `embed_batch_size` to 100 for faster processing
- Consider local models to eliminate API costs

**Basic Retrieval** (`src/10_basic_query_engine.py`):
- Baseline vector search implementation
- Adjust `similarity_top_k` based on chunk size

### For `src-iLand/` Pipeline (Thai Land Deeds)

**Data Processing** (`src-iLand/data_processing/`):
- Current chunk size: 1024 tokens (good for legal documents)
- Consider testing 512 with increased `top_k` for better precision

**Embeddings** (`src-iLand/docs_embedding/`):
- Current: OpenAI text-embedding-3-small
- Test: Cohere embed-multilingual-v3.0 for better Thai understanding

**Retrieval** (`src-iLand/retrieval/retrievers/`):
- Vector strategy: Baseline semantic search
- Hybrid strategy: Combines vector + BM25 for Thai queries
- Metadata strategy: Fast filtering (<50ms) on Thai geographic/legal metadata

## Detailed References

Load these reference files when you need comprehensive details:

- **reference-chunking.md**: Complete chunking strategies guide
  - Node parser types and configurations
  - Chunk size optimization for different domains
  - Sentence-window and hierarchical patterns
  - Metadata preservation

- **reference-embeddings.md**: Embedding model selection and optimization
  - All supported models (OpenAI, Cohere, HuggingFace, JinaAI, Voyage)
  - Performance benchmarks (hit rate, MRR)
  - ONNX/OpenVINO optimization details
  - Multi-language support
  - Cost optimization strategies

- **reference-retrieval-basics.md**: Core retrieval patterns
  - Vector retrieval implementation
  - BM25 keyword search
  - Hybrid search (vector + BM25)
  - Metadata filtering
  - Configuration parameters and tuning

## Common Workflows

### Workflow 1: New RAG Pipeline Setup

- [ ] **Step 1**: Choose chunking strategy based on document type
  - Load `reference-chunking.md` for detailed guidance
  - Test with sample documents

- [ ] **Step 2**: Select embedding model
  - Load `reference-embeddings.md` for model comparison
  - Consider: cost, latency, language support
  - For Thai: use multilingual models

- [ ] **Step 3**: Implement basic vector retrieval
  - Start with simple VectorStoreIndex
  - Test with sample queries
  - Measure baseline performance

- [ ] **Step 4**: Optimize chunk size and top_k
  - Adjust based on query results
  - Balance precision vs recall

- [ ] **Step 5**: (Optional) Upgrade to hybrid search
  - Combine vector + BM25 for production quality

### Workflow 2: Migrating from API to Local Embeddings

- [ ] **Step 1**: Choose local model (see `reference-embeddings.md`)
  - Recommended: BAAI/bge-base-en-v1.5

- [ ] **Step 2**: Install optimization backend
  ```bash
  pip install optimum[onnxruntime]
  ```

- [ ] **Step 3**: Update embedding configuration
  ```python
  Settings.embed_model = HuggingFaceEmbedding(
      model_name="BAAI/bge-base-en-v1.5",
      backend="onnx"
  )
  ```

- [ ] **Step 4**: Re-index all documents
  - **CRITICAL**: Must re-embed with new model
  - Use caching to avoid redundant work

- [ ] **Step 5**: Validate retrieval quality
  - Compare results with API embeddings
  - Measure latency improvement (3-7x faster expected)

### Workflow 3: Thai Language RAG Setup

- [ ] **Step 1**: Use multilingual embedding model
  ```python
  embed_model = CohereEmbedding(
      model_name="embed-multilingual-v3.0"
  )
  ```

- [ ] **Step 2**: Configure appropriate chunking
  - Test 512-1024 tokens for Thai text
  - Preserve Thai metadata

- [ ] **Step 3**: Implement hybrid search
  - Vector for semantic understanding
  - BM25 for exact Thai keyword matching

- [ ] **Step 4**: Add metadata filtering
  - จังหวัด (province), อำเภอ (district), ประเภท (type)
  - Enable fast filtering (<50ms)

- [ ] **Step 5**: Test with Thai queries
  - Validate Unicode handling
  - Check retrieval relevance

## Key Reminders

**Critical Requirements**:
- **Re-indexing**: When changing embedding models, MUST re-index all data
- **Model consistency**: Identical models for indexing and querying
- **Chunk size + top_k**: Halving chunk size → double `similarity_top_k`

**Best Practices**:
- Start simple (vector search) → Add complexity as needed (hybrid, metadata)
- Test with representative queries before full indexing
- Use local models for cost optimization at scale
- Enable parallel loading (`num_workers=10`) for 13x speedup

**Performance Tips**:
- Batch size: Set `embed_batch_size=100` for API calls
- Parallel loading: Use `SimpleDirectoryReader(...).load_data(num_workers=10)`
- Caching: Enable ingestion pipeline caching for faster re-runs

## Next Steps

After implementing basic RAG:
- **Optimize**: Use `optimizing-rag` skill for reranking, caching, production deployment
- **Evaluate**: Use `evaluating-rag` skill to measure hit rate, MRR, and compare strategies
