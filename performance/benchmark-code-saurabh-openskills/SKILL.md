---
name: benchmark
description: Performance benchmarking skill — baseline and compare page load times, Core Web Vitals, bundle sizes, and API response times. Use when the user wants to measure performance before and after a change, catch performance regressions in a PR, establish a performance baseline, or understand what is making their app slow.
---

# Benchmark

Benchmarking without a baseline is noise. A benchmark that can't be reproduced is a guess. Every benchmark in this skill produces a number, a method, and a comparison — not an impression.

Performance is a feature. Regressions ship silently. This skill makes regressions visible before they reach users.

---

## Benchmark Principles

- **Measure before you optimize.** An optimization without a before measurement is an assumption. Always baseline first.
- **Reproduce exactly.** A benchmark is only valid if another engineer can reproduce it with the same setup. Document the environment, the command, and the conditions.
- **Medians lie. Use percentiles.** P50 hides the users who are suffering. Always report P75, P95, and P99 alongside the median.
- **Synthetic vs real-user data.** Lighthouse in a lab tells you what's possible. RUM (Real User Monitoring) tells you what's happening. Use both.
- **One change at a time.** If two things change between benchmarks, you can't attribute the delta to either.
- **A regression is a regression.** A 10% slowdown on a fast page is still a regression. Set thresholds and enforce them.

---

## Step 0: Establish the Baseline

Before any optimization or PR review, establish the baseline. Without it, "after" numbers are meaningless.

```bash
# Run Lighthouse baseline (3 runs, take median)
npx lighthouse https://your-app.com/key-page \
  --output json \
  --output-path ./baseline.json \
  --chrome-flags="--headless" \
  --throttling-method=simulate \
  --preset=desktop

# Run 3 times and average — single runs are noisy
for i in 1 2 3; do
  npx lighthouse https://your-app.com/key-page \
    --output json \
    --output-path "./baseline-run-$i.json" \
    --chrome-flags="--headless"
done
```

Record in `benchmark-baseline.md`:
```markdown
## Baseline — [Page/Endpoint] — [Date] — [Commit SHA]

| Metric | Run 1 | Run 2 | Run 3 | Median |
|--------|-------|-------|-------|--------|
| LCP    |       |       |       |        |
| INP    |       |       |       |        |
| CLS    |       |       |       |        |
| FCP    |       |       |       |        |
| TTFB   |       |       |       |        |
| Total JS bundle | | | | |
| Total CSS bundle | | | | |
| Network requests | | | | |

**Environment:** macOS M2 / 6-core CPU throttle / Fast 3G simulation
**Tool:** Lighthouse 12.x / Chrome 124
**URL:** https://your-app.com/key-page
```

---

## Core Web Vitals — Reference

| Metric | Full Name | Measures | Good | Needs Improvement | Poor |
|--------|-----------|----------|------|-------------------|------|
| **LCP** | Largest Contentful Paint | Loading | ≤2.5s | 2.5–4.0s | >4.0s |
| **INP** | Interaction to Next Paint | Interactivity | ≤200ms | 200–500ms | >500ms |
| **CLS** | Cumulative Layout Shift | Visual stability | ≤0.1 | 0.1–0.25 | >0.25 |
| **FCP** | First Contentful Paint | Loading start | ≤1.8s | 1.8–3.0s | >3.0s |
| **TTFB** | Time to First Byte | Server response | ≤800ms | 800ms–1.8s | >1.8s |

---

## Frontend Benchmarking

### Lighthouse (automated, reproducible)
```bash
# Single page audit
npx lighthouse https://your-app.com \
  --output=json,html \
  --output-path=./lighthouse-report \
  --chrome-flags="--headless --no-sandbox"

# Key metrics to extract from JSON
cat lighthouse-report.report.json | jq '{
  lcp: .audits["largest-contentful-paint"].numericValue,
  inp: .audits["interaction-to-next-paint"].numericValue,
  cls: .audits["cumulative-layout-shift"].numericValue,
  fcp: .audits["first-contentful-paint"].numericValue,
  ttfb: .audits["server-response-time"].numericValue,
  score: .categories.performance.score
}'
```

### Bundle Size Analysis
```bash
# Next.js
npx next build 2>&1 | grep -A 50 "Route (app)"

# Webpack Bundle Analyzer
npm install --save-dev webpack-bundle-analyzer
# Add to webpack config, then:
npx webpack --profile --json > stats.json
npx webpack-bundle-analyzer stats.json

# Source map explorer (any bundler)
npm install --save-dev source-map-explorer
npx source-map-explorer 'build/static/js/*.js'

# Check for duplicate packages
npx duplicate-package-checker-webpack-plugin
```

### Bundle Size Regression Check
```bash
# Before (on main branch)
git checkout main && npm run build
du -sh .next/static/chunks/*.js | sort -rh | head -10 > bundle-before.txt

# After (on feature branch)
git checkout feature-branch && npm run build
du -sh .next/static/chunks/*.js | sort -rh | head -10 > bundle-after.txt

diff bundle-before.txt bundle-after.txt
```

---

## API Benchmarking

### Response Time (k6)
```javascript
// k6-script.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // ramp up
    { duration: '1m',  target: 10 },   // steady state
    { duration: '10s', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // <1% error rate
  },
};

export default function () {
  const res = http.get('https://your-app.com/api/endpoint', {
    headers: { Authorization: `Bearer ${__ENV.API_TOKEN}` },
  });
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  sleep(1);
}
```

