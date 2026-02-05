---
name: estimation-techniques
description: Back-of-envelope calculations for system design. Use when estimating QPS, storage, bandwidth, or latency for capacity planning. Includes latency numbers every programmer should know and common estimation patterns.
allowed-tools: Read, Glob, Grep
---

# Estimation Techniques

This skill provides frameworks for back-of-envelope calculations essential for system design and capacity planning.

## When to Use This Skill

**Keywords:** back-of-envelope, estimation, QPS, storage calculation, bandwidth, latency, capacity planning, scale estimation

**Use this skill when:**

- Estimating system capacity requirements
- Calculating storage needs for a feature
- Determining bandwidth requirements
- Sizing infrastructure for expected load
- Justifying architectural decisions with numbers
- Preparing for system design interviews

## Core Principle

**Estimation is not about precision, it's about order of magnitude.**

Getting within 10x is usually good enough for architectural decisions. The goal is to identify if you need:

- 1 server or 100 servers
- 1 GB or 1 TB of storage
- 10 ms or 1 second latency

## Essential Numbers to Know

### Powers of 2

| Power | Value | Approximate |
| ----- | ----- | ----------- |
| 2^10 | 1,024 | ~1 Thousand (KB) |
| 2^20 | 1,048,576 | ~1 Million (MB) |
| 2^30 | 1,073,741,824 | ~1 Billion (GB) |
| 2^40 | 1,099,511,627,776 | ~1 Trillion (TB) |

### Time Conversions

| Unit | Seconds | Useful For |
| ---- | ------- | ---------- |
| 1 minute | 60 | Short operations |
| 1 hour | 3,600 | Batch jobs |
| 1 day | 86,400 (~100K) | Daily aggregations |
| 1 month | 2,592,000 (~2.5M) | Monthly calculations |
| 1 year | 31,536,000 (~30M) | Annual projections |

### Availability Targets

| Availability | Downtime/Year | Downtime/Month | Downtime/Day |
| ------------ | ------------- | -------------- | ------------ |
| 99% (two 9s) | 3.65 days | 7.31 hours | 14.4 min |
| 99.9% (three 9s) | 8.76 hours | 43.8 min | 1.44 min |
| 99.99% (four 9s) | 52.6 min | 4.38 min | 8.64 sec |
| 99.999% (five 9s) | 5.26 min | 26.3 sec | 864 ms |

### Latency Numbers Every Programmer Should Know

**See full reference:** `references/latency-numbers.md`

Quick reference:

| Operation | Latency | Relative |
| --------- | ------- | -------- |
| L1 cache reference | 0.5 ns | 1x |
| L2 cache reference | 7 ns | 14x |
| Main memory reference | 100 ns | 200x |
| SSD random read | 16 us | 32,000x |
| HDD seek | 2 ms | 4,000,000x |
| Round trip same datacenter | 0.5 ms | 1,000,000x |
| Round trip CA to Netherlands | 150 ms | 300,000,000x |

## Estimation Patterns

### Pattern 1: QPS (Queries Per Second)

#### Formula

```text
QPS = (Number of Users) x (Actions per User per Day) / (Seconds per Day)
```

#### Example: Twitter-like service

```text
Given:
- 300 million monthly active users
- 50% are daily active = 150M DAU
- Average user reads 20 tweets/day

QPS = 150M * 20 / 86,400
    = 3 billion / 100,000
    = 30,000 QPS

Peak load (typically 2-3x average):
Peak QPS = 30,000 * 3 = 90,000 QPS
```

### Pattern 2: Storage Estimation

#### Formula

```text
Storage = (Number of Items) x (Size per Item) x (Replication Factor) x (Time Period)
```

#### Example: Photo storage service

```text
Given:
- 100 million users
- 10% upload daily = 10M uploads/day
- Average photo size = 2 MB
- Keep 5 years of data
- Replication factor = 3

Daily storage = 10M * 2 MB = 20 TB
Yearly storage = 20 TB * 365 = 7.3 PB
5-year storage = 7.3 * 5 = 36.5 PB
With replication = 36.5 * 3 = ~110 PB
```

### Pattern 3: Bandwidth Estimation

#### Formula

```text
Bandwidth = (QPS) x (Request Size or Response Size)
```

#### Example: Video streaming service

```text
Given:
- 1 million concurrent viewers
- Average bitrate = 5 Mbps
- Peak hours: 8 PM - 11 PM

Bandwidth = 1M * 5 Mbps = 5 Tbps

With 20% overhead: ~6 Tbps

CDN egress cost (rough):
$0.02/GB * 6 Tbps * 3 hours * 3600 sec/hour / 8 bits/byte
= massive cost (hence why Netflix built their own CDN)
```

### Pattern 4: Cache Size Estimation

#### Formula

```text
Cache Size = (QPS) x (Cache TTL) x (Response Size) x (Unique Ratio)
```

#### Example: API response cache

```text
Given:
- 10,000 QPS
- Cache TTL = 5 minutes = 300 seconds
- Average response = 10 KB
- 20% of requests are unique

Cache entries = 10,000 * 300 * 0.20 = 600,000 entries
Cache size = 600,000 * 10 KB = 6 GB

With overhead (keys, metadata): ~10 GB
```

