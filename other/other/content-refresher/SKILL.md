---
name: content-refresher
description: Identifies and updates outdated content to restore and improve search rankings. Analyzes content freshness, adds new information, updates statistics, and optimizes for current SEO and GEO best practices.
geo-relevance: "medium"
---

# Content Refresher

This skill helps identify and revitalize outdated content to reclaim lost rankings and traffic. It analyzes content freshness, identifies update opportunities, and guides the refresh process for maximum SEO and GEO impact.

## When to Use This Skill

- Content has lost rankings or traffic over time
- Statistics and information are outdated
- Competitors have published better content
- Content needs updating for a new year
- Industry changes require content updates
- Adding new sections to existing content
- Converting old content for GEO optimization

## What This Skill Does

1. **Freshness Analysis**: Identifies outdated content needing updates
2. **Performance Tracking**: Finds content with declining traffic
3. **Gap Identification**: Spots missing information competitors have
4. **Update Prioritization**: Ranks content by refresh potential
5. **Refresh Recommendations**: Provides specific update guidance
6. **GEO Enhancement**: Updates content for AI citation potential
7. **Republishing Strategy**: Advises on date and promotion tactics

## How to Use

### Identify Content to Refresh

```
Find content on [domain] that needs refreshing
```

```
Which of my blog posts have lost the most traffic?
```

### Refresh Specific Content

```
Refresh this article for [current year]: [URL/content]
```

```
Update this content to outrank [competitor URL]: [your URL]
```

### Content Refresh Strategy

