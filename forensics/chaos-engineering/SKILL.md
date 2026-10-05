---
name: chaos-engineering
description: Use when verifying a system's resilience by injecting controlled failure. Covers hypothesis-driven experiments, blast-radius control, failure injection techniques, and running game days safely.
metadata:
  category: devops
  version: 1.0.0
  tags: [chaos, resilience, testing, failure-injection, game-day]
---

# Chaos Engineering

## Purpose

Find out whether your resilience mechanisms work before an outage tests them for you. Every fallback, retry, and circuit breaker is a hypothesis until it has been exercised under real failure.

## When to Use

- Verifying that a documented failover, fallback, or degradation path actually works.
- Before a high-stakes event where the system must hold.
- After adding resilience mechanisms — to confirm they do what you think.
- Building confidence in a system nobody fully understands.

## Capabilities

- Hypothesis-driven experiment design.
- Failure injection: latency, errors, resource exhaustion, instance termination, network partition, dependency unavailability.
- Blast-radius control and automatic abort.
- Game-day facilitation.

## Inputs

- The steady-state metric that defines "working" (error rate, latency, throughput).
- The resilience mechanism being tested and what it is meant to do.
- The blast radius you are willing to accept and the abort criteria.

## Outputs

- A finding: the mechanism works, or it does not, with evidence.
- Fixes for the mechanisms that did not.
- A repeatable experiment that runs regularly.

## Workflow

1. **Define steady state** — A measurable metric that says the system is healthy right now. Without it, you cannot tell whether the experiment broke anything.
2. **Form a hypothesis** — "When the pricing service returns 500s, checkout will serve cached prices and the checkout success rate will stay above 99%." Falsifiable, specific, and about a mechanism you believe exists.
3. **Bound the blast radius** — Start with one instance, one percent of traffic, or a staging environment carrying production-shaped load. Never start in production at full scale.
4. **Define the abort criteria first** — And automate the abort. "We'll stop it if it looks bad" is not a control.
5. **Inject the failure and observe** — Watch the steady-state metric and the mechanism you are testing. Does the fallback fire? Does the circuit open? Does the alert page?
6. **Fix what you found, then widen** — Increase the blast radius only after the previous scope passes.

## Best Practices

- The purpose is to falsify a belief, not to break things. An experiment with no hypothesis is just an outage you caused.
- Announce the first experiments. Unannounced chaos in a team that has not built the mechanisms yet is destructive and erodes trust in the practice.
- Do not run chaos experiments during an incident, a freeze, or a peak-traffic event. The point is to learn safely.
- Test the failure you actually fear. Terminating a stateless pod proves little; making a dependency slow (rather than down) tests timeouts, which is where systems actually break.
- Slow is worse than down. A dependency that returns in 30 seconds instead of failing fast will exhaust your connection pool. Inject latency, not just errors.
- Automate the successful experiments so they run continuously. A one-off game day proves the system worked in March.

## Examples

**A well-formed experiment:**

```yaml
experiment: pricing-service-unavailable

steady_state:
  metric: checkout_success_rate
  threshold: "> 99%"
  measured_over: 5m

hypothesis: >
  When the pricing service returns 503 for all requests, checkout serves
  cached prices from Redis and the checkout success rate remains above 99%.
  The pricing circuit breaker opens within 30 seconds, and a warning (not a
  page) is emitted.

blast_radius:
  environment: production
  scope: 5% of traffic, single availability zone
  duration: 10m

abort_if:
  - checkout_success_rate < 98%      # automatic; no discussion
  - p99_checkout_latency > 3s
  - any SEV-2 or higher declared

injection:
  tool: fault-injection-proxy
  target: pricing-service
  fault: { type: error, status: 503, percentage: 100 }
```

**The finding this experiment actually produced:**

```text
Result: HYPOTHESIS FALSIFIED.

The cache fallback worked. The circuit breaker did not open — it was
configured to trip on connection errors, and a 503 is a successful
connection with an error status. Checkout latency rose from 180ms to
2.9s because every request waited for the full 3s pricing timeout before
falling back.

Success rate stayed at 99.4% (the hypothesis' headline claim held), so a
naive pass/fail on the steady-state metric alone would have reported
success and left a latent latency bomb in place.

Fix: trip the breaker on 5xx as well as connection failure; reduce the
pricing timeout from 3s to 400ms, which is above p99.9 for that call.
```

## Notes

- The experiment above is the archetype: the headline metric held, and the system was still broken. Always observe the *mechanism*, not just the outcome.
- Injecting latency is more informative than injecting failure, because most systems handle a fast failure and collapse under a slow one.
- Chaos engineering in an organization without runbooks, alerting, or a rollback path is premature. Build the mechanisms first; then verify them.
