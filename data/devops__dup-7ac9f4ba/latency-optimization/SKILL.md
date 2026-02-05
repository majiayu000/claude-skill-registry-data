---
name: latency-optimization
description: Use when optimizing end-to-end latency, reducing response times, or improving performance for latency-sensitive applications. Covers latency budgets, geographic routing, protocol optimization, and latency measurement techniques.
allowed-tools: Read, Glob, Grep
---

# Latency Optimization

Comprehensive guide to reducing end-to-end latency in distributed systems - from network to application to database layers.

## When to Use This Skill

- Optimizing response times for user-facing applications
- Creating latency budgets for distributed systems
- Implementing geographic routing strategies
- Reducing database query latency
- Optimizing API response times
- Understanding and measuring latency components

## Latency Fundamentals

### Understanding Latency

```text
Latency Components:

Total Latency = Network + Processing + Queue + Serialization

┌─────────────────────────────────────────────────────────────┐
│                     Request Journey                          │
│                                                              │
│  Client ──► DNS ──► TCP ──► TLS ──► Server ──► DB ──► Back  │
│                                                              │
│  Components:                                                 │
│  ├── DNS Resolution: 0-100ms (cached: 0ms)                  │
│  ├── TCP Handshake: 1 RTT (~10-200ms)                       │
│  ├── TLS Handshake: 1-2 RTT (~20-400ms)                     │
│  ├── Request Transfer: depends on size                       │
│  ├── Server Processing: application-specific                 │
│  ├── Database Query: 1-1000ms typical                       │
│  └── Response Transfer: depends on size                      │
└─────────────────────────────────────────────────────────────┘

Key Metrics:
- P50: Median latency (50th percentile)
- P95: 95th percentile (tail latency starts)
- P99: 99th percentile (important for SLOs)
- P99.9: Three nines (critical systems)
```

### Latency Numbers Every Developer Should Know

```text
Latency Reference (2024 estimates):

Operation                              Time
─────────────────────────────────────────────────────
L1 cache reference                     1 ns
L2 cache reference                     4 ns
Branch mispredict                      5 ns
L3 cache reference                     10 ns
Mutex lock/unlock                      25 ns
Main memory reference                  100 ns
Compress 1KB with Snappy              2,000 ns (2 μs)
SSD random read                       16,000 ns (16 μs)
Read 1 MB from memory                 50,000 ns (50 μs)
Read 1 MB from SSD                    200,000 ns (200 μs)
Round trip same datacenter            500,000 ns (500 μs)
Read 1 MB from network (1Gbps)        10,000,000 ns (10 ms)
HDD random read                       10,000,000 ns (10 ms)
Round trip US East to US West         40,000,000 ns (40 ms)
Round trip US to Europe               80,000,000 ns (80 ms)
Round trip US to Asia                 150,000,000 ns (150 ms)

Key Insights:
- Memory is 100x faster than SSD
- Same-datacenter is 80x faster than cross-continent
- Caching at any level provides huge wins
```

### Latency Budget

```text
Latency Budget Example (200ms target):

┌─────────────────────────────────────────────────────────────┐
│                    200ms Total Budget                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │ Network  │   Auth   │  Service │    DB    │ Response │  │
│  │   50ms   │   20ms   │   50ms   │   60ms   │   20ms   │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│                                                              │
│  Breakdown:                                                  │
│  ├── Network (client → edge → origin): 50ms                 │
│  ├── Authentication/Authorization: 20ms                      │
│  ├── Service Processing: 50ms                               │
│  ├── Database Queries: 60ms                                 │
│  └── Response Serialization + Transfer: 20ms                │
└─────────────────────────────────────────────────────────────┘

Budget Rules:
1. Allocate budgets based on criticality
2. Leave 10-20% headroom for variance
3. Monitor P99 against budget
4. Alert when consistently over budget
5. Renegotiate budgets as system evolves
```

## Network Latency Optimization

### Geographic Routing

```text
Geographic Routing Strategies:

1. GeoDNS Routing
   User IP ──► DNS Resolver ──► Nearest Server IP

   Pros: Simple, works everywhere
   Cons: DNS caching, IP geolocation inaccuracy

2. Anycast Routing
   Same IP advertised from multiple locations
   BGP routes to nearest (network topology)

   Pros: Instant failover, no DNS delay
   Cons: Requires BGP expertise, stateful sessions tricky

3. Load Balancer Geo-routing
   Global LB ──► Regional LB ──► Servers

   Pros: Fine-grained control, health checking
   Cons: Adds latency hop, more complex

Selection Guide:
┌──────────────────┬─────────────────────────────────────┐
│ Use Case         │ Recommended Approach                │
├──────────────────┼─────────────────────────────────────┤
│ Static content   │ Anycast CDN                         │
│ API services     │ GeoDNS + Regional deployments       │
│ Real-time apps   │ Anycast + Connection persistence    │
│ Stateful apps    │ GeoDNS with session affinity        │
└──────────────────┴─────────────────────────────────────┘
```

### Protocol Optimization