```
Create a content refresh strategy for [domain/topic]
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~analytics + ~~search console + ~~SEO tool connected:**
Claude can automatically pull historical traffic trends from ~~analytics, fetch impression and ranking data from ~~search console, retrieve keyword position history from ~~SEO tool, and identify content with declining performance. This enables data-driven refresh prioritization.

**With manual data only:**
Ask the user to provide:
1. Traffic data or screenshots showing performance trends
2. Ranking screenshots or history for key pages
3. Content publish dates and last update dates
4. List of pages the user suspects need refreshing

Proceed with the analysis using provided data. Note in the output which findings are from automated data vs. manual review.

## Instructions

When a user requests content refresh help:

1. **CORE-EEAT Quick Score — Identify Weak Dimensions**

   Before refreshing, run a quick CORE-EEAT assessment to focus effort on the weakest areas. Reference: [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md)

   ```markdown
   ### CORE-EEAT Quick Assessment

   **Content**: [title or URL]
   **Content Type**: [type]

   Rapidly score each dimension (estimate 0-100):

   | Dimension | Quick Score | Key Weakness | Refresh Priority |
   |-----------|-----------|--------------|-----------------|
   | C — Contextual Clarity | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | O — Organization | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | R — Referenceability | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | E — Exclusivity | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | Exp — Experience | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | Ept — Expertise | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | A — Authority | [X]/100 | [main issue] | 🔴/🟡/🟢 |
   | T — Trust | [X]/100 | [main issue] | 🔴/🟡/🟢 |

   **Weakest Dimensions** (focus refresh here):
   1. [Dimension] — [what needs fixing]
   2. [Dimension] — [what needs fixing]

   **Refresh Strategy**: Focus on 🔴 dimensions first, then 🟡.

   _For full 80-item audit, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/)_
   ```

2. **Identify Content Refresh Candidates**

   ```markdown
   ## Content Refresh Analysis
   
   ### Refresh Candidate Identification
   
   **Criteria for Content Refresh**:
   - Published more than 6 months ago
   - Contains dated information (years, statistics)
   - Declining traffic trend
   - Lost keyword rankings
   - Outdated references or broken links
   - Missing topics competitors now cover
   - No GEO optimization
   
   ### Content Audit Results
   
   | Content | Published | Last Updated | Traffic Trend | Priority |
   |---------|-----------|--------------|---------------|----------|
   | [Title 1] | [date] | [date] | ↓ -45% | 🔴 High |
   | [Title 2] | [date] | Never | ↓ -30% | 🔴 High |
   | [Title 3] | [date] | [date] | ↓ -20% | 🟡 Medium |
   | [Title 4] | [date] | [date] | → 0% | 🟡 Medium |
   
   ### Refresh Prioritization Matrix
   
   ```
   High Traffic + High Decline = 🔴 Refresh Immediately
   High Traffic + Low Decline = 🟡 Schedule Refresh
   Low Traffic + High Decline = 🟡 Evaluate & Decide
   Low Traffic + Low Decline = 🟢 Low Priority
   ```
   ```

3. **Analyze Individual Content for Refresh**

   ```markdown
   ## Content Refresh Analysis: [Title]
   
   **URL**: [URL]
   **Published**: [date]
   **Last Updated**: [date]
   **Word Count**: [X]
   
   ### Performance Metrics
   
   | Metric | 6 Mo Ago | Current | Change |
   |--------|----------|---------|--------|
   | Organic Traffic | [X]/mo | [X]/mo | [+/-X]% |
   | Avg Position | [X] | [X] | [+/-X] |
   | Impressions | [X] | [X] | [+/-X]% |
   | CTR | [X]% | [X]% | [+/-X]% |
   
   ### Keywords Analysis
   
   | Keyword | Old Position | Current Position | Change |
   |---------|--------------|------------------|--------|
   | [kw 1] | [X] | [X] | ↓ [X] |
   | [kw 2] | [X] | [X] | ↓ [X] |
   | [kw 3] | [X] | [X] | ↓ [X] |
   
   ### Why This Content Needs Refresh
   
   1. **Outdated information**: [specific examples]
   2. **Competitive gap**: [what competitors added]
   3. **Missing topics**: [new subtopics to cover]
   4. **SEO issues**: [current optimization problems]
   5. **GEO potential**: [AI citation opportunities]
   ```

4. **Identify Specific Updates Needed**

   ```markdown
   ## Refresh Requirements
   
   ### Outdated Elements
   
   | Element | Current | Update Needed |
   |---------|---------|---------------|
   | Year references | "[old year]" | Update to [current year] |
   | Statistics | "[old stat]" | Find current data |
   | Tool mentions | "[old tool]" | Add newer tools |
   | Links | [X] broken | Fix or replace |
   | Screenshots | Outdated UI | Recapture |
   
   ### Missing Information
   
   **Topics competitors now cover that you don't**:
   
   | Topic | Competitor Coverage | Words Needed | Priority |
   |-------|---------------------|--------------|----------|
   | [Topic 1] | 3/5 competitors | ~300 words | High |
   | [Topic 2] | 2/5 competitors | ~200 words | Medium |
   | [Topic 3] | 4/5 competitors | ~400 words | High |
   
   ### SEO Updates Needed
   
   - [ ] Update title tag with current year
   - [ ] Refresh meta description
   - [ ] Add new H2 sections for [topics]
   - [ ] Update internal links to newer content
   - [ ] Add FAQ section for featured snippets
   - [ ] Refresh images and add new alt text
   
   ### GEO Updates Needed
   
   - [ ] Add clear definition at start
   - [ ] Include quotable statistics with sources
   - [ ] Add Q&A formatted sections
   - [ ] Update sources with current citations
   - [ ] Create standalone factual statements
   ```

5. **Create Refresh Plan**

   ```markdown
   ## Content Refresh Plan
   
   ### Title/URL
   **Current**: [current title]
   **Refreshed**: [updated title with year/hook]
   
   ### Structural Changes
   
   **Keep As-Is**:
   - [Section 1] - Still relevant and accurate
   - [Section 2] - Still relevant and accurate
   
   **Update/Expand**:
   - [Section 3] - Update statistics, add [X] words
   - [Section 4] - Add new examples from [current year]
   
   **Add New Sections**:
   - [New Section 1] - [description, ~X words]
   - [New Section 2] - [description, ~X words]
   - FAQ Section - [X questions for featured snippets]
   
   **Remove/Consolidate**:
   - [Section 5] - Outdated, remove or redirect topic
   
   ### Content Additions
   
   **New Word Count Target**: [X] words (+[Y] from current)
   
   | Section | Current | After Refresh | Notes |
   |---------|---------|---------------|-------|
   | Introduction | [X] | [X] | Add hook, update context |
   | [Section 1] | [X] | [X] | Keep |
   | [Section 2] | [X] | [X] | Update stats |
   | [New Section] | 0 | [X] | Add entirely |
   | FAQ | 0 | [X] | Add for GEO |
   | Conclusion | [X] | [X] | Update CTA |
   
   ### Specific Updates
   
   **Statistics to Update**:
   
   | Old Statistic | New Statistic | Source |
   |---------------|---------------|--------|
   | "[old stat]" | "[find current]" | [source] |
   | "[old stat]" | "[find current]" | [source] |
   
   **Links to Update**:
   
   | Anchor Text | Old URL | New URL | Reason |
   |-------------|---------|---------|--------|
   | "[anchor]" | [old] | [new] | Broken |
   | "[anchor]" | [old] | [new] | Better resource |
   
   **Images to Update**:
   
   | Image | Action | New Alt Text |
   |-------|--------|--------------|
   | [img 1] | Replace | "[keyword-rich alt]" |
   | [img 2] | Keep | Update alt text |
   ```

6. **Write Refresh Content**

   ```markdown
   ## Refreshed Content Sections
   
   ### Updated Introduction
   
   [Write new introduction with:]
   - Updated hook for current year
   - Fresh statistics
   - Clear value proposition
   - Primary keyword in first 100 words
   
   ### New Section: [Title]
   
   [Write new section covering:]
   - [Topic competitors now cover]
   - Current information and examples
   - GEO-optimized with quotable statements
   
   ### Updated Statistics Section
   
   **Replace**:
   > "[Old statement with outdated stat]"
   
   **With**:
   > "[New statement with current stat] (Source, [current year])"
   
   ### New FAQ Section
   
   ## Frequently Asked Questions
   
   ### [Question matching PAA/common query]?
   
   [Direct answer in 40-60 words, optimized for featured snippets]
   
   ### [Question 2]?
   
   [Direct answer]
   
   ### [Question 3]?
   
   [Direct answer]
   ```

7. **Optimize for GEO During Refresh**

   ```markdown
   ## GEO Enhancement Opportunities
   
   ### Add Clear Definitions
   
   **Add at start of article**:
   > **[Topic]** is [clear, quotable definition in 40-60 words that 
   > AI systems can cite directly].
   
   ### Add Quotable Statements
   
   **Transform**:
   > "Email marketing is effective for businesses."
   
   **Into**:
   > "Email marketing delivers an average ROI of $42 for every $1 
   > invested, making it the highest-ROI digital marketing channel 
   > according to the Data & Marketing Association ([current year])."
   
   ### Add Q&A Sections
   
   Structure content with questions AI might answer:
   - What is [topic]?
   - How does [topic] work?
   - Why is [topic] important?
   - What are the benefits of [topic]?
   
   ### Update Citations
   
   - Add sources for all statistics
   - Link to authoritative references
   - Include publication dates
   - Use recent sources (last 2 years)
   ```

8. **Generate Republishing Strategy**

   ```markdown
   ## Republishing Strategy
   
   ### Date Strategy
   
   **Options**:
   
   1. **Update Published Date** 
      - Use when: Major overhaul (50%+ new content)
      - Pros: Signals freshness to Google
      - Cons: Loses "original" authority
   
   2. **Add "Last Updated" Date**
      - Use when: Moderate updates (20-50% new)
      - Pros: Shows both original and fresh
      - Cons: Original date visible
   
   3. **Keep Original Date**
      - Use when: Minor updates (<20% new)
      - Pros: Maintains authority
      - Cons: Doesn't signal update
   
   **Recommendation**: [Option X] because [reason]
   
   ### Technical Implementation
   
   - [ ] Update `dateModified` in schema
   - [ ] Update sitemap lastmod
   - [ ] Clear cache after publishing
   - [ ] Resubmit to ~~search console
   
   ### Promotion Strategy
   
   **Immediately after refresh**:
   - [ ] Share on social media as "updated for [current year]"
   - [ ] Send to email list if significant update
   - [ ] Update internal links with fresh anchors
   - [ ] Reach out for new backlinks
   
   **Track Results**:
   - [ ] Monitor rankings for 4-6 weeks
   - [ ] Track traffic changes
   - [ ] Watch for featured snippet capture
   - [ ] Check AI citation improvements
   ```

9. **Create Refresh Report**

   ```markdown
   # Content Refresh Report
   
   ## Summary
   
   **Content**: [Title]
   **Refresh Date**: [Date]
   **Refresh Level**: [Major/Moderate/Minor]
   
   ## Changes Made
   
   | Element | Before | After |
   |---------|--------|-------|
   | Word count | [X] | [Y] (+[Z]%) |
   | Sections | [X] | [Y] |
   | Statistics | [X] outdated | [Y] current |
   | Internal links | [X] | [Y] |
   | Images | [X] | [Y] |
   | FAQ questions | 0 | [X] |
   
   ## Updates Completed
   
   - [x] Updated title with current year
   - [x] Refreshed meta description
   - [x] Added [X] new sections
   - [x] Updated [X] statistics with sources
   - [x] Fixed [X] broken links
   - [x] Added FAQ section for GEO
   - [x] Implemented FAQ schema
   - [x] Updated images and alt text
   
   ## Expected Outcomes
   
   | Metric | Current | 30-Day Target | 90-Day Target |
   |--------|---------|---------------|---------------|
   | Avg Position | [X] | [Y] | [Z] |
   | Organic Traffic | [X]/mo | [Y]/mo | [Z]/mo |
   | Featured Snippets | 0 | 1+ | 2+ |
   
   ## Next Review

   Schedule next refresh review: [Date - 6 months from now]
   ```

## Validation Checkpoints

### Input Validation
- [ ] Target content URL or title clearly identified
- [ ] Historical performance data available (traffic trends, rankings)
- [ ] Content publish/update dates known
- [ ] If comparing to competitors, competitor URLs provided

### Output Validation
- [ ] Every recommendation cites specific data points (not generic advice)
- [ ] Outdated elements identified with specific examples and replacement data
- [ ] All suggested additions include word counts and section locations
- [ ] Source of each data point clearly stated (~~analytics data, ~~search console, ~~SEO tool, user-provided, or estimated)

## Example

**User**: "Refresh my blog post about 'best cloud hosting providers'"

**Output**:

```markdown
### CORE-EEAT Quick Assessment

