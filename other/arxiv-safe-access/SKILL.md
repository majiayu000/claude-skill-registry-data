---
name: arxiv-safe-access
description: "Best practices for safely accessing arXiv programmatically, avoiding common pitfalls with HTTP, SSL, and automated tools."
---
# arxiv-safe-access

## Description
This skill encapsulates lessons learned from programmatic access to arXiv, particularly in automated workflows and cron jobs. It provides guidance on avoiding common issues such as blocked HTTP requests, SSL errors, and tool-specific failures.

## When to Use
Apply this skill when:
- Writing scripts or automation that query arXiv for papers.
- Setting up cron jobs that fetch arXiv data.
- Integrating arXiv search into agent workflows.
- Troubleshooting failed attempts to retrieve arXiv metadata or PDFs.

## Best Practices
1. **Always use HTTPS**: arXiv's API and RSS feeds are accessible via HTTPS. Never use plain HTTP as it may be blocked by security scanners or proxies.
2. **Prefer the `arxiv-search` skill**: The built-in `arxiv-search` skill (under `ai_collection/arxiv-search`) already handles many of the pitfalls and provides a reliable way to search and retrieve paper metadata.
3. **Avoid `web_search` (Firecrawl) for arXiv queries**: As documented in the `arxiv-search` skill's pitfalls, the Firecrawl backend often fails with arxiv-related queries.
4. **If using `curl` or Python HTTP clients, use HTTPS and verify certificates**: 
   - For `curl`: always use `https://` URLs.
   - For Python: consider using `httpx` or `requests` with proper SSL context, but be aware of potential proxy-related SSL issues (see the `arxiv-search` skill's pitfalls about SSL errors).
5. **Leverage RSS feeds for recent papers**: arXiv provides category-specific RSS feeds (e.g., `https://rss.arxiv.org/rss/cs.NE`) that are simple to parse and reliable. This method avoids many API-related issues and works well for cron jobs.
6. **When in doubt, use browser automation**: The `browser_navigate` tool with HTTPS URLs is robust and avoids many programmatic access issues.
7. **Respect rate limits**: arXiv does not explicitly publish rate limits, but be courteous and avoid excessive requests.
8. **Combine approaches for robustness**: Consider using multiple methods (RSS for recent papers, API for specific queries) and have fallbacks in place.

## Pitfalls
- **Plain HTTP requests are blocked**: Attempts to use `http://export.arxiv.org/` may trigger security scans and result in pending approval or failure.
- **SSL errors with proxies**: Using Python's `httpx` or `requests` through certain proxies can lead to `EOF occurred in violation of protocol` errors.
- **Firecrawl incompatibility**: The `web_search` tool with Firecrawl backend is unreliable for arxiv queries.

## References
- arXiv API documentation: https://info.arxiv.org/help/api/index.html
- arXiv RSS feeds: https://arxiv.org/rss
- `arxiv-search` skill: `skill_view(name='ai_collection/arxiv-search')`

## Example Workflow
See the `scripts/fetch_arxiv_recent.py` for an example of how to fetch recent papers from an RSS feed and filter by keywords.