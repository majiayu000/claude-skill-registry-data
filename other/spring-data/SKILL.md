---
name: spring-data
description: "Spring Data JPA 와 QueryDSL — Repository, 동적 쿼리, JPA+QueryDSL 조합, 흔한 실수. Use when Spring 에서 JPA 로 엔티티를 조회·저장하거나 QueryDSL 로 복잡한 동적 쿼리를 작성할 때."
---

# Spring Data Access Patterns

Spring Data JPA + QueryDSL 데이터 액세스 패턴

## Quick Reference

```
데이터 액세스 기술 선택
    │
    ├─ 단순 CRUD ──────────> Spring Data JPA
    │
    ├─ 동적 쿼리/검색 ────> + QueryDSL
    │
    ├─ N+1 문제 ──────────> @EntityGraph / Fetch Join
    │
    └─ 고성능 읽기 ────────> + Redis 캐싱 (/java:spring-cache)
```

---

## 기술 선택 가이드

| 상황 | 추천 기술 |
|------|-----------|
| 단순 CRUD | Spring Data JPA |
| 동적 쿼리/검색 | JPA + QueryDSL |
| 고성능 읽기 | + Redis 캐싱 |

---

## Spring Data JPA

### 기본 Repository
```java
public interface UserRepository extends JpaRepository<User, Long> {
    // 메서드 이름으로 쿼리 생성
    Optional<User> findByEmail(String email);
    List<User> findByStatusAndCreatedAtAfter(Status status, LocalDateTime date);

    // 커스텀 쿼리
    @Query("SELECT u FROM User u WHERE u.department.id = :deptId")
    List<User> findByDepartment(@Param("deptId") Long deptId);
}
```

### N+1 문제 해결
```java
// 방법 1: @EntityGraph
@EntityGraph(attributePaths = {"orders", "orders.items"})
Optional<User> findWithOrdersById(Long id);

// 방법 2: Fetch Join
@Query("SELECT u FROM User u JOIN FETCH u.orders WHERE u.id = :id")
Optional<User> findWithOrdersByIdFetch(@Param("id") Long id);

// 방법 3: Batch Size (application.yml)
spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 100
```

### Projection (필요한 필드만)
```java
// Interface Projection
public interface UserSummary {
    Long getId();
    String getName();
    String getEmail();
}

List<UserSummary> findAllProjectedBy();

// DTO Projection
@Query("SELECT new com.example.dto.UserDto(u.id, u.name) FROM User u")
List<UserDto> findAllAsDto();
```

---

## QueryDSL

### 설정 (Gradle)
```groovy
dependencies {
    implementation 'com.querydsl:querydsl-jpa:5.0.0:jakarta'
    annotationProcessor 'com.querydsl:querydsl-apt:5.0.0:jakarta'
    annotationProcessor 'jakarta.persistence:jakarta.persistence-api'
}
```

### 기본 사용법
```java
@Repository
@RequiredArgsConstructor
public class UserQueryRepository {
    private final JPAQueryFactory queryFactory;

    public List<User> findByCondition(UserSearchCondition cond) {
        return queryFactory
            .selectFrom(user)
            .where(
                usernameEq(cond.getUsername()),
                statusEq(cond.getStatus()),
                createdAtBetween(cond.getFromDate(), cond.getToDate())
            )
            .orderBy(user.createdAt.desc())
            .offset(cond.getOffset())
            .limit(cond.getLimit())
            .fetch();
    }

    // 동적 조건 (null이면 조건 무시)
    private BooleanExpression usernameEq(String username) {
        return hasText(username) ? user.username.eq(username) : null;
    }

    private BooleanExpression statusEq(Status status) {
        return status != null ? user.status.eq(status) : null;
    }

    private BooleanExpression createdAtBetween(LocalDateTime from, LocalDateTime to) {
        if (from == null && to == null) return null;
        if (from == null) return user.createdAt.loe(to);
        if (to == null) return user.createdAt.goe(from);
        return user.createdAt.between(from, to);
    }
}
```

### 페이징
```java
public Page<UserDto> searchUsers(UserSearchCondition cond, Pageable pageable) {
    List<UserDto> content = queryFactory
        .select(Projections.constructor(UserDto.class,
            user.id,
            user.name,
            user.email
        ))
        .from(user)
        .where(
            usernameEq(cond.getUsername()),
            statusEq(cond.getStatus())
        )
        .orderBy(user.createdAt.desc())
        .offset(pageable.getOffset())
        .limit(pageable.getPageSize())
        .fetch();

    Long total = queryFactory
        .select(user.count())
        .from(user)
        .where(
            usernameEq(cond.getUsername()),
            statusEq(cond.getStatus())
        )
        .fetchOne();

    return new PageImpl<>(content, pageable, total != null ? total : 0L);
}
```

### 복잡한 조인
```java
public List<OrderDto> findOrdersWithDetails(Long userId) {
    return queryFactory
        .select(Projections.constructor(OrderDto.class,
            order.id,
            order.orderNumber,
            user.name,
            product.name,
            orderItem.quantity,
            orderItem.price
        ))
        .from(order)
        .join(order.user, user)
        .join(order.items, orderItem)
        .join(orderItem.product, product)
        .where(user.id.eq(userId))
        .fetch();
}
```

### 서브쿼리
```java
public List<User> findUsersWithManyOrders(int minOrders) {
    return queryFactory
        .selectFrom(user)
        .where(user.id.in(
            JPAExpressions
                .select(order.user.id)
                .from(order)
                .groupBy(order.user.id)
                .having(order.count().goe(minOrders))
        ))
        .fetch();
}
```

### 집계 쿼리
```java
public List<DepartmentStats> getDepartmentStats() {
    return queryFactory
        .select(Projections.constructor(DepartmentStats.class,
            department.name,
            user.count(),
            user.salary.sum(),
            user.salary.avg()
        ))
        .from(user)
        .join(user.department, department)
        .groupBy(department.id, department.name)
        .having(user.count().gt(0))
        .orderBy(user.count().desc())
        .fetch();
}
```

---

## JPA + QueryDSL 조합 패턴

```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;        // JPA (CRUD)
    private final UserQueryRepository queryRepository;  // QueryDSL (검색)

    // 생성/수정/삭제: JPA
    @Transactional
    public User createUser(CreateUserRequest request) {
        User user = User.builder()
            .email(request.getEmail())
            .name(request.getName())
            .build();
        return userRepository.save(user);
    }

    // 단순 조회: JPA
    @Transactional(readOnly = true)
    public User getUser(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("User not found"));
    }

    // 복잡한 검색: QueryDSL
    @Transactional(readOnly = true)
    public Page<UserDto> searchUsers(UserSearchCondition condition, Pageable pageable) {
        return queryRepository.search(condition, pageable);
    }
}
```

---

## Common Mistakes

| 실수 | 올바른 방법 |
|------|------------|
| `findAll()` 후 필터링 | QueryDSL로 DB에서 필터링 |
| N+1 무시 | `@EntityGraph` 또는 fetch join |
| 모든 필드 조회 | Projection으로 필요한 것만 |
| 읽기에 `@Transactional` 누락 | `@Transactional(readOnly = true)` |
| count 쿼리 매번 실행 | 필요할 때만 count |

---

## 선택 기준

```
단순 CRUD? ─────────────────> Spring Data JPA만
     │
     └─ 동적 검색/필터? ──────> + QueryDSL
           │
           └─ 읽기 성능? ─────> + Redis (/java:spring-cache)
```

**관련 skill**: `/infra:database`, `/java:spring-cache`
