---
name: persistence-expert
description: Long FK 전략, QueryDSL DTO Projection, N+1 해결. JPA 관계 어노테이션 금지. /kb-persistence 명령 시 자동 활성화.
triggers: [/kb-persistence, /go, /red, /green, /refactor, /tidy, repository, querydsl, jpa, entity, adapter]
---

# Persistence Layer 전문가

## 핵심 원칙 (Zero-Tolerance)

### ✅ Mandatory
1. **Long FK 전략** - `private Long userId` (관계 어노테이션 금지)
2. **Command/Query Adapter 분리** - SaveAdapter, LoadAdapter
3. **QueryDSL DTO Projection** - Entity 반환 금지
4. **No N+1** - 항상 fetch join 사용
5. **BaseAuditEntity 상속** - createdAt, updatedAt
6. **Constructor Pattern** - Protected 기본 생성자 + Public 생성자
7. **Flyway 필수** - Schema 버전 관리

### ❌ Prohibited
1. **JPA 관계 어노테이션 금지** - `@ManyToOne`, `@OneToMany` 금지
2. **Entity Graph 금지** - Long FK 전략만 사용
3. **Lazy Loading 금지** - QueryDSL 명시적 join
4. **Entity 직접 반환 금지** - DTO Projection 필수
5. **Setter 금지** - 상태 변경은 메서드로
6. **Lombok 금지** - Pure Java getter
7. **JPQL String 금지** - QueryDSL 사용

## 예시

### ✅ CORRECT: Long FK 전략
```java
@Entity
public class OrderJpaEntity extends BaseAuditEntity {
    @Id
    private Long orderId;

    @Column(nullable = false)
    private Long customerId;  // ✅ Long FK

    // ❌ WRONG
    // @ManyToOne
    // private CustomerJpaEntity customer;
}
```

### ✅ CORRECT: QueryDSL DTO Projection
```java
return queryFactory
    .select(Projections.constructor(
        OrderDto.class,
        order.orderId,
        order.customerId,
        order.status
    ))
    .from(order)
    .fetch();
```

## 참조

- **전체 가이드**: docs/coding_convention/04-persistence-layer/
- **상세 규칙 + 템플릿**: [REFERENCE.md](./REFERENCE.md)

## 자동 활성화

`/kb-persistence /go|red|green|refactor|tidy` 실행 시 자동 활성화.
