---




name: chroma
description: Integrates Chroma vector database (collections, embeddings, query, metadata
  filtering, persistence) using the chromadb Python SDK for local and server-based
  vector search.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: chroma, chromadb, vector database, embedding store, similarity search,
    chroma collection, how do i use chroma, local vector search
  archetypes:
  - tactical
  - generation
  anti_triggers:
  - brainstorming
  - vague ideation
  - code golf
  - over-engineering
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
  role: implementation
  scope: implementation
  output-format: code
  content-types:
  - code
  - guidance
  - examples
  - do-dont
  related-skills: coding-openai-api, coding-pinecone-api, coding-weaviate-api, coding-langchain,
    coding-llamaindex




---




# Chroma Integration

Integrates Chroma vector database using the `chromadb` Python SDK. When loaded, this skill makes the model implement Chroma operations for creating and managing collections, adding and querying documents, metadata filtering, embedding functions, and persistence.

## When to Use

Use this skill when:

- Building local vector search applications with in-memory or persistent storage
- Prototyping RAG pipelines before scaling to production vector databases
- Using Chroma as a local embedding store for testing and development
- Building applications that need a simple, lightweight vector database without cloud dependencies
- Running Chroma in server mode for distributed access
- Using custom embedding functions with collections
- Implementing metadata filtering and document filtering in vector search

---

## When NOT to Use

- For production-scale vector search with auto-scaling, use `coding-pinecone-api`
- For advanced hybrid search and generative modules, use `coding-weaviate-api`
- For production applications requiring high availability and replication, use a cloud vector database

---

## Core Workflow

1. **Choose a Client Mode** — Select the right client: `chromadb.Client()` for ephemeral in-memory (data lost on close); `chromadb.PersistentClient(path="./chroma")` for disk persistence; `chromadb.HttpClient()` for connecting to a running Chroma server. **Checkpoint:** For persistent mode, verify the data directory exists after the first write.

2. **Create or Get a Collection** — Use `client.create_collection(name)` for new collections or `client.get_or_create_collection(name)` for idempotent access. Collections have names (unique), optional metadata, and an embedding function. **Checkpoint:** Verify collection exists with `collection.count()` returning 0 initially.

3. **Add Documents** — Use `collection.add()` with `ids`, `documents`, `embeddings` (optional — auto-computed if omitted), `metadatas`, and `uris`. The embedding function configured on the collection automatically converts documents to vectors. **Checkpoint:** Verify after adding: `collection.count()` returns the expected count.

4. **Query by Similarity** — Use `collection.query()` with `query_texts`, `query_embeddings`, `query_images`, or `query_uris`. Set `n_results` for the number of neighbors. Use `where` for metadata filtering and `where_document` for content filtering. **Checkpoint:** Verify results contain the expected fields based on the `include` parameter.

5. **Update and Delete** — Use `collection.update()` to modify existing records (by ID), `collection.upsert()` to add or update, `collection.delete()` to remove by ID or filter, and `collection.get()` to retrieve by ID or filter. Use `collection.peek()` to inspect the first N records. **Checkpoint:** After delete, verify `collection.count()` decreased and `collection.get(ids=[...])` returns empty.

---

## Implementation Patterns

### Pattern 1: Persistent Client with Documents

```python
from __future__ import annotations

import chromadb

# ❌ BAD — ephemeral client, no persistence, no error handling
import chromadb
client = chromadb.Client()
collection = client.create_collection("docs")
collection.add(documents=["Hello"], ids=["1"])
results = collection.query(query_texts=["Hi"], n_results=1)
# Data lost when client closes — no persistence path

# ✅ GOOD — PersistentClient, proper error handling, context manager
client = chromadb.PersistentClient(path="./chroma_data")


class DocumentStore:
    """Manages a Chroma collection for document storage and retrieval."""

    def __init__(self, collection_name: str = "documents") -> None:
        self.collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Document storage for RAG"},
        )

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        metadatas: list[dict] | None = None,
    ) -> None:
        """Add documents to the collection.

        Args:
            ids: Unique identifiers for each document.
            documents: The document text content.
            metadatas: Optional metadata dicts for each document.

        Raises:
            ValueError: If IDs and documents lengths differ.
        """
        if len(ids) != len(documents):
            raise ValueError("ids and documents must have the same length.")
        if metadatas and len(metadatas) != len(documents):
            raise ValueError("metadatas length must match documents.")

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: dict | None = None,
        where_document: dict | None = None,
    ) -> list[dict]:
        """Search for similar documents.

        Args:
            query: Natural language query text.
            n_results: Number of nearest neighbors.
            where: Metadata filter (e.g., {"category": "tech"}).
            where_document: Document content filter.

        Returns:
            List of results with id, document, metadata, and distance.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            where_document=where_document,
            include=["documents", "metadatas", "distances"],
        )

        output: list[dict] = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })
        return output
```

