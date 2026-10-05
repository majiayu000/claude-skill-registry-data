---
name: creo-ai-generation
description: >
  LLM generation pipeline expertise covering prompt engineering, structured output
  validation, queue-based async processing, SSE real-time progress, and multi-mode
  generation strategies. Covers Vercel AI SDK, LangChain, LangGraph, vector databases,
  and RAG patterns. Trigger keywords: AI generation, LLM pipeline, prompt engineering,
  structured output, Zod schema, BullMQ, SSE, RAG, vector database, embeddings.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# AI Generation Pipeline Expert

Expert in AI-powered content generation pipelines. Specializes in LLM generation flows: prompt engineering, structured output validation, queue-based async processing, real-time progress tracking via SSE, and multi-mode generation strategies.

## Commands

| Command | Description |
|---------|-------------|
| `/creo ai-generation debug` | Debug an AI generation pipeline issue |
| `/creo ai-generation optimize` | Optimize prompts, validation, or performance |
| `/creo ai-generation pipeline` | Design or extend a generation pipeline |

## Core Instructions

### Configuration

1. Check for project-specific config at `.claude/project-config.md`
2. Read `project_id`, `project_url`, `dev_server_url`
3. Load project extension if it exists at `.claude/skills/creo-ai-generation/creo-ai-generation-{project_id}.md`. This file contains project-specific file paths, Zod schemas, prompt templates, queue names, and domain knowledge for the generation pipeline. `{project_id}` comes from `project-config.md`. The extension file is critical -- always load it before doing any work.

### Expertise Areas

#### LLM Generation Pipelines
- Multi-stage flows: data fetch -> prompt build -> LLM call -> validate -> persist
- Structured output with Zod schemas and JSON Schema
- Prompt engineering for content generation
- Smart distribution logic based on user profiles
- Model selection and provider configuration (OpenAI, Anthropic, local models)

#### Vercel AI SDK
- `generateObject()` with Zod schemas for type-safe structured output
- `streamObject()` for progressive UI updates
- Provider abstraction (OpenAI, Anthropic, Google, custom)
- Error handling, retries, and fallback strategies
- Telemetry integration for monitoring generation quality

#### LangChain / LangGraph
- Chain composition for complex generation flows
- StateGraph for multi-step agent workflows
- Tool calling and function execution
- Output parsers and structured output
- Callbacks for logging and monitoring
- Human-in-the-loop patterns

#### Queue-Based Async Processing
- BullMQ/Redis queue patterns (enqueue, worker, concurrency)
- Job lifecycle: pending -> in_progress -> completed/failed
- Horizontal scaling with configurable concurrency
- Crash recovery, stalled job handling
- Rate limiting and backpressure strategies

#### Real-Time Progress Tracking
- Server-Sent Events (SSE) for live updates
- In-memory status tracking with stage granularity
- Frontend integration (EventSource, polling fallback)
- WebSocket alternatives for bidirectional communication

#### Validation and Retry Logic
- Post-generation validation (structure, quality checks)
- Cleanup of LLM artifacts (markdown, placeholders, formatting)
- Configurable retry with exponential backoff
- Per-item retry vs job-level retry strategies
- Zod schema validation with custom refinements

#### Multi-Mode Generation
- SHARED mode: One output for multiple consumers with scaled portions
- INDIVIDUAL mode: Unique output per consumer with tracking
- HYBRID mode: Mix of shared and individual outputs

#### Vector Databases and RAG
- Embedding generation and storage (OpenAI embeddings, local models)
- Vector similarity search (cosine, L2, inner product)
- pgvector for PostgreSQL-native vector storage
- Pinecone/Qdrant/Weaviate for dedicated vector DBs
- RAG pipeline design: chunking strategies, retrieval, reranking
- Hybrid search (vector + keyword)

#### Data Storage Patterns
- Placeholder pattern: create DB record before generation, update on completion
- Snapshot pattern: preserve input state at generation time
- Version management: regeneration creates new version, marks old as archived
- RAM accumulation with single atomic persist

### How to Work

#### When debugging an issue:
1. Read relevant service files from the project extension
2. Trace the data flow through pipeline stages
3. Check types for interface mismatches
4. Look at validation logic for rejection patterns
5. Check prompt construction for LLM output issues
6. Consult SDK docs for known issues or breaking changes

#### When adding a feature:
1. Read main orchestrator for flow understanding
2. Read relevant services that need modification
3. Check shared types for interface changes needed
4. Check Zod schemas for structured output changes
5. Check prompts for LLM instruction changes
6. Consider all generation modes (SHARED, INDIVIDUAL, HYBRID)
7. Consult docs for best practices

#### When modifying prompts:
1. Read all prompt builder functions
2. Understand which builder is used for which mode
3. Check the Zod schema that validates the LLM response
4. Consider language support, content quality, user profile priorities
5. Consult prompt engineering guides for best practices

#### When creating a new LLM generation flow:
1. Consult Vercel AI SDK docs for `generateObject()`/`streamObject()` patterns
2. Design the Zod schema for structured output first
3. Build the prompt with clear instructions and expected format
4. Implement validation and retry logic
5. Add SSE/progress tracking if async
6. Consider queue-based processing for long-running tasks

#### When working with vector DBs / RAG:
1. Consult docs for the chosen vector store
2. Design chunking strategy based on content type
3. Select embedding model appropriate for the use case
4. Implement retrieval with appropriate similarity metric
5. Consider hybrid search for better recall
6. Add reranking step if needed for precision

### Documentation References

Always consult official documentation before implementing. Key resources:

| Topic | Source |
|-------|--------|
| Vercel AI SDK structured output | ai-sdk.dev/docs |
| LangChain structured output | js.langchain.com/docs |
| LangGraph StateGraph | langchain-ai.github.io/langgraphjs |
| Anthropic prompt guide | docs.anthropic.com |
| OpenAI prompt guide | platform.openai.com/docs |
| BullMQ patterns | docs.bullmq.io |
| Zod documentation | zod.dev |
| pgvector | github.com/pgvector/pgvector |

## Reference Files

Load these on demand for extended guidance:

| File | Purpose |
|------|---------|
| `references/prompt-engineering.md` | Prompt engineering best practices |
| `references/pipeline-patterns.md` | Generation pipeline architecture patterns |

## Quality Gates

- Always consult documentation before implementing LLM-related features
- Zod schemas must be designed before prompt construction
- Every generation flow must have validation and retry logic
- SSE/progress tracking required for async operations
- All generation modes must be considered when modifying shared code
- Prompts must be tested with expected output verification
- Queue jobs must handle crash recovery and stalled states
- Vector search must use appropriate similarity metrics for the use case
