---
name: blog-scraper
description: Fetch and compress blog articles from tech-lab.sios.jp into the doc/ directory with token usage statistics and OGP metadata
---

# Blog Scraper Skill

## Overview

This skill fetches blog articles from `tech-lab.sios.jp/archives/*`, compresses the HTML content by removing unnecessary attributes and whitespace, and saves the result to the `doc/` directory with metadata.

## When to Use

- User requests to fetch a specific blog article
- User wants to update existing cached articles
- User needs to scrape multiple articles for analysis or documentation

## Usage

### Single Article

```bash
URL=https://tech-lab.sios.jp/archives/[article-id] npm run scraper
```

Example:
```bash
URL=https://tech-lab.sios.jp/archives/48397 npm run scraper
```

### Multiple Articles

For multiple articles, run the command sequentially for each URL.

## Output

The scraper will:

1. **Fetch and parse** the HTML from the specified URL
2. **Extract content** using the CSS selector `section.entry-content`
3. **Compress** by removing:
   - Scripts, styles, and noscript tags
   - Class, ID, and style attributes
   - Whitespace between tags
4. **Preserve**:
   - Image alt text as `[画像: alt]`
   - Image src URLs
   - Link href attributes
5. **Add metadata** as HTML comment:
   - OGP title
   - Source URL
   - OGP image URL
   - Extraction timestamp
6. **Save** to `docs/data/tech-lab-sios-jp-archives-[id].html`
7. **Report** compression statistics:
   - Token count reduction (estimated for Claude)
   - Compression ratio percentages
   - File size

## Cache Behavior

- If the target HTML file already exists in `docs/data/`, the scraper **skips fetching** and reports the existing file size
- To re-fetch, delete the existing HTML file first

## Token Estimation

The scraper estimates Claude token usage for Japanese content:
- Hiragana/Katakana: ~1.5 chars/token
- Kanji: ~1 char/token
- ASCII: ~4 chars/token
- Other: ~2 chars/token

Typical compression achieves 60-85% token reduction.

## Implementation Details

See `application/tools/scraper.ts` for the TypeScript implementation using:
- `node-fetch` for HTTP requests
- `cheerio` for HTML parsing
- OGP metadata extraction
- Custom token estimation for Japanese text

## Permissions Required

This skill requires the following permissions in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run scraper:*)",
      "Bash(URL=:*)"
    ]
  }
}
```

**Note:** The `Bash(URL=:*)` permission uses prefix matching to allow any URL environment variable pattern. This is a broad permission - consider restricting to specific domains if needed for security.
