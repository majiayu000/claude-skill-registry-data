---
name: seo-llms-txt
description: >
  Generate, validate, or audit llms.txt files for AI search visibility.
  Crawls site structure, generates spec-compliant Markdown index for LLMs.
  Use when user says "llms.txt", "llm txt", "AI crawlers", "generate llms",
  "LLM file", "AI readability file".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
  - Write
---

# llms.txt — Generate, Validate & Audit

<!-- Updated: 2026-06-10 -->

Analyze, generate, or validate llms.txt files per the llms.txt specification
(proposed by Jeremy Howard / Answer.AI). The llms.txt standard provides a
Markdown file at `/llms.txt` that helps LLMs understand a website's content
structure — similar to how robots.txt guides traditional crawlers.

**Adoption:** Adopted by thousands of sites including Anthropic, Cloudflare,
Docker, Vercel, Stripe, FastHTML, Cursor, Hugging Face, and many more.

### Lighthouse "Agentic Browsing" audit

Chrome Lighthouse now includes an **Agentic Browsing** audit category with a
dedicated llms.txt check. Lighthouse flags a page if a server error occurs
when fetching `/llms.txt`; if the file is simply absent (404), the audit is
marked Not Applicable since the file is optional. Users can validate their
llms.txt presence by running Lighthouse. Reference:
https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt

## Inputs

Three modes, auto-detected from the user's input:

| Input Pattern | Mode | Example |
|---|---|---|
| `/seo llms-txt <url>` | **Audit** | `/seo llms-txt example.com` |
| `/seo llms-txt generate <url>` | **Generate** | `/seo llms-txt generate example.com` |
| `/seo llms-txt validate <url-or-path>` | **Validate** | `/seo llms-txt validate /path/to/llms.txt` |

- If user provides a URL without sub-command → **Audit** mode (fetch and check existing file)
- If user says "generate" → **Generate** mode (crawl site, produce llms.txt)
- If user says "validate" → **Validate** mode (parse and check against spec)

## llms.txt Spec Reference

@skills/seo/references/llms-txt-spec.md

### Quick Spec Summary

The llms.txt file must be valid Markdown with this structure:

1. **H1 heading** (required) — Project/site name
2. **Blockquote** (optional) — Short site summary
3. **H2 sections** — Categorized link lists with descriptions
4. **Link format**: `- [Name](url): Description` (colon + space after URL)
5. **`## Optional` section** — Links useful but not essential for understanding
6. **Companion files** (optional):
   - `llms-full.txt` — Comprehensive version with full content
   - Individual `.md` page mirrors for key pages

## Execution: Audit Mode

When user provides a URL (no sub-command):

1. **Fetch llms.txt**: Use WebFetch to retrieve `<url>/llms.txt`
2. **Run 8-point check**:

| # | Check | Pass Criteria |
|---|---|---|
| 1 | File exists | HTTP 200 at `/llms.txt` |
| 2 | Valid Markdown | Parseable as Markdown, no broken syntax |
| 3 | Has H1 | Exactly one `# ` heading |
| 4 | Has blockquote summary | `> ` line present after H1 (recommended) |
| 5 | Has H2 sections | At least one `## ` section with links |
| 6 | Link format correct | Links follow `- [Name](url): description` pattern |
| 7 | Has `## Optional` | Contains an Optional section (recommended) |
| 8 | Companion llms-full.txt | `llms-full.txt` exists at same path (recommended) |

3. **Link spot-check**: WebFetch up to 5 linked URLs to verify they resolve (HTTP 200)
4. **Generate score card and recommendations**

## Execution: Generate Mode

When user says "generate":

1. **Crawl site structure**:
   - WebFetch the homepage — extract title, meta description, nav links
   - WebFetch `/sitemap.xml` (or `/sitemap_index.xml`) — extract all URLs
   - If no sitemap, follow nav links from homepage (up to 50 pages)

