---
name: performance-engineer
description: Performance engineering including load testing, profiling, bottleneck analysis, capacity planning, and performance optimization. Use when load testing applications, profiling performance, analyzing bottlenecks, or planning capacity.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Performance Engineering Skill

You are a Performance Engineer specializing in load testing, profiling, bottleneck analysis, and capacity planning. You understand how to identify performance issues, optimize systems, and ensure applications scale under load.

## Core Responsibilities

1. **Load Testing**
   - Test plan design
   - Performance scenarios
   - Stress testing
   - Chaos testing

2. **Profiling**
   - CPU profiling
   - Memory profiling
   - I/O profiling
   - Database query profiling

3. **Bottleneck Analysis**
   - Performance metrics analysis
   - Flame graphs
   - Latency analysis
   - Throughput optimization

4. **Capacity Planning**
   - Resource forecasting
   - Scaling strategies
   - Cost-performance optimization
   - What-if analysis

5. **Performance Optimization**
   - Code optimization
   - Database tuning
   - Caching strategies
   - Concurrency optimization

## Load Testing

### Test Plan Design

```yaml
# test-plan.yml
load_test_plan:
  objectives:
    - baseline: establish_normal_behavior
    - stress: find_breaking_point
    - soak: test_stability_over_time
    - spike: test_sudden_traffic
    - endurance: sustained_load

  test_types:
    baseline_test:
      duration: 10_minutes
      users: 100
      ramp: 2_minutes
      purpose: establish_baseline_metrics

    load_test:
      duration: 30_minutes
      users: 1000
      ramp: 5_minutes
      purpose: validate_sla_under_expected_load

    stress_test:
      duration: until_failure
      users: 10000
      ramp: 10_minutes
      purpose: find_capacity_limits

    spike_test:
      duration: 10_minutes
      users: 5000
      ramp: 10_seconds
      purpose: test_autoscaling

    soak_test:
      duration: 24_hours
      users: 1000
      ramp: 5_minutes
      purpose: detect_memory_leaks

  success_criteria:
    response_time:
      p50: < 100ms
      p95: < 500ms
      p99: < 1000ms

    throughput:
      rps: > 10000

    error_rate:
      http_5xx: < 0.1%
      http_4xx: < 1%

    resource_utilization:
      cpu: < 80%
      memory: < 80%
```

### k6 Load Testing

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const apiLatency = new Trend('api_latency');
const successfulReq = new Counter('successful_requests');

// Test configuration
export const options = {
  scenarios: {
    // Baseline: Normal load
    baseline: {
      executor: 'constant-vus',
      vus: 100,
      duration: '10m',
      startTime: '0s',
    },
    // Ramp up stress test
    ramp_up: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 1000 },
        { duration: '10m', target: 1000 },
        { duration: '5m', target: 0 },
      ],
      gracefulRampDown: '30s',
      startTime: '10m',
    },
    // Spike test
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 5000 },
        { duration: '5m', target: 5000 },
        { duration: '30s', target: 0 },
      ],
      startTime: '30m',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],   // Error rate under 1%
    errors: ['rate<0.01'],
  },
};

// Test data
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export function setup() {
  // Setup: Create test users, etc.
  return {
    authToken: 'test-token',
  };
}

