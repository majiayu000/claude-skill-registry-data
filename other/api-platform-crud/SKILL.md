---
name: api-platform-crud
description: Create complete REST API CRUD operations using API Platform with DDD and CQRS patterns, YAML resource configuration, and the command bus. Use when adding new API resources, implementing CRUD endpoints, creating DTOs, configuring operations, or setting up state processors. Skip when `framework.api_platform` is false.
---

# API Platform CRUD Skill

## Profile keys consumed

- `framework.api_platform`
- `architecture.source_root`, `architecture.bounded_contexts`
- `persistence.mapper`, `persistence.engine`
- `make.ci`, `make.deptrac`, `make.e2e`
- `quality.phpinsights.complexity`, `quality.infection_msi`

## Applicability gate

Branch on `framework.api_platform` before doing anything:

- **`false`** — emit a skip note (`SKIPPED: framework.api_platform is false — no API Platform layer in this repository`) and stop. Do not scaffold resources by hand.
- **Version string** — proceed. The patterns below target the `ApiPlatform\Metadata\*` operation classes (API Platform 3/4 style); confirm against the installed major version.

## Context (Input)

- Need to create a new API resource with REST endpoints
- Implementing CRUD operations (Create, Read, Update, Delete)
- Adding DTOs for input/output transformation
- Configuring API Platform operations, filters, or pagination
- Working with state processors following the CQRS pattern

## Task (Function)

Implement production-ready REST API CRUD operations following DDD, CQRS, and hexagonal architecture patterns.

**Success Criteria**:

- All CRUD operations functional (POST, GET, PUT, PATCH, DELETE)
- DTOs properly validated
- Domain entities remain framework-agnostic
- Command bus pattern used for write operations
- The target mapped by `make.ci` exits `0`

> Mapping flavor follows `persistence.mapper`: with `doctrine-orm` use `.orm.xml` mappings and `EntityManagerInterface`; with `doctrine-odm` use `.mongodb.xml` mappings and `DocumentManager`. The layering and DTO/processor patterns are identical either way.

---

## Quick Start: Complete CRUD in 10 Steps

`{Context}` below must be one of `architecture.bounded_contexts`; all source paths are relative to `architecture.source_root`.

### Step 1: Create Domain Entity

Create a pure PHP entity in `<source_root>/{Context}/Domain/Entity/{Entity}.php`

- NO Doctrine annotations/attributes
- NO Symfony imports
- NO API Platform attributes
- Pure business logic only

### Step 2: Create Doctrine XML Mapping

Create `config/doctrine/{Entity}.orm.xml` (or `.mongodb.xml` per `persistence.mapper`) with field mappings and indexes.

**See**: [database-migrations](../database-migrations/SKILL.md) for XML mapping patterns.

### Step 3: Create Input DTOs

Create three DTOs in `<source_root>/{Context}/Application/DTO/` — one per write verb, never shared:

- `{Entity}Create` — for POST (all required fields)
- `{Entity}Put` — for PUT (full replacement set)
- `{Entity}Patch` — for PATCH (every field optional/nullable)

### Step 4: Configure Validation

Create `config/validator/{Entity}.yaml` with validation rules for each DTO. Never skip this — unvalidated DTOs are a defect, not a shortcut.

### Step 5: Create API Platform Resource Configuration

Create `config/api_platform/resources/{entity}.yaml`. The namespace prefix must match the PSR-4 mapping of `architecture.source_root`:

```yaml
App\{Context}\Domain\Entity\{Entity}:
  shortName: { Entity }
  operations:
    ApiPlatform\Metadata\GetCollection: ~
    ApiPlatform\Metadata\Get: ~
    ApiPlatform\Metadata\Post:
      input: App\{Context}\Application\DTO\{Entity}Create
      processor: App\{Context}\Application\Processor\Create{Entity}Processor
    ApiPlatform\Metadata\Put:
      input: App\{Context}\Application\DTO\{Entity}Put
      processor: App\{Context}\Application\Processor\Update{Entity}Processor
    ApiPlatform\Metadata\Patch:
      input: App\{Context}\Application\DTO\{Entity}Patch
      processor: App\{Context}\Application\Processor\Patch{Entity}Processor
    ApiPlatform\Metadata\Delete: ~
```

### Step 6: Configure Serialization Groups

Create `config/serialization/{Entity}.yaml` to control which fields are exposed.

### Step 7: Create State Processors

Create processors in `<source_root>/{Context}/Application/Processor/`:

- `Create{Entity}Processor` — handles POST
- `Update{Entity}Processor` — handles PUT
- `Patch{Entity}Processor` — handles PATCH

Each processor does exactly four things — nothing more:

1. Receives DTO
2. Transforms to Command
3. Dispatches via Command Bus
4. Returns resulting Entity

### Step 8: Create Command and Handler

Create:

- Command in `Application/Command/{Action}{Entity}Command.php`
- Handler in `Application/CommandHandler/{Action}{Entity}CommandHandler.php`

The handler contains the business logic and calls the repository.