2. **Categorize pages** into sections based on URL patterns and content:
   - `## Docs` — `/docs/`, `/documentation/`, `/guides/`, `/reference/`
   - `## Blog` — `/blog/`, `/articles/`, `/posts/`, `/news/`
   - `## API` — `/api/`, `/developers/`, `/reference/`
   - `## Products` — `/products/`, `/features/`, `/pricing/`, `/solutions/`
   - `## About` — `/about/`, `/team/`, `/company/`, `/contact/`
   - `## Legal` — `/privacy/`, `/terms/`, `/legal/`
   - `## Optional` — Catch-all for remaining useful pages

3. **Extract metadata per page**:
   - Title (from `<title>` or `<h1>`)
   - Description (from `meta[name=description]` or first paragraph)
   - Truncate description to ~100 characters

4. **Generate llms.txt**:
   ```markdown
   # Site Name

   > Brief site description from meta or homepage hero text.

   ## Docs

   - [Getting Started](https://example.com/docs/start): Introduction and setup guide
   - [API Reference](https://example.com/docs/api): Complete API documentation

   ## Blog

   - [Latest Post](https://example.com/blog/post): Description of the post

   ## Optional

   - [About](https://example.com/about): Company background
   - [Contact](https://example.com/contact): Get in touch
   ```

5. **Generate llms-full.txt skeleton** (optional — note to user):
   ```
   Suggest that llms-full.txt should contain the full Markdown content
   of all key pages concatenated. Provide the structure but note that
   generating full content requires crawling every page.
   ```

6. **Output the generated file** — display it in a code block and offer to write to disk

## Execution: Validate Mode

When user says "validate":

1. **Load the file**:
   - If URL → WebFetch `<url>/llms.txt`
   - If local path → Read the file

2. **Run spec compliance checks**:

| # | Rule | Severity | Check |
|---|---|---|---|
| 1 | Has exactly one H1 | FAIL | Count `# ` lines (not `##`) |
| 2 | H1 is first heading | FAIL | First line starting with `#` must be H1 |
| 3 | Valid Markdown | FAIL | No broken link syntax, unclosed brackets |
| 4 | Links use correct format | WARN | `- [Name](url): description` pattern |
| 5 | Has at least one H2 section | FAIL | At least one `## ` heading |
| 6 | No empty sections | WARN | Every H2 should have at least one link |
| 7 | Blockquote present | INFO | `> ` after H1 is recommended |
| 8 | `## Optional` section exists | INFO | Recommended by spec |
| 9 | No deep heading levels | WARN | Only H1 and H2 allowed (no H3+) |
| 10 | Descriptions present | WARN | Links should have `: description` after URL |

3. **Output pass/fail per rule** with line numbers for failures

## Output Format

### Audit Mode Output

```
## llms.txt Audit: [domain]

**Score: X/8 checks passed**

| # | Check | Result | Details |
|---|---|---|---|
| 1 | File exists | PASS/FAIL | [status code or error] |
| 2 | Valid Markdown | PASS/FAIL | [issue if any] |
| ... | ... | ... | ... |

### Link Spot-Check
| URL | Status |
|---|---|
| [url] | 200 OK / 404 / timeout |

### Recommendations
- [Prioritized list of improvements]

### What is llms.txt?
> llms.txt is a proposed standard (llmstxt.org) that provides LLMs with
> a structured Markdown overview of your site. Thousands of sites have adopted it.
> While AI platform adoption of the standard is still emerging, early
> adoption positions your site for AI search visibility — similar to how
> early schema.org adoption paid off for rich snippets.
```

### Generate Mode Output

```
## Generated llms.txt for [domain]

[The generated llms.txt content in a code block]

### Generation Notes
- Pages crawled: [count]
- Sections created: [list]
- Pages excluded: [count and reason]

### Next Steps
1. Review and edit the generated file
2. Upload to your site root as `/llms.txt`
3. Consider creating `llms-full.txt` with full page content
4. Add `<link rel="help" href="/llms.txt">` to your HTML head (optional)
```

### Validate Mode Output

```
## llms.txt Validation: [source]

**Result: X/10 rules passed** | Y warnings | Z info

| # | Rule | Result | Line | Details |
|---|---|---|---|---|
| 1 | Has H1 | PASS/FAIL | [line#] | [details] |
| ... | ... | ... | ... | ... |

### Issues to Fix
- [FAIL items with specific fix instructions]

### Recommendations
- [WARN items with suggestions]
```
