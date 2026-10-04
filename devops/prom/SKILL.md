---
name: Prometheus
slug: prom
version: 1.0.0
description: Prometheus monitoring patterns, cardinality management, alerting best practices, and PromQL traps.
homepage: https://clawic.com/skills/prom
metadata:
  category: infrastructure
  skills:
  - prometheus
  - monitoring
  - alerting
  - metrics
  - observability
  clawdbot:
    emoji: 🎉
    displayName: Prometheus
---

## Cardinality Explosions

- Every unique label combination creates a new time series — `user_id` as label kills Prometheus
- Avoid high-cardinality labels: user IDs, email addresses, request IDs, timestamps, UUIDs
- Check cardinality: `prometheus_tsdb_head_series` metric — above 1M series needs attention
- Use histograms for latency, not per-request labels — buckets are fixed cardinality
- Relabeling can drop dangerous labels before ingestion: `labeldrop` in scrape config

## Histogram vs Summary

- Histograms: use for SLOs, aggregatable across instances, buckets defined upfront
- Summaries: use when you need exact percentiles, cannot aggregate across instances
- Histogram bucket boundaries must be defined before data arrives — wrong buckets = wrong percentiles
- Default buckets (.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10) assume HTTP latency — adjust for your use case

## Rate and Increase

- `rate()` requires range selector at least 4x scrape interval — `rate(metric[1m])` with 30s scrape misses data
- `rate()` is per-second, `increase()` is total over range — don't confuse them
- Counter resets on restart — `rate()` handles this, raw delta doesn't
- `irate()` uses only last two samples — too spiky for alerting, use `rate()` for alerts

## Alerting Mistakes

- Alert on symptoms, not causes — "high latency" not "high CPU"
- `for` clause prevents flapping: `for: 5m` means condition must hold 5 minutes before firing
- Missing `for` clause = fires immediately on first match = noisy
- Alerts need `runbook_url` label — on-call needs to know what to do, not just that something's wrong
- Test alerts with `promtool check rules` — syntax errors discovered at 3am are bad

## PromQL Traps

- `and` is intersection by labels, not boolean AND — results must have matching label sets
- `or` fills in missing series, doesn't do boolean OR on values
- `{}` without metric name is expensive — scans all metrics
- `offset` goes back in time: `metric offset 1h` is value from 1 hour ago
- Comparison operators filter series: `http_requests > 100` drops series below 100, doesn't return boolean

## Scrape Configuration

- `honor_labels: true` trusts source labels — use only when source is authoritative (e.g., Pushgateway)
- `scrape_timeout` must be less than `scrape_interval` — otherwise overlapping scrapes
- Static configs don't reload without restart — use file_sd or service discovery for dynamic targets
- TLS verification disabled (`insecure_skip_verify`) should be temporary, never permanent

## Pushgateway Pitfalls

- Pushgateway is for batch jobs, not services — services should expose /metrics
- Metrics persist until deleted — stale metrics from dead jobs confuse dashboards
- Add job and instance labels to distinguish sources — default grouping hides failures
- Delete metrics when job completes: `curl -X DELETE http://pushgateway/metrics/job/myjob`

## Recording Rules

- Pre-compute expensive queries: `record: job:request_duration_seconds:rate5m`
- Naming convention: `level:metric:operations` — helps identify what rules produce
- Recording rules update every evaluation interval — not instant, plan for slight delay
- Reduce cardinality with recording rules: aggregate away labels you don't need for alerting

## Federation and Remote Write

- Federation for pulling from other Prometheus — use sparingly, adds latency
- Remote write for long-term storage — Prometheus local storage is not durable
- Remote write can buffer during outages — but buffer is finite, data loss on extended outages
- Prometheus is not highly available by default — run two instances scraping same targets

## Common Operational Issues

- TSDB corruption on unclean shutdown — use `--storage.tsdb.wal-compression` and monitor disk space
- Memory grows with series count — each series costs ~3KB RAM
- Compaction pauses during high load — leave 40% disk headroom
- Scrape targets stuck "Unknown" — check network, firewall, target actually exposing /metrics

## Label Best Practices

- Use labels for dimensions you'll filter/aggregate by — environment, service, instance
- Keep label values low-cardinality — tens or hundreds, not thousands
- Consistent naming: `snake_case`, prefix with domain: `http_requests_total`, `node_cpu_seconds_total`
- `le` label is reserved for histogram buckets — don't use for other purposes
