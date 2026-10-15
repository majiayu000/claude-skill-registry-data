---
name: "ad-research"
description: "Autonomous competitor ad intelligence. Scrapes competitor ads from Meta Ad Library and other platforms, transcribes video ads, extracts hooks/angles/structure, and produces a full competitive intel dump. Use when researching competitor ads, analyzing ad creative strategies, building competitive ad intelligence, or preparing for ad script generation. Mirrors Eddie's Stage 1 (Competitor Intelligence)."
risk: low
tags: [growth, marketing, competitive-intel, research]
created: 2026-03-23
updated: 2026-03-23
---

# Ad Research — Competitor Intelligence Engine

Automated competitor ad discovery, analysis, and pattern extraction. This is UAOP Stage 1 (Intelligence) for the Growth department.

## When to use

- Researching competitor ad strategies before creating new campaigns
- Discovering what angles/hooks/scripts are working in a niche
- Building a competitive ad intelligence library
- Preparing input for the `ad-script-generator` skill
- Weekly competitive monitoring (what's new, what stopped, what's scaling)

## When NOT to use

- Writing ad scripts (use `ad-script-generator`)
- Analyzing your own ad performance (use `ad-performance-loop`)
- General market research without an ad focus (use `competitive-intel` or `research-methodology`)

## Pipeline

### Step 1: Define Research Scope

Gather from user or context:
```
RESEARCH SCOPE:
  niche: <industry/product category>
  competitors: [<competitor 1>, <competitor 2>, ...]
  platforms: [meta, tiktok, google]  # which ad libraries to search
  keywords: [<keyword 1>, <keyword 2>, ...]  # search terms
  date_range: last_90_days  # how far back
  max_ads_per_competitor: 50
```

### Step 2: Discover Competitor Ads

**Using brave-search + tavily MCP:**
1. Search for `"[competitor name]" site:facebook.com/ads/library` for each competitor
2. Search for `"[competitor name]" ad creative` to find coverage and breakdowns
3. Search for `"[niche keyword]" best performing ads 2026` for angle discovery
4. Search for competitor landing pages to understand positioning

**Using playwright MCP (if available):**
1. Navigate to Meta Ad Library (facebook.com/ads/library)
2. Search by advertiser name or keyword
3. Filter by active ads, sort by longest running (oldest = most profitable)
4. Capture ad creative details: copy, headline, CTA, media type

**Key principle:** Sort by longevity. Ads running for 60+ days are likely profitable. Ads running for 7 days are still being tested.

### Step 3: Analyze Each Ad

For each discovered ad, extract:

```markdown
## Ad Analysis: [Competitor] — Ad #[N]

**Duration Running:** [X days/weeks/months]
**Platform:** [Meta/TikTok/Google]
**Format:** [Video/Image/Carousel]
**Estimated Profitability:** [High/Medium/Low] (based on run duration)

### Hook (First 3 seconds)
- Type: [Question/Statement/Pattern-interrupt/Story/Statistic]
- Text: "[exact hook text]"
- Why it works: [analysis]

### Angle
- Primary angle: [Pain point/Aspiration/Social proof/Authority/Urgency]
- Target emotion: [Fear/Desire/Frustration/Curiosity/FOMO]
- ICP signal: [who this ad targets based on language/imagery]

### Structure
1. Hook: [what grabs attention]
2. Problem: [what pain point is highlighted]
3. Solution: [how the product is positioned]
4. Proof: [testimonials/stats/demonstrations]
5. CTA: [what action is requested]

### Body Copy
- Headline: "[exact headline]"
- Primary text: "[exact body copy]"
- CTA button: "[exact CTA text]"

### Transcript (if video)
"[word-for-word transcript]"

### Key Takeaways
- What makes this ad work: [specific reasons]
- Angle reusability: [High/Medium/Low]
- Adaptation notes: [how to adapt for our product]
```

### Step 4: Pattern Synthesis

After analyzing all ads, produce:

```markdown
# Competitive Ad Intelligence Report

## Research Summary
- Competitors analyzed: [N]
- Total ads reviewed: [N]
- Date range: [start] to [end]
- Platforms: [list]

## Winning Patterns (sorted by frequency across competitors)

### Top Hooks
| Rank | Hook Type | Example | Competitors Using | Avg Duration |
|------|-----------|---------|-------------------|-------------|
| 1 | [type] | "[example]" | [N] | [X days] |

### Top Angles
| Rank | Angle | Description | Success Signals |
|------|-------|-------------|----------------|
| 1 | [angle] | [what it is] | [why we think it works] |

### Top Ad Structures
| Rank | Structure | Description | Best For |
|------|-----------|-------------|----------|
| 1 | [structure] | [steps] | [which ICPs] |

## Competitor Breakdown
[per-competitor summary: what they're running, their main angles, estimated spend level]

## Recommended Angles for Our Product
| Priority | Angle | Based On | Adaptation Notes |
|----------|-------|----------|-----------------|
| 1 | [angle] | [which competitor ads] | [how to adapt] |

## Anti-Patterns (What to Avoid)
- [pattern that multiple competitors tried and abandoned]
```

## Output Format

The skill produces a **Competitive Ad Intel Dump** — a structured document that feeds directly into `ad-script-generator` as input.

## Tools Used

| Tool | Purpose |
|------|---------|
| brave-search MCP | Privacy-focused web search for ad discovery |
| tavily MCP | AI-optimized search for deeper research |
| playwright MCP | Browser automation for ad library scraping |
| memory MCP | Store winning patterns in knowledge graph |
| sequential MCP | Multi-step reasoning for angle analysis |

## Agents

| Agent | Role |
|-------|------|
| growth-marketer (L2) | Owns the research process, sets scope |
| deep-research (L2) | Executes search queries, synthesizes findings |
| content-strategist (L3) | Analyzes copy patterns, voice, positioning |
| trend-researcher (L4) | Tracks competitive movements over time |
| analytics-reporter (L3) | Quantifies patterns, ranks by frequency |

## UAOP Integration

- **Stage 1 output** feeds into **Stage 3** (`ad-script-generator`)
- **Stage 5** (`ad-performance-loop`) feeds winners back into Stage 1 scope
- Research results stored in **memory MCP** for longitudinal tracking
- Weekly cadence: run every Monday to catch new competitor launches

## Scheduling

```
Cadence: Weekly (Monday)
Trigger: Manual or scheduled via GAOS pipeline
Input: Competitor list + keywords from growth/domain.md
Output: Competitive Ad Intel Dump → stored in memory + fed to ad-script-generator
```
