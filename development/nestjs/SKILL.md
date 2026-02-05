---
name: nestjs
version: 1.0.0
description: Build production-ready NestJS modules with entities, DTOs, services, controllers
scope: project
lastUpdated: 2025-12-30
learningCount: 0
successRate: 0
---

# NestJS Skill

Build production-ready NestJS modules with entities, DTOs, services, controllers.

## When to Use

- Creating new domain modules
- Adding entities to existing modules
- Creating CRUD endpoints
- Database migrations
- API design

## File Patterns

- `*.module.ts`
- `*.controller.ts`
- `*.service.ts`
- `*.entity.ts`
- `*.dto.ts`

## Quick Reference

### Layer Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **Controller** | HTTP handling + Business logic |
| **Service** | Database access ONLY |

### Service = Thin Data Access

Services contain ONLY database operations:
- `findById()`, `findByField()` - return entity or null
- `findAll()` - return arrays
- `save()`, `softRemove()`, `restore()` - mutations
- NO exceptions, NO business logic

### Controller = Business Logic

Controllers handle:
- HTTP routing and response formatting
- Business rule validation (duplicates, constraints)
- Exception throwing
- Calling service methods

## Progressive Content

| File | When to Load |
|------|--------------|
| `knowledge/learnings.md` | Starting NestJS task |
| `knowledge/patterns.md` | Looking for examples |
| `knowledge/anti-patterns.md` | Reviewing code or fixing issues |
| `rules/conventions.md` | Writing new code |

## Commands Added

| Command | Description |
|---------|-------------|
| `/nestjs-scaffold [name]` | Create complete module with all files |
| `/nestjs-entity [name]` | Create TypeORM entity |
| `/nestjs-dto [name]` | Create DTO with validation |
| `/nestjs-migration [name]` | Generate database migration |
| `/nestjs-db migrate` | Run pending migrations |
| `/nestjs-db seed` | Run seed data |

## Module Structure

```
src/{module}/
├── entities/
│   ├── {entity-name}.entity.ts
│   └── index.ts
├── dto/
│   ├── create-{entity}.dto.ts
│   ├── update-{entity}.dto.ts
│   └── index.ts
├── {module}.service.ts
├── {module}.controller.ts
└── {module}.module.ts
```

## Templates

See `templates/` directory for:
- `entity.template.ts` - TypeORM entity
- `dto.template.ts` - DTOs with validation
- `service.template.ts` - Data access service
- `controller.template.ts` - REST controller
- `module.template.ts` - NestJS module
- `migration.template.ts` - Database migration
