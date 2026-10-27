---
name: java-spring-boot
description: "Spring Boot 3, Spring Data JPA query optimization, dependency injection, and reactive web architectures."
---

# Spring Boot Enterprise Protocol

Build scalable enterprise services with Spring Boot 3.

---

## 1. JPA Query Performance

1. Use `@EntityGraph` or JPQL `JOIN FETCH` to eliminate N+1 queries.
2. Mark read-only queries with `@Transactional(readOnly = true)` to bypass dirty checking.

---

## 2. Layered Architecture

Strict separation of Controller -> Service -> Repository layers. Never expose JPA Entities directly in REST controllers; use DTOs.
