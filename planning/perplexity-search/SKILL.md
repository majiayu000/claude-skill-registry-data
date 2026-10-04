---
name: perplexity-search
description: Strategy guide for Perplexity MCP tools (perplexity_search, perplexity_ask, perplexity_reason, perplexity_research). Helps pick the right tool, craft queries, and use recency/domain filters. Reference when planning complex searches, literature reviews, or multi-step research — not needed for simple one-shot queries.
---

# Perplexity Search Strategy Guide

This skill guides optimal use of the four Perplexity MCP tools. It does NOT provide search capability itself — the `perplexity` MCP server (package: `@perplexity-ai/mcp-server`) provides the actual tools.

> **MCP server name:** `perplexity` → tools appear as `mcp__perplexity__perplexity_search`, etc.

## Tool Selection

You have four Perplexity tools. Pick the right one:

| Tool                  | Use When                                          | Speed       | Cost    |
| --------------------- | ------------------------------------------------- | ----------- | ------- |
| `perplexity_search`   | Finding URLs, checking news, discovering sources  | Fast        | Lowest  |
| `perplexity_ask`      | Quick factual questions, summaries, explanations  | Fast        | Low     |
| `perplexity_reason`   | Complex analysis, comparisons, step-by-step logic | Medium      | Medium  |
| `perplexity_research` | Deep literature reviews, comprehensive overviews  | Slow (30s+) | Highest |

### Decision Flow

```
Need specific URLs or source discovery?
  → perplexity_search

Quick factual answer or summary?
  → perplexity_ask

Needs step-by-step reasoning or comparison?
  → perplexity_reason

Needs deep multi-source synthesis (and time isn't critical)?
  → perplexity_research
```

**Default to `perplexity_ask`** — it handles 80% of queries well. Only escalate when you genuinely need reasoning or deep research.

## Tool Parameters

### perplexity_search

Returns ranked results (title, URL, snippet, date) — no AI synthesis.

- `query` (required): Search query string
- `max_results`: 1-20 (default: 10)
- `max_tokens_per_page`: 256-2048 (default: 1024) — tokens to extract per page
- `country`: ISO country code for regional results

### perplexity_ask

AI-generated answer with citations. Fastest AI tool.

- `messages` (required): Conversation messages array
- `search_recency_filter`: `hour` | `day` | `week` | `month` | `year`
- `search_domain_filter`: Restrict to specific domains, prefix `-` to exclude
- `search_context_size`: `low` (default, fastest) | `medium` | `high`

### perplexity_reason

Step-by-step reasoning with web grounding.

- `messages` (required): Conversation messages array
- `search_recency_filter`: Same as ask
- `search_domain_filter`: Same as ask
- `search_context_size`: Same as ask
- `strip_thinking`: Remove `<think>` tags from response (saves context tokens)

### perplexity_research

Deep multi-source research. **30+ seconds per query.**

- `messages` (required): Conversation messages array
- `reasoning_effort`: `minimal` | `low` | `medium` | `high`
- `strip_thinking`: Remove `<think>` tags from response

## Query Crafting

### Structure Every Query

Good queries have four components:

1. **Topic**: Main subject
2. **Scope**: Specific aspect
3. **Context**: Time frame, domain, constraints
4. **Output**: What kind of answer you need

**Bad**: "Tell me about cancer treatment"
**Good**: "What are the latest clinical trial results for CAR-T cell therapy in treating B-cell lymphoma published in 2024-2025?"

### Use Recency Filters

The `search_recency_filter` parameter is powerful — use it:

- Breaking news → `hour`
- Today's developments → `day`
- This week's updates → `week`
- Recent research → `month` or `year`

### Use Domain Filters

Restrict to authoritative sources with `search_domain_filter`:

- Scientific: `["arxiv.org", "pubmed.ncbi.nlm.nih.gov", "nature.com", "science.org"]`
- Technical: `["github.com", "stackoverflow.com", "docs.python.org"]`
- News: `["reuters.com", "apnews.com"]`
- Exclude noise: `["-reddit.com", "-quora.com"]`

### Use search_context_size Strategically

- `low` (default): Fast, good enough for most queries
- `medium`: When initial results seem thin
- `high`: For comprehensive topics where you need broad coverage

## Domain-Specific Patterns

### Scientific Literature

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What does recent research say about the role of gut microbiome in Parkinson's disease? Focus on peer-reviewed studies with specific bacterial species identified."
    }
  ],
  "search_recency_filter": "year",
  "search_domain_filter": ["pubmed.ncbi.nlm.nih.gov", "nature.com", "cell.com", "science.org"],
  "search_context_size": "high"
}
```

Use precise terminology: "randomized controlled trial" not "study", "meta-analysis" not "review", specific gene/protein names not general descriptions.

### Technical Documentation

```json
{
  "messages": [
    {
      "role": "user",
      "content": "How to implement real-time data streaming from Kafka to PostgreSQL using Python with backpressure handling and exactly-once semantics?"
    }
  ],
  "search_domain_filter": ["docs.confluent.io", "github.com", "stackoverflow.com"]
}
```

Include framework versions, specific APIs, and implementation constraints.

### Current Events / News

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What was announced regarding AI regulation at the EU parliament this week?"
    }
  ],
  "search_recency_filter": "week",
  "search_context_size": "medium"
}
```

### Comparative Analysis

Use `perplexity_reason` for comparisons — it shows its thinking:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Compare PyTorch versus TensorFlow for implementing transformer models in terms of ease of use, performance, and ecosystem support. Include benchmarks from recent studies."
    }
  ],
  "search_context_size": "high",
  "strip_thinking": true
}
```

### Deep Research

Use `perplexity_research` only when you need comprehensive multi-source synthesis:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Conduct a comprehensive analysis of competing CAR-T cell therapy approaches including mechanism differences, clinical outcomes, cost-effectiveness, and manufacturing challenges."
    }
  ],
  "reasoning_effort": "high"
}
```

## Common Mistakes

| Mistake                                          | Fix                                                 |
| ------------------------------------------------ | --------------------------------------------------- |
| Using `perplexity_research` for simple facts     | Use `perplexity_ask` — 10x faster, much cheaper     |
| Vague queries ("tell me about AI")               | Be specific: topic + scope + context + output       |
| Not using recency filters                        | Add `search_recency_filter` when freshness matters  |
| Not using domain filters                         | Restrict to authoritative sources for quality       |
| Asking multiple unrelated questions in one query | One focused question per tool call                  |
| Using `search_context_size: high` by default     | Start with `low`, escalate only if results are thin |
| Forgetting `strip_thinking` on reason/research   | Set `true` to save context window tokens            |

## Iterative Search Workflow

For comprehensive research, chain tools:

1. **Discover** (`perplexity_search`): Find key sources and URLs
2. **Summarize** (`perplexity_ask`): Get overview from those sources
3. **Analyze** (`perplexity_reason`): Compare approaches or reason through findings
4. **Deep dive** (`perplexity_research`): Only if steps 1-3 leave gaps

Don't jump to `perplexity_research` first — build understanding incrementally.

## Reference

See `references/search_strategies.md` for detailed query templates by domain (biomedical, computational, clinical, chemistry).
