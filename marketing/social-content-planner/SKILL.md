---
name: social-content-planner
description: Create a Meta Ads social content proposal based on brand guidelines and competitor analysis. Generates funnel strategy, landing pages, ad creatives, video scripts, and budget allocation. Outputs both markdown and HTML for review before asset creation.
---

# Social Content Planner

Generate a comprehensive Meta Ads social content proposal for any brand, based on their products, positioning, and competitor learnings.

## Prerequisites

Before running this skill, you should have:

1. **Brand Bible** — Run `/website_brand_analysis` first, or have existing brand guidelines
2. **Competitor Analysis** (optional but recommended) — Run `/meta_ads_analyser` on 1-2 competitors to identify winning patterns

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Brand guidelines | Brand bible or `/website_brand_analysis` output | ✅ Yes |
| Product ladder | From brand bible (pricing, tiers) | ✅ Yes |
| Competitor analysis | From `/meta_ads_analyser` output | ⭕ Recommended |
| Target audience | From brand bible ICP section | ✅ Yes |
| Existing assets | Landing pages, lead magnets, etc. | ⭕ Optional |

## Workflow

### Phase 1: Gather Context

1. **Load brand bible** — Products, pricing, voice, visual style
2. **Load competitor analysis** (if available) — Winning patterns, funnel structures
3. **Identify product ladder** — Free → Low-ticket → High-ticket → Enterprise
4. **Note existing assets** — What landing pages/lead magnets already exist?

### Phase 2: Design Funnel Strategy

Map the customer journey:

```
TOFU (Cold Traffic)
├── Lead magnets (quiz, free course, valuable content)
├── Goal: Email capture, pixel building
└── Budget: 50-60%

MOFU (Warm Traffic — Retargeting)
├── Low-to-mid ticket offers
├── Goal: First purchase, course sales
└── Budget: 30-40%

BOFU (Hot Traffic — High Intent)
├── High-ticket / enterprise offers
├── Goal: Sales calls, team deals
└── Budget: 10-15%
```

### Phase 3: Define Landing Pages

For each funnel stage, recommend landing pages:

**TOFU Landing Pages:**
- Quiz/assessment pages (high conversion, low friction)
- Free course/lead magnet pages
- Tutorial/value content pages

**MOFU Landing Pages:**
- Paid traffic variants of product pages
- More aggressive than organic pages
- Include: price anchoring, urgency, testimonials

**BOFU Landing Pages:**
- Existing sales pages
- "Book a call" pages
- Case study pages

### Phase 4: Design Ad Creatives

Create 6-10 ad concepts across the funnel:

