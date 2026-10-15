---
name: rag-patterns
description: >
  RAG architecture patterns and optimization. Chunking strategies, embedding selection,
  retrieval tuning, multimodal RAG, agentic RAG, and memory systems. Use when building
  knowledge retrieval systems, agent memory, or optimizing LLM context usage.
---

# RAG Patterns

Use this skill to design, review, or optimize Retrieval-Augmented Generation systems, document Q&A, knowledge retrieval, agent memory, multimodal retrieval, and LLM context usage.

## Invocation Triggers

- User asks for RAG architecture, chunking, embeddings, retrieval, reranking, vector databases, evaluation, or memory design.
- User is building document Q&A, agent memory, multimodal document processing, or retrieval tuning.
- User wants to reduce context usage through retrieval, caching, or memory patterns.

## Core Workflow

1. Clarify data shape, query types, freshness needs, latency/cost limits, and quality bar.
2. Choose architecture tier: naive, advanced, agentic, or multimodal.
3. Select chunking strategy and metadata model.
4. Select embeddings and storage.
5. Design retrieval: vector, keyword, hybrid, query expansion, reranking, or routing.
6. Add memory, cache, and multimodal handling only when the use case needs them.
7. Define evaluation metrics and feedback loop.

## Architecture Tiers

| Tier | Shape | Use When |
|---|---|---|
| Naive RAG | Query -> embed -> vector search -> top-k -> LLM | Prototype or small corpus |
| Advanced RAG | Query rewrite -> hybrid search -> rerank -> LLM | Production text retrieval |
| Agentic RAG | Router chooses search, SQL, APIs, tools | Complex questions and multi-source tasks |
| Multimodal RAG | Parse text, tables, images, diagrams | PDFs, slides, charts, mixed media |

## Design Rules

- Use recursive or document-aware chunking for structured docs.
- Use parent-child retrieval when small chunks need larger context at generation time.
- Use hybrid search when keyword precision and semantic recall both matter.
- Use reranking when top-k quality is more important than latency.
- Match embedding model to language, context length, cost, and storage limits.
- Prefer evaluation with faithfulness, context relevance, answer relevance, recall, and precision.
- Avoid adding agents, multimodal parsing, or cache layers unless the failure mode justifies the complexity.

## Safety and Quality Constraints

- Do not claim benchmark results without measured evidence.
- Do not store secrets, credentials, personal data, private files, or sensitive documents in vector stores or memory without explicit approval and a retention plan.
- Call out data freshness, access control, source attribution, and hallucination risk.
- Separate public examples from private corpus details.
- When using external APIs or managed vector databases, keep credentials in environment variables and avoid logging query payloads with sensitive content.

## Output Expectations

- Architecture recommendation with tier, retrieval strategy, storage choice, and tradeoffs.
- Chunking and metadata plan.
- Embedding and vector database recommendation.
- Retrieval pipeline or pseudocode when useful.
- Evaluation plan and metrics.
- Known risks, follow-up tests, and rollout steps.

## Reference Map

| Need | Read |
|---|---|
| Architecture tiers, chunking strategies, parent-child pattern | [architecture-and-chunking.md](references/architecture-and-chunking.md) |
| Embedding selection, hybrid search, query expansion, reranking | [embeddings-and-retrieval.md](references/embeddings-and-retrieval.md) |
| Multimodal RAG, agent memory, memory MCP, LLM caching | [multimodal-memory-and-caching.md](references/multimodal-memory-and-caching.md) |
| Vector database selection, evaluation metrics, cross-references | [vector-db-and-evaluation.md](references/vector-db-and-evaluation.md) |
