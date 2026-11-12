---
name: spring-cache
description: "Spring Cache 와 Redis — @Cacheable·@CacheEvict 등 캐시 어노테이션, 캐싱 전략, RedisTemplate 직접 사용. Use when Spring Boot 에 Redis 캐시를 설정하거나 캐시 무효화·TTL 전략을 정할 때."
---

# Spring Cache Patterns

Redis를 활용한 Spring Boot 캐싱 전략

## Quick Reference (결정 트리)

```
캐싱 대상 선정
    │
    ├─ 자주 조회 + 변경 적음 ────> 긴 TTL 캐싱
    │
    ├─ 자주 조회 + 자주 변경 ────> 짧은 TTL 또는 제외
    │
    ├─ 대용량 객체 ─────────────> 필요한 필드만 DTO로
    │
    └─ 일관성 중요 ─────────────> Write-Through 패턴
```

---

## 설정

```groovy
implementation 'org.springframework.boot:spring-boot-starter-data-redis'
implementation 'org.springframework.boot:spring-boot-starter-cache'
```

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
  cache:
    type: redis
    redis:
      time-to-live: 600000  # 10분
```

### Redis 설정 클래스

```java
@Configuration
@EnableCaching
public class RedisConfig {

    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
        RedisCacheConfiguration defaultConfig = RedisCacheConfiguration
            .defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeKeysWith(SerializationPair.fromSerializer(new StringRedisSerializer()))
            .serializeValuesWith(SerializationPair.fromSerializer(new GenericJackson2JsonRedisSerializer()));

        // 캐시별 개별 TTL
        Map<String, RedisCacheConfiguration> configs = Map.of(
            "users", defaultConfig.entryTtl(Duration.ofHours(1)),
            "products", defaultConfig.entryTtl(Duration.ofMinutes(30))
        );

        return RedisCacheManager.builder(factory)
            .cacheDefaults(defaultConfig)
            .withInitialCacheConfigurations(configs)
            .build();
    }
}
```

---

## CRITICAL: 캐시 어노테이션

### @Cacheable - 조회 캐싱

```java
@Cacheable(value = "users", key = "#id")
public User getUser(Long id) {
    return userRepository.findById(id).orElseThrow();
}

// 조건부 캐싱
@Cacheable(value = "users", key = "#id", condition = "#id > 0")
public User getUserConditional(Long id) { }

// null 결과 캐싱 방지
@Cacheable(value = "users", key = "#email", unless = "#result == null")
public User getUserByEmail(String email) { }
```

### @CachePut - 캐시 업데이트

```java
@CachePut(value = "users", key = "#result.id")
@Transactional
public User updateUser(Long id, UpdateUserRequest request) {
    User user = userRepository.findById(id).orElseThrow();
    user.update(request);
    return userRepository.save(user);
}
```

### @CacheEvict - 캐시 삭제

```java
// 단일 삭제
@CacheEvict(value = "users", key = "#id")
public void deleteUser(Long id) { }

// 전체 삭제
@CacheEvict(value = "users", allEntries = true)
public void clearUserCache() { }

// 여러 캐시 삭제
@Caching(evict = {
    @CacheEvict(value = "users", key = "#id"),
    @CacheEvict(value = "userSearch", allEntries = true)
})
public void deleteUserWithRelated(Long id) { }
```

---

## 캐싱 전략

### Cache-Aside (Lazy Loading)
```java
// @Cacheable이 이 패턴 - 가장 일반적
@Cacheable(value = "products", key = "#id")
public Product getProduct(Long id) {
    return productRepository.findById(id).orElseThrow();
}
```

### Write-Through
```java
// 쓰기 시 캐시도 함께 업데이트
@CachePut(value = "products", key = "#result.id")
public Product saveProduct(Product product) {
    return productRepository.save(product);
}
```

---

## RedisTemplate 직접 사용

```java
@Service
@RequiredArgsConstructor
public class RedisService {
    private final RedisTemplate<String, Object> redisTemplate;

    // String
    public void setValue(String key, Object value, Duration ttl) {
        redisTemplate.opsForValue().set(key, value, ttl);
    }

    // Hash (객체 필드별)
    public void setHash(String key, String field, Object value) {
        redisTemplate.opsForHash().put(key, field, value);
    }

    // Set (좋아요 목록 등)
    public void addToSet(String key, Object value) {
        redisTemplate.opsForSet().add(key, value);
    }

    // Sorted Set (랭킹)
    public void addToRanking(String key, Object value, double score) {
        redisTemplate.opsForZSet().add(key, value, score);
    }

    public Set<Object> getTopRanking(String key, int count) {
        return redisTemplate.opsForZSet().reverseRange(key, 0, count - 1);
    }
}
```

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| TTL 없이 캐싱 | 항상 적절한 TTL 설정 |
| 대용량 객체 캐싱 | 필요한 필드만 DTO로 |
| JPA Entity 직접 캐싱 (Serializable 구현 포함) | DTO 변환 후 캐싱. Spring Data Redis는 `GenericJackson2JsonRedisSerializer`(JSON) 사용. Entity Serializable은 lazy proxy / version 결합 / 캐시-DB 결합 문제 유발하는 안티패턴 |
| 캐시 키 충돌 | 명확한 네이밍 (prefix:entity:id) |
| 캐시-DB 불일치 | @CachePut/@CacheEvict 동기화 |

---

## 체크리스트

- [ ] @EnableCaching 추가
- [ ] 캐시별 TTL 설정
- [ ] 키 네이밍 규칙 정의
- [ ] Serializer 설정 (JSON 권장)
- [ ] 변경 시 @CacheEvict 적용
- [ ] 분산 락 필요시: `/architecture:distributed-lock` 참조
