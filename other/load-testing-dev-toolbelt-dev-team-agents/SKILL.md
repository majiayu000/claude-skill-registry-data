---
name: load-testing
description: Load testing — smoke/load/stress/soak/spike profiles, SLO thresholds, tooling.
---

# Load Testing

Server-side performance validation: how much traffic the system takes before it degrades, and where it breaks first.

## When to Load

Load for backend, API, or infrastructure work where capacity, concurrency or throughput matter — before a launch, before a traffic event, after an architecture change, or when investigating production saturation.

**Boundary with `skills/architecture/performance-budgets/SKILL.md`:**

| Concern | Skill |
|---|---|
| Client-side rendering, Core Web Vitals, bundle size, Lighthouse CI | `performance-budgets` |
| Server latency under concurrency, throughput, saturation, breaking point | this skill |

They are complementary: a page can hit every Core Web Vitals target at one user and still collapse at a thousand.

---

## Load Profiles

Pick the profile from the question being asked. Running the wrong profile answers a question nobody had.

| Profile | Shape | Question answered | Typical duration |
|---|---|---|---|
| **Smoke** | Minimal load, 1–5 virtual users | Does the script work and the system respond correctly at all? | 1–2 min |
| **Load** | Ramp to expected peak, hold | Does the system meet its SLOs at normal peak traffic? | 10–30 min |
| **Stress** | Ramp past peak until degradation | Where is the breaking point, and what breaks first? | 20–60 min |
| **Soak** (endurance) | Moderate load held for hours | Do leaks, unbounded caches, connection or disk growth appear over time? | 2–24 h |
| **Spike** | Instant jump to a multiple of peak, then drop | Does the system survive a sudden surge and **recover** afterwards? | 5–15 min |
| **Breakpoint** | Slow unbounded ramp | What is the maximum sustainable throughput per instance? | Until failure |

Rules:
- **Always run smoke first.** Most "failed" load tests are broken scripts, wrong credentials, or a 404 loop returning fast errors.
- Ramp gradually in load and stress tests — instant ramps only measure cold starts and connection pool warmup.
- Include a **recovery window** after spike and stress runs; a system that never recovers without a restart has a worse defect than the one that slowed down.
- Change one variable per run. A test that changes load *and* configuration explains nothing.

---

## Deriving Thresholds from SLOs

Thresholds are not invented for the test — they come from the service's SLOs (`skills/architecture/observability-slo/SKILL.md`). If no SLO exists, defining one is the first deliverable, not the load test.

1. Take the user-facing SLO (e.g. *99% of checkout requests complete under 800 ms*).
2. Convert to a **percentile threshold with a load level**: `p99 < 800ms at 500 concurrent users`.
3. Set the error-rate threshold **below** the error budget, not at it — the test must fail before users would notice.
4. Add a throughput floor: sustained requests/second the system must handle without breaching the above.
5. Encode all of them as **pass/fail assertions in the tool**, so the run exits non-zero on breach. A load test with no assertions is a graph nobody reads.

| Traffic input | Source |
|---|---|
| Expected peak concurrency | Production analytics — peak hour, not daily average |
| Request mix | Real endpoint distribution from access logs or APM, not an even split |
| Growth headroom | Test at 2× expected peak; capacity planning targets, not wishes |

---

## What to Measure

| Metric | Rule |
|---|---|
| **Latency percentiles** (p50, p90, p95, p99) | Report percentiles, never averages — an average hides the tail that defines user experience |
| **Throughput** (req/s, completed iterations/s) | The real capacity number; must be reported alongside the concurrency that produced it |
| **Error rate** by status and type | Separate 4xx (script/data problem) from 5xx and timeouts (system problem) |
| **Saturation** | CPU, memory, connection pool usage, queue depth, thread pool, disk I/O, file descriptors |
| **Downstream** | Database slow queries, lock waits, cache hit ratio, external API latency |
| **Client-side saturation** | Load generator CPU/network — a saturated generator invents latency that does not exist |

