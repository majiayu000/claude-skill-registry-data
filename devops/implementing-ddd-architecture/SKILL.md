---
name: implementing-ddd-architecture
description: Design and implement DDD patterns (entities, value objects, aggregates, CQRS) with strict hexagonal layer separation. Use when creating new domain objects, implementing bounded contexts, designing repository interfaces, or deciding proper layer placement for new code. For fixing existing Deptrac violations, use the deptrac-fixer skill instead.
---

# Implementing DDD Architecture

## Profile keys consumed

- `architecture.source_root`
- `architecture.bounded_contexts`
- `architecture.shared_context`
- `persistence.mapper`
- `persistence.engine`
- `framework.api_platform`
- `framework.graphql`
- `make.deptrac`
- `make.tests`
- `make.ci`
- `quality.deptrac_violations`

## Context (Input)

- Creating new entities, value objects, or aggregates
- Implementing bounded contexts or modules
- Designing repository interfaces and implementations
- Learning proper layer separation (Domain/Application/Infrastructure)
- Need to understand CQRS pattern (Commands, Handlers, Events)
- Code review for architectural compliance

## Task (Function)

Design and implement rich domain models following DDD, hexagonal architecture, and CQRS patterns.

**Success Criteria**:

- Domain entities remain framework-agnostic (no framework imports)
- Business logic in Domain layer, not in Application handlers
- The target mapped by `make.deptrac` shows zero violations —
  `quality.deptrac_violations` is a fixed ceiling shipped at `0` and may
  never be raised. (Score thresholds elsewhere are raise-only floors:
  canonical defaults are phpinsights complexity `94` and infection MSI
  `100`; a profile may tighten them, never relax them.)
- Repository interfaces in Domain, implementations in Infrastructure

---

## Core Principle

### Rich Domain Models, Not Anemic

Business logic belongs in the Domain layer. Application layer orchestrates, Domain executes.

---

## Layer Dependency Rules

```text
Domain ─────────────────> (NO dependencies - pure PHP)
           │
           │
Application ──────────> Domain + Infrastructure
           │
           │
Infrastructure ───────> Domain + Application
```

**Allowed Dependencies**:

| Layer | Can Import |
| --- | --- |
| **Domain** | ❌ Nothing (pure PHP, SPL, domain-specific libraries only) |
| **Application** | ✅ Domain, Infrastructure, framework components (API Platform when `framework.api_platform` is set; GraphQL when `framework.graphql` is true) |
| **Infrastructure** | ✅ Domain, Application, framework, the persistence mapper |

> Persistence constructs branch on the profile. `persistence.mapper`
> selects the API: `doctrine-orm` → `EntityManagerInterface` and
> `.orm.xml` mappings; `doctrine-odm` → `DocumentManager` and
> `.mongodb.xml` mappings. `persistence.engine` names the backing store
> (`mysql` | `mariadb` | `postgresql` | `mongodb`). Use the variant your
> profile declares — never the other one.

**See**: [DIRECTORY-STRUCTURE.md](../code-organization/DIRECTORY-STRUCTURE.md)
(in the code-organization skill) for the complete file placement guide.

---

## Critical Rules

### 1. Domain Layer Purity

❌ **FORBIDDEN in Domain**:

- Framework components (`use Symfony\...`)
- Doctrine annotations/attributes (ORM or ODM)
- API Platform attributes
- Any framework-specific code

✅ **ALLOWED in Domain**:

- Pure PHP
- SPL (Standard PHP Library)
- Domain-specific value objects
- Domain interfaces

### 2. Rich Domain Models

❌ **BAD (Anemic)**:

```php
class Customer {
    public function setName(string $name): void {
        $this->name = $name;  // No validation!
    }
}
```

✅ **GOOD (Rich)**:

```php
class Customer {
    public function changeName(CustomerName $name): void {
        // Business rules enforced
        $this->record(new CustomerNameChanged($this->id, $name));
        $this->name = $name;
    }
}
```

### 3. Validation Pattern

❌ **BAD**: Validation in Domain with framework constraints

```php
use Symfony\Component\Validator\Constraints as Assert;

class Customer {
    #[Assert\NotBlank]  // ❌ Framework in Domain!
    private string $name;
}
```

✅ **GOOD**: Validation in YAML config (Preferred)

```yaml
# config/validator/Customer.yaml
App\Customer\Application\DTO\CustomerCreate:
  properties:
    name:
      - NotBlank: ~
      - Length:
          min: 2
          max: 100
```

**Framework validators should always be used when possible.** They provide:

- Centralized configuration
- Easy maintenance
- Standard error messages
- Built-in constraints (NotBlank, Email, Length, etc.)
- Custom validators for business rules

**Value Objects** should only be used when:

- Framework validators cannot express the business rule
- Complex domain logic requires encapsulation
- The validation is part of domain invariants

**See**: [REFERENCE.md](REFERENCE.md) for complete validation patterns.

---

## CQRS Pattern Quick Start

