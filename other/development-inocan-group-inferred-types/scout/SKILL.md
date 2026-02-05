---
name: scout
description: Market validation engine for ID8Labs. Transforms raw ideas into validated (or invalidated) opportunities through systematic research. Returns BUILD/PIVOT/KILL verdicts with evidence.
version: 1.0.0
mcps: [Perplexity, Firecrawl, GitHub]
subagents: [market-intelligence-analyst]
---

# ID8SCOUT - Validation Engine

## Purpose

Transform raw ideas into validated (or invalidated) opportunities through systematic research. Every idea deserves rigorous testing before building.

**Output:** Validation Report with BUILD / PIVOT / KILL verdict

---

## When to Use

- User has a new business/product idea to evaluate
- User asks "should I build X?"
- User wants market research on a concept
- User needs competitive analysis
- User wants to understand if there's demand
- Project is in CAPTURED or VALIDATING state

---

## Commands

### `/scout <idea-description>`

Run full validation on an idea.

**Process:**
1. INTAKE - Clarify the idea
2. MARKET - Size the opportunity
3. COMPETITION - Map the landscape
4. COMMUNITY - Mine real signals
5. CALIBRATE - Adjust for solo builder
6. SYNTHESIZE - Render verdict

### `/scout market <topic>`

Run only market analysis.

### `/scout competitors <product/space>`

Run only competitive analysis.

### `/scout signals <topic>`

Run only community signal mining.

---

## Validation Process

### Phase 1: INTAKE (2-3 minutes)

Clarify the idea before researching.

**Questions to answer:**
1. **What is it?** - One sentence description
2. **Who is it for?** - Specific target user
3. **What problem does it solve?** - Pain point or desire
4. **How is it different?** - Why not use existing solutions?
5. **What's the hypothesis?** - What are we betting on?

**If project exists in tracker:**
- Load from project card
- Use existing one-liner and context

**If new idea:**
- Prompt for clarification
- Suggest creating project: `/tracker new`

---

### Phase 2: MARKET (5-10 minutes)

Size the opportunity and understand trends.

**Use:** `mcp__perplexity__search` and `mcp__perplexity__reason`

**Research areas:**

1. **TAM/SAM/SOM**
   - Total Addressable Market - Everyone who could use this
   - Serviceable Addressable Market - Those you can reach
   - Serviceable Obtainable Market - Realistic capture

2. **Market Trends**
   - Is this market growing or shrinking?
   - What's driving the trend?
   - Where in the adoption curve?

3. **Timing Assessment**
   - Too early? (Market not ready)
   - Too late? (Saturated)
   - Just right? (Growing, not crowded)

**Search queries to run:**
```
- "{topic} market size 2024 2025"
- "{topic} industry trends"
- "{topic} growth rate"
- "{problem} solutions market"
```

**Output:** Market Analysis section of validation report

---

### Phase 3: COMPETITION (5-10 minutes)

Map the competitive landscape and find gaps.

**Use:** `mcp__perplexity__search`, `mcp__firecrawl__firecrawl_search`, `mcp__firecrawl__firecrawl_scrape`

**Research areas:**

1. **Direct Competitors**
   - Who solves the same problem?
   - What do they charge?
   - How do they position?

2. **Indirect Competitors**
   - Alternative solutions to the problem
   - Adjacent products that could expand

3. **Competitor Weaknesses**
   - What do users complain about?
   - What's missing?
   - Where are the gaps?

4. **Competitive Moats**
   - What advantages do incumbents have?
   - Network effects? Data? Brand?

**Search queries to run:**
```
- "{topic} tools alternatives"
- "{competitor} reviews complaints"
- "best {solution type} 2024 2025"
- "{competitor} vs" (autocomplete reveals competitors)
```

**Scraping targets:**
- Competitor landing pages (positioning, pricing)
- Review sites (G2, Capterra, Product Hunt)
- Comparison articles

**Output:** Competitive Landscape section of validation report

---

### Phase 4: COMMUNITY (5-10 minutes)

Mine real signals from where users talk.

**Use:** `mcp__perplexity__search`, `mcp__firecrawl__firecrawl_search`

**Signal sources:**

1. **Reddit**
   - Subreddits where target users hang out
   - Posts asking for solutions
   - Complaints about existing tools

2. **YouTube**
   - Video comments on related content
   - Tutorial views (demand signal)
   - Creator complaints

3. **Twitter/X**
   - Threads about the problem
   - Product complaints
   - Feature requests

4. **Forums/Communities**
   - Indie Hackers
   - Hacker News
   - Niche communities

**What to look for:**
- Pain intensity (how much do they care?)
- Willingness to pay (are they spending already?)
- Frequency (how often do they have this problem?)
- Workarounds (what janky solutions do they use?)

**Search queries to run:**
```
- "site:reddit.com {problem} help"
- "site:reddit.com {existing solution} frustrating"
- "{topic} indie hackers"
- "{problem} twitter thread"
```

**Output:** Community Signals section with real quotes

---

### Phase 5: CALIBRATE (2-3 minutes)

Adjust all estimates for AI-augmented solo builder reality.