**Content**: "Best Cloud Hosting Providers 2023"
**Content Type**: Commercial comparison / listicle

| Dimension | Quick Score | Key Weakness | Refresh Priority |
|-----------|-----------|--------------|-----------------|
| C — Contextual Clarity | 60/100 | Title says 2023 — stale intent signal | 🔴 |
| O — Organization | 75/100 | Good comparison tables but no summary box | 🟡 |
| R — Referenceability | 35/100 | Pricing from Q1 2023, 3 broken links | 🔴 |
| E — Exclusivity | 50/100 | No original benchmarks or test data | 🟡 |
| Exp — Experience | 30/100 | No first-person testing narrative | 🔴 |
| Ept — Expertise | 65/100 | Author bio present but lacks credentials | 🟡 |
| A — Authority | 55/100 | 12 backlinks, was ranking page 1 | 🟢 |
| T — Trust | 60/100 | Affiliate links present but not disclosed | 🔴 |

**Weakest Dimensions** (focus refresh here):
1. **Experience** — Add hands-on testing results ("We migrated a test site to each provider")
2. **Referenceability** — Replace all 2023 pricing/uptime data with current figures

## Content Refresh Analysis: Best Cloud Hosting Providers 2023

**URL**: cloudhosting.com/best-cloud-hosting
**Published**: 2023-02-14
**Last Updated**: Never
**Word Count**: 2,100