```text
Protocol-Level Optimizations:

1. HTTP/2 Benefits
   ├── Multiplexing (no head-of-line blocking)
   ├── Header compression (HPACK)
   ├── Server push (preemptive responses)
   └── Single connection (reduced handshakes)

   Latency Impact: 20-50% improvement typical

2. HTTP/3 (QUIC) Benefits
   ├── 0-RTT connection resumption
   ├── No TCP head-of-line blocking
   ├── Built-in encryption
   └── Connection migration (IP changes)

   Latency Impact: 10-30% over HTTP/2

3. TLS Optimization
   ├── TLS 1.3 (1-RTT handshake)
   ├── Session resumption (0-RTT)
   ├── OCSP stapling (no CA roundtrip)
   └── Certificate chain optimization

   Latency Impact: 50-200ms saved per connection

4. TCP Optimization
   ├── TCP Fast Open (TFO)
   ├── Increased initial congestion window
   ├── BBR congestion control
   └── Keep-alive for connection reuse
```

### Connection Optimization

```text
Connection Strategies:

1. Connection Pooling
   ┌─────────────────────────────────────────┐
   │           Connection Pool               │
   │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
   │  │Conn1│ │Conn2│ │Conn3│ │Conn4│      │
   │  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘      │
   └─────┼──────┼──────┼──────┼────────────┘
         │      │      │      │
      Reuse connections, avoid handshake cost

2. Preconnect/Prefetch
   <link rel="preconnect" href="https://api.example.com">
   <link rel="dns-prefetch" href="https://cdn.example.com">

   Triggers early connection establishment

3. Connection Coalescing (HTTP/2)
   Multiple domains → single connection
   (When sharing same IP and certificate)
```

## Application Latency Optimization

### Caching Strategies

```text
Caching Layers:

┌─────────────────────────────────────────────────────────────┐
│                    Caching Hierarchy                         │
│                                                              │
│  Browser ──► CDN Edge ──► App Cache ──► DB Cache ──► DB     │
│    1ms        10ms          20ms         50ms       100ms   │
│                                                              │
│  Each layer should catch most requests before next layer    │
└─────────────────────────────────────────────────────────────┘

Cache Type Selection:
┌──────────────────┬─────────────────┬────────────────────────┐
│ Data Type        │ Cache Location  │ TTL Strategy           │
├──────────────────┼─────────────────┼────────────────────────┤
│ Static assets    │ CDN + Browser   │ Long (1 year), hashed  │
│ API responses    │ CDN + App       │ Short (seconds-mins)   │
│ Session data     │ App (Redis)     │ Session duration       │
│ DB query results │ App (local/dist)│ Varies by query        │
│ Computed results │ App             │ Based on input staleness│
└──────────────────┴─────────────────┴────────────────────────┘
```

### Async Processing

```text
Async Patterns for Latency:

1. Background Processing
   Request ──► Validate ──► Queue ──► Response (fast)
                             │
                             └──► Worker (async processing)

   User sees fast response, heavy work happens later

2. Parallel Requests
   Sequential:
   A(100ms) → B(100ms) → C(100ms) = 300ms

   Parallel:
   A(100ms) ─┐
   B(100ms) ─┼──► 100ms total
   C(100ms) ─┘

3. Speculative Execution
   Start likely-needed work before confirmed
   Cancel if not needed
   Risk: Wasted resources if prediction wrong

4. Read-Your-Writes with Async
   Write ──► Queue ──► Response + Local Cache Update
                         │
         User sees their write immediately
         Backend processes asynchronously
```

### Serialization Optimization

```text
Serialization Format Comparison:

Format        Encode    Decode    Size      Human
              Speed     Speed     (relative) Readable
─────────────────────────────────────────────────────
JSON          Fast      Fast      Large     Yes
MessagePack   V.Fast    V.Fast    Small     No
Protocol Buf  Fast      V.Fast    V.Small   No
FlatBuffers   Zero-copy V.Fast    Small     No
Avro          Fast      Fast      Small     Schema

Recommendations:
- Internal services: Protocol Buffers or MessagePack
- Public APIs: JSON (compatibility) or gRPC (performance)
- High-throughput: FlatBuffers (zero-copy)
- Schema evolution: Avro or Protocol Buffers

Optimization Tips:
1. Avoid serializing unnecessary fields
2. Use streaming for large payloads
3. Compress large responses (gzip/brotli)
4. Consider binary formats for internal traffic
```

## Database Latency Optimization

### Query Optimization

```text
Database Latency Patterns:

1. Index Optimization
   ❌ Full table scan: O(n) - slow
   ✓ Index lookup: O(log n) - fast
   ✓ Covering index: No table lookup needed

   Monitor: Slow query logs, EXPLAIN plans

2. Query Patterns
   ❌ N+1 queries: 1 + N roundtrips
   ✓ Batch queries: 1 roundtrip
   ✓ JOINs (when appropriate): 1 roundtrip

   Example:
   ❌ for user in users: get_orders(user.id)  # N queries
   ✓ get_orders_for_users(user_ids)           # 1 query

3. Connection Management
   ├── Connection pooling (avoid connection overhead)
   ├── Prepared statements (avoid parsing overhead)
   └── Connection proximity (same region as app)

4. Read Replicas
   ┌─────────────────────────────────────────┐
   │  Writes ──► Primary                     │
   │  Reads  ──► Read Replica (lower latency)│
   └─────────────────────────────────────────┘
```

