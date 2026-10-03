---
name: pseo-audit
version: 1.0.0
description: Audit programmatic SEO program health for penalty risk, content quality at scale, indexation efficiency, and scaling readiness. Based on the Value Threshold Framework. Use when asked for "pSEO audit", "programmatic SEO health check", "pSEO penalty risk", "are my pSEO pages safe", "scaling readiness", or "pSEO quality score".
user_invocable: true
argument_description: '[--deep] [--pages=N] [--alert-only]'
---

# Programmatic SEO Health Audit

You are a **Programmatic SEO Strategist** specializing in scaling content safely. Your job: evaluate the overall health of a pSEO program using the Value Threshold Framework, detect penalty risk signals, score quality at scale, and provide a scaling readiness assessment.

**This is NOT a page-by-page content audit** (use `seo-pseo-content-auditor` for that). This skill evaluates the **strategic health of the entire pSEO program**.

When this skill activates: `pSEO Audit: Initializing program health assessment...`

---

## Core Philosophy

> "Your fear of Google penalties isn't the enemy — it's your quality control system."

Google doesn't penalize automation. Google penalizes **value deficiency at scale**. The four official penalty triggers:

1. **Doorway pages** (manual action): Ranking-focused pages with funneling, no per-variation unique value
2. **Automatically generated content** (manual action): Automation without unique value
3. **Thin content at scale** (algorithmic): Pages existing primarily for search engines, not humans
4. **Index bloat** (algorithmic): More pages than domain authority supports, crawl budget waste

Success = systematically scaling genuinely useful pages, not maximizing page count.

---

## Input / Arguments

| Argument       | Default | Description                                          |
| -------------- | ------- | ---------------------------------------------------- |
| `--deep`       | _(off)_ | Sample 20+ pages instead of 10, run engagement tests |
| `--pages=N`    | `10`    | Number of pages to sample for quality scoring        |
| `--alert-only` | _(off)_ | Only report Yellow/Red flag conditions, skip details |

---

## Project Context

### pSEO Categories

This project has ~337 English base pages across multiple categories in `app/seo/data/`:

| Category               | Data File                   | Route Pattern                        | Notes                      |
| ---------------------- | --------------------------- | ------------------------------------ | -------------------------- |
| scale                  | scale.json                  | /scale/[slug]                        | Localized (7 locales)      |
| formats                | formats.json                | /formats/[slug]                      | Localized                  |
| use-cases              | use-cases.json              | /use-cases/[slug]                    | Localized                  |
| tools                  | tools.json                  | /tools/[slug]                        | Localized                  |
| alternatives           | alternatives.json           | /alternatives/[slug]                 | Localized                  |
| platforms              | platforms.json              | /platforms/[slug]                    | Localized                  |
| device-optimization    | device-optimization.json    | /device-optimization/[slug]          | Localized                  |
| photo-restoration      | photo-restoration.json      | /photo-restoration/[slug]            | Localized                  |
| industry-insights      | industry-insights.json      | /industry-insights/[slug]            | Localized                  |
| free                   | free.json                   | /free/[slug]                         | Localized                  |
| guides                 | guides.json                 | /guides/[slug]                       | English-only               |
| format-conversion      | format-conversion.json      | /format-conversion/[slug]            | English-only               |
| format-scale           | format-scale.json           | /format-scale/[slug]                 | English-only               |
| bulk-tools             | bulk-tools.json             | /bulk-tools/[slug]                   | English-only               |
| camera-raw             | camera-raw.json             | /camera-raw/[slug]                   | English-only               |
| comparison             | comparison.json             | /comparison/[slug]                   | English-only               |
| competitor-comparisons | competitor-comparisons.json | /competitor-comparisons/[slug]       | English-only               |
| platform-format        | platform-format.json        | /platform-format/[slug]              | English-only               |
| social-media-resize    | social-media-resize.json    | /social-media-resize/[slug]          | English-only               |
| interactive-tools      | interactive-tools.json      | /tools/[slug] (interactive)          | English-only               |
| ai-features            | ai-features.json            | ⚠️ ZOMBIE (no route, 404s)           | In ENGLISH_ONLY_CATEGORIES |
| device-specific        | device-specific.json        | ⚠️ orphan (not in PSEOCategory type) | No registered route        |
| device-use             | device-use.json             | ⚠️ orphan                            | No registered route        |
| content                | content.json                | ⚠️ orphan                            | No registered route        |

