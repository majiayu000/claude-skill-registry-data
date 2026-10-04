---
name: database-migrations
description: Create, manage, and apply database schema changes with Doctrine — versioned migrations when the profile's persistence.mapper is doctrine-orm, mapping-driven schema/index sync when it is doctrine-odm. Use when modifying entities or documents, adding fields, managing database schema changes, creating repositories, or troubleshooting schema/mapping issues.
---

# Database Migrations & Schema Management

## Profile keys consumed

- `persistence.mapper`
- `persistence.engine`
- `framework.name`
- `framework.api_platform`
- `architecture.source_root`
- `architecture.bounded_contexts`
- `architecture.shared_context`
- `make.start`
- `make.tests`
- `make.ci`
- `make.deptrac`
- `quality.infection_msi`

## Context (Input)

- New entity/document needs database persistence
- Existing entity requires schema changes (add/modify/remove fields)
- Repository implementation needed
- Schema or mapping validation fails
- Need to set up indexes for performance (for *which* indexes to add,
  see [query-performance-analysis](../query-performance-analysis/SKILL.md))

## Mapper branching (read this first)

This skill branches on `persistence.mapper`:

| `persistence.mapper` | Engines (`persistence.engine`) | Mapping file | Schema-change mechanism | Manager class |
| --- | --- | --- | --- | --- |
| `doctrine-orm` (Path A) | `mysql` \| `mariadb` \| `postgresql` | `config/doctrine/<Entity>.orm.xml` | versioned migrations (`doctrine:migrations:*`) | `EntityManagerInterface` |
| `doctrine-odm` (Path B) | `mongodb` | `config/doctrine/<Document>.mongodb.xml` | mapping-driven sync (`doctrine:mongodb:schema:*`) | `DocumentManager` |

Key difference: Path A keeps an append-only history of migration files;
Path B has **no migration files by default** — collections and indexes
are derived from the XML mappings and synced with a console command, and
only data backfills/renames need an explicit script or console command.

```yaml # profile-example
# Upstream reference service:
persistence:
  mapper: doctrine-odm
  engine: mongodb
```

When `framework.name` is `symfony` and the service runs in containers,
boot with the target mapped by `make.start` and run every `bin/console`
command inside the PHP container
(`docker compose exec <php-service> bin/console ...`).

## Task (Function)

Create entities/documents with XML mappings and repositories following
hexagonal architecture, then apply and verify the schema change via the
mapper-appropriate mechanism.

**Success criteria**: mappings validate, the test database recreates
without errors, all tests pass, the targets mapped by `make.deptrac` and
`make.ci` stay green.

---

## Core Principles

### Domain-Driven Design

With `<src>` = `architecture.source_root` and `<Context>` one of
`architecture.bounded_contexts`:

- **Entities/Documents**: Domain layer (`<src>/<Context>/Domain/Entity/`)
- **Repository interfaces**: Domain layer (`<src>/<Context>/Domain/Repository/`)
- **Repository implementations**: Infrastructure layer (`<src>/<Context>/Infrastructure/Repository/`)
- **XML mappings**: Infrastructure concern (`config/doctrine/`)

**See**: [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md).

### Doctrine mapping rules (both paths)

- Use **XML mappings** for all metadata — never annotations/attributes
  in Domain classes (keeps the Domain framework-agnostic)
- Define indexes in the XML mapping so code and schema stay in sync
- Use custom identifier types (see below) instead of auto-increment ids

### Custom identifier types

Registered in the shared context's Infrastructure layer
(`<src>/<architecture.shared_context>/Infrastructure/DoctrineType/`, or
the owning bounded context's own `Infrastructure/DoctrineType/` when
`architecture.shared_context` is `null`):

| Type | Usage | Purpose |
| --- | --- | --- |
| `ulid` | Primary keys, tokens | Sortable, time-ordered, URL-safe (26 chars) |
| `domain_uuid` | Domain identifiers | RFC 4122 UUID v4 |

Prefer `ulid` for primary keys (time-ordered → efficient indexing) and
`domain_uuid` where standard UUID compatibility matters. Generate in a
named constructor (`Ulid::generate()` / `Uuid::v4()`), never in the DB.

---

## Quick Start: Creating a New Entity/Document

### Step 1: Create the class (Domain layer — identical for both paths)

```php
// <src>/<Context>/Domain/Entity/Customer.php
namespace App\Customer\Domain\Entity;   // namespace mirrors <src>/<Context>

final class Customer
{
    public function __construct(
        private string $id,
        private string $name,
        private string $email,
        private \DateTimeImmutable $createdAt
    ) {}

    // Getters only — no setters (immutability); no framework imports
}
```

### Step 2: Create the XML mapping

**Path A (`doctrine-orm`)** — `config/doctrine/Customer.orm.xml`:

