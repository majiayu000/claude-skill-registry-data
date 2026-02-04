---
name: check-headings
description: Analyze and validate HTML heading hierarchy (H1-H6) on web pages. Use when users ask to check headings structure, verify H1 presence, analyze SEO heading hierarchy, find heading issues, or audit page structure. Detects missing H1, multiple H1s, skipped levels, empty headings, and hierarchy violations.
---

# Check Headings

Analyze and validate HTML heading hierarchy (H1-H6) on web pages for SEO and accessibility compliance.

## Quick Start

Run the heading checker from the scripts directory:

```bash
cd /path/to/html-checker/scripts
bun src/check-headings.ts <URL>
```

## CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--verbose` | `-v` | false | Show detailed heading content |
| `--json` | `-j` | false | Output results as JSON |

## Checks Performed

| Check | Severity | Description |
|-------|----------|-------------|
| Missing H1 | Error | Page has no H1 heading |
| Multiple H1 | Warning | Page has more than one H1 |
| Skipped Level | Warning | Heading level skipped (e.g., H2 to H4) |
| Empty Heading | Error | Heading tag with no text content |
| Wrong Order | Warning | Heading appears before its parent level |

## Usage Examples

### Basic check

```bash
bun src/check-headings.ts https://example.com
```

### Verbose output with heading content

```bash
bun src/check-headings.ts https://example.com --verbose
```

### JSON output for automation

```bash
bun src/check-headings.ts https://example.com --json
```

## Output

The checker provides:

1. **Summary** - Total headings found per level
2. **Issues** - List of problems with severity
3. **Hierarchy** - Visual tree of heading structure
4. **Recommendations** - Actionable fixes

### Example Output

```
Heading Analysis for https://example.com

Summary:
  H1: 1  H2: 5  H3: 12  H4: 3  H5: 0  H6: 0

Issues Found: 2
  [WARNING] Skipped level: H2 -> H4 at line 45
  [ERROR] Empty heading: H3 at line 78

Hierarchy:
  H1: Welcome to Example
    H2: About Us
      H3: Our Mission
      H3: Our Team
    H2: Services
      H4: Web Development  <-- Skipped H3
```

## SEO Best Practices

- **One H1 per page**: The H1 should match the page's main topic
- **Sequential hierarchy**: Don't skip levels (H2 -> H4)
- **Descriptive headings**: Avoid generic text like "Read More"
- **Keyword inclusion**: Include target keywords naturally
- **Logical structure**: Headings should outline page content

## Accessibility (WCAG)

- **SC 1.3.1**: Headings must convey structure
- **SC 2.4.6**: Headings must be descriptive
- **SC 2.4.10**: Section headings organize content

## Related Files

- **Scripts**: `/plugins/html-checker/scripts/`
- **Check Links**: `/plugins/html-checker/skills/check-links/`
