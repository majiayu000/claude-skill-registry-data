---
name: context-llm-pipeline
description: RAG pipeline, embeddings, LLM interactions, and flow orchestration.
tags: [backend, ai, rag]
---

# LLM Pipeline Context

## Overview
Core AI logic including RAG flows, LLM service orchestration, and vector retrieval.

## Active Files

### Orchestration (Flows)
- `backend/flows/ingestion_flow.py` - Document ingestion
- `backend/flows/scraping_flow.py` - Scrape orchestration
- `backend/flows/template_review_flow.py` - LLM review flow

### Services
- `backend/services/llm/orchestrator.py` - Main LLM handler
- `backend/services/llm/pipeline.py` - Pipeline logic
- `backend/services/llm/analyzer.py` - Analysis logic
- `backend/services/research/zai.py` - ZAI research integration
- `backend/services/search_pipeline_service.py` - Search pipeline

### Shared Packages
- `packages/llm-common/` - Shared types and utilities (Submodule)

## Usage
Use this skill when working on RAG, prompt engineering, or vector search logic.
