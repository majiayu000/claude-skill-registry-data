---
name: load-test-triage
description: "Use when a load test shows mass or (other)-bucketed failures, a suspiciously round latency, pool exhaustion, or throughput collapsing while the server idles, or before quoting any capacity figure. Also when 500s/502s pile up, a run dies as users rise, or failures shift with runner or generator count."
---

# Load test triage

When a load run reports mass failures, huge latency, or a throughput ceiling, the first job is deciding what you actually measured: the load harness, the database, or the application process. They look identical from outside and have opposite fixes. In one multi-day investigation, roughly 80% of failure volume traced back to the harness, not the server — treat the harness as the prime suspect and work cheapest-to-rule-out first.

## Decision flow: harness, database, or server?

Capture the harness's own counters, the database query, and a thread dump at the same moment, mid-hold — a query or dump taken between load steps shows an idle process and proves nothing:

| Failures | DB active | Server threads | Throughput | Verdict |
|---|---|---|---|---|
| many, early | low | normal | low | unramped stampede — re-run with a ramp |
| none | high, locks | high | plateau | real DB capacity |
| none | ~idle | climbing, many blocked in one frame | plateau | app-side bug (sync-over-async); scaling out multiplies fragility rather than fixing it |
| none | ~idle | **falling** | collapses as load rises | harness gate / rendezvous starvation — the number is the harness's, not the server's |

**Interpret in this order: harness, then database, then process.** The harness checks (section 1) are the cheapest and invalidate the whole run when they fail — most "server collapsed" reports are the harness starving itself. The database query (section 2) then exonerates or convicts the database in one sample: ~1 active connection while the app fails puts every remaining cause in-process (section 3). After fixing a harness fault, re-run the identical job before attributing any difference to the server — every capacity number is the harness's until proven otherwise.

## 1. The load harness

Harness artifacts are the most common cause and the cheapest to rule out.

### Offered rate is not the user count

`offered rate = users x per-user cadence`. Compute and print this in the run header — a run that cannot say what it asked for cannot be interpreted, and skipping it invalidates whole result tables.

- A default cadence of 1/s turns a user count directly into an operations-per-second demand: 10,000 users ask for 10,000 ops/s (3,200 users, 3,200 ops/s). No real crowd produces that rate.
- Convert to real-world cadence before calling anything a server limit: a player finishing a match every 10–20 minutes is about 0.001/s, so 10,000 such players offer roughly 8–17 ops/s, not 10,000/s.
- Example run-header format: `cadence 0.01/user/s = 100 matches/s offered, ramp 120s hold 180s`.
- Verify the driver actually *sends* the knob — a parsed-but-unplumbed variable silently runs the default and invalidates the run.

### Ramp shape and generator isolation

- **No ramp.** All virtual users arriving at t=0 measures account creation and cold caches contending with themselves, not steady state — a ramp is not optional. Symptom: login p50 in seconds, mass 500/502 concentrated at the start. Fix: stagger arrivals 30–60s and re-run before diagnosing anything else. Measured case: an identical 480-user run went from 246 failures to 0 with a 30s ramp added.
- Confirm the target address means the same thing to every runner: `localhost` in a job spec makes each remote worker aim at itself (instant connection-refused).
- **Isolate generators.** A generator sharing a CPU or box with the service under test corrupts every number — state it explicitly when it happens; local runners can succeed while remote ones fail, or vice versa. Compare a co-located runner's tail against an isolated one before quoting it: one measured case saw p99 7,568 ms co-located vs 180 ms isolated on an identical job (~40x). An attached debugger has the same effect — it turns timeouts into exceptions. More processes on a machine that's already refusing adds failures, not load; prefer more machines, and watch for the ~16,000 ephemeral-port ceiling per Windows box.
- **Upgrade every generator before comparing absolute counts.** Mixed harness builds make totals meaningless; only per-generator ratios survive.
- **Runner count changes the experiment.** The same user count driven by a different number (or weight) of generators is a different experiment, not a repeat — say the generator/runner count beside every figure. Two runs either side of a capacity knee can disagree by an order of magnitude (one measured case: 5 vs 7 runners, 15x); bracket the knee with both shapes rather than extrapolating from one, and vary the generator split at a fixed user count before concluding "broken at N".

