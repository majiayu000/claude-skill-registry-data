---
name: ddd-model
description: >
  Interactive Domain-Driven Design modeling workflow. Use when you need to:
  design a new domain, identify Aggregates and Entities, choose architecture,
  define invariants. Generates Go code following Uber Style Guide.
argument-hint: [domain-name]
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion
---

# DDD Domain Modeling Skill

This skill guides you through a complete DDD modeling cycle for Go projects.

## Overview

The workflow consists of 6 phases:
1. **Domain Discovery** - Understand the domain and subdomain type
2. **Bounded Contexts** - Define context boundaries and ubiquitous language
3. **Tactical Modeling** - Identify Entities, Value Objects, Aggregates
4. **Invariants** - Define business rules that must always hold
5. **Code Generation** - Generate Go code with Clean Architecture
6. **Validation** - Check DDD rules compliance

## Quick Start

When user invokes `/ddd-model [domain-name]`:

1. Read `workflow.md` for detailed phase instructions
2. Use `AskUserQuestion` to gather information at each phase
3. Read templates from `templates/` for code generation
4. Apply rules from `rules/` for validation
5. Reference `examples/banking.md` for real-world example

## Phase 1: Domain Discovery

Start by understanding the domain:

```
AskUserQuestion:
- "Describe the domain/subdomain you want to model"
- "What type of subdomain is this?" → Core / Supporting / Generic
- "What are the main business processes?"
```

Based on subdomain type, determine DDD investment level:
- **Core** → Full DDD (Aggregates, Domain Events, CQRS if needed)
- **Supporting** → Simplified DDD (Aggregates, basic patterns)
- **Generic** → CRUD/Transaction Script (minimal DDD)

## Phase 2: Bounded Contexts

Identify and define bounded contexts:

1. List key domain concepts through questions
2. Propose BC boundaries (with ASCII diagram)
3. Define Ubiquitous Language for each BC
4. Map relationships between BCs (Context Map)

Example Context Map:
```
┌─────────────┐     ┌─────────────┐
│  Accounts   │────>│  Transfers  │
│    (Core)   │     │   (Core)    │
└─────────────┘     └─────────────┘
       │                   │
       v                   v
┌─────────────┐     ┌─────────────┐
│    Fees     │     │   Loyalty   │
│ (Supporting)│     │   (Core)    │
└─────────────┘     └─────────────┘
```

## Phase 3: Tactical Modeling

For each Bounded Context, identify building blocks:

```
AskUserQuestion for each concept:
- "What has a unique identity?" → Entity
- "What is defined only by its values?" → Value Object
- "What entities always change together?" → Aggregate
- "What is the entry point to the aggregate?" → Aggregate Root
```

Decision Tree for Entity vs Value Object:
```
Does it have identity?
├── YES: Does identity matter for equality?
│   ├── YES → Entity
│   └── NO → Value Object with ID field
└── NO: Is it immutable?
    ├── YES → Value Object
    └── NO → Consider making it immutable
```

## Phase 4: Invariants

For each Aggregate, define invariants:

```
AskUserQuestion:
- "What business rules MUST always be true?"
- "What cannot be violated during changes?"
- "What conditions trigger errors?"
```

Format invariants as:
```go
// Invariant: Account balance cannot be negative
// Invariant: Transfer amount must be positive
// Invariant: Account must have at least one owner
```

## Phase 5: Code Generation

Generate Go code following Clean Architecture:

1. Read `rules/clean-arch.md` for folder structure
2. Use templates from `templates/`:
   - `aggregate.go.md` - Aggregate Root template
   - `entity.go.md` - Entity template
   - `value-object.go.md` - Value Object template
   - `repository.go.md` - Repository interface template
3. Generate files in:
   - `internal/domain/<bc>/` - Domain layer
   - `internal/application/<bc>/` - Application layer
   - `internal/infrastructure/<bc>/` - Infrastructure layer

## Phase 6: Validation

Output validation checklist:

```markdown
## DDD Validation Checklist

### Aggregate Rules
- [ ] Aggregate Root is the only entry point
- [ ] All changes go through Aggregate Root methods
- [ ] Invariants are checked in constructor and methods
- [ ] No direct references to other Aggregates (only IDs)
- [ ] One Aggregate = one transaction boundary

### Entity Rules
- [ ] ID is immutable after creation
- [ ] Equals/HashCode based on ID only

### Value Object Rules
- [ ] Fully immutable (no setters)
- [ ] Equals compares all fields
- [ ] Validation in constructor
```

## Uber Go Style Guide Conventions

Apply these conventions in generated code:

- **Value receivers** for Value Objects (immutable)
- **Pointer receivers** for Aggregates/Entities (mutable)
- **Compile-time interface checks**: `var _ Repository = (*PostgresRepo)(nil)`
- **Domain-specific error types**: `type InsufficientFundsError struct{}`
- **Package names** = bounded context names (lowercase)
- **Constructor functions**: `NewAccount()`, `MustMoney()` for tests

## File References

- Detailed workflow: `workflow.md`
- DDD rules checklist: `rules/ddd-rules.md`
- Clean Architecture guide: `rules/clean-arch.md`
- Invariants guide: `rules/invariants.md`
- Code templates: `templates/*.go.md`
- Example domain: `examples/banking.md`