### Performance Metrics

| Metric | 6 Mo Ago | Current | Change |
|--------|----------|---------|--------|
| Organic Traffic | 3,200/mo | 1,400/mo | -56% |
| Avg Position | 4.2 | 14.8 | ↓ 10.6 |
| Impressions | 18,000 | 9,500 | -47% |
| CTR | 6.1% | 2.3% | -3.8% |

### Content Decay Signals Identified

1. **Outdated year in title and H1** — "2023" signals stale content to users and search engines
2. **Pricing data 18+ months old** — AWS Lightsail listed at $3.50/mo (now $5/mo), DigitalOcean at $4/mo (now $6/mo)
3. **Missing new entrants** — No mention of Hetzner Cloud or Vultr, which 4/5 top competitors now cover
4. **3 broken outbound links** — Provider comparison pages that have moved or been retired

### Refresh vs. Rewrite Decision

| Factor | Assessment |
|--------|-----------|
| Content quality | Good structure, solid comparison tables — foundation is sound |
| URL equity | 12 referring domains, 18 months old |
| Scope of changes | ~40% of content needs updating |
| Search intent | Unchanged — still commercial comparison |

**Decision**: **REFRESH** — The URL has earned backlinks, the structure is solid, and less than 50% needs rewriting. Keep the URL, update in place.

