---
name: battle-scanner
description: 'Competitive intelligence engine that deconstructs competitor positioning, surfaces exploitable weaknesses, and predicts competitive responses. Use when: competitive analysis, competitor research, competitive landscape, competitive intelligence, who are our competitors, how do we compete against.'
---

# Battle Scanner (ARMOR Analysis)

Deconstruct competitor strategy, surface exploitable weaknesses, predict their responses to your moves, and generate win/loss playbooks.

## When to Use
- Pre-launch competitive assessment
- Competitive deal strategy
- Quarterly competitive landscape refresh
- New competitor entering the market
- Win rate declining against specific competitor

## What You'll Need
**Critical inputs (ask if not provided):**
- Your product/company name and category
- Top 3-5 known competitors

**Nice-to-have:**
- Signal Radar output (competitive threat signals)
- Win/loss data from CRM
- Customer feedback mentioning competitors

## Process

### Step 1: 4-Ring Competitor Classification
Map every competitor into concentric rings:

| Ring | Type | Threat Level | Examples |
|------|------|-------------|----------|
| Ring 1 | **Direct** -- same problem, same approach | Highest | Head-to-head feature competitors |
| Ring 2 | **Indirect** -- same problem, different approach | High | Alternative solution categories |
| Ring 3 | **Adjacent** -- different problem, could pivot | Medium | Companies with overlapping capabilities |
| Ring 4 | **Substitute** -- manual/DIY/status quo | Baseline | Spreadsheets, manual processes, in-house builds |

### Step 2: ARMOR Deep Dive (per Ring 1-2 competitor)
Analyze each competitor across 5 dimensions:

| Dimension | What to Analyze | Key Questions |
|-----------|----------------|---------------|
| **A**rchitecture | Product architecture, tech stack, scalability | What are their technical limitations? Where is their tech debt? |
| **R**eputation | Brand perception, NPS, review scores, analyst position | Where do customers love them? Where do customers complain? |
| **M**oat | Defensibility -- network effects, data, switching costs, IP | What makes them hard to displace? What is their weakest moat? |
| **O**penings | Exploitable weaknesses -- complaints, gaps, pricing issues | Where are they vulnerable RIGHT NOW? |
| **R**esponse Prediction | How they will respond to your launch | Will they: fast-follow, price war, FUD, ignore, or acquire? |

For Response Prediction, consider:
- Their resources (cash, team size, engineering velocity)
- Their strategic priorities (are they focused elsewhere?)
- Historical behavior (how did they react to past competitive moves?)

### Step 3: Win/Loss Pattern Extraction
For each Ring 1 competitor, document:
- **Win scenarios**: When and why we beat them (deal stage, buyer type, use case)
- **Loss scenarios**: When and why they beat us (same breakdown)
- **Swing factors**: What tips deals one way or the other
- **Killer questions**: Questions that expose their weaknesses in a sales conversation
- **Trap questions**: Questions they ask to make us look bad (and how to handle them)

### Step 4: Competitive Landscape Summary
Create the master competitive landscape document with:
- Market positioning map (2x2 or multi-axis)
- Per-competitor ARMOR summary (1 paragraph each)
- Top 3 strategic competitive moves to make in next 90 days

## Output
Save to `outputs/battle-scanner-[YYYY-MM-DD].md`

### Deliverables:
1. **Competitive Landscape Map**: 4-ring visual with all competitors classified and ARMOR-scored
2. **Competitor Profiles**: Per-competitor ARMOR deep dive with evidence
3. **Win/Loss Playbooks**: Scenario-based guides for competitive deal situations
4. **Response Prediction Matrix**: How each competitor will likely react to your launch with counter-strategies

## Chain Connections
- **Next skill**: Run `competitive-exec-brief` to create the executive-ready PPTX summary
- **Also feeds**: `position-lock` (competitive gaps inform positioning), `enablement-forge` (battle cards become sales assets)
- **Enhanced by**: Run after `signal-radar` (signals reveal competitive threats) and `whitespace-finder` (gaps show where competitors are weak)
