---
name: slo-sla-management
description: Define, calculate, and manage Service Level Indicators, Objectives, and Agreements. Covers error budget calculation, burn rate alerting (fast and slow burn), multi-window multi-burn-rate alerts, SLO-as-negotiation-tool between product and engineering, and the "ship or freeze" decision framework when burning error budget.
triggers:
  - "define an SLO"
  - "SLO"
  - "SLA"
  - "error budget"
  - "reliability target"
  - "how reliable should this be"
  - "service level objective"
  - "burn rate alert"
  - "SLI"
  - "service level indicator"
  - "availability target"
  - "error rate"
  - "reliability engineering"
audience: engineer, manager
---

# SLO / SLA Management

## Context

Service Level Indicators, Objectives, and Agreements are the language of reliability. They let engineering teams make explicit, data-driven commitments about system behavior — and give product and business stakeholders a meaningful way to negotiate trade-offs between reliability and velocity.

Without SLOs, reliability is either ignored until a P0 incident happens, or treated as infinite ("it must never go down"), which kills velocity. SLOs create a shared, quantified contract that makes both extremes visible.

Use this skill when:
- A team is being asked "how reliable is this service?" and has no answer
- Engineers and product managers are arguing about whether it's safe to ship
- You need to set up alerting that distinguishes "slow bleed" from "on fire"
- A service has an SLA with a customer and the engineering team doesn't know the underlying SLO
- After an incident, you want to calculate the cost in error budget terms

---

## Core Definitions

### SLI — Service Level Indicator
A **quantitative measure** of some aspect of service behavior. An SLI is a ratio:

```
SLI = (good events / valid events) × 100%
```

An SLI is always a measurement, not a target.

**Examples:**
- Availability SLI: `successful HTTP responses (2xx/3xx) / total HTTP requests`
- Latency SLI: `requests completing in < 300ms / total requests`
- Error rate SLI: `non-5xx responses / total responses`
- Throughput SLI: `tasks processed / tasks submitted`

### SLO — Service Level Objective
The **target value** for an SLI over a rolling time window.

```
SLO = "SLI must be ≥ X% over a rolling Y-day window"
```

An SLO is an internal engineering target. It is the signal for whether the service is healthy enough to keep shipping.

**Examples:**
- "99.9% of requests return a 2xx/3xx response over a rolling 28-day window"
- "p99 latency < 500ms for 95% of requests over a rolling 28-day window"
- "Payment processing success rate ≥ 99.95% over a rolling 7-day window"

### SLA — Service Level Agreement
A **contractual commitment** to a customer, typically with financial penalties for breach. An SLA is always set **lower** (looser) than the SLO, so that engineering has room to react before the contract is breached.

```
SLA ≤ SLO (always)
```

**Example:**
- SLO: 99.9% availability (internal target)
- SLA: 99.5% availability (customer contract — with credits if breached)

### The Hierarchy
```
SLI  →  measured value   (what is actually happening)
SLO  →  internal target  (what engineering is responsible for)
SLA  →  external promise (what you've contractually committed to customers)
```

---

## Error Budget

### What Is an Error Budget?

An error budget is the amount of unreliability you are **allowed** to have while still meeting your SLO. It is the mathematical complement of the SLO:

```
Error budget = 100% − SLO target
```

**Examples:**
| SLO | Error budget |
|---|---|
| 99.9% | 0.1% = 43.8 min/month |
| 99.95% | 0.05% = 21.9 min/month |
| 99.99% | 0.01% = 4.4 min/month |
| 99.5% | 0.5% = 3.65 hours/month |

### Error Budget Calculation Worksheet

```
INPUTS
------
SLO target:           ___% (e.g., 99.9)
Measurement window:   ___ days (typically 28 or 30)

DERIVED VALUES
--------------
Error budget %:       100 - SLO = ___%
Total minutes in window: ___ days × 24 hrs × 60 min = ___ min
Allowed downtime (min): Total minutes × (Error budget % / 100) = ___ min

CURRENT STATE
-------------
Bad minutes this window: ___ min (from monitoring system)
Remaining budget:         Allowed − Bad = ___ min
Budget consumed %:        (Bad / Allowed) × 100 = ___%

BURN RATE
---------
Burn rate = actual error rate / error budget rate
Example: SLO 99.9% → budget = 0.1%
  If actual error rate is 1.0%:
  Burn rate = 1.0% / 0.1% = 10× (burning 10× faster than allowed)

AT THIS RATE, BUDGET RUNS OUT IN:
  Remaining budget (minutes) / (burn rate × budget rate per minute)
```

