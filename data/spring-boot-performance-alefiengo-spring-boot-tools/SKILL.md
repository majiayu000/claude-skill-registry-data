---
name: spring-boot-performance
description: >
  Performance diagnosis and optimization in Spring Boot: N+1 queries,
  caching (@Cacheable), connection pool tuning, virtual threads, lazy
  loading and bounded pagination. Use when slow endpoints, N+1 queries,
  timeouts, or high resource consumption are reported.
---

# Performance

## Measure before tuning

Define the affected operation, reproducible workload and acceptance threshold. Capture a baseline with environment/data volume, client/server p95/p99, throughput/errors and the relevant query count/plan, pool wait, GC and CPU metrics. Change one hypothesis at a time, rerun the same workload and report before/after plus tradeoffs.

Do not increase pools merely because requests are slow: database capacity and query duration bound useful concurrency. Do not add indexes without a representative plan and write/storage impact. Do not add caches without ownership, invalidation and stale-data tolerance. Virtual threads reduce thread costs; they do not increase downstream capacity. Inspect `actuator_health` for readiness and use observability for metrics/traces; use load-testing for a repeatable experiment.

## N+1 queries

Inspect the queries and accessed associations on the slow path. Either eager or lazy loading can produce N+1; prove it with emitted SQL/query count.

### Fix with JOIN FETCH / EntityGraph

```java
// Repository with JOIN FETCH
@Query("SELECT u FROM User u JOIN FETCH u.roles WHERE u.email = ?1")
Optional<User> findByEmailWithRoles(String email);

// Or with EntityGraph
@EntityGraph(attributePaths = {"roles", "projects"})
Optional<User> findByEmail(String email);
```

Fetching multiple collection associations can multiply rows or fail for multiple bags. Verify cardinality and memory cost; do not apply this graph indiscriminately. Collection fetch joins and pagination need particular care.

### Batch fetching

```yaml
spring.jpa.properties.hibernate.default_batch_fetch_size: 25
```

Can reduce round trips for lazily fetched associations; verify emitted SQL and pagination behavior.

### Detect N+1 in development

```yaml
logging.level.org.hibernate.SQL: DEBUG
logging.level.org.hibernate.stat: DEBUG
```

Enable `spring.jpa.properties.hibernate.generate_statistics: true` locally and inspect Hibernate statistics alongside SQL logs. A query-plan cache does not detect N+1 execution.

## Caching with `@Cacheable`

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

```yaml
spring:
  cache:
    type: caffeine  # or redis, couchbase. local caches require an explicit cross-instance consistency strategy
```

```java
@Cacheable(value = "users", key = "#email.toLowerCase()", unless = "#result == null")
public UserDTO findByEmail(String email) { ... }

@CacheEvict(value = "users", allEntries = true)
public void evictAll() { ... }
```

**Caffeine:** add `com.github.ben-manes.caffeine:caffeine`, enable caching with `@EnableCaching`, and configure `spring.cache.caffeine.spec: maximumSize=10000,expireAfterWrite=10m`. With Redis, use `spring.cache.redis.time-to-live: 10m`. Plan invalidation and whether per-instance caching is acceptable.

## Connection pool (Hikari)

Illustrative settings, not defaults to apply: choose each from measured workload, database limits and infrastructure timeouts.

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 2
      idle-timeout: 300000
      max-lifetime: 1800000
      connection-timeout: 2000
      leak-detection-threshold: 20000
```

- `leak-detection-threshold` logs a stack trace when a connection stays checked out longer than the value. Set it above the slowest legitimate transaction (20000 ms here is a placeholder). HikariCP's `HikariConfig` validation (source on the `dev` branch, read 2026-11-21) disables it with a warning when it is below 2000 ms or above `max-lifetime`. A value close to `max-lifetime` is allowed but almost useless: `max-lifetime` applies to connections in the pool and a borrowed connection is retired only after it is returned.
- Size pools from measured query latency/concurrency and the database budget across all replicas, reserving capacity for migrations and administration. The sum of pools must fit the available connection budget.
- Read query latency and database saturation under the actual workload; API/ETL labels alone do not determine useful pool size.

## Virtual threads (Spring Boot 4+)

Virtual threads are opt-in on supported JVMs and web servers. Enable and benchmark them explicitly:

```yaml
spring:
  threads:
    virtual:
      enabled: true
  jpa:
    open-in-view: false       # do not enable lazy loading in views by default
```

JDBC remains blocking and the connection pool limits database concurrency even with virtual threads. There is no universal connection count for a given number of requests; measure queue time and database capacity.

> **Good news (Java 25 baseline):** virtual thread **pinning via `synchronized` is fixed** — since Java 24, `synchronized` blocks no longer pin virtual threads, but native/foreign calls may still pin. Framework contexts and MDC can use `ThreadLocal`; preserve their supported propagation. Use Scoped Values for application-owned immutable context where the lifecycle fits, and measure effects.

## Lazy loading

Disable **Open Session in View** (OSIV) to avoid silent N+1:

```yaml
spring.jpa.open-in-view: false
```

Use `@Transactional(readOnly = true)` on read paths to avoid unnecessary flushes.

## Bounded pagination

Bound potentially large result sets with pagination, cursoring or an explicit limited contract. A fixed small enumeration need not become a paginated API. The example limit of 1000 is illustrative: choose a limit from response size, query cost and service capacity.

```java
public ResponseEntity<PageResponse<UserDTO>> search(
    @RequestParam(defaultValue = "0") @Min(0) int page,
    @RequestParam(defaultValue = "20") @Min(1) @Max(1000) int size
) { ... }
```

## Slow query diagnosis

```sql
-- PostgreSQL: top 10 slow queries
SELECT query, calls, total_exec_time / NULLIF(calls, 0) AS avg_ms, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

`pg_stat_statements` requires the extension and appropriate access. Plain Hibernate SQL logs do not necessarily include duration: correlate SQL with collected timings/statistics or a sanitized database slow-query log, using its actual configured source.

## References

- [Boot virtual threads](https://docs.spring.io/spring-boot/reference/features/spring-application.html#features.spring-application.virtual-threads)
- [Boot caching](https://docs.spring.io/spring-boot/reference/io/caching.html)
