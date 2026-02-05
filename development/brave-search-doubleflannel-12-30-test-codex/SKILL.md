---
name: brave-search
description: Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required.
---

# Brave Search

Headless web search and content extraction using Brave Search. No browser required.
This skill exists to provide a reliable, reusable web lookup tool that behaves consistently across agents and projects, even though Codex can search when explicitly enabled; it standardizes the search/extract workflow so it is portable and predictable.

## Setup

Run once before first use:

```bash
cd /home/vnkbr/.codex/skills/brave-search
npm ci
```

Needs env: `BRAVE_API_KEY`.
If missing, `./search.js` exits with a missing key error.

Alt install: if this repo is mirrored elsewhere, `cd <that>/skills/brave-search` before `npm ci`.

## Search

```bash
./search.js "query"                    # Basic search (5 results)
./search.js "query" -n 10              # More results
./search.js "query" --content          # Include page content as markdown
./search.js "query" -n 3 --content     # Combined
```

## Extract Page Content

```bash
./content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown.

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## How to run

```bash
./search.js "steipete" -n 1
```

Success looks like: a `--- Result 1 ---` block with a non-empty Title/Link.
