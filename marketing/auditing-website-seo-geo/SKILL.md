---
name: auditing-website-seo-geo
description: Audits a site's SEO and AI-search (GEO) readiness — meta tags, Open Graph/Twitter, JSON-LD, robots/llms conventions — and generates fixes. Use when reviewing search visibility, social previews, structured data, or LLM/AI-crawler discoverability.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
  argument-hint: [url-or-file-path]
  stability: stable
  content-hash: sha256:6fc16d33ad7c663af30e578ac2b6fe93b1737781ec4df878ac84c2a52ff3515b
  last-verified-cc-version: 1.0.34
---

# Website SEO & GEO Audit

**Target**: $ARGUMENTS

Audits a site for traditional SEO and Generative-Engine Optimization (GEO —
visibility in AI search such as ChatGPT, Perplexity, Gemini, and Google AI
Overviews) and generates implementable fixes. Prefer configuring the site or
static-site generator so tags are emitted once (DRY) over hand-stuffing meta
into every page. No over-analysis.

## Audit Areas

### Core meta

- `<title>` (~30-60 chars, unique per page), `<meta name="description">`
  (~120-160 chars, entity-clear), `lang` on `<html>`, `charset`, `viewport`
  (no `maximum-scale` — it blocks zoom), `robots`, `author`, `keywords`,
  `format-detection`, and a `canonical` link.

### Open Graph & Twitter Card

- `og:title`, `og:description`, `og:url`, `og:type`, `og:site_name`, `og:image`.
- `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`,
  `twitter:site`, `twitter:creator`.

### Structured data (JSON-LD)

- `WebSite` / `Organization` (name, url, logo, sameAs) and per-page
  `Article` / `BlogPosting` (headline, description, datePublished, author,
  publisher, image). Validate against the matching schema.org type.

### GEO / AI-search

- `robots.txt` AI user-agents (GPTBot, ClaudeBot, Google-Extended, CCBot,
  PerplexityBot, OAI-SearchBot) — the highest-leverage, best-honored lever.
- `llms.txt` at root — cheap, uncertain adoption; fine to keep.
- Entity clarity, key info in the first ~160 chars, Q&A-friendly phrasing,
  explicit brand / product / service names.

## Static-site-generator pitfalls (verify, do not assume)

- **Do not double-emit.** If an SSG plugin emits OG/Twitter/JSON-LD (e.g.
  jekyll-seo-tag, Next SEO), do NOT also hand-write those tags — duplicates
  result. Configure the plugin instead.
- **Plugins emit conditionally.** Twitter Card tags often need a configured
  handle; `twitter:description` and `og:image` / `twitter:image` may not be
  emitted without explicit config or a per-page image. Fill only the genuine
  gaps in a single shared include.

## Known-unwinnable conflicts (flag, do not chase)

Some checkers want mutually-exclusive lengths on a single shared tag:

- `og:title` 25-35 vs `twitter:title` 50-70 — same tag, cannot satisfy both.
- `og:description` 55-65 vs `<meta name="description">` 120-160 — same tag.

Recommend the real-world optimum (Google limits plus GEO: a ~50-char title and
a ~150-char description) and note the tradeoff rather than ping-ponging.

## Reality check

- **ai.txt / `/.well-known/ai.txt`** is not a recognized standard (competing
  vendor proposals, no IANA `.well-known` registration, no major adopter).
  Skip it; do not spend effort on `/.well-known/ai.txt`.
- A complete `robots.txt` AI-agent policy plus a full OG/JSON-LD set are what
  actually move GEO and social previews.

## Workflow

1. **Identify scope** from $ARGUMENTS (URL, file, or directory). For a URL,
   fetch the rendered `<head>` — converting tools return markdown, so fetch
   raw HTML when you need the tags verbatim.
2. **Inventory** the tags present versus the audit areas above; detect
   duplicates.
3. **Classify** findings: HIGH (title, description, canonical, OG core),
   MEDIUM (Twitter, JSON-LD, keywords), LOW (format-detection, author).
4. **Generate fixes** — prefer SSG config plus a single shared include over
   per-page tags.
5. **Verify** by re-fetching the built output, not the raw templates.

## Output Format

### Findings

```text
HIGH
- [Tag/issue] - Current: [value or "missing"] - Page: [url/path]
  Fix: [code/config snippet]

MEDIUM / LOW
- [Tag/issue] - Current: [value or "missing"]
  Fix: [code/config snippet]
```

### Implementation Checklist

```text
- [ ] [Fix] - Impact: [High/Medium/Low] - scope: [site-wide | per-page]
```

## Rules

- Configure once (DRY); do not hand-stuff tags an SSG already emits.
- Flag mutually-exclusive checker targets instead of chasing impossible green.
- Optimize for real engines and GEO, not vanity checker scores.
- Every finding includes a concrete, implementable fix.
- Keep output concise: findings + fixes + checklist only.

## Further Reading

- [The Open Graph protocol](https://ogp.me/)
- [schema.org Article](https://schema.org/Article)
- [Google Search Central — structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [llms.txt proposal](https://llmstxt.org/)
