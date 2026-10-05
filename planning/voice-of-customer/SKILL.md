---
name: voice-of-customer
description: 'Voice of Customer program - multi-source signal collection, theming and prioritization, evidence-to-action routing, and product / CS / marketing feedback loop closure. Use when: voice of customer, VoC program, customer feedback, NPS / CSAT / CES, qualitative theming, feedback synthesis, product feedback loop, customer insight engine.'
---

# Voice of Customer (ECHO Framework)

Design a Voice-of-Customer program that turns raw feedback into routed, prioritized, evidence-backed actions - not a quarterly NPS report nobody reads. ECHO replaces ad-hoc surveys with a multi-source signal pipeline that PMs, CS, and marketing all rely on.

## Core Principle

**VoC fails when it conflates *collection* with *insight*.** A survey isn't a program. ECHO standardizes how signal is elicited, themed, prioritized, and *closed* - with the loop back to the customer being the most often skipped step.

## The ECHO Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **E** | Elicit | What sources are tapped, with what cadence, and how is bias controlled? |
| **C** | Categorize | How is feedback themed, tagged, and made queryable? |
| **H** | Highlight | What prioritization frame separates signal from noise? |
| **O** | Operationalize | Who owns the action, what's the SLA, and how is the loop closed with the customer? |

## Elicitation Sources

A robust program reads from **multiple channels** and triangulates:

| Source | Quality | Volume | Bias Risk |
|--------|---------|--------|-----------|
| **Surveys (NPS, CSAT, CES)** | Quantitative + open-ended | High | Survey fatigue, selection bias |
| **Win / loss interviews** | Deep qualitative | Low | Selection bias toward closed deals |
| **Customer advisory board** | Strategic qualitative | Very low | Top-customer bias |
| **Support tickets** | Reactive, problem-focused | Very high | Skewed to broken, not desired |
| **Product analytics** | Behavioral, not stated | Very high | Observation without intent |
| **CSM call notes** | Contextual qualitative | High | CSM filter |
| **Sales call recordings** | Pre-sale voice | High | Sales-stage filter |
| **Community / public reviews** | Honest, public | Medium | Vocal-minority bias |
| **Churn / contraction interviews** | High-signal | Low | Painful but most actionable |

## Theming & Tagging

Without disciplined theming, VoC becomes a junk drawer. Adopt:

| Field | Spec |
|-------|------|
| **Theme** | Standardized taxonomy (refreshed quarterly, not ad-hoc) |
| **Severity** | Critical / Major / Minor - based on revenue impact, not emotion |
| **Source** | Channel of origin (survey, ticket, call, etc.) |
| **Segment** | ICP segment, plan tier, motion |
| **Stage** | Pre-sale / Onboarding / Adoption / Renewal / Churn |
| **Evidence Count** | Number of distinct customers raising the theme |
| **Revenue at Risk / Opportunity** | ARR exposure or expansion potential |

## Prioritization Frame

| Lens | Question |
|------|----------|
| **Frequency** | How many distinct customers, by segment? |
| **Severity** | Revenue impact if unaddressed (churn risk, deal blocker) |
| **Solvability** | Effort vs leverage of the fix |
| **Strategic Fit** | Does the fix advance the platform thesis or fix a wart? |
| **Reach** | What share of ARR or users does the change touch? |

Combine into a RICE-style score, but never let the score replace judgment - leadership review is part of the process.

## Operationalize: Route, Act, Close

| Theme Type | Owner | SLA |
|------------|-------|-----|
| **Product bug / friction** | PM / Eng | Triaged in 5 business days |
| **Onboarding gap** | CS Ops | Updated playbook in 10 business days |
| **Messaging / positioning gap** | Product Marketing | Refreshed asset in 15 business days |
| **Pricing / packaging objection** | Pricing Council | Quarterly review |
| **Roadmap signal** | PM Leadership | Roadmap update in next planning cycle |
| **Service quality** | Support Ops | Triaged in 5 business days |

**Loop closure with the customer is non-negotiable.** Every customer who raised a theme should hear back when a related change ships - closes trust loop and earns the next round of feedback.

## Output

Save to `outputs/voice-of-customer-[scope]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **Source Pipeline** | Inventory of channels, cadence, bias controls |
| **Theme Taxonomy** | Standardized themes with definitions and examples |
| **Prioritization Spec** | Scoring criteria, weights, refresh cadence |
| **Routing Map** | Theme types → owners → SLAs |
| **Loop-Closure Protocol** | How and when customers are informed of action taken |
| **VoC Operating Cadence** | Weekly triage, monthly review, quarterly roadmap sync |
| **VoC Dashboard** | Theme volume, severity distribution, action SLA performance, NPS / CSAT trend, closed-loop rate |

## Process

1. **Inventory sources** and design the cadence; eliminate redundant surveys
2. **Standardize the taxonomy** with PM, CS, and marketing co-sign
3. **Score and prioritize** with a written rubric, leadership review monthly
4. **Route to owners** with SLAs; track action time, not just intent
5. **Close the loop** with every customer who raised an actioned theme
6. **Refresh the taxonomy quarterly** - emergent themes deserve their own bucket

## Tips

1. **Survey fatigue is real** - cap touches per customer per quarter
2. **Triangulate sources** - single-source insights are usually wrong
3. **Behavioral data beats stated preference** - pair always
4. **Loop closure is the most under-invested step** - and the highest-leverage one
5. **VoC is a *system*** - one-off projects don't compound

## Pairs With

- **customer-success** - VoC themes feed CS risk plays and EBR agendas
- **customer-analytics** - Behavioral data complements stated feedback
- **journey-architect** - Stage tags align VoC with journey gates
- **enablement-forge** - Updated objection handling responds to recurring VoC themes
