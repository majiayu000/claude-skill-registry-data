---
skill_id: marketing-sales-gtm
name: Sales & GTM Strategy
version: 1.0.0
parent: marketing
office: CMO
reads_first: MARKETING-CONTEXT.md
triggers:
  - sales enablement
  - go-to-market
  - launch strategy
  - sales deck
  - outbound
  - GTM
  - battle card
  - product launch
  - market entry
---

# Sales & GTM Strategy

> **Before starting:** Read `MARKETING-CONTEXT.md` in this domain for product, ICP, and positioning context.

## What This Skill Does

Designs go-to-market strategies and produces sales enablement materials that align marketing messaging with sales execution. Covers GTM motion selection (product-led vs. sales-led vs. community-led), launch planning, battle cards, objection handling guides, and outbound sequences. Ensures marketing and sales tell the same story with the same proof points.

## Key Questions to Ask

1. Is this a new product launch, new market entry, or existing product expansion?
2. What is the primary GTM motion? (product-led growth, sales-led, community-led, hybrid)
3. What is the sales cycle length and deal size?
4. Who are the buyer personas? (decision-maker, influencer, champion, blocker)
5. What is the current sales team structure? (inbound SDRs, outbound AEs, self-serve)
6. What competitors will come up in every sales conversation?

## Framework / Approach

### GTM Motion Selection

| Motion | Best When | Key Metric | Team Shape |
|---|---|---|---|
| **Product-Led Growth (PLG)** | Low price, high volume, try-before-buy | Activation rate, PQL conversion | Product + growth eng |
| **Sales-Led** | High ACV, complex sale, enterprise | Pipeline velocity, win rate | SDR + AE + SE |
| **Community-Led** | Developer tools, open source, niche | Community engagement, organic inbound | DevRel + content |
| **Partner/Channel** | Market coverage, industry expertise | Partner-sourced revenue | Partner manager |
| **Hybrid** | Multi-segment, expanding upmarket | Segment-specific metrics | Flexible team |

### Launch Planning Framework

1. **Pre-Launch (T-30 to T-0)**
   - Finalize positioning (use `positioning` skill)
   - Create sales enablement kit (deck, battle cards, FAQ, demo script)
   - Brief sales team (training session + recorded walkthrough)
   - Seed content and PR (use `content-strategy` skill)
   - Set up tracking and attribution (use `paid-measurement` skill)

2. **Launch Week (T-0 to T+7)**
   - Coordinated announcement (email, social, PR, community)
   - Sales outbound blitz (target accounts, personalized outreach)
   - Paid amplification (targeted campaigns to ICP)
   - Internal momentum (Slack updates, leaderboard, quick wins)

3. **Post-Launch (T+7 to T+90)**
   - Measure against launch KPIs
   - Collect early customer feedback (use `customer-research` skill)
   - Iterate messaging based on sales call recordings
   - Scale what's working, kill what's not

### Sales Enablement Kit

| Asset | Purpose | Owner |
|---|---|---|
| **Sales deck** | Structured pitch narrative | Marketing + Sales |
| **Battle cards** | Competitive positioning per competitor | Marketing |
| **Objection handling guide** | Top 10 objections with responses and proof | Marketing + Sales |
| **Demo script** | Structured product walkthrough | Product + Sales |
| **Case studies** | Social proof for specific segments | Marketing |
| **ROI calculator** | Quantify value for the buyer | Product Marketing |
| **Email templates** | Outbound and follow-up sequences | Marketing |
| **One-pager** | Leave-behind or attach to email | Marketing |

## Output Format

```markdown
## GTM Plan: [Product / Market / Launch Name]

### GTM Motion
- Primary: [PLG / Sales-Led / Community-Led / Hybrid]
- Rationale: [why this motion fits]

### Target Segments
| Segment | ICP Description | ACV Range | Sales Motion |
|---|---|---|---|
| [segment] | [description] | [$range] | [self-serve / inside sales / field sales] |

### Launch Timeline
| Phase | Dates | Key Activities | Owner |
|---|---|---|---|
| Pre-Launch | [T-30 to T-0] | [activities] | [team] |
| Launch | [T-0 to T+7] | [activities] | [team] |
| Post-Launch | [T+7 to T+90] | [activities] | [team] |

### Sales Enablement Deliverables
| Asset | Status | Due Date |
|---|---|---|
| [asset] | [draft / review / final] | [date] |

### Battle Card: [Competitor Name]
| Dimension | Us | Them | Talk Track |
|---|---|---|---|
| [dimension] | [our strength] | [their approach] | [what to say] |

### Launch KPIs
| Metric | Target | Measurement |
|---|---|---|
| [metric] | [goal] | [how measured] |
```

## Related Skills
- `positioning` -- messaging foundation for all GTM materials
- `copywriting` -- writing sales deck copy and email templates
- `email-sequences` -- outbound and follow-up email sequences
- `paid-measurement` -- launch campaign measurement
- `content-strategy` -- content supporting the GTM launch

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
