---
name: documentation
description: Generate Javadoc, README files, ADRs (Architecture Decision Records), and technical documentation for Java/Spring Boot projects. Use this skill whenever the user needs to write documentation, create a README, document a class or method, write an ADR, generate Javadoc, or says things like "document this code", "write a README for X", "add Javadoc to this", "write an ADR for this decision", "document this API", "create technical documentation". Always use this skill for any documentation task in a Java/Spring Boot context.
---

# Java Documentation Skill

Generate clear, useful documentation — Javadoc, README, ADRs, and technical guides — for Java/Spring Boot projects.

## Javadoc Standards

### Class-Level Javadoc

```java
/**
 * Service responsible for managing the user lifecycle including registration,
 * profile updates, and account deactivation.
 *
 * <p>All write operations are transactional. Read operations use
 * {@code @Transactional(readOnly = true)} for performance optimization.
 *
 * <p>Authentication is handled separately by {@link AuthService}.
 *
 * @author [Author]
 * @since 1.0
 * @see UserRepository
 * @see AuthService
 */
@Service
public class UserServiceImpl implements UserService { ... }
```

### Method-Level Javadoc

```java
/**
 * Retrieves a user by their unique identifier.
 *
 * @param id the user's unique identifier, must be positive
 * @return the user response DTO
 * @throws ResourceNotFoundException if no user exists with the given id
 * @throws IllegalArgumentException if id is null or negative
 */
UserResponse findById(Long id);
```

**Rules for good Javadoc**:
- Document **why**, not **what** (the code shows what)
- Always document `@throws` for checked and significant unchecked exceptions
- Use `{@link ClassName#method()}` for cross-references
- Document non-obvious parameter constraints (must be positive, cannot be empty)
- Skip Javadoc for self-explanatory getters/setters
- Always add Javadoc to public API interfaces

### Package-Level Documentation (package-info.java)
```java
/**
 * Domain services for the User bounded context.
 *
 * <p>Contains the business logic for user management, authentication,
 * and authorization. Services in this package orchestrate between
 * repositories and external integrations.
 *
 * <p>All services follow the interface/implementation pattern to
 * facilitate testing and dependency inversion.
 */
package com.example.user.service;
```

---

## README Template for Spring Boot Projects

```markdown
# [Project Name]

> One-line description of what this service does.

## Overview

[2-3 paragraph description of the service's purpose, domain, and how it fits 
into the broader system.]

## Technology Stack

- Java 21
- Spring Boot 3.x
- PostgreSQL 15
- [Other key dependencies]

## Prerequisites

- Java 21+
- Docker & Docker Compose
- Maven 3.8+

## Getting Started

### Run with Docker Compose

```bash
docker-compose up -d        # Start dependencies (DB, Kafka, etc.)
./mvnw spring-boot:run      # Start the application
```

### Run tests

```bash
./mvnw test                 # Unit tests
./mvnw verify               # Unit + integration tests
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_URL` | PostgreSQL JDBC URL | `jdbc:postgresql://localhost:5432/mydb` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASS` | Database password | (required) |
| `KAFKA_BOOTSTRAP` | Kafka bootstrap servers | `localhost:9092` |

## API Documentation

Swagger UI available at: `http://localhost:8080/swagger-ui.html`

### Key Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/v1/users` | List all users (paginated) |
| POST | `/api/v1/users` | Create a user |
| GET | `/api/v1/users/{id}` | Get user by ID |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |

## Project Structure

```
src/
├── main/java/com/example/
│   ├── config/          # Spring configuration classes
│   ├── controller/      # REST controllers
│   ├── service/         # Business logic (interfaces + impls)
│   ├── repository/      # Spring Data JPA repositories
│   ├── domain/          # JPA entities
│   ├── dto/             # Request/Response DTOs
│   ├── mapper/          # MapStruct mappers
│   └── exception/       # Custom exceptions + global handler
└── test/
    ├── unit/            # Pure unit tests (Mockito)
    └── integration/     # Spring Boot integration tests
```

## Architecture Decisions

See [docs/adr/](docs/adr/) for Architecture Decision Records.

## Contributing

1. Branch from `develop`
2. Follow the [Java coding standards](docs/coding-standards.md)
3. Ensure all tests pass: `./mvnw verify`
4. Open a PR with description of changes
```

---

## ADR (Architecture Decision Record) Template

```markdown
# ADR-[NUMBER]: [Short Title]

**Date**: YYYY-MM-DD  
**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]  
**Deciders**: [List of people involved]

## Context

[Describe the problem, situation, or requirement that forces a decision.
What constraints exist? What is non-negotiable?]

## Decision

[State the decision clearly. What have we decided to do?]

We will use **[technology/pattern/approach]** because [primary reason].

## Considered Alternatives

### Option 1: [Name] ← Chosen
**Pros**: [Why it's good]  
**Cons**: [Trade-offs accepted]

### Option 2: [Name]
**Pros**: ...  
**Cons**: [Why rejected]

### Option 3: [Name]
**Pros**: ...  
**Cons**: [Why rejected]

## Consequences

**Positive**:
- [Benefit 1]
- [Benefit 2]

**Negative / Trade-offs**:
- [Cost 1 — and how we mitigate it]
- [Cost 2]

**Neutral**:
- [Side effects to be aware of]

## Implementation Notes

[Optional: key technical details, migration steps, or code examples
needed to implement the decision]
```

---

## Inline Code Comments Best Practices

```java
// ✅ Comment explains WHY, not WHAT
// We use a short-lived token (15 min) to minimize exposure if intercepted
private static final int ACCESS_TOKEN_MINUTES = 15;

// ✅ Comment explains non-obvious business rule
// Per regulation §4.2: orders placed after 3PM ship the following business day
if (orderTime.getHour() >= 15) {
    shippingDate = nextBusinessDay(orderTime.toLocalDate());
}

// ✅ TODO with ticket reference
// TODO(JIRA-1234): Replace with circuit breaker once resilience4j is integrated
Thread.sleep(retryDelay);

// ❌ Comment restates the code (useless)
// Increment counter by 1
counter++;

// ❌ Commented-out code (use git instead)
// userRepository.deleteAll();
```

## Changelog Format (CHANGELOG.md)

```markdown
# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [1.2.0] - 2024-01-15

### Added
- Product filtering by category and price range (#142)
- Swagger UI documentation for all endpoints

### Changed
- Improved error response format to include `violations` array for 400 errors

### Fixed
- N+1 query in OrderService.findAllWithItems (#138)
- Missing @Transactional on UserService.transferCredits (#141)

### Security
- Updated spring-security to 6.2.1 (CVE-2024-XXXX)
```
