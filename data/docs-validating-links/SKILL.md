---
name: docs-validating-links
description: Comprehensive link validation methodology for markdown links including format requirements, path validation, broken link detection, external link verification, and checker implementation patterns
created: 2025-01-22
updated: 2026-01-25
---

# Validating Markdown Links

This Skill provides comprehensive guidance for validating markdown links across the repository, including internal link validation, external link verification, Hugo-specific patterns, and checker implementation strategies.

## Purpose

Use this Skill when:

- Implementing link validation in checker agents
- Validating internal documentation links
- Verifying external URL accessibility
- Checking Hugo site link formatting
- Implementing link caching strategies
- Understanding link validation patterns

## Link Validation Principles

### Why Link Validation Matters

**Broken links**:

- Break user navigation experience
- Reduce documentation credibility
- Create maintenance burden (hard to find broken links manually)
- Indicate structural issues (moved/deleted files)

**Link validation**:

- Prevents broken links from reaching production
- Catches file renames and moves
- Validates external resources still exist
- Ensures consistent link formatting

### Validation Scope

**What to validate**:

- Internal markdown links (docs/, governance/, plans/)
- Hugo content links (apps/ayokoding-web/, apps/ose-platform-web/)
- External URLs (HTTP/HTTPS)
- Image links (relative paths)
- Anchor links (same-page headings)

**What NOT to validate**:

- Links in code blocks (examples, not actual links)
- Links in quoted text (preserved formatting)
- Commented-out links (intentionally disabled)

## Internal Link Validation

### Required Link Format

**Documentation files** (docs/, governance/, plans/, root .md files):

✅ PASS: [File Naming Convention](../meta/file-naming.md)
✅ PASS: [AI Agents Convention](../../development/agents/ai-agents.md)

❌ FAIL: [File Naming Convention](../meta/file-naming) ← Missing .md extension
❌ FAIL: [[file-naming]] ← Obsidian wiki link (not GitHub-compatible)
❌ FAIL: [file-naming.md](../meta/file-naming.md) ← Using filename as link text

**Hugo content files** (apps/ayokoding-web/content/, apps/ose-platform-web/content/):

✅ PASS: [Learn AI](/learn/ai)
✅ PASS: [Chat with PDF Tutorial](/learn/ai/chat-with-pdf)

❌ FAIL: [Learn AI](/learn/ai.md) ← Should omit .md extension in Hugo
❌ FAIL: [Learn AI](../ai) ← Should use absolute path in Hugo (starts with /)

### Validation Methodology

**Step 1: Extract Links from Markdown**

Use regex or markdown parser to extract all links

**Step 2: Categorize Links**

Separate into categories:

