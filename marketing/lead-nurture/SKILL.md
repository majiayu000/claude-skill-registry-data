---
name: lead-nurture
description: 'Lead nurture orchestration - multi-track nurture design by intent stage, scoring, behavioral triggers, MQL→SQL handoff, and revival of cold leads. Use when: lead nurture, drip campaign, nurture track, lead scoring, MQL to SQL, lifecycle marketing, nurture sequence, behavioral trigger, lead revival, MQL handoff.'
---

# Lead Nurture (NURTURE Framework)

Design a lead-nurture system that respects buyer intent, routes leads to the right next action, and stops sending eight more emails to people who already raised their hand. NURTURE replaces single-track drip sequences with multi-track journeys gated by behavioral signals.

## Core Principle

**Nurture fails when it treats time as the trigger.** "Send email 3 on day 7" assumes every lead is on the same journey. NURTURE treats signal - not the calendar - as the trigger, and gates progression by demonstrated intent.

## The NURTURE Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **N** | Needs Mapping | What buying-stage needs does the lead currently have evidence of? |
| **U** | Understand Intent | What behavioral and explicit signals map to which stage? |
| **R** | Route to Track | Which nurture track does the lead enter, and on what entry criteria? |
| **T** | Trigger Progression | What signal moves the lead to the next step (or back)? |
| **U** | Upgrade to Sales | What threshold defines MQL → SQL handoff, and what's the SLA? |
| **R** | Recycle Cold | When does the lead exit the active track into long-cycle nurture? |
| **E** | Engagement Refresh | How is content kept current and personalization kept honest? |

## Buying-Stage Nurture Tracks

| Stage | Lead State | Track Goal | Cadence |
|-------|-----------|------------|---------|
| **Unaware** | Discovered category, no problem framing | Frame the problem | Bi-weekly |
| **Aware** | Acknowledges problem, exploring | Reframe with our POV | Weekly |
| **Considering** | Evaluating vendors | Differentiate + de-risk | 2-4×/week, behavior-gated |
| **Decision** | Short-listed | Accelerate to demo / sales | Daily during active window |
| **Dormant / Lost** | No activity 60+ days OR closed-lost | Reactivate on signal | Quarterly check-in + signal trigger |

## Intent Signals

A robust nurture system reads **explicit** and **behavioral** signals together:

| Type | Example | Implication |
|------|---------|-------------|
| **Explicit** | Form fill, demo request, pricing page submit | High-confidence stage signal |
| **Behavioral - high** | Pricing page, comparison page, case study deep read | Considering or Decision |
| **Behavioral - medium** | Webinar registration, ebook download | Aware → Considering |
| **Behavioral - low** | Blog visit, newsletter open | Unaware → Aware |
| **Decay** | No engagement 30+ days | Re-route to lighter cadence |

## Lead Scoring Design

Combine **fit** (firmographic) and **intent** (behavioral) into a 2D grid, not a single score:

| Fit \\ Intent | Low | Medium | High |
|---|---|---|---|
| **High** | Marketing nurture | Sales-assist | SQL - immediate |
| **Medium** | Standard nurture | Behavior-gated | SDR-triggered |
| **Low** | Newsletter only | Selective nurture | Manual triage |

## MQL → SQL Handoff

Failures here cost more pipeline than any other nurture problem. Codify:

| Element | Spec |
|---------|------|
| **MQL Definition** | Fit + intent threshold, with named behavioral triggers |
| **SQL Definition** | Sales-acceptance criteria written by sales |
| **Handoff SLA** | First sales touch within X hours of MQL |
| **Disposition Loop** | Sales must reason-code rejected MQLs; feeds scoring tuning |
| **Recycle Path** | Rejected MQLs return to specific track, not a black hole |

## Output

Save to `outputs/lead-nurture-[program]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **Track Map** | Named tracks with entry / exit criteria and goal |
| **Signal Catalog** | Explicit + behavioral signals with weights |
| **Scoring Grid** | Fit × intent matrix with routing rules |
| **Content Plan** | Asset list per stage, refresh cadence |
| **Handoff Spec** | MQL / SQL definitions, SLA, disposition loop |
| **Recycle Plan** | Cold-lead criteria and reactivation triggers |
| **KPIs** | MQL → SQL conversion, SQL → opportunity rate, time-to-handoff, disposition reasons |

## Process

1. **Map the buying stages** for your motion; never assume one-size-fits-all
2. **Catalog the signals** and weight them by historical conversion lift
3. **Design tracks per stage** with explicit entry / exit, not just send schedules
4. **Build the scoring grid** with sales co-sign; align on MQL / SQL definitions
5. **Spec the handoff** with SLA, disposition loop, and recycle path
6. **Stand up the engagement refresh cycle** - quarterly content audit + signal recalibration

## Tips

1. **Time-based drip is anti-nurture** - gate progression by signal, not by day
2. **Score is 2D, not 1D** - fit and intent must remain separable
3. **A rejected MQL with no reason code is a broken loop** - enforce disposition
4. **Refresh content quarterly** or the program self-decays
5. **Cold leads aren't dead** - long-cycle nurture frequently produces 10-20% of pipeline

## Pairs With

- **demand-engine** - Channel mix that originates the leads
- **journey-architect** - Stages the nurture tracks attach to
- **enablement-forge** - Produces the per-stage assets
- **customer-success** - Inherits the lead at first value handoff
