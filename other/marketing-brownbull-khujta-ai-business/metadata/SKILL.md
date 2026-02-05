---
name: metadata
description: HTML metadata and head content. Use when writing or reviewing page head sections including SEO, social sharing, performance hints, and bot control.
allowed-tools: Read, Write, Edit, Bash
---

# Metadata Skill

This skill provides guidance for writing complete, well-structured HTML `<head>` content. It covers essential meta tags, social sharing, performance optimization, and bot control.

## Quick Reference Template

Copy this template and customize for each page:

```html
<head>
  <!-- Essential (order matters) -->
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Page Title - Site Name</title>
  <meta name="description" content="Concise page description (150-160 chars)."/>

  <!-- Canonical URL -->
  <link rel="canonical" href="https://example.com/page"/>

  <!-- Authorship -->
  <meta name="author" content="Author Name"/>

  <!-- Bot Control -->
  <meta name="robots" content="index, follow"/>

  <!-- Open Graph (Social Sharing) -->
  <meta property="og:title" content="Page Title"/>
  <meta property="og:description" content="Description for social sharing."/>
  <meta property="og:image" content="https://example.com/images/share.jpg"/>
  <meta property="og:url" content="https://example.com/page"/>
  <meta property="og:type" content="website"/>
  <meta property="og:site_name" content="Site Name"/>

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image"/>

  <!-- Performance Hints -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="dns-prefetch" href="//analytics.example.com"/>

  <!-- Theme -->
  <meta name="theme-color" content="#ffffff"/>

  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico" sizes="32x32"/>
  <link rel="icon" href="/icon.svg" type="image/svg+xml"/>
  <link rel="apple-touch-icon" href="/apple-touch-icon.png"/>

  <!-- Stylesheets -->
  <link rel="stylesheet" href="/styles/main.css"/>
</head>
```

---

## Element Order in `<head>`

Order matters for performance and correctness:

1. `<meta charset>` - **Must be first** (within first 1024 bytes)
2. `<meta name="viewport">` - Before any CSS
3. `<title>` - Early for perceived performance
4. `<meta name="description">` - SEO critical
5. `<link rel="canonical">` - URL normalization
6. Other meta tags (author, robots, etc.)
7. Open Graph / Twitter meta
8. Performance hints (preconnect, dns-prefetch)
9. Favicon links
10. Stylesheets
11. Scripts (usually at end of body, but critical JS here)

---

## Metadata Categories

### 1. Essential (Required for All Pages)

| Element | Purpose | Notes |
|---------|---------|-------|
| `<meta charset="utf-8"/>` | Character encoding | Must be first element |
| `<meta name="viewport" content="width=device-width, initial-scale=1"/>` | Responsive design | Required for mobile |
| `<title>Page - Site</title>` | Browser tab, search results | 50-60 characters max |
| `<meta name="description" content="..."/>` | Search snippets | 150-160 characters |

**Example:**
```html
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Widget Pro - DemoCompany</title>
<meta name="description" content="The Widget Pro offers enhanced durability and a 5-year warranty. Our best-selling widget for professional use."/>
```

### 2. Authorship & Attribution

| Element | Purpose |
|---------|---------|
| `<meta name="author" content="..."/>` | Content author |
| `<link rel="canonical" href="..."/>` | Authoritative URL (prevents duplicate content) |
| `<meta name="generator" content="..."/>` | CMS/tool that generated the page |
| `<meta name="copyright" content="..."/>` | Copyright notice |

**Example:**
```html
<meta name="author" content="DemoCompany Editorial Team"/>
<link rel="canonical" href="https://democompany.com/products/widget-pro"/>
```

### 3. Bot Control (Robots)

| Directive | Meaning |
|-----------|---------|
| `index` | Allow indexing (default) |
| `noindex` | Prevent indexing |
| `follow` | Follow links (default) |
| `nofollow` | Don't follow links |
| `noarchive` | Don't cache the page |
| `nosnippet` | Don't show text snippets |
| `noimageindex` | Don't index images |

