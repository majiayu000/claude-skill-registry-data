---
name: seo-aeo-best-practices
version: 1.0.0
description: "SEO, GEO, and AEO best practices knowledge base — 9 on-demand reference files covering technical SEO (metadata, sitemaps, CWV, hreflang, AI crawlers), structured data (JSON-LD templates for Article/FAQ/HowTo/Organization/Product/Breadcrumb/Person/Event), E-E-A-T principles (Quality Rater signals + implementation), AEO (featured snippets, PAA, voice search, knowledge panels, extraction zones), GEO (AI citation optimization, entity authority, platform-specific for ChatGPT/Perplexity/Claude/Gemini, measurement tools), content architecture (pillar/cluster, internal linking, topical authority), an integration checklist for content-critique scoring, a content production guideline (BLUF writing, extraction zones, question headings, quantitative claims, GEO rules), and a website metadata spec (copy-paste-ready title/OG/Twitter/canonical/hreflang/sitemap/robots.txt/all JSON-LD templates/CWV/URL structure). Use when implementing page SEO, schema markup, international SEO, AI-overview readiness, improving content for Google/ChatGPT/Perplexity/Claude/Gemini, auditing content for the SEO & Value critique dimension, or building any production website."
---

# SEO, GEO & AEO Best Practices

Pure reference layer. No workflows, no agents — knowledge files that other skills and pipelines consume on demand.

## Boundaries

Do NOT load these reference files if what you need is:
- Core Web Vitals browser measurement with DevTools traces → `/web-perf`
- Vietnamese SEO (diacritics, CocCoc, regional vocabulary) → `vietnamese-language/references/seo-content-marketing.md`
- Content draft creation or copywriting formulas → `/content-creator`
- Full content pipeline (research/strategy/create/critique) → `/pipeline-content`
- Full SEO/GEO/AEO audit pipeline with scoring → `/pipeline-seo-geo-aeo`

This skill provides: actionable implementation checklists, JSON-LD schema templates, E-E-A-T signal guidance, AI citation optimization patterns, content architecture blueprints, and the SEO & Value scoring rubric for content-critique.

---

## Routing Table

Load only the file(s) needed for the current task. Never load all 7 at once.

| Task signal | Load |
|---|---|
| Page metadata, Open Graph, canonical tags, hreflang, sitemaps, robots.txt, crawl budget, Core Web Vitals thresholds, AI crawler directives | `references/technical-seo.md` |
| JSON-LD schema markup, Article/FAQ/HowTo/Organization/Product/Breadcrumb/Person/Event structured data, rich results validation | `references/structured-data.md` |
| E-E-A-T, author schema, trust signals, Quality Rater Guidelines, expertise/authority implementation, YMYL topics | `references/eeat-principles.md` |
| Featured snippets, PAA boxes, voice search, knowledge panels, position zero, extraction zones, AI Overviews, zero-click metrics | `references/aeo-optimization.md` |
| AI citation optimization, ChatGPT/Perplexity/Claude/Gemini visibility, entity authority, BLUF writing, GEO measurement, AI crawler access decisions | `references/geo-optimization.md` |
| Pillar/cluster architecture, internal linking strategy, topical authority, content silos, freshness signals, URL structure | `references/content-architecture.md` |
| Scoring content-critique dimension 5 (SEO & Value), quick pre-publish checklist, severity mapping | `references/integration-checklist.md` |
| Content production standard: BLUF writing, extraction zones, question headings, quantitative claims, E-E-A-T, FAQ format, GEO platform rules, internal linking, content length by intent | `references/content-guidelines.md` |
| Website implementation: title/meta templates, Open Graph, Twitter Cards, canonical, hreflang, sitemap, robots.txt, all JSON-LD schemas (Article/FAQ/HowTo/Organization/Person/Breadcrumb/Product/Event), Core Web Vitals thresholds, URL structure, pre-launch checklist, analytics & GTM/GA4 default install | `references/website-metadata-spec.md` |

---

## Integration Points

Skills that should cross-reference this knowledge base:

- **`content-critique`** dimension 5 (SEO & Value): load `references/integration-checklist.md` when content type is blog/landing/docs and deep SEO audit is requested
- **`content-strategy`** Content Brief Template: load `references/content-architecture.md` when building pillar strategy; `references/eeat-principles.md` when brief requires author credentialing
- **`content-creator`** with `type=blog` or `type=landing`: load `references/aeo-optimization.md` for extraction zone structure; `references/geo-optimization.md` for BLUF writing patterns
- **`pipeline-seo-geo-aeo`** (standalone audit): loads matching reference files per stage

---

## Loading Protocol

1. Check the routing table above for your current task signal
2. Load only the matching reference file(s) — typically 1-2 files per task
3. If the task spans multiple areas (e.g., launching a blog that needs schema + pillar structure + AI citation optimization), load the 2-3 relevant files
4. Cite which reference file(s) you loaded in your output

---

## Vietnamese SEO

For Vietnamese-market SEO, load `skills/vietnamese-language/references/seo-content-marketing.md` — covers co dau vs khong dau keyword split, CocCoc optimization (~30% VN browser share), regional vocabulary keyword splitting (Northern vs Southern), and Vietnamese meta description conventions.
