---
name: sre-practices
description: Site Reliability Engineering practices from Google - the company that invented SRE. Master SLOs, error budgets, incident response, and toil elimination. Use when designing reliable systems, implementing SRE practices, or improving operational excellence. Learn from the team that runs Google Search, Gmail, and YouTube at billions of users scale.
expert_level: 10/10
source_company: Google SRE
specialist: google-sre-devops
related:
  - kubernetes-expert
  - observability
  - chaos-engineering
---

# SRE Practices - Google Site Reliability Engineering

**Expert**: Alex Kim (Google SRE, 11 years)
**Level**: 10/10 - Google invented SRE

## Overview

Site Reliability Engineering from Google - what happens when you ask a software engineer to design an operations team. Not traditional ops or DevOps - applying software engineering to infrastructure.

Google runs services for billions (Search, Gmail, YouTube, Maps) with 99.99%+ uptime. These practices made that possible.

## Core SRE Principles

### 1. Embrace Risk
100% uptime is the wrong target. Use **error budgets** to balance reliability vs velocity.



### 2. Service Level Objectives (SLOs)
Define and measure service quality with SLIs, SLOs, SLAs.



### 3. Eliminate Toil
Automate manual, repetitive work. Target <50% time on toil.



### 4. Monitoring & Alerting
Alert on symptoms (user-facing), not causes. Use golden signals.



### 5. Incident Response
Blameless postmortems, clear escalation, reduce MTTR.



### 6. Capacity Planning
Plan for growth, forecast demand, optimize resource usage.



## SRE Workflow

1. **Define SLOs** - What reliability do users need?
2. **Measure SLIs** - Track service quality metrics
3. **Monitor error budget** - How much budget consumed?
4. **Respond to incidents** - Restore service quickly
5. **Conduct postmortems** - Learn from failures
6. **Automate toil** - Reduce manual work
7. **Plan capacity** - Scale for growth

## Google's Production Scale

SRE practices power:
- **Google Search**: 8.5 billion searches/day
- **Gmail**: 1.8 billion users
- **YouTube**: 2 billion users, 1 billion hours/day
- **Google Maps**: 1 billion users
- **99.99%+ uptime** across all services

## Golden Signals (Google's 4 Key Metrics)

1. **Latency** - Time to serve requests
2. **Traffic** - Demand on system
3. **Errors** - Failed requests
4. **Saturation** - Resource utilization



## Best Practices

1. SLOs over SLAs - Internal targets stricter than external
2. Error budget policy - Define consequences when budget exhausted
3. Blameless culture - Learn from failures, don't blame
4. Toil automation - Invest in eliminating repetitive work
5. On-call sustainability - Max 25% on-call time, 50% ticket time

## Related Skills

- **[kubernetes-expert](../kubernetes-expert/SKILL.md)** - Infrastructure platform
- **[observability](../observability/SKILL.md)** - Monitoring & tracing
- **[chaos-engineering](../chaos-engineering/SKILL.md)** - Resilience testing

---

**Last Updated**: 2026-02-03
**Expert**: Alex Kim (Google SRE, 11 years) - Runs billion-user services