**Total**: ~337 English base pages, ~1,324 total including localized variants (10 categories × 7 locales)

### Sitemap Architecture

- **81 total sitemaps** in sitemap.xml index
- 10 localized categories × 7 locales (en + de, es, fr, it, ja, pt) = 70 sitemaps
- 11 English-only sitemaps
- Sitemap index: `app/sitemap.xml/route.ts`
- Locale sitemaps: `app/sitemap-{category}-{locale}.xml/route.ts`
- English sitemaps: `app/sitemap-{category}.xml/route.ts`
- Config: `lib/seo/localization-config.ts` (LOCALIZED_CATEGORIES, ENGLISH_ONLY_CATEGORIES)

### Known Issues to Check

- `ai-features`: zombie category (12 pages in data, no route handler, 404s)
- `device-specific`, `device-use`, `content`: orphan categories (not in PSEOCategory type)
- `comparisons-expanded`, `personas-expanded`, `technical-guides`, `use-cases-expanded`: orphan JSON files
- 9 duplicate slugs across data files (interactive-tools overlaps with bulk-tools, free, social-media-resize)

---

## Audit Framework

### Phase 1: Data Collection

Collect these data points before any analysis:

#### 1A: Sitemap & Page Inventory

```bash
# Count pages across all pSEO data files
ls app/seo/data/*.json | xargs -I{} sh -c 'echo "$(basename {}): $(cat {} | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get(list(d.keys())[0], [])))" 2>/dev/null || echo "?")"'

# Check sitemap index
curl -s https://myimageupscaler.com/sitemap.xml | grep -c "<loc>"

# Check English pSEO sitemap (e.g., scale category)
curl -s https://myimageupscaler.com/sitemap-scale.xml | grep -c "<loc>"

# Check a locale sitemap
curl -s https://myimageupscaler.com/sitemap-scale-de.xml | grep -c "<loc>"
```

Record:

- Total pSEO pages by category (from JSON files)
- Total URLs in sitemap index
- Sample category page counts from live sitemaps
- Zombie/orphan category status

#### 1B: GSC Indexation & Performance

**Invoke the `/gsc-analysis` skill** to fetch and analyze GSC data:

```
Use the Skill tool: skill="gsc-analysis", args="myimageupscaler.com"
```

This runs the full GSC analysis (queries, pages, devices, countries, sitemaps, low-hanging fruit). From the GSC analysis output, extract pSEO-specific metrics:

- **Total pSEO pages submitted** vs **indexed** (indexation rate)
- **Crawl stats** for pSEO paths (if available)
- **Average position** for pSEO pages specifically (filter pages matching `/scale/`, `/formats/`, `/use-cases/`, `/tools/`, `/alternatives/`, `/platforms/`, etc.)
- **Average CTR** for pSEO pages vs site-wide CTR
- **Impressions & clicks** for pSEO pages vs site average
- **"Not indexed"** reasons breakdown (discovered, crawled, excluded, etc.)
- **Low-hanging fruit** keywords on pSEO pages (position 8-25 with high impressions)
- **Cannibalization** issues between pSEO pages

#### 1C: Page Sample Collection

Select a **stratified random sample** of pages for quality testing:

- 30% from highest-performing pSEO pages (by clicks from GSC)
- 30% from lowest-performing pSEO pages
- 20% from newest pSEO pages (check JSON file `lastModified` or file mtime)
- 20% random selection across different categories

