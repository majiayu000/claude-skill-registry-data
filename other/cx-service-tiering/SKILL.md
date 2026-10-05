---
name: cx-service-tiering
description: Use to design VIP or tiered support programmes and to test whether higher tiers actually deliver better outcomes. Trigger for "VIP support programme", "service tiering", queue priority for premium customers, entitlement vs priority, tier inflation, or "does our enterprise tier get faster support".
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Service tiering

Tiering promises **better support for paying or strategic customers**. The usual
failure is **queue priority without entitlement change** — they wait less but get
the same agents, policies, and outcomes. Executives see a VIP label; customers see
nothing meaningful. Then **tier inflation** puts half the base in "premium" and the
queue priority becomes meaningless.

Design tiering around **measurable outcome differences**, not badges.

## Entitlement vs queue priority

| Mechanism | What it changes | Customer-visible? |
| --- | --- | --- |
| **Queue priority** | Wait time to first reply | Sometimes |
| **Dedicated queue / team** | Skill match, context | If named team responds |
| **SLA targets** | Response and resolution clocks | If reported and met |
| **Entitlements** | What you can do — credits, escalations, phone line | Yes, when used |
| **Named CSM** | Relationship, not ticket speed | Parallel track |

**Priority alone** is cheap to implement and easy to erode. If tier B and tier A share
agents and macros, **only wait time differs** — measure whether that gap exists under load.

## Designing tiers that do something

For each tier, specify **concrete deltas**:

| Dimension | Example tier delta |
| --- | --- |
| Channels | Phone included vs chat-only |
| Hours | 24/7 vs business hours |
| SLA | First response / resolution targets |
| Escalation | Direct line to specialist or lead |
| Commercial | Credit authority, replacement shipping |
| Proactive | Incident notification, success reviews |

If two tiers differ only in **internal routing score**, assume customers experience
them as the same until proven otherwise.

## Measuring whether tiering works

Compare tiers on **matched drivers** — not raw CSAT.

| Metric | Tier A vs B comparison |
| --- | --- |
| Time to first human response | By channel, incident vs normal |
| Time to resolution | Same driver taxonomy |
| Repeat contact rate | Same issue within 7 days |
| Escalation rate | Avoidable vs policy |
| CSAT / effort | Response-rate adjusted |

**Under load test:** When queue depth spikes, does priority tier hold or collapse?
If SLA breaches simultaneously, tiering is cosmetic.

**Sample size:** Small VIP populations produce noisy metrics; use longer windows and
confidence intervals; do not rank on 20 tickets.

## Tier inflation

| Symptom | Cause |
| --- | --- |
| >30–40% of revenue in top tier | Sales adds tier to close deals |
| Automatic upgrade on spend threshold | Everyone becomes VIP |
| Support cannot see tier in UI | Tier exists only in CRM |
| Same SLA met rates all tiers | Priority not operationalised |

**Remedy:** Hard caps on tier population, annual tier audit, or **split "commercial
VIP" from "operational SLA"** so sales promises map to staffed entitlements.

## Operational requirements

- **Tier visible in agent UI** at accept time — not buried in CRM tab.
- **Routing rules** documented and versioned.
- **Overflow behaviour** when VIP queue empty — do not steal from standard incorrectly.
- **Contract registry** — which SKUs map to which tier; support can look up without sales.

## Traps

**Sales promises support cannot fulfil.** New tier launched in contract before queue
exists.

**Priority for angry customers.** Ad hoc escalations train noise; erodes real tiers.

**Outsourcer without tier training.** VIP routed to lowest-cost BPO line.

**Measuring wait time only.** Fast wrong answer is worse than slow right one.

## Present results to the user

1. **Tier definitions** — entitlements and priorities per tier, in customer language.
2. **Operational map** — queues, SLAs, channels, staffing model per tier.
3. **Outcome comparison** — key metrics by tier on matched drivers, with sample sizes.
4. **Load behaviour** — whether priority holds during spikes.
5. **Inflation assessment** — tier population vs design intent; sales drift noted.
6. **Recommendations** — merge tiers, add entitlements, or retire cosmetic priority.
