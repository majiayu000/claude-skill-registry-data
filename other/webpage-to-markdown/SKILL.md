---
name: webpage-to-markdown
description: Use when converting a public webpage URL into clean Markdown content
---

# Webpage To Markdown

## Overview

Convert a webpage into clean Markdown when the user provides only a URL. The goal is to preserve the meaningful article or page content while removing navigation, ads, scripts, cookie banners, and unrelated page chrome.

## When To Use

Use this skill when:

- The user gives a webpage URL and asks for Markdown.
- The user says "网页转 Markdown", "URL 转 markdown", "convert this page to markdown", or similar.
- The desired output is readable Markdown, not a screenshot, PDF, or browser automation trace.

Do not use it when:

- The URL requires private login that the agent cannot access.
- The user asks to crawl an entire site instead of converting one page.
- The user needs exact visual layout preservation.

## Inputs

Required:

- One public `http` or `https` URL.

Optional:

- Output path if the user wants the Markdown saved to a file.
- Focus instruction such as "只要正文", "保留表格", or "包含链接".

## Workflow

1. Fetch the URL with the best available webpage-reading tool.
2. If the fetch fails because of access restrictions, report the status and ask for a public URL or pasted HTML/text.
3. Identify the main content: title, headings, article body, lists, tables, code blocks, and important links.
4. Convert the main content to Markdown.
5. Remove unrelated content such as navigation menus, cookie banners, newsletter popups, footers, comments, tracking scripts, and repeated sidebar links.
6. Preserve source links when they are meaningful to the content.
7. If saving to a file, use a descriptive lowercase filename and the `.md` extension.

## Output Format

For direct chat output:

```markdown
# Page Title

Source: https://example.com/page

Converted content...
```

For file output, write the same Markdown content to the requested file path and tell the user where it was saved.

## Quality Rules

- Keep heading hierarchy valid: one `#` title, then `##` and below.
- Preserve code blocks with fenced Markdown.
- Preserve tables as Markdown tables when practical.
- Keep relative links only if the base URL is obvious; otherwise convert them to absolute links.
- Do not invent content that was not present on the page.
- If the page is very long, convert the full content unless the user asks for a summary.

## Verification

Before claiming completion:

- Confirm the Markdown contains the page title or a clear generated title.
- Confirm the source URL is included.
- Check that obvious boilerplate has been removed.
- Check that important headings, lists, tables, code blocks, and links were not lost.
- If a file was requested, confirm the file exists and contains Markdown.

## Common Failures

- Returning a summary instead of a Markdown conversion.
- Keeping navigation, ads, cookie banners, or footer link dumps.
- Dropping important tables or code blocks.
- Failing silently when the page cannot be fetched.
- Converting multiple pages when the user asked for one URL.

## Example

User:

```text
把 https://example.com/article 转成 markdown
```

Agent:

1. Fetches the page.
2. Extracts the main article content.
3. Returns Markdown with the title, source URL, headings, body, and meaningful links.
4. Notes any inaccessible sections or removed boilerplate only if it affects the result.
