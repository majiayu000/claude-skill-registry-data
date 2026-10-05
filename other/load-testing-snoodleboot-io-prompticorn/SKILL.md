---
name: load-testing
description: "Most teams run one test — expected peak for ten minutes — and believe they have"
---

# Load Testing (Verbose)

## Core Patterns

### The Four Shapes, and What Only Each One Finds

Most teams run one test — expected peak for ten minutes — and believe they have
load tested. Each shape isolates a different failure mode, and the others stay
invisible until production finds them.

| Shape | Profile | Duration | Failure class it exposes |
|---|---|---|---|
| Load | Steady expected peak | 15–30 min | SLO conformance under normal traffic |
| Stress | Step ramp past peak until degradation | 30–60 min | The knee; behaviour past saturation |
| Soak | 60–80% of peak, held | 4–24 h | Memory leaks, fd exhaustion, pool leaks, log/disk growth, cache eviction storms |
| Spike | 1× → 10× in under 30 s, hold 2 min, drop | 10–15 min | Cold start, autoscale lag, connection storms, thundering herd on cache miss |

A leak of 4 MB/hour is invisible in a 20-minute run and takes down a pod in three
days. A ten-minute ramp to peak gives an autoscaler nine minutes of warning it
will never get when a push notification lands. The shape is not cosmetic — it
determines which bugs are reachable.

Spike tests also expose the *recovery* half of the curve, which is usually worse
than the spike: after the drop, retried requests and rebuilt caches keep the
system saturated long after offered load is normal.

### Open vs Closed Workload Models

This is the single most consequential choice in the harness, and the default in
most tools is the wrong one.

A **closed model** holds a fixed population of virtual users. Each sends a
request, waits for the response, thinks, sends again. Throughput is therefore
`users / (latency + think time)` — a feedback loop. When the server slows,
offered load automatically drops.

An **open model** holds arrival rate fixed. Requests arrive on a schedule
regardless of whether prior ones have returned. If the server slows, work piles
up, exactly as it does when real users hit refresh and upstream services retry.

```javascript
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  discardResponseBodies: true,
  scenarios: {
    ramp_arrival: {
      executor: 'ramping-arrival-rate',
      startRate: 200,
      timeUnit: '1s',
      preAllocatedVUs: 200,
      maxVUs: 3000,          // headroom, or the generator becomes the bottleneck
      stages: [
        { target: 200, duration: '3m' },   // warm-up, excluded from analysis
        { target: 800, duration: '5m' },
        { target: 1600, duration: '5m' },
        { target: 2400, duration: '5m' },
        { target: 3200, duration: '5m' },
      ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500', 'p(99)<1500'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/products?page=1');
  check(res, { 'status 200': (r) => r.status === 200 });
}
```

The closed-model failure is subtle and common: a team runs 500 VUs, sees stable
throughput and rising-but-bounded latency, and concludes the system degrades
gracefully. In production the same system collapses at the same load, because
real arrivals do not back off. The closed model measured a *self-throttling*
version of the workload that does not exist.

Use a closed model only when it matches reality — a fixed pool of worker
processes calling your service, or a batch job with bounded concurrency.

### Why Averages Lie

The mean is dominated by the bulk of fast requests and is nearly blind to the
tail that users actually notice.

| | Mean | p50 | p95 | p99 | max |
|---|---|---|---|---|---|
| Build A | 118 ms | 95 ms | 210 ms | 380 ms | 900 ms |
| Build B | 121 ms | 92 ms | 240 ms | 4,100 ms | 31 s |

Reported as an average, build B is a 3 ms regression. Reported honestly, build B
has a GC pause or a lock convoy and one request in a hundred takes four seconds.

Tail latency compounds with fan-out. If a page issues 40 backend calls and each
independently has a 1% chance of exceeding 4 s, then `1 - 0.99^40 ≈ 33%` of page
renders contain one. The p99 of a dependency becomes the p66 of the page.

Two aggregation errors to avoid:

- **Averaging percentiles.** The mean of twenty per-minute p95 values is not the
  p95 of the run. Merge histograms, or compute over the whole window.
- **Including the ramp.** Percentiles over a period where load was changing
  describe no particular load level.

### Warming Up

The first minute of any run measures initialisation, not steady state:

- JIT-compiled runtimes (JVM, .NET, V8) interpret bytecode until methods pass
  their compilation threshold — early requests can be 10–50× slower.
- Caches are empty, so hit rate starts at zero and climbs.
- Connection pools are cold; every early request pays TCP and TLS setup.
- Lazily-initialised singletons, ORM metadata, and class loading fire once.
- Autoscalers sit at minimum replica count.

Ramp for 2–5 minutes at low rate, confirm the system reached steady state (flat
p99, stable cache hit rate, stable RSS), then start the measurement window. In
k6, express this as a separate warm-up scenario with `startTime` on the measured
one, so the warm-up traffic never enters the reported metrics.

### Production-Like Data

Query plans are chosen from statistics, so behaviour changes with cardinality.

- A nested-loop join that is optimal for 1,000 rows becomes catastrophic at 10M
  when the planner still estimates low and the loop actually runs 10M times.
- An index that fits in `shared_buffers` at small scale spills to disk at large
  scale, converting memory reads into random IO.
