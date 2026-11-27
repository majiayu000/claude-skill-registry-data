---
name: gtm-engineering
description: "Designs the technical and data infrastructure behind a go-to-market (GTM) motion - data topology, canonical schema, lead and account scoring, routing with Service Level Agreements (SLAs), lifecycle automation, attribution, reverse Extract-Transform-Load (ETL) sync contracts, and observability. Use when designing a lead scoring or Product Qualified Lead (PQL) model; architecting data flows between the Customer Relationship Management (CRM) system, marketing automation, and the warehouse; setting up multi-touch attribution; planning reverse ETL; or auditing a broken Revenue Operations (RevOps) stack."
---

# GTM Engineering

> Treat the revenue stack like a product: schemas, contracts, tests, and observability.

## What this skill is

A workflow for designing the plumbing that makes go-to-market (GTM) strategy executable at scale: lead scoring, routing, enrichment, lifecycle automation, attribution, and the data flows between product, Customer Relationship Management (CRM), Marketing Automation Platform (MAP), and the warehouse. It is not GTM strategy (positioning, channels, messaging); it is the execution layer that strategy depends on.

## What it solves

- Point tools wired together with no-code connectors and hope, with no clear source of truth
- Lead scores that do not reflect actual conversion data
- Attribution models that contradict each other and settle nothing
- Sales reps working the wrong leads because routing and Service Level Agreements (SLAs) are undefined
- Nobody can answer "what does a good lead actually look like?"
- Sync failures and score drift discovered by sales complaints instead of monitoring

## When to invoke

- Designing a lead scoring, Marketing Qualified Lead (MQL), or Product Qualified Lead (PQL) model
- Architecting CRM, warehouse, and MAP data flows
- Building lifecycle automation for onboarding, expansion, or churn risk
- Setting up multi-touch attribution or reverse Extract-Transform-Load (ETL) to operational tools
- Auditing a fragmented Revenue Operations (RevOps) stack or standing one up for a new motion

Gather first: the sales motion (product-led, sales-led, hybrid, channel), the current stack, the business's definition of a qualified lead or account, and where data is broken. Helpful extras: four quarters of conversion data by source and segment, existing scoring rules, SLA targets, and data team capacity.

## Phase 1: Map the current data topology

Inventory every system that produces or consumes GTM data, using these typical layers:

| Layer | Examples |
|-------|----------|
| Sources | Product events, CRM, MAP, ads, billing, support, intent providers |
| Warehouse | Snowflake, BigQuery, Databricks (the source of truth) |
| Modeling | dbt, SQLMesh (canonical entities and metrics) |
| Activation | Reverse ETL (Hightouch, Census) to CRM, MAP, ads, team chat |
| Operational tools | Salesforce, HubSpot, Marketo, Customer.io, Outreach |
| Observability | Monte Carlo, Sifflet, custom dbt tests |

Identify the source of truth for accounts, contacts, opportunities, product usage, and intent. Flag duplicates, conflicts, and orphaned fields.

## Phase 2: Define the canonical schema

Specify the unified account, contact, and event model every downstream system conforms to. For each entity, decide what lives in the warehouse versus the CRM versus the MAP, and why.

## Phase 3: Build the scoring model

| Model type | Use when |
|------------|----------|
| Rules-based | Little data, high need for explainability |
| Logistic regression or gradient boosting | Enough labeled conversion history |
| Two-model (fit x intent) | Separating Ideal Customer Profile (ICP) fit from buying intent |

Validate against historical closed-won data, not intuition. Avoid these anti-patterns:
- Scoring on activity (opens, clicks) instead of fit and intent
- One score that conflates fit and intent (ship two)
- Never re-validating against actual closed-won data
- Rule sprawl with no kill switch for stale rules

## Phase 4: Design routing and SLA logic

Specify routing rules (round-robin, territory, account ownership, capacity-aware), the SLA clock per lead type, and escalation when an SLA is breached. Starting defaults, tuned to the motion:

| Lead type | First-touch SLA |
|-----------|-----------------|
| Inbound demo request | Under 5 minutes |
| High-fit PQL | Under 1 hour |
| MQL | Under 24 hours |
| Re-engagement | Nurture, no SLA |

## Phase 5: Architect lifecycle automation

For each journey (onboarding, activation, expansion, churn risk, win-back), specify:

| Trigger event | Audience query | Channel | Exit criteria | Metric moved |
|---------------|----------------|---------|---------------|--------------|
| | | | | |

## Phase 6: Specify the attribution model

Pick the model honestly: first-touch, last-touch, linear, time-decay, U-shaped, W-shaped, or data-driven (Markov chain or Shapley value). Document its known biases and run at least two models in parallel so debates are data-grounded. Check:
- Does the model match the actual length of the sales cycle?
- Are dark social, direct, and brand-search traffic captured anywhere?
- Are offline touches (events, Account Executive (AE) outreach) ingested?
- Do marketing and sales agree on the model, or merely tolerate it?

## Phase 7: Define reverse ETL and sync contracts

For every field synced from the warehouse to an operational tool:

| Field | Source query | Refresh cadence | Conflict resolution | Downstream consumer | Backfill strategy |
|-------|--------------|-----------------|---------------------|---------------------|-------------------|
| | | | | | |

## Phase 8: Add observability and tests

Monitor lead score drift, routing latency, enrichment hit rate, sync failures, and deduplication collisions. Give each metric an alert threshold and an owner. Plan a phased rollout of what ships in 30, 60, and 90 days.

## Output

- Current-state data topology diagram
- Canonical account, contact, and event schema
- Scoring model specification with a validation plan
- Routing rules and SLA matrix
- Lifecycle journey specifications (trigger, audience, channel, exit)
- Attribution model selection memo
- Reverse ETL sync contracts
- Observability checklist with metrics, alerts, and owners
- Phased 30/60/90-day rollout plan

## Operating rules

**Always**
- Name one source of truth per entity
- Validate scoring against closed-won data
- Separate fit from intent in scoring
- Write a sync contract for every reverse ETL field
- Monitor the GTM stack like production infrastructure

**Never**
- Confuse GTM engineering with GTM strategy
- Score leads on email activity alone
- Rely on a single attribution model without documenting its bias
- Sync fields to operational tools without conflict resolution rules
- Leave stale scoring rules running with no kill switch