```xml
<entity name="App\Customer\Domain\Entity\Customer"
        repository-class="App\Customer\Infrastructure\Repository\CustomerRepository">
    <id name="id" type="domain_uuid"/>
    <field name="name" type="string" length="255"/>
    <field name="email" type="string" length="255" unique="true"/>
    <field name="createdAt" column="created_at" type="datetime_immutable"/>
    <indexes>
        <index name="idx_customer_email" columns="email"/>
    </indexes>
</entity>
```

**Path B (`doctrine-odm`)** — `config/doctrine/Customer.mongodb.xml`:

```xml
<document name="App\Customer\Domain\Entity\Customer" collection="customers">
    <id type="ulid" strategy="NONE"/>
    <field field-name="name" type="string"/>
    <field field-name="email" type="string"/>
    <field field-name="createdAt" name="created_at" type="date_immutable"/>
    <indexes>
        <index>
            <key name="email" order="asc"/>
            <option name="unique" value="true"/>
        </index>
    </indexes>
</document>
```

### Step 3: Configure the API resource (when `framework.api_platform` is a version)

```yaml
# config/api_platform/resources/customer.yaml
App\Customer\Domain\Entity\Customer:
  shortName: Customer
  operations:
    ApiPlatform\Metadata\GetCollection: ~
    ApiPlatform\Metadata\Get: ~
    ApiPlatform\Metadata\Post: ~
```

Ensure the resource directory is registered in `api_platform.yaml`.
**See**: [api-platform-crud](../api-platform-crud/SKILL.md). Skip this
step when `framework.api_platform` is `false`.

### Step 4: Apply and validate

**Path A (`doctrine-orm`)**:

```bash
bin/console cache:clear
bin/console doctrine:migrations:diff      # generate migration from mapping change
# REVIEW the generated migration before applying it
bin/console doctrine:migrations:migrate
bin/console doctrine:schema:validate      # expect: "Mapping files are correct."
```

**Path B (`doctrine-odm`)**:

```bash
bin/console cache:clear
bin/console doctrine:mongodb:mapping:info        # mappings load without error
bin/console doctrine:mongodb:schema:create       # new collections + indexes
bin/console doctrine:mongodb:schema:update      # sync indexes + validators on changes
```

---

## Modifying Existing Entities

1. Update the class (add/modify fields)
2. Update the XML mapping
3. `bin/console cache:clear`
4. Apply: Path A — `doctrine:migrations:diff` → review → `migrate`;
   Path B — `doctrine:mongodb:schema:update`
5. Validate (Path A `doctrine:schema:validate`; Path B `doctrine:mongodb:mapping:info`)
6. Path B only: field renames and backfills do not happen automatically —
   write an explicit console command/script for the data migration

---

## Creating Repositories

**Step 1 — interface (Domain)**:

```php
// Domain/Repository/CustomerRepositoryInterface.php
interface CustomerRepositoryInterface
{
    public function save(Customer $customer): void;
    public function findById(string $id): ?Customer;
}
```

**Step 2 — implementation (Infrastructure)**; the injected manager
branches on `persistence.mapper`:

```php
// Infrastructure/Repository/CustomerRepository.php
final class CustomerRepository implements CustomerRepositoryInterface
{
    public function __construct(
        // Path A: private readonly EntityManagerInterface $entityManager
        // Path B: private readonly DocumentManager $documentManager
        private readonly EntityManagerInterface $entityManager
    ) {}

    public function save(Customer $customer): void
    {
        $this->entityManager->persist($customer);
        $this->entityManager->flush();
    }
}
```

**Step 3 — register the alias in `services.yaml`**:

```yaml
App\Customer\Domain\Repository\CustomerRepositoryInterface:
  alias: App\Customer\Infrastructure\Repository\CustomerRepository
```

---

## Mapper-specific modeling features

### Path A: ORM (relational)

- Uniqueness: `unique="true"` on a field or `<unique-constraint>`
- `<indexes>` for frequent lookups; always index columns used in
  filters/sorting (email, token, foreign keys, timestamps)
- Associations: Doctrine relations (`one-to-one`, `one-to-many`,
  `many-to-many`); persist value objects as embeddables or simple fields
- Never put framework validation inside Domain classes

### Path B: ODM (MongoDB)

- **Compound indexes are used left-to-right**: `{status, type, createdAt}`
  serves filters on `status` and `status+type`, NOT on `type` alone
- Options: `unique`, `sparse` (index only documents having the field),
  `expireAfterSeconds` (TTL auto-deletion), `type=text` (text search)
- Keep indexes to roughly 3–5 per collection — each one slows writes
- **Value objects → embedded documents** (`<embedded-document>` mapping +
  `embed-one`/`embed-many` in the parent), loaded with the parent —
  keep them small