export default function (data) {
  group('API Endpoints', () => {
    // GET /api/users
    group('Get Users', () => {
      const start = Date.now();
      const response = http.get(`${BASE_URL}/api/users`, {
        headers: {
          Authorization: `Bearer ${data.authToken}`,
        },
      });
      const duration = Date.now() - start;
      apiLatency.add(duration);

      const checkRes = check(response, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
      });

      if (!checkRes) {
        errorRate.add(1);
      } else {
        successfulReq.add(1);
        errorRate.add(0);
      }
    });

    // POST /api/orders
    group('Create Order', () => {
      const payload = JSON.stringify({
        userId: `user-${__VU}`,
        items: [
          { productId: 'prod-1', quantity: 2 },
          { productId: 'prod-2', quantity: 1 },
        ],
      });

      const response = http.post(`${BASE_URL}/api/orders`, payload, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${data.authToken}`,
        },
      });

      check(response, {
        'order created': (r) => r.status === 201,
        'response has orderId': (r) => r.json('orderId') !== undefined,
      });
    });

    // Simulate user think time
    sleep(Math.random() * 2 + 1);
  });
}

export function teardown(data) {
  // Cleanup: Delete test data
}
```

### Locust Load Testing

```python
# locustfile.py
from locust import HttpUser, task, between, events
import random
import json

class ApiUser(HttpUser):
    """Simulates API user behavior."""
    wait_time = between(1, 5)
    weight = 10

    def on_start(self):
        """Login and get token."""
        response = self.client.post("/api/auth/login", json={
            "username": f"user_{self.user_id}",
            "password": "testpass"
        })
        self.token = response.json()["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(5)
    def get_products(self):
        """Browse products."""
        self.client.get("/api/products", headers=self.headers)

    @task(3)
    def get_product_detail(self):
        """View product details."""
        product_id = random.randint(1, 1000)
        self.client.get(f"/api/products/{product_id}", headers=self.headers)

    @task(2)
    def add_to_cart(self):
        """Add item to cart."""
        self.client.post("/api/cart/items", json={
            "productId": random.randint(1, 1000),
            "quantity": random.randint(1, 5)
        }, headers=self.headers)

    @task(1)
    def checkout(self):
        """Complete purchase."""
        self.client.post("/api/orders", json={
            "items": [
                {"productId": random.randint(1, 1000), "quantity": 1}
            ]
        }, headers=self.headers)

class AdminUser(HttpUser):
    """Simulates admin user behavior."""
    wait_time = between(5, 10)
    weight = 1

    @task
    def admin_dashboard(self):
        self.client.get("/admin/dashboard", headers=self.headers)

# Event hooks
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Test started")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Test stopped")
    # Generate report
    stats = environment.runner.stats
    print(f"Total requests: {stats.total.num_requests}")
    print(f"Average response time: {stats.total.avg_response_time}")
```

## Profiling

### CPU Profiling

```python
# python-profiling.py
import cProfile
import pstats
import io
from functools import wraps
import time

def profile_cpu(func):
    """Decorator to profile CPU usage."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 functions
        print(s.getvalue())

        return result
    return wrapper

# Memory profiling
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function with memory profiling."""
    data = []
    for i in range(100000):
        data.append({'index': i, 'data': 'x' * 1000})
    return data

# Line profiler
from line_profiler import LineProfiler

profiler = LineProfiler()

@profiler
def process_data(items):
    """Profile line by line."""
    results = []
    for item in items:
        processed = item * 2
        results.append(processed)
    return sum(results)

# Usage
if __name__ == "__main__":
    process_data(range(10000))
    profiler.print_stats()
```

### Go Profiling

```go
// profiling.go
package main

import (
    "net/http"
    _ "net/http/pprof"
    "runtime"
)

func main() {
    // Enable profiling
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()

    // Your application
    runApplication()
}

// Profiling commands:
// CPU:     go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
// Memory:  go tool pprof http://localhost:6060/debug/pprof/heap
// Goroutines: curl http://localhost:6060/debug/pprof/goroutine?debug=1
// Trace:   curl http://localhost:6060/debug/pprof/trace?seconds=5 > trace.out
```

### Java Profiling (async-profiler)

```bash
# Download async-profiler
wget https://github.com/jvm-profiling-tools/async-profiler/releases/download/v2.9/profiler.sh

# CPU profiling
./profiler.sh -d 30 -f cpu.html PID

# Memory allocation profiling
./profiler.sh -d 30 -e alloc -f alloc.html PID

# Flame graph generation
./profiler.sh -d 30 -f flamegraph.html PID

# JFR (Java Flight Recorder)
java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp
jfr print recording.jfr
```

## Flame Graphs

```bash
# Generate flame graph from perf data
# Record
cd /tmp
perf record -F 99 -a -g -- sleep 60

# Fold stacks
git clone https://github.com/brendangregg/FlameGraph
cd FlameGraph
perf script | ./stackcollapse-perf.pl > out.perf-folded

# Generate SVG
./flamegraph.pl out.perf-folded > kernel.svg

# For specific process
perf record -F 99 -p PID -g -- sleep 60
perf script | ./stackcollapse-perf.pl > out.folded
./flamegraph.pl out.folded > app.svg
```

## Database Performance

### Query Analysis

```sql
-- PostgreSQL slow query analysis
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = '1000';
SELECT pg_reload_conf();

-- Find slow queries
SELECT
    query,
    calls,
    total_time,
    mean_time,
    max_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- Missing indexes
SELECT
    schemaname,
    tablename,
    attname AS column,
    n_tup_read,
    n_tup_fetch,
    n_tup_insert,
    n_tup_update,
    n_tup_delete
FROM pg_stats
WHERE schemaname = 'public'
  AND n_tup_read > 10000
ORDER BY n_tup_read DESC;

-- Table bloat
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Query Optimization

```sql
-- EXPLAIN ANALYZE
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.name;

-- Index optimization
CREATE INDEX CONCURRENTLY idx_orders_user_created
ON orders(user_id, created_at)
WHERE status = 'completed';

-- Partition large tables
CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

## Caching Strategies

```python
# caching-strategy.py
import functools
import time
from typing import Optional
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def memoize_with_ttl(seconds: int = 300):
    """Cache function results with TTL."""
    def decorator(func):
        cache = {}
        timestamps = {}

        @functools.wraps(func)
        def wrapper(*args):
            key = str(args)
            now = time.time()

            if key in cache:
                if now - timestamps[key] < seconds:
                    return cache[key]
                else:
                    del cache[key]
                    del timestamps[key]

            result = func(*args)
            cache[key] = result
            timestamps[key] = now
            return result

        return wrapper
    return decorator

def cache_with_redis(ttl: int = 300):
    """Redis-backed caching decorator."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Compute and cache
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result

        return wrapper
    return decorator

# Multi-level cache
class MultiLevelCache:
    """L1: In-memory, L2: Redis, L3: Database"""

    def __init__(self):
        self.l1_cache = {}  # Local dict
        self.l2_cache = redis_client

    def get(self, key: str) -> Optional[any]:
        # L1
        if key in self.l1_cache:
            return self.l1_cache[key]

        # L2
        value = self.l2_cache.get(key)
        if value:
            self.l1_cache[key] = value
            return value

        return None

    def set(self, key: str, value: any, l1_ttl: int = 60, l2_ttl: int = 300):
        self.l1_cache[key] = value
        self.l2_cache.setex(key, l2_ttl, value)

    def invalidate(self, key: str):
        self.l1_cache.pop(key, None)
        self.l2_cache.delete(key)
```

## Performance Metrics

### Key Performance Indicators

```yaml
# performance-kpis.yml
performance_metrics:
  latency:
    p50:
      target: < 50ms
      warning: 100ms
      critical: 500ms

    p95:
      target: < 200ms
      warning: 500ms
      critical: 1000ms

    p99:
      target: < 500ms
      warning: 1000ms
      critical: 2000ms

  throughput:
    rps:
      target: 10000
      minimum: 5000

    tps:
      target: 1000
      minimum: 500

  errors:
    error_rate:
      target: < 0.1%
      warning: 0.5%
      critical: 1%

    timeout_rate:
      target: < 0.01%
      warning: 0.1%
      critical: 0.5%

  resources:
    cpu_utilization:
      target: 50-70%
      warning: 80%
      critical: 90%

    memory_utilization:
      target: 60-70%
      warning: 80%
      critical: 90%

    disk_io:
      read_latency:
        target: < 10ms
        warning: 50ms

      write_latency:
        target: < 10ms
        warning: 50ms

  saturation:
    queue_depth:
      target: < 10
      warning: 50
      critical: 100

    connection_pool:
      utilization:
        target: < 70%
        warning: 85%
        critical: 95%
```

## Capacity Planning

```python
# capacity-planning.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class CapacityPlanner:
    """Plan capacity based on growth projections."""

    def __init__(self, metrics_data):
        self.data = pd.DataFrame(metrics_data)

    def forecast_growth(self, months_ahead=6):
        """Forecast resource needs."""
        # Simple linear projection
        current_usage = self.data['cpu_usage'].mean()
        growth_rate = self.calculate_growth_rate()

        projections = []
        for month in range(1, months_ahead + 1):
            projected = current_usage * (1 + growth_rate) ** month
            projections.append({
                'month': month,
                'projected_cpu': projected,
                'projected_memory': projected * 1.5,  # Assumption
                'projected_storage': projected * 10
            })

        return projections

    def calculate_growth_rate(self):
        """Calculate month-over-month growth."""
        monthly = self.data.resample('M')['requests'].sum()
        return monthly.pct_change().mean()

    def recommend_capacity(self, projections):
        """Recommend capacity changes."""
        recommendations = []

        for proj in projections:
            if proj['projected_cpu'] > 80:
                recommendations.append({
                    'month': proj['month'],
                    'action': 'scale_out',
                    'reason': f"CPU projected at {proj['projected_cpu']:.1f}%",
                    'additional_nodes': int((proj['projected_cpu'] - 70) / 10)
                })

        return recommendations

    def cost_projection(self, projections, instance_cost=100):
        """Project infrastructure costs."""
        costs = []
        for proj in projections:
            nodes_needed = int(proj['projected_cpu'] / 70) + 1
            monthly_cost = nodes_needed * instance_cost
            costs.append({
                'month': proj['month'],
                'nodes': nodes_needed,
                'monthly_cost': monthly_cost
            })
        return costs
```

## Performance Test Report Template

```markdown
# Performance Test Report

## Executive Summary
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Avg Response Time | < 100ms | 85ms | ✅ Pass |
| P95 Response Time | < 500ms | 420ms | ✅ Pass |
| Throughput | > 10k RPS | 12k RPS | ✅ Pass |
| Error Rate | < 0.1% | 0.05% | ✅ Pass |

## Test Configuration
- **Duration**: 1 hour
- **Concurrent Users**: 5,000
- **Ramp Up**: 5 minutes
- **Test Environment**: Production-like

## Bottlenecks Identified
1. Database connection pool exhaustion at 3k users
2. Cache miss rate 45% on product catalog
3. Memory leak in payment service

## Recommendations
1. Increase DB connection pool to 200
2. Implement cache warming
3. Fix memory leak in payment service

## Next Steps
- Re-test after fixes
- Add soak test for 24 hours
- Test disaster recovery scenario
```
