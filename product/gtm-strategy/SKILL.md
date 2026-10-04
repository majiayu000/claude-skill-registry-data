---
name: gtm-strategy
description: Use when user says "go to market", "GTM", "how do we sell this", "find customers", when planning a launch, when defining the ideal customer profile, when designing a pilot program before broad launch, or when a structured sales motion needs to be documented.
---

# GTM Strategy

## Overview

Read `.forge/prd.md` and `.forge/competitive.md` to produce `.forge/gtm.md` — a concrete go-to-market plan. The output must be specific enough that a sales team can execute it without verbal briefing. ICP is a named persona, not a market segment.

## When to Use

- `.forge/prd.md` exists and the product is approaching market readiness
- User asks "how do we sell this" or "who do we sell to first"
- Competitive analysis is done and positioning is clear
- Need a pilot program design or ROI framework

## When NOT to Use

- No PRD exists — run `spec-driven-development` first
- Product is pre-idea — run `idea-griller` first
- User wants to refine the product, not sell it — use `spec-driven-development`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Our ICP is SMBs" | That's a market segment, not a person. Name the title, company size, and daily pain |
| "The product sells itself" | No product sells itself. Name the channel, motion, and first touchpoint |
| "We'll figure out pricing later" | Pricing shapes positioning. A free tool and a $500/mo platform attract different buyers |
| "ROI is hard to quantify" | If the buyer can't calculate ROI, they can't justify the purchase internally |
| "We don't need a pilot — just launch" | Pilots generate case studies. Case studies close deals. No pilot = no proof |

## Red Flags

- ICP is a market segment ("SMBs", "enterprises") instead of a named persona
- Wedge feature is the entire product (not a wedge — it's the whole door)
- Sales channel is "inbound" with no specifics on content strategy or distribution
- ROI calculator uses aspirational numbers instead of conservative estimates
- Pilot has no success criteria or timeline
- Case study template doesn't include quantified before/after

## Core Process

### Step 1: Define ICP

Name the person, not the market:
- **Title**: specific role (e.g., "VP of Sales at a 50-200 person B2B SaaS company")
- **Daily pain**: what frustrates them this week, not abstractly
- **Current solution**: what they do today (the status quo from competitive analysis)
- **Budget authority**: can they sign a check, or do they need approval?
- **Where they hang out**: conferences, communities, publications, Slack groups

### Step 2: Identify the wedge

The wedge is the ONE feature that gets you in the door. Not the whole product — the single capability that makes the ICP say "I need this today."

Rules: the wedge must solve an acute pain (not a nice-to-have), be demonstrable in under 5 minutes, and be usable without the rest of the product.

### Step 3: Design the pilot program

- **Duration**: typically 2-4 weeks
- **Success criteria**: specific metrics the pilot must hit (not "they liked it")
- **Pilot scope**: what's included, what's explicitly out
- **Support model**: how much hand-holding during pilot
- **Conversion trigger**: what happens at pilot end — auto-convert, sales call, or expire?

### Step 4: Map sales channels

For each channel, specify:
- **Channel**: outbound, inbound content, partnerships, PLG, community, events
- **Motion**: exact sequence (e.g., "LinkedIn post → DM → demo → pilot → close")
- **Volume**: how many touchpoints per week to generate pipeline
- **CAC estimate**: approximate cost per acquisition through this channel

### Step 5: Build ROI calculator

Create a formula the buyer can use to justify the purchase:
- **Cost of problem**: hours wasted × hourly rate × frequency
- **Cost of solution**: your pricing
- **Net savings**: conservative estimate (use 50% of theoretical max)
- **Payback period**: months until ROI positive

### Step 6: Create case study template

Structure for capturing pilot results:
- Company profile (size, industry, role of champion)
- Problem before (quantified)
- Solution implemented (which features, how long to deploy)
- Results after (quantified — same metrics as "before")
- Quote from champion

### Step 7: Define success metrics

- **Pilot conversion rate target**: what % of pilots should convert?
- **Time to close**: expected days from first touch to signed deal
- **Expansion signal**: what behavior indicates upsell opportunity?

## Output

Write `.forge/gtm.md` with all sections above. Prepend a `forge:meta` header (`generated_by: gtm-strategy`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/prd.md, .forge/competitive.md]` — paths only, never hashes, `generated_from: {.forge/prd.md: <hash>, .forge/competitive.md: <hash>}` — each upstream's content_hash AT generation time, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

After writing: "GTM strategy written to `.forge/gtm.md`."

## Verification

- [ ] `.forge/prd.md` and `.forge/competitive.md` read before starting
- [ ] ICP names a specific title and company profile, not a market segment
- [ ] Wedge is one feature, not the whole product
- [ ] Pilot has specific success criteria with numbers
- [ ] ROI calculator uses conservative estimates
- [ ] At least 2 sales channels mapped with specific motions
- [ ] Case study template includes quantified before/after
- [ ] `.forge/gtm.md` written
