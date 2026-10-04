---
name: startup-seo-starter
description: Build and improve SEO-ready startup websites and early organic growth foundations, including technical SEO, initial content, AI-search visibility, measurement, and recurring SEO/GEO change monitoring. Do not use for unrelated product UI work or mature enterprise SEO operations.
metadata:
  version: "1.1.0"
  focus: startup websites and early organic growth
---

# Startup SEO Starter

Use this skill to help an early-stage company establish a clear, useful, search-ready web presence. Treat SEO and GEO as part of a product-growth foundation: first clarify who the product serves and what problem it solves, then design a site that communicates that value, can be discovered, and gives visitors a credible next action.

## Choose the smallest useful mode

| Request | Mode | Read when needed |
|---|---|---|
| New product, unclear audience, value proposition, first website | Startup growth foundation | `references/startup-discovery.md` and `references/startup-web-foundation.md` |
| Homepage, landing page, page hierarchy, navigation, CTA, responsive experience | Startup website experience | `references/startup-web-foundation.md` |
| ICP, customer language, first keywords, search demand, page opportunities | Startup discovery and keyword system | `references/startup-discovery.md` |
| Indexing, crawlability, Core Web Vitals, page or site health | SEO foundation audit | `references/audit-checklist.md` |
| Pre-launch, migration, first deployment, post-launch verification | SEO launch checklist | `references/launch-checklist.md` |
| JSON-LD, Schema, sitemap, hreflang, canonical, social metadata | Technical SEO assets | `references/schema-patterns.md` |
| First keywords, search intent, topic clusters, content brief, internal links | Initial content system | `references/content-and-programmatic.md` |
| GA4/GSC setup, CTA events, signup funnel, organic conversion measurement | Analytics and conversion | `references/analytics-and-conversion.md` |
| Live Google data unavailable, MCP installation, OAuth, GA4 property access, connector setup | Google MCP setup | `references/mcp-setup.md` and `references/google-connectors.md` |
| AI Overviews, ChatGPT, Perplexity, citations, AI visibility | GEO foundation | `references/citability-checklist.md` |
| robots.txt, AI bots, llms.txt, server rendering, entity readiness | Technical GEO | `references/llms-template.md` |
| PR, directories, partnerships, reviews, founder expertise, early authority | Authority and distribution | `references/authority-and-distribution.md` |
| Local business, ecommerce, product/category pages | Optional business-model track | `references/local-and-commerce.md` |
| GSC, GA4, performance data, crawler exports, baseline, weekly report | Measurement and iteration | `references/evidence-and-reporting.md`, `references/google-connectors.md`, and `references/weekly-reporting.md` |
| Search algorithm/product changes, SEO/GEO blogs, recurring digest, industry updates | SEO/GEO change monitoring | `references/seo-geo-monitoring.md` |
| Minimum startup context, assumptions, missing inputs, or deliverable selection | Intake and evidence contract | `references/intake-template.md` |
| Startup SEO audit, 90-day plan, content brief, or GEO report format | Standard output templates | `references/output-templates.md` |
| Source verification, time-sensitive claims, or `llms.txt` status | Sources of truth and freshness | `references/sources-of-truth.md` |

Combine modes only when needed. For a new SaaS website, use Startup growth foundation + Startup website experience + SEO foundation audit. Do not trigger a full GEO or reporting workflow for a one-page metadata fix. Use the monitoring mode only when the user asks to track ecosystem changes or a recurring digest is explicitly configured.

## Operating workflow

1. Establish the startup context using `references/intake-template.md` when the request is broad or information is missing. Label unknowns and assumptions instead of inventing them.
2. State one concise design read before substantial website work: `Design read: [audience] needs [primary job]; use [information hierarchy and interaction strategy] with [visual character], while avoiding [generic pattern].`
3. Define the smallest useful site: homepage, product or service page, use cases, pricing or conversion page, proof, documentation/resources, and trust/about pages only when justified by the business.
4. Inspect available evidence before making claims. Prefer rendered HTML for client-side metadata and schema; use Search Console, analytics, performance data, crawl exports, or approved connectors when available; label assumptions and missing data.
5. Prioritize by business impact and implementation leverage. Every important finding should include evidence, impact, confidence, priority, owner, and a validation method.
6. Produce the requested artifact: positioning brief, page map, landing-page structure, implementation patch, content brief, technical markup, roadmap, baseline, or report. Do not invent metrics, testimonials, customers, citations, crawl results, or product claims.
7. End with validation: what to re-fetch, test, compare, or monitor, and when the change should be rechecked.

## Startup website experience

- Make the product, audience, problem, proof, and next action clear in the first useful viewport.
- Choose page hierarchy and visual language from the product and market; avoid generic AI defaults such as an interchangeable centered hero, three equal feature cards, decorative gradient blobs, and claims without proof.
- Use real or explicitly marked placeholder content. Do not invent customers, testimonials, logos, usage numbers, or performance claims.
- Define useful responsive behavior, accessible controls, focus states, loading/error states, and stable layouts where the site has interaction or dynamic data.
- Treat page performance and accessibility as launch requirements because they affect both user trust and organic acquisition.
- Prefer the smallest coherent design system: type roles, color roles, spacing, buttons, links, cards, forms, and content states.