**Calibration factors:**

| Traditional Assumption | Calibrated Reality |
|------------------------|-------------------|
| 6-person dev team | 1-2 people + AI tools |
| $100K+ budget | $0-10K bootstrap |
| 6-12 month timeline | 2-8 weeks to MVP |
| Enterprise features first | Core value only |
| VC-scale growth | Sustainable indie growth |

**Recalibrate:**
- Development estimates (AI makes this 5-10x faster)
- Market capture (smaller is fine for solo)
- Competitive moats (speed and focus beat resources)
- Revenue goals ($10K MRR can be life-changing)

**Apply to:**
- Execution plan timeline
- Budget requirements
- Success metrics

---

### Phase 6: SYNTHESIZE (5 minutes)

Combine all research into verdict.

**Verdict options:**

| Verdict | Meaning | Criteria |
|---------|---------|----------|
| **BUILD** | Proceed to architecture | Evidence of demand + achievable by solo builder + acceptable competition |
| **PIVOT** | Refine and revalidate | Core insight valid but approach needs change |
| **KILL** | Don't build this | No demand, or insurmountable competition, or poor fit |

**Confidence levels:**
- **High** - Strong evidence, clear signals
- **Medium** - Mixed signals, some uncertainty
- **Low** - Weak evidence, significant unknowns

**For BUILD verdict, also provide:**
- Recommended MVP scope
- Key risks to watch
- Suggested first milestone

**For PIVOT verdict, also provide:**
- What to change
- New hypothesis to test
- Suggested research focus

**For KILL verdict, also provide:**
- Why it won't work
- What we learned
- Any salvageable ideas

---

## Integration with Tracker

### On Start
```
If project slug provided:
  Load project from tracker
  Use existing context
Else:
  Prompt to create project first
  Or run as standalone research
```

### On Complete
```
1. Generate validation report
2. Save to project artifacts (if project exists)
3. Log to tracker:
   /tracker log {project} "Scout: Validation complete - {VERDICT} verdict ({confidence})"
4. If BUILD: Suggest /tracker update {project} VALIDATED
5. If KILL: Suggest /tracker kill {project}
```

---

## MCP Usage Patterns

### Perplexity (Primary Research)

```
# Quick market search
mcp__perplexity__search({
  query: "{topic} market size trends 2024 2025"
})

# Complex reasoning
mcp__perplexity__reason({
  query: "Analyze the competitive landscape for {product type}. Who are the major players, what are their strengths and weaknesses, and where are the gaps?"
})

# Deep research
mcp__perplexity__deep_research({
  query: "Comprehensive analysis of {market}",
  focus_areas: ["market size", "growth trends", "key players", "emerging opportunities"]
})
```

### Firecrawl (Web Scraping)

```
# Search for competitors
mcp__firecrawl__firecrawl_search({
  query: "{product type} tools alternatives",
  limit: 10
})

# Scrape competitor landing page
mcp__firecrawl__firecrawl_scrape({
  url: "https://competitor.com",
  formats: ["markdown"]
})

# Extract structured data
mcp__firecrawl__firecrawl_extract({
  urls: ["https://competitor.com/pricing"],
  prompt: "Extract pricing tiers, features, and target audience",
  schema: {
    type: "object",
    properties: {
      pricing_tiers: { type: "array" },
      features: { type: "array" },
      target_audience: { type: "string" }
    }
  }
})
```

### GitHub (Competitor Analysis)

```
# Search for open source alternatives
mcp__github__search_repositories({
  query: "{topic} tool"
})

# Check competitor repo activity
mcp__github__list_commits({
  owner: "competitor",
  repo: "their-product"
})
```

---

## Subagent Integration

### market-intelligence-analyst

Delegate complex research tasks:

```
Task({
  subagent_type: "market-intelligence-analyst",
  prompt: "Research the {topic} market. Focus on:
    1. Market size and growth rate
    2. Key trends driving the market
    3. Major players and their positioning
    4. Emerging opportunities and gaps

    Provide specific data points with sources."
})
```

---

## Output Format

Generate validation report using `templates/validation-report.md`

Key sections:
1. Executive Summary (verdict + confidence + one paragraph)
2. Market Analysis (TAM/SAM/SOM, trends, timing)
3. Competitive Landscape (players, gaps, moats)
4. Community Signals (real quotes, pain intensity)
5. Founder Fit Assessment (skills, resources, motivation)
6. Execution Plan (calibrated for solo builder)
7. Risks & Mitigations
8. Verdict & Reasoning
9. Sources

---

## Error Handling

| Issue | Response |
|-------|----------|
| MCP unavailable | Fall back to web search, note limitation |
| Insufficient data | Lower confidence, note gaps |
| Conflicting signals | Present both sides, explain uncertainty |
| No competitors found | Flag as potential blue ocean OR hidden problem |
| Overwhelming competition | Analyze for niche opportunities |

---

## Changelog

### v1.0.0 (2025-12-21)
- Initial release
- Full validation pipeline
- Perplexity + Firecrawl integration
- Calibration layer for solo builders
- Tracker integration
