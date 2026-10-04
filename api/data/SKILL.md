---
name: data
description: Generate data layer code (Freezed DTOs, repository implementations, data sources) from feature specifications or API references. Creates the bridge between domain entities and external data sources. Use after /domain to implement the data layer.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Data - Data Layer Generator

Generate data layer components that implement domain interfaces and handle external data sources.

## Philosophy

The data layer is the **only place** for:
- Freezed models with JSON serialization
- API field mapping (`@JsonKey`)
- Repository implementations
- Data source abstractions (remote, local, cache)

This keeps the domain pure while handling all serialization and external communication here.

## When to Use This Skill

- After `/domain` has created entities and repository interfaces
- When implementing API integration
- When adding local storage/caching
- When you have backend code or OpenAPI specs as reference
- User asks to "implement repository", "create DTOs", or "wire up API"

> **Note:** This skill replaces the former `/api` skill. All API integration functionality is now here.

## What This Skill Creates

```
lib/features/{feature}/data/
├── models/
│   ├── {entity}_model.dart       # Freezed DTO with JSON
│   └── {entity}_model.g.dart     # Generated JSON code
├── repositories/
│   └── {feature}_repository_impl.dart  # Implements domain interface
└── data_sources/
    ├── {feature}_remote_data_source.dart   # API calls
    └── {feature}_local_data_source.dart    # Local storage (optional)
```

## Input Sources

| Source | What Claude Extracts |
|--------|---------------------|
| Feature spec (`.spec.md`) | Endpoints, DTOs, storage needs |
| Backend code (NestJS, Express) | Controllers, DTOs, types |
| OpenAPI/Swagger spec | Paths, schemas, request/response shapes |
| Endpoint descriptions | `GET /users → User[]` |

## Workflow

### Step 1: Locate Requirements

Check for:
```
lib/features/{feature}/.spec.md           # Feature specification
lib/features/{feature}/domain/            # Domain entities/repository interface
```

If domain layer doesn't exist, ask user to run `/domain {feature}` first.

### Step 2: Analyze Data Sources

**From spec:**
- **API Endpoints** - Section 3.1 (URLs, methods, request/response shapes)
- **Local Storage** - Section 3.2 (what to persist, cache strategy)
- **Field Mappings** - API field names vs domain field names

**From backend code (if provided):**
- Extract endpoint paths from controllers/routes
- Extract request/response shapes from DTOs
- Map snake_case API fields to camelCase Dart fields

### Step 3: Generate Code

Use reference files in `reference/` directory as templates:

| Component | Reference File |
|-----------|----------------|
| Simple DTO | `reference/models/simple_model.dart` |
| Nested DTO | `reference/models/nested_model.dart` |
| Custom converters | `reference/models/custom_converter_model.dart` |
| Request DTOs | `reference/models/request_models.dart` |
| Pagination | `reference/models/paginated_response.dart` |
| Basic repository | `reference/repositories/basic_repository_impl.dart` |
| Cached repository | `reference/repositories/cached_repository_impl.dart` |
| Mock repository | `reference/repositories/mock_repository.dart` |
| Remote data source | `reference/data_sources/remote_data_source.dart` |
| Local (prefs) | `reference/data_sources/local_data_source_prefs.dart` |
| Local (secure) | `reference/data_sources/local_data_source_secure.dart` |
| Failures | `reference/failures/failures.dart` |
| Error mapping | `reference/failures/dio_error_handler.dart` |
| i18n mapping | `reference/failures/failure_mapper.dart` |
| Provider registration | `reference/providers/repository_provider.dart` |

### Step 4: Run Code Generation

```bash
dart run build_runner build --delete-conflicting-outputs
```

### Step 5: Verify

```bash
dart run .claude/skills/data/scripts/check.dart {feature}
```

## Commands

```bash
# Generate data layer from spec
/data {feature}

# Generate only DTOs
/data {feature} --only=models

# Generate only repository implementation
/data {feature} --only=repository

# Add new endpoint to existing data layer
/data {feature} --add-endpoint={methodName}
```

## Checklist

Before finishing data layer generation:

- [ ] All DTOs match API response shapes
- [ ] `@JsonKey` mappings handle snake_case → camelCase
- [ ] `toEntity()` and `fromEntity()` methods implemented
- [ ] Repository implements all domain interface methods
- [ ] Data source handles all API endpoints
- [ ] Error handling uses typed Failures (no hardcoded strings)
- [ ] Nullable fields handled correctly
- [ ] Run `build_runner` to generate code
- [ ] No lint errors after generation

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| DTO class | {Entity}Model | `MemoryModel` |
| DTO file | {entity}_model.dart | `memory_model.dart` |
| Repository impl | {Feature}RepositoryImpl | `MemoriesRepositoryImpl` |
| Remote data source | {Feature}RemoteDataSource | `MemoriesRemoteDataSource` |
| Local data source | {Feature}LocalDataSource | `MemoriesLocalDataSource` |

## Data Layer Rules

1. **Freezed for all DTOs** - Immutability + JSON + equality
2. **Always map to domain** - `toEntity()` and `fromEntity()` required
3. **Handle API field names** - Use `@JsonKey` for snake_case
4. **Repository is the boundary** - Only repository returns domain entities
5. **Data sources return DTOs** - Never return domain entities from data sources
6. **Typed failures** - No hardcoded error strings, use Failure types

## What Goes Where

| Concern | Layer | Example |
|---------|-------|---------|
| Entity fields & business logic | Domain | `Memory.isSynced` |
| JSON serialization | Data | `@JsonKey(name: 'is_synced')` |
| API endpoints | Data | `_dio.get('/memories')` |
| Field mapping | Data | `toEntity()`, `fromEntity()` |
| Error types | Data | `NetworkFailure.noConnection()` |
| Error messages | Presentation | `t.errors.noConnection` (i18n) |

## Guides

| Guide | Use For |
|-------|---------|
| [patterns-guide.md](patterns-guide.md) | Basic pattern descriptions and when to use |
| [advanced-patterns.md](advanced-patterns.md) | Pagination, retry, caching, uploads, auth interceptor |
| [examples.md](examples.md) | Complete before/after examples by input source |
| [reference/](reference/) | Actual code templates |

## Related Skills

- `/domain` - Run first to create entities and repository interfaces
- `/feature-init` - Initialize feature scaffold (run before /domain and /data)
- `/plan` - Plan data sources before implementation
- `/presentation` - Implement UI layer after data layer is complete
- `/testing` - Create tests for repositories and data sources
- `/i18n` - Localize error messages (via failure mapper)
