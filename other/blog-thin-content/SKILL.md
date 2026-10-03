---
name: blog-thin-content
description: Find, triage, and refresh thin blog content using GSC demand signals, GA4 engagement/conversion signals, blog metadata, and content quality review. Use when auditing blog posts for thin content, deciding which posts need refreshes, diagnosing pages with low value or stale intent, building a blog refresh backlog, merging weak posts, improving topical depth, or creating edit briefs for underperforming SEO content.
---

# Blog Thin Content

## Overview

Use this skill to identify blog pages that are not doing enough useful work for readers or search. Treat "thin" as a quality and usefulness diagnosis, not a word-count target.

Compose existing project skills and data sources:

- `.claude/skills/gsc-analysis/SKILL.md` for search demand, ranking, CTR, query/page pairs, cannibalization, and indexing signals.
- `.claude/skills/ga-analysis/SKILL.md` for organic sessions, engagement, bounce, conversions, declining landing pages, and device/country gaps.
- `.codex/skills/blog-eeat/SKILL.md` when the refresh requires stronger evidence, sourcing, author/reviewer support, or trust signals.
- `.claude/skills/blog-edit/SKILL.md` when applying approved content or metadata edits through the blog API.

## Quick Start

Fetch both datasets before scoring unless the user already supplied exports:

```bash
node ./.claude/skills/gsc-analysis/scripts/gsc-fetch.cjs \
  --site=myimageupscaler.com \
  --days=90 \
  --row-limit=25000 \
  --output=/tmp/gsc-miu-thin-content.json

node ./.claude/skills/ga-analysis/scripts/ga-fetch.cjs \
  --site=myimageupscaler.com \
  --days=90 \
  --landing-page-limit=2000 \
  --output=/tmp/ga-miu-thin-content.json
```

For metadata and SERP snippet checks, run the blog audit after the GSC export:

```bash
node ./.claude/skills/gsc-analysis/scripts/audit-blog-seo.cjs \
  --gsc=/tmp/gsc-miu-thin-content.json \
  --suggest \
  --output=/tmp/blog-audit-miu-thin-content.json
```

## Thin Content Definition

A page is thin when it gives a weak, shallow, outdated, duplicative, or poorly matched answer for the query intent it targets. Thinness can appear even on long pages.

Common patterns:

- Query mismatch: the page ranks for queries it does not answer directly.
- Shallow answer: generic advice, missing steps, missing examples, weak comparisons, or no original evidence.
- Stale answer: old tool limits, old platform behavior, outdated screenshots, obsolete dates, or expired assumptions.
- Duplicate value: multiple posts cover the same intent with no clear canonical winner.
- Weak SERP job: title/meta promise one thing while the body delivers another.
- Weak user job: organic visitors arrive but bounce, do not engage, or do not convert despite meaningful search demand.
- Orphaned or unsupported page: poor internal links, weak related content, no clear CTA, no schema/supporting metadata.

Do not label a page thin only because it is short, new, low-volume, or niche. A concise page can be high quality if it fully solves a narrow task.

## Data Signals

Use data to find candidates, then inspect the content before deciding the fix.

### GSC Signals

Prioritize blog URLs with one or more of these:

- High impressions and low CTR, especially positions 3-15.
- Position 5-20 with queries that the article only partially answers.
- Impressions declining while position worsens on a canonical, indexable page.
- Many query variants around an intent but no strong section matching those variants.
- Query/page rows where two or more blog URLs split the same query cluster.
- Indexed pages with very low impressions after at least 30-60 complete GSC days.
- URL inspection or sitemap signals showing canonical, indexing, or freshness issues.

Do not overreact to GSC alone. Low impressions can mean low demand, not thin content.

### GA4 Signals

Cross-check GSC candidates against:

- Organic landing pages with high sessions and low engagement.
- High organic traffic but low conversion or key-event rate.
- Declining organic landing pages, especially if GSC also shows query/ranking loss.
- High bounce or short engagement on pages whose snippet has strong CTR.
- Device-specific engagement gaps that suggest the page is hard to use on mobile.
- Country gaps that suggest localization or intent mismatch.

GA4 is a behavior signal, not a content verdict. A page can have low conversion because the CTA is wrong, the target query is informational, or tracking is incomplete.

## Scoring Model

Score each candidate from 0-10. Use the score to prioritize review, not to automate deletion.

| Area                    | Points | What to check                                                     |
| ----------------------- | -----: | ----------------------------------------------------------------- |
| Search demand exists    |    0-2 | Impressions, query variety, striking-distance positions           |
| Search underperformance |    0-2 | Low CTR, worsening position, query/page mismatch                  |
| Behavioral weakness     |    0-2 | Low engagement, high bounce, low conversion for intent            |
| Content weakness        |    0-2 | Shallow, stale, unsupported, no original examples, weak intro     |
| Portfolio risk          |    0-2 | Cannibalization, orphaning, duplicate intent, poor internal links |

