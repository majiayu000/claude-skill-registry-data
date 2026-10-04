---
name: dspy-qdrant
description: Use Qdrant as a vector database with DSPy, or connect any vector DB (Pinecone, ChromaDB, Weaviate) with custom retrievers. Use when you want to set up Qdrant, QdrantRM, dspy-qdrant, vector database for DSPy, vector search, hybrid search, or build custom retrievers for Pinecone, ChromaDB, or Weaviate. Also used for qdrant, dspy-qdrant, QdrantRM, vector database, vector search, pinecone DSPy, chromadb DSPy, weaviate DSPy, vector DB for DSPy, pip install dspy-qdrant, qdrant docker, qdrant cloud, hybrid search DSPy, sparse dense vectors, custom dspy.Retrieve, which vector DB for DSPy, DSPy 3.0 retriever removed.
---

# Qdrant — Vector Database Integration for DSPy

Guide the user through setting up Qdrant with DSPy using the official `dspy-qdrant` package, plus custom retriever patterns for Pinecone, ChromaDB, and Weaviate.

## Step 1 — Gather context

Ask before generating setup code:

1. **Vector DB** — Qdrant, Pinecone, ChromaDB, Weaviate, or something else?
2. **Qdrant deployment** (if Qdrant) — Docker locally, Qdrant Cloud, or in-memory for testing?
3. **Index state** — indexing documents from scratch, or connecting to an existing collection?
4. **Search mode** — standard dense search, or hybrid (keyword + semantic combined)?

Then jump to the relevant section.

## What is Qdrant

