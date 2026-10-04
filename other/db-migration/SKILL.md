---
name: db-migration
description: >
  데이터베이스 마이그레이션 SQL 스크립트를 생성하는 스킬.
  "/db-migration"을 입력하거나, "마이그레이션 스크립트 만들어줘",
  "테이블 변경 SQL", "DB 스키마 변경" 같은 요청에 트리거된다.
  ERD 문서와 JPA Entity를 비교하여 안전한 마이그레이션 스크립트를 생성한다.
---

# DB 마이그레이션 스크립트 생성

ERD 문서와 JPA Entity 간 차이를 분석하여 MySQL 마이그레이션 SQL을 생성하는 스킬이다.

## 사전 확인

1. `doc/ERD.md` — 현재 ERD 정의
2. `doc/ERD_ALIGNMENT.md` — ERD 정합 계획
3. `doc/ERD_NON_STANDARD_TABLES.md` — ERD에 없는 테이블
4. `src/main/java/com/sample/llm/entity/` — 현재 JPA Entity
5. `src/main/resources/application.yml` — `ddl-auto` 설정 확인

## 스크립트 작성 원칙

### 안전 제일

```sql
-- 항상 트랜잭션으로 감싸기
START TRANSACTION;

-- 변경 작업 ...

COMMIT;
```

### 롤백 스크립트 동시 작성

모든 마이그레이션에는 롤백 SQL도 함께 작성한다:

```sql
-- ========== ROLLBACK ==========
-- START TRANSACTION;
-- (역방향 작업)
-- COMMIT;
```

### 데이터 보존 우선

- `ALTER TABLE RENAME` > `DROP + CREATE`
- `ALTER TABLE CHANGE COLUMN` > `DROP COLUMN + ADD COLUMN`
- 컬럼 삭제 전 반드시 백업 SELECT 안내

## 마이그레이션 유형별 템플릿

### 테이블 리네이밍

```sql
-- {old_table} → {new_table}
ALTER TABLE {old_table} RENAME TO {new_table};
```

### 컬럼 리네이밍

```sql
ALTER TABLE {table}
    CHANGE COLUMN {old_column} {new_column} {TYPE} {CONSTRAINTS};
```

### FK 변경

```sql
-- 기존 FK 제거
ALTER TABLE {table} DROP FOREIGN KEY {fk_name};

-- 새 FK 추가
ALTER TABLE {table}
    ADD CONSTRAINT {new_fk_name}
    FOREIGN KEY ({column}) REFERENCES {ref_table}({ref_column});
```

### 컬럼 추가 (nullable)

```sql
ALTER TABLE {table}
    ADD COLUMN {column} {TYPE} NULL AFTER {after_column};
```

### 초기 데이터 업데이트

```sql
-- 새 컬럼에 기본값 채우기
UPDATE {table} SET {column} = {default_value} WHERE {column} IS NULL;
```

## 파일 위치 및 네이밍

```
scripts/
├── {기능명}-migration.sql          # 마이그레이션
└── {기능명}-migration-rollback.sql  # 롤백 (선택)
```

네이밍 예시:
- `erd-alignment-migration.sql`
- `medical-chat-history-migration.sql`
- `add-medical-rule-table.sql`

## 동작 순서

### Step 1: 차이 분석

ERD 문서와 현재 Entity를 비교하여 변경 목록을 작성한다:

| 변경 유형 | 대상 | 현재 | 목표 |
|-----------|------|------|------|
| RENAME TABLE | ... | ... | ... |
| ADD COLUMN | ... | — | ... |
| CHANGE COLUMN | ... | ... | ... |

### Step 2: 의존성 확인

- FK 관계가 있는 테이블의 변경 순서 결정
- 자식 테이블 먼저 → 부모 테이블 나중에 변경

### Step 3: SQL 생성

- 각 변경을 개별 ALTER 문으로 (디버깅 용이)
- 주석으로 변경 목적 명시
- 롤백 SQL 동시 작성

### Step 4: Entity 동기화

SQL 실행 후 JPA Entity도 함께 수정:
- `@Table(name = "...")` 갱신
- `@Column(name = "...")` 갱신
- `@JoinColumn(name = "...")` 갱신

### Step 5: 문서 갱신

- `doc/ERD.md` 업데이트
- `doc/ERD_ALIGNMENT.md` 상태 반영
- `README.md` 스키마 섹션 갱신

## 주의사항

- 운영 DB에는 `ddl-auto: validate` 사용 — Hibernate가 자동 변경하지 않도록
- 개발 DB는 `ddl-auto: update`이므로 Entity 변경만으로도 적용 가능
- 대량 데이터가 있는 테이블의 ALTER는 서비스 중단 필요 여부 안내
- H2(테스트)와 MySQL 간 SQL 구문 차이 주의 (예: FULLTEXT INDEX는 MySQL 전용)
