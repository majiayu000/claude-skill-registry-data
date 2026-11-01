---
name: testing-load
description: Load Testing Engineer — Institutional capability and runbook for testing-load.
---

# SKILL: Load Testing Engineer
## Domain: Locust, Performance Benchmarking, Capacity Planning, Bottleneck Analysis

**Activation triggers:** load test, performance benchmark, concurrent users,
throughput, Locust, k6, capacity planning, stress test, spike test, bottleneck,
latency under load.

---

## Load Test Types

```
Type            | Description                                    | When to Use
────────────────|────────────────────────────────────────────── |──────────────────
Load test       | Sustained load at expected peak traffic        | Before production deploy
Stress test     | Increase load until system breaks              | Find the breaking point
Spike test      | Sudden 10x traffic spike                       | Validate auto-scaling
Soak test       | Low load for 24+ hours                         | Find memory leaks
Smoke test      | Minimal load (1-2 users)                       | Verify test setup
```

---

## Locust Setup

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between, events
import json

class TradingPlatformUser(HttpUser):
    """Simulates a typical Integral Market user session."""
    wait_time = between(1, 5)    # 1-5s between tasks (realistic browsing)
    access_token: str = ""
    account_id: str = ""

    def on_start(self):
        """Called once per simulated user — authenticate first."""
        resp = self.client.post(
            "/api/v1/auth/login",
            data={"username": "loadtest@integralmarket.com", "password": "LoadTest123!"},
        )
        if resp.status_code == 200:
            self.access_token = resp.json()["access_token"]
            self.account_id = "00000000-0000-0000-0000-000000000001"  # load test account

    @property
    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    # ── Market Backend Tasks ─────────────────────────────────────────────────

    @task(5)   # weight: most frequent action
    def get_current_user(self):
        self.client.get("/api/v1/auth/me", headers=self._auth_headers)

    @task(2)
    def get_providers(self):
        self.client.get("/api/v1/copy-trading/providers", headers=self._auth_headers)

    # ── Expert Backend Tasks ─────────────────────────────────────────────────

    @task(8)   # most frequent — users check positions constantly
    def get_positions(self):
        self.client.get(
            f"/api/v1/brokers/accounts/{self.account_id}/positions",
            headers=self._auth_headers,
        )

    @task(4)
    def get_trade_history(self):
        self.client.get(
            f"/api/v1/journal/trades?account_id={self.account_id}&limit=50",
            headers=self._auth_headers,
        )

    @task(2)
    def get_performance_summary(self):
        self.client.get(
            f"/api/v1/journal/performance?account_id={self.account_id}",
            headers=self._auth_headers,
        )

    @task(1)
    def get_watchlist(self):
        self.client.get("/api/v1/imcharts/watchlists", headers=self._auth_headers)
```

---

## Running Load Tests

```bash
# Install locust
pip install locust

# Run with web UI (localhost:8089)
locust -f tests/load/locustfile.py \
  --host=http://localhost:8002 \
  --users=100 \
  --spawn-rate=10

# Run headless (CI mode)
locust -f tests/load/locustfile.py \
  --host=http://localhost:8002 \
  --users=100 \
  --spawn-rate=10 \
  --run-time=60s \
  --headless \
  --csv=results/loadtest_$(date +%Y%m%d)

# Report key metrics:
# - Requests per second (RPS)
# - P50, P95, P99 latency
# - Failure rate (should be 0%)
# - Active users vs. latency curve
```

---

## Acceptance Criteria (Performance SLAs)

```python
# tests/load/sla_check.py — validate results against SLAs
import pandas as pd

def check_sla(csv_path: str) -> dict:
    stats = pd.read_csv(f"{csv_path}_stats.csv")

    sla = {
        "/api/v1/auth/me":              {"p99_ms": 200, "failure_pct": 0.0},
        "/api/v1/journal/trades":       {"p99_ms": 500, "failure_pct": 0.5},
        "/api/v1/journal/performance":  {"p99_ms": 1000, "failure_pct": 0.5},
        "/api/v1/brokers/accounts":     {"p99_ms": 500, "failure_pct": 0.5},
    }

    violations = []
    for endpoint, limits in sla.items():
        row = stats[stats["Name"].str.contains(endpoint.split("/")[-1])]
        if row.empty:
            continue

        actual_p99 = row["99%"].values[0]
        actual_fail_pct = (row["Failure Count"].values[0] / row["Request Count"].values[0]) * 100

        if actual_p99 > limits["p99_ms"]:
            violations.append(f"{endpoint}: p99={actual_p99}ms > SLA {limits['p99_ms']}ms")
        if actual_fail_pct > limits["failure_pct"]:
            violations.append(f"{endpoint}: failure={actual_fail_pct:.1f}% > SLA {limits['failure_pct']}%")

    return {"passed": len(violations) == 0, "violations": violations}
```

---

## Bottleneck Identification

```bash
# During load test, monitor these concurrently:

# 1. Database connections
psql -c "SELECT count(*) FROM pg_stat_activity;"
# If count approaches max_connections (100), need connection pooling (PgBouncer)

# 2. Database slow queries
psql -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
# Queries > 100ms under load → add indexes or optimize

# 3. Redis memory
redis-cli info memory | grep used_memory_human

# 4. Python event loop lag (add to /health endpoint)
# import asyncio
# lag_start = asyncio.get_event_loop().time()
# await asyncio.sleep(0)
# event_loop_lag_ms = (asyncio.get_event_loop().time() - lag_start) * 1000
# If lag > 50ms → CPU-bound work blocking the event loop

# 5. Backend CPU/memory
htop -p $(pgrep -f "uvicorn app.main")
```

---

## k6 Alternative (TypeScript-based)

```javascript
// tests/load/k6/script.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const failRate = new Rate('failed_requests');

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // ramp up
    { duration: '2m',  target: 100 },  // steady state
    { duration: '30s', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(99)<500'],   // 99% requests < 500ms
    failed_requests: ['rate<0.01'],     // < 1% failures
  },
};

export default function() {
  const params = { headers: { Authorization: `Bearer ${__ENV.TOKEN}` } };
  const res = http.get('http://localhost:8002/api/v1/journal/trades?limit=50', params);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  failRate.add(res.status !== 200);
  sleep(1);
}
// Run: k6 run --env TOKEN=<jwt> tests/load/k6/script.js
```

---

## Anti-Patterns

```
✗ Load testing with a single user (doesn't reveal concurrency bugs)
✗ Running load tests against production (always use staging)
✗ Ignoring P99 (P50 looks fine but P99 is what users actually experience)
✗ Not monitoring DB connections during test (connection pool exhaustion is #1 cause)
✗ Load test accounts sharing state (create isolated test accounts)
✗ No warmup phase (cold start skews early results)
✗ Comparing absolute numbers across machines (compare relative changes on same hardware)
✗ Fixing symptoms not root cause (adding cache without fixing the slow query)
```
