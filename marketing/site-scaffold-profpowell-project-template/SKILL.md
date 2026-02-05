---
name: site-scaffold
description: Generate standardized static site structures. Use when creating new websites, setting up demos, or need consistent site structure with SEO, PWA, and accessibility foundations.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Site Scaffold Skill

Generate standardized static site structures with all essential files for production deployment.

## When to Use

Invoke this skill when:
- Creating a new static website from scratch
- Setting up a demo or prototype site
- Need consistent site structure with SEO, PWA, and accessibility foundations

## Skills to Consider Before Using

| Task | Invoke Skill | Why |
|------|--------------|-----|
| Writing HTML content | **xhtml-author** | XHTML-strict patterns, semantic structure |
| Styling components | **css-author** | Modular CSS, @layer cascade, design tokens |
| Page metadata | **metadata** | SEO, Open Graph, Twitter Cards |
| Icons | **icons** | Use `<x-icon>` component, Lucide library |
| Forms | **forms** | `<form-field>` custom element, validation |
| Patterns/sections | **patterns** | Hero, features, CTA, cards, navigation |

## Standard Site Structure

```
site-name/
├── index.html                    # Homepage
├── about/
│   └── index.html                # About page (folder-based for clean URLs)
├── contact/
│   └── index.html                # Contact page
├── errors/                       # Error and fallback pages
│   ├── 404.html                  # Not found
│   ├── 500.html                  # Server error (inline CSS, no deps)
│   ├── offline.html              # Service worker fallback
│   └── noscript.html             # JS-disabled fallback
├── assets/
│   ├── css/
│   │   ├── main.css              # @import hub only
│   │   ├── _reset.css            # CSS reset
│   │   ├── _tokens.css           # Design tokens (colors, spacing, etc.)
│   │   ├── _base.css             # Base element styles
│   │   ├── _layout.css           # Semantic layout (header, main, footer)
│   │   ├── _utilities.css        # Helper classes
│   │   ├── sections/             # Section-specific styles
│   │   │   ├── _header.css
│   │   │   └── _footer.css
│   │   ├── components/           # Reusable component styles
│   │   │   ├── _skip-link.css
│   │   │   └── _buttons.css
│   │   └── pages/                # Page-specific styles
│   │       ├── _home.css
│   │       └── _error.css
│   ├── js/
│   │   ├── main.js               # Progressive enhancement script
│   │   └── components/           # Web Components
│   │       └── x-icon/           # Icon component
│   └── images/
│       ├── favicon.svg           # Vector favicon (modern browsers)
│       ├── favicon.ico           # Legacy favicon (32x32)
│       ├── apple-touch-icon.png  # iOS icon (180x180)
│       ├── icon-192.png          # PWA icon small
│       ├── icon-512.png          # PWA icon large
│       ├── logo.svg              # Site logo
│       └── og-image.png          # Social sharing (1200x630)
├── .well-known/
│   └── security.txt              # Security contact info (RFC 9116)
├── robots.txt                    # Search engine directives
├── humans.txt                    # Credits and team info
├── sitemap.xml                   # XML sitemap for crawlers
├── manifest.json                 # PWA web app manifest
└── browserconfig.xml             # Windows tile configuration
```

## Required Configuration

When scaffolding, collect these values:

| Variable | Example | Description |
|----------|---------|-------------|
| `SITE_NAME` | Acme Corporation | Display name for title, headers |
| `SITE_URL` | https://acme.example.com | Production URL (no trailing slash) |
| `SITE_DESCRIPTION` | We make quality widgets | Meta description (max 160 chars) |
| `SITE_AUTHOR` | Acme Inc | Author or organization |
| `SITE_EMAIL` | hello@acme.example.com | Contact email |
| `THEME_COLOR` | #1e40af | Primary brand color (hex) |
| `BACKGROUND_COLOR` | #ffffff | PWA background (hex) |
| `CURRENT_YEAR` | 2025 | For copyright notices |

## HTML Template Structure

All HTML pages must follow XHTML-strict patterns:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>

  <!-- Primary Meta -->
  <title>Page Title - {{SITE_NAME}}</title>
  <meta name="description" content="{{SITE_DESCRIPTION}}"/>
  <meta name="author" content="{{SITE_AUTHOR}}"/>
  <meta name="referrer" content="strict-origin-when-cross-origin"/>
  <meta name="robots" content="index, follow"/>

  <!-- Canonical URL -->
  <link rel="canonical" href="{{SITE_URL}}/"/>

  <!-- Favicon Set -->
  <link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml"/>
  <link rel="icon" href="/assets/images/favicon.ico" sizes="32x32"/>
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png"/>

  <!-- PWA -->
  <link rel="manifest" href="/manifest.json"/>
  <meta name="theme-color" content="{{THEME_COLOR}}"/>

  <!-- Open Graph -->
  <meta property="og:type" content="website"/>
  <meta property="og:url" content="{{SITE_URL}}/"/>
  <meta property="og:site_name" content="{{SITE_NAME}}"/>
  <meta property="og:title" content="Page Title"/>
  <meta property="og:description" content="{{SITE_DESCRIPTION}}"/>
  <meta property="og:image" content="{{SITE_URL}}/assets/images/og-image.png"/>

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="Page Title"/>
  <meta name="twitter:description" content="{{SITE_DESCRIPTION}}"/>
  <meta name="twitter:image" content="{{SITE_URL}}/assets/images/og-image.png"/>

  <!-- Styles -->
  <link rel="stylesheet" href="/assets/css/main.css"/>
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>

  <header>
    <!-- Site header with logo and navigation -->
  </header>

  <main id="main">
    <!-- Page content -->
  </main>

  <footer>
    <!-- Site footer -->
  </footer>

  <script src="/assets/js/main.js" defer=""></script>
