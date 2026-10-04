---
name: seo-markdown-audit
description: >
  Audit markdown files for SEO before publishing. Checks heading structure,
  meta description, keyword density, content length, link quality, image alt
  text, and frontmatter completeness. Use when user says "markdown audit",
  "check my markdown", "SEO check markdown", or "audit this post".
allowed-tools:
  - Read
  - Bash
  - Glob
---

# Markdown SEO Audit

Analyzes a local markdown file for SEO issues before publishing. No MCP connection required.

## Inputs

- `path`: Absolute path to the markdown file to audit.
  If the user provides a relative path, resolve it using `Bash: realpath <path>` before calling Read.
  If the user provides a directory, use `Glob: **/*.md` to find all markdown files and let the user choose.

## Execution

@skills/seo/references/markdown-guide.md

Use the Read tool to load the file content, then run these 11 check categories:

**1. Title / H1 Check**
- Count lines starting with `# ` (H1) — flag if 0 or >1
- Check H1 character length — warn if >60 chars (Google truncates around 60)
- Extract primary keyword from H1 for use in other checks

**2. Meta Description (Frontmatter)**
- If YAML frontmatter exists (between `---` markers), check for `description` field
- Flag if missing, warn if <120 chars or >160 chars (optimal: 150-160)
- Check if description contains the primary keyword from H1

**3. Heading Hierarchy**
- Verify headings follow proper nesting: H1 → H2 → H3 (no H3 before first H2, no skipped levels)
- Flag duplicate heading text (exact same heading appearing twice)
- Warn if no H2 headings exist (flat content with no structure)

**4. Keyword Placement**
- Extract primary keyword from H1 (longest noun phrase or first 3 meaningful words)
- Check if keyword appears in first 100 words of body content (after H1)
- Check if keyword appears in at least one H2
- Do NOT calculate keyword density percentage (outdated SEO practice)

**5. Content Length**
- Count words (split on whitespace, exclude frontmatter and code blocks)
- Flag CRITICAL if <300 words
- Warn if <800 words (thin content for most topics)
- Note if >3,000 words (consider splitting into pillar + sub-pages)

**6. Readability**
- Calculate average sentence length (split on `.`, `!`, `?`)
- Warn if average >25 words per sentence (too complex for most audiences)
- Flag paragraphs >5 sentences without a subheading break

**7. Link Analysis**
- Find all `[text](url)` patterns
- Flag generic anchor text: "here", "click here", "this link", "read more", "link"
- Count internal links (relative paths starting with `/` or `./` or `../`) — warn if zero
- Count external links — note if zero (no external references can hurt E-E-A-T)

**8. Image Analysis**
- Find all `![alt](url)` patterns
- Flag empty alt text: `![](url)`
- Flag generic alt text: "image", "photo", "screenshot", "picture", "img"
- Note total image count — warn if zero for content >500 words

**9. Frontmatter Completeness**
- Check for YAML frontmatter presence (between `---` markers at top of file)
- Required fields: `title` (flag if missing), `description` (flag if missing)
- Recommended fields: `date`, `author`, `tags`/`categories`
- Check `title` length — warn if >60 chars

**10. Technical Issues**
- Check for broken markdown syntax: unclosed links `[text](`, unclosed images `![alt](`
- Check for raw HTML (not recommended in markdown for SEO — search engines may not parse consistently)
- Check for consecutive blank lines >2 (formatting issue)

**11. Markdown Syntax Quality**
Per Markdown Guide (https://www.markdownguide.org/) syntax best practices:
- Space after heading hash: flag `#Heading` (missing space after `#`) — correct: `# Heading`
- Consistent list delimiters: flag mixed `-` and `*` within the same list block — pick one delimiter and use it consistently throughout
- Blank lines before/after headings: flag any heading that does not have a blank line above it (except the very first line of the file)
- Blank lines before/after code blocks: flag fenced code blocks (` ``` `) that do not have a blank line immediately before and after them
- Ordered list numbering: warn if ordered lists do not start at `1` (e.g., starting at `3`) — most Markdown renderers accept any number but starting at 1 is the standard

## Output Format

```
## Markdown SEO Audit: [filename]

**Overall Score: X/11** (count of categories with no critical/high issues)

### Critical Issues
- [List of critical issues with line numbers if possible]

### High Priority
- [Issues that significantly impact SEO]

### Medium Priority
- [Optimization opportunities]

### Low Priority / Suggestions
- [Nice-to-have improvements]

### Summary
| Check | Status | Notes |
|-------|--------|-------|
| Title/H1 | PASS/WARN/FAIL | [brief note] |
| Meta Description | PASS/WARN/FAIL | [brief note] |
| Heading Hierarchy | PASS/WARN/FAIL | [brief note] |
| Keyword Placement | PASS/WARN/FAIL | [brief note] |
| Content Length | PASS/WARN/FAIL | [word count] |
| Readability | PASS/WARN/FAIL | [avg sentence length] |
| Links | PASS/WARN/FAIL | [internal/external count] |
| Images | PASS/WARN/FAIL | [count, alt text status] |
| Frontmatter | PASS/WARN/FAIL | [fields present/missing] |
| Technical | PASS/WARN/FAIL | [issues found] |
| Markdown Syntax | PASS/WARN/FAIL | [issues found] |
```
