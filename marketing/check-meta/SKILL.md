---
name: check-meta
description: Analyze and validate meta tags on web pages. Use when users ask to check meta tags, verify SEO tags, audit page titles, check Open Graph tags, verify canonical URLs, or analyze social sharing tags. Detects missing title, description issues, duplicate tags, and Open Graph problems.
---

# Check Meta

Analyze and validate meta tags on web pages for SEO and social sharing.

## Quick Start

```bash
cd /path/to/html-checker/scripts
bun src/check-meta.ts <URL>
```

## CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--verbose` | `-v` | false | Show all meta tags found |
| `--json` | `-j` | false | Output results as JSON |

## Checks Performed

| Check | Severity | Description |
|-------|----------|-------------|
| Missing title | Error | Page has no title tag |
| Title too short | Warning | Title under 30 characters |
| Title too long | Warning | Title over 60 characters |
| Missing description | Error | No meta description |
| Description too short | Warning | Description under 50 characters |
| Description too long | Warning | Description over 160 characters |
| Missing canonical | Warning | No canonical URL specified |
| Missing og:title | Info | No Open Graph title |
| Missing og:description | Info | No Open Graph description |
| Missing og:image | Info | No Open Graph image |
| Missing twitter:card | Info | No Twitter card meta |
| Duplicate meta | Warning | Same meta tag appears twice |

## Usage Examples

```bash
# Basic check
bun src/check-meta.ts https://example.com

# Verbose output
bun src/check-meta.ts https://example.com --verbose

# JSON output
bun src/check-meta.ts https://example.com --json
```

## Output Example

```
Meta Analysis for https://example.com

Title: "Example Domain" (14 chars)
Description: "This domain is for use in illustrative examples..." (156 chars)

SEO Tags:
  [OK] title: Example Domain
  [OK] description: This domain is for...
  [MISSING] canonical

Open Graph:
  [MISSING] og:title
  [MISSING] og:description
  [MISSING] og:image

Twitter:
  [MISSING] twitter:card
  [MISSING] twitter:title

Issues Found: 5
  [WARNING] Title too short (14 chars, min 30)
  [WARNING] Missing canonical URL
  [INFO   ] Missing og:title
  [INFO   ] Missing og:image
  [INFO   ] Missing twitter:card

Recommendations:
  - Expand title to 30-60 characters
  - Add canonical URL to prevent duplicate content
  - Add Open Graph tags for social sharing
```

## SEO Best Practices

- **Title**: 30-60 characters, include primary keyword
- **Description**: 50-160 characters, compelling call-to-action
- **Canonical**: Always specify to prevent duplicate content
- **Open Graph**: Essential for social media sharing
