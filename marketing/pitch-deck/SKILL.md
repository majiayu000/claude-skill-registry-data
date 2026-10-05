---
name: pitch-deck
description: Use when populates branded pitch deck templates with financial data and
  market comps. Use when user says "create pitch deck", "pitch for investors", "populate
  pitchbook".
domain: financial
author: oyi77
license: Apache-2.0
subdomain: financial-analysis
tags:
- analysis
- deck
- finance
- investment
- pitch
version: 1.0.0
category: financial
---


# Pitch Deck

## Persona

**Investment Banker** — Inspired by the `pitch-agent` from anthropics/financial-services. Masters storytelling with numbers, visual design, and investor psychology.

**Core Philosophy:** Every pitch deck answers one question: "Why will this company dominate its market?" Every slide, every number, every visual must point to that answer.

## Overview

Creates institutional-quality pitch decks for fundraising, M&A, and strategic initiatives. Populates branded PowerPoint templates with financial data, market analysis, and competitive positioning. Outputs .pptx files ready for investor meetings.


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use

**Trigger phrases:**
- "pitch deck"
- "Raising Series A/B/C or late-stage round"
- "Pitching to VCs or PE firms"
- "Creating CIM (Confidential Information Memorandum)"


- Raising Series A/B/C or late-stage round
- Pitching to VCs or PE firms
- Creating CIM (Confidential Information Memorandum)
- M&A sell-side process
- Board presentation for strategic decisions
- Teaser creation for anonymous marketing

## When NOT to Use:

- Internal strategy decks (use `research/mckinsey-research`)
- Product demos (use `content/video-editor`)
- Earnings presentations (use `financial/earnings-viewer`)
- One-pager company profiles (use `sales/high-ticket-closing`)

## Implementation


The implementation follows a phased approach: define content strategy, populate data, apply visual design, and generate PowerPoint.


### Phase 1: Content Strategy

**Standard Pitch Structure (10-12 Slides):**
```python
deck_outline = {
    "1_cover": "Company name, tagline, logo",
    "2_problem": "Market pain, size of problem",
    "3_solution": "Product/service, key differentiators",
    "4_market": "TAM/SAM/SOM, growth rate",
    "5_business_model": "Revenue streams, unit economics",
    "6_traction": "Growth metrics, key milestones",
    "7_competitive": "Comp matrix, moat analysis",
    "8_financials": "P&L, projections, unit econ",
    "9_team": "Founders, key hires, advisors",
    "10_ask": "Raise amount, use of funds, terms"
}
```

### Phase 2: Data Population

**Financial Slide (Example):**
```python
financials_slide = {
    "historical_revenue": [1.2, 2.5, 5.0, 10.0],  # $M
    "projected_revenue": [10.0, 18.0, 32.0, 55.0],
    "gross_margin": [0.65, 0.68, 0.72, 0.75],
    "ebitda_margin": [0.10, 0.15, 0.22, 0.28],
    "cash_burn": [-2.0, -3.0, -2.0, 0.0],  # Path to profitability
    "headcount": [20, 35, 60, 100]
}
```

**Market Slide (TAM/SAM/SOM):**
```python
market_slide = {
    "total_addressable_market": 50000,  # $M (global)
    "serviceable_addressable": 5000,   # $M (addressable)
    "serviceable_obtainable": 500,      # $M (realistic capture)
    "cagr": 0.25,  # Market growth rate
    "key_drivers": ["Regulatory tailwinds", "Digital transformation"]
}
```

### Phase 3: Visual Design

**Design Principles:**
```python
design_rules = {
    "density": "max 3 key messages per slide",
    "data_viz": "charts > tables > bullets",
    "color_palette": "brand_colors + 1 accent",
    "fonts": "max 2 (header + body)",
    "white_space": "40% minimum per slide"
}
```

**Chart Types:**
- Revenue growth → Area chart (show trajectory)
- Market sizing → Pyramid (TAM/SAM/SOM)
- Competitive → 2x2 matrix (innovation vs. execution)
- Unit economics → Cohort table or waterfall

### Phase 4: PowerPoint Generation

**Using python-pptx:**
```python
from pptx import Presentation

prs = Presentation("templates/brand_template.pptx")
# Slide 1: Cover
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Company Name"
slide.placeholders[1].text = "Tagline here"

# Slide 4: Market
# Add TAM/SAM/SOM pyramid chart...

prs.save("output/investor_pitch_v3.pptx")
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "More slides = more thorough" | VCs read 10 slides max; beyond that = noise |
| "Show all the features" | investors buy outcomes, not feature lists |
| "Financials are boring, skip details" | Unit economics = #1 investor question |
| "I'll design later" | Template first = 2x faster, consistent branding |
| "Competition slide is negative" | No competition = no market (red flag) |

## Red Flags

- > 15 slides (loses narrative drive)
- No "Why now?" slide (timing is critical)
- Financials not tied to milestones
- Vague TAM/SAM ("$50B market")
- No clear "ask" with use of funds
- Competitive slide missing (or shows "no competition")
- Template not followed (branding inconsistency)

## Verification

After creating a pitch deck, confirm:

- [ ] 10-12 slides max (or justified reason for more)
- [ ] Financial projections: 3 years minimum, unit economics visible
- [ ] Market sizing: TAM/SAM/SOM pyramid with sources
- [ ] Competitive slide: 2x2 matrix or feature comparison
- [ ] "Why now?" narrative: timing thesis articulated
- [ ] Ask slide: amount, use of funds, key milestones
- [ ] PowerPoint file: .pptx generated, opens without errors
- [ ] Branding: follows template, colors/fonts consistent

## Integration Points

**Cross-Skill References:**
- `financial/model-builder` — For DCF/LBO models to embed
- `sales/high-ticket-closing` — For investor meetings
- `research/mckinsey-research` — For market analysis
- `trading/alphaear-strategy` — For competitive intelligence
- `references/trading-checklist.md` — For investment thesis validation

**MCP Server Integrations:**
- FactSet MCP — For public comps data
- S&P Global MCP — For industry benchmarks
- PitchBook MCP — For PE/VC comparables

Load `references/trading-checklist.md` for complete trading checklists.

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
