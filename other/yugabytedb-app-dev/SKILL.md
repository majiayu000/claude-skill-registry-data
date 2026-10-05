---
name: yugabytedb-app-dev
description: >
  Build production-grade applications that connect to YugabyteDB across any language runtime or framework.
  Covers JDBC/Spring Boot, Spring Boot Reactive (WebFlux + R2DBC), Quarkus (SmallRye Fault Tolerance + Agroal), Python, Node.js, Go, .NET, and more — with correct driver config, pool tuning (HikariCP/Agroal/Npgsql),
  transaction retry logic, Flyway migrations, and topology-aware
  load balancing. Use this skill whenever the user is writing NEW application code that talks to YugabyteDB,
  integrating a framework (Spring, Quarkus, Micronaut, FastAPI, Express, etc.) with YugabyteDB, asking how to
  handle transaction retries or serialization errors with YugabyteDB, configuring a connection pool for YugabyteDB,
  Trigger even when the user just says
  "connect my app to YugabyteDB" or "YugabyteDB Spring Boot" or "YugabyteDB retry".
---

# YugabyteDB Application Development Skill

A reference skill for building applications on top of YugabyteDB, covering connection config,
transaction retries, and language/framework-specific best practices.

---

## Overview

YugabyteDB is a distributed SQL database compatible with PostgreSQL. Writing applications for it
requires attention to three areas standard Postgres apps often skip:

1. **Driver** — Use the YugabyteDB JDBC driver (`jdbc-yugabytedb`) or the standard Postgres driver.
   YB's driver adds cluster-aware load balancing and topology routing.
2. **Retries** — Distributed transactions can fail with transient errors (serialization failures `40001`,
   deadlocks `40P01`, connection resets). Applications MUST retry these rather than surface them to users.
---

## Quick Reference by Runtime

| Runtime | Driver / Library | Retry Mechanism |
|---|---|---|
| Java / Spring Boot | `jdbc-yugabytedb` + HikariCP | Spring core `RetryPolicy` + `ExponentialBackOff` (built-in, no extra dep) + AOP aspect |
| Java / Spring Boot Reactive | `r2dbc-postgresql` + r2dbc-pool | Reactor `.retryWhen(YbRetry.spec())` inline in pipeline |
| Java / Quarkus | `jdbc-yugabytedb` + Agroal | SmallRye `@Retry` + CDI interceptor for exception translation |
| Python | `psycopg2` / `asyncpg` | Custom decorator wrapping `psycopg2.errors.SerializationFailure` | Two connection pools |
| Node.js | `@yugabytedb/pg` (smart driver) | `withRetry` loop catching `40001`/`40P01`/`XX000` | `EndpointPoolManager` (multi-endpoint probe + failover) |
| Go | `pgx` | `pgx` retry loop | Two `pgxpool.Pool` instances |
| .NET / ASP.NET Core | `Npgsql` + EF Core | Polly `AsyncRetryPolicy` | Two `DbContext` registrations (rw + ro) |

---

## Instructions
- Use the latest stable version of the YugabyteDB driver for your language
- Use the latest stable version of the application framework for your language

---

## Core Concepts

### Transaction Error Codes to Retry

```
40001  — serialization_failure (optimistic concurrency)
40P01  — deadlock_detected
57P01  — admin_shutdown (node restart / kill -15)
08006  — connection_failure (socket timeout, kill -9)
XX000  — internal_error — ONLY retry conditionally
```

Also retry on these Java exception types for JPA/JDBC:
- `SQLRecoverableException`
- `SQLTransientConnectionException`
- `TransientDataAccessException`
- Hibernate `TransactionException` (begin/commit/rollback failures)

---

## Java References

### Spring Boot

For full details read → [`references/java-spring.md`](references/java-spring.md)

Key files in the reference implementation:

| File | Purpose |
|---|---|
| `KVRetryPolicy.java` | Implements `RetryPolicy` — classifies retryable exceptions; owns `ExponentialBackOff` |
| `DataSourceAspect.java` | AOP aspect wrapping all `@Service` methods with `RetryTemplate` |
| `YbDataApplication.java` | Wires `RetryTemplate` with exponential backoff from config |
| `KVService.java` | Service using `@Transactional` and `@Transactional(readOnly = true)` |
| `application.yaml` | Full driver + pool + retry config |

### Spring Boot Reactive (WebFlux + R2DBC)

For full details read → [`references/java-spring-reactive.md`](references/java-spring-reactive.md)

Key differences from Spring Boot (blocking):

| Topic | Reactive behaviour |
|---|---|
| Driver | `com.yugabyte:r2dbc-postgresql` (YugabyteDB fork) — URL scheme `r2dbc:postgresql://` |
| Retry | `RetryConfigSpec` bean provides `Retry`; controller applies `.retryWhen(retrySpec)` on each pipeline |
| Transactions | `@Transactional` in service; retry wraps outside via controller pipeline |
| Migrations | Flyway still runs over JDBC at startup (add `jdbc-yugabytedb` as a side-car dep) |

