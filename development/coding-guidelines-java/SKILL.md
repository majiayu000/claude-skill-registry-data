---
name: coding-guidelines-java
description: Comprehensive coding standards for Java and Spring Boot projects. Use when writing new code, refactoring, or setting up project structure. Focuses on robustness, immutability, dependency injection, and maintainability.
---

# Coding Guidelines (Java/Spring Boot)

Apply these standards to all Java and Spring Boot code. Focus on robustness, maintainability, and best practices.

## Section 1: Java Fundamentals (Effective Java)

### Class and Object Principles
- **Immutability:** Minimize mutability. Immutable classes are simpler and safer.
    - To create: Provide no setters, make the class `final`, make all fields `final` and `private`, and make defensive copies of mutable components.
- **Composition > Inheritance:** Prefer **composition** over inheritance. Inheritance violates encapsulation.
- **Encapsulation:** Minimize the accessibility of classes and members. Use `private` whenever possible. Never expose public fields; use getters.
- **Interfaces:** Prefer interfaces over abstract classes for defining types. Code to the interface, not the implementation (e.g., `List<String> list = new ArrayList<>()`).
- **`equals()` and `hashCode()`:** **Always** override `hashCode` when overriding `equals`.

### Resource Management
- **`try-with-resources`:** Prefer `try-with-resources` over `try-finally` blocks to ensure proper resource closure (`AutoCloseable`).
- **Avoid Finalizers:** Do not use `finalizers` or `cleaners`.

### Generics
- **No Raw Types:** Never use raw types (e.g., `List`). Use parameterized types (e.g., `List<String>`).
- **Wildcards (PECS):** Use bounded wildcards to increase API flexibility (PECS Rule: *Producer-Extends, Consumer-Super*).

### Lambdas and Streams
- **Method References:** Prefer method references (e.g., `User::getName`) over lambdas (e.g., `u -> u.getName`) when possible.
- **Pure Functions:** Prefer pure functions (no side effects) in stream operations.
- **Standard Functional Interfaces:** Use standard `java.util.function` interfaces (like `Predicate`, `Function`).

### Methods and General Programming
- **Validation:** Check parameter validity at the beginning of methods (e.g., `IllegalArgumentException`, `NullPointerException`).
- **Defensive Copies:** Make defensive copies of mutable components.
- **Primitives > Boxed:** Prefer primitive types (`int`) over boxed types (`Integer`) for performance and to avoid `NullPointerException`.
- **`Optional`:** Use `Optional` judiciously for return values that might be null. Do not use `Optional` for collections (return empty collections).

### Concurrency
- **Executor Framework:** Prefer Executors and Tasks (`java.util.concurrent`) over managing `Threads` directly.
- **Synchronization:** Synchronize access (read and write) to shared mutable data. Keep `synchronized` blocks small.

## Section 2: Spring and Spring Boot Patterns

### Dependency Injection (DI) and Configuration
- **Constructor Injection:** Use **constructor injection** to declare dependencies. This allows fields to be `final`, ensuring immutability.
- **`@ConfigurationProperties`:** To inject configuration properties, prefer a POJO annotated with **`@ConfigurationProperties`**. It is type-safe and more robust than `@Value`.
- **Starters:** Use Spring Boot Starters for simplified dependency management.
- **Java Configuration:** Prefer `@Configuration` classes and `@Bean` methods over XML.
- **Stereotypes:** Use standard stereotypes (`@Component`, `@Service`, `@Repository`, `@Controller`).

### Web, Data, and APIs
- **`@RestController`:** Use `@RestController` for REST services with specific mappings (e.g., `@GetMapping`).
- **Spring Data:** Use Spring Data Repository interfaces to abstract data access.
- **`WebClient`:** Prefer the `WebClient` (reactive) for service-to-service communication over the legacy `RestTemplate`.

### Testing and Production
- **`@SpringBootTest`:** Use `@SpringBootTest` for high-level integration tests.
- **Test Slices:** Use Test Slices (e.g., `@WebMvcTest`, `@DataJpaTest`) to test specific layers.
- **Testcontainers:** Use **Testcontainers** for integration tests with real dependencies (e.g., databases) in Docker containers.
- **`Actuator`:** Always include the `spring-boot-starter-actuator` for monitoring, health (`/health`), and metrics.
- **Security:** Use **Spring Security** for authentication and authorization.