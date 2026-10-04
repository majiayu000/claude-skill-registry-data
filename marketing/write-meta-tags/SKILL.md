---
name: write-meta-tags
description: Use when writing or auditing title tags and meta descriptions for any webpage
source: Google Search Documentation (developers.google.com/search), Moz Title Tag Guide
tags: [seo, meta-tags, title-tag, meta-description, on-page, click-through-rate]
verified: true
---

# Write Meta Tags

Craft title tags and meta descriptions that maximize click-through rate while signaling relevance to Google.

## Why This Is Best Practice

**Adopted by:** Google's own Search documentation specifies best practices; Moz CTR studies validate impact
**Impact:** A/B tests by Portent and Moz show optimized title tags improve organic CTR by 20-30% without any change in ranking

**Why best:** Title tags are the primary ranking signal Google reads first. Meta descriptions don't directly affect ranking but are the primary lever for CTR — the metric that creates a compounding ranking feedback loop. Both must serve humans and algorithms simultaneously.

## Steps

1. **Identify primary keyword** — Use the target keyword from the page's keyword cluster; it must appear in the title tag.
2. **Write the title tag** — Lead with keyword, add a benefit or differentiator, include brand name at the end separated by " | " or " – "; keep under 60 characters (600px pixel width).
3. **Verify uniqueness** — Check that no other page on the site has an identical or near-identical title; duplicates cause Google to rewrite both.
4. **Write the meta description** — 150-160 characters; include primary keyword naturally, state the page's value proposition, and end with a call to action.
5. **Add power words** — Words like "free," "guide," "checklist," "step-by-step" increase CTR; use one per description.
6. **Check for mobile truncation** — Preview in a SERP simulator (e.g., Portent's SERP Preview Tool); title should not truncate at a keyword boundary.
7. **Review against SERP competitors** — Ensure the title differentiates from the top-3 ranking results rather than mirroring them.
8. **Set and monitor CTR** — Track in Google Search Console; if CTR falls below the average for that position, iterate.

## Rules

- Never keyword-stuff title tags — Google rewrites stuffed titles and the rewrite is usually worse.
- Every page must have a unique title and unique meta description; batch-generated templates are a last resort.
- Do not use all-caps in meta descriptions — reduces readability and perceived trustworthiness.
- Include the year in titles for evergreen guides (e.g., "Best X Tools (2026)") to signal freshness.
- Meta descriptions longer than 160 characters are truncated; the truncation point must not cut a sentence mid-thought.

## Examples

Before: `Title: "Project Management | Software | Features | Pricing | Our Company"`
After: `Title: "Project Management Software for Remote Teams | Acme"`

Before: `Description: "We offer project management software with many features for teams of all sizes."`
After: `Description: "Assign tasks, track deadlines, and ship projects 2x faster. Try Acme free for 14 days."`

## Common Mistakes

- Writing titles for bots not humans — stuffed titles get rewritten by Google automatically.
- Ignoring meta descriptions because they "don't affect ranking" — they directly affect CTR which influences ranking.
- Setting the same meta description for category and product pages — wasted differentiation opportunity.
- Never reviewing Search Console CTR data — title/description optimization is iterative, not one-time.
