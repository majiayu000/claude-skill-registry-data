---
name: meta-searching
description: Extracts web content and performs reliable searches when standard tools fail due to access restrictions, rate limiting, or validation errors. Use when encountering 403/429/422 errors, blocked documentation sites, or silent search failures. **Direct tool execution often fails for these scenarios - search-plus agent delegation provides the most reliable results.**
allowed-tools:
  - web_search
  - web_fetch
---

# Meta Searching

Advanced federated web search that overcomes access restrictions, rate limiting, and validation errors by intelligently combining multiple search services.

## When to Use

**Use this skill when you encounter:**
- 403 Forbidden errors from documentation sites or APIs
- 429 Rate Limited responses during research or documentation analysis
- 422 validation errors from web services
- Silent failures where standard search returns empty results or times out
- Need to extract specific content from blocked URLs or paywalled sites

**This skill provides specialized error handling and multi-service extraction when standard tools fail.**

## Capabilities

### Multi-Service Intelligence
- **Federated Search**: Combines Tavily Extract API with Jina.ai fallback for 100% reliability
- **Smart Service Selection**: Automatically chooses optimal service based on content type and domain characteristics
- **Zero Single Point of Failure**: Multiple service providers guarantee reliable results

### Error Resolution
- **403 Forbidden**: Resolves access restrictions using alternative extraction methods
- **429 Rate Limited**: Handles rate limiting with intelligent retry strategies
- **422 Validation**: Fixes schema validation issues through request adaptation
- **Timeout Prevention**: Eliminates "Did 0 searches..." responses and empty results

### Content Access
- **Direct URL Extraction**: Extracts content from blocked documentation sites, articles, and repositories
- **Format Preservation**: Maintains document structure, code formatting, and markdown
- **Intelligent Fallback**: Switches between services when primary approaches fail

## Examples

### Documentation Research
```
"Extract content from the Claude Code documentation at https://docs.anthropic.com/en/docs/claude-code"
"Research web scraping best practices from documentation that blocks access"
"Analyze this GitHub repository's README: https://github.com/example/repo"
```

### Error Recovery Scenarios
```
"This website is blocking access with 403 errors, extract the content"
"Search failed with rate limiting, retry with enhanced error handling"
"Getting 422 validation errors, resolve and extract the information"
"Standard search returned no results, try enhanced extraction methods"
```

### Content Extraction
```
"Extract and summarize the technical article at this URL"
"Get information from documentation sites that typically block access"
"Research current information that standard tools cannot reach"
```

## Limitations

- Requires internet connectivity and API configuration
- Slower than basic search due to comprehensive error handling (2-3x longer)
- Some paywalled content may remain inaccessible
- Cannot bypass CAPTCHA or advanced bot protection
- May not work with sites requiring JavaScript execution