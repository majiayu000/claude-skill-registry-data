---
name: planning-java
description: Project planning and architecture decision workflow for Java/Spring. Use when starting new projects, designing microservices, or making architectural decisions. Emphasizes simplicity, Spring-based robustness, and observability.
---

# Project Planning (Java/Spring Boot)

Workflow for project planning, architecture decisions, and technical design in the Spring ecosystem.

## 1. Understand Requirements
- What problem are we solving?
- What are the constraints (time, performance, scale)?
- What are the non-functional requirements (Security, Observability)?

## 2. Technology Choices (Spring Ecosystem)
- **Main Framework:** Spring Boot
- **Build:** Maven or Gradle
- **Data Access:** Spring Data JPA (for SQL) or Spring Data MongoDB (for NoSQL).
- **Database:** PostgreSQL, MySQL, or H2 (for testing/development).
- **Communication:** `WebClient` for HTTP calls.
- **Security:** Spring Security
- **Observability:** Spring Boot Actuator + Micrometer (for Prometheus/Grafana).
- **Testing:** JUnit 5, Mockito, Testcontainers.

## 3. Architecture Design

### Core Principles
- **KISS** (Keep It Simple, Stupid)
- **YAGNI** (You Aren't Gonna Need It)
- **Composition > Inheritance**
- **Code to the Interface**

### Layered Architecture Pattern
- **`Controller` (Web Layer):** Responsible for exposing REST endpoints (`@RestController`). Receives DTOs (Data Transfer Objects) and calls the Service.
- **`Service` (Business Layer):** Contains business logic (`@Service`). Orchestrates calls to Repositories and other services.
- **`Repository` (Data Layer):** Spring Data interface (`@Repository`) for database access.
- **`DTOs`:** Use DTOs to transfer data between the Controller layer and the client, avoiding exposure of domain entities.
- **`Entities`:** Domain classes (e.g., annotated with `@Entity` from JPA).

### Architecture Checklist
- [ ] Constructor-based Dependency Injection
- [ ] Type-safe configuration via `@ConfigurationProperties`
- [ ] Security (Spring Security) planned from the start
- [ ] Observability (`Actuator`) included
- [ ] Exception handling strategy (e.g., `@ControllerAdvice`)

## 4. Testing Strategy
- **Unit Tests:** Test `Service` classes in isolation (using Mockito for mocks).
- **Test Slices (Integration):**
    - `@WebMvcTest`: Tests the `Controller` layer (mocking the `Service`).
    - `@DataJpaTest`: Tests the `Repository` layer (using in-memory DB or Testcontainers).
- **Integration Tests (Full):**
    - `@SpringBootTest`: Loads the full application context.
    - **Testcontainers:** Use to test real integration with the database.

## 5. Observability Planning
- **`Actuator`:** Include the starter (`/health`, `/metrics`, `/info`).
- **Logging:** Configure structured logging.
- **Tracing:** If using microservices, plan for Tracing (e.g., Micrometer Tracing).

## 6. Security Planning (Spring Security)
- [ ] Define authentication strategy (e.g., JWT, OAuth2).
- [ ] Define authorization on endpoints (e.g., `antMatchers` or `@PreAuthorize`).
- [ ] Handle CORS.

## 7. Decisions
- **Avoid Premature Optimization:** Write a good program first. Use a profiler to optimize bottlenecks.
- **Avoid Over-Engineering:** Don't use complex patterns (e.g., CQRS, Event Sourcing) unless required. Start simple with CRUD.