**See**: [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) for CQRS patterns.

### Step 9: Create Repository

Create:

- Interface in `Domain/Repository/{Entity}RepositoryInterface.php`
- Implementation in `Infrastructure/Repository/{Entity}Repository.php`
- Register the binding in `config/services.yaml`

**See**: [database-migrations](../database-migrations/SKILL.md) for repository patterns.

### Step 10: Configure Filters (Optional)

Declare filters (search, ordering, range, date, boolean) as services in `config/services.yaml` tagged `api_platform.filter`, then reference them from the resource YAML.

---

## Architecture Flow

```text
REST Request → API Platform
            ↓
        Processor (Application)
            ↓
        DTO → Transformer → Command
            ↓
        Command Bus
            ↓
        Handler (Application)
            ↓
        Entity (Domain) ← Repository (Infrastructure)
            ↓
        Database (persistence.engine)
```

---

## Constraints (Parameters)

### NEVER

- Add framework annotations/attributes to Domain entities
- Put business logic in Processors (use Handlers)
- Skip validation configuration
- Use PHP attributes for API Platform config (use YAML)
- Violate layer boundaries (check with the target mapped by `make.deptrac`)
- Skip DTO transformation (direct Entity manipulation)
- Edit `deptrac.yaml` or add suppression annotations to silence violations — fix the code
- Lower any `quality.*` threshold; floors are raise-only (shipped defaults: `quality.phpinsights.complexity` 94, `quality.infection_msi` 100)

### ALWAYS

- Keep Domain entities framework-agnostic
- Use YAML for all configuration (validation, serialization, resources)
- Dispatch Commands via Command Bus for write operations
- Create separate DTOs for Create, Put, and Patch
- Follow the IRI pattern for entity references
- Run the target mapped by `make.ci` before committing

---

## Format (Output)

### Expected API Endpoints

```text
GET    /api/{entities}           # List all
GET    /api/{entities}/{id}      # Get one
POST   /api/{entities}           # Create
PUT    /api/{entities}/{id}      # Full update
PATCH  /api/{entities}/{id}      # Partial update
DELETE /api/{entities}/{id}      # Delete
```

### Expected OpenAPI Spec

Regenerate the committed OpenAPI spec after any resource change. The export target is a repository convenience — check the Makefile for the exact name:

```bash # profile-example
make generate-openapi-spec
# Generates .github/openapi-spec/spec.yaml
```

### Expected CI Result

The target mapped by `make.ci` exits `0`. Many repositories also print a success banner:

```text # profile-example
✅ CI checks successfully passed!
```

---

## Verification Checklist

After implementation:

- [ ] Domain entity created (no framework imports)
- [ ] Doctrine XML mapping configured (extension matches `persistence.mapper`)
- [ ] Three DTOs created (Create, Put, Patch)
- [ ] Validation rules configured in YAML
- [ ] API Platform resource YAML created
- [ ] Serialization groups configured
- [ ] State Processors created for write operations
- [ ] Commands and Handlers implemented
- [ ] Repository interface and implementation created
- [ ] Filters configured (if needed)
- [ ] Resource directory registered in the API Platform package config (`mapping.paths`)
- [ ] All endpoints respond correctly (target mapped by `make.e2e`, or manual probe)
- [ ] Validation works (test invalid inputs)
- [ ] Target mapped by `make.deptrac` passes (no violations)
- [ ] Target mapped by `make.ci` passes (all checks green)
- [ ] OpenAPI spec regenerated successfully

---

## Related Skills

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - DDD patterns and CQRS
- [deptrac-fixer](../deptrac-fixer/SKILL.md) - Fix architectural violations
- [database-migrations](../database-migrations/SKILL.md) - Entity mapping and repository management
- [openapi-development](../openapi-development/SKILL.md) - OpenAPI documentation
- [testing-workflow](../testing-workflow/SKILL.md) - Write E2E tests for endpoints

---

## Quick Commands

Profile-mapped targets:

- Validate architecture: target mapped by `make.deptrac`
- Run E2E tests: target mapped by `make.e2e`
- Full CI check: target mapped by `make.ci`

Repositories typically also expose conveniences — verify in the Makefile before use:

```bash # profile-example
make cache-clear            # clear framework cache after config changes
make generate-openapi-spec  # export OpenAPI spec
```

> After editing any YAML config (resources, validation, serialization), clear the framework cache before re-testing — stale cache is the most common "my config change did nothing" pitfall.

---

## Template Syntax

Throughout this skill, placeholders follow these conventions:

| Placeholder  | Example            | Usage                                                        |
| ------------ | ------------------ | ------------------------------------------------------------ |
| `{Entity}`   | `Customer`         | PascalCase class name                                        |
| `{Context}`  | `Customer`         | Bounded context from `architecture.bounded_contexts`         |
| `{entity}`   | `customer`         | Lowercase for configs/filters                                |
| `{entities}` | `customers`        | Plural for collection names                                  |
| `{Action}`   | `Create`, `Update` | Command action verb                                          |
