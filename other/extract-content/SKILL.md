---
name: extract-content
description: Fetch a published article from a URL and extract its title, headings, body content, and metadata into a markdown file the update pipeline can audit.
allowed-tools: Read, Write, WebFetch, Bash
---

# Extract Content Skill

The first stage of the update pipeline. Pulls an existing article off the web and represents it as a structured markdown file that the audit skills (`update-claims`, `update-product-mentions`, `update-topic-gaps`) can analyze.

## Input

`/extract-content <url>`

Example:
- `/extract-content https://mybrand.com/blog/keyword-cannibalization`

## Process

1. **Slugify the URL.** Run `python scripts/slugify.py "<url>"` and capture the slug (uses the URL's last path segment).
2. **WebFetch the URL.** Ask for the full article text in markdown. Strip nav, ads, comments, share buttons, related-posts widgets.
3. **Parse the response into structured fields:**
   - **Title** — H1 of the article
   - **Publish date** — if visible in the page
   - **Last updated** — if visible (often more important than original publish date)
   - **Author** — if visible
   - **Word count** — count of words in the body
   - **H2 list** — every H2 in order
   - **Body** — the full prose
   - **Outbound links** — list of all external links in the body (URL + anchor text)
   - **Internal links** — list of all links to the brand's own domain
   - **Numerical claims** — every sentence containing a number, percentage, "X out of Y", "studies show", or similar
   - **Mentioned products** — any brand product names found (cross-reference `brand-config.md`)
4. **Save to** `content-pipeline/updates/1-extracted/{slug}.md` using this structure:

```markdown
---
url: <url>
title: <title>
publish_date: <date or unknown>
last_updated: <date or unknown>
author: <name or unknown>
word_count: <number>
extracted_at: <today>
---

# {Title}

## Article structure
- {H2 #1}
- {H2 #2}
- ...

## Body

{full article body in markdown}

## Outbound links
- [anchor text](url) — context: "...sentence the link appeared in..."

## Internal links
- [anchor text](url)

## Numerical claims (for /update-claims to audit)
- "{full sentence containing the claim}" — current source: [link or "no source"]

## Mentioned products
- ProductA — appears in section: "..."
- (or: "No brand products mentioned")
```

## Output

`content-pipeline/updates/1-extracted/{slug}.md`

Self-contained representation of the article. The next update skills read this; they don't re-fetch the URL.

## Quality checklist

- [ ] Title and URL captured
- [ ] H2 list matches the actual article
- [ ] Body preserves paragraph breaks and lists
- [ ] At least 3 numerical claims extracted (if the article has any)
- [ ] Outbound links list isn't empty (most articles have some)
- [ ] Mentioned products are real product names, not paraphrases

## When extraction is incomplete

WebFetch may return summarized content for very long articles. If the body looks truncated:
- Try fetching the URL again with a more specific prompt ("return paragraphs 5–10 verbatim")
- Note in the file `extraction_status: partial` and flag which sections may be missing
- The update skills should still work on what's available