</body>
</html>
```

## CSS Structure

Use modular @import with @layer for cascade control. The main.css file is an import hub only:

### main.css (Hub File)

```css
/**
 * {{SITE_NAME}} - Main Stylesheet
 * Modular CSS architecture with @layer cascade control
 */

@layer reset, tokens, base, layout, sections, components, pages, utilities;

/* Core */
@import "_reset.css" layer(reset);
@import "_tokens.css" layer(tokens);
@import "_base.css" layer(base);
@import "_layout.css" layer(layout);

/* Sections */
@import "sections/_header.css" layer(sections);
@import "sections/_footer.css" layer(sections);

/* Components */
@import "components/_skip-link.css" layer(components);
@import "components/_buttons.css" layer(components);

/* Pages */
@import "pages/_home.css" layer(pages);
@import "pages/_error.css" layer(pages);

/* Utilities */
@import "_utilities.css" layer(utilities);
```

### Layer Responsibilities

| Layer | Purpose | Examples |
|-------|---------|----------|
| reset | Normalize browser defaults | box-sizing, margin resets |
| tokens | Design tokens | colors, spacing, typography |
| base | Default element styles | body, headings, links |
| layout | Semantic containers | header, main, footer, section |
| sections | Page section styles | hero, features, cta |
| components | Reusable UI patterns | buttons, cards, forms |
| pages | Page-specific overrides | home, about, error |
| utilities | Helper classes | visually-hidden, skip-link |

### _tokens.css Example

```css
@layer tokens {
  :root {
    /* Colors */
    --color-primary: {{THEME_COLOR}};
    --color-primary-dark: color-mix(in srgb, var(--color-primary) 80%, black);
    --color-secondary: #059669;
    --color-text: #1f2937;
    --color-text-light: #6b7280;
    --color-bg: #ffffff;
    --color-bg-alt: #f3f4f6;
    --color-border: #e5e7eb;

    /* Spacing */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 2rem;
    --space-xl: 4rem;

    /* Typography */
    --font-family: system-ui, -apple-system, sans-serif;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.25rem;
    --font-size-xl: 1.5rem;
    --font-size-2xl: 2rem;
    --font-size-3xl: 2.5rem;

    /* Layout */
    --max-width: 1200px;
    --border-radius: 6px;
  }
}
```

## JavaScript Pattern

Use DOMContentLoaded with init function:

```javascript
/**
 * Site initialization
 * Progressive enhancement - site works without JS
 */
document.addEventListener('DOMContentLoaded', init);

function init() {
  initNavigation();
  initForms();
}

function initNavigation() {
  // Mobile menu, dropdowns, etc.
}

function initForms() {
  // Form validation, submission handling
}
```

## robots.txt Template

```
# Robots.txt for {{SITE_NAME}}
# {{SITE_URL}}/robots.txt

User-agent: *
Allow: /

# Block error pages
Disallow: /errors/

# Sitemaps
Sitemap: {{SITE_URL}}/sitemap.xml
```

## sitemap.xml Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{{SITE_URL}}/</loc>
    <lastmod>{{CURRENT_DATE}}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{{SITE_URL}}/about/</loc>
    <lastmod>{{CURRENT_DATE}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

## humans.txt Template

```
/* TEAM */
Site: {{SITE_NAME}}
Contact: {{SITE_EMAIL}}

