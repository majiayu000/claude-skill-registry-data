---
name: goodmem:mcp
description: Reference for GoodMem MCP server tools. Documents all available tools for managing embedders, LLMs, rerankers, spaces, memories, retrieval, OCR, users, API keys, and system administration. Use when an agent needs to understand what GoodMem MCP tools are available, how to use them, or what parameters they accept.
allowed-tools: Read
---

# GoodMem MCP Tools Reference

The GoodMem MCP server exposes 41 tools across 10 namespaces. Each tool maps directly to a GoodMem REST API endpoint.

**Setup**: The MCP server requires two environment variables:
```bash
export GOODMEM_BASE_URL="https://your-server.example.com"
export GOODMEM_API_KEY="gm_..."
```

---

## Embedders

Manage embedding models that convert text to vectors.

### `goodmem_embedders_create`
Register a new embedding model.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `display_name` | string | yes | Human-readable name |
| `model_identifier` | string | yes | Model name (e.g., `text-embedding-3-large`) |
| `provider_type` | string | yes | Provider: `OPENAI`, `VOYAGE`, `GOOGLE`, etc. |
| `endpoint_url` | string | no | Custom endpoint URL |
| `dimensionality` | integer | no | Embedding dimensions |
| `credentials` | object | no | API credentials for the provider |

### `goodmem_embedders_list`
List all registered embedders. Supports pagination via `max_results` and `next_token`.

### `goodmem_embedders_get`
Get an embedder by ID.
- `id` (string, required)

### `goodmem_embedders_update`
Update an embedder's configuration.
- `id` (string, required)
- Request body with fields to update

### `goodmem_embedders_delete`
Delete an embedder.
- `id` (string, required)

---

## LLMs

Manage large language model configurations.

### `goodmem_llms_create`
Register a new LLM configuration.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `display_name` | string | yes | Human-readable name |
| `model_identifier` | string | yes | Model name (e.g., `gpt-4o`) |
| `provider_type` | string | yes | Provider: `OPENAI`, `ANTHROPIC`, etc. |
| `endpoint_url` | string | no | Custom endpoint URL |
| `credentials` | object | no | API credentials |

### `goodmem_llms_list` / `goodmem_llms_get` / `goodmem_llms_update` / `goodmem_llms_delete`
Standard CRUD operations (same pattern as embedders).

---

## Rerankers

Manage reranker models for result re-ranking.

### `goodmem_rerankers_create`
Register a new reranker model.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `display_name` | string | yes | Human-readable name |
| `model_identifier` | string | yes | Model name (e.g., `rerank-2`) |
| `provider_type` | string | yes | Provider: `VOYAGE`, `COHERE`, etc. |
| `credentials` | object | no | API credentials |

### `goodmem_rerankers_list` / `goodmem_rerankers_get` / `goodmem_rerankers_update` / `goodmem_rerankers_delete`
Standard CRUD operations.

---

## Spaces

Manage memory spaces — containers for organizing memories with chunking and embedding settings.

### `goodmem_spaces_create`
Create a new memory space.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `display_name` | string | yes | Human-readable name |
| `embedder_id` | string | yes | ID of the embedder to use |
| `chunking_config` | object | no | Chunking strategy configuration |
| `description` | string | no | Space description |

### `goodmem_spaces_list` / `goodmem_spaces_get` / `goodmem_spaces_update` / `goodmem_spaces_delete`
Standard CRUD operations.

---

## Memories

Store, retrieve, and manage memories within spaces.

### `goodmem_memories_create`
Store a new memory in a space.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `space_id` | string | yes | Target space |
| `content` | string | yes | Text content to store |
| `content_type` | string | no | MIME type (default: `text/plain`) |

### `goodmem_memories_retrieve`
Semantic retrieval — search memories by meaning. Returns NDJSON stream.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `space_ids` | array | yes | Spaces to search |
| `query` | string | yes | Search query |
| `max_results` | integer | no | Max results to return |

### `goodmem_memories_list`
List memories in a space. Supports pagination.
- `space_id` (string, required)

### `goodmem_memories_get`
Get a memory by ID.
- `id` (string, required)

### `goodmem_memories_delete`
Delete a memory.
- `id` (string, required)

### `goodmem_memories_batch_create`
Create multiple memories in one request.

### `goodmem_memories_batch_get`
Get multiple memories by IDs.

### `goodmem_memories_batch_delete`
Delete multiple memories by IDs.

### `goodmem_memories_content`
*Not available via MCP (binary response).*

### `goodmem_memories_pages` / `goodmem_memories_pages_image`
*Not available via MCP (binary response).*

---

## OCR

### `goodmem_ocr_document`
Extract text from a document using OCR.

---

## Users

### `goodmem_users_me`
Get the current authenticated user.

### `goodmem_users_get`
Get a user by ID or email.

---

## API Keys

### `goodmem_apikeys_create` / `goodmem_apikeys_list` / `goodmem_apikeys_update` / `goodmem_apikeys_delete`
Manage API keys for authentication.

---

## System

### `goodmem_system_info`
Get server version and configuration info.

### `goodmem_system_init`
Initialize the server (first-time setup).

---

## Admin

### `goodmem_admin_drain`
Drain resources from the server.

### `goodmem_admin_background_jobs_purge`
Purge completed background jobs.

### `goodmem_admin_license_reload`
Reload the server license.