Context directories come from `architecture.bounded_contexts`; `{Context}`
below stands for one of them under `architecture.source_root`.

### Commands (Write Operations)

```php
// <architecture.source_root>/{Context}/Application/Command/{Action}{Entity}Command.php
final readonly class CreateCustomerCommand implements CommandInterface
{
    public function __construct(
        public string $id,
        public string $name,
        public string $email
    ) {}
}
```

### Command Handlers

```php
// <architecture.source_root>/{Context}/Application/CommandHandler/{Action}{Entity}CommandHandler.php
final readonly class CreateCustomerCommandHandler implements CommandHandlerInterface
{
    public function __invoke(CreateCustomerCommand $command): Customer
    {
        // Minimal orchestration only
        $customer = Customer::create(
            Ulid::fromString($command->id),
            new CustomerName($command->name),
            new Email($command->email)
        );

        $this->repository->save($customer);
        $this->eventBus->publish(...$customer->pullDomainEvents());

        return $customer;
    }
}
```

**See**: [REFERENCE.md](REFERENCE.md) for complete CQRS patterns.

---

## Repository Pattern

### Interface (Domain Layer)

```php
// <architecture.source_root>/{Context}/Domain/Repository/{Entity}RepositoryInterface.php
interface CustomerRepositoryInterface
{
    public function save(Customer $customer): void;
    public function findById(string $id): ?Customer;
}
```

### Implementation (Infrastructure Layer)

When `persistence.mapper` is `doctrine-orm`:

```php
// <architecture.source_root>/{Context}/Infrastructure/Repository/{Entity}Repository.php
final class CustomerRepository implements CustomerRepositoryInterface
{
    public function __construct(
        private readonly EntityManagerInterface $entityManager
    ) {}

    public function save(Customer $customer): void
    {
        $this->entityManager->persist($customer);
        $this->entityManager->flush();
    }
}
```

When `persistence.mapper` is `doctrine-odm`: same shape, but inject
`Doctrine\ODM\MongoDB\DocumentManager` and call
`$this->documentManager->persist()/flush()`.

**Register in `config/services.yaml`**:

```yaml
App\Customer\Domain\Repository\CustomerRepositoryInterface:
  alias: App\Customer\Infrastructure\Repository\CustomerRepository
```

---

## Domain Events Pattern

### Recording Events in Aggregates

```php
class Customer extends AggregateRoot  // Provides event recording
{
    public function changeName(CustomerName $name): void
    {
        $this->name = $name;
        $this->record(new CustomerNameChanged($this->id, $name));
    }
}
```

### Event Subscribers

```php
// <architecture.source_root>/{Context}/Application/EventSubscriber/{Event}Subscriber.php
final readonly class CustomerNameChangedSubscriber implements DomainEventSubscriberInterface
{
    public function __invoke(CustomerNameChanged $event): void
    {
        // React to event (e.g., send notification)
    }
}
```

**See**: [REFERENCE.md](REFERENCE.md) for complete event-driven patterns.

---

## Quick Start Workflows

### Creating a New Entity

1. **Create Entity** in `Domain/Entity/`
2. **Create Value Objects** in `Domain/ValueObject/`
3. **Create Repository Interface** in `Domain/Repository/`
4. **Create Repository Implementation** in `Infrastructure/Repository/`
5. **Create Commands** in `Application/Command/`
6. **Create Handlers** in `Application/CommandHandler/`
7. **Verify**: the target mapped by `make.deptrac` shows zero violations
   (if the mapping is `null`, the capability is absent — note it and
   verify the layer rules by review instead)

**See**: [REFERENCE.md](REFERENCE.md) for the full ten-step workflow with code.

### Fixing Deptrac Violations

**If** the target mapped by `make.deptrac` shows violations:

**Use**: [deptrac-fixer](../deptrac-fixer/SKILL.md) skill for step-by-step fix patterns.

---

## Constraints (Parameters)

### NEVER

- Add framework imports to Domain layer
- Put business logic in Application handlers
- Create anemic domain models (getters/setters only)
- Modify `deptrac.yaml` to allow violations
- Skip validation (either in Value Objects or YAML config)
- Use public setters in entities
- Use bare `array`, `list`, or `iterable` for domain object collections —
  create and pass typed collection classes instead (e.g.
  `CustomerCollection`, `DomainEventCollection`). Where the repository
  enforces this via Psalm custom rules, the rule applies to everything
  under `architecture.source_root`.
- Use `json_encode`/`json_decode` in production source — use the
  framework serializer (`SerializerInterface`), commonly enforced by
  Psalm under `architecture.source_root`
- Use constructor defaults that instantiate collaborators — inject dependencies instead
- Use direct `new` on a value object that ships a static factory method —
  call the factory (e.g. `{ValueObject}::fromString()`)
- Use direct `new` on normalizers/serializers outside Doctrine custom
  types (Doctrine types are exempt since they lack DI support)
- Use direct `new` for domain events and collections in production
  source code — use dedicated Factory classes instead

### ALWAYS

