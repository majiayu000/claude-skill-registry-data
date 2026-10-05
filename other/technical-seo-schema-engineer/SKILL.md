---
name: technical-seo-schema-engineer
description: Design deterministic technical SEO and schema.org guidance for crawlable public pages. Use this skill when the user asks for title and meta description rules, canonical and hreflang tags, JSON-LD schema, NewsArticle, Article, TechArticle, BreadcrumbList, WebSite, Organization, Person, OpenGraph, Twitter cards, sitemap, news-sitemap, RSS, robots.txt, llms.txt, publisher logo, ImageObject, or metadata templates that must match visible content.
---

# Technical SEO Schema Engineer

Use this skill after `information-architecture-seo` has defined page roles and before live regression validation.

Read [references/schema-patterns.md](references/schema-patterns.md) before designing full metadata or JSON-LD templates.

## Owns

- title and meta description rules;
- canonical and hreflang tag templates;
- JSON-LD schema patterns;
- OpenGraph and Twitter card metadata;
- sitemap, news-sitemap, RSS, robots.txt, and llms.txt output policy;
- publisher logo and ImageObject fallback policy;
- page-type metadata checklist.

## Does Not Own

- semantic core;
- final URL architecture;
- internal link graph;
- live audit execution;
- hidden content;
- visual page layout.

## Workflow

1. Read `url-map.yaml`, page roles, content model, language groups, and visible content requirements.
2. Select metadata and schema by page role.
3. Define title/meta fallbacks and length guidance.
4. Define canonical and hreflang tags from URL map.
5. Define JSON-LD nodes that match visible page content.
6. Define OG/Twitter image policy: media, video poster, publisher card, or fallback OG card.
7. Define sitemap/RSS/robots/llms.txt inclusion rules.
8. Produce schema/head guidance using [assets/jsonld-templates.md](assets/jsonld-templates.md) and [assets/head-metadata.template.html](assets/head-metadata.template.html).
9. Hand off validation to `seo-regression-validator`.

## Non-Negotiables

- Schema must match visible content.
- Do not add FAQPage unless the FAQ block is visible to users.
- Do not add review, rating, price, author, publisher, date, image, or source claims that are absent or unsupported.
- Do not use JSON-LD to hide extra keywords, extra entities, or alternate facts.
- NewsArticle.image must resolve to media, poster, or a stable fallback ImageObject.
- Canonical and hreflang must follow URL architecture.
- Current Google/schema.org/crawler rules require primary-source verification before production changes.

## Safety And Privacy Boundaries

- Do not expose admin, API, private dashboards, raw analytics, raw IP logs, secret files, tokens, unpublished drafts, or staging URLs in metadata, schema, sitemaps, RSS, robots, or llms.txt.
- Do not weaken authentication, access control, CSP, CORS, cookies, rate limits, or private-content boundaries for crawlability.
- Do not place private instructions or internal planning notes in public LLM-facing files.
- Do not treat robots.txt as a secrecy mechanism for sensitive content.
- Security, privacy, legal accuracy, accessibility, and visible user comprehension override SEO or LLM visibility tactics.

## Validation

Before marking work complete:

- every page type has title, description, canonical, OG, Twitter, and schema guidance;
- every schema type has required visible-content fields;
- every news/article page has image fallback policy;
- every hreflang group is based on URL map equivalents;
- sitemap and news-sitemap rules include only intended public canonical URLs;
- robots and llms.txt rules avoid private/admin/API surfaces;
- hidden schema and duplicate canonical patterns are rejected.

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/technical-seo-schema-engineer
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).

## Output Shape

Return:

1. Page-type metadata matrix.
2. Schema nodes and required visible fields.
3. Canonical/hreflang rules.
4. Sitemap/RSS/robots/llms.txt inclusion policy.
5. Validation checklist and handoff to regression validator.
