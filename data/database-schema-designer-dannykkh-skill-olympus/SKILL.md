---
name: database-schema-designer
description: |
  Design production-ready database schemas for SQL and NoSQL databases.
  Use when user asks to "design schema", "create tables", "database design", "ERD",
  "data model", or when starting a project that needs database structure.
  Triggers on "normalize", "migration plan", "index strategy", "테이블 설계".
license: MIT
---

# Database Schema Designer

Design production-ready database schemas with best practices built-in.

---

## Quick Start

Just describe your data model:

```
design a schema for an e-commerce platform with users, products, orders
```

You'll get a complete SQL schema like:

```sql
CREATE TABLE users (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  total DECIMAL(10,2) NOT NULL
);

-- 인덱스는 CREATE TABLE 밖에 분리 (MySQL/PostgreSQL 모두 동작)
CREATE INDEX idx_orders_user ON orders(user_id);
```

> 위 예시는 MySQL 기준입니다(`AUTO_INCREMENT`). PostgreSQL은 PK를 `BIGINT GENERATED ALWAYS AS IDENTITY`(또는 `BIGSERIAL`)로 쓰세요. 인덱스는 `CREATE INDEX`로 분리하면 양쪽에서 동작합니다(인라인 `INDEX ...`는 MySQL/MariaDB 전용 → Postgres 문법 에러). 이 스킬은 DB-First라 대상 DB에 맞춰 설계가 달라집니다.

**What to include in your request:**
- Entities (users, products, orders)
- Key relationships (users have orders, orders have items)
- Scale hints (high-traffic, millions of records)
- Database preference (SQL/NoSQL) - defaults to SQL if not specified

---

## Triggers

| Trigger | Example |
|---------|---------|
| `design schema` | "design a schema for user authentication" |
| `database design` | "database design for multi-tenant SaaS" |
| `create tables` | "create tables for a blog system" |
| `schema for` | "schema for inventory management" |
| `model data` | "model data for real-time analytics" |
| `I need a database` | "I need a database for tracking orders" |
| `design NoSQL` | "design NoSQL schema for product catalog" |

---

## Key Terms

| Term | Definition |
|------|------------|
| **Normalization** | Organizing data to reduce redundancy (1NF → 2NF → 3NF) |
| **3NF** | Third Normal Form - no transitive dependencies between columns |
| **OLTP** | Online Transaction Processing - write-heavy, needs normalization |
| **OLAP** | Online Analytical Processing - read-heavy, benefits from denormalization |
| **Foreign Key (FK)** | Column that references another table's primary key |
| **Index** | Data structure that speeds up queries (at cost of slower writes) |
| **Access Pattern** | How your app reads/writes data (queries, joins, filters) |
| **Denormalization** | Intentionally duplicating data to speed up reads |

---

## Quick Reference

| Task | Approach | Key Consideration |
|------|----------|-------------------|
| New schema | Normalize to 3NF first | Domain modeling over UI |
| SQL vs NoSQL | Access patterns decide | Read/write ratio matters |
| Primary keys | INT or UUID | UUID for distributed systems |
| Foreign keys | Always constrain | ON DELETE strategy critical |
| Indexes | FKs + WHERE columns | Column order matters |
| Migrations | Always reversible | Backward compatible first |

---

## Process Overview

**DB-First:** 대상 DB를 먼저 정하고 그 DB의 강점으로 구조를 정한다(PostgreSQL JSONB·RLS, MySQL 정규화, MongoDB 임베딩). DB 감지 순서, DB별 설계 매트릭스, 엔티티 추출·관계 판별, Audit 컬럼, ERD 표기, `db-schema.md` 출력 형식은 정본인 젭마인 `skills/zephermine/references/schema-design-guide.md`를 따른다(젭마인은 활성 스킬이라 활성 스킬 루트에서 읽힌다). 이 스킬에는 사본을 두지 않는다.

