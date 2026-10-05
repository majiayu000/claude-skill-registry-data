---
name: gtm-exec-plan
description: 'Creates a polished 3-4 page GTM executive brief and plan with a 4-slide PowerPoint deck. Orchestrates market analysis, positioning, competitive intel, channel strategy, and launch planning into exec-ready deliverables. Use when: GTM plan, go-to-market plan, GTM strategy, GTM brief, executive GTM plan, GTM deck, GTM presentation, launch plan deck, product GTM strategy, platform GTM, developer platform GTM, new product GTM.'
---

# GTM Exec Plan (PRIME Framework)

Create a polished, executive-ready Go-To-Market brief (3-4 pages) and a 4-slide GTM PowerPoint deck for any new product, feature, or platform initiative. PRIME synthesizes insights from across the GTM skill library into two high-impact deliverables that are ready for leadership review.

## When to Use
- Presenting a GTM strategy to leadership or a steering committee
- Kicking off a new product launch and need an executive-ready plan
- Preparing a GTM strategy for a platform play (e.g., ACME Insight Studio, API ecosystem)
- Board or investor readiness for a go-to-market motion
- Quarterly GTM refresh for an existing product line
- Cross-functional alignment on a launch strategy

## What You'll Need

**Critical inputs (ask if not provided):**
- Product or feature name
- One-sentence value proposition
- Target audience (persona, segment, industry)
- Launch timeline or target date
- Top 3 competitors

**Nice-to-have (will enrich the output):**
- Outputs from other skills: `market-analyzer`, `position-lock`, `battle-scanner`, `demand-engine`
- Pricing model or tier structure
- Internal stakeholder priorities or constraints
- Partner or ecosystem context
- Win/loss data or customer feedback themes

## PRIME Framework

The brief and deck are organized around five executive sections:

| Section | What It Covers | Brief Length | Deck Presence |
|---------|---------------|-------------|---------------|
| **P**ositioning | Why this product wins: value prop, differentiation, messaging hierarchy | ~1 page | Slide 2 |
| **R**eadiness | Market context, competitive landscape, timing rationale | ~0.5 page | Slide 2 |
| **I**mpact | Revenue model, target metrics, success criteria, projected outcomes | ~0.5 page | Slide 3 |
| **M**otion | Channel strategy, demand gen approach, partner leverage, enablement plan | ~1 page | Slide 3 |
| **E**xecution | Phased timeline, milestones, owners, go/no-go gates | ~0.5 page | Slide 4 |

## Process

### Step 1: Gather and Synthesize Inputs

If outputs from other skills are available, pull the following:
- From `market-analyzer` (SCOPE): market size, segment priorities, growth vectors
- From `position-lock` (PRISM): L0-L3 messaging, positioning statement, proof points
- From `battle-scanner` (ARMOR): top 3 competitive threats, differentiation matrix, win themes
- From `demand-engine` (WAVE): channel rankings, budget allocation, content plan

If these are not available, run lightweight inline versions:
1. **Market snapshot**: size the addressable market in 3 bullets
2. **Positioning draft**: write a 1-sentence positioning statement + 3 proof points
3. **Competitive scan**: identify top 3 competitors with 1 strength and 1 weakness each
4. **Channel hypothesis**: rank the top 3 channels for this audience

### Step 2: Write the Executive Brief

Produce a polished 3-4 page document in Markdown with this exact structure:

```
# [Product Name] Go-To-Market Plan
## Executive Summary (10 lines max)

## 1. Positioning and Differentiation
- Value proposition
- Target buyer persona and segment
- Messaging hierarchy (headline, supporting points, proof points)
- Key differentiators vs. alternatives

## 2. Market Readiness and Competitive Landscape
- Market size and opportunity (TAM/SAM/SOM or qualitative framing)
- Timing rationale: why now
- Competitive overview (table: Competitor | Strength | Our Advantage)
- Risk factors and mitigations

## 3. Impact Model and Success Metrics
- Revenue or adoption targets (30/60/90 day and 6-month)
- Primary KPIs (3-5 metrics)
- Leading indicators to track weekly
- Definition of success for this launch

## 4. Go-To-Market Motion
- Channel strategy with priority ranking
- Demand generation approach
- Sales enablement plan (assets, training, objection handling)
- Partner and ecosystem leverage
- Content and campaign calendar (first 90 days)

## 5. Execution Timeline
- Phase 1: Pre-launch (activities, owners, milestones)
- Phase 2: Launch week (day-by-day runbook summary)
- Phase 3: Post-launch (first 30 days)
- Go/no-go gate criteria
- RACI for key workstreams
```

