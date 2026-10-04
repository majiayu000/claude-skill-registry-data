---
name: go-samber-hot
description: "In-memory caching for Go with samber/hot. Covers eviction algorithms (LRU, LFU, W-TinyLFU), TTL, loaders, and metrics."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:25:00 GMT
---

## Core Philosophy

`samber/hot` is a comprehensive, type-safe in-memory caching library for Go (1.22+). It supports 9+ eviction algorithms and high-performance features like singleflight deduplication and sharding.

- **Type-safe**: Generic `HotCache[K, V]`.
- **Flexible**: Choose from LRU, LFU, W-TinyLFU, S3FIFO, etc.
- **Production-Ready**: Built-in TTL, janitor cleanup, and Prometheus metrics.

## Common Algorithms

| Algorithm | Best For |
| --- | --- |
| **W-TinyLFU** | **Default.** Best general-purpose choice for mixed workloads. |
| **LRU** | Recency-based access (e.g., user sessions). |
| **LFU** | Frequency-based access (e.g., popular static items). |
| **S3FIFO** | High-throughput, scan-resistant workloads. |
| **FIFO** | Simple expiration in exact order of creation. |

## Basic Usage

### Simple Cache with TTL
```go
import "github.com/samber/hot"

cache := hot.NewHotCache[string, *User](hot.WTinyLFU, 10000).
    WithTTL(5 * time.Minute).
    WithJanitor(). // Background cleanup
    Build()
defer cache.StopJanitor()

cache.Set("user:123", user)
val, found, _ := cache.Get("user:123")
```

### Loaders (Read-Through)
Automatically fetch missing keys and deduplicate concurrent requests for the same key.
```go
cache := hot.NewHotCache[int, *User](hot.WTinyLFU, 10000).
    WithLoaders(func(ids []int) (map[int]*User, error) {
        return db.GetUsers(ids) // Batch fetch
    }).
    Build()

user, found, err := cache.Get(123) // Triggers loader if missing
```

## Capacity Planning

Estimate memory usage before setting capacity:
`Total Memory = Capacity * (Item Size + Overhead)`
Overhead is roughly 100 bytes per entry for internal metadata.

## Best Practices

1. **Always use TTL** — Prevents unbounded growth and serves as a safety net against stale data.
2. **Enable the Janitor** — Use `WithJanitor()` to proactively remove expired items; otherwise, they only leave when the cache is full.
3. **Use Jitter** — Use `WithJitter` to prevent "thundering herd" issues where many items expire at the exact same second.
4. **Monitor Hit Rate** — Integrate `WithPrometheusMetrics` to ensure your cache size and algorithm are effective.
5. **Copy on Read/Write** — If cached items are mutable, use `WithCopyOnRead` to prevent different callers from corrupting the same shared object.

## Anti-patterns

- ❌ **Ignoring Errors from Loaders** — Always check the `err` return from `Get()`.
- ❌ **Unsized Caches** — Not setting a reasonable capacity can lead to Out Of Memory (OOM) errors.
- ❌ **Using LRU for All Workloads** — LRU is susceptible to "scan pollution" (a large sequential read evicting everything hot). Use `WTinyLFU` if unsure.
- ❌ **Global Unprotected Mutables** — Modifying an object returned by `Get()` without copying it first.
