---
name: whitespace-finder
description: 'Systematic unmet-needs discovery engine that maps gaps between market demand and existing solutions with quantified opportunity scores. Use when: find opportunities, unmet needs, market gaps, opportunity discovery, what should we build, where is the whitespace.'
---

# Whitespace Finder (DEPTH Model)

Map the gap between what the market demands and what exists. Produces quantified, validated opportunity scores for product and GTM decisions.

## When to Use
- New product ideation
- Feature prioritization against market need
- Adjacent market exploration
- Investment thesis validation
- Pre-PRD opportunity validation

## What You'll Need
**Critical inputs (ask if not provided):**
- Market or product category to analyze
- Target customer segment(s)
- Known competitors (or ask me to research)

**Nice-to-have:**
- Signal Radar output (if previously run)
- JTBD Extractor output (if previously run)
- Customer feedback or support ticket themes

## Process

### Step 1: Demand Evidence Collection
Audit demand across 6 evidence channels:

| Channel | What to Look For | Evidence Quality |
|---------|-----------------|-----------------|
| Community forums (Reddit, HN, Discourse) | Problem-statement posts, workaround discussions | Medium -- shows real pain |
| Review mining (G2, Capterra, TrustRadius) | 1-3 star review complaint patterns, missing feature mentions | High -- verified buyers |
| Search demand | Volume for problem queries vs. solution queries (gap = unmet need) | High -- quantifiable |
| Support tickets | Recurring themes, feature requests, workaround patterns | High -- your own customers |
| Analyst reports | Problem statements, unmet need callouts, market gaps cited | High -- expert validation |
| Adjacent product requests | Features users ask for that cross product boundaries | Medium -- shows expansion opportunities |

For each channel, extract the top 5 unmet needs with supporting evidence.

### Step 2: Gap Matrix Construction
Build a 2D matrix:
- **X-axis**: Customer needs/jobs (from research or JTBD Extractor)
- **Y-axis**: Existing solutions in market (products, workarounds, manual processes)

Rate each cell:
| Rating | Meaning |
|--------|---------|
| 0 | Completely unaddressed -- no solution exists |
| 1 | Poorly addressed -- solutions exist but are inadequate |
| 2 | Adequately addressed -- good-enough solutions exist |
| 3 | Well addressed -- strong solutions, hard to differentiate |

**Whitespace = cells rated 0-1 with strong demand evidence.**

### Step 3: DEPTH Scoring
Score each whitespace opportunity (1-10):

| Dimension | What It Measures | Scoring Guide |
|-----------|-----------------|---------------|
| **D**emand Evidence | Volume and quality of signals indicating real demand | 1=anecdotal, 5=multiple sources, 10=overwhelming evidence |
| **E**xisting Solutions | How well current solutions address it (inverse) | 1=well solved, 5=partial solutions, 10=nothing exists |
| **P**ain Intensity | Severity of unmet need | 1=nice-to-have, 5=significant friction, 10=hair-on-fire problem |
| **T**otal Addressable Need | Size of population with this unmet need | 1=tiny niche, 5=meaningful segment, 10=mass market |
| **H**urdle Analysis | Barriers to entry (inverse -- high = low barriers) | 1=massive barriers, 5=moderate effort, 10=easy to enter |

**Opportunity Score** = (D x 0.25) + (E x 0.20) + (P x 0.25) + (T x 0.15) + (H x 0.15)

**Classification:**
- 7.5+ = **Prime Opportunity** (high confidence, prioritize)
- 5.0-7.4 = **Promising** (validate further before committing)
- Below 5.0 = **Marginal** (park unless strategic fit is strong)

### Step 4: Opportunity Clustering
Group related whitespace opportunities into "opportunity zones" that could be addressed by a single product or feature set. Each zone gets:
- Combined DEPTH score (weighted average of constituent opportunities)
- Shared customer segment
- Common technical requirements
- Estimated effort to address

## Output
Save to `outputs/whitespace-[market]-[YYYY-MM-DD].md`

### Deliverables:
1. **Gap Matrix**: Heat map of needs vs. solutions with whitespace cells highlighted
2. **Opportunity Scorecards**: One per whitespace opportunity with DEPTH scores and evidence citations
3. **Opportunity Zones**: Clustered opportunities showing which can be addressed together
4. **Validation Roadmap**: Prioritized experiments to validate top opportunities (surveys, prototypes, landing page tests)

## Chain Connections
- **Next skill**: Run `market-analyzer` to size the opportunities you discovered
- **Also feeds**: `position-lock` (validated opportunities become positioning targets), `battle-scanner` (whitespace informs differentiation angles)
- **Enhanced by**: Run after `signal-radar` (signals point to where whitespace may exist)