**Writing rules:**
- Write for a VP or C-Suite audience: clear, concise, decisive
- Lead every section with the conclusion, then provide supporting detail
- Use tables and bullets over paragraphs
- No jargon without definition
- Every metric must have a target number or range
- Total length: 3-4 pages when rendered (roughly 1500-2000 words)

### Step 3: Generate the 4-Slide PowerPoint Deck

Use the `ppt-deck-generator` skill or `python-pptx` directly to create a polished .pptx file.

**Slide 1: Title Slide (Dark background)**
- Product name in large white text
- Subtitle: "Go-To-Market Strategy"
- Date and presenter name
- Company or team logo area

**Slide 2: The Opportunity (Light background)**
- Left column: Market context (size, timing, why now) in 3 concise bullets
- Right column: Positioning statement + 3 key differentiators
- Bottom strip: Competitive snapshot (3 competitors, 1 line each)
- Section label: "Positioning and Readiness"

**Slide 3: The Plan (Light background)**
- Left column: Top 3 channels with expected contribution (visual bars or percentages)
- Right column: Success metrics with targets (metric cards: name, target, timeline)
- Bottom strip: Partner/ecosystem leverage (1-2 lines)
- Section label: "Motion and Impact"

**Slide 4: The Timeline (Light background)**
- Horizontal timeline or phased layout: Pre-launch, Launch, Post-launch
- Key milestones with dates
- Go/no-go gate markers
- Owner assignments for each phase
- Section label: "Execution Roadmap"

**Deck design rules:**
- Use the `ppt-deck-generator` color palette (navy dark_bg, primary blue accent, teal accent2)
- Segoe UI font family throughout
- Maximum 30 words per slide section
- Every slide must have one clear takeaway in the title
- No generic titles: use specific, insight-driven headlines (e.g., "Developer Ecosystem is a $2.4B Opportunity" not "Market Overview")

### Step 4: Quality Checklist

Before delivering, verify:
- [ ] Executive summary can stand alone as a 1-minute verbal pitch
- [ ] Every section leads with the conclusion
- [ ] All metrics have specific targets
- [ ] Competitive table has real differentiators (not generic)
- [ ] Timeline has actual dates (not "TBD")
- [ ] Deck slides pass the "5-second scan" test (key message visible immediately)
- [ ] No orphan sections (every claim links to an action)
- [ ] Total brief length: 3-4 pages

## Output

Save to:
- `outputs/gtm-plan-[product]-[YYYY-MM-DD].md` (the executive brief)
- `outputs/gtm-plan-[product]-[YYYY-MM-DD].pptx` (the 4-slide deck)

### Deliverables:
1. **PRIME Executive Brief**: 3-4 page GTM plan covering positioning, readiness, impact, motion, and execution
2. **GTM Strategy Deck**: 4-slide PowerPoint ready for leadership presentation
3. **Execution Timeline**: Phased roadmap with milestones and owners (embedded in both deliverables)

## Chain Connections
- **Feeds from**: `market-analyzer`, `position-lock`, `battle-scanner`, `demand-engine`, `journey-architect`
- **Feeds into**: `launch-command` (the brief becomes the launch input), `enablement-forge` (generates sales assets from the plan), `launch-pulse` (metrics framework from the impact model)
- **Enhanced by**: Run `signal-radar` first for market signals, `whitespace-finder` for opportunity framing
- **Deck generation**: Uses `ppt-deck-generator` skill for PowerPoint output