### Pattern 5: Database Sizing

#### Formula

```text
DB Size = (Number of Rows) x (Row Size) x (Index Overhead) x (Replication)
```

#### Example: User profile database

```text
Given:
- 500 million users
- Average profile = 1 KB (name, email, settings, etc.)
- Index overhead = 30%
- Primary + 2 replicas = 3x

Data size = 500M * 1 KB = 500 GB
With indexes = 500 GB * 1.3 = 650 GB
With replication = 650 GB * 3 = ~2 TB

Memory for hot data (20%): ~400 GB
```

## Common Estimation Scenarios

### Scenario 1: URL Shortener

```text
Requirements:
- 100M new URLs/month
- 10:1 read:write ratio

Writes:
- 100M / (30 * 24 * 3600) = ~40 writes/second
- Peak: ~100 writes/second

Reads:
- 40 * 10 = 400 reads/second
- Peak: ~1000 reads/second

Storage (5 years):
- 100M URLs/month * 60 months = 6 billion URLs
- Average URL = 100 bytes (short) + 500 bytes (long) = 600 bytes
- 6B * 600 bytes = 3.6 TB
- With indexes and overhead: ~5 TB
```

### Scenario 2: Chat Application

```text
Requirements:
- 10M daily active users
- Average 50 messages sent/day
- Average 200 messages received/day

Message throughput:
- Sends: 10M * 50 / 86,400 = ~6,000 messages/second
- Peak: ~20,000 messages/second

Connections:
- Each user maintains 1-3 connections (phone, laptop, tablet)
- Peak concurrent: 10M * 0.1 (10% online) * 2 = 2M connections

Storage (1 year):
- 10M users * 50 msgs/day * 365 days = 182B messages/year
- Average message = 200 bytes
- 182B * 200 bytes = 36.4 TB/year
```

### Scenario 3: Video Streaming

```text
Requirements:
- 100M monthly active users
- 30% watch daily = 30M DAU
- Average 1 hour/day viewing

Concurrent viewers (peak):
- 30M DAU / 24 hours * 3 (peak factor) = ~4M concurrent

Bandwidth:
- Average stream: 5 Mbps
- 4M * 5 Mbps = 20 Tbps peak bandwidth

Storage (library of 10K titles):
- Average video = 2 hours
- Multiple qualities: 480p (1GB), 720p (3GB), 1080p (5GB), 4K (20GB)
- Per title: ~30 GB
- Library: 10K * 30 GB = 300 TB
```

## Estimation Tips

### Round Aggressively

```text
Instead of:      Use:
86,400 seconds   ~100,000 (10^5)
2.5 million      ~3 million
7.3 petabytes    ~10 petabytes
```

### Use Orders of Magnitude

Think in powers of 10:

- Thousands (10^3)
- Millions (10^6)
- Billions (10^9)
- Trillions (10^12)

### State Your Assumptions

Always verbalize:

- "I'm assuming 10% of users are active at peak"
- "I'm estimating average message size at 200 bytes"
- "I'm using a 3x replication factor"

### Sanity Check Results

After calculating, ask:

- "Does this make sense?"
- "Is this in the right order of magnitude?"
- "What would change if my assumption is off by 10x?"

## Common Mistakes

### Mistake 1: Ignoring Peak vs Average

#### Problem

Sizing for average load.

```text
Average QPS: 10,000
Peak QPS: 30,000 (often 2-3x average)

If you size for 10,000, you'll fail at peak.
```

### Mistake 2: Forgetting Replication

#### Problem

Calculating raw storage without copies.

```text
Data: 1 TB
With 3 replicas: 3 TB
With backups: 4-5 TB
```

### Mistake 3: Not Accounting for Growth

#### Problem

Sizing for current, not future.

```text
Current users: 10M
Expected growth: 50%/year
Year 3: 10M * 1.5^3 = 34M users

Size for at least 2x current to avoid near-term issues.
```

### Mistake 4: Over-Precision

#### Problem

Calculating to 3 decimal places.

```text
Bad: "We need exactly 3,456,789 IOPS"
Good: "We need roughly 3-4 million IOPS"
```

## Quick Reference Calculations

| Need | Formula |
| ---- | ------- |
| QPS | users * actions/day / 86400 |
| Storage/day | items/day * size/item |
| Bandwidth | QPS * response_size |
| Cache hit rate | 1 - (DB_QPS / total_QPS) |
| Servers needed | QPS / QPS_per_server |
| Shards needed | data_size / max_shard_size |

## Related Skills

- `design-interview-methodology` - Overall interview framework
- `quality-attributes-taxonomy` - NFR definitions (scalability, performance)
- `database-scaling` - Database capacity planning (Phase 3)
- `caching-strategies` - Cache sizing and hit rates (Phase 3)

## Related Commands

- `/sd:estimate <scenario>` - Calculate capacity interactively

## Related Agents

- `capacity-planner` - Guided estimation with calculations

## References

- `references/latency-numbers.md` - Complete latency reference table

---

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
