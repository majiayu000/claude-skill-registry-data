---
name: "cognitive-architecture"
description: 'Design and implement the "brain" of AI agents. Use when defining agent memory strategy (short/long-term), building RAG pipelines (knowledge retrieval), or designing state management systems.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2026-02-11"
 updated: "2026-02-11"
compatibility:
 model_providers: ["azure-openai", "openai", "anthropic"]
 vector_stores: ["azure-ai-search", "cosmos-db-mongo", "qdrant", "chroma"]
---

# Cognitive Architecture

> **Purpose**: Patterns for the cognitive components of AI agents: Memory, Knowledge (RAG), and Reasoning.

---

## When to Use This Skill

- Designing **Memory Systems** (Conversation history, User profiles, Entity tracking).
- Building **RAG Pipelines** (Chunking, Embedding, Retrieval, Reranking).
- Managing **Agent State** across sessions.
- Selecting **Vector Databases** for knowledge retrieval.

## Table of Contents

1. [Cognitive Components](#cognitive-components)
2. [RAG Patterns](#rag-patterns)
3. [Memory Architectures](#memory-architectures)
4. [References](#references)

---

## Cognitive Components

A complete agent "brain" consists of three layers:

1. **Context (Short-term Memory)**: The active context window (conversation history).
2. **Knowledge (Long-term Memory/RAG)**: Static facts retrieved from vector stores or databases.
3. **State (Episodic Memory)**: Structured data about the user or task progress persisted indefinitely.

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scaffold-cognitive.py` | Scaffold RAG pipeline and/or Memory system modules | `python scaffold-cognitive.py --name my-agent --component all` |

**Options**:
- `--component rag` - RAG only (ingestion + retrieval + tests)
- `--component memory` - Memory only (short-term + long-term + tests)
- `--component all` - Both (default)
- `--vector-store azure-ai-search` - Use Azure AI Search instead of ChromaDB

---

## Reference Patterns

| Pattern | Description | File |
|---------|-------------|------|
| **RAG Pipeline** | Standard for ingesting and retrieving knowledge. | [pattern-rag-pipeline.md](pattern-rag-pipeline.md) |
| **Memory System** | Schema for short-term and long-term memory. | [pattern-memory-systems.md](pattern-memory-systems.md) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hallucinations | Increase retrieval "groundedness" threshold or reduce `top_k`. |
| Context Window Overflow | Implement "Summarization" strategy for conversation history. |
| Slow Retrieval | Use "Hybrid Search" (Keyword + Semantic) with filtered metadata. |
