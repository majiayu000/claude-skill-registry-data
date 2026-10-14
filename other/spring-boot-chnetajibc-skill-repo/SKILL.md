---
name: spring-boot
description: "Spring Boot engineering: layered structure, DI, config/profiles, MVC/WebFlux, validation, transactions, JPA, Actuator, Testcontainers. Use for Spring Boot services; auth specifics in spring-security."
---

# spring-boot

Boot favors convention: structure by domain, configure externally, test against real infrastructure.

## Activate when

- Building or changing Spring Boot services: controllers, services, repositories, config, transactions, tests, production setup.

## Do NOT activate for

- Authentication/authorization design (see frameworks/spring-security); plain-Java concerns (see languages/java).

## Procedure

1. Version: detect Spring Boot generation from pom.xml/build.gradle; research in https://docs.spring.io/spring-boot/ for THAT generation (Boot 2→3 namespace and Security changes bite). Consult https://docs.spring.io/spring-framework/reference/ for core semantics.
2. Structure: controller (HTTP only) → service (transactions, orchestration) → repository/domain; DTOs at the web boundary, never expose JPA entities; MapStruct/manual mappers explicit.
3. DI/config: constructor injection; `@ConfigurationProperties` + profiles over scattered `@Value`; secrets from vault/env, never properties files in git.
4. Web: Spring MVC by default; WebFlux only for proven non-blocking need (R2DBC drivers end-to-end); validation with Bean Validation at the boundary; global `@ControllerAdvice` error envelope (RFC-7807 shape).
5. Data: Spring Data repositories + explicit queries; transactions at service layer with correct propagation/isolation; N+1 checked via query logs; Flyway/Liquibase migrations versioned and reversible (see https://docs.spring.io/spring-data/ and https://hibernate.org/orm/documentation/).
6. Observability: Actuator health/info/metrics, Micrometer + tracing, structured logs; readiness/liveness probes wired to real checks.
7. Testing: JUnit 5 + Mockito for units, `@SpringBootTest` slices for integration, Testcontainers for Postgres/Kafka/Redis reality (see https://testcontainers.com/guides/).
8. Production: externalized config, graceful shutdown, connection-pool sizing, banner/endpoint exposure locked down.
9. Verify: full test suite green on pinned JDK, migration up+down on scratch DB, actuator endpoints reviewed for exposure.

## Failure modes

- Boot-generation API drift; lazy-loading outside transactions; transactions on private/self-invoked methods (proxy bypass); actuator overexposure.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (spring-boot, spring-framework, spring-data, hibernate, junit, mockito, testcontainers).
