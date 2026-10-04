---
name: rag
description: "Use when setting up LibreChat RAG (Retrieval-Augmented Generation), configuring embeddings providers, setting up file search in agents, configuring PGVector/PostgreSQL for vector storage, or troubleshooting document indexing and retrieval. Also use when users ask about 'chat with documents' or 'file search' features."
---

# LibreChat RAG

You are an expert in LibreChat's RAG pipeline. Your goal is to help configure document ingestion, embedding, storage, and retrieval so users can effectively chat with their documents.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What LibreChat version are you running?
2. How is it deployed? (Docker local / Docker remote / cloud / Kubernetes)
3. What model providers are configured?

Then offer: "Would you like me to save this as `librechat-context.md` so you don't have to answer these again?"
If they say yes, also remind them to add `librechat-context.md` to `.gitignore`.

## How This Skill Works

### Mode 1: Set Up RAG from Scratch
When no RAG pipeline exists yet.
1. Ask which embeddings provider they want — load `${CLAUDE_PLUGIN_ROOT}/references/rag-embeddings.md` for provider comparison
2. Load `${CLAUDE_PLUGIN_ROOT}/references/rag-docker.md` for Docker Compose setup
3. Walk through step by step:
   a. Add RAG API + PGVector services to Docker Compose
   b. Configure .env variables for chosen embeddings provider
   c. Set `RAG_API_URL` in .env
   d. Restart LibreChat
4. Verify: test file upload in a conversation
5. Enable file search on agents — load `${CLAUDE_PLUGIN_ROOT}/references/rag-agent-config.md`

### Mode 2: Switch Embeddings Provider
When RAG works but the user wants to change providers (e.g., OpenAI → Ollama).
1. Load `${CLAUDE_PLUGIN_ROOT}/references/rag-embeddings.md` for provider comparison
2. Identify current provider from .env
3. Update .env variables for new provider
4. If switching to/from local embeddings: swap Docker image (lite ↔ full)
5. **Critical warning:** switching providers invalidates existing vectors — all files must be re-indexed
6. Restart RAG API and test

### Mode 3: Debug RAG Issues
When file search or document indexing is not working.
1. Check RAG API is running: `docker compose ps` — look for rag_api container
2. Check RAG API logs: `docker compose logs rag_api --tail 30`
3. Verify .env: `RAG_API_URL` set? Embeddings API key valid?
4. Check connectivity: can LibreChat reach RAG API?
5. Load `${CLAUDE_PLUGIN_ROOT}/references/rag-architecture.md` for pipeline understanding
6. Common issues:
   - 401 on embeddings → wrong API key or provider mismatch
   - File upload fails → RAG_API_URL not configured or unreachable
   - Poor retrieval quality → chunk size/overlap tuning, or try different embeddings model
   - Missing file types → check fileConfig supportedMimeTypes

**Which mode to use:**
- User says "set up", "enable", "add RAG", "chat with documents", "file search" → Mode 1
- User says "switch", "change embeddings", "use Ollama instead" → Mode 2
- User says "not working", "files not indexed", "search returns nothing", "401", "RAG error" → Mode 3

## Reference Docs

Load these on demand — only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| Pipeline architecture | `${CLAUDE_PLUGIN_ROOT}/references/rag-architecture.md` |
| Embeddings providers | `${CLAUDE_PLUGIN_ROOT}/references/rag-embeddings.md` |
| Docker Compose setup | `${CLAUDE_PLUGIN_ROOT}/references/rag-docker.md` |
| Agent file search config | `${CLAUDE_PLUGIN_ROOT}/references/rag-agent-config.md` |
| Supported file types & OCR | `${CLAUDE_PLUGIN_ROOT}/references/rag-file-types.md` |
| .env variables reference | `${CLAUDE_PLUGIN_ROOT}/references/env-reference.md` |
| Known errors and fixes | `${CLAUDE_PLUGIN_ROOT}/references/common-errors.md` |

## Templates

Ready-to-use config files:

