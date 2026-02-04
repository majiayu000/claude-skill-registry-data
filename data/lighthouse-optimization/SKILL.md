---
name: lighthouse-optimization
description: Optimize web applications to achieve 95%+ Lighthouse scores across all categories. Use when optimizing performance, accessibility, best practices, or SEO for web applications.
---

# Lighthouse Optimization

## Overview

This skill covers comprehensive optimization techniques to achieve 95%+ scores in all Lighthouse categories: Performance, Accessibility, Best Practices, and SEO.

## Target Scores

- **Performance**: ≥ 95%
- **Accessibility**: ≥ 95%
- **Best Practices**: ≥ 95%
- **SEO**: ≥ 95%

## Performance Optimization

### Core Web Vitals

**Target Metrics**:
- **FCP (First Contentful Paint)**: < 1.8s
- **LCP (Largest Contentful Paint)**: < 2.5s
- **TBT (Total Blocking Time)**: < 200ms
- **CLS (Cumulative Layout Shift)**: < 0.1
- **Speed Index**: < 3.4s

### Optimization Strategies

1. **Minimize JavaScript Execution**
   - Code splitting
   - Lazy loading
   - Tree shaking

2. **Optimize Asset Loading**
   - Preload critical resources
   - Defer non-critical resources
   - Use efficient cache lifetimes

3. **Reduce Main Thread Blocking**
   - Minimize synchronous operations
   - Use Web Workers for heavy computations
   - Optimize WASM loading

## Accessibility Optimization

### Critical Issues

#### 1. Touch Targets

**Requirement**: All interactive elements ≥ 48x48px

```css
.btn, .tab, button {
    min-width: 48px;
    min-height: 48px;
    padding: 12px 16px;
    margin: 4px; /* Spacing between targets */
}
```

#### 2. Semantic HTML

**Required Elements**:
- `<html lang="en">` - Language attribute
- `<main role="main">` - Main landmark
- `<header role="banner">` - Header landmark
- `<footer role="contentinfo">` - Footer landmark

#### 3. ARIA Labels

Add ARIA labels for screen readers:

```rust
rsx! {
    button {
        aria_label: "Add new reminder",
        onclick: move |_| { /* ... */ },
        "+ New Reminder"
    }
}
```

#### 4. Heading Hierarchy

Ensure proper heading structure:
- One `<h1>` per page
- Sequential heading levels (h1 → h2 → h3)
- No skipping levels

### Accessibility Checklist

- [ ] All touch targets ≥ 48x48px
- [ ] Minimum 8px spacing between touch targets
- [ ] `<html>` has `lang` attribute
- [ ] `<main>` landmark present
- [ ] Proper heading hierarchy
- [ ] ARIA labels for interactive elements
- [ ] Color contrast ratio ≥ 4.5:1
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

## Best Practices Optimization

### Console Errors

**Fix all console errors**:
- Handle all error cases
- Remove debug logs in production
- Fix WASM loading errors
- Fix CSS 404 errors

### Source Maps

**Enable source maps** for debugging:

```toml
[profile.wasm-release]
debug = true  # Enable source maps
```

### Security Headers

**Implement security headers**:
- Content Security Policy (CSP)
- HSTS (if using HTTPS)
- COOP (Cross-Origin-Opener-Policy)
- X-Frame-Options

## SEO Optimization

### Required Elements

1. **Meta Tags**:
```rust
rsx! {
    head {
        meta { charset: "utf-8" }
        meta { name: "viewport", content: "width=device-width, initial-scale=1.0" }
        meta { name: "description", content: "A simple and elegant reminder app" }
        title { "Remind Me PWA - Your Personal Reminder Assistant" }
    }
}
```

2. **Open Graph Tags** (optional but recommended):
```rust
meta { property: "og:title", content: "Remind Me PWA" }
meta { property: "og:description", content: "A simple and elegant reminder app" }
meta { property: "og:type", content: "website" }
```

