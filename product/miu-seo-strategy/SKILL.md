---
name: miu-seo-strategy
description: Build and operate MyImageUpscaler's AI-led SEO strategy from GSC/GA4 evidence, using Claude agents/skills as the SEO team. Use when asked what to do next for MIU SEO, how to turn impressions into clicks/signups, how to prioritize SEO work, or how to coordinate Claude-only SEO execution.
---

# MIU SEO Strategy

Use this skill when the goal is not a single title rewrite or one blog edit, but an operating strategy for MyImageUpscaler SEO. The baseline signal from João's Reddit prompt is strong demand with weak capture: **1.5M impressions and 12.9K clicks in 3 months = 0.86% CTR**. Treat that as the starting problem: MIU has visibility; the work is to convert visibility into qualified clicks, engaged users, and paid conversions.

The SEO team is Claude. That means the strategy must be decomposed into repeatable agent workstreams, with GSC and GA4 as the manager, not vibes.

## Activation

When this skill activates, say:

`MIU SEO Strategy: using Claude as the SEO team, with GSC/GA4 as ground truth.`

## Core Principles

1. **Evidence first.** Start from fresh GSC and GA4 or the latest saved reports. If fresh GSC fails, stop and say exactly why.
2. **Impressions are inventory.** A 1.5M-impression quarter means the site already has query coverage. Prioritize CTR, intent fit, snippets, internal links, and conversion routing before blindly publishing more pages.
3. **Claude is the team, not the source of truth.** Use Claude agents/skills for analysis and execution, but require real data, diffs, tests, and post-change measurement.
4. **Separate traffic, engagement, and money.** Ranking fixes, snippet fixes, page fixes, CTA fixes, and attribution fixes are different jobs.
5. **Do not touch winning pages casually.** If a page is improving or recently changed, monitor until GSC lag clears unless there is a clear defect.
6. **Every action gets an owner skill and a success metric.** No vague “improve SEO” tasks.

## Required Context Before Any Plan

Read these before recommending or executing SEO work:

- `CLAUDE.md`
- `docs/SEO/maintenance/seo-changes-backlog.md`
- `docs/SEO/maintenance/gsc-request-indexing-backlog.md`
- Latest relevant report under `docs/SEO/reports/`

Then fetch fresh data when possible:

```bash
node ./.claude/skills/gsc-analysis/scripts/gsc-fetch.cjs --site=myimageupscaler.com --days=90 --output=/tmp/gsc-miu-90d.json
node ./.claude/skills/ga-analysis/scripts/ga-fetch.cjs --site=myimageupscaler.com --days=90 --output=/tmp/ga-miu-90d.json
node ./.claude/skills/seo-growth-plan/scripts/seo-synthesize.cjs \
  --gsc=/tmp/gsc-miu-90d.json \
  --ga=/tmp/ga-miu-90d.json \
  --site=myimageupscaler.com \
  --output=/tmp/seo-plan-miu-90d.json
```

If 90-day data is too broad for a recent experiment, use 28 days plus the latest change backlog entries.

## Strategic Triage

Classify each opportunity into exactly one primary lane:

### Lane 1: CTR Capture

Use when pages have high impressions and acceptable positions but low clicks.

Signals:

- Position 1-10 with weak CTR for query class.
- Position 4-20 with lots of impressions and few clicks.
- GSC query/page pairs with zero clicks but repeated impressions.

Owner skills:

- `serp-ctr-snippet-rewrite-technique`
- `seo-content-3-kings-technique`
- `blog-edit`

Actions:

- Rewrite title/meta/H1/first-screen answer for exact intent.
- Add comparison or proof blocks when the SERP wants evaluation.
- Add image-upscaler-specific wording: free, no watermark, before/after, batch, resolution, artifact removal, print, anime, product photo, etc. only where true.

Success metrics:

- Query/page CTR lift.
- Click lift without position loss.
- No cannibalization increase.

### Lane 2: Ranking Lift

Use when pages sit in positions 8-25 with enough impressions to matter.

Signals:

- Strong impressions, middling average position.
- Query intent matches the page but authority/coverage is thin.
- Page needs internal links, missing topical sections, schema, or consolidation.

Owner skills:

- `seo-money-page-lift-technique`
- `pseo-page-quality-scoring-technique`
- `cannibalization-consolidation-technique`
- `content-gap`

Actions:

- Add internal links from homepage/tool/blog winners.
- Fill exact missing intent sections.
- Consolidate duplicate/cannibalized pages before publishing more.
- Improve pSEO templates only when the whole family benefits.

Success metrics:

- Position improvement for target query cluster.
- More clicks from same or rising impressions.
- Fewer query splits across duplicate URLs.

### Lane 3: Conversion and CTA Repair

Use when organic traffic lands but does not become signups, checkout starts, or purchases.

Signals:

- GA4 shows organic sessions with weak engagement or conversion.
- GSC clicks are strong but revenue/signups are not attributable.
- Page intent is informational but has no useful next step.

Owner skills:

- `search-intent-cta-mapping-technique`
- `organic-funnel-attribution-repair-technique`
- `ga-analysis`

Actions:

- Map each page to the next believable action: upload image, compare models, read guide, sign up, pricing, API, batch processing.
- Fix GA4 attribution before judging SEO ROI if organic conversions are missing.
- Add measured CTAs; do not add generic sales spam.

Success metrics:

- Organic signups or key events.
- Better GSC-click to GA organic-session consistency.
- Improved engagement for targeted landing pages.

### Lane 4: Programmatic Expansion

Use only after cannibalization and quality gates pass.

Signals:

- New query families with no owned page.
- Competitors own landing pages for formats, use cases, or alternatives MIU can genuinely serve.
- Existing pSEO templates score well and have no indexation problems.

Owner skills:

