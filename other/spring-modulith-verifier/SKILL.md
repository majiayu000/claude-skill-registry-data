---
name: spring-modulith-verifier
description: >
  Verifies whether code follows Spring Modulith code structure or not.
  Show list of violations along with recommendations on how to fix them.
  Use this skill:
    * When reviewing Spring Boot applications which uses Spring Modulith
    * When verifying whether Spring Boot application code follows Spring Modulith package structure
---

# Spring Modulith Verifier Skill

Use a **domain-driven, modular layout**: organize packages by **business modules**, not by technical layers.

### Recommended Example Package Structure

```
dev.sivalabs.projectname/
├── Application                      # Main Spring Boot entrypoint class
├── shared/                          # Cross-cutting concerns
│   ├── package-info.java
├── users/                           # Users module (bounded context)
│   ├── config/                      # Users module-specific config
│   ├── domain/                      # Domain logic
│   │   ├── models/                  # Domain models
│   │   │   ├── package-info.java
│   │   ├── exceptions/              # Domain custom Exception classes
│   │   │   ├── package-info.java
│   │   ├── {entities, repositories, mappers, services}
│   ├── api/                        # REST API layer
│   │   ├── {controllers, DTOs}      # REST controllers, Request, Response payload DTOs
│   └── UsersAPI.java                # Module's public API (facade)
│
├── catalog/                         # Catalog module
├── orders/                          # Orders module
└── config/                          # Global Configuration
    └── WebMvcConfig.java
    └── SecurityConfig.java
    └── WebSecurityConfig.java
    └── GlobalExceptionHandler.java
```

Explanation of the above package structure:

- **Application.java**: The main Spring Boot entry point class annotated with `@SpringBootApplication`. Contains the `main()` method that bootstraps the application.

- **shared/**: Contains cross-cutting concerns and utilities shared across multiple modules (e.g., common utilities, shared DTOs, base classes, custom annotations).

- **{module}/** (e.g., users/, catalog/, orders/): Each business module represents a bounded context and contains:

    - **config/**: Module-specific configuration classes annotated with `@Configuration` for beans, properties, or third-party integrations relevant only to this module.

    - **domain/**: Core business logic layer containing:
        - **models/**: Domain model classes (Command, Query objects, Enums, Value Objects, Result objects, etc) representing business concepts (not JPA entities). These are pure Java objects that encapsulate business rules.
        - **exceptions/**: Domain specific custom Exception classes.
        - **entities**: JPA entity classes annotated with `@Entity` that map to database tables. These should not be `public` to prevent direct instantiation and ensure encapsulation.
        - **repositories**: Spring Data JPA repository interfaces extending `JpaRepository` or `CrudRepository` for data access. These should not be `public`.
        - **mappers**: Mapper classes/interfaces (e.g., MapStruct mappers) for converting between entities, domain models, and DTOs. These should not be `public`.
        - **services**: Service classes annotated with `@Service` containing business logic, converting beans using mappers, transaction management, and orchestration of repository calls.

    - **api/**: REST API layer containing:
        - **controllers**: REST controller classes annotated with `@RestController` that handle HTTP requests, validate input, and delegate to services.
        - **DTOs**: Data Transfer Objects including request payloads (data coming from clients) and response payloads (data sent to clients).

    - **{Module}API.java**: A facade class that serves as the module's public API, delegating calls to services, exposing only what other modules should access while hiding internal implementation details.

- **config/**: Global application-wide configuration classes including:
    - **WebMvcConfig.java**: MVC configuration (CORS, interceptors, formatters).
    - **SecurityConfig.java**: Spring Security configuration for authentication and authorization.
    - **GlobalExceptionHandler.java**: Centralized exception handling using `@RestControllerAdvice` for consistent error responses.

### Visibility Modifiers

Default to **minimum necessary visibility**. Only expose what other modules or layers genuinely need.

| Component                | Class                       | Constructor     | Methods         |
|--------------------------|-----------------------------|-----------------|-----------------|
| Controller               | package-private             | package-private | package-private |
| Service                  | `public`                    | package-private | `public`        |
| Repository               | package-private (interface) | —               | —               |
| Entity                   | package-private             | protected       | `public`        |
| DTO / record             | `public` or package-private | —               | —               |
| Module API facade        | `public`                    | package-private | `public`        |
| Request/Response records | package-private             | —               | —               |
| Config/Exception handler | package-private             | —               | —               |


### Naming Conventions

| Type                  | Convention           | Example                                                     |
|-----------------------|----------------------|-------------------------------------------------------------|
| **Entities**          | `*Entity`            | `UserEntity`, `AddressEntity`                               |
| **Value Objects**     | Domain name (record) | `Email`, `UserCode`, `UserId`                               |
| **Commands**          | `*Cmd`               | `CreateUserCmd`, `UpdateAddressCmd`                         |
| **Command Response**  | `*Result`            | `LoginResult`, `RegistrationResult`                         |
| **DTOs**              | `*Dto`               | `UserDto`, `AddressDto`                                     |
| **HTTP Request**      | `*Request`           | `CreateUserRequest`, `CreateAddressRequest`                 |
| **HTTP Response**     | `*Response`          | `CreateUserResponse`, `CreateAddressResponse`               |
| **Repositories**      | `*Repository`        | `UserRepository`, `AddressBookRepository`                   |
| **Services**          | `*Service`           | `UserService`, `AddressBookService`                         |
| **Domain Exceptions** | `*Exception`         | `InvalidUserCreationException`, `UserCancellationException` |
| **Module API**        | `*API`               | `UsersAPI`                                                  |
