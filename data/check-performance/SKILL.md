---
name: check-performance
description: Analyze performance-related HTML issues on web pages. Use when users ask to check page performance, audit resource loading, verify lazy loading, check preload hints, or analyze render-blocking resources. Detects missing optimizations, large resources, render-blocking issues, and Core Web Vitals problems.
---

# Check Performance

Analyze performance-related HTML patterns on web pages.

## Quick Start

```bash
cd /path/to/html-checker/scripts
bun src/check-performance.ts <URL>
```

## CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--verbose` | `-v` | false | Show all resources |
| `--json` | `-j` | false | Output results as JSON |

## Checks Performed

| Check | Impact | Description |
|-------|--------|-------------|
| Render-blocking CSS | High | CSS in head without media query |
| Render-blocking JS | High | Scripts without async/defer |
| No lazy loading | Medium | Images/iframes without loading="lazy" |
| Missing preconnect | Medium | Third-party domains without preconnect |
| Missing preload | Medium | Critical resources not preloaded |
| Large inline styles | Medium | Inline CSS over 14KB |
| Large inline scripts | Medium | Inline JS over 14KB |
| No image dimensions | Medium | Images without width/height (CLS) |
| Unoptimized images | Low | Images without srcset/sizes |
| No resource hints | Low | Missing dns-prefetch for external domains |
| Sync third-party | High | Synchronous third-party scripts |

## Usage Examples

```bash
# Basic check
bun src/check-performance.ts https://example.com

# Verbose output
bun src/check-performance.ts https://example.com --verbose

# JSON output
bun src/check-performance.ts https://example.com --json
```

## Output Example

```
Performance Analysis for https://example.com

Resource Summary:
  Stylesheets: 5 (3 render-blocking)
  Scripts: 12 (4 render-blocking)
  Images: 25 (18 without lazy loading)
  Iframes: 2 (2 without lazy loading)

Critical Issues:
  [HIGH  ] 3 render-blocking CSS files
    - /styles/main.css
    - /styles/vendor.css
    - https://fonts.googleapis.com/css
  [HIGH  ] 4 render-blocking scripts
    - /js/jquery.min.js
    - /js/analytics.js
    - /js/main.js
    - https://third-party.com/widget.js

Optimization Opportunities:
  [MEDIUM] 18 images could use lazy loading
  [MEDIUM] Missing preconnect for 3 domains
    - fonts.googleapis.com
    - third-party.com
    - cdn.example.com
  [MEDIUM] 5 images missing width/height

Resource Hints Found:
  [OK] preconnect: fonts.gstatic.com
  [MISSING] preconnect: third-party.com

Score: 45/100

Recommendations:
  - Add async/defer to non-critical scripts
  - Use media="print" for non-critical CSS
  - Add loading="lazy" to below-fold images
  - Add preconnect for third-party domains
  - Specify width/height on images to prevent CLS
```

## Core Web Vitals Impact

### LCP (Largest Contentful Paint)

- Preload critical resources
- Remove render-blocking resources
- Optimize images

### CLS (Cumulative Layout Shift)

- Set image dimensions
- Reserve space for ads/embeds
- Avoid injecting content above fold

### INP (Interaction to Next Paint)

- Defer non-critical JavaScript
- Break up long tasks
- Use async event handlers

## Quick Fixes

```html
<!-- Preconnect to third-party -->
<link rel="preconnect" href="https://fonts.googleapis.com">

<!-- Defer non-critical CSS -->
<link rel="stylesheet" href="print.css" media="print">

<!-- Async/defer scripts -->
<script src="analytics.js" async></script>
<script src="main.js" defer></script>

<!-- Lazy load images -->
<img src="photo.jpg" loading="lazy" width="800" height="600">
```