[Qdrant](https://qdrant.tech/) is an open-source vector search engine written in Rust. It's the **only vector database with an official DSPy integration package** (`dspy-qdrant`). Features: hybrid search (dense + sparse), payload filtering, multi-tenancy, and horizontal scaling.

## Why Qdrant for DSPy

DSPy 3.0 removed all community-contributed retriever modules (`ChromadbRM`, `PineconeRM`, `WeaviateRM`, `QdrantRM` from the main repo). The `dspy-qdrant` package is the official replacement — maintained separately with full DSPy compatibility.

For other vector databases, you write a short custom `dspy.Retrieve` subclass (~15 lines). This skill covers that pattern too.

## Setup

### Install

```bash
pip install dspy-qdrant
```

This installs both the Qdrant client and the DSPy retriever module.

### Start Qdrant

#### Option 1: Docker (local development)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

#### Option 2: Qdrant Cloud (managed, free tier available)

1. Sign up at [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a cluster (free tier: 1GB, 1 node)
3. Copy your URL and API key

```bash
export QDRANT_URL="https://your-cluster.aws.cloud.qdrant.io"
export QDRANT_API_KEY="your-api-key"
```

#### Option 3: pip install (in-memory, for testing)

```python
from qdrant_client import QdrantClient
client = QdrantClient(":memory:")  # no server needed
```

## Using QdrantRM in DSPy

### Basic setup

```python
import dspy
from qdrant_client import QdrantClient
from dspy_qdrant import QdrantRM

client = QdrantClient("http://localhost:6333")

retriever = QdrantRM(
    qdrant_collection_name="my_docs",
    qdrant_client=client,
    k=5,
    document_field="document",  # payload field containing document text (default)
)

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"), rm=retriever)  # or "anthropic/claude-sonnet-4-5-20250929", etc.

# Now dspy.Retrieve() uses Qdrant
search = dspy.Retrieve(k=5)
result = search("How do refunds work?")
print(result.passages)
```

### QdrantRM constructor

```python
QdrantRM(
    qdrant_collection_name: str,       # required — collection name in Qdrant
    qdrant_client: QdrantClient,       # required — initialized client instance
    k: int = 3,                        # top passages to retrieve
    document_field: str = "document",  # payload field with document text
    vectorizer=None,                   # BaseSentenceVectorizer (default: FastEmbedVectorizer)
    vector_name: str = None,           # named vector to search (default: first available)
)
```

By default, QdrantRM uses [FastEmbed](https://qdrant.github.io/fastembed/) (`BAAI/bge-small-en-v1.5`) for query vectorization. To use a different embedder, pass a custom `vectorizer`.

### Using Qdrant Cloud

```python
import os
from qdrant_client import QdrantClient
from dspy_qdrant import QdrantRM

client = QdrantClient(
    url=os.environ["QDRANT_URL"],
    api_key=os.environ["QDRANT_API_KEY"],
)

retriever = QdrantRM(
    qdrant_collection_name="my_docs",
    qdrant_client=client,
    k=5,
)
```

## Indexing documents into Qdrant

Before you can search, you need to populate your Qdrant collection:

```python
from qdrant_client import QdrantClient, models
import dspy

client = QdrantClient("http://localhost:6333")
embedder = dspy.Embedder("openai/text-embedding-3-small", dimensions=512)

# Your documents
docs = [
    {"id": 1, "document": "Refunds are processed within 5-7 business days.", "category": "billing"},
    {"id": 2, "document": "Reset your password at Settings > Security.", "category": "account"},
    {"id": 3, "document": "Enterprise plans include SSO and dedicated support.", "category": "plans"},
]

# Create collection
client.create_collection(
    collection_name="my_docs",
    vectors_config=models.VectorParams(size=512, distance=models.Distance.COSINE),
)

# Upsert with embeddings
vectors = embedder([d["document"] for d in docs])
client.upsert(
    collection_name="my_docs",
    points=[
        models.PointStruct(
            id=d["id"],
            vector=v,
            payload={"document": d["document"], "category": d["category"]},
        )
        for d, v in zip(docs, vectors)
    ],
)
```

## RAG pipeline with Qdrant

```python
import dspy
from qdrant_client import QdrantClient
from dspy_qdrant import QdrantRM

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))  # or "anthropic/claude-sonnet-4-5-20250929", etc.

retriever = QdrantRM(
    qdrant_collection_name="my_docs",
    qdrant_client=QdrantClient("http://localhost:6333"),
    k=5,
)

class RAG(dspy.Module):
    def __init__(self):
        self.retrieve = retriever
        self.answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.answer(context=context, question=question)

rag = RAG()
result = rag(question="How do refunds work?")
print(result.answer)
```

## Verify retrieval is working

Before wiring retrieval into a RAG pipeline, run a sanity check:

```python
result = retriever("your test query here")
assert len(result.passages) > 0, "Empty results — check document_field matches your payload schema"
print(result.passages[0][:300])  # Top passage should be semantically relevant to the query
```

Empty results: likely a `document_field` mismatch (gotcha #2). Irrelevant results: query vectorizer does not match the model used when indexing (gotcha #4).

## Hybrid search (dense + sparse)

Qdrant supports hybrid search combining dense (semantic) and sparse (keyword) vectors in the same collection. This improves recall for queries that need both semantic understanding and exact keyword matching.

```python
from qdrant_client import QdrantClient, models

client = QdrantClient("http://localhost:6333")

# Create collection with both dense and sparse vectors
client.create_collection(
    collection_name="hybrid_docs",
    vectors_config=models.VectorParams(size=512, distance=models.Distance.COSINE),
    sparse_vectors_config={
        "keywords": models.SparseVectorParams(
            modifier=models.Modifier.IDF,
        ),
    },
)
```

Then query with both:

```python
results = client.query_points(
    collection_name="hybrid_docs",
    prefetch=[
        models.Prefetch(query=dense_vector, using="", limit=20),
        models.Prefetch(query=sparse_vector, using="keywords", limit=20),
    ],
    query=models.FusionQuery(fusion=models.Fusion.RRF),  # reciprocal rank fusion
    limit=5,
)
```

## Other vector DBs with DSPy

Since DSPy 3.0 removed built-in community retrievers, use a custom `dspy.Retrieve` subclass for any vector database. The pattern is always the same:

### Custom retriever pattern

```python
class MyVectorDBRetriever(dspy.Retrieve):
    def __init__(self, client, collection, k=3):
        super().__init__(k=k)
        self.client = client
        self.collection = collection

    def forward(self, query, k=None):
        k = k or self.k
        results = self.client.search(self.collection, query, top_k=k)
        return dspy.Prediction(passages=[r["text"] for r in results])
```

### Pinecone custom retriever

```python
from pinecone import Pinecone
import dspy

class PineconeRetriever(dspy.Retrieve):
    def __init__(self, index_name, embedder, k=3):
        super().__init__(k=k)
        pc = Pinecone()  # reads PINECONE_API_KEY from env
        self.index = pc.Index(index_name)
        self.embedder = embedder

    def forward(self, query, k=None):
        k = k or self.k
        vector = self.embedder(query)
        results = self.index.query(vector=vector, top_k=k, include_metadata=True)
        passages = [m["metadata"]["text"] for m in results["matches"]]
        return dspy.Prediction(passages=passages)

# Usage
embedder = dspy.Embedder("openai/text-embedding-3-small", dimensions=512)
retriever = PineconeRetriever("my-index", embedder, k=5)
```

### ChromaDB custom retriever

```python
import chromadb
import dspy

class ChromaRetriever(dspy.Retrieve):
    def __init__(self, collection_name, k=3):
        super().__init__(k=k)
        client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = client.get_or_create_collection(collection_name)

    def forward(self, query, k=None):
        k = k or self.k
        results = self.collection.query(query_texts=[query], n_results=k)
        return dspy.Prediction(passages=results["documents"][0])

# Usage
retriever = ChromaRetriever("my_docs", k=5)
```

### Weaviate custom retriever

```python
import weaviate
import dspy

class WeaviateRetriever(dspy.Retrieve):
    def __init__(self, class_name, url="http://localhost:8080", k=3):
        super().__init__(k=k)
        self.client = weaviate.connect_to_local(host=url.replace("http://", "").split(":")[0])
        self.collection = self.client.collections.get(class_name)

    def forward(self, query, k=None):
        k = k or self.k
        results = self.collection.query.near_text(query=query, limit=k)
        passages = [obj.properties["text"] for obj in results.objects]
        return dspy.Prediction(passages=passages)

# Usage
retriever = WeaviateRetriever("MyDocs", k=5)
```

## Vector DB comparison

| Feature | Qdrant | Pinecone | ChromaDB | Weaviate |
|---------|--------|----------|----------|----------|
| **DSPy package** | `dspy-qdrant` (official) | None (custom retriever) | None (custom retriever) | None (custom retriever) |
| **Self-hosted** | Yes (Docker, binary) | No (cloud only) | Yes (pip, Docker) | Yes (Docker) |
| **Cloud option** | Yes (free tier) | Yes (free tier) | No | Yes (free tier) |
| **Hybrid search** | Yes (dense + sparse) | Yes (sparse + dense) | No | Yes (BM25 + vector) |
| **Best for** | Production + DSPy | Cloud-native, serverless | Local prototyping | Multi-modal, GraphQL |
| **Language** | Rust | Managed service | Python | Go |

### Choosing a vector DB

```
Starting a new DSPy project?
  → Qdrant (official DSPy package, easiest setup)

Prototyping locally, smallest footprint?
  → ChromaDB (pip install, in-memory or persistent, no server)

Already using Pinecone/Weaviate in production?
  → Write a custom retriever (15 lines, shown above)

Need hybrid search (keyword + semantic)?
  → Qdrant or Weaviate
```

## Gotchas

1. **Claude fabricates QdrantRM constructor parameters.** Claude invents params like `qdrant_client_url`, `qdrant_client_api_key`, `embedding_model`, and `embedding_dimensions`. These do not exist. QdrantRM takes a `qdrant_client` (an initialized `QdrantClient` instance) and a `vectorizer` (a `BaseSentenceVectorizer`). Always construct the `QdrantClient` separately, then pass it.
2. **Claude uses `document_field="text"` but the default is `"document"`.** When indexing, store content in a payload field named `document` (the default), or explicitly set `document_field="text"` if your payload uses `text`. Mismatched field names silently return empty passages.
3. **DSPy 3.0 removed community retrievers** — `from dspy.retrieve.chromadb_rm import ChromadbRM` no longer works. Use `dspy-qdrant` or write a custom `dspy.Retrieve` subclass.
4. **QdrantRM uses FastEmbed by default, not OpenAI embeddings.** The default vectorizer is `FastEmbedVectorizer` using `BAAI/bge-small-en-v1.5`. Your indexed vectors must match this model. If you indexed with OpenAI embeddings, pass a custom vectorizer that uses the same model.
5. **`dspy.Embeddings` is simpler for in-memory retrieval.** If you just need to search a small corpus (under ~100k passages) without a vector DB, use `dspy.Embeddings(corpus=docs, embedder=embedder)` instead. It handles indexing and search in one class. Use Qdrant when you need persistence, filtering, hybrid search, or scale.

## Additional resources

- [Qdrant DSPy integration guide](https://qdrant.tech/documentation/frameworks/dspy/)
- [dspy-qdrant GitHub](https://github.com/qdrant/dspy-qdrant)
- [Qdrant hybrid search guide](https://qdrant.tech/documentation/search/hybrid-queries/)
- [dspy.Embeddings API docs](https://dspy.ai/api/tools/Embeddings/)
- For API details, see [reference.md](reference.md)
- For worked examples, see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **DSPy retrieval basics** (Retrieve, ColBERTv2, Embedder, Embeddings) — `/dspy-retrieval`
- **Building RAG pipelines** end-to-end — `/ai-searching-docs`
- **Evaluating RAG quality** with decomposed metrics — `/dspy-ragas`
- **Stopping hallucinations** in RAG — `/ai-stopping-hallucinations`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
