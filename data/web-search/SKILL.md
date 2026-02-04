---
name: web-search
description: Lightweight web search using DuckDuckGo HTML and curl. No browser dependencies, works on Raspberry Pi.
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"]}}}
---

# Web Search Skill

## Role
You are a **Web Search Assistant**. Use this skill when the user wants to search the web and get content from the results.

## When to Use

**USE THIS SKILL** when the user asks you to:
- Search the web or internet
- Find information online
- Look up documentation, tutorials, or guides
- Research a topic

**DO NOT USE** for local file search or when the user has the information already.

## Installation

The tool is already installed at `/home/srose/clawdbot/skills/web-search/`

```bash
cd /home/srose/clawdbot/skills/web-search
npm install  # Already done
```

## Usage

### Basic Search
```bash
web-search -q "your search query"
```

### With Content Fetching
```bash
web-search -q "TypeScript tutorial" --fetch --max-results 3
```

### Options
| Option | Description |
|--------|-------------|
| `-q, --query` | Search query (required) |
| `--max-results` | Number of results (default: 5) |
| `--fetch` | Fetch full page content for each result |

### Examples

```
You: Search for React TypeScript tutorials
Bot: web-search -q "React TypeScript tutorial"

You: Get detailed content from results
Bot: web-search -q "Rust async programming" --fetch --max-results 3

You: Quick answer lookup
Bot: web-search -q "how to install Docker on Raspberry Pi"
```

## Output Format

**Search only:**
```json
{
  "query": "your search",
  "results": [
    { "title": "Result Title", "url": "https://...", "snippet": "..." }
  ]
}
```

**With --fetch:**
```json
{
  "query": "your search",
  "results": [
    { 
      "title": "Result Title", 
      "url": "https://...",
      "snippet": "...",
      "content": "Full page content (truncated to ~1500 chars)..."
    }
  ]
}
```

## Notes
- Uses DuckDuckGo HTML (no API key needed)
- Lightweight: uses native `fetch` + `cheerio` parser
- No headless browser = very low memory footprint
- Works on Raspberry Pi (arm64) without issues
- ~1-2 seconds per search
- 10 second timeout for fetching page content
