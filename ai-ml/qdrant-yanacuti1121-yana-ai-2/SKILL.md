---
name: qdrant
description: Qdrant vector database — collections, upsert, search, filtering, payloads, sparse vectors, BM25
triggers:
  - qdrant
  - vector database qdrant
  - qdrant collection
  - qdrant search
  - qdrant upsert
  - sparse dense hybrid search
  - qdrant filter
  - qdrant payload
  - qdrant python client
  - vector store qdrant
do_not_use_for:
  - relational queries — use PostgreSQL/SQLite
  - full-text only — use Elasticsearch
  - generic key-value store — use Redis
see_also:
  - ragas
  - langfuse
  - crawl4ai
  - firecrawl
---

# Qdrant — Vector Database

## Connect + Create Collection

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue, Range,
    SparseVectorParams, SparseIndexParams,
)

# Local (in-memory for dev)
client = QdrantClient(":memory:")

# Local persistent
client = QdrantClient(path="./qdrant_storage")

# Remote
client = QdrantClient(
    url="http://localhost:6333",
    api_key="your-api-key",          # for Qdrant Cloud
    timeout=30,
)

# Create collection
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=1536,                    # OpenAI ada-002 dim
        distance=Distance.COSINE,     # COSINE | EUCLID | DOT
    ),
)

# With multiple named vectors
from qdrant_client.models import NamedVectorStruct
client.create_collection(
    collection_name="multi_vec",
    vectors_config={
        "dense": VectorParams(size=1536, distance=Distance.COSINE),
        "sparse": SparseVectorParams(index=SparseIndexParams(on_disk=False)),
    },
)
```

## Upsert Points

```python
from qdrant_client.models import PointStruct

# Single or batch upsert
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,                           # int or UUID string
            vector=[0.1, 0.2, ...],         # 1536-dim float list
            payload={
                "text": "Document content",
                "source": "wiki",
                "year": 2024,
                "tags": ["ml", "nlp"],
            },
        ),
        PointStruct(id=2, vector=embed("Second doc"), payload={"text": "..."}),
    ],
    wait=True,                              # wait for indexing
)

# Batch upsert from embeddings
texts = ["doc1", "doc2", "doc3"]
embeddings = embed_batch(texts)            # returns List[List[float]]
points = [
    PointStruct(id=i, vector=vec, payload={"text": t})
    for i, (t, vec) in enumerate(zip(texts, embeddings))
]
client.upsert(collection_name="documents", points=points)
```

## Search

```python
# Basic similarity search
results = client.search(
    collection_name="documents",
    query_vector=embed("machine learning"),
    limit=5,
    with_payload=True,
    score_threshold=0.7,                    # minimum score
)
for r in results:
    print(r.score, r.payload["text"])

# Filtered search
results = client.search(
    collection_name="documents",
    query_vector=embed("neural networks"),
    query_filter=Filter(
        must=[
            FieldCondition(key="source", match=MatchValue(value="wiki")),
            FieldCondition(key="year", range=Range(gte=2022, lte=2024)),
        ],
        should=[
            FieldCondition(key="tags", match=MatchValue(value="ml")),
        ],
    ),
    limit=10,
    with_payload=["text", "source"],        # select payload fields
)
```

## Hybrid Search (Dense + Sparse / BM25)

```python
from qdrant_client.models import SparseVector, NamedVector, NamedSparseVector

# Sparse vector (BM25-style from fastembed)
from fastembed import SparseTextEmbedding
sparse_model = SparseTextEmbedding("prithivida/Splade_PP_en_v1")

def get_sparse(text: str) -> SparseVector:
    emb = list(sparse_model.embed([text]))[0]
    return SparseVector(indices=emb.indices.tolist(), values=emb.values.tolist())

# Hybrid search with RRF fusion
from qdrant_client.models import Prefetch, FusionQuery, Fusion

results = client.query_points(
    collection_name="multi_vec",
    prefetch=[
        Prefetch(query=embed_dense(query), using="dense", limit=20),
        Prefetch(query=get_sparse(query), using="sparse", limit=20),
    ],
    query=FusionQuery(fusion=Fusion.RRF),   # Reciprocal Rank Fusion
    limit=5,
    with_payload=True,
)
```

## Payload Indexing

```python
from qdrant_client.models import PayloadSchemaType

# Create index for faster filtered search
client.create_payload_index(
    collection_name="documents",
    field_name="source",
    field_schema=PayloadSchemaType.KEYWORD,
)
client.create_payload_index(
    collection_name="documents",
    field_name="year",
    field_schema=PayloadSchemaType.INTEGER,
)
```

## Manage Points

```python
# Get by ID
points = client.retrieve(
    collection_name="documents",
    ids=[1, 2, 3],
    with_payload=True,
    with_vectors=False,
)

# Delete
client.delete(
    collection_name="documents",
    points_selector=Filter(
        must=[FieldCondition(key="source", match=MatchValue(value="old"))]
    ),
)

# Update payload
client.set_payload(
    collection_name="documents",
    payload={"updated": True},
    points=[1, 2],
)

# Scroll (iterate all points)
offset = None
while True:
    result, offset = client.scroll(
        collection_name="documents",
        limit=100,
        offset=offset,
        with_payload=True,
    )
    if not result:
        break
    process_batch(result)
```

## Collections Management

```python
# List collections
colls = client.get_collections()
names = [c.name for c in colls.collections]

# Collection info
info = client.get_collection("documents")
print(info.points_count, info.vectors_count)

# Delete collection
client.delete_collection("documents")

# Recreate (idempotent)
client.recreate_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)
```

## Anti-Fake-Pass Checks

- Vector dimension must match `VectorParams(size=...)` exactly — mismatches raise `Unprocessable`
- `id` must be `int` or UUID string — nested objects raise validation error
- `score_threshold` filters out points — if no results, lower threshold or check embeddings
- `wait=True` on upsert ensures indexing before search — omit only for fire-and-forget ingestion
- Sparse vectors need `SparseVectorParams` in collection config — can't add after creation without recreation
- `query_points` (v1.7+) replaces legacy `search` API — check client version
