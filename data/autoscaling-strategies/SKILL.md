---
name: autoscaling-strategies
description: "Every autoscaling decision is driven by one of three trigger types, and mature"
---

# Autoscaling Strategies (Verbose)

## Core Patterns

### The Three Trigger Types

Every autoscaling decision is driven by one of three trigger types, and mature
systems layer them rather than choosing one.

**Reactive** watches a live metric and acts when it crosses a threshold. It is
never wrong about the present, but it is structurally late: by the time the metric
has risen, load already exists, and new capacity still has to boot. Reactive
scaling alone always serves the leading edge of a spike from an undersized fleet.

**Scheduled** changes capacity on a clock or calendar — scale up at the start of
business hours, before a known sale, ahead of a batch window. When the pattern is
genuinely periodic it has zero lag, because provisioning happens before demand.
Its failure mode is the unexpected: it does nothing for a spike that isn't on the
calendar.

**Predictive** forecasts near-future load from historical patterns and provisions
ahead of it. It can hide cold-start latency entirely when the forecast is good.
When the forecast is wrong — a novel traffic shape, an incident, a viral event —
it commits capacity in the wrong direction and needs a reactive layer to recover.

The robust design is a **scheduled or predictive baseline** that absorbs the known
shape of demand, with a **reactive layer** on top as the safety net for everything
the baseline didn't anticipate.

### Choosing the Scaling Signal

The single most common autoscaling mistake is scaling on CPU because it is the
default, not because it represents the workload.

| Workload | Signal that tracks load | Why CPU misleads |
|---|---|---|
| HTTP API | Requests/sec or in-flight concurrency | I/O-bound work saturates latency well before CPU |
| Queue consumer | Queue depth, backlog per consumer, oldest-message age | A backlogged worker can be near-idle on CPU |
| Latency-critical tier | Primary signal + p95 latency guardrail | CPU rises after latency has already degraded |
| Batch/compute | CPU or GPU utilization | Genuinely CPU-bound — here CPU is correct |

For a queue, the useful signal is not "how busy is a worker" but "how far behind
are we." Backlog per consumer — messages waiting divided by consumers — directly
expresses whether adding workers will help. Scaling a queue tier on CPU can leave
a million-message backlog while every worker reports 20% CPU, because the
bottleneck is downstream I/O, not compute.

Whatever the signal, target the thing users feel. A guardrail metric (latency,
error rate) can trigger scale-out even when the primary metric looks fine.

### Horizontal vs Vertical

**Horizontal (scale out/in)** adds or removes instances. It is the default for a
reason: capacity is nearly unbounded, one instance failing removes a fraction of
capacity rather than all of it, and adding an instance needs no restart of the
others. The precondition is that work can be spread — the instances are stateless
or keep their state in a shared store.

**Vertical (scale up/down)** moves to a larger or smaller instance. It is the
answer when the unit of work genuinely cannot be split — a stateful singleton, a
primary database, an in-memory index that must be whole — or when a per-instance
resource wall (memory, connection limits) is the actual constraint. It typically
requires a restart or failover and hits a hard ceiling at the largest instance
type.

Reach for vertical only when sharding is impossible; otherwise horizontal wins on
availability and headroom.

### Cold Start and Warm Pools

New capacity is not useful the instant it is requested. The gap includes instance
provisioning, image pull, runtime and JIT warm-up, cache population, and
connection-pool establishment. If this ramp is longer than the time it takes load
to climb, reactive scaling is always behind and the new instances finish warming
up after the spike has passed.

Mitigations, in rough order of cost:

- **A minimum floor / warm pool.** Never scale a latency-sensitive path to zero.
  Keep enough running capacity that scale-up adds to a warm base instead of
  building from nothing.
- **Pre-provisioning.** For scheduled or predicted peaks, add capacity *before*
  demand so the ramp completes during quiet time.
- **Provisioned/warm concurrency** for serverless functions on user-facing paths,
  trading standing cost for the elimination of per-invocation cold start.
- **Faster ramps.** Slim images, lazy heavy initialization, readiness probes that
  only pass once caches and pools are actually ready — so traffic isn't routed to
  an instance that will serve slow first requests.

### Damping the Control Loop

An autoscaler is a feedback controller, and an under-damped controller oscillates.
The classic pattern: load rises, scale out, load per instance drops, scale in,
load per instance rises again, scale out — flapping every few minutes. Each cycle
pays cold-start cost, churns connections, and can evict in-flight work.

The core fix is **asymmetry**: treat adding and removing capacity differently.
Scale out quickly and generously, because the cost of being under-provisioned is
dropped or slow requests. Scale in slowly and conservatively, because the cost of
being briefly over-provisioned is only money, and premature scale-in is what
starts the oscillation.

Concretely: a short (or zero) stabilization window on scale-out, a long one on
scale-in; a metric averaging window wide enough to ignore momentary spikes; and a
cooldown so the loop cannot react faster than new capacity can become useful. On
Kubernetes these knobs live in the HPA `behavior` block — see
`kubernetes-resource-management` for how utilization targets relate to pod
requests and how the stabilization windows are configured.

## Common Anti-Patterns

❌ **Scaling every service on CPU by default.**
✅ Scale on the signal that tracks the workload — RPS/concurrency for APIs, queue
depth for consumers; keep CPU only for genuinely compute-bound work.

❌ **Symmetric scale-out and scale-in.**
✅ Fast out, slow in. Aggressive scale-in is the usual root of flapping.

❌ **Scaling a latency-critical path to zero, then eating a cold start on every
burst.**
✅ Keep a warm floor; use provisioned concurrency where cold start is user-visible.

❌ **Chasing a periodic, predictable pattern purely reactively.**
✅ Add a scheduled or predictive baseline so provisioning leads demand.

❌ **Setting a `max` below real peak.** The autoscaler silently caps and requests
queue behind a fleet that looks "fully scaled."
✅ Bound `max` by real peak and real capacity, and alert when it is reached.

❌ **Predictive scaling with no reactive fallback.** A bad forecast then has
nothing to correct it.
✅ Always keep a reactive layer under any predictive or scheduled scheme.

❌ **Readiness that passes before caches/pools are warm.** Traffic routes to an
instance that serves slow or failing first requests.
✅ Gate readiness on actual warm-up completion.

## Autoscaling Checklist

- [ ] Scaling signal represents real load for each tier (not CPU by default)
- [ ] Queue workers scale on backlog/queue depth, not instance CPU
- [ ] Latency or error-rate guardrail can trigger scale-out independently
- [ ] Horizontal scaling used wherever work can be spread
- [ ] Vertical scaling reserved for unsplittable/stateful units
- [ ] Minimum replica floor or warm pool on latency-sensitive paths
- [ ] Cold-start time measured and compared against traffic ramp rate
- [ ] Known periodic patterns covered by schedule or forecast, not reaction alone
- [ ] Reactive fallback present under any predictive/scheduled scheme
- [ ] Scale-out fast, scale-in slow (asymmetric stabilization)
- [ ] Cooldown ≥ time for new capacity to become useful
- [ ] `max` bounded by real peak and capacity, with an alert when hit
- [ ] Readiness probe passes only after warm-up completes
