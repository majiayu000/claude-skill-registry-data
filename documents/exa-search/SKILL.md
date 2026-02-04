---
name: exa-search
description: Real-time web search using Exa AI. Use when you need current information, fact-checking, researching unfamiliar topics, or finding documentation. Triggers on requests mentioning search, lookup, find online, current information, or research.
---

# Exa Web Search

Search the web for current information using the Exa AI search engine.

## When to Use

- Need information beyond training data cutoff
- Fact-checking claims or statistics
- Researching unfamiliar topics
- Finding official documentation or sources
- Getting current news or recent developments

## Quick Start

Use the `mcp__exa__web_search` tool:

```python
# Basic search
result = mcp__exa__web_search(query="TypeScript 5.0 new features")

# With more results
result = mcp__exa__web_search(query="MCP protocol specification", numResults=10)
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query |
| `numResults` | number | No | 5 | Number of results to return |

## Response Format

Returns search results with:
- `title` - Page title
- `url` - Source URL
- `snippet` - Text excerpt
- `content` - Full page content (when available)

## Examples

### Research a topic
```
Search for: "latest React 19 features and changes"
```

### Find documentation
```
Search for: "Anthropic Claude API authentication docs"
```

### Fact check
```
Search for: "current TypeScript version 2025"
```

## Best Practices

1. **Be specific** - Include relevant keywords and context
2. **Use quotes** - For exact phrases: `"error message text"`
3. **Add context** - Include technology/domain: `Python asyncio tutorial`
4. **Limit results** - Use 3-5 for quick lookups, 10+ for research
