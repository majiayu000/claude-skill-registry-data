---
name: spring-boot-database
description: >
  Flyway migrations and relational schema for Spring Boot: review or create
  files under db/migration, naming and version order, checksum/validation
  failures, evolving applied migrations, table/constraint/index design,
  entity-to-schema mapping and native queries. Use when asked whether a
  migration is correct, how to name or evolve it, how a schema should change,
  or to diagnose database connection failures and locks. For slow endpoints,
  N+1 queries or pool sizing use spring-boot-performance.
---

# Database in Spring Boot

Guide for Flyway migrations, table design, JPA entities, naming conventions, and data-layer troubleshooting.

> Inspect the project database, schema, migration configuration and managed dependency versions first. The JPA 3.2 / Hibernate 7 and PostgreSQL examples below are conditional; adapt them to the actual project rather than changing its stack.

## Scope

To load these conventions explicitly in Claude Code, invoke `/spring-boot-tools:spring-boot-database` with the migration review request. Automatic selection depends on the model; an answer about a simple naming question may otherwise be produced without loading the skill.

## Choose the operation from evidence

Use `analyze_project` to discover persistence dependencies, module paths and entity evidence; `check_migrations` combines local migration inspection and optional applied/pending Flyway state. Local naming checks do not prove an applied schema matches the files. A database query requires the selected environment, configured credentials and a trusted build.

- **Migration change:** inspect the existing sequence, applied state and data/backfill/lock impact. Applied versioned migrations remain immutable; add a forward migration.
- **Mapping change:** inspect the aggregate, access strategy, constraints and queries using it. An annotation inventory does not prove runtime loading behavior.
- **Incident diagnosis:** collect sanitized SQL/error, query plan, timings and connection metrics before suggesting changes. Keep schema writes out of diagnosis.

Deliver evidence and scope separately for migration, mapping and runtime findings; mark missing database access rather than inferring applied state.

## Flyway Migrations

### Location

```
src/main/resources/db/migration/
├── V1__create_users.sql
├── V2__add_email_unique.sql
├── V3__create_posts.sql
└── V4__add_index_post_user.sql
```

### Naming

```
V<version>__<short_description>.sql
```

- Match configured Flyway prefixes, separator and locations. For default versioned SQL migrations, numeric versions may use dots or underscores; sequential integers and timestamps are common choices.
- Double underscore `__` separator.
- Follow existing description conventions; snake_case English is an example, not an execution requirement. Repeatable migrations use the configured repeatable prefix (default `R__`).

### Writing rules

- **Versioned migrations run once**: let unexpected schema differences fail instead of hiding them with `IF NOT EXISTS`. Use repeatable migrations deliberately for replaceable objects.
- **Transactions depend on the database and SQL**. For PostgreSQL `CREATE INDEX CONCURRENTLY`, isolate the statement and add a sibling `V4__add_index.sql.conf` containing `executeInTransaction=false`. Also set `spring.flyway.postgresql.transactional-lock=false` (Flyway `postgresql.transactionalLock`) so Flyway uses a session-level advisory lock; otherwise the concurrent index build can wait indefinitely. Test the migration on a representative database.
- **Recovery**: select a tested forward fix, restore, or compatible application rollback from the actual data and deployment constraints. An inverse migration is an option only when its data effects are understood; it cannot recover discarded data by itself.
- **Applied versioned migrations are immutable**: retain their names and contents. Add a new versioned migration for every change. `repair` changes history metadata, not the schema; use it only after investigating and reconciling an explicitly understood failure, with backups and the same locations used by `migrate`.

### Example

```sql
-- V1__create_users.sql

CREATE TABLE users (
    id         BIGSERIAL    NOT NULL PRIMARY KEY,
    email      VARCHAR(255) NOT NULL,
    name       VARCHAR(100) NOT NULL,
    role       VARCHAR(20)  NOT NULL DEFAULT 'USER',
    created_at TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX uq_users_email ON users (email);
```

## JPA entities

### EntityManager injection (JPA 3.2 / Hibernate 7)

Following the JPA 3.2 injection arrangement, Spring Framework 7's `LocalContainerEntityManagerFactoryBean` (auto-configured by Boot) exposes the shared `EntityManager` and `EntityManagerFactory` for `@Autowired`/constructor injection, with qualifier support for multiple persistence units. `@PersistenceContext` remains valid; constructor injection of the Boot-provided shared EntityManager is also suitable for a single persistence unit. Do not create a shared EntityManager manually without a concrete need:

```java
@Service
public class UserSearchService {

    private final EntityManager em;

    UserSearchService(EntityManager em) {  // @Autowired is optional on a single constructor
        this.em = em;
    }
}
```

If the application defines multiple persistence units, qualify the injection point (e.g. `@Qualifier("ordersEm")`). `LocalContainerEntityManagerFactoryBean` also accepts the JPA 3.2 `PersistenceConfiguration` when a custom setup is needed.

### Conventions

- Preserve schema names and the configured naming strategy. Explicit `@Table` / `@Column` mappings are useful when defaults do not match; plural snake_case is only the example convention.
- Choose identifier types from existing identity, scale and generation requirements; do not replace UUIDs or sequences to match the BIGSERIAL example.
- Choose timestamp semantics from the domain and database. PostgreSQL `TIMESTAMPTZ` suits instants and maps to `java.time.Instant` or `OffsetDateTime` (the `createdAt` query below binds an `Instant`); local wall-clock values can need `TIMESTAMP` and `LocalDateTime`.
- Map booleans to the actual database type and dialect; avoid a blanket type conversion across databases.
- For PostgreSQL JSONB with a compatible Hibernate version, use `@JdbcTypeCode(SqlTypes.JSON)`; `columnDefinition = "jsonb"` alone does not configure JSON serialization.

### Embedded value objects

```java
@Embeddable
public class Address {
    @Column(name = "address_street")
    private String street;
    @Column(name = "address_city")
    private String city;
    @Column(name = "address_zip")
    private String zipCode;
}
```

## Native queries

- Prefer JPQL or repository methods (derived queries) over native queries.
- When you need a native query: use `@Query(nativeQuery = true, ...)` and parameterize with `?1, ?2, ...`.
- For very complex queries that don't fit in a repository: create a separate `@Service` (`UserSearchService`) with an injected EntityManager and wrap results in DTOs.

```java
public interface UserRepository extends JpaRepository<User, Long> {
    // Derived query
    Optional<User> findByEmail(String email);

    // JPQL
    @Query("""
        SELECT u FROM User u
        WHERE u.createdAt > ?1
        """)
    List<User> findSince(Instant date);

    // Native
    @Query(nativeQuery = true, value = """
        SELECT COUNT(*) FROM users
        WHERE role = ?1
          AND created_at >= now() - CAST(?2 AS interval)
        """)
    long countByActiveRole(String role, String interval);
}
```

## Database troubleshooting

For connection failures, locks or slow queries, select the relevant diagnostic
from [database troubleshooting](references/troubleshooting.md). Use the actual
database and existing telemetry; do not run every example for a mapping change.

## References

- [Flyway script configuration](https://documentation.red-gate.com/flyway/reference/script-configuration)
- [Flyway repair](https://documentation.red-gate.com/flyway/reference/commands/repair)