```
Your Data Requirements
    |
    v
+-----------------------------------------------------+
| Phase 1: ANALYSIS                                   |
| * Identify entities and relationships               |
| * Determine access patterns (read vs write heavy)   |
| * Choose SQL or NoSQL based on requirements         |
+-----------------------------------------------------+
    |
    v
+-----------------------------------------------------+
| Phase 2: DESIGN                                     |
| * Normalize to 3NF (SQL) or embed/reference (NoSQL) |
| * Define primary keys and foreign keys              |
| * Choose appropriate data types                     |
| * Add constraints (UNIQUE, CHECK, NOT NULL)         |
+-----------------------------------------------------+
    |
    v
+-----------------------------------------------------+
| Phase 3: OPTIMIZE                                   |
| * Plan indexing strategy                            |
| * Consider denormalization for read-heavy queries   |
| * Add timestamps (created_at, updated_at)           |
+-----------------------------------------------------+
    |
    v
+-----------------------------------------------------+
| Phase 4: MIGRATE                                    |
| * Generate migration scripts (up + down)            |
| * Ensure backward compatibility                     |
| * Plan zero-downtime deployment                     |
+-----------------------------------------------------+
    |
    v
Production-Ready Schema
```

---

## Commands

| Command | When to Use | Action |
|---------|-------------|--------|
| `design schema for {domain}` | Starting fresh | Full schema generation |
| `normalize {table}` | Fixing existing table | Apply normalization rules |
| `add indexes for {table}` | Performance issues | Generate index strategy |
| `migration for {change}` | Schema evolution | Create reversible migration |
| `review schema` | Code review | Audit existing schema |

**Workflow:** Start with `design schema` → iterate with `normalize` → optimize with `add indexes` → evolve with `migration`

---

## Core Principles

| Principle | WHY | Implementation |
|-----------|-----|----------------|
| Model the Domain | UI changes, domain doesn't | Entity names reflect business concepts |
| Data Integrity First | Corruption is costly to fix | Constraints at database level |
| Optimize for Access Pattern | Can't optimize for both | OLTP: normalized, OLAP: denormalized |
| Plan for Scale | Retrofitting is painful | Index strategy + partitioning plan |

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| VARCHAR(255) everywhere | Wastes storage, hides intent | Size appropriately per field |
| FLOAT for money | Rounding errors | DECIMAL(10,2) |
| Missing FK constraints | Orphaned data | Always define foreign keys |
| No indexes on FKs | Slow JOINs | Index every foreign key |
| Storing dates as strings | Can't compare/sort | DATE, TIMESTAMP types |
| SELECT * in queries | Fetches unnecessary data | Explicit column lists |
| Non-reversible migrations | Can't rollback | Always write DOWN migration |
| Adding NOT NULL without default | Breaks existing rows | Add nullable, backfill, then constrain |

---

## Verification Checklist

After designing a schema:

- [ ] Every table has a primary key
- [ ] All relationships have foreign key constraints
- [ ] ON DELETE strategy defined for each FK
- [ ] Indexes exist on all foreign keys
- [ ] Indexes exist on frequently queried columns
- [ ] Appropriate data types (DECIMAL for money, etc.)
- [ ] NOT NULL on required fields
- [ ] UNIQUE constraints where needed
- [ ] CHECK constraints for validation
- [ ] created_at and updated_at timestamps
- [ ] Migration scripts are reversible
- [ ] Tested on staging with production data

---

## Deep Dives (References)

| 주제 | 파일 |
|------|------|
| DB-First Design (DB별 설계·출력 형식) — 정본은 젭마인 | `skills/zephermine/references/schema-design-guide.md` |
| Normalization (SQL 정규화) | [references/normalization.md](references/normalization.md) |
| Data Types (타입 선택) | [references/data-types.md](references/data-types.md) |
| Indexing Strategy (인덱스 전략) | [references/indexing-strategy.md](references/indexing-strategy.md) |
| Constraints (제약 조건) | [references/constraints.md](references/constraints.md) |
| Relationship Patterns (관계 패턴) | [references/relationship-patterns.md](references/relationship-patterns.md) |
| Migrations (마이그레이션) | [references/migrations.md](references/migrations.md) |
| NoSQL Design (MongoDB) | [references/nosql-mongodb.md](references/nosql-mongodb.md) |
| Performance Optimization | [references/performance-optimization.md](references/performance-optimization.md) |

---

## Related Resources

- **DB별 구현:** 네이티브 작업자 + 프로젝트 DB 버전·schema·migration 도구·테스트
- **Supabase Best Practices:** `skills/supabase-postgres-best-practices/SKILL.md`