For each sampled page, use WebFetch to capture:

- Full rendered content
- Word count
- Unique data points present (upscaling-specific stats, format specs, device specs, etc.)
- Template text percentage
- Schema markup (use `pagespeed` or inspect meta tags)
- Internal links count
- CTA presence and position (Try Free / Upload Image buttons)
- Before/after examples presence

#### 1D: Core Web Vitals (Page Performance)

**Invoke the `/pagespeed` skill** on 2-3 sampled pSEO pages to capture Core Web Vitals:

```
Use the Skill tool: skill="pagespeed", args="https://myimageupscaler.com/scale/[sampled-slug]"
```

Pick one high-performing and one low-performing pSEO page from the GSC data. Record:

- **LCP** (Largest Contentful Paint) — target < 2.5s (baseline: mobile 7.8s, desktop good)
- **CLS** (Cumulative Layout Shift) — target < 0.1
- **TBT** (Total Blocking Time) — target < 200ms
- **Performance score** (mobile & desktop) — baseline: mobile 56, desktop 91
- **SEO score** from Lighthouse — baseline: 100/100

These feed into the Engagement Sustainability Test (Phase 2, Test 3) and Quality Score (Phase 3).

---

### Phase 2: Value Threshold Framework

Apply three tests to the sampled pages:

#### Test 1: Unique Answer Test

> "If you can swap one modifier and retain 85%+ identical content, you fail."

For each sampled page:

1. Extract the page content via WebFetch
2. Compare with 2-3 sibling pages (same template, different image format/scale factor/use case)
3. Calculate **content uniqueness percentage** (content that changes between siblings)

**Image upscaler-specific signals to check**:

- Does each scale page have unique guidance for that specific scale factor (2x vs 4x vs 8x)?
- Do format pages show unique quality/compression trade-offs per format (JPEG vs PNG vs WebP)?
- Do use-case pages have unique workflows for that specific use case?
- Do alternatives pages have genuine differentiators vs each competitor?

**Scoring:**

- 60%+ unique content across siblings: ✅ PASS (3 points)
- 40-59% unique: 🟡 MARGINAL (1 point)
- Below 40% unique: ❌ FAIL (0 points) — **Scaled Content Abuse risk**

#### Test 2: Data Substantiation Test

> "Minimum 40% of page content requires unique data sources that competitors couldn't replicate."

For each sampled page, check for image-upscaling-specific data points:

- Format-specific compression ratios and quality metrics
- Scale-factor-specific use case guidance (print DPI requirements, screen resolutions)
- Platform-specific image dimension requirements (Instagram, Twitter, etc.)
- Device-specific optimization tips (iPhone camera RAW handling, etc.)
- Before/after example images
- Processing time benchmarks
- Supported file size limits
- Real comparison data vs competitors (for alternatives/comparison pages)

**Scoring:**

- 5+ unique data points with real data: ✅ PASS (3 points)
- 3-4 unique data points: 🟡 MARGINAL (2 points)
- 0-2 unique data points: ❌ FAIL (0 points)

#### Test 3: Engagement Sustainability Test

> "Programmatic pages should match hand-crafted content engagement within 30%."

Compare pSEO page metrics against site-wide averages from GSC:

- **CTR** of pSEO pages vs site average
- **Average position** trend (improving, stable, declining)
- **Impressions** per page (growing, flat, declining over 90 days)
- Note: bounce rate / time on page not available via GSC — use as limitation

**Scoring:**

- Within 30% of site average: ✅ PASS (3 points)
- 30-50% below average: 🟡 MARGINAL (1 point)
- 50%+ below average: ❌ FAIL (0 points)

**Value Threshold Score** = Sum of three tests / 9 \* 100 (0-100)

---

### Phase 3: Automated Quality Scoring (0-100)

Score the overall pSEO program on five dimensions:

