---
name: browser-content-capture
description: Capture content from JavaScript-rendered pages, login-protected sites, and multi-page documentation using Playwright MCP tools or Claude Chrome extension. Use when WebFetch fails on SPAs, dynamic content, or auth-required pages.
version: 1.1.0
tags: [browser, playwright, mcp, scraping, spa, authentication, chrome-extension, 2025]
---

# Browser Content Capture

**Capture web content that traditional scrapers cannot access.**

## Overview

This skill enables content extraction from sources that require browser-level access:
- **JavaScript-rendered SPAs** (React, Vue, Angular apps)
- **Login-protected documentation** (private wikis, gated content)
- **Dynamic content** (infinite scroll, lazy loading, client-side routing)
- **Multi-page site crawls** (documentation trees, tutorial series)

## When to Use This Skill

**Use when:**
- `WebFetch` returns empty or partial content
- Page requires JavaScript execution to render
- Content is behind authentication
- Need to navigate multi-page structures
- Extracting from client-side routed apps

**Do NOT use when:**
- Static HTML pages (use `WebFetch` - faster)
- Public API endpoints (use direct HTTP calls)
- Simple RSS/Atom feeds

---

## Quick Start

### Check Available MCP Tools

```
MCPSearch: "select:mcp__playwright__browser_navigate"
```

### Basic Capture Pattern

```python
# 1. Navigate to URL
mcp__playwright__browser_navigate(url="https://docs.example.com")

# 2. Wait for content to render
mcp__playwright__browser_wait_for(selector=".main-content", timeout=5000)

# 3. Capture page snapshot
snapshot = mcp__playwright__browser_snapshot()

# 4. Extract text content
content = mcp__playwright__browser_evaluate(
    script="document.querySelector('.main-content').innerText"
)
```

---

## MCP Tools Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `browser_navigate` | Go to URL | First step of any capture |
| `browser_snapshot` | Get DOM/accessibility tree | Understanding page structure |
| `browser_evaluate` | Run custom JS | Extract specific content |
| `browser_click` | Click elements | Navigate menus, pagination |
| `browser_fill_form` | Fill inputs | Authentication flows |
| `browser_wait_for` | Wait for selector | Dynamic content loading |
| `browser_take_screenshot` | Capture image | Visual verification |
| `browser_console_messages` | Read JS console | Debug extraction issues |
| `browser_network_requests` | Monitor XHR/fetch | Find API endpoints |

**Full tool documentation:** See [references/mcp-tools.md](references/mcp-tools.md)

---

## Capture Patterns

### Pattern 1: SPA Content Extraction

For React/Vue/Angular apps where content renders client-side:

```python
# Navigate and wait for hydration
mcp__playwright__browser_navigate(url="https://react-docs.example.com")
mcp__playwright__browser_wait_for(selector="[data-hydrated='true']", timeout=10000)

# Extract after React mounts
content = mcp__playwright__browser_evaluate(script="""
    // Wait for React to finish rendering
    await new Promise(r => setTimeout(r, 1000));
    return document.querySelector('article').innerText;
""")
```

**Details:** See [references/spa-extraction.md](references/spa-extraction.md)

### Pattern 2: Authentication Flow

For login-protected content:

```python
# Navigate to login
mcp__playwright__browser_navigate(url="https://docs.example.com/login")

# Fill credentials (prompt user for values)
mcp__playwright__browser_fill_form(
    selector="#login-form",
    values={"username": "...", "password": "..."}
)

# Click submit and wait for redirect
mcp__playwright__browser_click(selector="button[type='submit']")
mcp__playwright__browser_wait_for(selector=".dashboard", timeout=10000)

# Now navigate to protected content
mcp__playwright__browser_navigate(url="https://docs.example.com/private-docs")
```

**Details:** See [references/auth-handling.md](references/auth-handling.md)

### Pattern 3: Multi-Page Crawl

For documentation with navigation trees:

```python
# Get all page links from sidebar
links = mcp__playwright__browser_evaluate(script="""
    return Array.from(document.querySelectorAll('nav a'))
        .map(a => ({href: a.href, text: a.innerText}));
""")

# Iterate and capture each page
all_content = []
for link in links:
    mcp__playwright__browser_navigate(url=link['href'])
    mcp__playwright__browser_wait_for(selector=".content")
    content = mcp__playwright__browser_evaluate(
        script="document.querySelector('.content').innerText"
    )
    all_content.append({
        'url': link['href'],
        'title': link['text'],
        'content': content
    })
```

**Details:** See [references/multi-page-crawl.md](references/multi-page-crawl.md)

---

