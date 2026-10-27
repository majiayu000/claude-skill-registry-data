---
name: load-testing-k6
description: "Load and stress testing with Grafana k6, virtual user ramp-up, p95/p99 latency thresholds, and smoke testing."
---

# Load Testing (k6) Protocol

1. Define explicit SLA thresholds: http_req_duration: ['p(95)<500', 'p(99)<1000'].
2. Simulate realistic traffic with virtual user ramp-up and cool-down stages.
3. Run smoke tests in CI to detect performance regressions.
