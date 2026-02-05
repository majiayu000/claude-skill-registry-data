---
name: cache-observability
description: "Track cache hit rates, latency, and detect cache-related issues"
triggers:
  - "cache metrics"
  - "Redis monitoring"
  - "cache hit rate"
  - "cache performance"
priority: 2
---

# Cache Observability

Cache is performance-critical. Track hit rate, latency, and evictions.

## Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `cache.hits` | Counter | Successful reads |
| `cache.misses` | Counter | Reads that missed |
| `cache.gets.duration` | Histogram | GET latency |
| `cache.evictions` | Counter | Keys evicted |
| `cache.memory.used` | Gauge | Memory consumption |

## Span Attributes

| Attribute | Example | Required |
|-----------|---------|----------|
| `cache.system` | redis, memcached | Yes |
| `cache.operation` | GET, SET | Yes |
| `cache.hit` | true/false | Yes |
| `cache.key_prefix` | user:* | Recommended (**not full key!**) |

## Hit Rate

```
hit_rate = cache.hits / (cache.hits + cache.misses)
```

- **Good:** >90%
- **Concerning:** <80% → Check TTL, warming strategy

## Issues to Detect

| Issue | Detection | Fix |
|-------|-----------|-----|
| **Low hit rate** | <80% | Tune TTL, warm cache |
| **Cache stampede** | Many misses for same key | Distributed locks |
| **High latency** | p99 >10ms | Check network, value size |
| **Memory pressure** | memory >90% of max | Eviction policy, sizing |

## Cache Wrapper Pattern

```
Before GET: Start timer
After GET:  Record duration, increment hits or misses, set cache.hit on span
```

## Anti-Patterns

- **Full keys in metrics** → High cardinality, use prefix only
- **No eviction monitoring** → Can't detect memory pressure
- **Ignoring serialization time** → Track total time including marshal

## References

- `references/platforms/{platform}/cache.md`
