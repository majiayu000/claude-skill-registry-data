---
name: spring-boot-fallback
category: architecture
description: Use when Java is chosen but Quarkus does not fit - build the service with Spring Boot using the same clean layering, only when a required library lacks a Quarkus extension or the repo already standardizes on Spring
tech_stack: Java
---
# Spring Boot Fallback

## Overview

Quarkus is the default (see quarkus-service-architecture). Spring Boot is the fallback — reach for it only when Quarkus genuinely does not fit. The architecture is the same clean layering; only the annotations and container differ.

**Core principle:** Same layered design as Quarkus. Spring is a container choice, not a license to sprawl.

## When Spring Boot instead of Quarkus

- The repository already uses Spring Boot — follow it.
- A required library/integration has no Quarkus extension and no clean CDI alternative.
- The deployment target or team standard mandates Spring.

If none of these hold, use Quarkus.

## Layer mapping (same responsibilities, Spring surface)

| Layer | Quarkus | Spring Boot |
|-------|---------|-------------|
| Resource/Controller | JAX-RS `@Path` | `@RestController` `@RequestMapping` |
| Service | `@ApplicationScoped` | `@Service` |
| Repository | Panache | `JpaRepository` (Spring Data) |
| Validation | `@Valid` + Bean Validation | `@Valid` + Bean Validation |
| Config | `@ConfigProperty` | `@ConfigurationProperties` / `@Value` |
| Transaction | `@Transactional` (service) | `@Transactional` (service) |

## Patterns (identical discipline)

- **Constructor injection only** — Spring injects a single constructor automatically; no `@Autowired` on fields.
- **DTOs (records) at the controller edge**; never return JPA entities from a controller.
- **Bean Validation** on request DTOs, `@Valid` on the controller method.
- Domain invariants live in the domain class, not only in the DTO annotations.
- Global error handling via `@RestControllerAdvice` mapping domain exceptions to status codes — controllers stay thin.

## Worked Example

```java
@RestController
@RequestMapping("/tasks")
class TaskController {
    private final TaskService service;
    TaskController(TaskService service) { this.service = service; }   // constructor injection

    @PostMapping
    ResponseEntity<TaskResponse> create(@Valid @RequestBody CreateTaskRequest req) {
        Task t = service.create(req.title());
        return ResponseEntity.status(201).body(TaskResponse.from(t));
    }
}

@Service
class TaskService {
    private final TaskRepository repo;
    TaskService(TaskRepository repo) { this.repo = repo; }

    @Transactional
    Task create(String title) {
        Task t = Task.create(title);   // domain enforces invariants
        return repo.save(t);
    }
}
```

## Boot 4 notes

- Spring Boot 4.x runs on Spring Framework 7 and Jakarta EE 11; Java 17 is the floor, 25 is recommended. Never bump a repo's Boot major in a feature task — 3.5's open-source support ended 2026-06-30, so a repo still on 3.5 should be flagged, not silently upgraded mid-task.
- Jackson 3 (`tools.jackson.*`) replaces the `com.fasterxml.jackson.*` import paths used through Boot 3.x — check which the repo is on before copying an import.
- Error responses: `ProblemDetail` + `spring.mvc.problemdetails.enabled=true`, or throw `ErrorResponseException` — see api-design-conventions for the shape.
- Outbound HTTP: prefer `RestClient` or a declarative `@HttpExchange` interface client over a hand-rolled `RestTemplate` call.
- Boot 4 has built-in API versioning (`spring.mvc.apiversion.*`) — use it instead of a custom header/path scheme when the repo needs to version an endpoint.
- `ResponseEntity.created(uri)` for a 201 with `Location` set, rather than building the header by hand.
- `spring.jpa.open-in-view=false` (java-persistence) and structured logging (`logging.structured.format.console=ecs`, available since 3.4) are repo-level settings, not per-task changes — follow what's already set.
- `@MockitoBean`/`@MockitoSpyBean` replace `@MockBean`/`@SpyBean` (removed in 4.0) — see java-testing-junit-mockito.

## Common Mistakes

- Choosing Spring by habit when Quarkus fits — Quarkus is the default.
- `@Autowired` field injection — use the constructor.
- Business logic in `@RestControllerAdvice` or the controller.
- Returning entities instead of DTOs.
- Using `@MockBean`/`RestTemplate`-only patterns on a Boot 4 repo where the current idiom (`@MockitoBean`, `RestClient`) already applies.

## Red Flags

- You chose Spring but can't name why Quarkus didn't fit.
- Fat controller, anemic service.
