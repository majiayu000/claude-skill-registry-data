---
name: abm-playbook
description: 'Account-Based Marketing playbook builder - tiered account list (1:1, 1:few, 1:many), buying-group mapping, coordinated multi-channel plays per account, and pipeline acceleration plays for in-cycle accounts. Use when: ABM playbook, account-based marketing, target account list, tiered accounts, 1:1 marketing, buying group, named-account strategy, ABM plays, pipeline acceleration, in-cycle account acceleration.'
---

# ABM Playbook (TIER Framework)

Build a complete Account-Based Marketing playbook - tiered account list, buying-group map per tier, coordinated multi-channel plays, and pipeline acceleration plays for accounts already in cycle. ABM is structurally different from PLG, sales-led, and channel motions; this skill captures that difference rather than bolting it onto a generic GTM template.

## Core Principle

**ABM is a *coordination* problem, not a targeting problem.** Most failed ABM programs pick the right accounts and then run the same demand-gen plays they always did. The TIER framework forces explicit coordination across channels and across tiers, with different play patterns for different account intimacy levels.

## The TIER Framework

| Letter | Stage | The Question |
|--------|-------|--------------|
| **T** | Tier the Accounts | Which accounts get 1:1, which get 1:few, which get 1:many? |
| **I** | Identify the Buying Group | Who are the personas in each account, and what's each one's win condition? |
| **E** | Execute Coordinated Plays | What multi-channel plays run *per account* (not per persona)? |
| **R** | Re-route on Signal | When an account hits an in-cycle signal, which acceleration play activates? |

## Account Tiering

| Tier | Account Count | Investment per Account | Personalization | Signal Cadence |
|------|--------------:|------------------------|-----------------|----------------|
| **1:1** | 5-25 | High (custom content, exec engagement, dedicated SDR) | Per-account creative | Weekly |
| **1:few** | 25-150 | Medium (cluster-level personalization, named SDR pod) | Per-cluster (3-8 accounts share) | Bi-weekly |
| **1:many** | 150-2000 | Low (scaled programs with industry/persona personalization) | Per-segment creative | Monthly |

## Buying Group Mapping

Every targeted account has a **buying group**, not a single buyer. The skill enforces explicit mapping:

| Role | Win Condition | Common Title Patterns |
|------|---------------|----------------------|
| **Champion** | Personal outcome (career capital, problem solved) | Director / Sr. Manager in problem domain |
| **Economic Buyer** | Business outcome (revenue, cost, risk) | VP / SVP, CFO |
| **Technical Evaluator** | Risk reduction (architecture, security, fit) | Sr. Engineer / Architect / IT Director |
| **End User** | Day-to-day usability | Individual contributors |
| **Procurement / Legal** | Compliance, terms, pricing posture | Procurement, Legal, Security |

A play that engages only the Champion fails because the deal stalls at Economic Buyer or Procurement. The skill enforces multi-role engagement design.

## Output

Save to `outputs/abm-playbook-[motion]-[YYYY-MM-DD].md`

| Artifact | Description |
|----------|-------------|
| **Tiered Account List** | Account names + tier assignment + rationale |
| **Buying Group Maps** | Per-account (1:1) or per-cluster (1:few) with named roles + engagement state |
| **Play Library** | 6-10 named plays, each tagged by tier + buying-group role + channel mix |
| **Acceleration Plays** | 3-5 plays triggered by in-cycle signals |
| **Coordination Calendar** | Weekly view across all channels per tier - catches over- and under-engagement |
| **Measurement Plan** | Per-tier KPIs: account-level engagement, opportunity creation, pipeline velocity, win rate |

## The Play Library Pattern

Every play follows this structure:

| Field | Example |
|-------|---------|
| **Name** | "Exec-to-Exec Insight Letter" |
| **Trigger** | New 1:1 account assigned, or champion change |
| **Roles Engaged** | Economic Buyer, Champion |
| **Channels** | LinkedIn (exec), Email (champion), Direct mail (exec) |
| **Sequence** | Day 0 LI connect → Day 3 letter delivered → Day 5 champion email → Day 14 ABR follow-up |
| **Personalization Level** | Per-account (researched insight specific to stated priorities) |
| **Success Signal** | Exec response or champion-confirmed read |
| **Hand-off** | Signal → SDR books exec briefing; no signal in 21 days → re-route |

## Acceleration Play Triggers

| Signal | Acceleration Play |
|--------|-------------------|
| Intent surge (3rd-party) | Account-level ad burst + SDR re-engagement within 48h |
| Pricing-page or competitor-comparison hit | Inbound BDR call within 1 business day, deal-context-aware script |
| Security questionnaire received | Pre-built security artifact pack + named SE engagement |
| Deal stalled > 21 days in stage | Champion enablement kit + multi-thread to EB + Procurement |
| Champion changes role / leaves | "Land the new champion" play within 1 week of signal |

## Process

1. **Tier the accounts** with explicit rationale per tier; cut accounts that don't justify any tier
2. **Map buying groups** - full named mapping for 1:1, role patterns for 1:few, persona-level for 1:many
3. **Build the play library** - 6-10 plays covering cold start through expansion; every play names a role
4. **Design acceleration plays** for each in-cycle signal - trade scale for speed
5. **Build the coordination calendar** - weekly view to catch over- and under-engagement
6. **Define per-tier measurement** with ABM-friendly metrics (lead-level MQLs are not the right yardstick)

## Per-Tier Measurement

| Tier | Primary KPI | Secondary KPIs |
|------|-------------|----------------|
| 1:1 | Pipeline created per account | Account engagement score, EB meetings booked, deal velocity |
| 1:few | Pipeline created per cluster | Cluster engagement rate, opportunity conversion |
| 1:many | Pipeline created per program | Account engagement coverage, MQA rate |

## Tips
1. **Tier with rationale, not gut feel** - every 1:1 is an investment commitment
2. **Plays are per-account, not per-channel** - channel-led ABM almost always over-engages
3. **Acceleration > acquisition** - in-cycle accounts are 5-10× more efficient than cold ABM
4. **Re-tier quarterly** - accounts that don't engage in 1:1 for 2 quarters drop to 1:few
5. **Pair with intent scoring + channel orchestration** - ABM consumes those outputs

## Pairs With

- **journey-architect** - Maps the buyer journey; ABM coordinates above it
- **demand-engine** - Channel-level orchestration the calendar consumes
- **enablement-forge** - Produces the assets each play needs
- **competitive-battlecard** - Per-deal cards that drop into in-cycle acceleration