- Keep Domain layer pure (no framework dependencies)
- Put business logic in Domain entities/aggregates
- Use Value Objects for validation and invariants
- Provide static factory methods on value objects when production code needs a stable construction path
- Use dedicated Factory classes for domain events and collection assembly in production code
- Create typed collection classes (implementing `IteratorAggregate`,
  `Countable`) when a module exposes repeated domain object groups
- Use the framework `SerializerInterface` for serialization in infrastructure repositories
- Create repository interfaces in Domain layer
- Implement repositories in Infrastructure layer
- Use Command Bus for write operations
- Record Domain Events for state changes
- Verify with the target mapped by `make.deptrac` after changes

---

## Format (Output)

### Expected Directory Structure

One context directory per `architecture.bounded_contexts` entry; a shared
kernel lives at `<architecture.source_root>/<architecture.shared_context>/`
when the profile declares one (`null` = none).

```text
<architecture.source_root>/{Context}/
├── Domain/
│   ├── Entity/
│   │   └── {Entity}.php          # Pure PHP, no attributes
│   ├── ValueObject/
│   │   └── {ValueObject}.php     # Validation logic here
│   ├── Repository/
│   │   └── {Entity}RepositoryInterface.php
│   ├── Event/
│   │   └── {Event}.php
│   └── Exception/
│       └── {Exception}.php
├── Application/
│   ├── Command/
│   │   └── {Action}{Entity}Command.php
│   ├── CommandHandler/
│   │   └── {Action}{Entity}CommandHandler.php
│   └── EventSubscriber/
│       └── {Event}Subscriber.php
└── Infrastructure/
    └── Repository/
        └── {Entity}Repository.php
```

### Expected Deptrac Output

```text
✅ No violations found
```

---

## Verification Checklist

After implementing DDD patterns:

- [ ] Domain entities have no framework imports
- [ ] Business logic in Domain layer, not Application
- [ ] Value Objects used for validation and invariants
- [ ] Repository interfaces in Domain layer
- [ ] Repository implementations in Infrastructure layer
- [ ] Commands implement `CommandInterface`
- [ ] Handlers implement `CommandHandlerInterface`
- [ ] Domain Events recorded in aggregates
- [ ] Event Subscribers implement `DomainEventSubscriberInterface`
- [ ] Target mapped by `make.deptrac` shows zero violations
      (`quality.deptrac_violations` = 0, fixed ceiling)
- [ ] All tests pass (target mapped by `make.tests`)
- [ ] Target mapped by `make.ci` passes

---

## Related Skills

- [deptrac-fixer](../deptrac-fixer/SKILL.md) - Fix architectural violations
- [api-platform-crud](../api-platform-crud/SKILL.md) - YAML-based API Platform with DDD
- [database-migrations](../database-migrations/SKILL.md) - XML-based Doctrine mappings
- [complexity-management](../complexity-management/SKILL.md) - Keep domain logic maintainable

---

## Reference Documentation

For detailed patterns, workflows, and examples:

- **[REFERENCE.md](REFERENCE.md)** - Complete DDD workflows and patterns:
  layer responsibilities, the full create-an-entity workflow, Deptrac
  violation fixes, Doctrine configuration per `persistence.mapper`,
  event-driven details, factory patterns, and the pragmatic
  value-object decision guide
- **[DIRECTORY-STRUCTURE.md](../code-organization/DIRECTORY-STRUCTURE.md)**
  (code-organization skill) - File placement guide (CodelyTV style)

---

## Anti-Patterns to Avoid

### ❌ Business Logic in Handlers

```php
// ❌ BAD: Logic in handler
class CreateCustomerHandler {
    public function __invoke($command) {
        if (strlen($command->name) < 2) {  // ❌ Validation in handler!
            throw new Exception();
        }
        // ...
    }
}
```

### ❌ Framework Dependencies in Domain

```php
// ❌ BAD: framework constraint in Domain
use Symfony\Component\Validator\Constraints as Assert;

class Customer {
    #[Assert\NotBlank]  // ❌ Framework coupling!
    private string $name;
}
```

### ❌ Anemic Domain Models

```php
// ❌ BAD: Just getters/setters
class Customer {
    public function setName(string $name): void {
        $this->name = $name;  // No business rules!
    }
}
```

### ✅ GOOD Patterns

- Value Objects enforce invariants
- Domain methods express business operations
- Handlers orchestrate, Domain executes
- Configuration externalized to YAML/XML

---

## CodelyTV Architecture Pattern

This skill follows CodelyTV's hexagonal architecture patterns:

- **Directory structure**: Bounded Context → Layer → Component Type
- **Naming conventions**: Explicit suffixes (Command, Handler, Repository, etc.)
- **Layer isolation**: Deptrac enforces boundaries
- **CQRS**: Commands for writes, Queries for reads
- **Event-driven**: Domain Events for decoupling

**See**: [DIRECTORY-STRUCTURE.md](../code-organization/DIRECTORY-STRUCTURE.md)
(in the code-organization skill) for the complete hierarchy.