## Traditional SEO guardrails

- Check status codes, robots.txt, XML sitemaps, canonicals, noindex, redirects, rendering, internal links, metadata, headings, mobile UX, and Core Web Vitals where relevant. Use INP rather than the deprecated FID metric.
- Match page type to search intent and SERP expectations. Evaluate content quality, originality, freshness, first-hand evidence, authorship, and internal linking rather than keyword density alone.
- Include only canonical, indexable, 200-status URLs in sitemaps. Keep hreflang alternates reciprocal, self-referencing, canonical, and valid for the locale.
- Mark up only truthful, visible page content. Distinguish structured-data machine understanding from eligibility for a rich result. Do not promise FAQ or deprecated HowTo rich results.
- For programmatic SEO, require unique value, freshness, quality gates, crawl paths, and an explicit index/noindex decision before scaling page creation.

## GEO guardrails

Evaluate five dimensions: citability, entity clarity, authority, third-party/platform presence, and technical access. For content, lead with direct answers, use question-led headings, keep answer blocks self-contained, add dated sources and attribution, and use comparison tables where they improve extraction.

For technical GEO, distinguish search/citation access from model-training access. Inspect `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `PerplexityBot`, `Googlebot`, `Google-Extended`, `Bingbot`, `CCBot`, and other relevant tokens without assuming that every bot has the same purpose. Blocking a training crawler is a policy decision; blocking retrieval/search crawlers can reduce AI answer visibility.

For AI visibility measurement, preserve the exact query corpus, run isolated tests when platform behavior is being compared, record complete answers and visible sources, timestamp each run, and retain historical evidence. Never infer visibility from a single anecdotal answer.

## Deliverable defaults

For a startup plan, lead with assumptions, target audience, page priorities, first conversion path, technical foundation, first content bets, and a 30/60/90-day roadmap. For an implementation request, show the smallest accurate patch plus validation steps. For a content request, provide intent, audience, outline or rewrite direction, evidence requirements, internal-link targets, and citability checks. For a recurring report, compare the current period with the correct prior period and rebuild actions from fresh evidence instead of copying prior recommendations.

## Scope boundary

Use this skill for early-stage websites and initial organic-growth systems. Route unrelated dashboard/product UI work to a dedicated product-design skill. Route mature enterprise SEO operations, large-scale migration programs, paid acquisition, and general business analytics to a specialized workflow unless the user explicitly asks to connect them to startup SEO.

## Supporting references

- Read [references/audit-checklist.md](references/audit-checklist.md) for a compact site/page audit checklist.
- Read [references/citability-checklist.md](references/citability-checklist.md) for page-level GEO scoring and rewrite checks.
- Read [references/llms-template.md](references/llms-template.md) when drafting or reviewing `llms.txt`.
- Read [references/schema-patterns.md](references/schema-patterns.md) when generating JSON-LD.
- Read [references/content-and-programmatic.md](references/content-and-programmatic.md) for content authority, programmatic, and competitive page work.
- Read [references/startup-discovery.md](references/startup-discovery.md) before building the first keyword list, page inventory, or content roadmap.
- Read [references/launch-checklist.md](references/launch-checklist.md) before launch, migration, or the first public deployment.
- Read [references/analytics-and-conversion.md](references/analytics-and-conversion.md) when connecting organic traffic to CTA, signup, demo, activation, or revenue events.
- Read [references/google-connectors.md](references/google-connectors.md) when the local `search-console-mcp` runtime is available and the user wants live GSC or GA4 data.
- Read [references/mcp-setup.md](references/mcp-setup.md) when the runtime is missing, authorization is incomplete, or the user asks how to install and connect the Google MCP project.
- Read [references/authority-and-distribution.md](references/authority-and-distribution.md) when planning early mentions, links, partnerships, reviews, or founder-led distribution.
- Read [references/local-and-commerce.md](references/local-and-commerce.md) for local, maps, ecommerce, and product visibility work.
- Read [references/evidence-and-reporting.md](references/evidence-and-reporting.md) for data-source contracts, citation benchmarks, crawler telemetry, and recurring reports.
- Read [references/startup-web-foundation.md](references/startup-web-foundation.md) for product-to-website framing, page maps, landing-page structure, and design quality gates.
- Read [references/weekly-reporting.md](references/weekly-reporting.md) when the user explicitly wants a recurring SEO/GEO report or weekly operating cadence.
- Read [references/seo-geo-monitoring.md](references/seo-geo-monitoring.md) when tracking SEO/GEO blogs, official platform changes, search incidents, or a recurring two-day/weekly industry digest.
- Read [references/intake-template.md](references/intake-template.md) before a broad startup SEO/GEO engagement or when the user's inputs are incomplete.
- Read [references/output-templates.md](references/output-templates.md) when the user asks for a standard audit, 90-day roadmap, content brief, or GEO report.
- Read [references/sources-of-truth.md](references/sources-of-truth.md) when making time-sensitive SEO/GEO claims, citing platform behavior, or evaluating `llms.txt`.
