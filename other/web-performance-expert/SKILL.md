---
name: "web-performance-expert"
description: "Master guide for optimizing web application performance. Covers Core Web Vitals (LCP, FID, CLS), asset optimization, caching strategies, and performance auditing."
---

# Web Performance Expert Guide

This skill provides the standards for building lightning-fast web applications that deliver exceptional user experiences.

## 📊 Core Web Vitals (CWV)
- **LCP (Largest Contentful Paint)**: Aim for < 2.5s. Optimize critical path CSS, preload hero images, and use efficient server response times.
- **INP (Interaction to Next Paint)**: Aim for < 200ms. Minimize main thread blocking logic. Use Web Workers for heavy computations.
- **CLS (Cumulative Layout Shift)**: Aim for < 0.1. Set explicit dimensions for images and ads. Avoid inserting content above existing content.

## 🚀 Asset Optimization
- **Images**: Use modern formats (WebP, AVIF). Implement lazy loading and responsive images (`srcset`).
- **Scripts**: Defer or async non-critical scripts. Tree-shake dependencies to reduce bundle size.
- **Fonts**: Use `font-display: swap`. Preload critical web fonts. Favor system fonts where possible.

## 💾 Caching & Networking
- **CDN**: Serve static assets from the edge. Use stale-while-revalidate patterns.
- **Browser Cache**: Set appropriate `Cache-Control` headers. Use versioned filenames (hashing) for long-term caching.
- **Payloads**: Compress responses using Gzip or Brotli. Minify HTML, CSS, and JS.

## 🔍 Auditing & Monitoring
- **Tools**: Use Lighthouse, PageSpeed Insights, and Web Vitals extension for lab data.
- **RUM**: Implement Real User Monitoring to capture field data from actual users.
- **Budgets**: Define performance budgets (e.g., max bundle size, max LCP) and enforce them in CI.

## 🔗 References
- [web.dev - Performance](https://web.dev/learn/performance/)
- [Next.js Performance Optimization](https://nextjs.org/docs/app/building-your-application/optimizing)
