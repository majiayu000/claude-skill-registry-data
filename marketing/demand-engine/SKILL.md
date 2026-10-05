---
name: demand-engine
description: 'Multi-channel demand generation strategy builder that designs the full pipeline from awareness to hand-raise with channel scoring and budget allocation. Use when: demand generation, demand gen strategy, lead generation, pipeline strategy, marketing channels, how do we generate demand, channel strategy.'
---

# Demand Engine (WAVE Model)

Design the strategic demand gen machine: which channels, what content at each stage, how they interconnect, and how budget is allocated for maximum pipeline impact.

## When to Use
- Pre-launch demand gen planning
- Annual marketing strategy
- Channel mix optimization
- New segment demand gen design
- Marketing budget planning

## What You'll Need
**Critical inputs (ask if not provided):**
- Product and target audience
- Available budget range
- Sales motion (PLG, sales-led, hybrid)

**Nice-to-have:**
- Position Lock output (messaging to fuel campaigns)
- Journey Architect output (gates define content staging)
- Current channel performance data

## Process

### Step 1: Channel Inventory and WAVE Scoring
Evaluate 15+ demand channels:

Score each channel on 4 dimensions (1-10):

| Dimension | What It Measures | Scoring Guide |
|-----------|-----------------|---------------|
| **W**eight | Volume of qualified demand possible | 1=tiny reach, 5=meaningful, 10=massive scale |
| **A**udience-fit | How well does this channel reach your ICP? | 1=wrong audience, 5=partial overlap, 10=perfect match |
| **V**elocity | Time from first touch to hand-raise (inverse) | 1=12+ months, 5=3-6 months, 10=under 30 days |
| **E**fficiency | Expected CAC relative to LTV | 1=unsustainable, 5=acceptable, 10=highly efficient |

**WAVE Composite** = (W x 0.25) + (A x 0.30) + (V x 0.20) + (E x 0.25)

Channels to evaluate: Organic search/SEO, Paid search, Social organic, Social paid, Content marketing, Email nurture, Events/webinars, Partnerships/co-marketing, Community/PLG, Analyst relations, PR/media, Review sites, Account-based marketing, Influencer/creator, Product-led virality, Referral programs

### Step 2: Channel Mix Architecture
Based on WAVE scores:

| Classification | WAVE Score | Investment Level | Action |
|---------------|-----------|-----------------|--------|
| **Primary** | 7.5+ | Heavy -- full program build | 60% of budget |
| **Secondary** | 5.0-7.4 | Moderate -- test and scale | 25% of budget |
| **Experimental** | Below 5.0 | Small experiments | 15% of budget |

Map channel interplay: how channels reinforce each other (e.g., content fuels SEO fuels organic social fuels email nurture).

### Step 3: Content-to-Stage Mapping
Using Journey Architect's 7 gates (or simplified awareness-consideration-decision):

| Stage | Content Purpose | Content Types |
|-------|----------------|--------------|
| G1-G2 (Awareness) | Trigger problem recognition | Thought leadership, industry reports, provocative POVs |
| G2-G3 (Education) | Educate on solutions | How-to guides, comparison frameworks, analyst reports |
| G3-G4 (Differentiation) | Prove you are the best choice | Case studies, demos, technical deep-dives, ROI calculators |
| G4 (Conversion) | Remove purchase barriers | Business case templates, security docs, implementation guides |

### Step 4: Campaign Architecture
For each primary channel, define:
- Campaign theme and messaging (from Position Lock)
- Target audience segment
- Content assets required (from Step 3)
- KPIs and targets (impressions, clicks, MQLs, SQLs, pipeline)
- Timeline (pre-launch, launch week, post-launch sustain)
- Budget allocation

### Step 5: Rebalancing Rules
Monthly rebalancing criteria:
- Channel exceeds CAC target by 25%+ for 2 months: reduce budget 30%
- Channel outperforms CAC target by 25%+: increase budget 20%
- Experiment reserve replenished quarterly from underperforming channel cuts

## Output
Save to `outputs/demand-engine-[YYYY-MM-DD].md`

### Deliverables:
1. **Channel Strategy Matrix**: All channels scored, ranked, and classified with investment levels
2. **Demand Gen Playbook**: Channel-specific tactics, content requirements, and KPIs
3. **Budget Allocation Model**: Allocation by channel and month with rebalancing rules
4. **Content Requirements Map**: What assets are needed, by stage and channel

## Chain Connections
- **Next skill**: Run `enablement-forge` to create the content and sales assets identified here
- **Also feeds**: `budget-allocator` (demand gen budget feeds overall launch budget), `launch-command` (campaigns are a launch workstream)
- **Enhanced by**: Run after `position-lock` (messaging drives content) and `journey-architect` (gates define staging)
