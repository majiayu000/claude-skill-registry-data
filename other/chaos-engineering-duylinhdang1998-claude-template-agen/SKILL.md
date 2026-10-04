---
name: chaos-engineering
description: Chaos Engineering expertise from Netflix - the company that invented Chaos Monkey. Build resilient systems through controlled failure injection. Use when implementing resilience testing, chaos experiments, or building fault-tolerant systems. Learn from the pioneers of chaos engineering.
expert_level: 10/10
source_company: Netflix
specialist: netflix-backend-architect
requires:
  - microservices
  - observability
related:
  - sre-practices
  - kubernetes-expert
  - aws-expert
---

# Chaos Engineering - Netflix Chaos Monkey Expertise

**Expert**: Marcus Johnson (Netflix, 14 years)
**Level**: 10/10 - Netflix invented Chaos Engineering

## Overview

Chaos Engineering from Netflix - created Chaos Monkey and pioneered failure testing in production. Learn how Netflix achieves 99.999% uptime by intentionally breaking systems.

## Why Netflix Created Chaos Engineering (2010)

**The Problem:**
- Migrating from monolith to cloud microservices
- Hundreds of services with complex dependencies
- Traditional testing didn't catch production failures
- "Works in dev" ≠ "Works at scale in production"

**The Solution: Chaos Monkey (2011)**
- Randomly terminate EC2 instances in production
- Force engineers to build resilient services
- Discover weaknesses before customers do
- Cultural shift: Assume everything fails

## Core Principles

1. **Define steady state** - Normal system behavior
2. **Hypothesize** - Predict system response to failures
3. **Inject chaos** - Controlled blast radius
4. **Measure and learn** - Track impact, improve resilience

## Chaos Experiments Workflow

1. **Measure baseline** - Capture normal metrics
2. **Define hypothesis** - "IF failure X, THEN system remains stable BECAUSE Y"
3. **Set abort conditions** - Safety thresholds
4. **Inject failure** - Start small (1% instances)
5. **Observe impact** - Monitor metrics
6. **Analyze results** - Did hypothesis hold?
7. **Improve resilience** - Fix weaknesses found

## Netflix Simian Army Tools

- **Chaos Monkey** - Terminate random instances in production
- **Latency Monkey** - Inject artificial delays into services
- **Chaos Kong** - Simulate entire AWS region failure

## Building Resilience (Netflix Patterns)

1. **Redundancy** - Multiple instances, multi-AZ, multi-region
2. **Graceful degradation** - Fallbacks for failures
3. **Circuit breakers** - Stop cascading failures
4. **Auto-healing** - Kubernetes restarts failed pods

## Netflix's Chaos Maturity Model

**Level 1**: Ad-hoc manual testing
**Level 2**: Scheduled chaos experiments (GameDays)
**Level 3**: Automated chaos in pre-prod
**Level 4**: Continuous chaos in production ← Netflix is here
**Level 5**: Chaos as a service for all teams

## Best Practices

1. Start small - 1% instances, single service, dev/staging first
2. Define success criteria - Measurable steady state metrics
3. Automate everything - Execution, metrics, rollback
4. Learn and improve - Document findings, fix weaknesses

## Related Skills

- **[microservices](../microservices/SKILL.md)** - Resilient architecture
- **[sre-practices](../sre-practices/SKILL.md)** - Reliability engineering
- **[kubernetes-expert](../kubernetes-expert/SKILL.md)** - Container resilience
- **[observability](../observability/SKILL.md)** - Measure chaos impact

---

**Last Updated**: 2026-02-03
**Expert**: Marcus Johnson (Netflix, 14 years) - 99.999% uptime at 260M+ subscribers