### Alert Threshold Calculator (28-Day Budget)

For a 28-day SLO window:

```
Total error budget minutes = 28 × 24 × 60 × (1 - SLO)
                           = 40,320 × (1 - SLO)

Example: 99.9% SLO → 40,320 × 0.001 = 40.32 min budget

BURN RATE THRESHOLDS
--------------------
Burn rate  | Budget consumed in | Alert type
-----------|-------------------|------------------------
  1×       | 28 days           | (normal — no alert)
  2×       | 14 days           | Ticket / low-urgency
  5×       | 5.6 days          | Warning — slow burn
  10×      | 2.8 days          | Page / fast burn
  14.4×    | 1 hour (!)        | Critical — emergency

HOURLY BURN RATE (for real-time monitoring)
-------------------------------------------
Budget per hour = total budget minutes / (28 × 24)
               = total budget minutes / 672

Example: 99.9% SLO → 40.32 / 672 = 0.06 min/hour budget
If you're consuming 0.6 min/hour: burn rate = 10× → page
```

---

## Common SLIs by Service Type

### HTTP/REST API
| SLI | Good event definition | Valid event |
|---|---|---|
| Availability | HTTP 2xx or 3xx | All requests |
| Latency | Response time < threshold (e.g., 300ms p99) | All requests |
| Error rate | Non-5xx response | All requests |

### gRPC Service
| SLI | Good event definition |
|---|---|
| Availability | Status code OK or NOT_FOUND or ALREADY_EXISTS |
| Latency | RPC completes within threshold |

### Asynchronous / Queue-Based
| SLI | Good event definition |
|---|---|
| Throughput | Messages processed successfully / messages received |
| Freshness | Message age at processing < threshold |
| Processing latency | Time from enqueue to processed < threshold |

### Data Pipeline
| SLI | Good event definition |
|---|---|
| Completeness | Records output / records expected |
| Freshness | Data age at query < threshold |
| Correctness | Records passing validation / records processed |

### Storage / Database
| SLI | Good event definition |
|---|---|
| Availability | Successful read/write / total operations |
| Durability | Data retrievable after acknowledged write |
| Latency | Read/write completes within threshold |

---

## Setting the Right SLO

### The Three Rules

1. **Use historical data as a baseline.** Your SLO should reflect what the service actually achieves, not a guess. Pull the last 90 days of data. If you're running at 99.93%, start your SLO at 99.9%.

2. **Set it tight enough to matter, loose enough to breathe.** An SLO of 99.0% for a payment API is meaningless. An SLO of 99.9999% for a blog is wasteful. Use user impact as the calibration: at what reliability level do users start noticing?

3. **Leave a gap between SLO and SLA.** The SLO is your internal warning system. The SLA is the customer contract. Never set them equal — you need headroom to react before breaching the SLA.

### SLO Setting Worksheet

```
SERVICE: _______________

STEP 1: Gather historical data
  90-day measured availability: ___%
  90-day p99 latency:           ___ ms

STEP 2: Define user impact threshold
  Users notice degradation at: ___%  or  ___ ms p99
  Users abandon / churn at:    ___%  or  ___ ms p99

STEP 3: Set initial SLO
  Availability SLO:   ___% (at or slightly below historical baseline)
  Latency SLO:        p___ < ___ ms (e.g., p99 < 300ms)

STEP 4: Calculate error budget
  Error budget:       ___ min/28 days (use worksheet above)

STEP 5: Pressure-test with product
  "Is this budget sufficient for the features we plan to ship?"
  "Does this target require heroics to maintain?"

STEP 6: Set SLA (if applicable)
  SLA = SLO − buffer
  Availability SLA:   ___% (e.g., SLO 99.9% → SLA 99.5%)

STEP 7: Schedule first review
  Review date:        ___ (recommended: 90 days from now)
```

