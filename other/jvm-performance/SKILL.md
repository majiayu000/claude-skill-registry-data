---
name: jvm-performance
description: "JVM·Spring 성능 튜닝 — Virtual Threads vs WebFlux, HikariCP, 다단계 캐싱, Resilience4j Circuit Breaker, JVM 옵션. Use when Spring 서비스의 지연·스레드·커넥션 풀 병목을 분석하거나 성능 목표를 맞출 때."
---

# JVM / Spring 성능 튜닝

언어 관용구는 [`effective-java`](../effective-java/SKILL.md), 락/동시성 문제는 [`concurrency-spring`](../concurrency-spring/SKILL.md),
Circuit Breaker 설계는 `/architecture:msa-resilience` 참조. 여기서는 **런타임 측정과 튜닝**을 다룬다.

## Virtual Threads vs WebFlux (2026)

| 기준 | Virtual Threads | WebFlux |
|------|-----------------|---------|
| **학습 곡선** | 낮음 (익숙한 블로킹 스타일) | 높음 (리액티브 패러다임) |
| **디버깅** | 쉬움 (일반 스택 트레이스) | 어려움 (비동기 스택) |
| **Best For** | Request-response, DB-heavy | Streaming, 백프레셔 필요 |
| **팀 도입** | 기존 MVC 마이그레이션 쉬움 | 마인드셋 변화 필요 |

**2026 권장**: 새 프로젝트는 Virtual Threads로 시작. WebFlux는 스트리밍/백프레셔 필요시에만.

## Virtual Threads (Java 21+)

### Setup (Spring Boot 3.2+)

```yaml
spring:
  threads:
    virtual:
      enabled: true  # 모든 요청 처리에 virtual threads 사용
```

### Configuration

```java
@Configuration
public class VirtualThreadConfig {
    @Bean
    public Executor asyncExecutor() {
        return Executors.newVirtualThreadPerTaskExecutor();
    }

    @Bean
    public TomcatProtocolHandlerCustomizer<?> virtualThreadsCustomizer() {
        return handler -> handler.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
    }
}
```

### Best Practices

```java
// ✅ 블로킹 코드 OK (virtual threads에서 스케일됨)
@Transactional(readOnly = true)
public UserDTO getUser(Long id) {
    User user = userRepository.findById(id).orElseThrow();
    UserProfile profile = apiClient.fetchProfile(user.getExternalId());  // 외부 HTTP도 OK
    return UserDTO.from(user, profile);
}

// ❌ synchronized는 virtual thread를 platform thread에 고정 (pin)
public synchronized String get(String key) { return cache.get(key); }

// ✅ ReentrantLock 사용
private final ReentrantLock lock = new ReentrantLock();
public String get(String key) {
    lock.lock();
    try { return cache.get(key); }
    finally { lock.unlock(); }
}

// ✅ BETTER: ConcurrentHashMap (락 불필요)
private final ConcurrentHashMap<String, String> cache = new ConcurrentHashMap<>();
```

### Structured Concurrency (Java 21+)

```java
public OrderDetails getOrderDetails(Long orderId) throws Exception {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        var orderTask = scope.fork(() -> orderRepository.findById(orderId).orElseThrow());
        var itemsTask = scope.fork(() -> itemRepository.findByOrderId(orderId));
        var customerTask = scope.fork(() -> customerClient.getCustomer(orderId));

        scope.join();
        scope.throwIfFailed();

        return new OrderDetails(orderTask.get(), itemsTask.get(), customerTask.get());
    }
}
```

## WebFlux (스트리밍 필요 시)

```java
// SSE - WebFlux가 빛나는 영역
@GetMapping(value = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<String>> streamEvents() {
    return Flux.interval(Duration.ofSeconds(1))
        .map(seq -> ServerSentEvent.<String>builder()
            .id(String.valueOf(seq))
            .event("heartbeat")
            .data("Sequence: " + seq)
            .build());
}
```

## Connection Pool (HikariCP)

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20      # SSD 기준 10-20 최적
      minimum-idle: 5
      max-lifetime: 1800000      # 30분
      connection-timeout: 30000  # 30초
      leak-detection-threshold: 60000  # 개발용
```

### Virtual Threads + Connection Pool 주의

```java
// ⚠️ Virtual threads는 수천 개 동시 요청 생성 가능
// 하지만 DB 커넥션 풀은 제한적 (예: 20개)
// → Semaphore로 동시 DB 접근 제한 필요

@Bean
public DataSource dataSource(DataSourceProperties props) {
    HikariDataSource ds = props.initializeDataSourceBuilder().type(HikariDataSource.class).build();
    return new SemaphoreDataSource(ds, 100);  // 최대 100개 동시 DB 작업
}