Interpretation rules:
- A rising p99 with flat p50 means **queuing or contention**, not slow code.
- Throughput plateauing while latency climbs marks the **saturation point** — the breaking point is just after it.
- Errors appearing before latency degrades usually means a hard limit (connection pool, rate limiter, file descriptors), not capacity.
- Correlate every run with server-side observability. Numbers from the load generator alone cannot tell you *why*.

---

## Test Data and Environment Pitfalls

| Pitfall | Consequence | Mitigation |
|---|---|---|
| Same user/record for every virtual user | Unrealistic cache hits and row-level lock contention | Parameterize with a realistic data pool |
| Dataset far smaller than production | Every query hits an in-memory index; results are meaningless | Seed representative volume and cardinality |
| Environment scaled down from production | Results cannot be extrapolated linearly | Match topology, or state the scaling factor explicitly and never extrapolate silently |
| Autoscaling enabled without noting it | Measures the scaler's reaction time, not the system's capacity | Test fixed capacity first, then autoscaling behavior separately |
| Caches/CDN in front absorbing the load | Tests the cache, not the origin | Bypass or vary keys deliberately; test both paths |
| Rate limiters or WAF throttling the generator | 429s reported as system failure | Allowlist the generator, or make throttling part of the scenario |
| Third-party APIs called for real | Cost, bans, and someone else's latency in the results | Stub with realistic latency and error injection |
| Test writes into shared/production data | Data corruption and contaminated analytics | Dedicated tenant/dataset, cleanup routine, never load-test production without written approval |
| Metrics polluting production dashboards | False alerts and paged on-call | Tag all synthetic traffic with a header and exclude it from alerts |

Also budget for **think time** between requests — real users pause. A no-pause script produces a load pattern that no real population creates.

---

## Tool Selection

Gate on the signals already present in the project — a tool the team can read and maintain beats a marginally faster one.

| Signal | Tool |
|---|---|
| JS/TS codebase, CI-first, scriptable scenarios, thresholds as code | `k6` |
| Python codebase, custom logic per user, distributed generators | `Locust` |
| Java/JVM shop, GUI-driven test design, protocol variety (JMS, JDBC, LDAP) | `JMeter` |
| Scala/Java, high per-node throughput, HTML reports | `Gatling` |
| Quick sanity check on a single endpoint | `hey`, `wrk`, `oha`, `autocannon` |
| gRPC services | `ghz` |
| Cloud-managed distributed runs, no generator infrastructure to operate | Managed service from the existing cloud provider |
| Browser-level load (real rendering, JS execution) | Browser-driver mode of the chosen tool — expensive, use only when protocol-level load cannot answer the question |

Rules:
- Store scripts in the repo next to the code they exercise, reviewed like tests.
- Run smoke profiles in CI on every PR; run heavier profiles on a schedule or before releases — a 30-minute soak does not belong in the PR pipeline.
- Record results as artifacts and track them over time; a single run has no trend and therefore no verdict.
- Test through the same entry point real traffic uses (gateway, load balancer, TLS) — bypassing it removes the layers that usually fail first.

---

## Reporting a Run

Every result must state, in one place:

- Profile and duration, target environment and its capacity
- Concurrency/arrival rate and the request mix
- Throughput achieved, latency percentiles, error rate by type
- Saturation of the top resource and what limited it
- Pass/fail against each declared threshold
- The single next bottleneck to address

"It handled the load" without the numbers above is not a result.

---

## Decision Checklist

- [ ] Is there a stated question, and does the chosen profile answer it?
- [ ] Do thresholds derive from an SLO rather than from intuition?
- [ ] Are latency results reported as percentiles, with the concurrency that produced them?
- [ ] Did a smoke run validate the script before the real run?
- [ ] Is test data parameterized and the dataset representative in volume?
- [ ] Is the environment's relationship to production documented?
- [ ] Are caches, autoscaling, rate limiters and third parties accounted for deliberately?
- [ ] Is server-side saturation captured alongside client-side latency?
- [ ] Are thresholds encoded as assertions so the run fails automatically?
- [ ] Is synthetic traffic tagged and excluded from production alerting?
- [ ] Is the result stored for trend comparison against previous runs?
