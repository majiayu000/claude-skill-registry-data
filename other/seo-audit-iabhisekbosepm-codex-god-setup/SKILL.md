---
name: seo-audit
description: "Run a technical SEO audit: crawlability, meta tags, structured data, Core Web Vitals, content issues."
argument-hint: "[url-or-path]"
allowed-tools: Read Grep Glob Bash
model: gpt-5.3-codex
---

# /seo-audit — Technical SEO Audit

Audit: **$ARGUMENTS**. See `agents/seo-specialist.md`.

1. **Technical** — robots.txt, meta robots, canonicals, redirects (max 2 hops), internal links
2. **On-page** — Titles (<60 chars), meta descriptions (<160 chars), heading hierarchy (single H1), image alt text, URL structure
3. **Structured data** — JSON-LD validation, schema.org compliance
4. **Core Web Vitals** — LCP <2.5s, FID <100ms, CLS <0.1. Cross-ref `agents/performance-optimizer.md`.
5. **Content** — Thin pages, duplicate content, orphan pages, keyword cannibalization
6. **Priority fix list** — Implementable recommendations only. No SEO folklore.