Priority bands:

- `P1 refresh now`: 7-10 points, meaningful demand, clear quality gap, no recent edit waiting on data.
- `P2 improve soon`: 4-6 points, fixable weaknesses but lower demand or unclear causality.
- `P3 monitor or maintain`: 1-3 points, weak signal, recent edit, low demand, or mostly technical/indexing follow-up.
- `No action`: useful page, healthy intent fit, or data does not justify content work.

## Workflow

1. **Read recent SEO history**
   - Check `.claude/skills/blog-changelog.md`.
   - Check `docs/SEO/maintenance/seo-changes-backlog.md`.
   - Check `docs/SEO/maintenance/gsc-request-indexing-backlog.md`.
   - Search these files for candidate slugs before recommending another edit.

2. **Fetch and join data**
   - Use the GSC and GA commands in Quick Start.
   - Join by canonical blog URL or path. Normalize trailing slashes, query strings, and redirects.
   - Prefer 90 days for thin-content audits; use 28 days only for narrow follow-ups.
   - Note GSC lag and avoid judging changes before enough complete data exists.

3. **Build the candidate list**
   - Filter to `/blog/` URLs unless the user asks for all content.
   - Include GSC page metrics, top query clusters, GA organic sessions, engagement, conversions, and recent edit status.
   - Flag cannibalization and redirect/canonical anomalies before content scoring.

4. **Inspect each top candidate**
   - Fetch the current post through the API or local content source.
   - Review title, H1, intro, table of contents, section depth, examples, images, internal links, CTAs, schema, dates, and sources.
   - Compare top GSC queries to headings and paragraphs. Missing exact user tasks are the strongest thin-content clue.

5. **Choose the remedy**
   - Refresh: strengthen the same URL when intent is correct and demand exists.
   - Expand: add missing modules, examples, original tests, FAQs, comparisons, screenshots, or troubleshooting.
   - Consolidate: merge weak overlapping posts into the strongest canonical page when multiple URLs split intent.
   - Redirect or noindex: only for pages with no unique value, no demand, and no useful business role.
   - Technical fix: handle canonical, indexing, template, schema, or internal-link issues before rewriting.
   - Monitor: defer only with an exact trigger and date, especially after recent edits.

6. **Prepare edit briefs**
   - For each `P1 refresh now` page, produce a concrete brief:
     - URL and slug.
     - Current data signals from GSC and GA4.
     - Target query cluster and intent.
     - Diagnosis: why the page is thin or mismatched.
     - Proposed SEO title and meta description.
     - H1 or title adjustment if needed.
     - First paragraph rewrite direction.
     - Sections to add, remove, merge, or update.
     - Original evidence to add, such as before/after images, tool outputs, settings, file dimensions, screenshots, or tests.
     - Internal links to add and anchor text.
     - CTA change if GA4 shows low conversion for a page that should convert.
     - Indexing or changelog follow-up.

7. **Apply changes only when asked or when the maintenance task explicitly includes implementation**
   - Load `.claude/skills/blog-edit/SKILL.md`.
   - Patch only the fields and content needed for the brief.
   - Append a concise changelog entry after edits.
   - Add important updated URLs to the indexing backlog when appropriate.

## Refresh Strategy

Prefer depth that proves usefulness:

- Answer the dominant query in the first screen, then expand into edge cases.
- Replace generic advice with specific steps, screenshots, tested settings, examples, and before/after outcomes.
- Add comparison tables only when they clarify a decision; avoid decorative filler.
- Add "when not to use this" and troubleshooting sections for task guides.
- Update stale dates and claims only after verifying the current fact.
- Link from stronger related posts and tool pages with descriptive anchor text.
- Keep the CTA aligned with intent: informational pages can use soft tool CTAs; commercial or tool-intent pages can use direct conversion CTAs.
- Preserve the existing URL when it has backlinks, history, rankings, or a clear canonical role.

## Deletion And Consolidation Guardrails

Do not delete, unpublish, noindex, or redirect just because a page is low traffic. Require all of:

- No meaningful GSC demand after a mature measurement period.
- No meaningful GA4 organic sessions, conversions, or assisted business role.
- No unique intent, evidence, link equity, or internal-support role.
- A better destination exists, or the page can be safely retired without creating a gap.

When consolidating, write the destination update first, preserve useful sections from the weaker page, then redirect the weaker URL and add the action to the SEO maintenance backlog.

## Output Format

For audits, lead with a prioritized table:

| Priority | URL | Score | Evidence | Diagnosis | Action |
| -------- | --- | ----: | -------- | --------- | ------ |

Then include:

- Data window and freshness note.
- Top `P1` edit briefs.
- Consolidation candidates.
- Technical/indexing blockers.
- Deferred pages with exact next-check triggers.
- Files or APIs changed, if implementation happened.

Keep recommendations concrete enough that `blog-edit` can execute them without redoing the audit.
