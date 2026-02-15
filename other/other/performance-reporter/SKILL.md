---
name: performance-reporter
description: 'Use when the user asks to "generate SEO report", "performance report", "traffic report", "SEO dashboard", "report to stakeholders", "show me the numbers", "monthly SEO report", or "present SEO results to my boss". Generates comprehensive SEO and GEO performance reports combining rankings, traffic, backlinks, and AI visibility metrics. Creates executive summaries and detailed analyses for stakeholder reporting. For detailed rank tracking, see rank-tracker. For link-specific analysis, see backlink-analyzer.'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - performance report
    - seo report
    - traffic analysis
    - seo dashboard
    - executive summary
    - analytics report
    - kpi tracking
  triggers:
    - "generate SEO report"
    - "performance report"
    - "traffic report"
    - "SEO dashboard"
    - "report to stakeholders"
    - "monthly report"
    - "SEO analytics"
    - "show me the numbers"
    - "monthly SEO report"
    - "present SEO results to my boss"
---

# Performance Reporter


> **[SEO & GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills for SEO + GEO · Install all: `npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>Browse all 20 skills</summary>

**Research** · [keyword-research](../../research/keyword-research/) · [competitor-analysis](../../research/competitor-analysis/) · [serp-analysis](../../research/serp-analysis/) · [content-gap-analysis](../../research/content-gap-analysis/)

**Build** · [seo-content-writer](../../build/seo-content-writer/) · [geo-content-optimizer](../../build/geo-content-optimizer/) · [meta-tags-optimizer](../../build/meta-tags-optimizer/) · [schema-markup-generator](../../build/schema-markup-generator/)

**Optimize** · [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) · [technical-seo-checker](../../optimize/technical-seo-checker/) · [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) · [content-refresher](../../optimize/content-refresher/)

**Monitor** · [rank-tracker](../rank-tracker/) · [backlink-analyzer](../backlink-analyzer/) · **performance-reporter** · [alert-manager](../alert-manager/)

**Cross-cutting** · [content-quality-auditor](../../cross-cutting/content-quality-auditor/) · [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) · [entity-optimizer](../../cross-cutting/entity-optimizer/) · [memory-management](../../cross-cutting/memory-management/)

</details>

This skill creates comprehensive SEO and GEO performance reports that combine multiple metrics into actionable insights. It produces executive summaries, detailed analyses, and visual data presentations for stakeholder communication.

## When to Use This Skill

- Monthly/quarterly SEO reporting
- Executive stakeholder updates
- Client reporting for agencies
- Tracking campaign performance
- Combining multiple SEO metrics
- Creating GEO visibility reports
- Documenting ROI from SEO efforts

## What This Skill Does

1. **Data Aggregation**: Combines multiple SEO data sources
2. **Trend Analysis**: Identifies patterns across metrics
3. **Executive Summaries**: Creates high-level overviews
4. **Visual Reports**: Presents data in clear formats
5. **Benchmark Comparison**: Tracks against goals and competitors
6. **Content Quality Tracking**: Integrates CORE-EEAT scores across audited pages
7. **ROI Calculation**: Measures SEO investment returns
8. **Recommendations**: Suggests actions based on data

## How to Use

### Generate Performance Report

```
Create an SEO performance report for [domain] for [time period]
```

### Executive Summary

```
Generate an executive summary of SEO performance for [month/quarter]
```

### Specific Report Types

```
Create a GEO visibility report for [domain]
```

```
Generate a content performance report
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~analytics + ~~search console + ~~SEO tool + ~~AI monitor connected:**
Automatically aggregate traffic metrics from ~~analytics, search performance data from ~~search console, ranking and backlink data from ~~SEO tool, and GEO visibility metrics from ~~AI monitor. Creates comprehensive multi-source reports with historical trends.

**With manual data only:**
Ask the user to provide:
1. Analytics screenshots or traffic data export (sessions, users, conversions)
2. Search Console data (impressions, clicks, average position)
3. Keyword ranking data for the reporting period
4. Backlink metrics (referring domains, new/lost links)
5. Key performance indicators and goals for comparison
6. AI citation data if tracking GEO metrics

Proceed with the full analysis using provided data. Note in the output which metrics are from automated collection vs. user-provided data.

## Instructions

When a user requests a performance report:

1. **Define Report Parameters**

   ```markdown
   ## Report Configuration
   
   **Domain**: [domain]
   **Report Period**: [start date] to [end date]
   **Comparison Period**: [previous period for comparison]
   **Report Type**: [Monthly/Quarterly/Annual/Custom]
   **Audience**: [Executive/Technical/Client]
   **Focus Areas**: [Rankings/Traffic/Content/Backlinks/GEO]
   ```

2. **Create Executive Summary**

   ```markdown
   # SEO Performance Report
   
   **Domain**: [domain]
   **Period**: [date range]
   **Prepared**: [date]
   
   ---
   
   ## Executive Summary
   
   ### Overall Performance: [Excellent/Good/Needs Attention/Critical]
   
   **Key Highlights**:
   
   🟢 **Wins**:
   - [Win 1 - e.g., "Organic traffic increased 25%"]
   - [Win 2 - e.g., "3 new #1 rankings achieved"]
   - [Win 3 - e.g., "Conversion rate improved 15%"]
   
   🟡 **Watch Areas**:
   - [Area 1 - e.g., "Mobile rankings declining slightly"]
   - [Area 2 - e.g., "Competitor gaining ground on key terms"]
   
   🔴 **Action Required**:
   - [Issue 1 - e.g., "Technical SEO audit needed"]
   
   ### Key Metrics at a Glance
   
   | Metric | This Period | Last Period | Change | Target | Status |
   |--------|-------------|-------------|--------|--------|--------|
   | Organic Traffic | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   | Keyword Rankings (Top 10) | [X] | [Y] | [+/-Z] | [T] | ✅/⚠️/❌ |
   | Organic Conversions | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   | Domain Authority | [X] | [Y] | [+/-Z] | [T] | ✅/⚠️/❌ |
   | AI Citations | [X] | [Y] | [+/-Z%] | [T] | ✅/⚠️/❌ |
   
   ### SEO ROI
   
   **Investment**: $[X] (content, tools, effort)
   **Organic Revenue**: $[Y]
   **ROI**: [Z]%
   ```

3. **Report Organic Traffic Performance**

   ```markdown
   ## Organic Traffic Analysis
   
   ### Traffic Overview
   
   | Metric | This Period | vs Last Period | vs Last Year |
   |--------|-------------|----------------|--------------|
   | Sessions | [X] | [+/-Y%] | [+/-Z%] |
   | Users | [X] | [+/-Y%] | [+/-Z%] |
   | Pageviews | [X] | [+/-Y%] | [+/-Z%] |
   | Avg. Session Duration | [X] | [+/-Y%] | [+/-Z%] |
   | Bounce Rate | [X]% | [+/-Y%] | [+/-Z%] |
   | Pages per Session | [X] | [+/-Y] | [+/-Z] |
   
   ### Traffic Trend
   
   ```
   [Month 1]  ████████████████████ [X]
   [Month 2]  █████████████████████ [Y]
   [Month 3]  ███████████████████████ [Z]
   [Current]  ████████████████████████ [W]
   ```
   
   ### Traffic by Source
   
   | Channel | Sessions | % of Total | Change |
   |---------|----------|------------|--------|
   | Organic Search | [X] | [Y]% | [+/-Z%] |
   | Direct | [X] | [Y]% | [+/-Z%] |
   | Referral | [X] | [Y]% | [+/-Z%] |
   | Social | [X] | [Y]% | [+/-Z%] |
   
   ### Top Performing Pages
   
   | Page | Sessions | Change | Conversions |
   |------|----------|--------|-------------|
   | [Page 1] | [X] | [+/-Y%] | [Z] |
   | [Page 2] | [X] | [+/-Y%] | [Z] |
   | [Page 3] | [X] | [+/-Y%] | [Z] |
   
   ### Traffic by Device
   
   | Device | Sessions | Change | Conv. Rate |
   |--------|----------|--------|------------|
   | Desktop | [X] ([Y]%) | [+/-Z%] | [%] |
   | Mobile | [X] ([Y]%) | [+/-Z%] | [%] |
   | Tablet | [X] ([Y]%) | [+/-Z%] | [%] |
   ```

4. **Report Keyword Rankings**

   ```markdown
   ## Keyword Ranking Performance
   
   ### Rankings Overview
   
   | Position Range | Keywords | Change | Traffic Impact |
   |----------------|----------|--------|----------------|
   | Position 1 | [X] | [+/-Y] | [Z] sessions |
   | Position 2-3 | [X] | [+/-Y] | [Z] sessions |
   | Position 4-10 | [X] | [+/-Y] | [Z] sessions |
   | Position 11-20 | [X] | [+/-Y] | [Z] sessions |
   | Position 21-50 | [X] | [+/-Y] | [Z] sessions |
   
   ### Ranking Distribution Change
   
   ```
   Last Period:  ▓▓▓▓░░░░░░░░░░░░
   This Period:  ▓▓▓▓▓▓░░░░░░░░░░
                 ↑ More keywords in top positions
   ```
   
   ### Top Ranking Improvements
   
   | Keyword | Previous | Current | Change | Traffic |
   |---------|----------|---------|--------|---------|
   | [kw 1] | [X] | [Y] | +[Z] | [sessions] |
   | [kw 2] | [X] | [Y] | +[Z] | [sessions] |
   | [kw 3] | [X] | [Y] | +[Z] | [sessions] |
   
   ### Rankings That Declined
   
   | Keyword | Previous | Current | Change | Impact | Action |
   |---------|----------|---------|--------|--------|--------|
   | [kw 1] | [X] | [Y] | -[Z] | -[sessions] | [action] |
   
   ### SERP Feature Performance
   
   | Feature | Won | Lost | Opportunities |
   |---------|-----|------|---------------|
   | Featured Snippets | [X] | [Y] | [Z] |
   | People Also Ask | [X] | [Y] | [Z] |
   | Local Pack | [X] | [Y] | [Z] |
   ```

5. **Report GEO/AI Performance**

   ```markdown
   ## GEO (AI Visibility) Performance
   
   ### AI Citation Overview
   
   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | Keywords with AI Overview | [X]/[Y] | [X]/[Y] | [+/-Z] |
   | Your AI Citations | [X] | [Y] | [+/-Z%] |
   | Citation Rate | [X]% | [Y]% | [+/-Z%] |
   | Avg Citation Position | [X] | [Y] | [+/-Z] |
   
   ### AI Citation by Topic
   
   | Topic Cluster | Opportunities | Citations | Rate |
   |---------------|---------------|-----------|------|
   | [Topic 1] | [X] | [Y] | [Z]% |
   | [Topic 2] | [X] | [Y] | [Z]% |
   | [Topic 3] | [X] | [Y] | [Z]% |
   
   ### GEO Wins This Period
   
   | Query | Citation Status | Source Page | Impact |
   |-------|-----------------|-------------|--------|
   | [query 1] | 🆕 New citation | [page] | High visibility |
   | [query 2] | ⬆️ Improved position | [page] | Better exposure |
   
   ### GEO Optimization Opportunities
   
   | Query | AI Overview | You Cited? | Gap | Action |
   |-------|-------------|------------|-----|--------|
   | [query] | Yes | No | [gap] | [action] |
   ```

6. **Report Domain Authority (CITE Score)**

   If a CITE domain audit has been run previously (via domain-authority-auditor), include domain authority trends:

   ```markdown
   ## Domain Authority (CITE Score)

   ### CITE Score Summary

   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | CITE Score | [X]/100 | [Y]/100 | [+/-Z] |
   | C — Citation | [X]/100 | [Y]/100 | [+/-Z] |
   | I — Identity | [X]/100 | [Y]/100 | [+/-Z] |
   | T — Trust | [X]/100 | [Y]/100 | [+/-Z] |
   | E — Eminence | [X]/100 | [Y]/100 | [+/-Z] |

   **Veto Status**: ✅ No triggers / ⚠️ [item] triggered

   ### Key Changes

   - [Notable improvement or concern 1]
   - [Notable improvement or concern 2]

   _For full 40-item evaluation, run `/seo:audit-domain`_
   ```

   **Note**: If no previous CITE audit exists, note this section as "Not yet evaluated — run domain-authority-auditor for baseline" and skip.

7. **Content Quality (CORE-EEAT Score)**

   If content-quality-auditor has been run on key pages (via `/seo:audit-page`), include content quality metrics:

   ```markdown
   ## Content Quality (CORE-EEAT Score)

   ### Content Quality Summary

   | Metric | Value |
   |--------|-------|
   | Pages Audited | [count] |
   | Average CORE-EEAT Score | [score]/100 ([rating]) |
   | Average GEO Score (CORE) | [score]/100 |
   | Average SEO Score (EEAT) | [score]/100 |
   | Veto Items Triggered | [count] ([item IDs]) |

   ### Dimension Averages Across Audited Pages

   | Dimension | Average Score | Trend |
   |-----------|--------------|-------|
   | C — Contextual Clarity | [score] | [↑/↓/→] |
   | O — Organization | [score] | [↑/↓/→] |
   | R — Referenceability | [score] | [↑/↓/→] |
   | E — Exclusivity | [score] | [↑/↓/→] |
   | Exp — Experience | [score] | [↑/↓/→] |
   | Ept — Expertise | [score] | [↑/↓/→] |
   | A — Authority | [score] | [↑/↓/→] |
   | T — Trust | [score] | [↑/↓/→] |

   ### Key Content Quality Changes

   - [Notable score changes since last report]
   - [Pages with significant quality improvements/declines]

   _For full 80-item evaluation, run `/seo:audit-page` on individual pages. See CORE-EEAT benchmark for methodology._
   ```

   **Note**: If no content quality audit exists, note this section as "Content quality not yet evaluated — run `/seo:audit-page` on key landing pages to establish baseline" and skip.

8. **Report Backlink Performance**

   ```markdown
   ## Backlink Performance
   
   ### Link Profile Summary
   
   | Metric | This Period | Last Period | Change |
   |--------|-------------|-------------|--------|
   | Total Backlinks | [X] | [Y] | [+/-Z] |
   | Referring Domains | [X] | [Y] | [+/-Z] |
   | Domain Authority | [X] | [Y] | [+/-Z] |
   | Avg. Link DA | [X] | [Y] | [+/-Z] |
   
   ### Link Acquisition
   
   | Period | New Links | Lost Links | Net |
   |--------|-----------|------------|-----|
   | Week 1 | [X] | [Y] | [+/-Z] |
   | Week 2 | [X] | [Y] | [+/-Z] |
   | Week 3 | [X] | [Y] | [+/-Z] |
   | Week 4 | [X] | [Y] | [+/-Z] |
   | **Total** | **[X]** | **[Y]** | **[+/-Z]** |
   
   ### Notable New Links
   
   | Source | DA | Type | Value |
   |--------|-----|------|-------|
   | [domain 1] | [DA] | [type] | High |
   | [domain 2] | [DA] | [type] | High |
   
   ### Competitive Position
   
   Your referring domains rank #[X] of [Y] competitors.
   ```

9. **Report Content Performance**

   ```markdown
   ## Content Performance
   
   ### Content Publishing Summary
   
   | Metric | This Period | Last Period | Target |
   |--------|-------------|-------------|--------|
   | New articles published | [X] | [Y] | [Z] |
   | Content updates | [X] | [Y] | [Z] |
   | Total word count | [X] | [Y] | - |
   
   ### Top Performing Content
   
   | Content | Traffic | Rankings | Conversions | Status |
   |---------|---------|----------|-------------|--------|
   | [Title 1] | [X] | [Y] keywords | [Z] | ⭐ Top performer |
   | [Title 2] | [X] | [Y] keywords | [Z] | 📈 Growing |
   | [Title 3] | [X] | [Y] keywords | [Z] | ✅ Stable |
   
   ### Content Needing Attention
   
   | Content | Issue | Traffic Change | Action |
   |---------|-------|----------------|--------|
   | [Title] | [issue] | -[X]% | [action] |
   
   ### Content ROI
   
   | Content Piece | Investment | Traffic Value | ROI |
   |---------------|------------|---------------|-----|
   | [Title 1] | $[X] | $[Y] | [Z]% |
   | [Title 2] | $[X] | $[Y] | [Z]% |
   ```

10. **Generate Recommendations**

   ```markdown
   ## Recommendations & Next Steps
   
   ### Immediate Actions (This Week)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🔴 High | [Action 1] | [Impact] | [Owner] |
   | 🔴 High | [Action 2] | [Impact] | [Owner] |
   
   ### Short-term (This Month)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🟡 Medium | [Action 1] | [Impact] | [Owner] |
   | 🟡 Medium | [Action 2] | [Impact] | [Owner] |
   
   ### Long-term (This Quarter)
   
   | Priority | Action | Expected Impact | Owner |
   |----------|--------|-----------------|-------|
   | 🟢 Planned | [Action 1] | [Impact] | [Owner] |
   
   ### Goals for Next Period
   
   | Metric | Current | Target | Action to Achieve |
   |--------|---------|--------|-------------------|
   | Organic Traffic | [X] | [Y] | [action] |
   | Keywords Top 10 | [X] | [Y] | [action] |
   | AI Citations | [X] | [Y] | [action] |
   | Referring Domains | [X] | [Y] | [action] |
   ```

11. **Compile Full Report**

   ```markdown
   # [Company] SEO & GEO Performance Report
   
   ## [Month/Quarter] [Year]
   
   ---
   
   ### Table of Contents
   
   1. Executive Summary
   2. Organic Traffic Performance
   3. Keyword Rankings
   4. GEO/AI Visibility
   5. Domain Authority (CITE Score)
   6. Content Quality (CORE-EEAT Score)
   7. Backlink Analysis
   8. Content Performance
   9. Technical Health
   10. Competitive Landscape
   11. Recommendations
   12. Appendix
   
   ---
   
   [Include all sections from above]
   
   ---
   
   ## Appendix
   
   ### Data Sources
   - ~~analytics (traffic and conversion data)
   - ~~search console (search performance)
   - ~~SEO tool (rankings and backlinks)
   - ~~AI monitor (GEO metrics)

   ### Methodology
   [Explain how metrics were calculated]

   ### Glossary
   - **GEO**: Generative Engine Optimization
   - **DA**: Domain Authority
   - [Additional terms]
   ```

## Validation Checkpoints

### Input Validation
- [ ] Reporting period clearly defined with comparison period
- [ ] All required data sources available or alternatives noted
- [ ] Target audience identified (executive/technical/client)
- [ ] Performance goals and KPIs established for benchmarking

### Output Validation
- [ ] Every metric cites its data source and collection date
- [ ] Trends include period-over-period comparisons
- [ ] Recommendations are specific, prioritized, and actionable
- [ ] Source of each data point clearly stated (~~analytics data, ~~search console data, ~~SEO tool data, user-provided, or estimated)

## Example

**User**: "Create a monthly SEO report for cloudhosting.com for January 2025"

**Output**:

```markdown
# CloudHosting SEO & GEO Performance Report

**Domain**: cloudhosting.com
**Period**: January 1-31, 2025
**Comparison**: vs December 2024
**Prepared**: February 3, 2025

---

## Executive Summary

### Overall Performance: Good

**Key Highlights**:

🟢 **Wins**:
- Organic traffic increased 15.3% (45,200 → 52,100 sessions)
- 4 new Top 10 keyword rankings in "cloud hosting" cluster
- Organic conversions up 11.8% (612 → 684 trial signups)

🟡 **Watch Areas**:
- Mobile page speed declining (LCP 3.1s → 3.4s)
- Competitor SiteGround gaining on "managed cloud hosting" terms

🔴 **Action Required**:
- Fix crawl errors on /pricing/ pages (37 404s detected)

### Key Metrics at a Glance

| Metric | Jan 2025 | Dec 2024 | Change | Target | Status |
|--------|----------|----------|--------|--------|--------|
| Organic Traffic | 52,100 | 45,200 | +15.3% | 50,000 | ✅ |
| Keywords Top 10 | 87 | 79 | +8 | 90 | ⚠️ |
| Organic Conversions | 684 | 612 | +11.8% | 700 | ⚠️ |
| Domain Rating | 54 | 53 | +1 | 55 | ⚠️ |
| AI Citations | 18 | 12 | +50.0% | 20 | ⚠️ |

### SEO ROI

**Investment**: $8,200 (content production, tools, link building)
**Organic Revenue**: $41,040 (684 trials × 12% close rate × $500 MRR)
**ROI**: 400%

---

## Organic Traffic Analysis

### Traffic Overview

| Metric | Jan 2025 | vs Dec 2024 | vs Jan 2024 |
|--------|----------|-------------|-------------|
| Sessions | 52,100 | +15.3% | +38.2% |
| Users | 41,680 | +14.1% | +35.7% |
| Pageviews | 98,990 | +12.6% | +29.4% |
| Avg. Session Duration | 2m 48s | +6.2% | +18.3% |
| Bounce Rate | 42.3% | -3.1% | -8.7% |

### Top Performing Pages

| Page | Sessions | Change | Conversions |
|------|----------|--------|-------------|
| /guide/cloud-hosting | 8,420 | +22.1% | 142 |
| /compare/aws-vs-gcp | 5,310 | +31.4% | 87 |
| /pricing | 4,890 | +9.8% | 201 |

---

## GEO (AI Visibility) Performance

### AI Citation Overview

| Metric | Jan 2025 | Dec 2024 | Change |
|--------|----------|----------|--------|
| Keywords with AI Overview | 34/120 | 28/120 | +6 |
| Your AI Citations | 18 | 12 | +50.0% |
| Citation Rate | 15.0% | 10.0% | +5.0% |
| Avg Citation Position | 2.4 | 3.1 | +0.7 |

### GEO Wins This Period

| Query | Citation Status | Source Page | Impact |
|-------|-----------------|-------------|--------|
| "best cloud hosting for startups" | 🆕 New citation | /guide/cloud-hosting | High visibility |
| "cloud hosting vs shared hosting" | ⬆️ Position 4→2 | /compare/cloud-vs-shared | Better exposure |
| "managed cloud hosting benefits" | 🆕 New citation | /features/managed | High visibility |

---

## Domain Authority (CITE Score)

### CITE Score Summary

| Metric | Jan 2025 | Dec 2024 | Change |
|--------|----------|----------|--------|
| CITE Score | 71/100 | 67/100 | +4 |
| C — Citation | 68/100 | 65/100 | +3 |
| I — Identity | 55/100 | 52/100 | +3 |
| T — Trust | 82/100 | 80/100 | +2 |
| E — Eminence | 61/100 | 58/100 | +3 |

**Veto Status**: ✅ No triggers

_For full 40-item evaluation, run `/seo:audit-domain`_

---

## Recommendations & Next Steps

### Immediate Actions (This Week)

| Priority | Action | Expected Impact | Owner |
|----------|--------|-----------------|-------|
| P0 | Fix 37 crawl errors on /pricing/ pages | Recover ~800 lost sessions/month | Dev team |

### Short-term (This Month)

| Priority | Action | Expected Impact | Owner |
|----------|--------|-----------------|-------|
| P1 | Optimize mobile LCP on top 10 landing pages | Improve mobile rankings for 15+ keywords | Dev team |
| P1 | Publish 3 comparison pages targeting AI Overview queries | +5-8 new AI citations | Content team |

### Long-term (This Quarter)

| Priority | Action | Expected Impact | Owner |
|----------|--------|-----------------|-------|
| P2 | Build Wikidata entry and Schema.org for CloudHost Inc. | Strengthen CITE Identity score by +10 pts | SEO lead |
```

## Report Templates by Audience

### Executive Report (1 page)

Focus on: Business impact, ROI, top-line metrics, key recommendations

### Marketing Team Report (3-5 pages)

Focus on: Detailed metrics, content performance, campaign results

### Technical SEO Report (5-10 pages)

Focus on: Crawl data, technical issues, detailed rankings, backlink analysis

### Client Report (2-3 pages)

Focus on: Progress against goals, wins, clear recommendations

## Tips for Success

1. **Lead with insights** - Start with what matters, not raw data
2. **Visualize data** - Charts and graphs improve comprehension
3. **Compare periods** - Context makes data meaningful
4. **Include actions** - Every report should drive decisions
5. **Customize for audience** - Executives need different info than technical teams
6. **Track GEO metrics** - AI visibility is increasingly important

## SEO/GEO Metric Definitions and Benchmarks

### Organic Search Metrics

| Metric | Definition | Good Range | Warning | Source |
|--------|-----------|-----------|---------|--------|
| Organic sessions | Visits from organic search | Growing MoM | >10% decline | ~~analytics |
| Keyword visibility | % of target keywords in top 100 | >60% | <40% | ~~SEO tool |
| Average position | Mean position across tracked keywords | <20 | >30 | ~~search console |
| Organic CTR | Clicks / impressions from search | >3% | <1.5% | ~~search console |
| Pages indexed | Pages in Google index | Growing | Dropping | ~~search console |
| Organic conversion rate | Conversions / organic sessions | >2% | <0.5% | ~~analytics |
| Non-brand organic traffic | Organic traffic minus brand searches | >50% of total organic | <30% | ~~analytics |

### GEO/AI Visibility Metrics

| Metric | Definition | Good Range | Warning | Source |
|--------|-----------|-----------|---------|--------|
| AI citation rate | % of monitored queries citing your content | >20% | <5% | ~~AI monitor |
| AI citation position | Average position in AI response citations | Top 3 sources | Not cited | ~~AI monitor |
| AI answer coverage | % of your topics appearing in AI answers | Growing | Declining | ~~AI monitor |
| Brand mention in AI | Times your brand is mentioned in AI responses | Growing | Zero | ~~AI monitor |

### Domain Authority Metrics

| Metric | Definition | Good Range | Warning | Source |
|--------|-----------|-----------|---------|--------|
| Domain Rating/Authority | Overall domain strength | Growing | Declining | ~~SEO tool |
| Referring domains | Unique domains linking to you | Growing MoM | Loss >10% MoM | ~~link database |
| Backlink growth rate | Net new backlinks per month | Positive | Negative trend | ~~link database |
| Toxic link ratio | Toxic links / total links | <5% | >10% | ~~link database |

## Reporting Templates by Audience

### Executive Report (C-Suite / Leadership)

**Focus:** Business outcomes, ROI, competitive position
**Length:** 1 page + appendix
**Frequency:** Monthly or Quarterly

| Section | Content |
|---------|---------|
| Traffic & Revenue | Organic traffic trend + attributed revenue |
| Competitive Position | Visibility share vs. top 3 competitors |
| AI Visibility | AI citation trend and coverage |
| Key Wins | Top 3 achievements with business impact |
| Risks | Top 3 concerns with proposed mitigation |
| Investment Ask | Resources needed for next period |

### Marketing Team Report

**Focus:** Channel performance, content effectiveness, technical health
**Length:** 2-3 pages
**Frequency:** Monthly

| Section | Content |
|---------|---------|
| Keyword Performance | Rankings gained/lost, new keywords discovered |
| Content Performance | Top pages by traffic, engagement, conversions |
| Technical Health | Crawl errors, speed scores, indexation |
| Backlink Profile | New links, lost links, quality assessment |
| GEO Performance | AI citation changes, new citations |
| Action Items | P0-P3 prioritized task list |

### Technical SEO Report

**Focus:** Crawlability, indexation, speed, errors
**Length:** Detailed
**Frequency:** Weekly or Bi-weekly

| Section | Content |
|---------|---------|
| Crawl Stats | Pages crawled, errors, crawl budget usage |
| Index Coverage | Indexed/excluded/errored pages |
| Core Web Vitals | LCP, CLS, INP trends |
| Error Log | New 4xx/5xx errors with resolution status |
| Schema Validation | New warnings, rich result eligibility |
| Technical Debt | Outstanding issues by priority |

## Trend Analysis Framework

### Period-Over-Period Analysis

| Comparison | Best For | Limitation |
|-----------|---------|-----------|
| Week over week (WoW) | Detecting sudden changes | Noisy, affected by day-of-week patterns |
| Month over month (MoM) | Identifying trends | Seasonal bias |
| Year over year (YoY) | Accounting for seasonality | Does not reflect recent trajectory |
| Rolling 30-day average | Smoothing noise | Lags behind real changes |

### Trend Interpretation Guidelines

| Pattern | Likely Cause | Recommended Action |
|---------|-------------|-------------------|
| Steady growth | Strategy is working | Continue, optimize high performers |
| Sudden spike then drop | Viral content or algorithm volatility | Investigate cause, build on if repeatable |
| Gradual decline | Content decay, competition, technical debt | Comprehensive audit needed |
| Flat line | Plateau — existing strategy maxed out | New content areas, new link strategies |
| Seasonal pattern | Industry/demand cycles | Plan content calendar around peaks |

## SEO Attribution Guidance

### Attribution Challenges in SEO

| Challenge | Impact | Mitigation |
|----------|--------|-----------|
| Long conversion paths | SEO rarely gets last-touch credit | Use assisted conversions report |
| Brand vs. non-brand | Brand searches inflate organic metrics | Always separate brand/non-brand |
| Cross-device journeys | Mobile search to desktop conversion | Enable cross-device tracking |
| SEO + paid overlap | Cannibalization or lift? | Test turning off paid for branded terms |
| Content assists sales | Hard to attribute | Track content touches in CRM |

## Reference Materials

- [KPI Definitions](./references/kpi-definitions.md) — Complete SEO/GEO metric definitions with benchmarks, good ranges, and warning thresholds
- [Report Templates](./references/report-templates.md) — Report templates by audience (executive, marketing, technical, client)

## Related Skills

- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — Include CORE-EEAT scores as page-level content quality KPIs
- [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) — Include CITE score as a domain-level KPI in periodic reports
- [rank-tracker](../rank-tracker/) — Detailed ranking data
- [backlink-analyzer](../backlink-analyzer/) — Link profile data
- [alert-manager](../alert-manager/) — Set up report triggers
- [serp-analysis](../../research/serp-analysis/) — SERP composition data
- [memory-management](../../cross-cutting/memory-management/) — Archive reports in project memory
- [entity-optimizer](../../cross-cutting/entity-optimizer/) — Track branded search and Knowledge Panel metrics
- [technical-seo-checker](../../optimize/technical-seo-checker/) — Technical health data feeds into reports