## Content Refresh Plan

**Current Title**: "Best Cloud Hosting Providers 2023"
**Refreshed Title**: "Best Cloud Hosting Providers 2024: 7 Platforms Tested & Compared"

### Specific Refresh Actions

1. **Update all pricing and specs** (~30 min)
   - Replace 2023 pricing for all 5 listed providers with current data
   - Add uptime stats from the last 12 months (source: UptimeRobot public status pages)
   - Update feature comparison table with current plan tiers

2. **Add 2 missing providers + testing narrative** (~600 words)
   - Add Hetzner Cloud and Vultr sections with same comparison format
   - Write intro paragraph: "We deployed a WordPress benchmark site to each provider and measured TTFB, uptime, and support response times over 30 days"

3. **Add affiliate disclosure and FAQ section** (~200 words)
   - Add disclosure statement below introduction: "This post contains affiliate links. See our editorial policy."
   - Add FAQ with 4 questions targeting People Also Ask (e.g., "What is the cheapest cloud hosting?", "Is cloud hosting faster than shared hosting?")
   - Implement FAQ schema markup for rich result eligibility

4. **Fix broken links and update internal links** (~15 min)
   - Replace 3 broken outbound links with current provider URLs
   - Add internal links to cloudhosting.com/vps-vs-cloud and cloudhosting.com/hosting-speed-test

### Republishing Strategy

**Recommendation**: Update Published Date — this is a major overhaul (40%+ new content, new providers, fresh test data). Update `dateModified` in Article schema, resubmit URL in Search Console, and share on social as "Updated for 2024."

### Expected Outcomes

| Metric | Current | 30-Day Target | 90-Day Target |
|--------|---------|---------------|---------------|
| Avg Position | 14.8 | 8-10 | 3-6 |
| Organic Traffic | 1,400/mo | 2,200/mo | 3,500/mo |
| Featured Snippets | 0 | 1 (FAQ) | 2+ |
```

## Content Refresh Checklist

```markdown
### Pre-Refresh
- [ ] Analyze current performance metrics
- [ ] Identify outdated information
- [ ] Research competitor updates
- [ ] Note missing topics

### Content Updates
- [ ] Update year references
- [ ] Refresh statistics with sources
- [ ] Add new examples and case studies
- [ ] Expand thin sections
- [ ] Add new relevant sections
- [ ] Create FAQ section

### SEO Updates
- [ ] Update title tag
- [ ] Refresh meta description
- [ ] Optimize headers
- [ ] Update internal links
- [ ] Add new images with alt text

### GEO Updates
- [ ] Add clear definition
- [ ] Include quotable statements
- [ ] Add Q&A formatted content
- [ ] Update source citations