### A round-number latency is a timeout, not load

If p50 or p95 sits on a suspiciously round number — 5,000 ms, 15,000 ms, 30,000 ms — stop looking at capacity and find the constant: grep the server for that timeout (a matchmaking/rendezvous gate wait, a connection-pool rent timeout, an HTTP client timeout). Measured case: p50 of 15,027 ms against a 15s gate meant the client waited out a timeout on most calls — nothing was working hard.

- **Split latency by operation kind**, not whole-flow (e.g. a matchmaking flow into `login` / `prematch` / `postmatch`). A fast sub-step (e.g. 50 ms) beside a timeout-pinned one means waiting on a peer, not work; whole-flow timing and a single climbing percentile both hide this, because a gate wait and real work look identical in aggregate.
- **Compare completion counts between stages**, not just failures. If one stage ran far more often than the dependent stage that must follow it, most attempts never got past the gate — in one run step A ran 2,303 times and dependent step B only 787: two-thirds of attempts never got past A. A tolerated outcome (an HTTP 303, a "no partner" result) hides this, because zero failures is compatible with almost nothing happening.

### Arrival pacing and pairing

How arrivals are spread decides whether paired/matchmaking workloads survive. Three implementations, not comparable to each other:

| Pacing | Behaviour | Failure mode |
| --- | --- | --- |
| None (delay after own call returns) | Each user is spaced only against itself; response-time jitter drifts users apart slowly | Crowd stays in the phase the ramp built: N users at 1/interval arrive as N at once |
| Random offset per user | Crowd spreads evenly | **Breaks any pairing/matchmaking**: partners never coincide, latency pins to the gate timeout |
| Offset derived from the pair/group id | Both halves take the same slot; groups spread | Correct for paired workloads |

- After a ramp with no spreading, the whole crowd fires together, sleeps, and fires together again — average rate looks low while instantaneous concurrency equals the whole population.
- Random per-user spreading is the obvious fix and is wrong for any paired or correlated workload: it pulls partners apart, so you can see **zero failures and a p50 sitting exactly on the gate timeout** at the same time.
- Fix: derive the offset from the same identifier the pairing uses (hash the pair/party/group id) so both halves compute it independently with no coordination between runners, then hold a fixed schedule (`nextCall += interval`) rather than `delay(interval)` after each call returns — a slow call must not desynchronise a pair for the rest of the run.

### In-flight and concurrency gates

- A concurrency/semaphore cap sized to stop a login stampede during the **ramp** must not carry into the steady-state **hold**, or the run silently caps in-flight work at `gate_size x runners` regardless of the user count and measures the semaphore instead of the server. Size the hold gate to the crowd instead, and keep it a separate object from the ramp gate — read which semaphore instance each phase actually receives; they're easy to conflate when declared near each other. Example: a `Concurrency = 25` per-runner cap means "800 users" is really ~125 concurrent; removing such a cap makes results look *worse* because the load finally became real — say so, rather than reporting a regression.
- Compute `users per runner : in-flight slots`. Past roughly 5:1, a paired operation (one needing two users in the same window) stops converging, and throughput collapses while the server goes quiet.
- If the workload has a **rendezvous** (matchmaking, pairing, barriers), a low in-flight ratio makes partners fail to coincide, every attempt burns the full server-side wait timeout, and throughput collapses *while the server goes idle*. The tell is unmistakable: more requested load → fewer server threads, idle database, zero failures, near-zero throughput — the same signature a generator that can't deliver its share produces.

### Make failures nameable before fixing anything

Harnesses key failure counts by raw message or cap distinct error keys. If a reason string embeds a trace id, request id, connection id, or GUID, **every failure becomes a unique key** and overflows into an `(other)` bucket that reports a count and no cause — one session lost hours to 4,876 failures reported as `(other)` that were all one nameable cause. Normalise correlation fields by name before counting, and raise the distinct-key cap once the keys are real causes:

