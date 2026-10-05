---
name: web-search
description: Advanced web search using Tavily API for current information retrieval
allowed-tools: tavily-web-search
---

# Web Search

Search the web for current information on any topic using the Tavily search API.

## When to Use

- Searching for recent news, articles, blog posts, and web content
- Finding current statistics, data, and factual information
- Retrieving information that may not be in academic papers or the knowledge base
- Verifying claims with multiple web sources

## How to Use

1. Formulate a specific, targeted search query (max 400 characters)
2. Call `tavily_web_search` with the query
3. Review returned results for relevance and quality
4. Extract key facts and note the source URL for citation

## Result Format

Results are returned in Document XML format:

```xml
<Document href="https://example.com/article" title="Article Title">
  Content excerpt from the page...
</Document>
```

## Constraints

- Maximum 5 results returned per query
- Query will be truncated to 400 characters
- Search mode: advanced (includes content extraction)
- Each call counts toward the researcher's 8-call limit per task
