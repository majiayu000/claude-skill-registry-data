---
name: get-web-page-raw
description: Capture a web page as raw material (extracted text/Markdown) with metadata, storing it in the raw/ directory for later distillation.
---

# Get Web Page (Raw)

## When to use

Use this skill when:
- The user provides a URL to capture as source material
- You need to store a web page for later distillation
- You're building up raw materials for the distillation pipeline

**Keywords:** capture, web page, URL, fetch, raw

## Inputs

Required:
- `url` (string): The URL of the web page to capture

Optional:
- `title_hint` (string): A human-provided hint for the title if extraction fails

## Outputs

This skill produces:
1. A new file in `raw/` with the naming pattern: `YYYYMMDD-HHMMSSZ--<slug>.md`
2. Metadata returned to the agent:
   - `raw_path`: full path to the created file
   - `title`: extracted or inferred title
   - `canonical_url`: canonical URL if found, otherwise the input URL
   - `captured_at`: ISO timestamp (UTC)

## Procedure

### 1. Generate timestamp and slug

- Get current UTC timestamp: `date -u +"%Y%m%d-%H%M%SZ"`
- Create a slug from the page title or URL path:
  - Use the main topic/title in lowercase
  - Replace spaces and special chars with hyphens
  - Keep it concise (typically 3-8 words)
  - Example: `patterns-for-ai-assisted-software-development`

### 2. Fetch the web page content

**Primary method: fetch_webpage tool**
- Call `fetch_webpage` with the URL and a descriptive query about the content
- This extracts main content, removes navigation/ads, and converts to clean Markdown
- Captures metadata like title and author when available

**Alternative methods (when needed):**
- **Playwright MCP:** For complex interactive pages, JavaScript-heavy sites, or when you need precise browser control
- **curl + HTML parsing:** For simple pages when fetch_webpage isn't available, though requires manual Markdown conversion
- **Browser tools:** Built-in browser navigation and snapshot capabilities

**Note:** Most public articles and blog posts work well with fetch_webpage

### 3. Build front matter

Create YAML front matter with required and available fields:

```yaml
---
title: "<extracted from page>"
source_url: "<original URL provided>"
captured_at: "<ISO timestamp from step 1>"
capture_type: web_page
capture_tool: fetch_webpage  # or browser if used
raw_format: markdown
status: captured
author: "<if clearly visible>"  # optional
published_at: "<YYYY-MM-DD if available>"  # optional
tags: ["keyword1", "keyword2"]  # optional, 3-5 relevant tags
---
```

**Tips:**
- Use the page's actual title, not a description
- Convert published_at to simple date format (YYYY-MM-DD)
- Tags should be broad topics, not exhaustive keywords

### 4. Write the file

- Filename: `<timestamp>--<slug>.md` (e.g., `20260102-095107Z--patterns-for-ai-assisted-software-development.md`)
- Full path: `raw/<filename>`
- Content: front matter + blank line + extracted content
- Use `create_file` tool with the full content

### 5. Confirm to user

Provide a brief confirmation:
- Link to the created file using relative path
- One-sentence summary of what the article covers (2-3 key topics)

## Examples

### Example 1: Dev.to article capture

**Input:**
```
url: "https://dev.to/javatarz/patterns-for-ai-assisted-software-development-4ga2"
```

**Actions:**
1. Generate timestamp: `20260102-095107Z`
2. Fetch with `fetch_webpage` tool
3. Extract title: "Patterns for AI assisted software development"
4. Create slug: `patterns-for-ai-assisted-software-development`
5. Write to: `raw/20260102-095107Z--patterns-for-ai-assisted-software-development.md`

**Output:**
```yaml
---
title: "Patterns for AI assisted software development"
source_url: "https://dev.to/javatarz/patterns-for-ai-assisted-software-development-4ga2"
captured_at: "2026-01-02T09:51:07Z"
capture_type: web_page
capture_tool: fetch_webpage
raw_format: markdown
status: captured
author: "Karun Japhet"
published_at: "2025-12-27"
tags: ["ai", "programming", "productivity", "patterns"]
---
```



## Edge cases

**fetch_webpage fails:**
- Check if authentication is required
- Try browser-based extraction if needed
- Inform user if the page cannot be accessed

**Missing metadata:**
- If no title is extracted, use the URL path or ask user for a title hint
- If no author/date visible, omit those fields
- Minimal front matter is acceptable

**Paywalled or restricted content:**
- Inform user about the restriction
- Capture what's visible if useful (preview text)
- Consider asking if they have alternative access

## References

- Parent workflow: `docs/distillation/distillation-pipeline.md`
- Front matter schema: see "Raw file front matter" in distillation-pipeline.md
- Next step after capture: use `make-distilled` skill to process this raw file
