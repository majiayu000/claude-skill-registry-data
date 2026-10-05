---
name: tavily-search
description: Provides web search capabilities using Tavily AI-optimized search API. Supports searching the web for relevant results, extracting content from URLs, crawling websites, and generating AI-powered research reports.
---

# Tavily Search

This skill provides powerful web search capabilities using the Tavily API, which is specifically optimized for AI applications.

## API Configuration

**API Key:** `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`

## Available Commands

### `/search` - Web Search
Search the web for relevant information using Tavily's LLM-optimized search API.

**Usage:**
```
/search current React best practices
/search quantum computing applications
/search latest AI agent developments
```

**What it does:**
- Returns relevant search results with content snippets
- Provides metadata about sources
- Filters for relevance and quality

### `/research` - Deep Research
Generate comprehensive AI-powered research reports on any topic.

**Usage:**
```
/research AI agent architecture and trends
/research comparison of frontend frameworks 2024
/research best practices for Python API design
```

**What it does:**
- Compiles information from multiple sources
- Provides structured JSON output
- Includes citations and references
- Supports saving reports to files

### `/extract` - Content Extraction
Extract clean content from specific URLs.

**Usage:**
```
/extract https://example.com/blog/post
/extract https://docs.example.com/guide
```

**What it does:**
- Returns webpage content in markdown/text format
- Preserves structure and formatting
- Removes ads and clutter

### `/crawl` - Website Crawling
Crawl websites and save as local markdown files.

**Usage:**
```
/crawl https://docs.example.com
/crawl https://example.com/api --save ./docs
```

**What it does:**
- Downloads entire websites as markdown
- Preserves directory structure
- Ideal for building knowledge bases

## When to Use This Skill

Use this skill when the user:
- Asks to search the web for current information
- Wants to research a topic comprehensively
- Needs to extract content from specific URLs
- Wants to crawl documentation or knowledge bases
- Asks about recent developments or trends
- Needs citations for sources

## Examples

### Example 1: Search for Current Best Practices
```
User: "What are the current React 19 best practices?"
→ /search React 19 new features best practices
```

### Example 2: Research Topic with Sources
```
User: "I need a comprehensive report on vector databases"
→ /research vector database comparisons and save to vector-db-report.json
```

### Example 3: Extract Documentation
```
User: "Can you get the content from this documentation page?"
→ /extract https://docs.example.com/guide/overview
```

### Example 4: Build Knowledge Base
```
User: "Download the React documentation as markdown"
→ /rawl https://react.dev --save ./react-docs
```

## Best Practices

1. **Be Specific**: Use detailed search queries for better results
   - Good: "React 19 server actions best practices"
   - Bad: "React stuff"

2. **Use Research for Complex Topics**: For comprehensive understanding
   - `/research` compiles multiple sources
   - Includes citations for verification

3. **Extract for Specific Content**: When you need the full content of a page
   - Better than copy-paste for formatted content
   - Preserves markdown structure

4. **Crawl for Documentation**: Build local knowledge bases
   - Great for offline documentation access
   - Preserves site structure

## API Configuration in Settings

To configure Tavily API key in Claude Code settings:

**Windows:**
```bash
notepad %USERPROFILE%\.claude\settings.json
```

**macOS/Linux:**
```bash
nano ~/.claude/settings.json
```

Add the following configuration:
```json
{
  "env": {
    "TAVILY_API_KEY": "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"
  }
}
```

## Troubleshooting

**Q: Search returns no results**
- Check API key is correctly configured
- Verify network connectivity
- Try rephrasing the search query

**Q: Rate limiting errors**
- Tavily has rate limits based on your plan
- Wait a moment before retrying
- Consider upgrading your Tavily plan

**Q: Content extraction fails**
- Ensure URL is accessible
- Check if the site blocks automated requests
- Try crawling instead of extracting

## Related Resources

- [Tavily Official Documentation](https://docs.tavily.com)
- [Tavily GitHub Repository](https://github.com/tavily-ai)
- [Tavily Skills Repository](https://github.com/tavily-ai/skills)
- [Tavily API Dashboard](https://tavily.com)
