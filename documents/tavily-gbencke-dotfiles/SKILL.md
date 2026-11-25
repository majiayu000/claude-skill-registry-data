---
name: tavily
description: Perform AI-powered web searches to find documentation, troubleshoot errors, and summarize information.
---

# Tavily Web Search

This skill provides an AI-optimized web search engine via Tavily. It excels at finding recent information, exact error solutions, and synthesizing content from multiple sources.

**Requires `TAVILY_API_KEY` to be set in your environment.**

## Available Tools

### `tavily_search(query, ...)`

Search the web and retrieve ranked results with titles, URLs, and relevant content snippets. 

*   **When to use:** 
    *   You encounter an error message you don't recognize.
    *   You need to look up documentation that isn't available in Context7 or your local files.
    *   You need to check for recent news or library updates.
*   **Key Parameters:**
    *   `query`: The search string (e.g., `pydantic v2 migration guide`).
    *   `search_depth`: Use `'basic'` (default) for speed, or `'advanced'` for a deeper crawl with richer content.
    *   `topic`: Use `'general'` (default) or `'news'` to favor recent articles.
    *   `include_answer`: Set to `true` to have Tavily's AI generate a summary answer of the results.
    *   `include_raw_content`: Set to `true` if you need the full HTML/text content of the resulting pages instead of just snippets.
    *   `include_domains` / `exclude_domains`: Filter results to specific sites (e.g., `["github.com", "stackoverflow.com"]`).

## Workflow

1. Keep queries specific. Instead of searching `python docs`, search `python 3.12 asyncio task groups`.
2. If the snippets returned by a basic search aren't enough, you can re-run the search with `include_raw_content: true` or `search_depth: 'advanced'`.
3. For finding official documentation, consider using the `include_domains` parameter to restrict results to `docs.python.org` or `developer.mozilla.org`.

## In Claude Code

Claude Code reaches Tavily through its MCP server (`claude mcp add -s user tavily -- npx -y tavily-mcp`). The server reads `TAVILY_API_KEY` from the environment. Call `mcp__tavily__tavily_search` with the same parameters. The server also offers `tavily_extract` (full text of given URLs), `tavily_crawl`, `tavily_map` and `tavily_research`.
