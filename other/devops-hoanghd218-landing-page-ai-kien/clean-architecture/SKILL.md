---
name: clean-architecture
description: Apply Clean Architecture layering and dependency rules (Domain, Application, Infrastructure, Presentation layers). Use when structuring applications or ensuring dependencies point inward.
---

# Clean Architecture Skill

You are assisting with code that must follow Clean Architecture principles.

## Core Concept

**Dependency Rule**: Source code dependencies must point INWARD toward higher-level policies.
- Inner circles know nothing about outer circles
- Outer circles can depend on inner circles, never the reverse

## Architecture Layers (from innermost to outermost)

### 1. Entities (Domain Layer)
**What**: Enterprise business rules, domain models
**Responsibilities**:
- Pure business logic
- Domain entities and value objects
- No framework dependencies
- No infrastructure concerns

**For admission system**:
- `Student`, `Course`, `AdmissionRule`, `Grade`, `Quota`
- Business validation rules
- Domain events

### 2. Use Cases (Application Layer)
**What**: Application-specific business rules
**Responsibilities**:
- Orchestrate data flow between entities
- Implement application business rules
- Coordinate entity interactions
- Define input/output boundaries (DTOs)

**For admission system**:
- `EvaluateAdmissionUseCase`
- `CalculateCompetencePointsUseCase`
- `ApplyQuotaRulesUseCase`

### 3. Interface Adapters (Infrastructure Layer)
**What**: Convert data between use cases and external agencies
**Responsibilities**:
- Controllers, presenters, gateways
- Repository implementations
- API adapters
- Data mappers

**For admission system**:
- `AdmissionRuleRepository`
- `StudentGateway`
- `RESTController`
- Database adapters

### 4. Frameworks & Drivers (External Layer)
**What**: External tools and frameworks
**Responsibilities**:
- Web frameworks (FastAPI, Flask)
- Database (PostgreSQL, MongoDB)
- UI frameworks
- External APIs

## Key Patterns

### Dependency Inversion at Boundaries
```python
# GOOD: Use case depends on abstraction
class EvaluateAdmissionUseCase:
    def __init__(self, rule_repository: RuleRepositoryProtocol):
        self._repository = rule_repository

# Repository implementation is in outer layer
class PostgresRuleRepository(RuleRepositoryProtocol):
    pass
```

### The Dependency Rule
```
[Entities] <- [Use Cases] <- [Interface Adapters] <- [Frameworks]
   (Domain)    (Application)     (Infrastructure)        (External)
```

### Input/Output Boundaries
- Use DTOs (Data Transfer Objects) for crossing boundaries
- Never pass entity objects to outer layers
- Keep entities pure and protected

## Directory Structure for Clean Architecture

```
src/
├── domain/              # Entities layer
│   ├── entities/
│   ├── value_objects/
│   └── domain_services/
├── application/         # Use cases layer
│   ├── use_cases/
│   ├── ports/          # Interfaces/protocols
│   └── dtos/           # Input/output models
├── infrastructure/      # Interface adapters
│   ├── repositories/
│   ├── gateways/
│   └── adapters/
└── presentation/        # External layer
    ├── api/            # REST/GraphQL
    ├── cli/
    └── web/
```

## Rules to Enforce

### 1. No Inward Dependencies
- Domain layer has ZERO external imports
- Use cases only import from domain and application
- Never import outer layers in inner layers

### 2. Business Logic in Domain
- Keep business rules in entities
- Use cases orchestrate, entities decide
- No business logic in controllers/adapters

### 3. Framework Independence
- Core business logic works without frameworks
- Can swap FastAPI for Flask without touching domain
- Database is a detail, can be changed

### 4. Testability
- Domain and use cases are easily testable
- No need to mock frameworks for business logic tests
- Use test doubles for ports/protocols

## Code Review Checklist

- [ ] Are dependencies pointing inward only?
- [ ] Is business logic in the domain layer?
- [ ] Are use cases framework-independent?
- [ ] Are abstractions defined in inner layers?
- [ ] Are DTOs used for boundary crossing?
- [ ] Can the domain be tested without infrastructure?

## Practical Application for Admission Rules

### Domain Layer
- `AdmissionRule` entity with evaluation logic
- `Student` entity with validation
- `CompetencePoints` value object

### Application Layer
- `EvaluateAdmissionUseCase(student_id, program_id)`
- `RuleRepositoryProtocol` interface
- Input/output DTOs

### Infrastructure Layer
- `SQLAlchemyRuleRepository` implementing protocol
- `SamordnaOpptak` external API adapter

### Presentation Layer
- FastAPI routes
- CLI commands
- Response formatters

## Response Format

When applying Clean Architecture:
1. Identify which layer the code belongs to
2. Check dependencies follow the inward rule
3. Ensure proper separation of concerns
4. Suggest refactoring if layers are mixed
5. Provide clean structure following the architecture
