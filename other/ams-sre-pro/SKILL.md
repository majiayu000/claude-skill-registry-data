---
name: sre-pro
description: Site reliability engineering — SLIs/SLOs, error budgets, and reliability practices — use when making systems reliable at scale.
category: operations
---

## Overview

SRE applies engineering discipline to operations: define reliability in
measurable terms, automate the toil away, and make deliberate trade-offs
between shipping speed and stability. This skill covers the core SRE
framework — SLIs, SLOs, error budgets — and the practices that sustain
reliability as systems grow.

## When to use

- Defining SLIs (indicators) and SLOs (objectives) for a service
- Setting up error budgets and the policies they drive
- Reducing operational toil through automation
- Designing for reliability: redundancy, graceful degradation, capacity
- Building an SRE practice or reliability review process on a team

## Core concepts

**SLIs measure, SLOs promise, SLAs contract.** A Service Level Indicator is a
quantified metric (99th-percentile latency, successful-request ratio).
The Objective is the target (99.9% of requests succeed over 30 days). The
Agreement adds business consequences. Most teams need SLIs + SLOs; SLAs only
where contracts demand them.

**Error budgets make reliability a resource.** 99.9% SLO = 0.1% budget for
failure (~43 min/month). Spend it on releases and experiments; when it's
exhausted, freeze non-essential changes until reliability recovers. This turns
"move fast vs be stable" from an argument into arithmetic.

**Toil is the enemy.** Toil = manual, repetitive, automatable operational work
with no enduring value. Track it (aim for <50% of on-call time, trending
down); every toil task is a candidate for automation or elimination. Toil that
grows with traffic is a scaling bug.

**Design for failure.** Redundancy across zones, graceful degradation (serve
stale cache rather than error), timeouts and retries with backoff and
jitter, bulkheads and circuit breakers to contain cascading failures, and
load shedding under extreme pressure. Reliability is a property of the
architecture, not of hope.

**Blameless culture.** Postmortems focus on systemic causes, never individual
fault. People don't cause outages; systems that allow human error to become
outages do. Psychological safety is a reliability control.

## Practical workflow

1. **Choose SLIs from the user's perspective:** availability (successful
   responses / valid requests), latency (p50/p99 of successful requests),
   and domain-specific ones (freshness, correctness, durability) — 2–4 per
   service, not 20.
2. **Set SLOs deliberately:** start slightly below current performance
   (achievable, not aspirational), with a 28–30 day rolling window;
   multi-window burn-rate alerting (fast-burn page, slow-burn ticket).
3. **Implement the error budget policy:** define what happens at 50%, 100%,
   and sustained exhaustion (feature freeze, reliability sprint); get
   leadership sign-off so it's enforceable.
4. **Instrument everything:** the "four golden signals" (latency, traffic,
   errors, saturation) per service, plus business-level indicators; dashboards
   that a new on-call can read at 3am.
5. **Attack toil systematically:** list recurring manual tasks, estimate
   hours/quarter, automate the highest-cost ones first; measure toil
   percentage over time.
6. **Run blameless postmortems** for every significant incident: timeline,
   contributing factors, action items with owners and deadlines — and track
   action-item completion as a reliability metric.

## Common pitfalls

- **Too many SLIs/SLOs** — 15 objectives nobody looks at; a few meaningful
  ones beat comprehensive-but-ignored.
- **SLOs nobody enforces** — an error budget without a freeze policy is
  theater; get the policy agreed before the first exhaustion.
- **Alerting on symptoms instead of burn rate** — pages on CPU spikes while
  users are fine (or silence while the budget burns); alert on SLI burn.
- **Aspirational SLOs** (five nines on a best-effort service) — unachievable
  targets teach the team to ignore SLOs entirely.
- **Toil normalized as "just ops work"** — manual deploys, ticket-driven
  routine changes, and hand-run runbooks that never get automated compound
  until the team drowns.
- **Skipping postmortems for "small" incidents** — patterns hide in the small
  ones; the discipline matters more than the severity threshold.