---

## Burn Rate Alerting

### Why Standard Threshold Alerts Fail

Alerting on raw error rate (e.g., "alert if error rate > 1%") misses two scenarios:
- **Too slow**: A 0.5% error rate sustained for 10 days burns 50% of a 99.9% monthly budget — but never fires the alert
- **Too noisy**: A 2% error rate for 10 minutes burns < 0.3% of budget — and fires the alert

Burn rate alerting solves both problems.

### Multi-Window Multi-Burn-Rate Alerting

Use two windows per alert to balance sensitivity and specificity:

| Alert | Burn rate | Short window | Long window | Purpose |
|---|---|---|---|---|
| **Page (critical)** | 14.4× | 5 min | 1 hour | Budget gone in 1 hour |
| **Page (high)** | 6× | 30 min | 6 hours | Budget gone in ~4.7 days |
| **Ticket (warning)** | 3× | 6 hours | 3 days | Budget gone in ~9.3 days |
| **Track (info)** | 1× | 3 days | — | Burning at normal rate |

**Alert fires when BOTH windows exceed the burn rate threshold** — this prevents single-spike false positives.

### Prometheus / OpenSLO Alert Example

```yaml
# Fast burn — page immediately
- alert: ErrorBudgetFastBurn
  expr: |
    (
      job:slo_errors:rate5m{job="api"} / job:slo_budget_rate:rate5m{job="api"}
    ) > 14.4
    and
    (
      job:slo_errors:rate1h{job="api"} / job:slo_budget_rate:rate1h{job="api"}
    ) > 14.4
  labels:
    severity: critical
  annotations:
    summary: "Error budget burning at 14.4×+ — will exhaust in < 1 hour"

# Slow burn — ticket
- alert: ErrorBudgetSlowBurn
  expr: |
    (
      job:slo_errors:rate6h{job="api"} / job:slo_budget_rate:rate6h{job="api"}
    ) > 3
    and
    (
      job:slo_errors:rate3d{job="api"} / job:slo_budget_rate:rate3d{job="api"}
    ) > 3
  labels:
    severity: warning
  annotations:
    summary: "Error budget burning at 3×+ — will exhaust in < 9.3 days"
```

---

## SLO as Product/Engineering Negotiation Tool

SLOs make reliability trade-offs explicit. When product wants to ship fast and engineering is worried about stability, the error budget is the shared ledger.

### The Negotiation Framework

```
Current error budget remaining: ___%

IF budget > 50%:
  → Ship freely. Reliability is healthy.
  → Use some budget for risky experiments (feature flags, gradual rollout).

IF budget between 20–50%:
  → Ship with extra care. Add canary deploys and feature flags.
  → Fix reliability issues in parallel.

IF budget < 20%:
  → Freeze risky features. Reliability work takes priority.
  → Engineering and product agree on what counts as "risky."

IF budget exhausted:
  → Freeze all feature work until budget is restored.
  → Conduct a reliability sprint: reduce toil, fix flaky infra, add SLO coverage.
  → Revisit SLO — may be too tight.
```

### The "Ship or Freeze?" Error Budget Decision Guide

```
DECISION GATE — Should we ship this feature?

1. What is our remaining error budget?
   > 50%: Green — proceed
   20–50%: Yellow — proceed with mitigations (canary, flag, rollback plan)
   < 20%: Red — must justify or defer
   Exhausted: Stop — fix reliability first

2. What is the estimated blast radius of this change?
   No database migration, no config change, no new external call: LOW
   Database migration or new external dependency: MEDIUM
   Architecture change, new critical path: HIGH

3. Does the change have a rollback plan?
   Instant rollback (feature flag, no migration): subtract risk
   Requires migration reversal: add risk

4. Is monitoring in place for this change?
   Yes, with alerting: subtract risk
   No: add risk

VERDICT:
  Green budget + Low blast radius = Ship
  Yellow budget + Low blast radius = Ship with canary
  Yellow budget + High blast radius = Defer or add mitigations
  Red budget + any = Defer (feature) or Emergency fix (reliability)
  Exhausted + any = Reliability sprint first
```

