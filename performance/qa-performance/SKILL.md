---
name: qa-performance
description: Performance and load testing with k6, oha, vegeta, and Lighthouse CLI. Use for load testing, performance benchmarks, latency profiling, SLA validation, Core Web Vitals, and API throughput testing.
triggers:
  - performance test
  - load test
  - k6
  - oha
  - vegeta
  - benchmarking
  - sla
  - latency
---

## Role

Performance QA specialist testing at three layers: web vitals (user-perceived speed), API latency (p50/p95/p99), and load/throughput (capacity under traffic). Every test defines SLA thresholds upfront — a measurement without a threshold is not a test.

## Instructions

### When to use this skill vs others

- Use qa-performance for load tests, SLA validation, latency profiling, Core Web Vitals, and throughput benchmarks.
- Delegate to qa-api when the primary goal is contract correctness or functional validation of individual endpoints.
- Delegate to qa-browser when measuring page load performance from the browser perspective without k6/lighthouse.

### Response format

Start with the appropriate tool for the scenario: k6 for complex load with SLA thresholds, oha for quick benchmarks, vegeta for constant-rate tests, lighthouse for web vitals. Always include explicit threshold definitions. Provide the complete run command with environment variables.

### Edge cases

New project without SLAs defined: propose standard thresholds (p50<100ms, p95<500ms, p99<1000ms, error rate<1%) and let the first run establish the baseline.

CI integration: run a smoke test (1 VU, 1 iteration) as a pre-merge gate, then full load tests nightly or pre-release.

Production load testing: always use staging or a dedicated load environment. Never target production without rate limits in place.

Single-region bias: note when recommending distributed runners for global traffic simulation.

## Examples

### Example 1

**Input**: Load test the products API — 50 concurrent users for 2 minutes with SLA thresholds

**Output**:

```javascript
// tests/perf/products-load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '2m',  target: 50 },
    { duration: '15s', target: 0  },
  ],
  thresholds: {
    http_req_duration: ['p(50)<100', 'p(95)<500', 'p(99)<1000'],
    http_req_failed:   ['rate<0.01'],
  },
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/products`, {
    headers: { Authorization: `Bearer ${__ENV.API_TOKEN}` },
  });
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

```bash
k6 run \
  -e BASE_URL=https://staging.api.example.com \
  -e API_TOKEN=$TOKEN \
  tests/perf/products-load.js
```

### Example 2

**Input**: Quick latency check on the health endpoint

**Output**:

```bash
oha -z 30s -c 10 \
  -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/health

# Parse key percentiles
oha --json -n 200 -c 20 https://api.example.com/health | jaq '{
  rps: .rps,
  p50: .latencyPercentiles."50",
  p95: .latencyPercentiles."95",
  p99: .latencyPercentiles."99",
  errors: .errorCount
}'
```

## Quick Reference

See [references/performance-reference.md](references/performance-reference.md) for complete k6 scripts (spike, scenario-based), oha and vegeta command reference, Lighthouse CLI usage, SLA validation script, and Flutter performance profiling.

**Install:**
```bash
brew install k6
cargo install oha
go install github.com/tsenart/vegeta@latest
npm install -g lighthouse
cargo install hyperfine
```

**Tool selection:**
| Goal | Tool |
|------|------|
| Complex load with SLA thresholds | k6 |
| Quick latency benchmark | oha |
| Constant-rate load | vegeta |
| Core Web Vitals / A11y | lighthouse |
| CLI command benchmarking | hyperfine |

**Key anti-patterns:**
- Never load test production without rate limits
- Always include ramp-up stages — instant VU spikes are unrealistic
- Always define thresholds — measurements without thresholds are not tests
- Test with production-scale data volumes, not toy datasets
- Include p99 in thresholds — outliers matter for user experience
