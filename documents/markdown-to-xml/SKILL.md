---
name: markdown-to-xml
description: Convert markdown articles from Obsidian vault to XML format, preserving bold text, blockquotes, and header hierarchy based on hashtag count
---

# Markdown to XML Converter

Automatically convert the "### Article" section of markdown files from the Obsidian Articles folder to XML format.

## When to use this skill

Use this skill when the user:
- Asks to convert an article to XML
- Wants to export or format an article for external use
- Mentions converting markdown to XML/HTML
- Needs to prepare article content for publishing

## What this skill does

1. Locates the article file in the Obsidian vault's Articles folder
2. Extracts content under the "### Article" header
3. Converts markdown formatting to XML:
   - Headers: # → `<h1>`, ## → `<h2>`, etc. (based on hashtag count)
   - Bold: **text** → `<strong>text</strong>`
   - Blockquotes: > quote → `<blockquote>quote</blockquote>`
   - Italic: *text* → `<em>text</em>`
   - Links: [text](url) → `<a href="url">text</a>`
   - Lists: - item → `<ul><li>item</li></ul>`
4. Saves the converted content to `~/Desktop/article_converted.md`

## How to use

Execute the Python conversion script:

```bash
python /Users/biancopeve/.claude/skills/markdown-to-xml/convert.py "ARTICLE_NAME"
```

**Arguments:**
- `ARTICLE_NAME`: The full or partial name of the article file to convert

**Example:**
```bash
python /Users/biancopeve/.claude/skills/markdown-to-xml/convert.py "17. ProductInterview"
```

## Output

The converted XML content will be saved to:
- **Location**: `~/Desktop/article_converted.md`
- **Format**: XML tags with preserved markdown formatting

## Important notes

- The script preserves all bold text and blockquotes (important for engagement and meaningful quotes)
- Headers are converted based on hashtag count (# = h1, ## = h2, ### = h3, etc.)
- The script automatically finds the article in the Obsidian vault's Articles folder
- Partial filename matches are supported for convenience
