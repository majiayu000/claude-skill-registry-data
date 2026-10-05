---
name: customer-analytics
description: 'Customer analytics framework - cohort retention, lifecycle funnels, engagement scoring, segmentation, and behavioral diagnostics for product and CS teams. Use when: customer analytics, cohort analysis, retention curve, engagement score, customer segmentation, behavioral analysis, lifecycle funnel, RFM, activation diagnostics, usage analysis.'
---

# Customer Analytics (LENS Framework)

Design a customer analytics architecture that answers *which customers, doing what, are driving (or breaking) the business* - instead of dashboards full of vanity counts. LENS produces a defensible segmentation, a retention model, an engagement score, and a behavioral diagnostic loop that PMs and CS can act on weekly.

## Core Principle

**Customer analytics fails when it stops at "users went up." LENS forces decomposition into *who*, *what*, *when*, and *why* - the four axes a dashboard usually collapses into one number.**

## The LENS Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **L** | Lifecycle Mapping | What are the named lifecycle stages and what does each one's "good" look like? |
| **E** | Engagement Scoring | What weighted score combines depth, breadth, and recency of value events? |
| **N** | Net Retention Decomposition | Where exactly is NRR coming from - new logo, expansion, contraction, churn? |
| **S** | Segment Behavior | Which segments behave differently, and which behavioral cohorts predict outcomes? |

## Lifecycle Stages

| Stage | "Good" Signal | Diagnostic |
|-------|---------------|------------|
| **New** | First value event within target window | Activation rate by cohort |
| **Activated** | ≥ N value events / week within 30 days | Stickiness (DAU/WAU or analog) |
| **Habituated** | Multi-workflow + multi-user adoption | Workflow coverage % |
| **Expanding** | New seats / modules / use cases attached | Expansion lead indicators |
| **At-risk** | Engagement decay + stakeholder loss | Churn-risk score |
| **Churned / Contracted** | Logo or ARR loss | Reason-coded post-mortems |

## Engagement Scoring

Engagement is **depth × breadth × recency**, not raw event counts.

| Dimension | Definition | Example |
|-----------|------------|---------|
| **Depth** | Frequency of core value events per active user | Core actions / week |
| **Breadth** | % of paid seats active + # of distinct workflows used | Seat activation, workflow coverage |
| **Recency** | Time since last value event, weighted exponentially | Decay half-life of 14-30 days |

Combine into a 0-100 score; bucket into Engaged / Mixed / Disengaged for routing into CS plays.

## Net Retention Decomposition

A single NRR number hides the truth. Always decompose:

| Component | Formula | What It Tells You |
|-----------|---------|-------------------|
| **GRR** | (Starting ARR − Churn − Contraction) / Starting ARR | Floor on the business |
| **Expansion %** | Expansion ARR / Starting ARR | Upside from existing book |
| **NRR** | GRR + Expansion % | Compound growth signal |
| **Churn drivers** | Reason-coded, % of churned ARR by reason | Where to fix the leak |
| **Contraction drivers** | Seat reductions vs price reductions vs downgrades | Where pricing/packaging is misaligned |

## Segment Behavior

Segments must be **decision-driving**, not decorative. Two segmentation lenses:

| Lens | Example | Use For |
|------|---------|---------|
| **Firmographic** | Industry × Size × Region | GTM motion design |
| **Behavioral** | Activation pattern, workflow mix, usage intensity | Lifecycle interventions, expansion targeting |

The behavioral lens almost always predicts retention better than the firmographic one - most teams underuse it.

## Output

Save to `outputs/customer-analytics-[scope]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **Lifecycle Model** | Named stages with entry/exit criteria + "good" definitions |
| **Engagement Score Spec** | Dimensions, weights, decay, bucket thresholds |
| **NRR Decomposition** | Waterfall: starting → expansion → contraction → churn → ending |
| **Segment Behavior Matrix** | Behavior cohorts × outcome (retention, expansion, time-to-value) |
| **Diagnostic Loop** | Weekly review template: anomaly → hypothesis → action → owner |
| **Cohort Retention Curves** | M0-M12 retention by acquisition cohort and segment |

## Process

1. **Map lifecycle stages** with entry/exit criteria - agree with PM and CS before instrumenting
2. **Define engagement score** with explicit weights; validate against historical churn
3. **Decompose NRR** into a waterfall - every component reason-coded
4. **Build behavioral cohorts** that predict outcomes better than firmographics
5. **Stand up the diagnostic loop** - weekly anomaly review, owner assigned, action tracked
6. **Wire cohort retention curves** into the executive cadence, not buried in a tool

## Tips

1. **Avoid vanity engagement metrics** - logins, page views, and DAU rarely predict retention
2. **Validate the score against churn before deploying** - score that doesn't correlate is decoration
3. **Segment behavior beats firmographic targeting** for retention plays
4. **Treat contraction separately from churn** - different root causes, different fixes
5. **Anomaly without action is noise** - every diagnostic must end with an owner

## Pairs With

- **journey-architect** - Lifecycle stages map directly to journey gates
- **customer-success** - Health score consumes the engagement score
- **growth-loop** - Retention curves feed loop-strength analysis
- **revenue-analytics** - NRR decomposition rolls into revenue diagnostics