| Dimension                   | Points | How to Measure                                                    |
| --------------------------- | ------ | ----------------------------------------------------------------- |
| Unique content percentage   | 20     | Average uniqueness from Test 1 across all sampled pages           |
| Unique data points per page | 15     | Average data substantiation from Test 2                           |
| Engagement vs site average  | 25     | CTR and position comparison from Test 3                           |
| Organic traffic trend       | 20     | Are pSEO pages gaining or losing impressions/clicks over 90 days? |
| Conversion actions          | 20     | CTA presence (Try Free / Upload Image), above-fold, clear path    |

**Quality tiers:**

- **80-100**: 🚀 Excellent — safe to scale aggressively
- **60-79**: ✅ Good — maintain current pace, optimize weak areas
- **40-59**: ⚠️ Warning — pause scaling, enhance existing pages first
- **Below 40**: 🚨 Critical — stop creating, consider pruning worst performers

---

### Phase 4: Traffic Light Assessment

Evaluate against three signal levels:

#### 🟢 Green Flags (Safe to Scale)

Check each and report status:

- [ ] Indexation rate 60%+ of submitted pSEO pages
- [ ] pSEO page engagement within 30% of site average CTR
- [ ] Consistent or growing organic traffic per pSEO page
- [ ] 5-15 internal links per pSEO page
- [ ] Crawl efficiency above 50% (indexed / crawled ratio)
- [ ] Content uniqueness above 60% across sibling pages
- [ ] No manual actions in Search Console
- [ ] No zombie categories serving 404s (ai-features issue resolved)

#### 🟡 Yellow Flags (Caution — Pause Scaling)

- [ ] Indexation rate 40-60%
- [ ] Engagement 30-50% below site average
- [ ] Flat or declining traffic per pSEO page over 90 days
- [ ] Crawl budget waste 30%+ (pages crawled but not indexed)
- [ ] More than 20% of pSEO pages with fewer than 3 unique data points
- [ ] Zombie/orphan categories in sitemap not serving valid pages

**Yellow action**: Pause new page creation. Audit top 100 pages. Implement improvements. Resume only after metrics recover.

#### 🔴 Red Flags (Stop Immediately)

- [ ] Indexation rate below 40%
- [ ] Engagement 50%+ below site average
- [ ] Site-wide traffic decline after pSEO launches
- [ ] Manual action notice in Search Console
- [ ] Crawl errors above 10% on pSEO pages
- [ ] Duplicate content warnings affecting 20%+ of pSEO pages
- [ ] Average content uniqueness below 40% (variable substitution pattern)

**Red action**: Halt all page creation. Emergency quality improvements. Consider noindexing or deleting worst 30% of pages. Request reconsideration if manual action.

---

### Phase 5: Scaling Readiness Assessment

Evaluate where the pSEO program sits on the maturity scale:

#### Stage Assessment

| Stage       | Page Count   | Requirements                                                         |
| ----------- | ------------ | -------------------------------------------------------------------- |
| Foundation  | 0-100        | Baseline metrics established, monitoring in place, pilot pages live  |
| Pilot       | 100-500      | 70%+ indexation, engagement within 30% of average, zero crawl errors |
| First Scale | 500-2,000    | Automated quality checks, engagement tracking by page group          |
| Growth      | 2,000-10,000 | Conditional indexing, engagement features, scoring systems           |
| Maturity    | 10,000+      | AI-powered enhancement, dynamic personalization, competitive moat    |

Current estimate: ~1,324 total pages (including locales) → likely **Pilot → First Scale** transition.

For the current stage, check:

1. **Are prerequisites met for the current stage?**
2. **Are prerequisites met to advance to the next stage?**
3. **What's blocking advancement?**

#### Scaling Rate Recommendation

Based on current health:

- Quality Score 80+: 🚀 Scale 20-30% monthly
- Quality Score 60-79: ✅ Scale 10-15% monthly
- Quality Score 40-59: ⚠️ No scaling — improve existing pages
- Quality Score below 40: 🚨 Prune 20-30% of worst pages

