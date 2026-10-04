---
name: load-test
description: Performance and load testing for HTTP APIs
activation_keywords: [load, performance, stress, benchmark, latency, throughput]
execution_mode: server
---

# Load Test Skill

Perform HTTP API load and performance testing:

- Concurrent requests simulation
- Request rate control (RPS)
- Duration-based or count-based tests
- Latency percentiles (p50, p95, p99)
- Throughput metrics (requests/sec)
- Error rate calculation

Use `builtin_load_test` tool with fields:
- `operation`: "run" | "stop" | "results"
- `url`: Target endpoint URL
- `method`: HTTP method (default: GET)
- `concurrency`: Number of concurrent users
- `requests`: Total number of requests
- `duration`: Test duration in seconds
- `rate`: Target requests per second
- `headers`: (optional) Request headers as JSON

Returns:
- Total/Successful/Failed requests
- Average/Min/Max latency
- Percentiles (p50, p90, p95, p99)
- Requests per second
- Error rate percentage