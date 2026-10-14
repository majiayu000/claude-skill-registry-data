---
name: rate-limiting
description: "Rate limiting: per-user/IP/API-key quotas, cost caps, expensive-computation guards. Return 429 with clear contracts."
---

# rate-limiting

Price every endpoint in requests: quota it, cap its cost, and say no with 429.

## Activate when

- Public/partner APIs, auth endpoints, expensive operations (exports, AI calls, reports), webhooks.

## Do NOT activate for

- Internal backpressure between services (see distributed/systems, backend/concurrency).

## Inspection

Rank endpoints by cost × abuse potential; find current limits (or their absence) and what breaks first under load.

## Decision rules

- Key by the abuse unit: authenticated user, API key, or IP (behind proxies, use the verified client identity, not spoofable headers).
- Tier: strict on auth/login (slow down credential stuffing), proportional on expensive endpoints, generous on cheap reads.
- Algorithm: token bucket for bursty humans, fixed/sliding window for hard quotas; distributed state in Redis, not in-process memory.
- Contract: `429` with `Retry-After`, documented quotas, upgrade path — never silent drops or confusing 403s.

## Procedure

1. Set quotas per tier + global cost caps; implement with tests for burst, sustained, and multi-key abuse.
2. Prove expensive endpoints degrade (queue/shed) instead of dying.
3. Verify: limit tests green (allowed/blocked/headers), abuse simulation sheds gracefully, legitimate burst traffic unaffected.

## Failure modes

- IP-keying behind NAT/proxies punishing innocents; in-memory limits per replica; no headers so clients hammer blindly; limits nobody monitors.

## Escalation

Abuse beyond rate control (fraud, scraping rings) → product-level defenses; infra edge (WAF/CDN) via cloud/*.

## References

- Related: `../api-security/`, `../caching/`, `../../security/secure-baseline/`.
