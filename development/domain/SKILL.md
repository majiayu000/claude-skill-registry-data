---
name: domain
description: Generate domain layer code (entities, enums, repository interfaces) from feature specifications. Creates pure Dart business logic with no external dependencies. Use after /feature-init to fill in the domain layer.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Domain - Domain Layer Generator

Generate domain layer components from feature specifications. Creates the foundation that data and presentation layers build upon.

## Philosophy

The domain layer is **pure Dart** with zero external dependencies:
- No Flutter
- No Freezed (that's for data layer DTOs)
- No JSON serialization
- Only language primitives

This ensures the domain is:
- Framework-agnostic
- Easily testable
- Stable (changes least frequently)

## When to Use This Skill

- After `/feature-init` has created the folder structure
- When you need to fill in entities, enums, or repository interfaces
- When adding new domain concepts to an existing feature
- User asks to "create domain", "generate entities", or "create repository interface"

## What This Skill Creates

```
lib/features/{feature}/domain/
├── entities/
│   ├── {entity}.dart           # Pure Dart class
│   └── {value_object}.dart     # Value objects (if needed)
├── enums/
│   └── {enum_name}.dart        # Enum definitions
└── repositories/
    └── {feature}_repository.dart  # Abstract interface
```

## Workflow

### Step 1: Locate the Spec

Look for:
```
lib/features/{feature}/.spec.md     # If feature exists
docs/features/{feature}.spec.md     # If feature is new
```

If no spec exists, ask user to run `/plan {feature}` first.

### Step 2: Extract Domain Requirements

From the spec, identify:
- **Entities** - Section 2.1 (fields, types, required/optional)
- **Enums** - Section 2.2 (values and descriptions)
- **Repository Interface** - Section 2.3 (methods and signatures)
- **Value Objects** - Composite types like LatLng, Money
- **Business Rules** - Validation, computed properties

### Step 3: Generate Code

Use reference files in `reference/` directory as templates:

| Component | Reference File |
|-----------|----------------|
| Simple entity | `reference/entities/simple_entity.dart` |
| Entity with computed | `reference/entities/entity_with_computed.dart` |
| Entity with equality | `reference/entities/entity_with_equality.dart` |
| Entity with copyWith | `reference/entities/entity_with_copywith.dart` |
| LatLng value object | `reference/value_objects/lat_lng.dart` |
| Money value object | `reference/value_objects/money.dart` |
| Simple enum | `reference/enums/simple_enum.dart` |
| Enum with properties | `reference/enums/enum_with_properties.dart` |
| Enum with methods | `reference/enums/enum_with_methods.dart` |
| Basic CRUD repository | `reference/repositories/basic_crud_repository.dart` |
| Paginated repository | `reference/repositories/paginated_repository.dart` |
| Offline repository | `reference/repositories/offline_repository.dart` |

### Step 4: Verify

```bash
dart run .claude/skills/domain/scripts/check.dart {feature}
```

## Commands

```bash
# Generate domain layer from spec
/domain {feature}

# Generate only entities
/domain {feature} --only=entities

# Generate only repository interface
/domain {feature} --only=repository

# Add entity to existing feature
/domain {feature} --add-entity={EntityName}
```

## When to Add What

| Need | Add |
|------|-----|
| Just store data | Nothing extra |
| Compare instances | `==` and `hashCode` |
| Update immutably | `copyWith` |
| Debug output | `toString` |

**Default: Add nothing extra. Only add when there's a clear need.**

## Checklist

Before finishing domain generation:

- [ ] All entities from spec are created
- [ ] All enums from spec are created
- [ ] Repository interface has all methods from spec
- [ ] All fields have correct types
- [ ] Required vs optional fields match spec
- [ ] Computed properties are implemented
- [ ] Doc comments explain purpose
- [ ] **No external dependencies** (pure Dart only)
- [ ] Files follow naming convention ({snake_case}.dart)
- [ ] `==`/`hashCode` added only where needed
- [ ] `copyWith` added only where needed

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Entity class | PascalCase, `final` | `final class Memory` |
| Entity file | snake_case | `memory.dart` |
| Enum | PascalCase | `SyncStatus` |
| Enum values | camelCase | `pending`, `inProgress` |
| Repository | {Feature}Repository | `MemoriesRepository` |
| Value object | PascalCase, `final` | `final class LatLng` |

## Domain Layer Rules

1. **No Flutter imports** - Domain is pure Dart
2. **No Freezed** - That's for data layer DTOs
3. **No JSON/serialization** - Data layer concern
4. **No implementation details** - Repository is interface only
5. **Minimal boilerplate** - Only add `==`/`hashCode`/`copyWith` when needed

## Guides

| Guide | Use For |
|-------|---------|
| [patterns-guide.md](patterns-guide.md) | Pattern descriptions and when to use |
| [reference/](reference/) | Actual code templates |

## Related Skills

- `/plan` - Run first to create feature specification
- `/feature-init` - Initialize feature scaffold (run before /domain)
- `/data` - Implement repository and data sources after domain
- `/presentation` - Implement UI layer after data
- `/testing` - Create unit tests for domain logic
