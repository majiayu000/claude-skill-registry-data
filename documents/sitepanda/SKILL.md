---
name: sitepanda
description: >
  Scrape websites with a headless browser and extract main readable content as Markdown.
  Use this skill when the user asks to retrieve, analyze, or summarize content from a URL or website.
---

# Sitepanda (Web Scraping Tool)

## Instructions

1. When the user provides a URL or asks for website content, use Sitepanda to scrape the page.
2. By default, use the following command to scrape a single page:

   sitepanda scrape <URL> --silent --limit 1

3. If you need to perform recursive scraping (following links), you **must** ask the user for confirmation before starting, as it may take a long time.
4. Capture the output, which is returned in Markdown format.
5. Read and analyze the extracted content.
6. Respond to the user using only the relevant information from the page.
7. If the content is long, summarize or extract only the necessary sections.

## Examples

### Example 1

**User request:**
"Please summarize the article at https://example.com/blog/post-123"

**Agent behavior:**
- Use Sitepanda to scrape the page
- Read the extracted Markdown
- Summarize the main points in the response

### Example 2

**User request:**
"What does this documentation page say? https://example.com/docs"

**Agent behavior:**
- Fetch the page using Sitepanda
- Extract key sections
- Explain the content concisely
