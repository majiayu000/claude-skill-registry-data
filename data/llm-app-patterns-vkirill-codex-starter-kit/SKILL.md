---
name: llm-app-patterns
description: Production-ready patterns for building LLM applications. Covers RAG pipelines, agent architectures, prompt IDEs, and LLMOps monitoring. Use when designing AI applications, implementing
  RAG, building agents, or setting up LLM observability.
stacks:
  - llm-api
packages:
  - openai
tags:
  - llm
  - ai
---

# LLM Application Patterns

## Use this skill when

- Designing LLM-powered applications
- Implementing RAG (Retrieval-Augmented Generation)
- Building AI agents with tools
- Setting up LLMOps monitoring and observability
- Choosing between agent architectures
- Implementing caching, rate limiting, and fallback strategies for LLM APIs

## Do not use this skill when

- You are using the LangChain framework specifically — use `langchain-architecture`
- You are building with the Anthropic SDK only — use `autonomous-agent-patterns`
- The task is about fine-tuning or training models — this skill covers inference patterns only

## Instructions

1. Clarify goals, constraints, and required inputs.
2. Apply relevant best practices and validate outcomes.
3. Provide actionable steps and verification.

## Capabilities

### RAG Pipeline Architecture

RAG (Retrieval-Augmented Generation) grounds LLM responses in your data. The pipeline has three phases: ingestion, retrieval, and generation.

**Ingestion phase**: load documents from sources, chunk them, embed each chunk, store embeddings in a vector database. Chunking strategies: fixed-size (simple, may break context), semantic (preserves meaning by splitting on paragraphs/sections), recursive (tries multiple separators: `\n\n`, `\n`, `. `, ` `), document-aware (respects structural elements like headers). Recommended settings: chunk size 512 tokens, 50-token overlap.

**Vector database selection**: Pinecone (managed, billions of vectors, hybrid search), Weaviate (self-hosted, multi-modal, GraphQL API), Chroma (development/prototyping, simple API), pgvector (existing PostgreSQL, SQL integration, ACID compliance).

**Embedding model selection**: OpenAI text-embedding-3-small (1536d, $0.02/1M tokens, good for most use cases), text-embedding-3-large (3072d, $0.13/1M tokens, best for complex queries), local BGE-large (1024d, free compute, comparable to OpenAI small).

**Retrieval strategies** in order of sophistication:
1. Semantic search — embed query, find nearest vectors
2. Hybrid search — combine semantic and BM25 keyword results via Reciprocal Rank Fusion; `alpha=1.0` is pure semantic, `alpha=0.0` is pure keyword, `alpha=0.5` is balanced
3. Multi-query retrieval — generate N query variations, retrieve for each, deduplicate
4. Contextual compression — retrieve broadly, then extract only relevant portions with an LLM

**Generation**: inject retrieved context into the prompt alongside the user question. The prompt must instruct the LLM to answer only from the provided context and acknowledge when context is insufficient.

### Agent Architectures

**ReAct Pattern (Reasoning + Acting)**: the LLM interleaves Thought → Action → Observation steps in a loop until it reaches a Final Answer. Implemented as an inference loop: parse the LLM output for action calls, execute the tool, append the observation, repeat up to `max_iterations`. Works with any LLM that can follow the format.

**Function Calling Pattern**: the LLM selects tools via the model's native function calling API. Tools are described as JSON schemas with name, description, and parameters. The loop continues while the response contains `tool_calls`; when the model returns content without tool calls the task is complete. More reliable than ReAct for structured tool schemas; requires a function-calling-capable model.

**Plan-and-Execute Pattern**: a planner LLM creates a step-by-step plan upfront, then an executor LLM implements each step. After each step, the agent checks whether replanning is needed based on accumulated results. Good for complex, multi-stage tasks where upfront decomposition is valuable. Higher cost due to multiple LLM calls per task.

