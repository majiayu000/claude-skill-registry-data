---
name: moss
description: Documentation and capabilities reference for Moss semantic search.
  Use for understanding Moss APIs, SDKs, and integration patterns.
metadata:
  author: usemoss
  version: "1.0"
  docs-url: https://docs.moss.dev
  mintlify-proj: moss
  primary-credential: MOSS_PROJECT_KEY
  required-env:
    - name: MOSS_PROJECT_ID
      description: Project identifier from the Moss Portal
    - name: MOSS_PROJECT_KEY
      description: Project access key from the Moss Portal (treat as a secret)
  minis:
    originalSource: "https://clawskills.sh/skills/coderomaster-moss"
    convertedAt: "2026-10-31T22:12:41.365Z"
    license: "Unknown"
---

# Moss Agent Skills

## Capabilities

Moss is the real-time semantic search runtime for conversational AI. It delivers sub-10ms lookups and instant index updates that run in the browser, on-device, or in the cloud - wherever your agent lives. Agents can create indexes, embed documents, perform semantic/hybrid searches, and manage document lifecycles without managing infrastructure. The platform handles embedding generation, index persistence, and optional cloud sync - allowing agents to focus on retrieval logic rather than infrastructure.

## Skills

### Index Management

- **Create Index**: Build a new semantic index with documents and embedding model selection
- **Load Index**: Load an existing index from persistent storage for querying
- **Get Index**: Retrieve metadata about a specific index (document count, model, etc.)
- **List Indexes**: Enumerate all indexes under a project
- **Delete Index**: Remove an index and all associated data

### Document Operations

- **Add Documents**: Insert or upsert documents into an existing index with optional metadata
- **Get Documents**: Retrieve stored documents by ID or fetch all documents
- **Delete Documents**: Remove specific documents from an index by their IDs

### Search & Retrieval

- **Semantic Search**: Query using natural language with vector similarity matching
- **Keyword Search**: Use BM25-based keyword matching for exact term lookups
- **Hybrid Search**: Blend semantic and keyword search with configurable alpha weighting (Python SDK)
- **Metadata Filtering**: Constrain results by document metadata (category, language, tags)
- **Top-K Results**: Return configurable number of best-matching documents with scores

### Embedding Models

- **moss-minilm**: Fast, lightweight model optimized for edge/offline use (default)
- **moss-mediumlm**: Higher accuracy model with reasonable performance for precision-critical use cases

### SDK Methods

| JavaScript        | Python             | Description                    |
| ----------------- | ------------------ | ------------------------------ |
| `createIndex()`   | `create_index()`   | Create index with documents    |
| `loadIndex()`     | `load_index()`     | Load index from storage        |
| `getIndex()`      | `get_index()`      | Get index metadata             |
| `listIndexes()`   | `list_indexes()`   | List all indexes               |
| `deleteIndex()`   | `delete_index()`   | Delete an index                |
| `addDocs()`       | `add_docs()`       | Add/upsert documents           |
| `getDocs()`       | `get_docs()`       | Retrieve documents             |
| `deleteDocs()`    | `delete_docs()`    | Remove documents               |
| `query()`         | `query()`          | Semantic / hybrid search       |

### API Actions

All REST API operations go through `POST /v1/manage` (base URL: `https://service.usemoss.dev/v1`) with an `action` field:

| Action         | Purpose                                          | Extra required fields                           |
| -------------- | ------------------------------------------------ | ----------------------------------------------- |
| `initUpload`   | Get a presigned URL to upload index data         | `indexName`, `modelId`, `docCount`, `dimension` |
| `startBuild`   | Trigger an index build after uploading data      | `jobId`                                         |
| `getJobStatus` | Check the status of an async build job           | `jobId`                                         |
| `getIndex`     | Fetch metadata for a single index                | `indexName`                                     |
| `listIndexes`  | Enumerate every index under the project          | —                                               |
| `deleteIndex`  | Remove an index record and assets                | `indexName`                                     |
| `getIndexUrl`  | Get download URLs for a built index              | `indexName`                                     |
| `addDocs`      | Upsert documents into an existing index          | `indexName`, `docs`                             |
| `deleteDocs`   | Remove documents by ID                           | `indexName`, `docIds`                           |
| `getDocs`      | Retrieve stored documents (without embeddings)   | `indexName`                                     |

## Workflows

### Basic Semantic Search Workflow

1. Initialize MossClient with project credentials
2. Call `createIndex()` with documents and model options (`{ modelId: 'moss-minilm' }` in JS; `"moss-minilm"` string in Python)
3. Call `loadIndex()` to prepare index for queries
4. Call `query()` with search text and `topK` (JS) or `QueryOptions(top_k=...)` (Python)
5. Process returned documents with scores

### Hybrid Search Workflow (Python)

Hybrid blending via `alpha` is available in the Python SDK via `QueryOptions`:

1. Create and load index as above
2. Call `query()` with a `QueryOptions` object specifying `alpha`
3. `alpha=1.0` = pure semantic, `alpha=0.0` = pure keyword, `alpha=0.6` = 60/40 blend
4. Default is semantic-heavy for conversational use cases

### Document Update Workflow

