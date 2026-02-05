---
name: markdown-formatter
description: Format and lint Markdown documents with consistent style, proper heading hierarchy, link validation, and code block formatting. Use when working with Markdown files, documentation, README files, or technical writing. Checks for common issues like broken links, inconsistent formatting, and missing alt text. Triggers on "format markdown", "lint markdown", "markdown style", ".md file", "documentation formatting".
---

# Markdown Formatter

## Purpose

Format and lint Markdown documents to ensure consistent style, proper structure, and best practices.

## When to Use

- Formatting Markdown documentation
- Linting README files
- Checking markdown syntax
- Validating links in documentation
- Ensuring consistent style across docs

## Core Instructions

1. **Read File**: Load the Markdown file
2. **Check Syntax**: Validate Markdown syntax
3. **Format**: Apply consistent formatting
   - Heading hierarchy (h1 -> h2 -> h3, no skips)
   - List indentation (2 spaces)
   - Code block language tags
   - Link format consistency
4. **Validate**: Check for common issues
   - Broken internal links
   - Missing alt text on images
   - Empty links
5. **Output**: Write formatted file or report issues

### Formatting Rules

- Headings: ATX style (`#`, `##`, `###`)
- Lists: 2-space indentation for nested items
- Code blocks: Always specify language
- Links: Use reference style for repeated links
- Line length: 80-120 characters (guidance)

### Example Pattern

```markdown
# Main Title

## Section

### Subsection

Regular paragraph text.

- List item 1
  - Nested item
- List item 2

```python
def example():
    return "formatted"
```

[Link text](https://example.com)
```

## Dependencies

- Markdown parser (built-in)
- No external dependencies required

## Version

v1.0.0