**TOFU Ads (3-4 creatives):**
- Video: Hook + problem + free offer CTA (25-35s)
- Image: Native/organic style (doesn't look like ad)
- Carousel: Value bomb / tutorial teaser

**MOFU Ads (2-3 creatives):**
- Video: Identity + agitation + solution + proof (30-40s)
- Image: Price anchoring, transformation

**BOFU Ads (1-2 creatives):**
- Video: Case study, results-focused (35-45s)
- Image: Social proof, consultation CTA

### Phase 5: Write Video Scripts

For each video ad, write a full script with:

```
[TIMESTAMP] SECTION NAME
"Dialogue / voiceover text"

Visual notes: What's on screen
```

**Script structure:**
1. **Hook (0-3s)** — Pattern interrupt, curiosity, or identity call-out
2. **Problem (3-10s)** — Agitate the pain point
3. **Solution (10-20s)** — Introduce the offer
4. **Proof (20-30s)** — Testimonials, numbers, credibility
5. **CTA (last 5s)** — Clear next step

### Phase 6: Define Image Ad Concepts

For each image ad, describe:
- **Concept** — What style/approach
- **Text on image** — Actual copy
- **Visual notes** — Design direction
- **Landing page** — Where it drives

**Image styles that work:**
- Native/organic (notebook, text post)
- Bold claim + price
- Before/after
- Tutorial preview
- Quote/testimonial

### Phase 7: Budget & Testing Plan

**Budget allocation:**
- TOFU: 50-60%
- MOFU: 30-40%
- BOFU: 10-15%

**Testing phases:**
1. Weeks 1-2: TOFU testing, find winning lead magnet
2. Weeks 3-4: MOFU activation, first sales
3. Weeks 5-8: Optimization, scaling winners

### Phase 8: Generate Outputs

Create two files:

1. **Markdown** — `{brand}-social-content-plan.md`
2. **HTML** — `{brand}-social-content-plan.html`

Both should include:
- Executive summary
- Funnel strategy with diagram
- Landing page recommendations
- Ad creative cards (with scripts/concepts)
- Budget allocation
- Testing plan
- Approval checklist

**Save to:** `~/clawd/output/`

### Phase 9: Deliver & Get Approval

Send both files to user with summary:
- Number of landing pages proposed
- Number of ad creatives
- Key strategic decisions to approve

**Include approval checklist:**
1. ✅/❌ Overall funnel strategy
2. ✅/❌ Landing page concepts
3. ✅/❌ Ad creative concepts
4. ✅/❌ Video scripts
5. ✅/❌ Budget allocation

**Wait for approval before creating actual assets.**

## Output Format

### Markdown Structure

```markdown
# {Brand} Meta Ads Social Content Plan

## Executive Summary
[Overview, approach, asset count]

## Strategic Framework
[Competitor learnings, product ladder, funnel structure]

## Proposed Landing Pages
[For each page: URL, purpose, structure, key elements]

## Proposed Ad Creatives
### TOFU Ads
[Ad cards with scripts/concepts]

### MOFU Ads
[Ad cards with scripts/concepts]

### BOFU Ads
[Ad cards with scripts/concepts]

## Creative Summary
[Table of all ads]

## Budget Allocation
[Percentages and reasoning]

## Testing Plan
[Phased approach]

## Assets to Create
[Checklist]

## Approval Checklist
[Items for client to approve]
```

### HTML Structure

Use template at `templates/proposal-template.html`:
- Clean white background, doc-like styling
- Funnel diagrams (text-based)
- Script blocks with timestamps
- Image ad mockups (styled divs)
- Badge system for TOFU/MOFU/BOFU
- Approval checklist section

## Patterns from Competitor Analysis

When competitor analysis is available, apply these patterns:

| Pattern | How to Apply |
|---------|--------------|
| Quiz/assessment TOFU | Create a quiz lead magnet if none exists |
| Credibility stacking | Add logos/credentials in first 10s of video |
| Two-tier funnel | Separate cold and warm audiences clearly |
| Native creative | Include at least one "doesn't look like an ad" image |
| Identity-driven copy | Use "you're the kind of person who..." language |
| Price anchoring | Compare low-ticket to high-ticket alternative |

## Example Funnel Structures

### Education/Course Business
```
FREE: Crash course / Quiz / Tutorials
€200-500: Beginner course
€500-1000: Advanced course
€5k+: Coaching / Team training
```

### SaaS Business
```
FREE: Trial / Freemium / Lead magnet
€50-200/mo: Individual plan
€200-500/mo: Team plan
€1k+/mo: Enterprise
```

### Agency/Services
```
FREE: Audit / Assessment / Calculator
€500-2k: Entry service / Workshop
€5-20k: Main service package
€50k+: Retainer / Enterprise
```

## Integration with Other Skills

This skill works best when combined with:

1. **`/website_brand_analysis`** — Generate brand bible first
2. **`/meta_ads_extractor`** → **`/meta_ads_analyser`** — Analyze competitor ads
3. After approval: Create assets (landing pages, video scripts, images)

## Tips for Better Proposals

1. **Lead with strategy, not tactics** — Explain the funnel logic before listing ads
2. **Show the math** — If possible, estimate CAC, LTV, ROAS
3. **Include native creative** — At least one ad that doesn't look like an ad
4. **Write real scripts** — Don't leave placeholders, write actual dialogue
5. **Make approval easy** — Clear checklist at the end
6. **Visual mockups help** — Even text-based mockups of image ads