## Integration with RAG Systems

After capturing content, send it to your knowledge base or RAG pipeline:

```python
import httpx

async def send_to_knowledge_base(content: str, source_url: str):
    """Send captured content to vector database or RAG system."""
    async with httpx.AsyncClient() as client:
        # Example: Send to Pinecone/Weaviate/custom endpoint
        response = await client.post(
            "https://api.yourapp.com/v1/knowledge/ingest",
            json={
                "content": content,
                "source_url": source_url,
                "metadata": {
                    "capture_method": "browser_playwright",
                    "timestamp": "2025-12-29T10:00:00Z"
                }
            },
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        return response.json()

# Example usage
content = mcp__playwright__browser_evaluate(script="document.body.innerText")
result = await send_to_knowledge_base(content, "https://docs.example.com/page")
print(f"Ingested document ID: {result['document_id']}")
```

---

## Fallback Strategy

Use this decision tree for content capture:

```
User requests content from URL
         │
         ▼
    ┌─────────────┐
    │ Try WebFetch│ ← Fast, no browser needed
    └─────────────┘
         │
    Content OK? ──Yes──► Done
         │
         No (empty/partial)
         │
         ▼
    ┌──────────────────┐
    │ Check URL pattern│
    └──────────────────┘
         │
    ├─ Known SPA (react, vue, angular) ──► Playwright MCP
    ├─ Requires login ──► Chrome Extension (user session)
    └─ Dynamic content ──► Playwright MCP with wait_for
```

---

## Best Practices

### 1. Minimize Browser Usage
- Always try `WebFetch` first (10x faster, no browser overhead)
- Cache extracted content to avoid re-scraping
- Use `browser_evaluate` to extract only needed content

### 2. Handle Dynamic Content
- Always use `wait_for` after navigation
- Add delays for heavy SPAs: `await new Promise(r => setTimeout(r, 2000))`
- Check for loading spinners before extracting

### 3. Respect Rate Limits
- Add delays between page navigations
- Don't crawl faster than a human would browse
- Honor robots.txt and terms of service

### 4. Clean Extracted Content
- Remove navigation, headers, footers
- Strip ads and promotional content
- Convert to clean markdown before storing

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty content | Add `wait_for` with appropriate selector |
| Partial render | Increase timeout or add explicit delay |
| Login required | Use Chrome extension with user session |
| CAPTCHA blocking | Manual intervention required |
| Content in iframe | Use `browser_evaluate` to access iframe content |

---

## Real-World Examples

### Example 1: Capturing React Documentation

```python
# Navigate to React docs (client-side rendered)
mcp__playwright__browser_navigate(url="https://react.dev/learn")

# Wait for React to hydrate
mcp__playwright__browser_wait_for(selector="[data-react-hydrated='true']")

# Extract main article content
content = mcp__playwright__browser_evaluate(script="""
    const article = document.querySelector('article');
    return article ? article.innerText : '';
""")

# Send to knowledge base
await send_to_knowledge_base(content, "https://react.dev/learn")
```

### Example 2: Private Notion Documentation

```python
# User must be logged in via Chrome extension
# Content captures their authenticated session

mcp__playwright__browser_navigate(url="https://notion.so/private-team-docs")
mcp__playwright__browser_wait_for(selector=".notion-page-content")

content = mcp__playwright__browser_evaluate(script="""
    return document.querySelector('.notion-page-content').innerText;
""")
```

### Example 3: Multi-Page Tutorial Series

```python
# Capture entire tutorial series
base_url = "https://docs.example.com/tutorials"
pages = []

# Get all tutorial links
mcp__playwright__browser_navigate(url=base_url)
links = mcp__playwright__browser_evaluate(script="""
    return Array.from(document.querySelectorAll('.tutorial-link'))
        .map(a => a.href);
""")

# Capture each page
for link in links:
    mcp__playwright__browser_navigate(url=link)
    mcp__playwright__browser_wait_for(selector=".tutorial-content")
    
    content = mcp__playwright__browser_evaluate(script="""
        return document.querySelector('.tutorial-content').innerText;
    """)
    
    pages.append({'url': link, 'content': content})
    
    # Rate limiting
    time.sleep(2)

# Batch ingest
for page in pages:
    await send_to_knowledge_base(page['content'], page['url'])
```

---

## Related Skills

- `webapp-testing` - Playwright test automation patterns
- `api-integration-patterns` - REST API data fetching
- `vector-search-optimization` - Storing captured content in vector DBs

---

**Version:** 1.1.0 (December 2025)
**MCP Requirement:** Playwright MCP server or Claude Chrome extension