```bash
# Run benchmark
k6 run k6-script.js

# Compare before/after
k6 run --out json=before.json k6-script.js
# Make the change
k6 run --out json=after.json k6-script.js
```

### Quick curl timing
```bash
# Measure individual request timing
curl -o /dev/null -s -w \
  "TTFB: %{time_starttransfer}s\nTotal: %{time_total}s\nSize: %{size_download} bytes\n" \
  https://your-app.com/api/endpoint

# Run 10 times and get stats
for i in $(seq 1 10); do
  curl -o /dev/null -s -w "%{time_total}\n" https://your-app.com/api/endpoint
done | awk '{sum+=$1; if(NR==1||$1<min)min=$1; if($1>max)max=$1} END {printf "min=%.3fs avg=%.3fs max=%.3fs\n", min, sum/NR, max}'
```

---

## Database Query Benchmarking

```sql
-- Explain analyze a slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.*, o.total
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.created_at > NOW() - INTERVAL '30 days'
ORDER BY o.total DESC
LIMIT 100;

-- Check for sequential scans on large tables (should be index scans)
-- Look for: Seq Scan on large_table — this is the red flag

-- Find slow queries in PostgreSQL
SELECT query,
       calls,
       mean_exec_time::numeric(10,2) AS mean_ms,
       max_exec_time::numeric(10,2)  AS max_ms,
       total_exec_time::numeric(10,2) AS total_ms
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

---

## Before / After Comparison Format

Always produce this table when benchmarking a change:

```markdown
## Benchmark Results — [Feature/Change] — [Date]

**Commit before:** abc1234  
**Commit after:**  def5678  
**Environment:** [describe exactly]  
**Tool:** [Lighthouse 12 / k6 1.0 / custom]

### Core Web Vitals (median of 3 runs)

| Metric | Before | After | Delta | Verdict |
|--------|--------|-------|-------|---------|
| LCP    | 2.8s   | 2.1s  | -25%  | ✅ Improved |
| INP    | 180ms  | 210ms | +17%  | ⚠️ Regressed |
| CLS    | 0.05   | 0.05  |   0%  | ✅ Neutral |
| Perf score | 72 | 81  | +9pts | ✅ Improved |

### Bundle Size

| Asset | Before | After | Delta | Verdict |
|-------|--------|-------|-------|---------|
| main.js | 284KB | 301KB | +6%  | ⚠️ Regressed |
| vendor.js | 412KB | 398KB | -3% | ✅ Improved |
| CSS total | 48KB | 48KB |  0%  | ✅ Neutral |

### API Response Time (p50 / p95 / p99)

| Endpoint | Before | After | Delta | Verdict |
|----------|--------|-------|-------|---------|
| GET /api/users | 45/120/280ms | 38/95/210ms | -25% | ✅ Improved |
| POST /api/orders | 120/380/950ms | 125/390/960ms | +1% | ✅ Neutral |

### Overall Verdict
🟢 SHIP — performance improved overall. INP regression is within acceptable range (180→210ms, still <200ms threshold). main.js increase (+17KB) is offset by lazy-loading the settings panel.
```

---

## Regression Thresholds

Define these per project. These are sensible defaults:

| Metric | Warning threshold | Block threshold |
|--------|------------------|-----------------|
| LCP | +10% | +25% or >4.0s |
| INP | +15% | +30% or >500ms |
| CLS | any increase | >0.1 absolute |
| JS bundle | +5% | +15% or +50KB |
| API P95 | +10% | +25% or >1s |
| Lighthouse score | -3pts | -10pts |

---

## CI Integration (Lighthouse CI)

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build
      - run: npm run start &
      - uses: treosh/lighthouse-ci-action@v11
        with:
          urls: |
            http://localhost:3000/
            http://localhost:3000/dashboard
          budgetPath: ./lighthouse-budget.json
          uploadArtifacts: true

# lighthouse-budget.json
[{
  "path": "/*",
  "timings": [
    { "metric": "largest-contentful-paint", "budget": 2500 },
    { "metric": "cumulative-layout-shift",  "budget": 0.1 }
  ],
  "resourceSizes": [
    { "resourceType": "script", "budget": 400 },
    { "resourceType": "total",  "budget": 800 }
  ]
}]
```

---

## Bundled Resource

Use `python scripts/compare_metrics.py baseline.json candidate.json` to compare flat JSON metric files in a repeatable way. Read [metric-contract.md](./references/metric-contract.md) first to define units and regression thresholds; do not compare incompatible measurements.

## Definition of Done — Benchmark

- [ ] Baseline established before any change (commit SHA recorded)
- [ ] Same environment used for before and after measurements
- [ ] Minimum 3 runs taken, median reported (not single run)
- [ ] All Core Web Vitals measured (LCP, INP, CLS, FCP, TTFB)
- [ ] Bundle sizes measured before and after
- [ ] API P50/P95/P99 measured for changed endpoints
- [ ] Before/after comparison table produced
- [ ] Every metric has a verdict: Improved / Regressed / Neutral
- [ ] Any regression explained (is it acceptable? why?)
- [ ] Overall ship/hold verdict stated with rationale
- [ ] Results committed to `benchmark-results/` for historical comparison
