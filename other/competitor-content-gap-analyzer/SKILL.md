---
name: competitor-content-gap-analyzer
description: Analyze competitor websites to identify content gaps your site doesn't cover. Crawls competitor blog URLs, extracts article titles/topics/H2s, maps coverage across topic clusters, and produces a prioritized content calendar with "they have it, we don't" gap scoring. Use when user wants to find content gaps against competitors, build a topic-driven content calendar, discover untapped keyword opportunities, or plan an article cluster strategy based on competitive intelligence.
---

# Competitor Content Gap Analyzer

Crawl competitor blog sections and identify content opportunities your site is missing. Output a gap-scored topic list ready for content calendar planning.

## Prerequisites

Collect from the user:
- **Your website domain** and current blog URL structure
- **3-5 competitor URLs** (homepage or blog index)
- **Industry/niche** for topic classification
- **Existing article list** (optional — helps avoid suggesting topics you already cover)

## Workflow

### Step 1: Crawl Competitor Blog Index

For each competitor, visit their blog/sitemap and extract:
- All article titles
- Article URLs
- Publish dates (if available)
- H2 headings from each article (for topic depth analysis)

### Step 2: Map to Topic Clusters

Classify every competitor article into one of these 8 B2B cluster types:

| # | Cluster | Match Keywords |
|---|---|---|
| 1 | Educational | what is, explained, types, uses, 101, basics, understanding |
| 2 | Buying Guide | how to choose, selection guide, buying guide, best X for |
| 3 | Comparison | vs, versus, compare, alternative, pros and cons, difference |
| 4 | Specifications | specifications, dimensions, standards, tolerance, technical |
| 5 | Application Scenarios | best for, for hotels, for retailers, for hospitals, use case |
| 6 | Process/Quality | manufacturing, quality control, how it's made, troubleshooting |
| 7 | Certification/Compliance | certification, ISO, CE, REACH, ASTM, compliance, testing |
| 8 | Procurement/Supplier | OEM, ODM, MOQ, lead time, factory audit, how to evaluate, supplier |

### Step 3: Identify Content Gaps

For each competitor article, check if your site covers the same topic:

- **Direct Gap**: A competitor article with no equivalent on your site → score 100
- **Partial Coverage**: Your site touches the topic but not at the same depth → score 50
- **Covered**: Your site has a comparable article → score 0

### Step 4: Score and Prioritize

Score each gap on:

| Factor | Weight | Scale |
|---|---|---|
| Topic Relevance | 30% | 1-10 (How relevant to your product/audience?) |
| Competitor Coverage | 25% | 1-10 (How many competitors cover it?) |
| Search Intent Match | 25% | 1-10 (Commercial/transactional intent = higher) |
| Timeliness | 20% | 1-10 (Recently published = more relevant) |

**Priority Score** = (Relevance × 0.30) + (Coverage × 0.25) + (Intent × 0.25) + (Timeliness × 0.20)

### Step 5: Generate Content Calendar

Output a prioritized content plan:

| # | Article Title (Suggested) | Cluster | Priority Score | Competitors Covering | Your Coverage | Action |
|---|---|---|---|---|---|---|
| 1 | [Title] | [Type] | 85 | 3/5 | None | Write new |
| 2 | [Title] | [Type] | 72 | 2/5 | Thin | Expand existing |

### Step 6: Competitor Coverage Map

Visual overview (text-based):

```
Topic Cluster         Competitor A   Competitor B   Competitor C   YOU
─────────────────────────────────────────────────────────────────────
Educational           ████████       ████           ██████         ████
Buying Guide          ████           ██████████     ████           ██
Comparison            ██████         ████           ██████████     ░░░░  ← GAP
Specifications        ██████████     ██████         ████           ░░░░  ← GAP
Application Scenarios ████           ██████         ██████████     ██████
Process/Quality       ░░░░           ████           ██████         ░░░░  ← GAP
Certification         ██             ██████         ████           ██████
Procurement           ██████         ████           ██             ██
```

## Output Deliverables

1. **Gap Scorecard** — table of all competitor articles with gap/partial/covered status
2. **Priority Ranking** — top 20 topics ranked by Priority Score
3. **Content Calendar** — 12-week publishing plan with cluster coverage balance
4. **Coverage Map** — ASCII chart showing topic coverage density per competitor per cluster
5. **Recommendations** — quick-win topics (high score, easy to write) vs strategic plays (high score, requires research)