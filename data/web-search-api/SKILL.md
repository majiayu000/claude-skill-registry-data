---
name: web-search-api
description: Search the web and extract content using WebSearchAPI.ai. Use when needing real-time web data, current information, news, research, or when asked to search the internet. Supports web search, content extraction, and web scraping with advanced filtering options.
---
 
# Web Search API Skill
 
This skill enables real-time web search and content extraction using WebSearchAPI.ai, providing Google-quality results optimized for AI applications.

## API Key

API key for websearchapi.ai is stored in .env file in the format of,
WEBSEARCHAPI_KEY=api-key-value

Before execute curl or python scripts for search and extract, you need to read the API key from the .env file and setup it as environment variable by shell command

export WEBSEARCHAPI_KEY=api-key-value

and report to stdout that the WEBSEARCHAPI_KEY is loaded from .env file and setup as environment variable.
 
## Curl command for web search and context extraction
 
Basic Web Search - use the following curl command:
curl -X POST "https://api.websearchapi.ai/v1/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WEBSEARCHAPI_KEY" \
  -d '{"query": "YOUR_SEARCH_QUERY", "num_results": 10}'
 
Advanced Options:
- Geographic filtering: Add "country": "US", "language": "en"
- Time filtering: Add "freshness": "day|week|month|year"
- Full content: Add "include_content": true
 
Content Extraction:
curl -X POST "https://api.websearchapi.ai/v1/extract" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $WEBSEARCHAPI_KEY" \
  -d '{"url": "https://example.com", "output_format": "markdown"}'

### Report curl and python scripts execution

You need to report the status of the skill invocation to stdout.
- Report 'Start executing {cli-command} for {purpose}' before invoking curl or python scripts
- Report '{cli-command} execution done' after curl or python script execution finished

cli-command is the curl or python scripts in this skill you invoked and purpose is search or extract.

Report example for curl command,
```curl
Start executing curl for search
```

Report example for python script,
```python
Start executing python extract.py for context extraction
```
 
## Tips:
1. Use specific queries for better results
2. Limit results to what you need
3. Use freshness filters for time-sensitive info
4. Always check response status codes