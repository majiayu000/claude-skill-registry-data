---
name: gemini-research
description: Delegates research to Google Gemini. Use when user says "이거 좀 찾아봐", "Gemini한테 물어봐", "문서 검색해줘", "best practice 알려줘", "리서치해줘", "최신 정보 찾아줘", or needs web search, documentation lookup.
---

# Gemini Research

Delegate research and information gathering to Google Gemini.

## When to Use

- Documentation lookup
- Best practices research
- Technology comparisons
- API documentation search
- General knowledge queries
- Current events or recent updates

## How to Use

```bash
.claude/scripts/gemini-wrapper.sh "your research query"
```

### With specific model:
```bash
.claude/scripts/gemini-wrapper.sh "query" gemini-3-pro
```

## Available Models

| Model | Best For |
|-------|----------|
| `gemini-3-flash` | Fast responses (default) |
| `gemini-3-pro` | Complex research |
| `gemini-2.5-pro` | Detailed analysis |
| `gemini-2.5-flash` | Quick lookups |

## Prerequisites

Requires `GOOGLE_API_KEY` environment variable.

## Example Workflow

1. User asks: "What's the best practice for Kubernetes ingress in 2025?"
2. Run gemini-wrapper with the query
3. Summarize findings with sources