- `keyword-research-strategy`
- `competitor-sitemap-spy`
- `pseo-system`
- `pseo-page-quality-scoring-technique`

Actions:

- Create tightly scoped page families, not generic keyword clones.
- Validate middleware, localization config, sitemap, schema, and tests for every new pSEO category.
- Prefer use-case and format pages with real product fit.

Success metrics:

- Indexed pages with impressions.
- No sitemap/canonical/hreflang regressions.
- New pages route users into measurable product actions.

### Lane 5: Distribution and SERP Support

Use when a page already answers a question and needs qualified traffic or off-SERP validation.

Signals:

- Reddit/Quora/forum threads rank for the same queries.
- Target blog/tool page is useful enough to share without sounding promotional.
- Page has good engagement or has been fixed first.

Owner skills:

- `reddit-seo-response`
- `blog-opportunities-publisher`
- `blog-performance-monitor`

Actions:

- Answer exact questions in relevant threads.
- Link only when it helps and subreddit rules allow it.
- Use no-link participation when link risk is high.

Success metrics:

- Referral sessions.
- Assisted GSC movement for supported queries.
- No spammy duplicate posting.

## Claude Team Operating Model

Run SEO as a weekly or campaign-based assembly line:

1. **SEO Manager** (`seo-manager`) collects GSC, GA4, technical, pSEO, blog, schema, internal-link, and competitor data.
2. **Strategist** (`miu-seo-strategy`) turns the evidence into lane-ranked bets.
3. **Specialists** execute only their lane:
   - CTR specialist: snippets and first-screen intent.
   - Content specialist: blog/tool edits.
   - pSEO specialist: page families and template quality.
   - Technical specialist: sitemap, robots, hreflang, canonical, schema, speed.
   - Attribution specialist: GA4 and funnel proof.
   - Distribution specialist: Reddit/forum response plans.
4. **Verifier** checks tests, diffs, production behavior when deployed, and GSC/IndexNow follow-ups.

Use parallel Claude tasks for independent analysis, but serialize edits that touch the same page, metadata, route, sitemap, schema, or tracking surface.

## Prioritization Formula

Score each candidate from 0-100:

- Demand: 25 points — impressions, query volume, trend.
- Capture gap: 25 points — low CTR, position 4-20, zero-click rows.
- Business value: 20 points — signup, paid, API, batch, commercial use case.
- Fix confidence: 15 points — clear mismatch, proven template, low regression risk.
- Time-to-signal: 10 points — title/meta/internal link beats full rewrite when enough.
- Risk inverse: 5 points — avoid touching winners, recent experiments, or cannibalized clusters without proof.

Default order for the current 1.5M impression / 12.9K click situation:

1. CTR capture on high-impression pages.
2. Fix-before-pushing pages with engagement/CTA defects.
3. Internal links and consolidation for striking-distance clusters.
4. Distribution for already-useful pages.
5. New pSEO/content only for uncovered, non-cannibalized intents.

## Output Format

Return a concise strategy document:

```markdown
# MIU SEO Strategy

## Baseline

- Period:
- GSC clicks / impressions / CTR:
- GA4 organic sessions / conversions:
- Biggest bottleneck:

## Ranked Bets

1. [Lane] [Page/cluster] — evidence, action, owner skill, success metric, expected signal date.
2. ...

## This Week

- Day 1:
- Day 2:
- Day 3:
- Day 4:
- Day 5:

## Do Not Touch Yet

- [Page/cluster] — why waiting is better.

## Measurement

- GSC query/page rows to monitor:
- GA4 events/pages to monitor:
- Backlog/indexing follow-up:
```

## Strategy Gaps to Check Explicitly

A good MIU SEO plan must not stop at web-search CTR. Always check these dimensions before finalizing priorities:

1. **Revenue/ICP weighting.** A high-impression query is not automatically valuable. Upweight API, batch, commercial, professional, ecommerce, real-estate, print, restore, and paid-tool intent; downweight curiosity traffic unless it routes into a measurable product action.
2. **Image SEO.** MIU is an image product. Check Google Images/search type mix, image landing pages, preview quality, Open Graph images, before/after assets, alt text, and whether visual examples support the SERP promise.
3. **Experiment cadence.** Treat title/meta/H1/CTA changes as experiments with baseline date, changed URL/query rows, expected GSC lag, and rollback criteria. Avoid changing the same page repeatedly before signal matures.
4. **Technical quality moat.** Keep schema, Core Web Vitals, sitemap health, canonical/hreflang, and indexation clean. For AI-generated scale, technical regressions can erase content gains.
5. **Human QA against AI slop.** Claude can draft and audit, but final pages need real usefulness: specific examples, true product claims, no generic intros, no duplicated sections, and no fake comparisons.

## Guardrails

- Do not recommend new content if the query is already owned by an existing page that needs consolidation, CTR, or CTA work.
- Do not request indexing through an API. Normal GSC request indexing remains manual; update or remind from the backlog.
- Do not treat Reddit links as link-building. Treat Reddit as useful distribution and problem discovery.
- Do not use LLM-written SEO advice without matching it to real MIU pages, real queries, and recent backlog entries.
- Any production SEO-facing code/content changes must update `docs/SEO/maintenance/seo-changes-backlog.md` and include appropriate tests when metadata, sitemap, schema, canonical, hreflang, robots, or SEO routes change.

## Verification Checklist

- [ ] Fresh GSC or latest report used.
- [ ] GA4 checked or failure noted.
- [ ] SEO changes backlog and request-indexing backlog checked.
- [ ] Opportunities assigned to lanes with owner skills.
- [ ] Existing/recent work deduplicated.
- [ ] Each recommended action has a success metric and measurement date.
- [ ] If files changed, tests and `yarn verify` were run or the blocker is stated.