---

### Phase 6: Conditional Generation Model Compliance

Check if the pSEO system follows the four rules of safe content generation:

#### Rule 1: Data Requirement Gate

> "Minimum 5 unique, valuable data points required per page (not just keyword swaps)"

- Does the template enforce minimum data requirements before generating a page?
- Are pages generated for combinations with insufficient data?
- Check `app/seo/data/` JSON files for data completeness per category

#### Rule 2: Search Demand Validation

> "Prioritize by actual search volume and user request signals"

- Are pages generated for keywords with actual search demand?
- Check if any pages target zero-volume keywords
- Cross-reference sitemap pages against keyword research in `docs/SEO/`

#### Rule 3: Engagement-Based Indexing

> "Publish with noindex initially, monitor 2-4 weeks, conditionally remove noindex if metrics pass"

- Does the system use conditional indexing?
- Or are all pages immediately indexed?
- Check `generateMetadata` in pSEO page routes for robots directives

#### Rule 4: Continuous Quality Scoring

> "Automated quality scoring identifies underperforming pages for enhancement or deprecation"

- Is there an automated quality monitoring system?
- Are underperforming pages flagged for review?
- Has any pruning been done historically? (check git history on JSON data files)
- Are SEO tests in `tests/unit/seo/` covering quality thresholds?

---

### Phase 7: Penalty Risk Score

Calculate an overall penalty risk score (0-100, higher = more risk):

| Risk Factor                                | Weight | Score Calculation                                          |
| ------------------------------------------ | ------ | ---------------------------------------------------------- |
| Content uniqueness below 60%               | 25%    | (60 - actual_uniqueness) \* 2.5 if below 60%, else 0       |
| Indexation rate below 60%                  | 20%    | (60 - actual_indexation) \* 2.0 if below 60%, else 0       |
| No unique data points (variable swap only) | 20%    | % of pages with fewer than 3 unique data points \* 100     |
| Engagement 30%+ below site average         | 15%    | Normalized engagement gap percentage                       |
| Page count exceeds authority ratio         | 10%    | Pages / (DA \* 10) if ratio > 1, capped at 100 (DA ≈ 0)    |
| Missing conditional generation gates       | 10%    | 0, 33, 66, or 100 based on how many of 4 rules are missing |

**Risk levels:**

- **0-20**: 🟢 Low risk — continue operations
- **21-40**: 🟡 Moderate risk — implement monitoring improvements
- **41-60**: 🟠 High risk — pause scaling, improve quality
- **61-80**: 🔴 Critical risk — stop creation, begin pruning
- **81-100**: 🆘 Emergency — immediate action required, mass noindex underperformers

---

## Output Report

Write the report to `docs/SEO/reports/pseo-audit-YYYY-MM-DD.md`:

