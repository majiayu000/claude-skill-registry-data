---
name: qdrant
description: "Manage Qdrant vector databases; optimize HNSW indexing, payload filtering, hybrid dense-sparse search, and high-dimensional collection schemas."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-09-13"
tags: ["qdrant", "vector-database", "hnsw", "embeddings", "semantic-search", "rag", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Qdrant Vector Database & Similarity Search AI Skill Guide

## Overview & Engine Architecture

Qdrant is an open-source, high-performance vector search engine and database implemented in Rust. It specializes in approximate nearest neighbor (ANN) search over high-dimensional vectors, paired with rich metadata payload storage. Qdrant combines custom **Hierarchical Navigable Small World (HNSW)** graph indexing with **scalar and product quantization (SQ/PQ)** and hardware-accelerated vector distance SIMD instructions (AVX-512, NEON), enabling millisecond searches over millions of vectors while supporting filtered queries without precision loss.

Claude operates as a Principal AI Data Architect and RAG Specialist, specializing in **collection schema design**, **HNSW graph hyperparameter tuning (`m`, `ef_construct`, `ef_search`)**, **quantization memory optimization**, **payload filtering index configuration**, and **hybrid dense-sparse search pipelines**.

### Qdrant Collection & Segment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Qdrant Storage & Index Engine               │
│                                                             │
│  Client API Ingress (gRPC Port 6334 / REST Port 6333)       │
│  ├── Upsert Points | Query Points | Hybrid Score Reranking  │
│                                                             │
│  Collection ("knowledge_base_v1")                           │
│  ├── Shard & Segment Pool (Immutable & Appendable Segments) │
│  │   ├── Vector Storage: Raw FP32 / mmap On-Disk Storage    │
│  │   ├── Quantized Vectors: Scalar Quantization (1-byte)    │
│  │   ├── HNSW Graph Index: Fast ANN Multi-Layer Traversal   │
│  │   └── Payload Index: Inverted B-Tree / Geo / Keyword Map │
│  └── Segment Background Optimizer (Vacuums & Merges Segments│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Explicit Distance Metric Alignment**: Choose the distance metric that matches your embedding model: `Cosine` for standard normalized embeddings (e.g., OpenAI, Cohere), `Dot` for pre-normalized vectors to bypass square root overhead, or `Euclid` for spatial data.
2. **Mandatory Payload Indexing**: Whenever filtering points by metadata fields (e.g., `user_id`, `tenant_id`, `document_type`), always create explicit payload schema indexes (`create_payload_index`). Unindexed payload filtering degrades ANN search into slow full-collection table scans.
3. **Quantization for Large Datasets**: For collections exceeding 1,000,000 vectors, enable `scalar_quantization` (`INT8`) and set `always_ram: false` to reduce RAM requirements by up to 75% with less than 1% drop in recall.
4. **Resilient Batch Upserts**: Upsert points in batches (500–2,000 points) with retries, rather than individual one-by-one writes.

---

## Production Python Automation: Collection Setup & Filtered Hybrid Search

```python
"""Production Qdrant collection setup and filtered ANN similarity search."""
from qdrant_client import QdrantClient
from qdrant_client.http import models

def setup_production_collection(client: QdrantClient, collection_name: str = "rag_documents"):
    # 1. Create collection with HNSW tuning and Scalar Quantization
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE,
                on_disk=True, # Vectors stored on disk to conserve RAM
            ),
            hnsw_config=models.HnswConfigDiff(
                m=16,               # Max edges per node in HNSW
                ef_construct=128,   # Search depth during index building
                full_scan_threshold=10000,
            ),
            quantization_config=models.ScalarQuantization(
                scalar=models.ScalarQuantizationConfig(
                    type=models.ScalarType.INT8,
                    quantile=0.99,
                    always_ram=True, # Keep quantized vectors in RAM for fast search
                )
            ),
        )

        # 2. Create payload indexes for frequent filter attributes
        client.create_payload_index(
            collection_name=collection_name,
            field_name="tenant_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
        client.create_payload_index(
            collection_name=collection_name,
            field_name="published_timestamp",
            field_schema=models.PayloadSchemaType.INTEGER,
        )
        print(f"Collection {collection_name} created with indexes.")

def query_relevant_chunks(
    client: QdrantClient,
    query_vector: list[float],
    tenant_id: str,
    top_k: int = 5
) -> list[models.ScoredPoint]:
    """Execute filtered similarity search with custom search-depth."""
    search_result = client.search(
        collection_name="rag_documents",
        query_vector=query_vector,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="tenant_id",
                    match=models.MatchValue(value=tenant_id),
                )
            ]
        ),
        search_params=models.SearchParams(
            hnsw_ef=64, # High search accuracy
            exact=False,
        ),
        limit=top_k,
    )
    return search_result

if __name__ == "__main__":
    qdrant = QdrantClient(host="localhost", port=6333)
    setup_production_collection(qdrant)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Filtered vector query takes >500ms** | Query filters on unindexed metadata attributes, forcing Qdrant to perform full scans. | Create explicit payload schema index for the filter field using `create_payload_index`. |
| **Low search recall (<90%)** | `hnsw_ef` parameter during query is too low, or quantization quantile is mismatched. | 1. Increase `search_params.hnsw_ef` to 64 or 128.<br>2. Recalibrate scalar quantization `quantile` to 0.99.<br>3. Verify vectors are normalized if using `Distance.DOT`. |
| **High memory consumption crashing container** | Raw 32-bit floating point vectors loaded entirely into uncompressed RAM. | 1. Set `vectors_config.on_disk = True`.<br>2. Enable `scalar_quantization` with `always_ram = True` to only store 8-bit quantized representations in memory. |
| **Segment optimizer thrashing / CPU pinned at 100%** | Continual small single-point upserts keeping background index build loops perpetually active. | 1. Batch upserts into chunks of 500-2,000 points.<br>2. Temporarily pause optimizer during massive bulk ingestion by setting `indexing_threshold = 0`. |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Run production Qdrant container with persistent storage volume
docker run -d -p 6333:6333 -p 6334:6334 \
  -v /var/lib/qdrant/storage:/qdrant/storage:z \
  --name qdrant qdrant/qdrant:latest

# 2. Check cluster health and collection statistics
curl http://localhost:6333/collections/rag_documents

# 3. Trigger immediate on-demand collection snapshot backup
curl -X POST http://localhost:6333/collections/rag_documents/snapshots

# 4. Download created snapshot file for disaster recovery
curl -O http://localhost:6333/collections/rag_documents/snapshots/<snapshot-name>
```

---

## Agent Operational Directive

> **MANDATORY**: Never initiate bulk vector insertion without verifying that payload indexes for your primary tenant, user, or category filtering fields are created first.
