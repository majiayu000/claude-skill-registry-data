---
name: blog-proofreading
description: |
  Check blog posts for flow, broken links, and formatting issues. Technical review for content ready to publish.
  Trigger phrases: "proofread", "check links", "formatting", "technical review", "check formatting", "review links"
allowed-tools: Read, Bash, WebFetch
---

# Proofreading

## What to Check

### 1. Reading Flow
- Transitions between sections make sense
- Paragraph lengths are reasonable
- Technical explanations are clear
- No jarring jumps in logic
- Check for contradicting statements (within paragraphs, between sections, intro vs conclusion)

### 2. Links
- Test external URLs resolve (use `web_fetch` or `curl -I`)
- Check internal links exist
- **Convert inline URLs to reference-style links:**
  - Inline format: `[text](https://example.com)` → should be `[text][ref-name]`
  - All references defined at bottom of post in format: `[ref-name]: https://example.com`
  - Check for any raw URLs like `https://example.com` that should be wrapped in links
- Verify reference-style links formatted correctly: `[text][ref]`
- Verify all reference definitions exist at bottom

### 3. Formatting
- Code blocks have language tags: ```bash, ```python, etc.
- Lists formatted consistently
- Headers follow `##` pattern (no single `#`)
- Proper markdown escaping where needed

### 4. Basic Checks
- Spelling and grammar (light touch)
- Consistent terminology throughout
- Consistent person (first person for experience, "you" when addressing reader is OK, but no "users should" or "one might")
- Section headers match content

## Tools

```bash
# Test if URL resolves
curl -I -s https://example.com | head -1

# Or use web_fetch for full content check
```

## Keep It Light
- Flag issues, don't fix everything
- Focus on broken stuff, not stylistic preferences
- Trust the author's voice

## Response Format

```
**Flow**: Good overall, but transition between § "DNS Fix" and § "Desktop Packages" feels abrupt.

**Links**: 
- ✅ All external links resolve
- ⚠️ Reference [1] not defined at bottom

**Formatting**:
- Missing language tag on line 45 code block
- Inconsistent list formatting in § "Troubleshooting"
```
