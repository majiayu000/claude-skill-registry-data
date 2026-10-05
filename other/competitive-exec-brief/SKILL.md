---
name: competitive-exec-brief
description: 'Creates an executive-ready competitive analysis brief with a 1-slide PPTX summary for leadership presentations. Use when: competitive brief, exec competitive summary, competitive slide, competitive pptx, board competitive update, leadership competitive briefing.'
---

# Competitive Exec Brief (SHARP Framework)

Transform competitive intelligence into a polished executive-ready brief with a single PowerPoint slide that tells the competitive story at a glance.

## When to Use
- Board meeting competitive updates
- Leadership team strategy reviews
- Investor presentations (competitive landscape slide)
- Quarterly business reviews
- Pre-launch executive briefings

## What You'll Need
**Critical inputs (ask if not provided):**
- Battle Scanner output (or competitor list + your product)
- Audience (board, C-suite, investors, team)

**Nice-to-have:**
- Market Analyzer output (market sizing context)
- Recent win/loss data
- Brand/color guidelines for PPTX

## Process

### Step 1: SHARP Distillation
Take the full competitive analysis and distill into 5 executive-ready elements:

| Element | What It Captures | Max Length |
|---------|-----------------|-----------|
| **S**ituation | Current competitive landscape in 2-3 sentences | 50 words |
| **H**ighlights | Top 3 competitive moves/changes since last review | 3 bullets |
| **A**dvantages | Our top 3 defensible differentiators with proof points | 3 bullets |
| **R**isks | Top 3 competitive threats ranked by likelihood x impact | 3 bullets |
| **P**lan | Recommended competitive actions for next 90 days | 3 bullets |

Rule: Executives need signal, not noise. Every word must earn its place.

### Step 2: Positioning Map
Create a 2x2 positioning matrix:
- Choose the 2 axes that most differentiate you favorably
- Suggested axis pairs: Ease-of-use vs. Power, Price vs. Completeness, Innovation vs. Maturity, Vertical-specific vs. Horizontal
- Place all Ring 1 and Ring 2 competitors on the map
- You should occupy the most attractive quadrant
- If you don't, explain why and what the plan is to get there

### Step 3: Competitive Snapshot Table
One row per competitor, maximum 6 competitors:

| Column | Content |
|--------|---------|
| Competitor | Name and logo (if available) |
| Positioning | Their tagline/positioning in 5 words |
| Strength | Their #1 advantage over us |
| Weakness | Their #1 exploitable vulnerability |
| Our Win Rate | % of competitive deals we win against them |
| Trend | Arrow: improving, stable, declining |

### Step 4: Executive PPTX Slide
Generate a single PowerPoint slide containing:
- **Title**: "Competitive Landscape -- [Quarter/Year]"
- **Left half**: 2x2 positioning map with competitor logos/names plotted
- **Right half**: SHARP summary (Situation + Highlights + Advantages + Risks + Plan)
- **Footer**: Key metric -- overall competitive win rate and trend

Use the `ppt-deck-generator` skill or python-pptx to create the actual .pptx file.

Slide design rules:
- Max 40 words of body text (the rest is visual)
- Use color coding: green = advantage, red = risk, blue = neutral
- One clear takeaway in the slide title (not generic "Competitive Landscape" but specific like "We're winning on [X] but losing ground on [Y]")

### Step 5: Talking Points
Prepare 5 executive talking points (for the presenter):
1. The headline: What is the competitive situation in one sentence?
2. The change: What has shifted since last review?
3. The opportunity: Where can we gain ground?
4. The risk: What keeps you up at night competitively?
5. The ask: What do you need from leadership to win?

## Output
Save to:
- `outputs/competitive-brief-[YYYY-MM-DD].md` (the full brief)
- `outputs/competitive-brief-[YYYY-MM-DD].pptx` (the exec slide)

### Deliverables:
1. **SHARP Executive Brief**: 1-page written brief with all 5 elements
2. **Positioning Map**: 2x2 visual with competitors plotted
3. **Competitive Snapshot Table**: At-a-glance comparison of top competitors
4. **PPTX Slide**: Single exec-ready PowerPoint slide for presentations
5. **Talking Points**: 5 presenter-ready points for the executive meeting

## Chain Connections
- **Next skill**: Run `position-lock` to lock down your positioning based on competitive insights
- **Also feeds**: `enablement-forge` (brief becomes a sales enablement asset), `launch-command` (competitive readiness is a launch gate)
- **Enhanced by**: Run after `battle-scanner` (provides the raw competitive intelligence to distill)
