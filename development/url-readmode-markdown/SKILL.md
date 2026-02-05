---
name: url-readmode-markdown
description: Convert a web URL into reader-mode Markdown and save it as a .md file named after the content's topic/title. Use for tasks like extracting article text, cleaning noisy pages, and producing a readable Markdown file from a URL.
---

# Url Readmode Markdown

## Overview

Extract the primary article content from a URL using reader-mode heuristics and save it as Markdown. The output filename should be the content topic/title (sanitized for filenames).

## Quick Start (scripted)

1. Prefer the provided script: `scripts/extract_readmode.js`
2. Use `@mozilla/readability` + `jsdom` + `turndown`.
3. The script prints the output path after writing the Markdown file.

Example:

```bash
node scripts/extract_readmode.js \"https://example.com/article\" -o .
```

Dependencies (Node):

- `npm install @mozilla/readability jsdom turndown`

## Workflow (manual or scripted)

1. Collect the target URL and verify it is article-like content.
2. Extract the main content container using reader-mode heuristics.
3. Convert cleaned HTML to Markdown while preserving headings, lists, and images.
4. Set the output filename to the content topic/title (sanitize invalid filename characters).
5. Review the Markdown for missing sections or noisy blocks and trim as needed.

## Reader-Mode Heuristics

For extraction guidance, use `references/readmode.md` as the heuristic summary.

## Output Requirements

- Output: a single Markdown file containing the main article content.
- Filename: use the article/topic title; sanitize disallowed filename characters; replace spaces with `_`; keep the original language if possible.
- Place output in the user-specified directory or the current working directory by default.

## Resources

### scripts/

`scripts/extract_readmode.js` extracts reader-mode content from a URL and saves Markdown.

### references/

`references/readmode.md` summarizes reader-mode heuristics for fallback/manual extraction.