- Internal links (start with ./, ../, or /)
- External links (start with http://, https://)
- Anchor links (start with #)
- Image links (extensions: .png, .jpg, .svg, etc.)

**Step 3: Validate Internal Links**

For each internal link:

1. Resolve relative path from current file location
2. Check target file exists using filesystem
3. Validate format (has .md extension for docs/, no extension for Hugo)
4. Check link text quality (descriptive, not filename-based)

### Common Internal Link Errors

**Error 1: Missing .md extension**

❌ FAIL: [File Naming](../meta/file-naming)
✅ PASS: [File Naming](../meta/file-naming.md)

**Criticality**: HIGH - Breaks GitHub web navigation
**Detection**: Check link ends with .md (docs/ files only)

**Error 2: Wrong relative path depth**

From: governance/conventions/formatting/linking.md (3 levels deep)
❌ FAIL: [Documentation Home](../README.md) ← Only 1 ../, need 3
✅ PASS: [Documentation Home](../../../README.md)

**Criticality**: CRITICAL - Link points to wrong file or 404
**Detection**: Resolve path and check file exists

**Error 3: Obsidian wiki links**

❌ FAIL: [[file-naming-convention]]
❌ FAIL: [[file-naming-convention|File Naming]]
✅ PASS: [File Naming Convention](../meta/file-naming.md)

**Criticality**: HIGH - Breaks GitHub web compatibility
**Detection**: Regex match for wiki-style links

**Error 4: Filename as link text**

❌ FAIL: [ex-co__file-naming.md](../meta/file-naming.md)
✅ PASS: [File Naming Convention](../meta/file-naming.md)

**Criticality**: MEDIUM - Poor accessibility and readability
**Detection**: Check if link text matches filename pattern or contains file extension

**Error 5: Hugo link with .md extension**

From: apps/ayokoding-web/content/learn/ai/_index.md
❌ FAIL: [Chat with PDF](/learn/ai/chat-with-pdf.md) ← Hugo omits .md
✅ PASS: [Chat with PDF](/learn/ai/chat-with-pdf)

**Criticality**: HIGH - Hugo won't resolve the link correctly
**Detection**: Check Hugo content files don't use .md in absolute paths

**Error 6: Hugo link using relative path**

From: apps/ayokoding-web/content/learn/ai/_index.md
❌ FAIL: [Security](../security) ← Hugo needs absolute paths
✅ PASS: [Security](/learn/security)

**Criticality**: CRITICAL - Breaks navigation when page rendered in different contexts
**Detection**: Check Hugo content uses absolute paths (start with /)

## External Link Validation

### Verification Strategy

**Challenge**: External links can be slow to verify (network requests)

**Recommended approach**:

1. Cache results - Store validation results in cache file
2. Respect cache TTL - Re-verify after 7 days (configurable)
3. Batch verification - Verify multiple URLs in parallel
4. Handle failures gracefully - Network errors != broken link

### HTTP Request Pattern

**Verification steps**:

1. HEAD request first - Faster than GET, checks if URL accessible
2. Follow redirects - HTTP 301/302 are OK (but report for info)
3. Check status codes:
   - 200-299: OK
   - 300-399: REDIRECT (report but don't fail)
   - 400-499: BROKEN (client error, link is wrong)
   - 500-599: SERVER_ERROR (temporary, re-verify later)
   - Timeout: UNREACHABLE (network issue, re-verify later)

### Link Caching Strategy

**Cache file format** (JSON):

{
  "https://diataxis.fr/": {
    "status": "OK",
    "http_code": 200,
    "last_checked": "2026-01-25T13:30:00+07:00",
    "ttl": 604800
  }
}

**Cache TTL recommendations**:

- OK links: 7 days
- BROKEN links: 1 day
- REDIRECT links: 7 days
- SERVER_ERROR: 1 hour
- UNREACHABLE: 1 hour

### Common External Link Errors

**Error 1: Link returns 404**

**Criticality**: HIGH - Link is dead, user gets 404
**Action**: Update or remove link

**Error 2: Link redirects (301/302)**

**Criticality**: LOW - Link works but could be updated to final URL
**Action**: Consider updating to final destination (optional)

**Error 3: Link times out**

**Criticality**: MEDIUM - May be temporary network issue
**Action**: Re-verify after TTL expires, flag if persistent

## Hugo-Specific Link Validation

### Hugo Link Patterns

Hugo internal links use absolute paths without .md extension:

✅ PASS: [Learn AI](/learn/ai)
✅ PASS: [Chat with PDF](/learn/ai/chat-with-pdf)

❌ FAIL: [Learn AI](../ai) ← Should be absolute path
❌ FAIL: [Chat with PDF](/learn/ai/chat-with-pdf.md) ← Should omit .md

### Why Hugo Uses Absolute Paths

Hugo renders the same navigation content in different contexts (sidebar, mobile menu, homepage). Relative paths would resolve incorrectly depending on page context. Absolute paths work consistently across all contexts.

### Validation Differences: Hugo vs. Docs

| Aspect | Docs/ Files | Hugo Content |
|--------|-------------|--------------|
| Extension | MUST include .md | MUST omit .md |
| Path Type | Relative (../, ./) | Absolute (/path) |
| Link Format | [Text](../file.md) | [Text](/path) |
| Validation | Check file exists on filesystem | Check file exists in content/ tree |
| Criticality | CRITICAL if missing .md | CRITICAL if includes .md |

## Checker Implementation Patterns

### Link Validation Workflow

Standard 5-step checker workflow:

Step 0: Initialize Report
Step 1: Discover Files (glob for *.md)
Step 2: Extract Links (parse markdown, categorize)
Step 3: Validate Internal Links (file exists, format correct)
Step 4: Validate External Links (HTTP request, cache results)
Step 5: Finalize Report (summary, grouped by criticality)

### Progressive Writing Requirement

**CRITICAL**: Write findings to report file immediately after discovery (don't buffer in memory)

**Why**: Context compaction can lose buffered findings during long validation runs

### Tool Requirements for Link Checkers

**Required tools**:

- Read: Read markdown files to extract links
- Glob: Find all markdown files in scope
- Grep: Extract link patterns
- Bash: File existence checks, path resolution, HTTP requests
- Write: Initialize and update report file

### Categorization by Criticality

**CRITICAL** (Must fix before publication):

- Broken internal links (404, file not found)
- Wrong Hugo link format (includes .md or uses relative path)
- Obsidian wiki links (breaks GitHub compatibility)

**HIGH** (Should fix before publication):

- Missing .md extension in docs/ links
- Broken external links (404, 410)
- Filename as link text (poor accessibility)

**MEDIUM** (Fix when convenient):

- External link redirects (works but suboptimal)
- External link timeouts (may be temporary)
- Suboptimal link text (not descriptive enough)

**LOW** (Optional improvements):

- Consider updating redirect to final URL
- Suggest alternative link text

### Dual-Label Pattern for Link Checkers

Link checkers use both verification status AND criticality:

Finding: [BROKEN] - Internal Link to Non-Existent File

**Verification**: [BROKEN] - Target file does not exist
**Criticality**: CRITICAL - Breaks user navigation

**Verification labels**:

- [OK] - Link is valid
- [BROKEN] - Link target doesn't exist (404)
- [REDIRECT] - External link redirects (informational)
- [FORMAT_ERROR] - Wrong format (missing .md, etc.)

**Why dual labels?**

- Verification describes FACTUAL STATE
- Criticality describes URGENCY/IMPORTANCE
- Complementary information for fixer decision-making

## Related Conventions

**Linking Standards**:

- Linking Convention - Complete linking standards
- Hugo Content Convention - Hugo linking patterns

**Validation Standards**:

- Repository Validation Methodology - Standard validation patterns
- Criticality Levels Convention - Criticality classification

**Quality Standards**:

- Content Quality Principles - Link text quality requirements

## Related Skills

**Validation Skills**:

- repo-assessing-criticality-confidence - Criticality and confidence levels
- repo-applying-maker-checker-fixer - Checker workflow patterns
- repo-generating-validation-reports - Report format and progressive writing

**Domain Skills**:

- apps-ayokoding-web-developing-content - Hugo-specific linking patterns

## Related Agents

**Link Validation Agents**:

- docs-link-general-checker - Validates links in docs/, governance/, plans/
- apps-ayokoding-web-link-checker - Validates links in ayokoding-web Hugo content
