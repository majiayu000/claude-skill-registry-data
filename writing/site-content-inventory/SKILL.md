---
name: site-content-inventory
description: Map every page on a site with its intent, keywords, performance, status and next action, so research, audits and briefs never duplicate work. Use for "list all my pages", "content inventory", "content audit spreadsheet", "what pages do I have", "map keywords to pages".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/site-content-inventory
---

# Site content inventory

Build and maintain a durable map of a site's SEO surface: URLs, page purpose, keywords, performance, history, content gaps, and recommended next actions. This inventory is the shared memory for opportunity research, performance audits, content briefs, writing, QA, publishing, and task de-duplication. It hands back the inventory records (one per URL) plus a summary of what changed, what is wrong, and what needs a human.

> **Romeo's rule:** Every duplicate article starts with someone who didn't check what the site already had.

## Use this when

- You are starting SEO work on a site and need one list of every page with its purpose, keyword, intent and status.
- Before research or briefs, so new ideas get checked against what already exists.
- After a crawl, sitemap change, CMS export or migration, to catch new, removed and redirected URLs and refresh the records.
- Search Console or analytics data needs attaching to pages so movement can be explained later.
- You need the full record for one specific page before refreshing or auditing it.

## Don't use this for

- Diagnosing crawl, indexing, canonical or redirect problems → `technical-seo-audit`.
- Deciding what to create next → `seo-opportunity-research`.
- Explaining why performance moved → `seo-performance-audit`.
- Checking the XML sitemap itself against what should be indexed → `xml-sitemap-check`.

## What you need

### Required

At least one page source:

- Sitemap.
- Crawl.
- CMS export/API.
- Static-site repo index.
- Manually uploaded URL list.

And site context:

- Primary domain and canonical rules.
- Target countries/languages/locales.
- Important site sections.
- Conversion pages.
- Business/product profile.
- Known topics to prioritize, avoid, or suppress.

### Helpful

- Google Search Console or equivalent search data.
- Analytics by URL.
- Keyword provider data.
- CMS metadata: title, meta, author, publish date, updated date, status, category, tags, locale.
- Crawl details: canonical, H1, schema, word count, status code, indexability, internal links, images.
- Task/project management records.
- Prior SEO reports and recommendation history.

### No tools?

Open `/sitemap.xml` (or `/sitemap_index.xml`, or the `Sitemap:` line in `/robots.txt`) in a browser and copy the URLs; for a small site, the CMS page list or the site's navigation is enough. Search Console's Page indexing report shows which URLs are indexed or excluded, and a Performance export (Pages and Queries) gives clicks, impressions, CTR and position to attach. For per-page metadata, use view-source on each important page: `<title>`, `<meta name="description">`, `<h1>`, `<link rel="canonical">`, `<meta name="robots">`, and any JSON-LD. Keep the inventory as a CSV or spreadsheet with the record model fields as columns, and leave unknown fields blank rather than guessing.

## Ground rules

- Inventory is not truth when fresh crawl/search/CMS data contradicts it.
- Preserve human-entered strategy fields unless evidence clearly supersedes them.
- Normalize by intent, not just URL.
- Store enough history to explain movement, not every raw API row forever.
- Keep site-specific integration quirks (CMS field names, API oddities) in the import step, not in the records.
- Make duplicate suppression easy: every recommendation should map to a URL, cluster, intent, and active task state.

## Record model

Each URL record should support:

- `canonical_url`
- `normalized_url`
- `locale` / language / country target
- `section`: blog, landing, comparison, docs, help, pricing, product, template, glossary, other
- `content_type`
- `status`: live, draft, archived, redirected, noindex, unknown
- `title`
- `meta_description`
- `h1`
- `schema_types`
- `publish_date`
- `updated_date`
- `owner` / author
- `primary_keyword_cluster`
- `secondary_keywords`
- `search_intent`
- `funnel_stage`
- `conversion_page`
- `internal_link_targets`
- `linked_from_count` / key source pages when available
- screenshots/assets present
- current search metrics
- current analytics metrics
- historical performance snapshots
- `recommended_action`
- `priority`
- `active_task_id` / status
- `last_checked`
- `source_freshness`
- notes/risks

## Steps

1. **Ingest pages.**
   - Read sitemap/crawl/CMS/export/upload.
   - Normalize URLs: protocol, trailing slash, lowercase rules, query stripping, canonical mapping.
   - Exclude irrelevant URLs: admin, search, parameters, staging, assets, configured locales, noindex if not useful.
   - Group by section and locale.

2. **Enrich technical/content metadata.**
   - Attach title, meta, H1, schema, word count, publish/update dates, author, status.
   - Detect missing title/meta/H1/schema when available.
   - Detect stale dates and thin content.
   - Detect page type from URL patterns, CMS collection, schema, and headings.

