---
name: database
description: "DB 성능 일반 — 인덱스 설계, N+1 해결, 쿼리 최적화, 커넥션 풀 설정. Use when 쿼리가 느리거나 인덱스·커넥션 풀을 점검할 때."
---

# Database Patterns

인덱스 최적화, N+1 해결, 쿼리 성능, 마이그레이션 패턴

## Quick Reference (결정 트리)

```
성능 문제?
    │
    ├─ 조회 느림 ──────> 인덱스 확인 (EXPLAIN)
    │   ├─ Seq Scan ──> 인덱스 추가
    │   └─ 인덱스 있음 ─> 복합 인덱스 순서 확인
    │
    ├─ N+1 문제 ───────> Fetch Join / Preload
    │
    └─ 페이지네이션 ───> Cursor 기반 (OFFSET 회피)

인덱스 타입
    ├─ 일반 조회 ─────> B-Tree (기본)
    ├─ JSONB/배열 ────> GIN
    └─ 시계열 대용량 ──> BRIN
```

---

## 인덱스 종류

| 타입 | PostgreSQL | MySQL | 용도 |
|------|------------|-------|------|
| B-Tree | ✅ (기본) | ✅ (기본) | 일반 조회, 범위, 정렬 |
| Hash | ✅ | ✅ (Memory) | 정확한 일치만 |
| GIN | ✅ | ❌ | 배열, JSONB, 전문검색 |
| GiST | ✅ | ❌ | 지리 데이터, 범위 |
| BRIN | ✅ | ❌ | 대용량 시계열 데이터 |
| Full-Text | ✅ | ✅ | 전문 검색 |

---

## CRITICAL: 인덱스 설계

### 복합 인덱스 순서

**IMPORTANT**: 순서가 성능을 결정함

```sql
-- WHERE tenant_id = ? AND status = ? AND created_at > ?
CREATE INDEX idx_orders_search
ON orders(tenant_id, status, created_at);
--         └─ 등호(=)  └─ 등호(=)  └─ 범위(>)
```

**규칙**: 등호(=) 조건 → 범위(<, >) 조건 → ORDER BY

### 복합 인덱스 사용 규칙

```sql
-- (tenant_id, status, created_at) 인덱스일 때
-- ✅ 사용 가능: 왼쪽부터 순서대로
WHERE tenant_id = ?
WHERE tenant_id = ? AND status = ?
WHERE tenant_id = ? AND status = ? AND created_at > ?

-- ❌ 사용 불가: 중간 건너뜀
WHERE status = ?
WHERE tenant_id = ? AND created_at > ?  -- status 건너뜀
```

### 커버링 인덱스

```sql
-- 테이블 접근 없이 인덱스만으로 조회 (Index-Only Scan)
CREATE INDEX idx_users_email_covering
ON users(email) INCLUDE (id, name);
```

### 부분 인덱스

```sql
-- 활성 사용자만 인덱스 (크기 감소)
CREATE INDEX idx_users_active
ON users(email) WHERE status = 'active';
```

---

## CRITICAL: N+1 문제 해결

### 문제

```java
List<User> users = userRepository.findAll();  // 1번
for (User user : users) {
    user.getOrders();  // N번 추가 쿼리
}
// 사용자 100명 = 101번 쿼리
```

### 해결 1: Fetch Join (JPA)

```java
@Query("SELECT u FROM User u JOIN FETCH u.orders")
List<User> findAllWithOrders();
```

### 해결 2: EntityGraph

```java
@EntityGraph(attributePaths = {"orders", "orders.items"})
List<User> findAll();
```

### 해결 3: Batch Size

```yaml
spring.jpa.properties.hibernate.default_batch_fetch_size: 100
```

### 해결 4: Preload (Go/GORM)

```go
// Bad
db.Find(&users)
for _, u := range users {
    db.Where("user_id = ?", u.ID).Find(&u.Orders)
}

// Good
db.Preload("Orders").Find(&users)
```

---

## 쿼리 최적화

### EXPLAIN 분석

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123;

-- 확인 포인트:
-- 1. Seq Scan → Index Scan 필요
-- 2. actual time: 실제 시간
-- 3. rows: 예상 vs 실제
```

### 페이지네이션 최적화

```sql
-- Bad: OFFSET 크면 느림 (100,000개 스캔 후 버림)
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;

-- Good: Cursor 기반
SELECT * FROM orders
WHERE id > :last_id
ORDER BY id LIMIT 20;
```

### SELECT 최적화

```sql
-- Bad
SELECT * FROM users WHERE status = 'active';

-- Good: 필요한 컬럼만
SELECT id, name, email FROM users WHERE status = 'active';
```

---

## 마이그레이션

**상세 내용**: `/infra:database-migration` skill 참조

### 핵심 패턴

```sql
-- 안전: 인덱스 생성 (락 없이)
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

-- 안전: NOT NULL 추가 (3단계)
-- 1. 컬럼 추가 → 2. 데이터 채움 → 3. 제약 추가
```

| 도구 | 용도 |
|------|------|
| Flyway | 단순함 (SQL 기반) |
| Liquibase | 복잡한 환경 (롤백 자동) |
| golang-migrate | Go 프로젝트 |

---

## 커넥션 풀 설정

### Spring Boot (HikariCP)

```yaml
spring.datasource.hikari:
  maximum-pool-size: 20
  minimum-idle: 5
  connection-timeout: 30000
```

### Go

```go
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(5 * time.Minute)
```

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| SELECT * | 필요한 컬럼만 |
| 인덱스 없이 JOIN | 조인 컬럼 인덱스 |
| LIKE '%keyword%' | Full-Text Search |
| OR 조건 남용 | UNION 또는 재설계 |
| 함수 in WHERE | 표현식 인덱스 |
| 모든 컬럼에 인덱스 | 필요한 것만 |
| 큰 OFFSET | Cursor 기반 |
| N+1 쿼리 | Fetch Join/Preload |

---

## 체크리스트

### 인덱스
- [ ] WHERE, JOIN, ORDER BY 컬럼에 인덱스
- [ ] 복합 인덱스 순서 확인 (등호 → 범위)
- [ ] 사용되지 않는 인덱스 정리
- [ ] 커버링 인덱스 검토

### 쿼리
- [ ] EXPLAIN으로 실행 계획 확인
- [ ] N+1 문제 없는지 확인
- [ ] 페이지네이션 최적화 (cursor)
- [ ] 불필요한 SELECT * 제거

### 마이그레이션 (`/infra:database-migration` 참조)
- [ ] 버전 관리 도구 사용
- [ ] 대용량 테이블은 CONCURRENTLY
