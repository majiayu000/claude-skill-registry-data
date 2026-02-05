---
name: Project Folder Structure and Organization Understanding Capabillity
description: Understand the already-done project folder structure, archtecture, file patterns, and similar, in order to apply better solutions and file organizations. Use when you need to understand the project archtecture, and file/folder patterns and conventions.
---

# Basic Understanding

## Folder Structure

```
src/
├── domain/                         # Application CORE (pure TypeScript, framework-free)
│   ├── @shared/                    # Shared between bounded contexts
│   │   ├── entities/               # Base Entity, base AggregateRoot
│   │   ├── value-objects/          # Base ValueObject, UniqueEntityId
│   │   ├── errors/                 # Base DomainError
│   │   └── either.ts               # Either pattern (Left/Right)
│   │
│   └── [bounded-context]/          # E.g.: identity, catalog, orders, billing
│       ├── enterprise/             # Enterprise Layer (entities and business rules)
│       │   ├── entities/           # Domain entities
│       │   └── value-objects/      # Specific Value Objects
│       │
│       ├── application/            # Application Layer (use cases)
│       │   ├── use-cases/          # Use cases
│       │   └── repositories/       # Repository interfaces (contracts)
│       │
│       └── errors/                 # Bounded context specific errors
│
├── infra/                          # Infrastructure implementations
│   ├── database/
│   │   ├── prisma/                 # Prisma Client, migrations
│   │   └── repositories/           # Repository implementations
│   │
│   ├── cryptography/               # Hashing, JWT, etc.
│   └── cache/                      # Redis, etc.
│
├── http/                           # HTTP Layer (NestJS)
│   ├── app.module.ts
│   ├── main.ts
│   └── [module]/                   # E.g.: auth, users, products
│       ├── controllers/            # Receives request, calls service
│       ├── services/               # Instantiates and executes use-case
│       ├── schemas/                # Zod schemas for validation
│       ├── pipes/                  # Validation pipes
│       ├── presenters/             # Transforms entity into response
│       └── [module].module.ts
│
└── env/                            # Environment configuration
    └── env.ts
```

## Dependency Rules

```
HTTP (NestJS) --> Application (Use Cases) --> Enterprise (Entities)
      |                  |
      v                  v
   Infra  <-----------  Repositories (interfaces)
```

## Planned Bounded Contexts

| Context  | Responsibility                     |
| -------- | ---------------------------------- |
| identity | Users, authentication, permissions |
| [others] | Define according to business needs |

## File Naming

| Type         | Suffix           | Example                           |
| ------------ | ---------------- | --------------------------------- |
| Entity       | `.entity.ts`     | `user.entity.ts`                  |
| Value Object | `.vo.ts`         | `email.vo.ts`                     |
| Use Case     | `.use-case.ts`   | `create-account.use-case.ts`      |
| Repository   | `.repository.ts` | `users.repository.ts`             |
| Error        | `.error.ts`      | `account-already-exists.error.ts` |
| Controller   | `.controller.ts` | `auth.controller.ts`              |
| Service      | `.service.ts`    | `auth.service.ts`                 |
| Schema       | `.schema.ts`     | `auth.controller.schema.ts`       |
| Presenter    | `.presenter.ts`  | `user.presenter.ts`               |
| Mapper       | `.mapper.ts`     | `prisma-user.mapper.ts`           |
| Pipe         | `.pipe.ts`       | `zod-validation.pipe.ts`          |
| Guard        | `.guard.ts`      | `auth.guard.ts`                   |
| Decorator    | `.decorator.ts`  | `public.decorator.ts`             |
| Enum         | `.enum.ts`       | `role.enum.ts`                    |
| Provider     | `.provider.ts`   | `bcrypt.provider.ts`              |

## Tests

```
src/domain/[bounded-context]/application/use-cases/__tests__/
  create-account.use-case.spec.ts

src/http/[module]/__tests__/
  auth.e2e-spec.ts
```

- Unit tests for use-cases (mocking repositories)
- E2E tests for controllers

# Scripts for full understanding (MUST USE)

- Use the `.claude/skills/structure_understander/scripts/read-structure.py` to get recursivelly all folders and files by name, organizated in an understandable structure.
