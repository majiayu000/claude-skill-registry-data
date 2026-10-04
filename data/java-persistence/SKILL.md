---
name: java-persistence
category: architecture
description: Use when a Java service reads or writes the database - JPA/Hibernate and Panache/Spring Data mapping, transaction boundaries, pagination and avoiding N+1 and entity-over-the-wire leaks
tech_stack: Java
---
# Java Persistence (JPA / Panache / Spring Data)

## Overview

Persistence is where Java services most often leak — lazy-loading exceptions, N+1 queries, entities serialized over HTTP, pagination applied in memory. Keep persistence at the repository boundary and mapped deliberately.

**Core principle:** Entities are a persistence detail. They never cross the HTTP boundary and they never carry business logic that belongs in the domain. Every list query is bounded AND the bound is honored by the SQL, not by Java code truncating a full result set.

## Mapping surface

| Concern | Quarkus (Panache) | Spring Data |
|---------|-------------------|-------------|
| Entity | `@Entity` + `PanacheEntityBase` or plain `@Entity` | `@Entity` |
| Repository | `implements PanacheRepository<Task>` | `extends JpaRepository<Task, UUID>` |
| Query | `find("status", s)` / HQL | derived methods / `@Query` |
| Transaction | `@Transactional` on the service | `@Transactional` on the service |
| Pagination | `.page(Page.of(n, size))` | `Pageable` / `Page<T>` |
| Optimistic lock | `@Version` | `@Version` |
| Schema management (non-test) | `quarkus.hibernate-orm.schema-management.strategy=none` (or `validate`; property renamed from `database.generation` in 3.23) | `spring.jpa.hibernate.ddl-auto=validate` |

## Rules

- **Transaction boundary = the service method**, never the repository or the resource. One use-case = one transaction.
- **Never return entities from a controller/resource.** Map to a DTO inside the service (or a JPA projection). Returning entities causes lazy-init serialization errors and leaks the schema.
- **Fetch deliberately to avoid N+1.** A loop that touches a lazy collection per row issues a query per row. Use a `JOIN FETCH` / entity graph / `@BatchSize` or `hibernate.default_batch_fetch_size`, and verify with a query-count assertion in a test.
- **Never paginate a collection `JOIN FETCH`.** Hibernate applies `LIMIT`/`OFFSET` in memory when the query also fetches a `*-to-many` collection (warning `HHH90003004`) — it loads the whole table to paginate it. Set `hibernate.query.fail_on_pagination_over_collection_fetch=true` in the test profile so this fails loudly instead of shipping slow. Page the root entity's ids first (plain query, no fetch join), then fetch the page by id with the collection join, or rely on `@BatchSize`/`hibernate.default_batch_fetch_size` instead of a fetch join at all.
- **Bound every list query.** Page (`Page`/`Pageable`, Panache `.page(...)`) — never `findAll()`/`listAll()` on a growing table. Default and maximum page size live with the endpoint (api-design-conventions), not just the repository call.
- **Migrations own the schema, not `hibernate.hbm2ddl=update`/Quarkus `generate-schema`.** Set validate/none in non-test envs; schema changes go through a migration (postgres-migrations), never auto-DDL in production.
- **Optimistic locking (`@Version`)** on entities with concurrent updates; map `OptimisticLockException`/`ObjectOptimisticLockingFailureException` to 409 in the central error mapper (api-design-conventions), never let it surface as 500.
- `spring.jpa.open-in-view=false` (Spring) — Open Session In View hides N+1s in the view layer and that lazy access outside a clear transaction boundary is exactly the mistake this skill exists to prevent.

## Worked Example — killing an N+1 without breaking pagination

```java
// ❌ N+1: one query for projects, then one per project for its tasks
List<Project> projects = repo.findAll(pageable).getContent();
projects.forEach(p -> total += p.getTasks().size());   // lazy hit per row

// ❌ "fixed" with a fetch join but now unbounded: Hibernate pages in memory
@Query("select p from Project p left join fetch p.tasks")
Page<Project> findAllWithTasks(Pageable pageable);   // HHH90003004

// ✅ page the roots first (no collection fetch), then fetch by id with the join
Page<UUID> ids = repo.findIds(pageable);
List<Project> page = repo.findByIdInWithTasks(ids.getContent());
```

Add a query-count assertion (Hibernate `Statistics`, see java-testing-junit-mockito) so the N+1 can't creep back in, and a test on the test profile with `hibernate.query.fail_on_pagination_over_collection_fetch=true` so an accidental collection-fetch-plus-page regresses loudly instead of just getting slow.

## Common Mistakes

- `@Transactional` on the repository or resource instead of the service.
- Serializing entities in the HTTP response.
- `findAll()`/`listAll()` with no paging.
- Paginating a query that also does a collection `JOIN FETCH`.
- `hbm2ddl=update` / Quarkus schema generation in a real environment instead of migrations.
- Testing on H2 where the SQL dialect differs from Postgres (java-testing-junit-mockito: use Testcontainers).
- Letting `OptimisticLockException` surface as an unmapped 500.

## Red Flags

- `LazyInitializationException` in an HTTP response → you serialized an entity outside the transaction.
- Query count scales with row count → N+1.
- `HHH90003004` in the logs, or a pagination query that also lists `fetch` in its JPQL.
- Schema changes with no migration file in the diff.
