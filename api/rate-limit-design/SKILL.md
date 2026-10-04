---
name: rate-limit-design
description: Design backend API rate limits, quotas, throttling, and abuse controls. Use when Codex is asked to define limits by user, tenant, token, IP, endpoint, plan, or workload, including headers, errors, retries, and operational monitoring.
license: MIT
---

# Rate Limit Design

## Core Workflow

1. Identify protected resources, abuse cases, client types, tenants, plans,
   expected traffic, and operational constraints.
2. Choose limit dimensions: user, tenant, token, IP, endpoint, method, workload,
   or account plan.
3. Define algorithm and policy: fixed window, sliding window, token bucket,
   concurrency limit, quota, or adaptive control.
4. Specify response headers, error contract, retry guidance, burst behavior,
   exemptions, and monitoring.
5. Include rollout, tuning, and support override procedures.
6. Add tests for allowed, limited, burst, and recovery behavior.

## Safety Rules

- Do not invent production traffic, plan limits, or customer entitlements.
- Do not recommend limits that could silently block critical customer workflows
  without monitoring and support path.
- Escalate rate limits affecting billing, SLAs, compliance, security, or
  customer commitments.

## Deliverable Shape

For rate-limit plans, provide:

- Protected resources and abuse cases
- Limit dimensions and policy
- Headers and error behavior
- Retry and burst guidance
- Monitoring and alerting
- Rollout and tuning plan
- Support override path
- Test cases

## References

- Read `references/rate-limit-design-checklist.md` when designing or reviewing
  API rate limits.
