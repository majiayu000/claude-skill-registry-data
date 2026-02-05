---
name: rag-chatbot
description: Build the FastAPI-based RAG service using OpenAI Agents/ChatKit, Neon Postgres, and Qdrant for the textbook. Use when creating ingestion pipelines, query endpoints, or configuring vector storage for book content.
---

# RAG Chatbot Skill

## Instructions

1. **Setup**
   - Create Python virtual environment
   - Install dependencies:
     ```bash
     pip install fastapi uvicorn pydantic openai qdrant-client asyncpg langchain-text-splitters tenacity python-dotenv
     ```
   - Create `.env.example` with: `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `NEON_DATABASE_URL`, `EMBED_MODEL`, `CHAT_MODEL`

2. **Data model**
   - Neon tables:
     - `documents(id, path, checksum, meta jsonb)`
     - `chunks(id, doc_id, content, meta jsonb)`
     - `sessions(id, user_id, prefs jsonb)`
   - Qdrant collection `book_chunks` with payload: `doc_path`, `module`, `week`, `tags`, `heading_path`

3. **Ingestion**
   - Walk markdown glob, parse frontmatter
   - Split chunks (by headings and tokens)
   - Embed via OpenAI, upsert to Qdrant
   - Store doc/chunk metadata in Neon
   - Track checksum for incremental ingest

4. **Query endpoints**
   - `/health` - healthcheck
   - `/ingest` - trigger ingestion
   - `/query` - semantic search + LLM answer with sources
   - `/query/selected` - bypass vector search, inject user-selected text as context

5. **Ops**
   - Configure CORS for Docusaurus origin
   - Add logging with request IDs
   - Include safety: max tokens, fallback answers, latency budget

## Examples

```python
# Query endpoint structure
@app.post("/query")
async def query(request: QueryRequest):
    # 1. Embed query
    # 2. Search Qdrant
    # 3. Build context from chunks
    # 4. Call OpenAI with context
    # 5. Return answer + sources
    pass
```

```bash
# Run server
uvicorn main:app --reload --port 8000
```

## Definition of Done

- FastAPI runs locally with env sample; healthcheck ok
- Ingestion populates Qdrant + Neon with at least sample doc; idempotent reruns succeed
- Query endpoints return grounded answers with cited headings
- Selected-text mode echoes user selection
- README snippet for running server and triggering ingest
