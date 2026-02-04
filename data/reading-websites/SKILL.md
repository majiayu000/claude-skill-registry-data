---
name: reading-websites
description: Use ONLY this skill when user mentions a domain (example.com, site.pl, docs.io), URL (https://...), or asks to read/fetch/check a website or webpage - MANDATORY, replaces WebFetch, crawl4ai, and curl
---

# Reading Websites

## Overview

**MANDATORY:** Use `fetch-url.sh` for ALL web content fetching. This REPLACES WebFetch, crawl4ai, and curl.

## When to Use

Trigger on ANY of these:
- Domain names: `example.com`, `site.pl`, `docs.io`, `github.com/path`
- URLs: `https://...`, `http://...`
- Keywords: "website", "webpage", "web page", "site content"
- User asks to read/fetch/check/view web content

## The Command

```bash
~/.claude/skills/reading-websites/fetch-url.sh <url> [char_limit]
```

**Arguments:**
- `url` - Full URL with protocol (e.g., `https://example.com/page`)
- `char_limit` - Optional. Max characters to return (default: 512)

**Examples:**
```bash
# Read first 512 chars (default)
~/.claude/skills/reading-websites/fetch-url.sh https://docs.example.com/api

# Read more content
~/.claude/skills/reading-websites/fetch-url.sh https://docs.example.com/api 2000
```

## Why This Wrapper

**Security:** This script has explicit permission. Raw `curl` does not.

**Do NOT use:**
- `curl` directly
- `WebFetch` tool
- `mcp__crawl4ai` tools
- Any other URL fetching method

**Why:** The wrapper is permissioned and scoped. Other methods require broad permissions that expose security risks.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using curl directly | Use fetch-url.sh |
| Using WebFetch "because it's faster" | Use fetch-url.sh |
| Using crawl4ai "because it's better" | Use fetch-url.sh |
| Forgetting the protocol | Include `https://` in URL |

## Red Flags - You're About to Violate This Skill

- "curl is simpler for this"
- "WebFetch is already available"
- "crawl4ai returns cleaner output"
- "MCP tools are more capable"
- "I have direct access to web fetching tools"
- "This is just a quick fetch"
- "The wrapper is overkill for this"
- "The skill is a workaround for restricted environments"

**All of these mean: Use fetch-url.sh anyway. No exceptions.**