**Examples:**
```html
<!-- Standard public page -->
<meta name="robots" content="index, follow"/>

<!-- Private/internal page -->
<meta name="robots" content="noindex, nofollow"/>

<!-- Legal page (index but don't cache) -->
<meta name="robots" content="index, follow, noarchive"/>

<!-- Search results page -->
<meta name="robots" content="noindex, follow"/>
```

**Google-specific:**
```html
<meta name="googlebot" content="notranslate"/>
```

### 4. Open Graph (Social Sharing)

Required for rich social media previews on Facebook, LinkedIn, etc.

| Property | Purpose | Recommended |
|----------|---------|-------------|
| `og:title` | Share title | 60 characters |
| `og:description` | Share description | 200 characters |
| `og:image` | Share image | 1200x630px |
| `og:url` | Canonical URL | Absolute URL |
| `og:type` | Content type | website, article, product |
| `og:site_name` | Site name | Brand name |

**Example:**
```html
<meta property="og:title" content="Widget Pro - Professional Grade Widget"/>
<meta property="og:description" content="Enhanced durability, 5-year warranty. Perfect for professional use."/>
<meta property="og:image" content="https://democompany.com/images/widget-pro-share.jpg"/>
<meta property="og:url" content="https://democompany.com/products/widget-pro"/>
<meta property="og:type" content="product"/>
<meta property="og:site_name" content="DemoCompany"/>
```

**Article-specific:**
```html
<meta property="og:type" content="article"/>
<meta property="article:published_time" content="2024-01-15T08:00:00Z"/>
<meta property="article:modified_time" content="2024-01-20T10:30:00Z"/>
<meta property="article:author" content="Jane Smith"/>
<meta property="article:section" content="Technology"/>
```

### 5. Twitter Cards

| Property | Purpose |
|----------|---------|
| `twitter:card` | Card type: summary, summary_large_image, player |
| `twitter:site` | @username of website |
| `twitter:creator` | @username of author |

**Example:**
```html
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:site" content="@democompany"/>
<meta name="twitter:creator" content="@janesmith"/>
```

### 6. Network Performance Hints

| Element | Purpose | When to Use |
|---------|---------|-------------|
| `<link rel="dns-prefetch">` | Pre-resolve DNS | Third-party domains |
| `<link rel="preconnect">` | Establish early connection | Critical third-parties |
| `<link rel="preload">` | High-priority fetch | Fonts, critical CSS |
| `<link rel="prefetch">` | Low-priority fetch | Next-page resources |
| `<link rel="prerender">` | Pre-render entire page | Very likely next page |

**Examples:**
```html
<!-- DNS prefetch for analytics -->
<link rel="dns-prefetch" href="//www.google-analytics.com"/>

<!-- Preconnect for fonts (includes DNS + TCP + TLS) -->
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>

<!-- Preload critical font -->
<link rel="preload" href="/fonts/brand.woff2" as="font" type="font/woff2" crossorigin="anonymous"/>

<!-- Preload critical CSS -->
<link rel="preload" href="/css/critical.css" as="style"/>

<!-- Prefetch likely next page -->
<link rel="prefetch" href="/products/widget-pro"/>
```

### 7. Security

| Element | Purpose |
|---------|---------|
| `<meta name="referrer">` | Control referrer information |
| `<meta http-equiv="Content-Security-Policy">` | Inline CSP (prefer HTTP header) |

**Referrer values:**
- `no-referrer` - Never send referrer
- `origin` - Send only origin (domain)
- `strict-origin-when-cross-origin` - Full URL same-origin, origin cross-origin (recommended)

**Example:**
```html
<meta name="referrer" content="strict-origin-when-cross-origin"/>
```

### 8. Mobile & PWA