```csharp
private static readonly Regex TraceFields =
    new("\"(trace_id|request_id|traceId|requestId)\":\\s*\"[^\"]*\"", RegexOptions.Compiled);
// ...
var normalised = TraceFields.Replace(body, "\"$1\":\"{id}\"");
```

Skipping this step wastes whole cycles guessing at a hidden cause.

### Other harness truths

- **Check the generators' own counters**: `attempted`, `connected`, `peakActive`, `failed`. If `peakActive` is well under the ask, the load never arrived and nothing about the server is proven. Counters that match the ask with zero connect failures clear the generators' connections — logins were fine, and any refusal came from the server — but not the load's shape: an unramped start, a ramp gate carried into the hold, lockstep pacing or a co-located generator (all above) still throttle a run whose counters all match.
- **First run after a restart is a cold start** (cold pools, first-time account creation). Repeat warm before calling it a rate limit. An inversion — lower rate fails, higher rate passes — is the signature.
- **Closed vs open loop.** Users that wait for their own call self-throttle and degrade gracefully; paced (open-loop) users keep arriving and queue without bound. The paced number is lower and is the honest one, because it's the shape a real crowd has.

## 2. The database

One query, sampled during the hold:

```sql
SELECT coalesce(state,'?'), count(*), count(*) FILTER (WHERE wait_event_type='Lock')
FROM pg_stat_activity WHERE backend_type='client backend' GROUP BY 1;
```

- `active` high, lock waits high, or `max_connections` reached → genuinely the database; find the query in `pg_stat_statements`.
- `idle in transaction` count exceeding `active` → the app is holding connections rather than using them.
- `active` ~1 with hundreds `idle`, zero lock waits, while latency climbs or the run is failing → **the database is exonerated**; the app is holding connections without querying. The time is going somewhere in-process — continue to section 3.

`pg_stat_activity` can rule the database in or out, but not which client owns a backend — a client-side pool ceiling needs the socket count in section 3.

## 3. The application / server process

### Thread-pool starvation

Capture a thread dump *during* the hold, not after — wait for the step to be posted and sleep past the ramp, then:

```bash
dotnet-stack report -p <pid> > dump.txt   # install: dotnet tool install --global dotnet-stack
```

Parse it correctly or you will blame the wrong code:

- The file may be **UTF-16** when redirected by PowerShell — decode before matching, or every regex silently returns nothing.
- Split threads on `Thread (`.
- Keep only threads parked in a blocking wait: `SpinThenBlockingWait`, `GetResult`, `ManualResetEventSlim.Wait`.
- `dotnet-stack` prints each thread's **innermost frame first**, so "group by the innermost frame" and "group by the first frame matching your own namespace" are the same instruction. Grouping by the *last* frame instead blames the pipeline (e.g. a response-buffering middleware that is entirely async) — it's only the outermost middleware.
- A finding is only a diagnosis when it's concrete: "78 of 80 blocked in X" names the site directly; a raw thread count does not.

```python
import re, collections
text = open('dump.txt', 'rb').read().decode('utf-16-le', errors='replace')  # or utf-8
counts = collections.Counter()
for block in text.split('Thread ('):
    if not any(s in block for s in ('SpinThenBlockingWait', 'GetResult', 'ManualResetEventSlim.Wait')):
        continue
    inner = next((l.strip() for l in block.split('\n') if 'YourNamespace' in l), None)
    if inner:
        counts[inner.split('!')[-1].split('(')[0]] += 1
print(counts.most_common(10))
```

A constructor atop the histogram means work is being done per request that should be async, or done once at startup. **The dominant .NET bug class:** a `Scoped` (`AddScoped`) service resolving async work in its **constructor** via `GetSomethingAsync().GetAwaiter().GetResult()` (or `.Result`). DI constructors run on the request thread, so every arrival blocks a thread-pool thread before doing any work. The thread pool injects new threads slowly — roughly one per 500 ms (~1–2/s) — so an arrival burst queues behind thread creation, hits connection-rent timeouts, and surfaces as connection-pool timeouts and 502s from the proxy, while the database sits idle. Fix: hold the *session/factory*, not the resolved context, and resolve inside the async methods that already `await`. Constructors cannot be async; the fix removes blocking work from them, it doesn't make them async.

