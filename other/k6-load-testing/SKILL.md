---
name: k6-load-testing
description: "Authors k6 JavaScript load-test scripts (VU loops + checks + sleeps), configures the `options` block with `stages` (ramp-up patterns) and `thresholds` (p(95) latency, error rate), runs via `k6 run script.js` or `--vus / --duration` ad-hoc flags, and uses thresholds as the CI pass/fail signal. Includes a latency-percentile interpretation reference: tail ratio (p99/p50), bimodal-distribution detection, coordinated omission and why naive p99 is optimistic, and constant-vus vs constant-arrival-rate executors. Use when the project ships HTTP / WebSocket / gRPC load tests and the team wants developer-friendly JavaScript authoring, or when a k6 threshold passes but the system still feels slow."
---

# k6-load-testing

[overview]: https://grafana.com/docs/k6/latest/
[running]: https://grafana.com/docs/k6/latest/get-started/running-k6/
[thresholds]: https://grafana.com/docs/k6/latest/using-k6/thresholds/

k6 tests are `.js` files with a default-exported function that runs
once per virtual user (VU) per iteration (per [k6-running][running]).
This skill covers the load-testing workflow; k6's browser, synthetic
monitoring, and chaos modes share the same script structure but are
out of scope here.

## When to use

- The project ships HTTP, WebSocket, or gRPC services that need
  performance testing.
- The team prefers JavaScript authoring (vs. JMeter's XML, Gatling's
  Scala/Java, or Locust's Python).
- A CI gate is needed on **p(95) latency** + **error rate** - k6's
  thresholds are designed for this.
- The team is on Grafana Cloud (k6 integrates natively) or wants a
  self-hosted CLI-only flow.

If the team is already deep in JMeter, the migration cost is non-
trivial - evaluate `jmeter-load-testing`
in place. For Python / Locust shops and JVM / Gatling teams, see the
Gatling and Locust references in `load-testing-overview`.

## Install

Install via [k6 installation](https://grafana.com/docs/k6/latest/set-up/install-k6/)
(brew, apt/yum, choco, Docker). Pin a specific k6 version in CI
rather than "latest".

## Authoring

### Minimal script

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function () {
  const res = http.get('https://quickpizza.grafana.com/');
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}
```

(Per [k6-running][running].)

The default-exported function runs once per virtual-user iteration.
`check()` is a non-failing assertion that contributes to the
`checks` metric; `sleep()` simulates think-time between requests.

### Options block - stages

Per [k6-running][running], the `options` export controls the run:

```javascript
export const options = {
  stages: [
    { duration: '30s',    target: 20 },   // ramp up to 20 VUs over 30s
    { duration: '1m30s',  target: 10 },   // hold ~10 VUs for 90s (gradual scale-down)
    { duration: '20s',    target: 0 },    // ramp down to 0
  ],
};
```

Three canonical shape patterns:

| Pattern             | Stages                                                                |
|---------------------|-----------------------------------------------------------------------|
| Smoke test          | One stage, `{ duration: '1m', target: 1 }` - sanity check.            |
| Average load test   | Ramp up → plateau → ramp down (the example above).                    |
| Stress test         | Ramp past expected peak; observe where the system breaks.             |
| Spike test          | Sudden ramp to high VU; back to normal; verify recovery.              |
| Soak test           | Long plateau (hours); verify no resource leaks over time.             |

### Options block - thresholds

Per [k6-thresholds][thresholds], thresholds are "the pass/fail
criteria that you define for your test metrics" - the canonical CI
gate:

```javascript
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],   // 95% of requests under 500ms
    http_req_failed:   ['rate<0.01'],   // <1% errors
    checks:            ['rate>0.99'],   // >99% of checks pass
  },
};
```

(Per [k6-thresholds][thresholds].)

The threshold expression syntax is `<aggregation_method> <operator>
<value>`. Available aggregation methods per metric type:

| Metric type | Methods                                          |
|-------------|--------------------------------------------------|
| Trend       | `avg`, `min`, `max`, `med`, `p(N)` (percentile, ms) |
| Counter     | `count`, `rate`                                  |
| Rate        | `rate`                                           |
| Gauge       | `value`                                          |

A test that fails any threshold exits non-zero - the canonical CI
gate signal.

### `abortOnFail`

For long-running stress / soak tests, abort early if a threshold is
already violated ([k6-thresholds][thresholds]):

```javascript
thresholds: {
  http_req_duration: [
    { threshold: 'p(95)<500', abortOnFail: true, delayAbortEval: '10s' },
  ],
},
```

`delayAbortEval` postpones the abort decision to let metrics
accumulate before evaluating; without it, a 1-second test could
abort on a single slow request.

## Running

### Ad-hoc (no options block needed)

```bash
k6 run --vus 10 --duration 30s script.js
```

(Per [k6-running][running].)

`--vus` overrides the script's options; `--duration` runs for a
fixed time without ramps.

### Standard run

```bash
k6 run script.js
```

`options` block in the script controls everything; the CLI is
hands-off. Preferred for CI.

### Useful flags

| Flag                              | Purpose |
|-----------------------------------|---------|
| `--out json=<file>`               | Stream raw metrics to a JSON file. |
| `--summary-export=<file>`         | Write the end-of-test summary to JSON. |
| `--quiet`                         | Silence the live progress UI (CI noise). |
| `--http-debug=full`               | Verbose HTTP debug for triage runs. |
| `--env KEY=VAL`                   | Inject env vars accessible via `__ENV.KEY`. |
| `--config <file>`                 | Externalize the options block to a JSON file. |

## Parsing results

The end-of-run summary prints to stdout; `--summary-export` writes
the same data as JSON for downstream consumption:

```json
{
  "metrics": {
    "http_req_duration": {
      "values": { "p(95)": 432.1, "avg": 198.3, ... },
      "thresholds": { "p(95)<500": { "ok": true } }
    },
    "http_req_failed": {
      "values": { "rate": 0.004, "passes": 996, "fails": 4 },
      "thresholds": { "rate<0.01": { "ok": true } }
    }
  }
}
```

Pipe to `jq` for a quick gate report:

```bash
jq -r '
  .metrics
  | to_entries[]
  | select(.value.thresholds)
  | .key + ": " + (.value.thresholds | to_entries | map("\(.key) → \(if .value.ok then "PASS" else "FAIL" end)") | join(", "))