/* SITE */
Last update: {{CURRENT_DATE}}
Language: English
Standards: HTML5, CSS3, JavaScript ES6+
```

## manifest.json Template

```json
{
  "name": "{{SITE_NAME}}",
  "short_name": "{{SITE_SHORT_NAME}}",
  "description": "{{SITE_DESCRIPTION}}",
  "start_url": "/",
  "display": "standalone",
  "background_color": "{{BACKGROUND_COLOR}}",
  "theme_color": "{{THEME_COLOR}}",
  "icons": [
    {
      "src": "/assets/images/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/assets/images/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## browserconfig.xml Template

```xml
<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square150x150logo src="/assets/images/icon-192.png"/>
      <TileColor>{{THEME_COLOR}}</TileColor>
    </tile>
  </msapplication>
</browserconfig>
```

## security.txt Template

Place in `.well-known/security.txt` (RFC 9116):

```
# Security contact for {{SITE_NAME}}
# {{SITE_URL}}/.well-known/security.txt

Contact: mailto:security@example.com
Expires: 2026-12-31T23:59:00.000Z
Preferred-Languages: en
Canonical: {{SITE_URL}}/.well-known/security.txt

# Optional
Policy: {{SITE_URL}}/security-policy
Acknowledgments: {{SITE_URL}}/security-thanks
```

**Required fields:**
- `Contact:` - Email or URL for security reports
- `Expires:` - ISO 8601 date (must be renewed annually)

## Error Pages

All error pages go in the `errors/` directory.

### errors/404.html
- Friendly message explaining page not found
- Link back to homepage
- Same header/footer as main site
- Search functionality (optional)

### errors/500.html
- Apologetic message for server error
- **Inline critical CSS** (no external stylesheet dependency)
- Contact information for support
- No dynamic content

### errors/offline.html

Service worker fallback with inline styles:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Offline - {{SITE_NAME}}</title>
  <meta name="robots" content="noindex"/>
  <style>
    body {
      font-family: system-ui, -apple-system, sans-serif;
      max-width: 600px;
      margin: 4rem auto;
      padding: 1rem;
      text-align: center;
      color: #1f2937;
    }
    h1 { color: #4b5563; }
    .icon { font-size: 4rem; margin-bottom: 1rem; }
    a { color: #2563eb; }
  </style>
</head>
<body>
  <div class="icon" aria-hidden="true">📡</div>
  <h1>You're Offline</h1>
  <p>It looks like you've lost your internet connection.</p>
  <p>Please check your connection and <a href="/">try again</a>.</p>
</body>
</html>
```

Register in service worker:

```javascript
const OFFLINE_PAGE = '/errors/offline.html';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('offline-v1').then((cache) => cache.add(OFFLINE_PAGE))
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(OFFLINE_PAGE))
    );
  }
});
```

### errors/noscript.html

Fallback for JavaScript-required applications:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>JavaScript Required - {{SITE_NAME}}</title>
  <meta name="robots" content="noindex"/>
  <style>
    body {
      font-family: system-ui, -apple-system, sans-serif;
      max-width: 600px;
      margin: 4rem auto;
      padding: 1rem;
      text-align: center;
      color: #1f2937;
    }
    h1 { color: #4b5563; }
    .icon { font-size: 4rem; margin-bottom: 1rem; }
    a { color: #2563eb; }
    code { background: #f3f4f6; padding: 0.2em 0.4em; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="icon" aria-hidden="true">⚙️</div>
  <h1>JavaScript Required</h1>
  <p>This application requires JavaScript to function properly.</p>
  <p>Please enable JavaScript in your browser settings and <a href="/">reload the page</a>.</p>

  <details>
    <summary>How to enable JavaScript</summary>
    <ul style="text-align: left;">
      <li><strong>Chrome:</strong> Settings → Privacy and security → Site settings → JavaScript</li>
      <li><strong>Firefox:</strong> Type <code>about:config</code> in address bar, search for <code>javascript.enabled</code></li>
      <li><strong>Safari:</strong> Preferences → Security → Enable JavaScript</li>
      <li><strong>Edge:</strong> Settings → Cookies and site permissions → JavaScript</li>
    </ul>
  </details>
</body>
</html>
```

Use with `<noscript>` redirect:

```html
<head>
  <noscript>
    <meta http-equiv="refresh" content="0; url=/errors/noscript.html"/>
  </noscript>
</head>
```

## Favicon Requirements

| File | Size | Purpose |
|------|------|---------|
| favicon.svg | Vector | Modern browsers, scales perfectly |
| favicon.ico | 32x32 | Legacy browser support |
| apple-touch-icon.png | 180x180 | iOS home screen |
| icon-192.png | 192x192 | Android/PWA small |
| icon-512.png | 512x512 | Android/PWA large, splash |
| og-image.png | 1200x630 | Social sharing preview |

## Checklist

When scaffolding a new site:

### Core Files
- [ ] Create directory structure
- [ ] Generate index.html with full meta tags
- [ ] Create about/index.html and contact/index.html
- [ ] Create robots.txt with sitemap reference
- [ ] Create sitemap.xml with all pages
- [ ] Create humans.txt with team info
- [ ] Create manifest.json for PWA
- [ ] Create browserconfig.xml for Windows

### Error & Fallback Pages
- [ ] Generate errors/404.html
- [ ] Generate errors/500.html (inline CSS, no external deps)
- [ ] Create errors/offline.html for service worker
- [ ] Create errors/noscript.html (if app requires JavaScript)

### Security
- [ ] Create .well-known/security.txt with contact info

### Assets
- [ ] Set up modular CSS with @layer and @import
- [ ] Set up JS with init pattern
- [ ] Create/copy favicon set
- [ ] Create og-image.png for social sharing
- [ ] Copy x-icon component to assets/js/components/

### Validation
- [ ] Validate all HTML files pass linters
- [ ] Test error pages render correctly
- [ ] Verify security.txt is accessible at /.well-known/security.txt

## Related Skills

- **xhtml-author** - Write valid XHTML-strict HTML5 markup
- **css-author** - Modern CSS organization with native @import, @layer cascade
- **metadata** - HTML metadata and head content
- **performance** - Write performance-friendly HTML pages
- **icons** - Lucide icons with `<x-icon>` component
- **patterns** - Reusable section and component patterns
