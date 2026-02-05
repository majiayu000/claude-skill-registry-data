---
name: Cite-Assist Research
description: Semantic search across Zotero library using cite-assist v3 API for academic research
version: 1.0.0
---

# Cite-Assist Research Skill

**Domain:** Academic research and citation retrieval
**Version:** 1.0.0
**Last Updated:** 2025-12-15

## Overview

Cite-assist provides semantic search across a Zotero library with ~224 documents and ~41k text chunks. It uses ModernBERT-large embeddings with MPS GPU acceleration for fast, accurate retrieval of relevant passages and document summaries.

## API Endpoint

```
POST http://localhost:8000/api/v3/search
```

## Request Format

```json
{
  "query": "prosecutorial discretion",
  "library_id": 5673253,
  "max_results": 10,
  "min_score": 0.3,
  "output_mode": "auto",
  "weights": {"chunk": 0.8, "summary": 0.2}
}
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | - | Natural language search text |
| `library_id` | Yes | 5673253 | Zotero library ID |
| `max_results` | No | 10 | Maximum results to return (1-50) |
| `min_score` | No | 0.3 | Minimum similarity threshold (0.0-1.0) |
| `output_mode` | No | `auto` | Result format (see Output Modes) |
| `weights` | No | `{chunk: 0.8, summary: 0.2}` | Score weighting between chunk and summary matches |

## Output Modes

| Mode | Returns | Best For |
|------|---------|----------|
| `auto` | Chunks OR summaries (whichever scores higher) | General research, exploratory searches |
| `chunks` | Only text chunks with context | Finding quotable passages, specific evidence |
| `summaries` | Only document summaries | Document-level matching, literature review |
| `both` | Both chunk + summary per result | Comprehensive research, need context + evidence |

### Mode Selection Guide

**Use `auto` when:**
- Starting research on a new topic
- Unsure whether you need passages or document overviews
- Want the system to optimize for relevance

**Use `chunks` when:**
- Need specific quotable passages
- Looking for particular arguments or evidence
- Building support for a specific claim

**Use `summaries` when:**
- Conducting literature review
- Need to understand what documents cover a topic
- Looking for documents to read in full

**Use `both` when:**
- Need comprehensive research results
- Want to see both the specific passage and document context
- Evaluating multiple sources for depth

## Response Format

```json
{
  "results": [
    {
      "id": "SCC7P3FV",
      "title": "Progressive Prosecution",
      "result_type": "chunk",
      "score": 0.85,
      "chunk_text": "Prosecutorial discretion allows...",
      "chunk_index": 5,
      "summary": "This article examines...",
      "chunk_score": 0.85,
      "summary_score": 0.60
    }
  ]
}
```

### Response Fields by Mode

| Field | `auto` | `chunks` | `summaries` | `both` |
|-------|--------|----------|-------------|--------|
| `id` | Yes | Yes | Yes | Yes |
| `title` | Yes | Yes | Yes | Yes |
| `result_type` | Yes | "chunk" | "summary" | "both" |
| `score` | Yes | Yes | Yes | Yes |
| `chunk_text` | Maybe | Yes | No | Yes |
| `chunk_index` | Maybe | Yes | No | Yes |
| `summary` | Maybe | No | Yes | Yes |
| `chunk_score` | Maybe | Yes | No | Yes |
| `summary_score` | Maybe | No | Yes | Yes |

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Mean response time | ~372ms |
| Embedding generation | ~200-300ms (MPS GPU) |
| Qdrant search | ~100ms |
| First request warmup | 2-3s (model loading) |

## Research Workflow

### 1. Exploratory Search

Start broad with `auto` mode to understand what's available:

```json
{
  "query": "criminal justice reform",
  "output_mode": "auto",
  "max_results": 15
}
```

### 2. Targeted Evidence Search

Narrow to specific passages with `chunks` mode:

```json
{
  "query": "prosecutorial discretion reduces racial disparities",
  "output_mode": "chunks",
  "min_score": 0.5,
  "max_results": 10
}
```

### 3. Literature Review

Use `summaries` mode to map the field:

```json
{
  "query": "progressive prosecution movement",
  "output_mode": "summaries",
  "max_results": 20
}
```

### 4. Comprehensive Research

Use `both` mode for thorough analysis:

```json
{
  "query": "plea bargaining coercion",
  "output_mode": "both",
  "max_results": 10
}
```

## Adjusting Weights

The `weights` parameter controls how chunk vs. summary scores contribute to final ranking:

```json
{
  "weights": {"chunk": 0.8, "summary": 0.2}
}
```

**High chunk weight (default):** Prioritizes specific passage matches
**High summary weight:** Prioritizes document-level relevance

Adjust for your research needs:
- `{"chunk": 1.0, "summary": 0.0}` - Pure passage search
- `{"chunk": 0.5, "summary": 0.5}` - Balanced search
- `{"chunk": 0.2, "summary": 0.8}` - Document-focused search

## Integration with Bluebook

After retrieving sources, format citations using the Academic Bluebook skill:

```
See `.claude/skills/academic-bluebook/SKILL.md` for citation formatting rules.
```

Key integration points:
- Use document `title` for article titles (italicize in academic format)
- Use `id` (Zotero key) to retrieve full metadata if needed
- Apply appropriate signals based on how source supports your argument

## Collections Reference

| Collection | Contents | Use |
|------------|----------|-----|
| `text_chunks` | ~41k semantic chunks | Passage search |
| `document_sync_status` | 224 documents + summaries | Document search |

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Connection refused | cite-assist server not running | Start server on port 8000 |
| Empty results | Query too specific or min_score too high | Broaden query, lower min_score |
| Timeout | First request loading model | Wait for warmup, retry |

## Available Workflows

- `workflows/exploratory-search.md` - Initial research on a topic
- `workflows/evidence-gathering.md` - Finding supporting passages
- `workflows/literature-review.md` - Mapping sources on a topic

---

*Cite-assist enables semantic research across your academic library.*