' summary.json
```

## CI integration

Full GitHub Actions workflow - apt install, PR + nightly triggers,
summary upload via `if: always()` - in
[references/ci-integration.md](references/ci-integration.md). A
failing threshold causes `k6 run` to exit non-zero, failing the job.

## Interpreting latency distributions

Passing a p95 threshold is necessary but not sufficient. The full
interpretation workflow - expanding `summaryTrendStats` to p99/p99.9, the
tail ratio (p99/p50) as a spread signal, bimodal-distribution heuristics,
sub-metric cross-checks (`http_req_waiting` / `http_req_blocked`),
coordinated omission and HdrHistogram correction, and `constant-vus` vs
`constant-arrival-rate` executor semantics - is in
[references/latency-percentiles.md](references/latency-percentiles.md).

## Anti-patterns

| Anti-pattern                                                    | Why it fails                                                     | Fix |
|-----------------------------------------------------------------|------------------------------------------------------------------|-----|
| Hard-coded URLs / tokens in script                                | Scripts bind to one environment; secrets leak.                   | Read from `__ENV.API_BASE_URL`, `__ENV.API_TOKEN`. |
| `--vus 1000 --duration 1h` from a developer laptop                | Laptop resource contention; client-side bottlenecks corrupt metrics. | Run from a CI runner / dedicated load generator; never from a dev box for serious numbers. |
| Threshold `p(95)<10000`                                           | Practically meaningless - passes any sane API. Hides regressions. | Set thresholds at meaningful budgets (500ms, 1s) tied to NFRs from the `non-functional-requirement-extractor`. |
| Soak tests in PR CI                                                | Multi-hour PR CI; team disables.                                | Soak tests are scheduled-only; PRs run smoke / average load. |
| Missing `sleep()` between requests                                | Hammering at full VU rate generates synthetic numbers; doesn't model real users. | Include `sleep(1)` or randomized think-time after each iteration. |
| Asserting only `http_req_failed` rate                              | A 30-second response that succeeds passes the rate gate but breaks UX. | Always pair with `http_req_duration` percentile thresholds. |

## Limitations

- **Single-machine VU limits.** A single k6 instance saturates one
  machine's outbound CPU / network - typically 20-50k concurrent VUs
  for HTTP. For higher loads, distribute via Grafana Cloud or k6
  Operator on Kubernetes.
- **No native browser execution.** The `k6/browser` module covers it
  but adds Chromium overhead; for browser-driven perf testing,
  consider `lighthouse-perf` instead.
- **JS sandbox limits.** k6 uses goja (Go-based ES5+/some-ES6),
  not Node.js. npm packages with native deps don't work; pure-JS
  packages do. Use `k6 archive` to bundle.

## References

- [k6-overview][overview] - main docs landing page.
- [k6-running][running] - basic script + options + stages + ad-hoc
  flags.
- [k6-thresholds][thresholds] - threshold syntax, aggregation methods,
  abortOnFail / delayAbortEval.
- `jmeter-load-testing` and the Gatling / Locust references in
  `load-testing-overview` - alternatives by language stack.
- [references/latency-percentiles.md](references/latency-percentiles.md) -
  interpreting the latency distributions this skill's runs produce.
- `perf-budget-gate` - downstream
  gate that aggregates k6 / lighthouse / load-runner verdicts.