Scaling out does not fix this: every replica starves the same way, so it multiplies the fragility, not the capacity — unlike a client-side pool ceiling (below), where each replica brings its own pools.

### Connection-pool ceiling

The database being idle does **not** mean the pool is fine — connections can be checked out and parked. Signature: the client reports `"the connection pool has been exhausted"` while the database itself shows ~1 active connection against a high `max_connections` — that combination means the limit is client-side pooling, not the database. Pools are per process, so replicas multiply that ceiling.

Count sockets from the client side instead:

```powershell
$pid_ = (Get-Process <Service>).Id
(Get-NetTCPConnection -OwningProcess $pid_ -State Established |
    Where-Object { $_.RemotePort -eq <dbPort> }).Count
# several known ports instead of one: Where-Object { $ports -contains $_.RemotePort }
```

- Sample once a second through a failing run and compare against rest. **A flat plateau on a round number is the pool cap.** Npgsql defaults to `Maximum Pool Size` 100 per data source, so a reader pool plus a writer pool plateaus at exactly 200 (two pools x default 100).
- The port may be a proxy/sidecar port, not the published container port — list the process's remote ports first rather than assuming. If the count reads zero, the filter is wrong, not the theory.
- Check the *runtime* connection string for an override, not just source files, and confirm the default from primary/vendor docs rather than memory.

### Leak vs ceiling

A leak and a ceiling both exhaust a pool but differ in time: a leak degrades *within* a steady run and never recovers; a ceiling fails immediately at a given concurrency and is clean below it. A long clean run at lower load, plus connections pruning back at rest, rules out a leak.

### Other blocking patterns to grep for

- Replacing a blocking `.GetResult()`/`.Result` call with a *synchronous* accessor that opens a connection is a safer flavour of blocking, not a non-blocking fix — state that precisely rather than "fixed".
- Static mutable collections written from request paths — a plain `Dictionary` mutated per login fails all logins under concurrency.

## Reporting rules

- Report the ladder as a table (users, generators, throughput, failures, blocked threads) and name the binding constraint with its measurement.
- Separate what's fixed from what's structural. When the remaining limit is arithmetic (slots × hold time < demand) or otherwise structural (pool size, port range, thread cap), say plainly that no further code fix moves it, and list the remaining levers by cost — stop hunting for one more code bug.
- Distinguish a **confirmed bug** from a **confirmed cause of the collapse** — say which is proven and which is inferred. A blocking constructor can be real and still not be what failed the run.
- A ceiling measured through a throttling harness is a **floor**, never a ceiling. If zero failures occurred at every level tested, say the ceiling was never reached and the throughput figure is a floor.
- Zero failures is not success if the flow silently tolerates a miss (e.g. an unpaired match counted as a skip) — always check completion counts per stage, not just failure counts.
- Say which pacing implementation and build produced each figure — changing *when* calls arrive changes results as much as changing how many; rows from different pacing implementations are not a ladder.
- Fix harness limits before server code, or the before/after of a server fix cannot be measured.
- **Blast radius:** shared base classes and DAL infrastructure are the last place to fix, not the first. Surface the evidence and get explicit approval before editing a type every consumer inherits — a load test is not authorisation to rewrite the data layer.

## Before quoting a capacity number

State, alongside the figure itself: the offered rate (not just the user count), the pacing implementation, the generator/runner count and isolation, the build configuration, and what the run did **not** cover. A figure from a Debug build on loopback against one process is a floor, and any flow that is registered but not routed has never been tested at all.

## Make the diagnosis reusable

Put the three signals in the product, next to each other, so a diagnosis doesn't require a terminal: a DB rollup, a server thread-count readout, and a button that captures and histograms stacks grouped by innermost own-code frame. That turns a terminal-only diagnosis into one button anyone can press.