1. Initialize client and ensure index exists
2. Call `addDocs()` with new documents (upserts by default — existing IDs are updated)
3. Call `deleteDocs()` to remove outdated documents by ID

### Voice Agent Context Injection Workflow

This is an opt-in integration pattern for voice agent pipelines — it is not automatic behavior of this skill.

1. Initialize MossClient and load index at agent startup
2. In your application code, call `query()` on each user message to retrieve relevant context
3. Inject search results into the LLM context before generating a response
4. Respond with knowledge-grounded answer (no tool-calling latency)

### Offline-First Search Workflow

1. Create index with documents using local embedding model
2. Load index from local storage
3. Query runs entirely on-device with sub-10ms latency
4. Optionally sync to cloud for backup and sharing

## Integration

### Voice Agent Frameworks

- **LiveKit**: Context injection into voice agent pipeline with `inferedge-moss` SDK
- **Pipecat**: Pipeline processor via `pipecat-moss` package that auto-injects retrieval results

## Context

### Authentication

SDK requires project credentials:

- `MOSS_PROJECT_ID`: Project identifier from Moss Portal
- `MOSS_PROJECT_KEY`: Project access key from Moss Portal

```bash theme={null}
export MOSS_PROJECT_ID=your_project_id
export MOSS_PROJECT_KEY=your_project_key
```

REST API requires the following on every request:

- `x-project-key` header: project access key
- `x-service-version: v1` header: API version
- `projectId` field in the JSON body

```bash theme={null}
curl -X POST "https://service.usemoss.dev/v1/manage" \
  -H "Content-Type: application/json" \
  -H "x-service-version: v1" \
  -H "x-project-key: moss_access_key_xxxxx" \
  -d '{"action": "listIndexes", "projectId": "project_123"}'
```

### Package Installation

| Language              | Package           | Install Command               |
| --------------------- | ----------------- | ----------------------------- |
| JavaScript/TypeScript | `@inferedge/moss` | `npm install @inferedge/moss` |
| Python                | `inferedge-moss`  | `pip install inferedge-moss`  |
| Pipecat Integration   | `pipecat-moss`    | `pip install pipecat-moss`    |

### Document Schema

```typescript theme={null}
interface DocumentInfo {
  id: string;        // Required: unique identifier
  text: string;      // Required: content to embed and search
  metadata?: object; // Optional: key-value pairs for filtering
}
```

### Query Parameters

| Parameter   | SDK         | Type   | Default  | Description                                  |
| ----------- | ----------- | ------ | -------- | -------------------------------------------- |
| `indexName` | JS + Python | string | —        | Target index name (required)                 |
| `query`     | JS + Python | string | —        | Natural language search text (required)      |
| `topK`      | JS          | number | 5        | Max results to return                        |
| `top_k`     | Python      | int    | 5        | Max results to return                        |
| `alpha`     | Python only | float  | ~0.8     | Hybrid weighting: 0.0=keyword, 1.0=semantic  |
| `filters`   | JS + Python | object | —        | Metadata constraints                         |

### Model Selection

| Model           | Use Case                            | Tradeoff          |
| --------------- | ----------------------------------- | ----------------- |
| `moss-minilm`   | Edge, offline, browser, speed-first | Fast, lightweight |
| `moss-mediumlm` | Precision-critical, higher accuracy | Slightly slower   |

### Performance Expectations

- Sub-10ms local queries (hardware-dependent)
- Instant index updates without reindexing entire corpus
- Sync is optional; compute stays on-device
- No infrastructure to manage

### Chunking Best Practices

- Aim for ~200–500 tokens per chunk
- Overlap 10–20% to preserve context
- Normalize whitespace and strip boilerplate

### Common Errors

| Error                      | Cause               | Fix                                          |
| -------------------------- | ------------------- | -------------------------------------------- |
| Unauthorized               | Missing credentials | Set `MOSS_PROJECT_ID` and `MOSS_PROJECT_KEY` |
| Index not found            | Query before create | Call `createIndex()` first                   |
| Index not loaded           | Query before load   | Call `loadIndex()` before `query()`          |
| Missing embeddings runtime | Invalid model       | Use `moss-minilm` or `moss-mediumlm`         |

### Async Pattern

All SDK methods are async — always use `await`:

```typescript theme={null}
// JavaScript
import { MossClient, DocumentInfo } from '@inferedge/moss'
const client = new MossClient(process.env.MOSS_PROJECT_ID!, process.env.MOSS_PROJECT_KEY!)
await client.createIndex('faqs', docs, { modelId: 'moss-minilm' })
await client.loadIndex('faqs')
const results = await client.query('faqs', 'search text', { topK: 5 })
```

```python theme={null}
# Python
import os
from inferedge_moss import MossClient, QueryOptions
client = MossClient(os.getenv('MOSS_PROJECT_ID'), os.getenv('MOSS_PROJECT_KEY'))
await client.create_index('faqs', docs, 'moss-minilm')
await client.load_index('faqs')
results = await client.query('faqs', 'search text', QueryOptions(top_k=5, alpha=0.6))
```

---

> For additional documentation and navigation, see: [https://docs.moss.dev/llms.txt](https://docs.moss.dev/llms.txt)