| Element | Purpose |
|---------|---------|
| `<meta name="theme-color">` | Browser chrome color |
| `<meta name="apple-mobile-web-app-capable">` | iOS standalone mode |
| `<meta name="apple-mobile-web-app-status-bar-style">` | iOS status bar |
| `<link rel="manifest">` | PWA manifest |

**Example:**
```html
<meta name="theme-color" content="#1a73e8"/>
<meta name="apple-mobile-web-app-capable" content="yes"/>
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
<link rel="manifest" href="/manifest.json"/>
```

### 9. Favicon

Modern favicon setup:

```html
<!-- Standard favicon -->
<link rel="icon" href="/favicon.ico" sizes="32x32"/>

<!-- SVG favicon (modern browsers) -->
<link rel="icon" href="/icon.svg" type="image/svg+xml"/>

<!-- Apple touch icon -->
<link rel="apple-touch-icon" href="/apple-touch-icon.png"/>

<!-- Web app manifest (includes icons) -->
<link rel="manifest" href="/manifest.webmanifest"/>
```

---

## Page Type Profiles

Different pages need different metadata:

### Homepage
```html
<meta name="robots" content="index, follow"/>
<meta property="og:type" content="website"/>
<!-- Include full Open Graph set -->
<!-- Include performance hints for common resources -->
```

### Article/Blog Post
```html
<meta name="author" content="Author Name"/>
<meta name="robots" content="index, follow"/>
<meta property="og:type" content="article"/>
<meta property="article:published_time" content="2024-01-15T08:00:00Z"/>
<meta property="article:author" content="Author Name"/>
```

### Product Page
```html
<meta name="robots" content="index, follow"/>
<meta property="og:type" content="product"/>
<meta property="product:price:amount" content="79.99"/>
<meta property="product:price:currency" content="USD"/>
```

### Legal/Policy Pages
```html
<meta name="robots" content="noindex, follow"/>
<!-- Or if should be indexed: -->
<meta name="robots" content="index, follow, noarchive"/>
```

### Search Results
```html
<meta name="robots" content="noindex, follow"/>
```

### Error Pages (404, 500)
```html
<meta name="robots" content="noindex, follow"/>
```

---

## Validation

Run metadata validation:

```bash
npm run lint:meta
```

The validator checks:
- Required elements present
- Elements in correct order
- Content meets length requirements
- URLs are absolute where required
- Image dimensions adequate for social sharing

---

## Common Mistakes

### 1. Charset Not First
```html
<!-- Wrong -->
<title>Page</title>
<meta charset="utf-8"/>

<!-- Correct -->
<meta charset="utf-8"/>
<title>Page</title>
```

### 2. Relative URLs in Open Graph
```html
<!-- Wrong -->
<meta property="og:image" content="/images/share.jpg"/>

<!-- Correct -->
<meta property="og:image" content="https://example.com/images/share.jpg"/>
```

### 3. Missing Viewport
Results in pages rendering at desktop width on mobile.

### 4. Duplicate Titles/Descriptions
Each page should have unique title and description.

### 5. Title Too Long
Search engines truncate after ~60 characters. Put important words first.

### 6. Missing Canonical
Can cause duplicate content issues, especially with URL parameters.

---

## Extensibility

Metadata profiles are defined in JSON files in `profiles/`:

```json
{
  "name": "article",
  "extends": "default",
  "required": [
    { "name": "author" },
    { "property": "article:published_time" }
  ],
  "recommended": [
    { "property": "article:author" },
    { "property": "article:section" },
    { "property": "article:tag" }
  ]
}
```

Create custom profiles by:
1. Adding a new JSON file to `profiles/`
2. Setting `extends` to inherit from another profile
3. Adding `required` and `recommended` arrays

## Related Skills

- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **performance** - Write performance-friendly HTML pages
- **security** - Write secure web pages and applications
- **i18n** - Write internationalization-friendly HTML pages