### Technical
- [ ] Update schema dateModified
- [ ] Clear page cache
- [ ] Update sitemap
- [ ] Test page speed
```

## Tips for Success

1. **Prioritize by ROI** - Refresh high-potential content first
2. **Don't just add dates** - Make substantial improvements
3. **Beat competitors** - Add what they have and more
4. **Track results** - Monitor ranking changes post-refresh
5. **Schedule regular audits** - Check content health quarterly
6. **Optimize for GEO** - Every refresh is a GEO opportunity

## Content Decay Signal Taxonomy

### Decay Indicators

| Signal | Source | Severity | Detection Method |
|--------|--------|----------|-----------------|
| Traffic decline >20% MoM | Analytics | High | Monthly traffic comparison |
| Position drop >5 positions | Rank tracker | High | Weekly rank monitoring |
| Outdated statistics/dates | Manual review | Medium | Annual content audit |
| Broken external links | Crawler | Medium | Monthly crawl reports |
| Decreased CTR | Search Console | Medium | Quarterly CTR analysis |
| Competitor new content | SERP monitoring | Medium | Monthly SERP checks |
| User engagement drop | Analytics | Low | Quarterly engagement review |
| Index coverage issues | Search Console | High | Weekly coverage monitoring |

### Content Decay Stages

| Stage | Symptoms | Urgency | Recommended Action |
|-------|---------|---------|-------------------|
| **Early decay** | Slight traffic/position dip | Low | Monitor for 2-4 weeks |
| **Active decay** | Consistent decline across 2+ months | Medium | Schedule refresh within 2 weeks |
| **Significant decay** | 50%+ traffic loss, page 2+ | High | Immediate refresh or rewrite |
| **Terminal decay** | No organic traffic, deindexed | Critical | Rewrite, redirect, or retire |

## Refresh vs. Rewrite Decision Framework

| Factor | Refresh (Update) | Rewrite (New version) |
|--------|-----------------|---------------------|
| Content quality | Good foundation, needs updating | Fundamentally flawed or outdated approach |
| Position | Was ranking well, now dropping | Never ranked well despite optimization |
| URL age | 1+ years, has earned backlinks | Young URL with no backlink equity |
| Backlinks | Has external links pointing to it | No backlinks worth preserving |
| Scope of changes needed | <50% of content changing | >50% needs rewriting |
| Search intent | Intent hasn't changed | Search intent has evolved |

**Decision rule:** If the URL has backlinks and was ranking, REFRESH. If not, consider REWRITE at a new URL (with 301 redirect if old URL has any equity).

## Content Lifecycle Model

```
CREATE → PROMOTE → MAINTAIN → REFRESH → [REFRESH again] or RETIRE
  │         │          │          │                          │
  │      Month 1    Month 2-6   Month 6-12              When terminal
  │    Social,      Monitor     Update facts,            301 redirect
  │    outreach,    rankings,   add new sections,         to related
  │    email        fix issues  improve depth              content
```

### Lifecycle Actions by Phase

| Phase | Duration | Key Actions | Metrics to Track |
|-------|----------|------------|-----------------|
| Create | Week 1 | Publish, submit to Search Console | Indexation |
| Promote | Month 1 | Social shares, email, outreach | Referral traffic, backlinks |
| Maintain | Months 2-6 | Monitor, fix broken links, respond to comments | Rankings, traffic trend |
| Refresh | Months 6-12+ | Update data, add sections, improve structure | Traffic recovery, new keywords |
| Retire | When terminal | 301 redirect to best alternative | Redirect traffic recovery |

## Update Strategy by Content Type

| Content Type | Refresh Frequency | Key Updates | Shelf Life |
|-------------|-------------------|------------|-----------|
| Statistics roundups | Every 6 months | Replace old stats, add new sources | 6-12 months |
| Tool comparisons | Every 3-6 months | Update pricing, features, screenshots | 3-6 months |
| How-to guides | Annually | Update steps, screenshots, links | 12-18 months |
| Evergreen guides | Every 12-18 months | Add new sections, update examples | 18-24 months |
| News/trend content | Don't refresh | Archive or redirect | 1-3 months |
| Case studies | Rarely | Update results if available | 2-3 years |
| Glossary/definitions | As needed | Update when definitions evolve | 2-5 years |

## Reference Materials

- [Content Decay Signals](./references/content-decay-signals.md) — Decay indicators, lifecycle stages, and refresh triggers by content type

## Related Skills

- [content-gap-analysis](../../research/content-gap-analysis/) — Find what to add
- [seo-content-writer](../../build/seo-content-writer/) — Write new sections
- [geo-content-optimizer](../../build/geo-content-optimizer/) — Enhance for AI
- [on-page-seo-auditor](../on-page-seo-auditor/) — Audit refreshed content
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — Full 80-item CORE-EEAT audit