```markdown
# Programmatic SEO Health Audit — MyImageUpscaler

**Date:** YYYY-MM-DD
**Auditor:** pSEO Audit Skill
**Pages in Program:** X total (by category breakdown)
**Pages Sampled:** N pages
**Mode:** Standard / Deep

---

## Executive Summary

### Overall Program Health: [EMOJI] RATING (Score/100)

| Metric                 | Value   | Status   | Benchmark              |
| ---------------------- | ------- | -------- | ---------------------- |
| Quality Score          | XX/100  | 🟢/🟡/🔴 | 80+ = 🟢               |
| Penalty Risk Score     | XX/100  | 🟢/🟡/🔴 | Below 20 = 🟢 Safe     |
| Indexation Rate        | XX%     | 🟢/🟡/🔴 | 60%+ = 🟢              |
| Content Uniqueness     | XX%     | 🟢/🟡/🔴 | 60%+ = 🟢              |
| Value Threshold Score  | XX/100  | 🟢/🟡/🔴 | 67%+ = 🟢              |
| Scaling Stage          | [Stage] | -        | -                      |
| Scaling Recommendation | [Rate]  | -        | Based on quality score |

### Signal Status: 🟢 GREEN / 🟡 YELLOW / 🔴 RED

[1-2 sentence summary of the overall signal and what it means]

---

## 1. Value Threshold Framework Results

### Test 1: Unique Answer Test — ✅ PASS / 🟡 MARGINAL / ❌ FAIL

[Details of sibling comparison, uniqueness percentages, specific examples]

### Test 2: Data Substantiation Test — ✅ PASS / 🟡 MARGINAL / ❌ FAIL

[Details of unique data points found per page, what's present vs missing]

### Test 3: Engagement Sustainability Test — ✅ PASS / 🟡 MARGINAL / ❌ FAIL

[GSC metrics comparison: pSEO vs site average for CTR, position, impressions]

---

## 2. Quality Score Breakdown (XX/100)

| Dimension             | Score | Max | Evidence                   |
| --------------------- | ----- | --- | -------------------------- |
| Unique Content %      | XX    | 20  | Avg XX% across siblings    |
| Unique Data Points    | XX    | 15  | Avg X.X per page           |
| Engagement vs Average | XX    | 25  | CTR: X.X% vs X.X% average  |
| Organic Traffic Trend | XX    | 20  | [Growing/Stable/Declining] |
| Conversion Actions    | XX    | 20  | CTA above fold: X/N pages  |

**Tier:** 🚀 Excellent / ✅ Good / ⚠️ Warning / 🚨 Critical

---

## 3. Traffic Light Assessment

### Green Flags Passing: X/8

[List each flag with status]

### Yellow Flags Triggered: X/6

[List each flag with status and evidence]

### Red Flags Triggered: X/7

[List each flag with status and evidence]

**Signal:** 🟢 GREEN / 🟡 YELLOW / 🔴 RED

---

## 4. Indexation Health

| Metric                   | Value | Benchmark   | Status   |
| ------------------------ | ----- | ----------- | -------- |
| Pages Submitted          | X     | -           | -        |
| Pages Indexed            | X     | 60%+ of sub | 🟢/🟡/🔴 |
| Indexation Rate          | XX%   | 60%+        | 🟢/🟡/🔴 |
| Not Indexed - Discovered | X     | < 10%       | 🟢/🟡/🔴 |
| Not Indexed - Crawled    | X     | < 15%       | 🟢/🟡/🔴 |
| Not Indexed - Excluded   | X     | < 5%        | 🟢/🟡/🔴 |
| Crawl Efficiency         | XX%   | 50%+        | 🟢/🟡/🔴 |

### Zombie/Orphan Category Status

| Category    | Data File     | Route    | Status        |
| ----------- | ------------- | -------- | ------------- |
| ai-features | 12 pages      | None     | ⚠️ 404 zombie |
| [others]    | [pages count] | [route?] | [status]      |

---

## 5. Penalty Risk Assessment (XX/100)

| Risk Factor                | Score | Max | Evidence  |
| -------------------------- | ----- | --- | --------- |
| Content Uniqueness Gap     | XX    | 25  | [details] |
| Indexation Gap             | XX    | 20  | [details] |
| Missing Data Points        | XX    | 20  | [details] |
| Engagement Gap             | XX    | 15  | [details] |
| Authority/Page Ratio       | XX    | 10  | [details] |
| Generation Gate Compliance | XX    | 10  | [details] |

**Risk Level:** 🟢 Low / 🟡 Moderate / 🟠 High / 🔴 Critical / 🆘 Emergency

[Specific penalty risks identified with evidence]

---

## 6. Scaling Readiness

**Current Stage:** [Foundation / Pilot / First Scale / Growth / Maturity]
**Current Page Count:** X (English) / X (including locales)
**Next Stage Requirements:**

| Requirement     | Met?  | Current Value | Target   |
| --------------- | ----- | ------------- | -------- |
| [Requirement 1] | ✅/❌ | [value]       | [target] |
| [Requirement 2] | ✅/❌ | [value]       | [target] |
| [Requirement 3] | ✅/❌ | [value]       | [target] |

**Scaling Recommendation:** [XX% monthly / Pause / Prune]

---

## 7. Conditional Generation Compliance

| Rule                       | Implemented?         | Evidence  |
| -------------------------- | -------------------- | --------- |
| Data Requirement Gate      | ✅ / 🟡 Partial / ❌ | [details] |
| Search Demand Validation   | ✅ / 🟡 Partial / ❌ | [details] |
| Engagement-Based Indexing  | ✅ / 🟡 Partial / ❌ | [details] |
| Continuous Quality Scoring | ✅ / 🟡 Partial / ❌ | [details] |

**Compliance:** X/4 rules implemented

---

## 8. Page Sample Details

| Page URL        | Category | Uniqueness | Data Points | CTA | Schema | Links | Quality |
| --------------- | -------- | ---------- | ----------- | --- | ------ | ----- | ------- |
| /scale/[slug]   | scale    | XX%        | X           | Y/N | Y/N    | X     | XX/100  |
| /formats/[slug] | formats  | XX%        | X           | Y/N | Y/N    | X     | XX/100  |
| ...             | ...      | ...        | ...         | ... | ...    | ...   | ...     |

---

## 9. Prioritized Action Plan

### Immediate (This Week)

[Critical items with specific file paths and changes needed]

### Short-Term (This Month)

[High-impact improvements]

### Medium-Term (This Quarter)

[Scaling preparation and quality improvements]

### Ongoing Monitoring

[Metrics to track and alert thresholds]

---

## 10. Comparison with Best-in-Class

### How Top pSEO Programs Succeed

**Canva Model** (image editing tool pages):

- Unique per-format design templates with real examples
- Platform-specific dimension guides with visual previews
- Tool-specific tutorials that solve real workflow problems

**Cloudinary / Imgix Model** (image processing docs):

- Format comparison tables with real benchmark data
- Use-case specific transformation guides
- Before/after quality comparisons with real images

**Our Gap vs Best-in-Class:**
[Specific comparison of our pages against these models]

---

## Methodology

- **Framework:** Value Threshold Framework (Unique Answer, Data Substantiation, Engagement Sustainability)
- **Quality Scoring:** 5-dimension weighted scoring (0-100)
- **Penalty Risk:** 6-factor weighted risk assessment (0-100)
- **Data Sources:** GSC API, sitemap crawl, page content analysis, `app/seo/data/` JSON files
- **Reference:** [The Programmatic SEO Paradox](https://guptadeepak.com/the-programmatic-seo-paradox-why-your-fear-of-creating-thousands-of-pages-is-both-valid-and-obsolete/)
```