**Multi-Agent Collaboration**: specialized agents (researcher, analyst, writer, critic) work in parallel on sub-tasks coordinated by a coordinator agent. A critic agent reviews results and triggers revision if needed. Very high complexity and cost — only appropriate for research-grade tasks where quality outweighs efficiency.

**Architecture decision matrix**:

| Pattern | Use When | Complexity | Cost |
|---------|----------|------------|------|
| Simple RAG | FAQ, docs search | Low | Low |
| Hybrid RAG | Mixed queries | Medium | Medium |
| ReAct Agent | Multi-step tasks | Medium | Medium |
| Function Calling | Structured tools | Low | Low |
| Plan-Execute | Complex tasks | High | High |
| Multi-Agent | Research tasks | Very High | Very High |

### Prompt Management

**Template system**: prompts are parameterized with named variables. Templates validate that all required variables are provided at render time. Few-shot examples are prepended as formatted `Input:` / `Output:` pairs.

**Versioning and A/B testing**: store prompts in a registry with version identifiers and timestamps. Retrieve by name and version (or `latest`). A/B testing assigns users to variants deterministically via hash(user_id) modulo variant count. Record outcomes per prompt version to measure quality.

**Prompt chaining**: string multiple prompt steps together, passing `output_key` values from one step as input variables to the next. Each step can have an optional output parser to transform the raw LLM text into structured data before passing downstream.

### LLMOps and Observability

**Key metrics to track**:
- Performance: latency p50/p99, tokens per second
- Quality: user satisfaction (thumbs up/down), task completion rate, hallucination rate
- Cost: cost per request, tokens per request, cache hit rate
- Reliability: error rate, timeout rate, retry rate

**Logging**: log every request (model, truncated prompt, token counts, temperature, user_id) and every response (completion tokens, total tokens, latency, finish_reason, cost). Use structured JSON logs for easy querying.

**Distributed tracing**: use OpenTelemetry spans around each LLM call, setting attributes for prompt length, response length, and token counts. This enables end-to-end latency attribution across multi-step workflows.

**Evaluation framework**: score responses on relevance (does it answer the question?), coherence (is it well-structured?), groundedness (is it based on the provided context?), accuracy (does it match ground truth?), and safety (is it harmless?). Run benchmark suites over test cases to track quality regressions between prompt versions.

### Production Patterns

**Caching**: generate a deterministic cache key from the prompt, model, and serialized kwargs. Check the cache before calling the LLM. Only cache responses from deterministic runs (temperature=0). Store in Redis with a TTL (default 1 hour).

**Rate limiting**: maintain a sliding window of request timestamps. Before each request, evict timestamps older than 60 seconds and compare count against the RPM limit. Sleep for the remainder of the window if the limit is reached. Combine with exponential backoff retry using `tenacity` (min 4s, max 60s, up to 5 attempts) for API errors.

**Fallback strategy**: maintain a priority list of models (primary + fallbacks). Try each in sequence; on `RateLimitError` or server error (5xx), catch and continue to the next model. Raise a custom error only when all models are exhausted.

## Behavioral Traits

- Chooses the simplest pattern that meets the requirement (Simple RAG before Hybrid RAG, Function Calling before ReAct)
- Always validates LLM outputs before using them as tool inputs or displaying to users
- Implements caching for identical prompt+model combinations at temperature=0
- Monitors token usage in production to control costs
- Versions prompts to enable rollback and A/B testing
- Adds timeout and max-iteration guards to all agent loops

## Knowledge Base

- RAG ingestion: chunk → embed → store; retrieval: embed query → nearest neighbor search → inject context
- Hybrid search Reciprocal Rank Fusion: merges ranked lists from semantic and BM25 without needing score normalization
- ReAct format requires strict output parsing — fragile with weaker models; function calling is more reliable
- Plan-and-Execute reduces context length per step but adds planning cost and latency
- LLM cache key must include model name, prompt, and all generation parameters to avoid false hits
- Tenacity retry: `RateLimitError` and server errors (5xx) should retry; client errors (4xx except 429) should not
- Evaluation metrics: relevance and groundedness are the most important for RAG quality

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