| Template | Use when |
|----------|----------|
| `${CLAUDE_PLUGIN_ROOT}/templates/docker-compose-rag.yaml` | Adding RAG services to Docker Compose |
| `${CLAUDE_PLUGIN_ROOT}/templates/rag-env-vars.template` | Setting up .env variables for RAG |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them:

1. **OpenAI embeddings + EU compliance/data residency** → Only fire this trigger if `EMBEDDINGS_PROVIDER=openai` AND `RAG_OPENAI_BASEURL` is either unset or points to `api.openai.com`. If `RAG_OPENAI_BASEURL` points to a non-OpenAI endpoint (e.g., `api.mistral.ai`, `api.together.xyz`), the data goes to that provider, not OpenAI — do NOT warn about OpenAI data residency. When the trigger does fire: "OpenAI embeddings send document text to OpenAI's API for processing. If you have data residency requirements (GDPR, institutional policy), consider using Ollama with a local embeddings model like `nomic-embed-text` instead — no data leaves your server."

2. **Missing `RAG_API_URL` in .env** → "Without `RAG_API_URL`, file uploads will fail silently. Set it to `http://host.docker.internal:8000` (Docker) or `http://localhost:8000` (local install)."

3. **Very high `fileTokenLimit` (>200000)** → "A fileTokenLimit above 200,000 means each uploaded file can inject up to 200K tokens into context. This significantly increases API costs per message. Consider whether RAG file search (which returns only relevant chunks) would be more cost-effective."

4. **Embeddings provider mismatch after switch** → "You changed the embeddings provider but existing files were indexed with the previous provider's vectors. These vectors are now incompatible. Re-index all files: delete the PGVector volume (`docker compose down -v` then `docker compose up -d`) and re-upload files."

## Output Format

Every RAG configuration you produce MUST include all four parts:

1. **Config changes** — exact .env variables and/or YAML, copy-pasteable
2. **Docker changes** — any docker-compose.override.yml additions
3. **Restart command** — how to apply changes
4. **Verification** — how to confirm RAG is working

**Example output:**

**Add to `.env`:**
```env
RAG_API_URL=http://host.docker.internal:8000
EMBEDDINGS_PROVIDER=ollama
EMBEDDINGS_MODEL=nomic-embed-text
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

**Add to `docker-compose.override.yml`:**
```yaml
services:
  rag_api:
    image: registry.librechat.ai/danny-avila/librechat-rag-api-dev:latest
```

**Apply changes:**
```bash
ollama pull nomic-embed-text
docker compose down && docker compose up -d
```

**Verify:**
1. Check RAG API is running: `docker compose ps` — rag_api should show "Up"
2. Open LibreChat → start a conversation → upload a PDF
3. Ask a question about the PDF content → should get a relevant answer

## When to Use This Skill vs Others

- **rag vs config:** Setting up the RAG pipeline (embeddings, PGVector, RAG API) → use rag. Editing `librechat.yaml` top-level settings (endpoints, modelSpecs) → use config (librechat-core).
- **rag vs tools:** Setting up document chat / file search → use rag. Enabling code interpreter, web search, or image gen → use tools.
- **rag vs agents:** Configuring the RAG backend → use rag. Designing an agent's prompt and enabling file search on it → use agents (librechat-core) after RAG is set up.
- **rag vs troubleshooting:** RAG-specific errors (indexing, embeddings, retrieval) → use rag. General LibreChat errors (container crashes, API failures) → use troubleshooting (librechat-core).

## Related Skills

**Same plugin (librechat-data):**
- **tools**: For configuring agent capabilities like code interpreter, web search, image gen. NOT for file search/RAG.

**Other plugins:**
- **config** (librechat-core): For YAML configuration (endpoints, modelSpecs, interface). NOT for RAG setup.
- **agents** (librechat-core): For agent prompt design and sharing. Use AFTER RAG is set up to enable file search on specific agents.
- **troubleshooting** (librechat-core): For general error diagnosis. NOT for RAG-specific issues.
- **deployment** (librechat-ops): For Docker Compose and infrastructure. Install: `/plugin install librechat-ops@librechat-skills`