### Quarkus

For full details read → [`references/java-quarkus.md`](references/java-quarkus.md)

Key differences from Spring Boot:

| Topic | Quarkus behaviour |
|---|---|
| Connection pool | Agroal (not HikariCP); config via `quarkus.datasource.jdbc.*` |
| Retry mechanism | SmallRye Fault Tolerance `@Retry` + custom CDI interceptor for SQL-state translation |
| **Interceptor ordering** | **CRITICAL**: set `mp.fault.tolerance.interceptor.priority=100` so `@Retry` wraps outside `@Transactional`, giving each retry a fresh transaction |
| Native image | YugabyteDB driver is JVM-mode only — not compatible with GraalVM native compilation |

---

## Python Reference

For full details read → [`references/python.md`](references/python.md)

---

## Node.js Reference

For full details read → [`references/nodejs.md`](references/nodejs.md)

---

## Go Reference

For full details read → [`references/go.md`](references/go.md)

---

## .NET Reference

For full details read → [`references/dotnet.md`](references/dotnet.md)

---

## Step-by-Step: New Application Setup

### 1. Add Dependencies

**Maven (Java):**
```xml
<dependency>
  <groupId>com.yugabyte</groupId>
  <artifactId>jdbc-yugabytedb</artifactId>
  <version>42.7.3-yb-4</version>
</dependency>
<dependency>
  <groupId>org.springframework.retry</groupId>
  <artifactId>spring-retry</artifactId>
  <version>2.0.12</version>
</dependency>
```

**Python:**
```bash
pip install psycopg2-binary  # or asyncpg for async
```

**Node.js:**
```bash
npm install @yugabytedb/pg    # YugabyteDB smart driver (fork of node-postgres)
```

**Go:**
```bash
go get github.com/jackc/pgx/v5
```

### 2. Configure Datasource

Always set:
- `auto-commit: false` — YugabyteDB works best with explicit transaction management
- `connection-init-sql` with `prepare warmup; execute warmup; commit;` — validates and warms the connection
- `socketTimeout` — prevents hanging connections on node failure
- `yb-servers-refresh-interval` — refreshes cluster topology periodically

### 3. Implement Retry Logic

**Never skip retries.** YugabyteDB distributed transactions can fail with `40001` under normal operation
(two concurrent writers hitting the same row). Without retries, these surface as errors to end users.

Use the reference `KVRetryPolicy` pattern — read [`references/java-spring.md`](references/java-spring.md)
for the full annotated implementation with all retry-worthy SQL states.

### 4. Schema Migrations

Use Flyway (Java) or Alembic (Python) for schema management. YugabyteDB supports all standard PostgreSQL DDL.

```sql
-- Example migration: V1_0_0__create.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS kvinfo (
    key   uuid PRIMARY KEY,
    value text
);   -- tune tablet count to expected data size
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Not retrying `40001` | Always wrap service layer with retry |
| `auto-commit: true` | Set to false; manage transactions explicitly |
| Using standard `org.postgresql` driver | Use `com.yugabyte` driver for topology-aware load balancing |
| Missing `socketTimeout` | Connections can hang indefinitely on node failure without it |
| Forgetting `@Transactional` on service methods | Without it, each repo call is its own transaction; retries won't help multi-step operations |

---

## Sample Prompts

These are example prompts that should trigger this skill.

**Java / Spring Boot**
- "I'm building a Spring Boot app and need to connect it to YugabyteDB. Show me the Maven dependencies, application.yaml config, and how to set up the connection pool correctly."
- "My Spring Boot app talking to YugabyteDB keeps getting '40001 serialization failure' errors under load. How do I handle this properly?"
- "I have an existing Spring Boot app connected to PostgreSQL. What do I need to change to migrate it to YugabyteDB?"

**Java / Spring Boot Reactive**
- "How do I build a reactive Spring Boot application using WebFlux and R2DBC that connects to YugabyteDB with retry support?"

**Java / Quarkus**
- "I want to build a Quarkus REST API backed by YugabyteDB. Walk me through the setup including retry handling."
- "My Quarkus app has @Retry on the service but transactions still fail without retrying. What's wrong?"

**Python**
- "How do I write a Python service that connects to YugabyteDB and handles transaction retries correctly? I need create, read, and delete operations."
- "Show me how to use asyncpg with FastAPI and YugabyteDB with proper retry handling."

**Node.js**
- "Show me how to connect a Node.js Express app to YugabyteDB with proper retry logic for distributed transaction errors."

**Go**
- "I'm using Go with pgx and need to connect to YugabyteDB and retry on transaction conflicts. Show me a complete example."

**.NET**
- "How do I set up a .NET ASP.NET Core app with Entity Framework Core to use YugabyteDB, including handling serialization failures?"

**General / Cross-runtime**
- "What SQL error codes do I need to retry on when using YugabyteDB, and why?"
- "How should I configure my connection pool for YugabyteDB?"
- "Connect my app to YugabyteDB"
- "YugabyteDB retry"
- "YugabyteDB Spring Boot setup"
