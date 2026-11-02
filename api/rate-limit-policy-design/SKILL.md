---
name: rate-limit-policy-design
description: Design rate limits using identity scope, burst behavior, distributed enforcement, and actionable retry responses.
---

# Rate Limit Policy Design

## Goal

Protect services from overload and abusive usage without surprising legitimate multi-device or multi-tenant clients.

## Inputs to inspect

API operations, identity model, service capacity, traffic profile, abuse patterns, and retry/client behavior.

## Workflow

1. Choose rate-limit dimensions by operation: user, tenant, API key, IP, resource, or global service; consider NAT and shared identities.
2. Set steady-state quota, burst allowance, and cost weights using capacity evidence instead of one arbitrary request count for every route.
3. Select an enforcement algorithm and consistency level that match deployment topology; define behavior when the rate-limit store is unavailable.
4. Return consistent status and retry metadata, while ensuring clients do not synchronize into retry storms; define exemptions with ownership and expiry.
5. Load-test legitimate peaks, abusive bursts, distributed clients, identity changes, clock skew, and backend outage; review false positives and bypasses.

## Validation checklist

- [ ] Quota scopes are explicit and do not accidentally let one tenant consume everyone else's allowance.
- [ ] High-cost endpoints can have stricter budgets than inexpensive reads.
- [ ] Retry metadata matches actual enforcement reset behavior.
- [ ] Distributed deployment semantics are tested, including store failure.
- [ ] Exemptions are observable, time-bounded, and do not become hidden bypasses.

## Required output

Deliver a rate-limit matrix, algorithm choice, response contract, capacity/load test plan, and override policy.

## Boundaries and failure handling

Do not use IP-only throttling for all identity-sensitive endpoints; do not return exact sensitive policy details that make trivial abuse easier.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