3. **Structured Data** (optional):
- JSON-LD for better search results

## Implementation Patterns

### HTML Structure

```rust
rsx! {
    html {
        lang: "en",
        head {
            meta { charset: "utf-8" }
            meta { name: "viewport", content: "width=device-width, initial-scale=1.0" }
            meta { name: "description", content: "App description" }
            title { "App Title" }
            link { rel: "stylesheet", href: "assets/style.css" }
            link { rel: "manifest", href: "assets/manifest.json" }
        }
        body {
            header {
                role: "banner",
                // Header content
            }
            main {
                role: "main",
                // Main content
            }
        }
    }
}
```

### Touch Target CSS

```css
:root {
    --touch-target-min: 48px;
    --touch-target-spacing: 8px;
}

.btn, .tab, button {
    min-width: var(--touch-target-min);
    min-height: var(--touch-target-min);
    padding: 12px 16px;
    margin: var(--touch-target-spacing);
}
```

### Service Worker Optimization

```javascript
const CACHE_NAME = 'remind-me-pwa-v2';
const urlsToCache = [
  '/remind-me-pwa/',
  '/remind-me-pwa/index.html',
  '/remind-me-pwa/assets/style.css',
  '/remind-me-pwa/assets/manifest.json',
  '/remind-me-pwa/wasm/remind-me-pwa.wasm',
  '/remind-me-pwa/wasm/remind-me-pwa.js'
];

// Cache with efficient lifetimes
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request).then((fetchResponse) => {
                // Cache static assets with long lifetime
                if (event.request.url.includes('/assets/') || 
                    event.request.url.includes('/wasm/')) {
                    const responseToCache = fetchResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return fetchResponse;
            });
        })
    );
});
```

## Testing and Validation

### Lighthouse Audit Process

1. **Run Audit**:
   - Open Chrome DevTools
   - Go to Lighthouse tab
   - Select categories
   - Run audit

2. **Review Results**:
   - Check all scores
   - Review failing audits
   - Note opportunities

3. **Fix Issues**:
   - Address critical issues first
   - Fix accessibility issues
   - Optimize performance bottlenecks

4. **Re-audit**:
   - Run audit again
   - Verify improvements
   - Target 95%+ in all categories

### Automated Testing

```bash
# Install Lighthouse CI
npm install -g @lhci/cli

# Run Lighthouse CI
lhci autorun
```

## Common Issues and Solutions

### Issue: Touch Targets Too Small

**Solution**:
- Increase min-width/min-height to 48px
- Add padding to increase touch area
- Add spacing between elements

### Issue: Missing Main Landmark

**Solution**:
- Wrap main content in `<main>` element
- Add `role="main"` attribute

### Issue: Missing Lang Attribute

**Solution**:
- Add `lang="en"` to `<html>` element
- Use appropriate language code

### Issue: CSS 404 Error

**Solution**:
- Verify CSS path matches `base_path`
- Check file exists in build output
- Update service worker cache URLs

### Issue: Console Errors

**Solution**:
- Fix all JavaScript/WASM errors
- Handle error cases gracefully
- Remove debug logs

## Best Practices

### DO:
- ✅ Always test with Lighthouse before release
- ✅ Fix accessibility issues immediately
- ✅ Optimize performance continuously
- ✅ Use semantic HTML
- ✅ Ensure proper touch target sizes
- ✅ Add all required meta tags
- ✅ Fix console errors

### DON'T:
- ❌ Don't ignore Lighthouse warnings
- ❌ Don't skip accessibility fixes
- ❌ Don't use small touch targets
- ❌ Don't forget semantic HTML
- ❌ Don't leave console errors
- ❌ Don't skip source maps

## Resources

- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/)
- [Web.dev Performance](https://web.dev/performance/)
- [Web.dev Accessibility](https://web.dev/accessible/)
- [Core Web Vitals](https://web.dev/vitals/)

