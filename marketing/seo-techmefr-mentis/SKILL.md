---
name: seo
description: "Use when writing or reviewing a frontend page or app meant to be indexed, or auditing a built public site before launch or migration: meta tags, HTML semantics, Core Web Vitals, structured data and dates, social previews, crawl health (redirects, canonical, sitemap, link graph, URL form), content trust signals and local presence. The matching rules of robots.txt and sitemap limits are seo-crawl-control-pitfalls; diagnosing a poor vital is cwv-diagnosis-pitfalls."
---

# seo

Step 6 of the pipeline (`WORKFLOW.md`), complementing
`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`: applies only to pages meant to be indexed
by a search engine (not to back-offices, authenticated internal apps, or dashboards). The rules follow
the web standards and the search engines' published guidance, not any assistant or tool.

## When
As soon as a frontend page is public and has to be findable through search: during `code` (6) or at
review time (`review`, 8) if the diff touches public pages.

## Steps

**Read the sections the task touches.** One file per section under `references/`; a single public page diff
is usually §1 to §4, a launch or a migration adds §5, and a page with structured data, a published date or
a share card adds §6; an assistant-visibility audit is §8.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Meta and indexing: title, description, canonical, robots, social tags, `hreflang` | any public page | [`01-meta-indexing.md`](./references/01-meta-indexing.md) |
| 2 | HTML semantics a crawler and a screen reader share | headings, links, images, or content reaching the HTML | [`02-html-semantics.md`](./references/02-html-semantics.md) |
| 3 | Core Web Vitals | the largest element, image sizing, main interactions | [`03-core-web-vitals.md`](./references/03-core-web-vitals.md) |
| 4 | Structured data, sitemap and URL shape at the page level | a page type could carry structured data, or sitemap, robots or URLs change | [`04-structured-sitemap-urls.md`](./references/04-structured-sitemap-urls.md) |
| 5 | Crawl and index health of a built site: statuses, redirects, canonical and directive conflicts, sitemap, link graph, URL form | before a launch or migration, a URL change, or a site audit | [`05-crawl-health.md`](./references/05-crawl-health.md) |
| 6 | Structured data types, dates and social previews | JSON-LD is added, a date or an author is published, or a page is meant to be shared | [`06-structured-data-social.md`](./references/06-structured-data-social.md) |
| 7 | Content trust signals and local presence | a site publishes advice or articles, a sensitive subject, or a physical location | [`07-content-trust-local.md`](./references/07-content-trust-local.md) |
| 8 | AI-assistant visibility audit: crawler access as the owner's decision, renderability, markup that matches the page, facts that agree everywhere, listings, repeat snapshot tests with no score, no promised ranking, no instructions to assistants in a page | the question is whether assistants can reach, read and quote a public site correctly | [`08-ai-assistant-visibility.md`](./references/08-ai-assistant-visibility.md) |

How a `robots.txt` is actually matched, and the sitemap size limits, are in `skills/seo-crawl-control-pitfalls`; finding the cause of a poor vital is `skills/cwv-diagnosis-pitfalls`, and §3 here stays the page rules.

## Output / checkpoint
The sections reviewed on the diff touched; for a broader audit of a site already in production
(not just the diff in progress), see the `keymaker` agent.

## Guardrails
- Never applies to non-public pages (auth, back-office, internal dashboard): don't impose this
  checklist outside its scope.
- No JSON-LD over-engineering: only the content types that get a real benefit from it (product page,
  article), not a systematic addition.
- Never promise a ranking or a recommendation by an assistant, report a visibility score, or write instructions to
  assistants into a page; record what an assistant answered, with the date (§8).
- This block has no dedicated in-house production experience yet: to be confronted with the first real SEO
  audit, not to be treated as proven doctrine.

## Origin
Provenance, the re-checks and the correction log are in [`references/origin.md`](./references/origin.md).