- Uniform synthetic keys give a flat access distribution, so every cache looks
  effective. Real traffic is Zipfian: a small hot set plus a long cold tail. The
  cold tail is what causes cache misses and slow queries.

Match, at minimum: row counts within an order of magnitude, realistic key
skew, realistic value sizes (a 2 KB JSON blob behaves differently from `"x"`),
and the same indexes. Feed a parameter corpus rather than one hardcoded id:

```javascript
import { SharedArray } from 'k6/data';

// Init context: parsed once, shared across all VUs
const skus = new SharedArray('skus', () => JSON.parse(open('./skus.json')));

export default function () {
  const sku = skus[Math.floor(Math.random() * skus.length)];
  http.get(`https://api.example.com/products/${sku}`, {
    tags: { name: 'GET /products/:sku' },   // group dynamic paths
  });
}
```

### Finding the Knee

The goal of a stress test is a curve, not a verdict. Step the arrival rate and
record, at each step, throughput, p50/p95/p99, error rate, and saturation
signals from the system under test.

| Offered req/s | Completed req/s | p99 | Errors | DB pool wait |
|---|---|---|---|---|
| 800 | 800 | 190 ms | 0.0% | 0 ms |
| 1,600 | 1,598 | 240 ms | 0.0% | 1 ms |
| 2,400 | 2,390 | 410 ms | 0.1% | 22 ms |
| 2,900 | 2,860 | 830 ms | 0.4% | 140 ms |
| 3,200 | 3,050 | 2,600 ms | 3.1% | 610 ms |
| 3,600 | 2,700 | 9,400 ms | 14% | 2,400 ms |

Three things are readable here and none of them is pass/fail. The knee is near
2,900. Past 3,200, completed throughput *falls* while offered load rises — the
signature of retry amplification and timeout waste. And pool wait time tracks p99
almost exactly, which names the bottleneck: the connection pool, not CPU.

That last column is the point. Latency alone tells you it broke; resource
telemetry tells you what to fix. Always collect CPU, memory, GC pause, pool
utilisation and queue depth alongside the client-side numbers. See
`performance-optimization` for what to do once the bottleneck is named.

### Not Measuring Your Own Load Generator

A load generator that is itself saturated silently under-delivers and adds its
own latency to every sample. Before trusting any run, confirm:

- Generator CPU below ~70% and no run-queue backlog.
- Enough source ports and file descriptors (`ulimit -n`); ephemeral port
  exhaustion looks exactly like server-side connection refusal.
- k6 `dropped_iterations` at zero — nonzero means `maxVUs` was too low and the
  intended arrival rate was never actually offered.
- Generator and target in the same region unless you are deliberately testing
  WAN latency; 80 ms of cross-continent RTT drowns the signal you want.

## Common Anti-Patterns

❌ **Reporting a single average response time.** It hides the tail entirely and
makes tail regressions invisible.
✅ Report p50/p95/p99/max, and set thresholds on p95 and p99.

❌ **A fixed VU count with `sleep()`, presented as realistic traffic.** It is a
closed model; it self-throttles and cannot produce queue collapse.
✅ Use an arrival-rate executor unless a closed model genuinely matches the
caller.

❌ **Including ramp-up and cold-start in the reported window.** Every run starts
with its worst numbers and the comparison between builds becomes noise.
✅ Warm to steady state, then measure a separate, clearly bounded window.

❌ **Testing against a dev database with 5,000 rows.** Query plans, cache hit
rates, and index residency are all different from production.
✅ Restore an anonymised production-scale dataset with realistic key skew.

❌ **Replaying one hardcoded user id or product id.** Cache hit rate approaches
100% and you measure the cache, not the system.
✅ Drive from a parameter corpus with a production-like distribution.

❌ **A pass/fail number with no curve behind it.** "Handles 2,000 req/s" says
nothing about what happens at 2,100.
✅ Publish the load-versus-latency curve and name the bottleneck resource.

❌ **Load testing only before launch.** The knee moves with every schema change
and dependency upgrade.
✅ Run a short load test on a schedule, and trend the results across builds.

❌ **Ignoring the generator's own health.** Ephemeral port exhaustion and dropped
iterations are read as server failures.
✅ Assert on generator saturation metrics before accepting any result.

## Load Testing Checklist

- [ ] Test shape chosen to match the failure class in question (load/stress/soak/spike)
- [ ] Soak run long enough to reveal leaks (≥ 4 h) before any major release
- [ ] Spike test covers both the surge and the recovery period after it
- [ ] Workload model is open (arrival-rate) unless a closed model matches reality
- [ ] Warm-up period defined and excluded from reported metrics
- [ ] Steady state confirmed (flat p99, stable RSS, stable cache hit rate) before measuring
- [ ] Dataset within an order of magnitude of production row counts
- [ ] Request parameters drawn from a corpus with realistic key skew
- [ ] p50/p95/p99/max reported; no bare averages
- [ ] Percentiles computed from histograms, not averaged across time buckets
- [ ] Load-versus-latency curve produced and the knee identified
- [ ] Server-side resource telemetry captured alongside client latency
- [ ] Bottleneck resource named in the result, not just the failing load level
- [ ] Load generator CPU, fd, and port headroom verified; dropped iterations at zero
- [ ] Thresholds expressed against SLOs rather than invented round numbers
- [ ] Results trended across builds so regressions surface as a slope