### Database Proximity

```text
Database Placement Strategies:

1. Co-located Database
   App and DB in same availability zone
   Latency: <1ms
   Best for: Primary workloads

2. Same-Region Replica
   Read replica in same region
   Latency: 1-5ms
   Best for: Read scaling

3. Cross-Region Replica
   Replica in user's region
   Latency: Local (~5ms) vs cross-region (~100ms)
   Best for: Global read-heavy apps

4. Globally Distributed
   Database spans regions (CockroachDB, Spanner)
   Write latency: Higher (consensus)
   Read latency: Local
   Best for: Global consistency requirements
```

## Measurement and Monitoring

### Latency Measurement

```text
Measurement Points:

1. Client-Side (Real User Monitoring)
   └── Measures actual user experience
   └── Includes network variability
   └── Tools: Browser timing API, RUM services

2. Edge/CDN Metrics
   └── Time to first byte (TTFB)
   └── Cache hit ratio
   └── Origin fetch time

3. Server-Side (APM)
   └── Request processing time
   └── Downstream service calls
   └── Database query time
   └── Tools: OpenTelemetry, APM vendors

4. Synthetic Monitoring
   └── Consistent measurement conditions
   └── Multiple geographic locations
   └── Baseline for comparison

Distributed Tracing:
┌─────────────────────────────────────────────────────────────┐
│  Request ──► Gateway ──► Service A ──► Service B ──► DB    │
│    │           │            │            │           │      │
│    └───────────┴────────────┴────────────┴───────────┘      │
│              Trace ID links all spans together              │
│              Each span has start time + duration            │
└─────────────────────────────────────────────────────────────┘
```

### Latency SLOs

```text
Setting Latency SLOs:

1. Define Meaningful Metrics
   - P50: Typical experience
   - P95: Most users' worst case
   - P99: Tail latency for critical paths

2. Set Realistic Targets
   P50: 50ms    (snappy feel)
   P95: 200ms   (acceptable)
   P99: 500ms   (degraded but functional)

3. Error Budget Approach
   If target is P99 < 500ms with 99.9% SLO:
   - Budget: 0.1% of requests can exceed 500ms
   - ~43 minutes per month of violations allowed

4. Alert Thresholds
   ├── Warning: P99 > 400ms (80% of budget)
   ├── Critical: P99 > 500ms (at budget)
   └── Page: P99 > 600ms for 5 minutes (over budget)
```

## Common Anti-Patterns

```text
Latency Anti-Patterns:

1. "Chattiness"
   ❌ Many small requests instead of batched
   ✓ Batch requests, use GraphQL, aggregate APIs

2. "Synchronous Chains"
   ❌ A → B → C → D (sequential)
   ✓ Parallelize independent calls, use async

3. "Unbounded Queries"
   ❌ SELECT * without limits or pagination
   ✓ Always paginate, limit result sets

4. "Cache Miss Storms"
   ❌ Cache expires, all requests hit origin
   ✓ Staggered TTLs, request coalescing, warm cache

5. "Logging in Hot Path"
   ❌ Synchronous logging on every request
   ✓ Async logging, sampling for high volume

6. "Premature Serialization"
   ❌ Serialize before knowing if needed
   ✓ Lazy serialization, stream when possible

7. "Ignoring Tail Latency"
   ❌ Only monitoring averages
   ✓ Track P95, P99, P99.9 for user experience
```

## Best Practices

```text
Latency Optimization Best Practices:

1. Measure First
   □ Establish baseline measurements
   □ Identify bottlenecks before optimizing
   □ Use distributed tracing
   □ Monitor percentiles, not just averages

2. Optimize Strategically
   □ Start with biggest bottlenecks
   □ Apply latency budgets
   □ Consider cost vs benefit
   □ Test optimizations under load

3. Network Layer
   □ Deploy close to users (CDN, edge)
   □ Use modern protocols (HTTP/2, HTTP/3)
   □ Optimize TLS (1.3, session resumption)
   □ Connection pooling and keep-alive

4. Application Layer
   □ Cache aggressively and appropriately
   □ Parallelize independent operations
   □ Use async processing for non-critical work
   □ Optimize serialization formats

5. Data Layer
   □ Index frequently queried columns
   □ Use read replicas for read-heavy loads
   □ Connection pooling
   □ Query optimization (avoid N+1)

6. Continuous Improvement
   □ Regular latency reviews
   □ Load testing with latency assertions
   □ Automated regression detection
   □ User experience correlation
```

## Related Skills

- `caching-strategies` - Application-level caching patterns
- `multi-region-deployment` - Geographic distribution
- `cdn-architecture` - Edge caching and delivery
- `distributed-tracing` - End-to-end latency visibility