- **Entity references → IRI strings** (e.g. `"/api/customer_types/<id>"`)
  stored as plain string fields, NOT `reference-one` DBRefs: API Platform
  expects IRIs, and DBRefs add lazy-loading complexity and overhead
- Multi-document writes needing atomicity: `$dm->transactional(fn ($dm) => ...)`
  (requires a replica set)

---

## Constraints (Parameters)

### NEVER

- Use Doctrine annotations/attributes in Domain classes
- Modify a migration after it has been applied anywhere (Path A)
- Leave empty migration files in the codebase — delete a generated
  migration whose `up()`/`down()` bodies are empty immediately (Path A)
- Skip mapping validation
- Commit without testing the schema change
- Skip recreating the test database before integration tests
- Edit `deptrac.yaml` or add suppression annotations to silence layer
  violations — fix the code
  (see [deptrac-fixer](../deptrac-fixer/SKILL.md))

### ALWAYS

- Create XML mappings for all metadata; keep Domain framework-agnostic
- Define indexes for frequently queried fields in the mapping
- Test migrations/schema sync on the dev database before committing
- Use Faker for unique test data (emails, names, etc.)
- Register resource directories in `api_platform.yaml` (when
  `framework.api_platform` is enabled)

---

## Testing with the database

Recreate the test database before integration/E2E tests:

```bash
# Path A (doctrine-orm)
bin/console --env=test doctrine:database:drop --force --if-exists
bin/console --env=test doctrine:database:create
bin/console --env=test doctrine:migrations:migrate -n

# Path B (doctrine-odm)
bin/console --env=test doctrine:mongodb:schema:drop
bin/console --env=test doctrine:mongodb:schema:create
```

Integration test pattern (run via the target mapped by `make.tests`):

```php
final class CustomerRepositoryTest extends IntegrationTestCase
{
    private CustomerRepositoryInterface $repository;

    protected function setUp(): void
    {
        parent::setUp();
        $this->repository = $this->getContainer()->get(CustomerRepositoryInterface::class);
    }

    public function testSaveAndRetrieveCustomer(): void
    {
        $customer = new Customer(/* unique test data with Faker */);
        $this->repository->save($customer);

        $this->assertNotNull($this->repository->findById($customer->getId()));
    }
}
```

New repository tests must keep the mutation score at or above
`quality.infection_msi` (canonical default 100 — raise-only: a profile
may tighten the floor, never lower it).

---

## Migration best practices (Path A) / schema-sync practices (Path B)

1. **Review every generated migration** — `doctrine:migrations:diff`
   output can include unrelated drift; delete empty ones
2. **Test before committing**: apply on dev, validate, run all tests,
   test rollback (`doctrine:migrations:migrate prev`) where applicable
3. **Production safety**: back up first, apply, verify the application
   works, keep the backup for rollback
4. **Path B**: index changes are online by default (MongoDB 4.2+), but
   destructive mapping changes (field renames, drops) silently orphan
   data — pair them with an explicit data-migration command

---

## Verification Checklist

- [ ] Class in Domain layer (no framework imports)
- [ ] XML mapping in `config/doctrine/` (`.orm.xml` / `.mongodb.xml` per `persistence.mapper`)
- [ ] API resource configured (when `framework.api_platform` is enabled)
- [ ] Repository interface in Domain, implementation in Infrastructure, alias in `services.yaml`
- [ ] Path A: migration reviewed + applied; `doctrine:schema:validate` passes
- [ ] Path B: `doctrine:mongodb:schema:update` applied; mappings load
- [ ] Test database recreates cleanly; all integration tests pass
- [ ] Target mapped by `make.deptrac` passes (no violations)
- [ ] Target mapped by `make.ci` passes

---

## Troubleshooting

**Database connection errors**:

```bash
docker compose ps <db-service>
docker compose logs <db-service>
```

**Schema sync issues** — re-validate and check state:

```bash
bin/console doctrine:schema:validate          # Path A
bin/console doctrine:migrations:status        # Path A
bin/console doctrine:mongodb:mapping:info     # Path B
```

**Migration conflicts (Path A)** — check `doctrine:migrations:status`;
roll back with `doctrine:migrations:migrate prev`, fix, regenerate.

**Index conflict (Path B)** — an existing index with the same name but
different options blocks `schema:update`; drop the old index in `mongosh`
(`db.<collection>.dropIndex("<name>")`), then re-run the sync.

---

## Related Skills

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) — DDD patterns and repository interfaces
- [api-platform-crud](../api-platform-crud/SKILL.md) — configuring API resources
- [deptrac-fixer](../deptrac-fixer/SKILL.md) — fixing architectural violations
- [query-performance-analysis](../query-performance-analysis/SKILL.md) — WHAT indexes to add (this skill covers HOW to create them)
- [testing-workflow](../testing-workflow/SKILL.md) — running the test suites
