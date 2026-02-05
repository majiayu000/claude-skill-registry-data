---
name: check-images
description: Analyze and validate images on web pages. Use when users ask to check image alt tags, verify image accessibility, find missing alt attributes, audit image SEO, or check image optimization. Detects missing alt, empty alt, decorative images without proper markup, oversized images, and missing dimensions.
---

# Check Images

Analyze and validate images on web pages for accessibility and SEO compliance.

## Quick Start

```bash
cd /path/to/html-checker/scripts
bun src/check-images.ts <URL>
```

## CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--verbose` | `-v` | false | Show all images including valid ones |
| `--json` | `-j` | false | Output results as JSON |

## Checks Performed

| Check | Severity | Description |
|-------|----------|-------------|
| Missing alt | Error | Image has no alt attribute |
| Empty alt | Warning | Image has alt="" (verify if decorative) |
| Generic alt | Warning | Alt text like "image", "photo", "picture" |
| Long alt | Info | Alt text exceeds 125 characters |
| Missing dimensions | Warning | No width/height attributes (CLS risk) |
| No lazy loading | Info | Large images without loading="lazy" |

## Usage Examples

```bash
# Basic check
bun src/check-images.ts https://example.com

# Verbose output
bun src/check-images.ts https://example.com --verbose

# JSON output
bun src/check-images.ts https://example.com --json
```

## Output Example

```
Image Analysis for https://example.com

Summary:
  Total Images: 25
  With alt: 20
  Missing alt: 3
  Empty alt: 2

Issues Found: 5
  [ERROR  ] Missing alt at position 5
    <img src="/hero.jpg">
  [WARNING] Empty alt at position 12
    <img src="/divider.png" alt="">
  [WARNING] Generic alt at position 18
    <img src="/team.jpg" alt="image">

Recommendations:
  - Add descriptive alt text to all informative images
  - Use alt="" only for decorative images
  - Add width/height to prevent layout shifts
```

## Accessibility Guidelines

- **Informative images**: Describe the content/function
- **Decorative images**: Use empty alt (alt="")
- **Functional images**: Describe the action (e.g., "Search", "Submit")
- **Complex images**: Use longdesc or aria-describedby

## SEO Impact

- Alt text helps search engines understand images
- Improves image search rankings
- Required for Google Images indexing