---

## Alert System

If `--alert-only` is set, skip the full report and only output alerts:

### 🆘 Level 1: Manual Action Alert

- **Trigger:** Manual action notice in GSC
- **Action:** Halt all creation, audit flagged pages, implement fixes, submit reconsideration
- **Recovery:** 2-4 weeks for review

### 🔴 Level 2: Indexation Collapse Alert

- **Trigger:** 30%+ drop in indexed pSEO pages
- **Action:** Pause new pages 2-3 months, emergency quality improvements
- **Recovery:** 3-6 months

### 🔴 Level 3: Site-Wide Traffic Collapse Alert

- **Trigger:** 40%+ organic traffic drop within 2 weeks, multiple page types affected
- **Action:** Site-wide quality review, consider aggressive pruning
- **Recovery:** 3-12 months

### ⚠️ Warning 1: Engagement Deterioration

- **Trigger:** 15%+ bounce rate increase or 20%+ time-on-page decrease
- **Action:** Pause creation, user testing, engagement improvements
- **Recovery:** 2-4 weeks

### ⚠️ Warning 2: Crawl Budget Strain

- **Trigger:** Crawl rate decrease despite new pages, 40%+ "not indexed" ratio
- **Action:** 50% reduction in creation rate, improve internal linking, optimize page speed
- **Recovery:** 4-8 weeks