3. **Attach search performance.**
   - Map queries to pages.
   - Store clicks, impressions, CTR, average position, country, device, and date window.
   - Preserve snapshots for movement detection.
   - Attach primary and secondary keyword clusters based on actual query data when available.
   - Mark page-2 queries, low-CTR queries, high-CTR/low-impression signals, and new queries.

4. **Attach analytics performance.**
   - Map pageviews, sessions, users, organic traffic, conversions, engagement, and events to URLs.
   - Record timezone and source freshness.
   - Mark conversion-supporting pages and traffic mismatches.

5. **Attach strategy fields.**
   - Primary keyword cluster.
   - Search intent.
   - Funnel stage.
   - Business priority.
   - Conversion page.
   - Topics/claims relevant to the page.
   - Known owner, task, or editorial status.

6. **Detect inventory issues.**
   - Missing target keyword.
   - Duplicate intent/cannibalization.
   - Blog page exists where landing page is needed.
   - Landing page exists but lacks supporting blog/internal links.
   - Stale facts or old year/date.
   - No answer-first section or weak TL;DR if content structure is known.
   - No conversion path.
   - Weak internal linking.
   - Missing schema.
   - Missing screenshots/product images for listicles/comparisons.
   - Title/meta risk on ranking pages.

7. **Update recommended action.**
   - create supporting page
   - refresh
   - consolidate
   - internal-link update
   - snippet review
   - add schema
   - add assets
   - watch
   - ignore/suppress
   - needs human/CMS/design action

8. **Serve downstream skills.**
   - Research (`seo-opportunity-research`) uses inventory to avoid duplicate ideas and find gaps.
   - Audit (`seo-performance-audit`) uses inventory to explain movement and avoid repeated alerts.
   - Briefs (`seo-content-brief`) use inventory to choose create vs refresh.
   - Writer (`seo-blog-writer`) uses inventory for internal links and existing page constraints.
   - QA (`seo-content-qa`) uses inventory to check page purpose, links, assets, and facts.
   - Publishing (`cms-publishing-adapter`) uses inventory to read back and update status.

## Validation

Before saving or returning inventory:

- Check URL normalization does not merge distinct valid pages.
- Check excluded locales/topics are not reintroduced.
- Check manually entered strategy fields are preserved unless explicitly overwritten.
- Check metrics have date ranges and source labels.
- Check active task IDs still exist if you can reach the task tracker.

## What to hand back

For a full inventory update, fill in this template and attach the records themselves.

```markdown
# Content inventory update: <site>, <date>

**What I found:** <one plain-English sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

## Inventory file
- <path or attachment: CSV/JSON, one row per URL, record model fields; sources and date ranges>

## Counts
- By section: <blog x, landing x, comparison x, ...>
- By status: <live x, draft x, redirected x, noindex x, unknown x>
- By locale: <...>

## New URLs
## Removed or redirected URLs
## Changed metadata
- <URL>: <field> changed from <old> to <new>

## Performance updates
- <URL>: <metric, date window, source>

## Detected issues
- <URL>: <issue> (seen / tool / inferred, high / medium / low confidence)

## Recommended actions
- <URL>: <action> | `Fix now` / `Fix next` / `Worth doing` / `Leave it` | why

## Records needing human review
- <URL>: <what is unclear or conflicting>

## What I could not check
- <...>
```

For a specific page, use this instead:

```markdown
# Inventory record: <URL>

**What I found:** <one sentence>
**What matters most:** <one sentence>
**What to do first:** <one sentence>

- Normalized URL / canonical URL: <...> / <...>
- Page purpose / content type: <...>
- Target keyword cluster: <...>
- Search intent: <...>
- Current metrics: <clicks, impressions, CTR, position, sessions, conversions; date window and source>
- Historical movement summary: <...>
- Internal and conversion links: <...>
- Asset / schema status: <...>
- Active task / recommendation status: <...>
- Next recommended action: <...>

## What I could not check
- <...>
```

## Stop and flag if

Fail the inventory update, and say so instead of saving or returning it, if:

- It overwrites strategy fields without evidence.
- It treats stale crawl/CMS data as fresher than connected live data.
- It cannot distinguish localized versions.
- It stores raw massive API payloads instead of compact records.
- It cannot support duplicate checks by URL + cluster + intent.

## Next step

- Run `seo-opportunity-research` with the inventory to find gaps and page-2 wins without duplicating existing pages.
- Run `seo-performance-audit` with the inventory and a Search Console date comparison to explain movement.
- If the inventory shows status, canonical or noindex surprises, run `technical-seo-audit` on those URLs.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