### Pattern 2: Custom Embedding Function

```python
from __future__ import annotations

from chromadb import Documents, EmbeddingFunction, Embeddings


class OpenAIEmbeddingFunction(EmbeddingFunction[Documents]):
    """Custom embedding function using OpenAI's API.

    Chroma calls __call__ to convert documents to vectors automatically
    during add() and query() operations.
    """

    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def __call__(self, input: Documents) -> Embeddings:
        """Convert documents to embedding vectors.

        Args:
            input: List of document text strings.

        Returns:
            List of embedding vectors, one per input document.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=input,
        )
        sorted_data = sorted(response.data, key=lambda x: x.index)
        return [item.embedding for item in sorted_data]

    @staticmethod
    def name() -> str:
        return "openai_embedding"

    def get_config(self) -> dict:
        return {"model": self.model}


# Usage with custom embedding function
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
embedding_fn = OpenAIEmbeddingFunction(api_key="sk-...", model="text-embedding-3-small")

collection = client.create_collection(
    name="openai-docs",
    embedding_function=embedding_fn,
)

# Chroma automatically uses the embedding function
collection.add(
    documents=["This is a document about AI"],
    ids=["doc-1"],
    metadatas=[{"topic": "AI"}],
)

# Query also uses the same embedding function automatically
results = collection.query(query_texts=["Tell me about artificial intelligence"], n_results=5)
```

### Pattern 3: Server Mode with HttpClient

```python
from __future__ import annotations

import chromadb


def connect_to_server(host: str = "localhost", port: int = 8000) -> chromadb.ClientAPI:
    """Connect to a Chroma server instance.

    Start the server first with: chroma run --path /db_path

    Args:
        host: Chroma server hostname.
        port: Chroma server HTTP port.

    Returns:
        Configured client for remote Chroma access.
    """
    return chromadb.HttpClient(
        host=host,
        port=port,
        headers={"Authorization": "Bearer your-auth-token"} if False else None,
    )


# Example with a configured schema
from chromadb import Schema, VectorIndexConfig, HnswIndexConfig

schema = Schema()
schema.create_index(
    name="vector_idx",
    config=VectorIndexConfig(
        space="cosine",
        hnsw=HnswIndexConfig(ef_construction=200, m=16),
    ),
)

client = connect_to_server()
collection = client.create_collection(
    name="configured_collection",
    schema=schema,
    metadata={"description": "Collection with custom HNSW parameters"},
)
```

---

## Constraints

### MUST DO
- Use `PersistentClient(path=...)` when data must survive application restarts
- Use `get_or_create_collection()` for idempotent collection access in production code
- Use context managers (`with client:`) or call `client.close()` on `PersistentClient` to avoid SQLite file locking
- Use `collection.count()` to verify data was added or deleted correctly
- Use `include=["documents", "metadatas", "distances"]` in queries to get full result context

### MUST NOT DO
- Use the default `Client()` (ephemeral) for production — data is lost when the process exits
- Hardcode embedding API keys in embedding function definitions — read from environment variables
- Use `collection.add()` with mismatched list lengths for ids, documents, embeddings, and metadatas
- Skip `client.close()` or the context manager for `PersistentClient` — this causes SQLite locking issues

---

## Live References

| Resource | URL |
|----------|-----|
| Chroma Documentation | https://docs.trychroma.com/ |
| Chroma Python API Reference | https://docs.trychroma.com/reference/python/ |
| Chroma Client Setup | https://docs.trychroma.com/docs/run-chroma/clients |
| Chroma Collections | https://docs.trychroma.com/docs/concepts/collections |
| Chroma Embedding Functions | https://docs.trychroma.com/docs/guides/embedding-functions |
| Chroma GitHub | https://github.com/chroma-core/chroma |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `coding-openai-api` | Generating embeddings for Chroma with OpenAI models |
| `coding-pinecone-api` | Production-scale vector database alternative |
| `coding-weaviate-api` | Advanced vector search with generative modules |
| `coding-langchain` | LangChain vector store integration with Chroma |
| `coding-llamaindex` | LlamaIndex vector store backend with Chroma |