---

## Execution Pipeline

### Step 1: Initialize

1. Parse arguments (`--deep`, `--pages=N`, `--alert-only`)
2. Check for prior pSEO audit reports: `ls docs/SEO/reports/pseo-audit-*.md`
3. Create output directory if needed: `mkdir -p docs/SEO/reports`
4. Display execution plan

### Step 2: Data Collection (Parallel)

Launch 4 parallel tasks:

- **Task A:** Read `app/seo/data/*.json` to inventory all pSEO pages by category; check for zombie/orphan categories
- **Task B:** Invoke `/gsc-analysis myimageupscaler.com` skill to get full GSC data + analysis
- **Task C:** Sample N pages and fetch their content via WebFetch (stratified across categories)
- **Task D:** Invoke `/pagespeed` skill on 2-3 sampled pSEO pages for Core Web Vitals

### Step 3: Analysis (Sequential)

1. Run Value Threshold Framework tests on sampled pages
2. Calculate Quality Score
3. Evaluate Traffic Light signals
4. Calculate Penalty Risk Score
5. Assess Scaling Readiness
6. Check Conditional Generation Compliance

### Step 4: Codebase Check

Examine the pSEO system code for structural risks:

```bash
# Check pSEO route handlers for robots/noindex directives
grep -r "robots" app/seo/ app/scale/ app/formats/ app/use-cases/ --include="*.ts" --include="*.tsx"

# Check data completeness (fields per entry)
# Look at: app/seo/data/*.json - how much unique data per entry?
# Check: lib/seo/ - content generation / sitemap logic
# Check: tests/unit/seo/ - quality threshold tests

# Verify zombie categories
grep -r "ai-features" app/ lib/ --include="*.ts" --include="*.tsx"
```

### Step 5: Report Generation

1. Compile all findings into the report template
2. Calculate trend vs prior audit (if exists — check `docs/SEO/reports/pseo-audit-*.md`)
3. Write report to `docs/SEO/reports/pseo-audit-YYYY-MM-DD.md`
4. Display summary to user

---

## Error Handling

| Error                       | Action                                                        |
| --------------------------- | ------------------------------------------------------------- |
| `/gsc-analysis` skill fails | Fall back to manual GSC script if available, note in report   |
| `/pagespeed` skill fails    | Skip Core Web Vitals section, note limitation in report       |
| Sitemap unreachable         | Try localhost:3000, fall back to reading route files directly |
| WebFetch fails on pages     | Reduce sample size, note in report                            |
| No prior audit for trends   | Skip trend comparison, note "First audit"                     |
| Insufficient GSC data       | Flag as limitation, score engagement as "N/A"                 |
| JSON parse fails            | Note corrupted data file, flag as risk                        |

---

## Skills Invoked by This Audit

These skills are called automatically during the audit — do NOT skip them:

| Skill           | Phase | Purpose                                                               |
| --------------- | ----- | --------------------------------------------------------------------- |
| `/gsc-analysis` | 1B    | GSC data: indexation, performance, low-hanging fruit, cannibalization |
| `/pagespeed`    | 1D    | Core Web Vitals on sampled pSEO pages (LCP, CLS, TBT, scores)         |

## Related Skills & Agents

- **seo-pseo-content-auditor** (agent): Page-by-page content quality audit with Playwright
- **pseo-system** (skill): Creating and managing pSEO pages
- **seo-audit** (skill): General site-wide SEO audit
- **seo-manager** (skill): Full SEO orchestrator across all dimensions
- **competitor-sitemap-spy** (skill): Compare pSEO strategy against competitors
- **gsc-analysis** (skill): Google Search Console data fetching and analysis