---

## SLA Breach: Consequences and Escalation

### When an SLA Is At Risk

1. **Detect early**: Set an SLO alert at 80% budget consumed — this gives time to act before the SLA is breached
2. **Escalate to on-call manager and customer success immediately**
3. **Prepare customer communication** before the breach (not after)
4. **Document the incident timeline** — breach SLAs almost always require a post-mortem report to the customer

### SLA Breach Escalation Path

```
Budget < 20% remaining
  → Engineering manager + SRE lead notified
  → Feature freeze enacted
  → Customer Success pre-alerted ("monitoring an elevated situation")

SLA at risk (< 5% remaining or incident in progress)
  → Engineering VP engaged
  → Customer Success drafts proactive communication
  → War room convened for services with revenue-linked SLAs

SLA breached
  → Customer Success contacts affected customers
  → Engineering provides hourly status updates
  → Post-mortem scheduled within 5 business days
  → Credits calculated per SLA contract terms
  → Root cause communicated to customer within agreed timeline
```

---

## SLO Review Template

Run quarterly (or after any major incident that consumed >20% of budget).

```
SLO QUARTERLY REVIEW
=====================
Service:       _______________
Period:        _______________
Reviewer:      _______________

PERFORMANCE SUMMARY
-------------------
SLO target:                      ___%
Measured SLI (period average):   ___%
Error budget consumed this period: ___%
Error budget remaining:           ___%

INCIDENTS CONSUMING BUDGET
---------------------------
Date | Duration | Budget consumed | Root cause
-----|----------|----------------|------------
     |          |                |
     |          |                |

TRENDS
------
SLI trend (vs. last quarter): ↑ improving / ↓ degrading / → stable
Budget burn trend:             ↑ faster / ↓ slower / → stable

SLO CALIBRATION
---------------
Was the SLO achievable without heroics?   Y / N
Was the SLO tight enough to signal real problems?  Y / N
Should the SLO be tightened?  Y / N  If yes, new target: ___%
Should the SLO be loosened?   Y / N  If yes, new target: ___%

ACTIONS
-------
[ ] Fix: [reliability improvement with owner and date]
[ ] Alert tuning: [false positives or missed alerts to address]
[ ] SLO update: [if target is changing, update runbook and dashboards]

NEXT REVIEW DATE: _______________
```

---

## Output Format

When applying this skill, the agent should:

1. **Clarify the tier**: Ask whether the user needs SLI definition, SLO target-setting, error budget calculation, alerting setup, or SLA review — these are distinct problems.
2. **Calculate concretely**: When given an SLO target and window, calculate error budget in minutes/hours. Show the arithmetic.
3. **Generate burn rate alert thresholds**: Provide the 14.4×, 6×, 3× values for the specific SLO.
4. **Produce templates on request**: SLO review, decision guide, SLA breach escalation path.
5. **Flag misconfigurations**: SLA tighter than SLO, SLO set at 100% (impossible), no burn rate alerting, single-window alerts.
6. Format calculations as code blocks with labeled inputs/outputs. Format checklists as Markdown task lists.

---

## References

- Beyer, Jones, Petoff, Murphy — *Site Reliability Engineering* (Google), chapters 4 (SLOs), 5 (Eliminating Toil), 6 (Monitoring)
- Beyer, Murphy, Rensin, Kawahara, Thorne — *The Site Reliability Workbook* (Google), Chapter 2 (SLOs in Practice)
- Alex Hidalgo — *Implementing Service Level Objectives* (O'Reilly, 2020)
- Google SRE — ["The Calculus of Service Availability"](https://sre.google/workbook/alerting-on-slos/) (sre.google)
- LeadDev — ["How to set meaningful SLOs"](https://leaddev.com/monitoring-observability)
- OpenSLO — [openslo.com](https://openslo.com) (vendor-neutral SLO specification)
- Sloth — [sloth.dev](https://sloth.dev) (SLO generator for Prometheus)