public class SemaphoreDataSource implements DataSource {
    private final Semaphore semaphore;
    @Override
    public Connection getConnection() throws SQLException {
        semaphore.acquire();
        return new SemaphoreConnection(delegate.getConnection(), semaphore);
    }
}
```

## Caching (Multi-Level)

```java
@Configuration
@EnableCaching
public class CacheConfig {
    @Bean
    public CacheManager cacheManager(RedisConnectionFactory redisFactory) {
        // L1: Caffeine (in-memory)
        CaffeineCacheManager caffeine = new CaffeineCacheManager();
        caffeine.setCaffeine(Caffeine.newBuilder()
            .maximumSize(10_000).expireAfterWrite(Duration.ofMinutes(5)));

        // L2: Redis (distributed)
        RedisCacheManager redis = RedisCacheManager.builder(redisFactory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(30))).build();

        return new CompositeCacheManager(caffeine, redis);
    }
}
```

## Circuit Breaker (Resilience4j)

```java
@CircuitBreaker(name = "paymentGateway", fallbackMethod = "paymentFallback")
@Retry(name = "paymentGateway")
@TimeLimiter(name = "paymentGateway")
public CompletableFuture<PaymentResult> processPayment(PaymentRequest request) {
    return CompletableFuture.supplyAsync(() -> gatewayClient.process(request));
}

private CompletableFuture<PaymentResult> paymentFallback(PaymentRequest req, Throwable t) {
    return CompletableFuture.completedFuture(PaymentResult.pending("Payment queued"));
}
```

## JVM Tuning

### G1GC (권장 기본)

```bash
java -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=100 \
     -XX:G1HeapRegionSize=16m \
     -Xms4g -Xmx4g \
     -XX:+AlwaysPreTouch \
     -jar app.jar
```

### ZGC (초저지연)

```bash
java -XX:+UseZGC \
     -XX:+ZGenerational \
     -Xms8g -Xmx8g \
     -jar app.jar
```

### Profiling Commands

```bash
# CPU + allocation profiling (Async Profiler)
./profiler.sh -e cpu -d 60 -f cpu.html <pid>
./profiler.sh -e alloc -d 60 -f alloc.html <pid>

# JFR
jcmd <pid> JFR.start duration=60s filename=recording.jfr

# Thread dump / Heap dump
jcmd <pid> Thread.print
jcmd <pid> GC.heap_dump /tmp/heap.hprof
```

## Anti-Patterns

```java
// 🚫 synchronized + virtual threads → pinning
public synchronized void process() { }

// 🚫 요청마다 새 HTTP client
RestTemplate restTemplate = new RestTemplate();

// 🚫 @Async with no thread pool limit
@Async public void processAsync() { }

// 🚫 N+1 query
orders.forEach(order -> order.getItems());

// 🚫 Block in WebFlux
Mono.just(userRepository.findById(1L).block());

// 🚫 과도한 connection pool
hikari.maximum-pool-size: 200  // 보통 10-30이 최적
```

## Performance Targets

| 메트릭 | 목표 | 경고 |
|--------|------|------|
| P50 Latency | < 20ms | > 50ms |
| P99 Latency | < 200ms | > 500ms |
| GC Pause (G1) | < 100ms | > 200ms |
| GC Pause (ZGC) | < 1ms | > 10ms |
| Heap Usage | < 70% | > 85% |

## 체크리스트

### Concurrency
- [ ] Virtual Threads 환경에서 `synchronized` 로 pinning 이 생기지 않는가 (→ `ReentrantLock`)
- [ ] `ThreadLocal` 누수 없음 (Virtual Threads 는 수가 많다)
- [ ] Structured Concurrency 로 하위 작업 취소가 전파되는가

### Database
- [ ] HikariCP `maximumPoolSize` 근거 있음 (Virtual Threads 라도 풀은 유한)
- [ ] `connectionTimeout` / `leakDetectionThreshold` 설정
- [ ] N+1 검증 (`spring.jpa.show-sql` 또는 p6spy)

### Resilience
- [ ] Circuit Breaker 임계치가 실측 기반인가
- [ ] Timeout 이 상위 호출자 타임아웃보다 짧은가
- [ ] Fallback 이 조용히 빈 값을 반환하지 않는가

## 참조 스킬

- [`effective-java`](../effective-java/SKILL.md) — 설계 관용구 / Modern Java
- [`concurrency-spring`](../concurrency-spring/SKILL.md) — 낙관적/비관적 락, 데드락
- [`spring-cache`](../spring-cache/SKILL.md) — `@Cacheable` 설정
- [`spring-data`](../spring-data/SKILL.md) — JPA / N+1
- `/architecture:msa-resilience` — Circuit Breaker / Retry / Bulkhead 설계
- `/observability:observability-pyroscope` — 상시 프로파일링
- [`spring-security-review`](../spring-security-review/SKILL.md) — Spring 보안 리뷰
