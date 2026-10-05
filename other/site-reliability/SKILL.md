---
name: site-reliability
description: Use when establishing reliability practice. Covers SLOs and error budgets, capacity planning, graceful degradation, load shedding, retry and timeout policy, and the arithmetic of availability.
metadata:
  category: devops
  version: 1.0.0
  tags: [sre, slo, reliability, resilience, capacity]
---

# Site Reliability

## Purpose

Make reliability a measured, budgeted property rather than an aspiration. Perfect availability is neither achievable nor desirable — the goal is to be exactly as reliable as the product requires, and to spend the remaining budget on shipping.

## When to Use

- Defining SLOs and an error-budget policy.
- Designing a system's behavior under overload or dependency failure.
- Capacity planning ahead of a known load event.
- Setting retry and timeout policy across services.

## Capabilities

- SLI selection, SLO definition, and error-budget policy.
- Availability arithmetic across dependency chains.
- Graceful degradation and load shedding.
- Retry, timeout, and circuit-breaker configuration.
- Capacity planning and load testing.

## Inputs

- The user-facing operations that matter, ranked.
- Current reliability, measured — not assumed.
- Dependency availability, including third parties.

## Outputs

- SLOs with an error budget and an agreed policy for exhausting it.
- Defined degraded behavior for each dependency failure.
- Timeout and retry budgets that do not amplify an outage.

## Workflow

1. **Pick SLIs the user would recognize** — Request success rate and latency for the operations that matter. Not internal metrics.
2. **Set the SLO from the business need** — 99.9% is 43 minutes of downtime per month. 99.99% is 4 minutes, and costs roughly ten times as much to achieve. Choose knowingly.
3. **Do the dependency arithmetic** — A service depending synchronously on four services, each at 99.9%, has a ceiling of 99.6%. If your SLO is higher than your dependency chain permits, the design must change, not the target.
4. **Design the degradation** — For each dependency: what does the user see when it is down? Serve stale, serve partial, or fail fast with a clear message. Decide in advance.
5. **Bound the retries** — A retry budget, not unlimited retries. Retries during a partial outage are what turn it into a total one.
6. **Shed load deliberately** — Under overload, reject the excess at the edge, cheaply. A system that accepts everything and times out serves nobody.

## Best Practices

- An error budget that is never spent means the SLO is too lax or the team is too cautious. A budget consistently exhausted means the SLO is too strict or reliability work is being deferred.
- Retries multiply load precisely when the system is least able to handle it. Cap them, back off exponentially with jitter, and stop entirely when the error rate is high (a retry budget).
- A timeout longer than the caller's timeout is useless work. Timeouts must decrease as you go down the call stack.
- Load shedding at the edge, based on a queue-depth or latency signal, protects the system's ability to serve *some* requests. Without it, overload degrades to serving none.
- Test the degraded path. A fallback that has never run is a fallback that does not work.
- Every third-party dependency in the critical path caps your availability at theirs. Either make it non-critical or accept its number.

## Examples

**Availability arithmetic, done before the SLO is promised:**

```text
Checkout depends synchronously on:
  auth        99.95%
  inventory   99.9%
  pricing     99.9%
  payments    99.9%   (third party, contractual)

Serial availability = 0.9995 x 0.999 x 0.999 x 0.999 = 99.65%
Maximum achievable checkout SLO: 99.65%  (~2.5 hours downtime/month)

A 99.9% checkout SLO is therefore unachievable with this design.
Options:
  1. Make pricing non-critical: cache prices, serve the last known good
     on failure.  -> removes 0.1%
  2. Make inventory non-critical: accept the order, verify asynchronously,
     cancel with an apology on the rare failure. -> removes 0.1%
  3. Accept 99.6% and stop promising 99.9%.

Chosen: (1) and (3). Inventory remains critical because overselling is
worse than a failed checkout.
```

**Retry budget that refuses to amplify an outage:**

```python
class RetryBudget:
    """Allow retries only while they are a small fraction of total traffic.

    During a broad outage every request fails, so an unbudgeted retry policy
    triples the load on an already-failing dependency. The budget stops that.
    """

    def __init__(self, ratio: float = 0.1, window: timedelta = timedelta(seconds=10)):
        self.ratio = ratio
        self.requests = SlidingWindowCounter(window)
        self.retries = SlidingWindowCounter(window)

    def allow_retry(self) -> bool:
        total = self.requests.count()
        if total < 20:                       # too little data; permit
            return True
        return self.retries.count() < total * self.ratio
```

## Notes

- The single most effective reliability change in most systems is setting a timeout on an outbound call that currently has none. An unbounded call ties up a thread or a connection until the process is exhausted.
- Circuit breakers need a defined open behavior. "Fail fast" is a decision; so is "serve stale". "Undefined" is not.
- Error-budget policies work only if the organization honors them. If reliability work is never prioritized when the budget is exhausted, the SLO is decoration.
