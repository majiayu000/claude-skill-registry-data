---
name: code-organization
description: Enforce code organization principles - the "Directory X contains ONLY class type X" law, DDD naming patterns, type safety, SOLID, factory usage, and hardcoded config extraction to .env. Use when placing new classes, reviewing code structure, refactoring (moving, renaming, splitting classes), fixing CI failures that stem from structural or naming issues, or extracting hardcoded configuration values.
---

# Code Organization Skill

## Profile keys consumed

- `architecture.source_root`
- `architecture.bounded_contexts`
- `architecture.shared_context`
- `framework.name`
- `framework.api_platform`
- `framework.graphql`
- `persistence.mapper`
- `make.ci`
- `make.psalm`
- `make.deptrac`
- `make.phpinsights`
- `make.tests`
- `quality.phpinsights.architecture`
- `quality.phpinsights.style`
- `quality.phpinsights.complexity`
- `quality.deptrac_violations`
- `quality.psalm_errors`

## Core Principle

> **Directory X contains ONLY class type X**

This is the fundamental, stack-generic law of code organization. It holds
in every bounded context under `architecture.source_root`, regardless of
framework or persistence engine.

## Context (Input)

- Creating new classes and determining the correct directory
- Moving classes to proper locations
- Reviewing code for organizational compliance
- Fixing organizational issues from code reviews
- Ensuring class names match their responsibilities
- **Refactoring code structure** (moving, renaming, splitting classes)
- **Fixing CI failures** that stem from structural/naming issues
- **Extracting hardcoded config values** (TTLs, timeouts, limits) to `.env`

## Task (Function)

Enforce strict code organization principles: proper directory structure,
DDD naming conventions, specific variable names, type safety, SOLID
principles, and PHP best practices.

Source paths follow the profile: classes live under
`<architecture.source_root>/<Context>/` where `<Context>` is one of
`architecture.bounded_contexts` (or `architecture.shared_context` when
set). See [DIRECTORY-STRUCTURE.md](DIRECTORY-STRUCTURE.md) for the full
layer-by-layer placement reference.

## Directory Type Classification

Classes MUST be in directories matching their type:

| Directory          | Contains ONLY                   | Example                            |
| ------------------ | ------------------------------- | ---------------------------------- |
| `Converter/`       | Type converters                 | `UlidTypeConverter`                |
| `Transformer/`     | Data transformers (DB/serial)   | `CustomerToArrayTransformer`       |
| `Validator/`       | Validation logic                | `UlidValidator`                    |
| `Builder/`         | Object builders                 | `QueryBuilder`                     |
| `Fixer/`           | Data fixers/modifiers           | `DataFixer`                        |
| `Factory/`         | Object factories                | `CustomerFactory`                  |
| `Resolver/`        | Value resolvers                 | `CustomerUpdateScalarResolver`     |
| `Serializer/`      | Serializers/normalizers         | `CustomerNormalizer`               |
| `Formatter/`       | Data formatters                 | `CustomerNameFormatter`            |
| `Mapper/`          | Data mappers                    | `PathsMapper`                      |
| `Provider/`        | Data/service providers          | `TimestampProvider`                |
| `Processor/`       | API state processors            | `CreateCustomerProcessor`          |
| `EventListener/`   | Framework event listeners       | `QueryParameterValidationListener` |
| `EventSubscriber/` | Event subscribers               | `SendEmailOnCustomerCreated`       |

`Processor/` applies when `framework.api_platform` is set (not `false`);
GraphQL-specific directories (`MutationInput/`, GraphQL `Resolver/`)
apply when `framework.graphql` is true.

### Directory Creation Guardrails

- **NEVER create new directories autonomously** — every new class-type
  directory MUST follow a well-known software engineering pattern
  (Factory, Builder, Processor, Validator, Provider, Resolver, etc.) AND
  be explicitly requested/approved by the user. When in doubt, use an
  existing directory.
- Do not invent ad-hoc class-type directories or suffixes. The following
  are **explicitly forbidden**:
  - `Applier/`, `Attacher/`, `Enricher/` — not well-known patterns
  - `Augmenter/` — not a well-known pattern
  - `Helper/`, `Util/`, `Manager/` — vague catch-all anti-patterns
  - `Service/` — leads to anemic domain models; use specific pattern
    names instead (Provider, Factory, Resolver, etc.)
- Any proposed new directory MUST be a **well-known software engineering
  pattern** (e.g. Factory, Builder, Strategy, Observer, Adapter,
  Decorator, Proxy, Iterator, Mediator, etc.) — not an invented
  verb-noun.
- Use existing DDD/CQRS directory types and naming patterns from this
  skill.
- Follow DDD and CQRS strictly — all class organization must align with
  established DDD layers and CQRS patterns.

## DDD Naming Patterns

### By Layer and Type

| Layer              | Class Type         | Naming Pattern                       | Example                           |
| ------------------ | ------------------ | ------------------------------------ | --------------------------------- |
| **Domain**         | Entity             | `{EntityName}.php`                   | `Customer.php`                    |
|                    | Value Object       | `{ConceptName}.php`                  | `Email.php`, `Money.php`          |
|                    | Domain Event       | `{Entity}{PastTenseAction}.php`      | `CustomerCreated.php`             |
|                    | Repository Iface   | `{Entity}RepositoryInterface.php`    | `CustomerRepositoryInterface.php` |
|                    | Exception          | `{SpecificError}Exception.php`       | `InvalidEmailException.php`       |
| **Application**    | Command            | `{Action}{Entity}Command.php`        | `CreateCustomerCommand.php`       |
|                    | Command Handler    | `{Action}{Entity}Handler.php`        | `CreateCustomerHandler.php`       |
|                    | Event Subscriber   | `{Action}On{Event}.php`              | `SendEmailOnCustomerCreated.php`  |
|                    | DTO                | `{Entity}{Type}.php`                 | `CustomerInput.php`               |
|                    | Processor          | `{Action}{Entity}Processor.php`      | `CreateCustomerProcessor.php`     |
|                    | Transformer        | `{From}To{To}Transformer.php`        | `CustomerToArrayTransformer.php`  |
| **Infrastructure** | Repository         | `{Technology}{Entity}Repository.php` | `DoctrineCustomerRepository.php`  |
|                    | Doctrine Type      | `{ConceptName}Type.php`              | `UlidType.php`                    |
|                    | Bus Implementation | `{Framework}{Type}Bus.php`           | `SymfonyCommandBus.php`           |

### Directory Structure by Layer

```text
<architecture.source_root>/<Context>/
├── Application/
│   ├── Command/          ← Commands
│   ├── CommandHandler/   ← Command Handlers
│   ├── EventSubscriber/  ← Event Subscribers
│   ├── DTO/              ← Data Transfer Objects
│   ├── Processor/        ← API state processors (framework.api_platform)
│   ├── Transformer/      ← Data Transformers
│   ├── Validator/        ← Validators
│   ├── Converter/        ← Type Converters
│   ├── Resolver/         ← Value Resolvers
│   ├── Factory/          ← Factories
│   ├── Builder/          ← Builders
│   ├── Formatter/        ← Formatters
│   └── MutationInput/    ← GraphQL Mutation Inputs (framework.graphql)
├── Domain/
│   ├── Entity/           ← Entities & Aggregates
│   ├── ValueObject/      ← Value Objects
│   ├── Event/            ← Domain Events
│   ├── Repository/       ← Repository Interfaces
│   └── Exception/        ← Domain Exceptions
└── Infrastructure/
    ├── Repository/       ← Repository Implementations
    ├── DoctrineType/     ← Custom Doctrine Types
    ├── EventSubscriber/  ← Infrastructure Event Subscribers
    ├── EventListener/    ← Framework Event Listeners
    └── Bus/              ← Message Bus Implementations
```

`<Context>` is each entry of `architecture.bounded_contexts`; the shared
kernel (when `architecture.shared_context` is set) follows the same
layout.

## Verification Checklist

When creating or reviewing a class, verify:

1. ✅ **Class Type Matches Directory** (Directory X contains ONLY class type X)
   - Example: `UlidValidator` in `Validator/`, NOT `Transformer/`
2. ✅ **Class Name Follows DDD Pattern** for its type
3. ✅ **Namespace Matches Directory Structure** exactly
4. ✅ **Class Name Reflects Actual Functionality**
5. ✅ **Correct Layer** (Domain/Application/Infrastructure)
6. ✅ **Domain Layer Has NO Framework Imports** (`framework.name`
   components, Doctrine, API Platform)
7. ✅ **Variable Names Are Specific** (not vague)
   - ✅ `$typeConverter`, `$scalarResolver` (specific)
   - ❌ `$converter`, `$resolver` (too vague)
8. ✅ **Parameter Names Match Actual Types**
   - ✅ `mixed $value` when accepts any type
   - ❌ `string $binary` when accepts mixed
9. ✅ **No "Helper" or "Util" Classes** (extract specific responsibilities)
10. ✅ **No ad-hoc class-type suffixes/directories** (`Applier`,
    `Attacher`, `Enricher`, `Augmenter`, `Helper`, `Util`, `Manager`,
    `Service`)
11. ✅ **New directories are explicit and standard**, not agent-invented —
    must be explicitly approved by the user

## PHP Best Practices

### Required Patterns

- ✅ **Constructor property promotion**
- ✅ **Inject ALL dependencies** (no default instantiation)
- ✅ **Use `readonly`** when appropriate
- ✅ **Use `final`** for classes that shouldn't be extended
- ✅ **No static methods** (except named constructors like `create()`, `from()`)

### Anti-Patterns (Forbidden)

Where the repository ships static-analysis architecture guards (Psalm
plugins, `forbiddenFunctions`), they enforce these rules under
`architecture.source_root`; treat the rules as binding even when no
automated guard exists.

- ❌ **Helper/Util/Service/Manager classes** - Extract specific
  responsibilities; `Service` leads to anemic domain models
- ❌ **Non-standard pattern directories** - No `Applier/`, `Attacher/`,
  `Enricher/`, `Augmenter/` — use well-known patterns (Processor,
  Transformer, Validator, Factory, etc.)
- ❌ **Default instantiation in constructors** - Inject dependencies
- ❌ **Vague variable names** - Be specific
- ❌ **Namespace mismatches** - Must match directory structure
- ❌ **Ad-hoc directory/class type inventions** - Use established
  patterns only; NEVER create new directories without explicit user
  approval
- ❌ **Constructor defaults that instantiate collaborators** - Inject
  dependencies instead of using `new` in `__construct(...)` defaults
- ❌ **Direct `new` of value objects that expose named constructors** -
  Use the named constructor (`{ValueObject}::fromString()`) in
  production code
- ✅ **Direct `new` of normalizers inside custom Doctrine types** -
  Allowed because Doctrine types cannot use constructor DI
- ❌ **Direct instantiation of guarded collections/events in production
  code** - Use dedicated factory classes (`{Object}CollectionFactory`,
  `{Event}Factory`)
- ❌ **Plain `json_encode`/`json_decode`** - Use the framework serializer
  (`SerializerInterface` for `framework.name: symfony`); tests are
  excluded from this rule
- ❌ **Untyped `array` in method signatures** - Always specify the
  array's content type via docblock (`list<string>`,
  `array<string, int>`) or use a typed collection class (custom Doctrine
  type and collection-internal storage excluded)
- ❌ **Bare `array`, `list`, or `iterable` collections of domain
  objects** - Every domain object type that has a dedicated collection
  class must use it, repo-wide under `architecture.source_root`.
  Internal storage inside collection classes may still use `array`.

```text # profile-example
Upstream reference service: Psalm architecture guards enforce these
domain-type -> collection mappings repo-wide in src/ and require factory
classes (OAuthProviderCollectionFactory, SignInEventFactory,
SessionRevocationEventFactory, TwoFactorEventFactory,
RefreshTokenEventFactory) plus OAuthProvider::fromString():
  OAuthProvider/OAuthProviderInterface -> OAuthProviderCollection
  User/UserInterface                   -> UserCollection
  RecoveryCode                         -> RecoveryCodeCollection
  AuthSession                          -> AuthSessionCollection
  PasswordResetTokenInterface          -> PasswordResetTokenCollection
  DomainEvent                          -> DomainEventCollection
```

## Factory Pattern (Maintainability & Flexibility)

> **Avoid hardcoded `new ClassName()` in production source code — use
> factory methods or Factory classes**

### Factory Methods on Value Objects

Value objects SHOULD provide static factory methods as named constructors:

```php
// ❌ BAD: Direct instantiation in production code
$status = new CustomerStatus($value);

// ✅ GOOD: Factory method
$status = CustomerStatus::fromString($value);
```

Factory methods (`fromString()`, `fromArray()`, `create()`) are the
**preferred** way to instantiate value objects outside of their own
class. The constructor remains public for use within named constructors
and tests.

Collections and domain events should follow a different rule in
production code: use dedicated Factory classes instead of adding static
convenience constructors just to avoid `new`.

### When Factory Classes Are REQUIRED (Production Code)

1. Objects with injected dependencies (timestamp providers, config, etc.)
2. Objects requiring complex construction logic
3. Objects needing different implementations per environment
4. Objects created from external input (DTOs, metrics, etc.)

### When Direct `new` Is ACCEPTABLE

- Inside factory methods and Factory classes (that's their purpose)
- In test code (simplicity over abstraction)
- For framework-required patterns (e.g., `throw new InvalidArgumentException()`)
- Inside the value object's own named constructors

### Factory Benefits

- ✅ Centralized object creation logic
- ✅ Easy to inject different implementations
- ✅ Configuration changes don't affect consumers
- ✅ Single place for validation/transformation
- ✅ Enables dependency injection for complex objects

### Example: Bad vs Good

```php
// ❌ BAD: Direct instantiation with configuration
public function emit(BusinessMetric $metric): void
{
    $timestamp = (int)(microtime(true) * 1000);
    $payload = new MetricsPayload(
        new MetricsMetadata($timestamp, new MetricConfig(...)),
        new DimensionValueCollection(...),
        new MetricValueCollection(...)
    );
    $this->logger->info($payload);
}

// ✅ GOOD: Factory handles complexity
public function emit(BusinessMetric $metric): void
{
    $payload = $this->payloadFactory->createFromMetric($metric);
    $this->logger->info($payload);
}
```

### Factory Naming Convention

- `{ObjectName}Factory` - creates `{ObjectName}` instances
- Location: Same namespace as the object being created
- Example: `MetricsPayloadFactory` creates `MetricsPayload`

## Type Safety: Classes Over Arrays

> **Arrays are NOT allowed for collections that already have a dedicated
> collection type. Use the collection class instead.**

Arrays lack type safety and self-documentation. Use concrete classes
instead. CI guards (where present) block bare collections of guarded
domain types in production code, including iterable-based variants.

### Array vs Class Comparison

| Pattern       | Bad (Array)                               | Good (Class)                                |
| ------------- | ----------------------------------------- | ------------------------------------------- |
| Configuration | `['endpoint' => 'X', 'operation' => 'Y']` | `new EndpointOperationDimensions('X', 'Y')` |
| Return data   | `return ['name' => $n, 'value' => $v]`    | `return new MetricData($n, $v)`             |
| Method params | `function emit(array $metrics)`           | `function emit(MetricCollection $metrics)`  |
| Events data   | `['type' => 'created', 'id' => $id]`      | `new CustomerCreatedEvent($id)`             |
| Registry      | `private array $providers`                | `private ProviderCollection $providers`     |

### Benefits of Typed Classes

- ✅ IDE autocompletion and refactoring support
- ✅ Static analysis catches type errors
- ✅ Self-documenting code
- ✅ Encapsulation (validation in constructor)
- ✅ Single Responsibility
- ✅ Open/Closed principle (extend via new classes)

### Collection Pattern

```php
// ❌ BAD: Array of arrays
$metrics = [
    ['name' => 'OrdersPlaced', 'value' => 1],
    ['name' => 'OrderValue', 'value' => 99.99],
];

// ✅ GOOD: Typed collection of objects
$metrics = new MetricCollection(
    new OrdersPlacedMetric(value: 1),
    new OrderValueMetric(value: 99.99)
);
```

### When Arrays ARE Acceptable

- Simple key-value maps for serialization output (`toArray()` methods)
- Framework integration points requiring arrays
- Temporary internal data within a single method
- Internal storage inside collection classes

## Cross-Cutting Concerns Pattern

> **Use event subscribers for cross-cutting concerns (metrics, logging),
> NOT direct injection into handlers**

### Anti-Pattern: Metrics in Command Handler

```php
// ❌ WRONG: Metrics in command handler
final class CreateCustomerHandler
{
    public function __construct(
        private CustomerRepository $repository,
        private BusinessMetricsEmitterInterface $metrics  // Wrong place!
    ) {}

    public function __invoke(CreateCustomerCommand $cmd): void
    {
        $customer = Customer::create(...);
        $this->repository->save($customer);
        $this->metrics->emit(new CustomersCreatedMetric());  // Violates SRP
    }
}
```

### Correct Pattern: Dedicated Event Subscriber

```php
// ✅ CORRECT: Clean command handler
final class CreateCustomerHandler
{
    public function __construct(
        private CustomerRepository $repository,
        private EventBusInterface $eventBus
    ) {}

    public function __invoke(CreateCustomerCommand $cmd): void
    {
        $customer = Customer::create(...);
        $this->repository->save($customer);
        $this->eventBus->publish(...$customer->pullDomainEvents());
        // Metrics subscriber handles emission
    }
}

// ✅ CORRECT: Metrics in dedicated subscriber
final class CustomerCreatedMetricsSubscriber implements DomainEventSubscriberInterface
{
    public function __invoke(CustomerCreatedEvent $event): void
    {
        // Error handling is automatic via the domain event message handler.
        // Subscribers run in async workers - failures are logged + emit metrics.
        // This ensures observability never breaks the main request (AP from CAP).
        $this->metricsEmitter->emit($this->metricFactory->create());
    }
}
```

## Common Issues and Fixes

### Issue 1: Class in Wrong Type Directory

```bash
❌ WRONG:
<source_root>/<SharedContext>/Infrastructure/Transformer/UlidValidator.php

✅ CORRECT:
<source_root>/<SharedContext>/Infrastructure/Validator/UlidValidator.php

# Fix:
mv <source_root>/<SharedContext>/Infrastructure/Transformer/UlidValidator.php \
   <source_root>/<SharedContext>/Infrastructure/Validator/UlidValidator.php
# Update namespace and all imports
```

### Issue 2: Vague Variable Names

```php
❌ WRONG:
private UlidTypeConverter $converter;  // Converter of what?

✅ CORRECT:
private UlidTypeConverter $typeConverter;  // Specific!
```

### Issue 3: Misleading Parameter Names

```php
❌ WRONG:
public function fromBinary(mixed $binary): Ulid  // Accepts mixed, not just binary

✅ CORRECT:
public function fromBinary(mixed $value): Ulid  // Accurate!
```

### Issue 4: Helper/Util Classes

```php
❌ WRONG:
class CustomerHelper {
    public function validateEmail() {}
    public function formatName() {}
    public function convertData() {}
}

✅ CORRECT: Extract specific responsibilities
- CustomerEmailValidator (Validator/)
- CustomerNameFormatter (Formatter/)
- CustomerDataConverter (Converter/)
```

### Issue 5: Namespace Mismatch

```php
❌ WRONG:
// File: <source_root>/<SharedContext>/Infrastructure/Validator/UlidValidator.php
namespace App\Shared\Infrastructure\Transformer;  // Mismatch!

✅ CORRECT:
// File: <source_root>/<SharedContext>/Infrastructure/Validator/UlidValidator.php
namespace App\Shared\Infrastructure\Validator;  // Matches directory!
```

## Decision Tree: Where Does It Belong?

```text
What does the class DO?

├─ Converts between types (string ↔ object)? → Converter/
├─ Transforms for DB/serialization? → Transformer/
├─ Validates values? → Validator/
├─ Builds/constructs objects? → Builder/
├─ Fixes/modifies data? → Fixer/
├─ Creates complex objects? → Factory/
├─ Resolves/determines values? → Resolver/
├─ Normalizes/serializes? → Serializer/
├─ Formats data for display? → Formatter/
├─ Maps data between structures? → Mapper/
├─ Provides data/cookies/context? → Provider/
└─ Something else? → Ask the user before creating a new directory!
```

## Verification Commands

```bash
# Check namespace consistency and types:
#   run the targets mapped by make.psalm and make.phpinsights
#   (the style score covers coding-standard fixes)

# Find organizational issues (generic tooling)
grep -r "class.*Helper" <architecture.source_root>/   # Find Helper classes
grep -r "class.*Util" <architecture.source_root>/     # Find Util classes
grep -r 'private.*\$converter;' <architecture.source_root>/  # Find vague names

# Verify architecture compliance:
#   run the target mapped by make.deptrac
#   must show quality.deptrac_violations (= 0) violations
```

If a `make.*` entry is `null`, the capability is absent — note the skip
and fall back to the remaining checks instead of inventing a target.

## Service Configuration: No Redundant Wiring

Applies when `framework.name` is `symfony` (adapt the mechanics for
other DI containers; the rule itself is generic).

> **Do not add explicit interface aliases in `services.yaml` when
> autowiring can resolve them automatically.**

### Rule

When an interface has **exactly one implementation** under
`architecture.source_root`, autowiring automatically aliases the
interface to that implementation. Do NOT add a manual alias — it is
redundant.

### When an Explicit Alias IS Required

- The interface has **multiple implementations** (e.g., a cached
  decorator plus the persistence implementation)
- The implementation lives **outside** the autowired source resource
  (e.g., a third-party bundle class)
- You need to alias to a **different** implementation than what
  autowiring would pick

### When an Explicit Alias is REDUNDANT (remove it)

- Only one class under `architecture.source_root` implements the interface
- Both the interface and implementation are covered by the autowired
  resource in `services.yaml`

### Example

```yaml
# ❌ REDUNDANT: Only one implementation exists — autowiring handles this
App\Customer\Domain\Repository\PaymentTokenRepositoryInterface:
  alias: App\Customer\Infrastructure\Repository\RedisPaymentTokenRepository

# ✅ REQUIRED: Two implementations exist — must disambiguate
App\Customer\Domain\Repository\CustomerRepositoryInterface:
  alias: App\Customer\Infrastructure\Repository\CachedCustomerRepository
```

(`Customer` stands for any entry of `architecture.bounded_contexts`.)

### Explicit Constructor Arguments Are Still Needed

Even when the alias is redundant, you may still need an explicit service
definition for **constructor arguments** that autowiring cannot resolve
(e.g., non-type-hinted parameters, named service references):

```yaml
# ✅ NEEDED: $stateRedis is a named Redis connection, not autowirable
App\Customer\Infrastructure\Repository\RedisStateRepository:
  arguments:
    $stateRedis: '@customer.redis_connection'
# ❌ NOT NEEDED: the interface alias (autowiring resolves it)
# App\Customer\Domain\Repository\StateRepositoryInterface:
#   alias: App\Customer\Infrastructure\Repository\RedisStateRepository
```

### Verification

```bash
# Check that autowiring resolves the interface correctly
# (Symfony console; run inside the PHP container)
bin/console debug:container <InterfaceName>
# Should show "This service is a private alias for the service <Implementation>"
```

## Constraints (Never Do This)

**NEVER**:

- Place class in wrong type directory (violates "Directory X contains ONLY class type X")
- Allow Domain layer to import framework code (`framework.name` components, Doctrine, API Platform)
- Use vague variable names (`$converter`, `$resolver` - be specific!)
- Create "Helper" or "Util" classes (extract specific responsibilities)
- Allow namespace to mismatch directory structure
- Use arrays for structured data when typed classes would be appropriate
- Use untyped `array` in method signatures — always specify content type via docblock or use collection classes
- Use `array` type for collections of domain/application objects — use typed collections
- Use `json_encode`/`json_decode` — use the framework serializer
- Use constructor defaults that instantiate collaborators — inject the dependency instead
- Use direct `new` for value objects with named constructors — use `{ValueObject}::fromString()`
- Inject cross-cutting concerns (metrics, logging) into command handlers
- Create complex objects directly without factories in production code
- Add redundant interface aliases in service config when autowiring resolves them
- Add suppression annotations (`@psalm-suppress`, `@phpstan-ignore*`, `phpcs:ignore`) instead of fixing structure
- Lower any `quality.*` threshold or edit `deptrac.yaml` to make misplaced code pass

**ALWAYS**:

- Verify "Directory X contains ONLY class type X" principle
- Use specific variable names (`$typeConverter`, not `$converter`)
- Use accurate parameter names (match actual types)
- Ensure namespace matches directory structure exactly
- Extract specific responsibilities from Helper/Util classes
- Prefer typed classes over arrays for structured data
- Always specify array content types in method signatures (e.g. `list<string>`, `array<string, int>`)
- Use typed collection classes instead of arrays of objects
- Use the framework serializer instead of `json_encode`/`json_decode`
- Inject dependencies instead of instantiating constructor defaults
- Use named constructors for value objects in production code
- Use event subscribers for cross-cutting concerns
- Use factories for complex object creation in production code

## Hardcoded Configuration Values → `.env` Extraction

> **Configurable values (TTLs, timeouts, limits, sizes, batch counts)
> belong in `.env`, not as class constants.**

### When to Extract

Extract a constant to `.env` when it represents:

- **Time durations**: TTLs, timeouts, expiration periods, intervals
- **Rate limits**: Max requests, windows, thresholds
- **Sizes**: Batch sizes, max body sizes, token lengths
- **Retry configuration**: Delay, max attempts, backoff intervals
- **Infrastructure tunables**: Cache TTLs, queue settings, lockout parameters

### When NOT to Extract

Keep as constants when the value is:

- **Protocol/spec-defined**: HTTP status codes, cipher IV lengths, segment lengths
- **Security-critical internal**: Encryption tag lengths, HSTS header values
- **Domain invariants**: Validation rules that are part of the domain model

### Extraction Pattern (3-Step)

**Step 1**: Add env variable to `.env` and `.env.test`

```dotenv
# .env
CACHE_CUSTOMER_BY_ID_TTL=600
CACHE_CUSTOMER_BY_EMAIL_TTL=300

# .env.test (same or test-appropriate value)
CACHE_CUSTOMER_BY_ID_TTL=600
CACHE_CUSTOMER_BY_EMAIL_TTL=300
```

**Step 2**: Bind in the service config (`config/services.yaml` for Symfony)

```yaml
App\Customer\Infrastructure\Repository\CachedCustomerRepository:
  arguments:
    $ttlById: '%env(int:CACHE_CUSTOMER_BY_ID_TTL)%'
    $ttlByEmail: '%env(int:CACHE_CUSTOMER_BY_EMAIL_TTL)%'
```

**Step 3**: Replace constant with constructor parameter

```php
// ❌ BEFORE: Hardcoded constant
final class CachedCustomerRepository
{
    private const TTL_BY_ID = 600;
    private const TTL_BY_EMAIL = 300;
}

// ✅ AFTER: Injected from .env
final readonly class CachedCustomerRepository
{
    public function __construct(
        private CustomerRepositoryInterface $inner,
        private CacheInterface $cache,
        private int $ttlById,
        private int $ttlByEmail,
    ) {
    }
}
```

### Common Extraction Candidates

| Pattern in Source                         | Extract To `.env`                       |
| ----------------------------------------- | --------------------------------------- |
| `private const TTL_* = <seconds>`         | `CACHE_*_TTL=<seconds>`                 |
| `private const EXPIRES_AFTER_* = <value>` | `TOKEN_EXPIRATION_SECONDS=<value>`      |
| `private const MAX_ATTEMPTS = <n>`        | `*_MAX_ATTEMPTS=<n>`                    |
| `private const BATCH_SIZE = <n>`          | `*_BATCH_SIZE=<n>`                      |
| `private const DEFAULT_*_SECONDS = <n>`   | `*_SECONDS=<n>`                         |
| Constructor default `= 900`               | Remove default, bind via service config |

### Verification After Extraction

Run, in order:

1. Target mapped by `make.phpinsights` — style score stays at
   `quality.phpinsights.style`
2. Target mapped by `make.psalm` — `quality.psalm_errors` (= 0) errors
3. Target mapped by `make.tests` — update mocks for new constructor params
4. Target mapped by `make.ci` — full validation

## CI Integration: When CI Fails

When the target mapped by `make.ci` fails, consult this skill if the
failure involves:

| CI Failure Indicator                 | Code Organization Fix                               |
| ------------------------------------ | --------------------------------------------------- |
| Class not found / namespace mismatch | Verify namespace matches directory structure        |
| Deptrac violation after moving class | Check layer placement (Domain/Application/Infra)    |
| PHPInsights architecture score drop  | Verify "Directory X contains ONLY class type X"     |
| Psalm type errors after refactoring  | Check that imports and namespaces were all updated  |
| Test failures after class move       | Move test file too, update test namespace + imports |

Thresholds come from the profile only: PHPInsights scores must stay at
`quality.phpinsights.architecture` / `quality.phpinsights.style` (default
100) and `quality.phpinsights.complexity` (default 94); Deptrac at
`quality.deptrac_violations` and Psalm at `quality.psalm_errors` (fixed
ceilings of 0). Score floors are **raise-only** (ADR-7): a profile may
tighten them, never relax them — fix the code, never the threshold.

### Refactoring Checklist (Before Running CI)

When moving, renaming, or restructuring classes:

- [ ] Class in correct directory for its type (see Decision Tree above)
- [ ] Namespace matches directory structure exactly
- [ ] All `use` imports updated under `architecture.source_root` and `tests/`
- [ ] Test file moved to mirror source structure
- [ ] Test namespace updated
- [ ] Service config references updated (if service was explicitly configured)
- [ ] Doctrine mapping files updated if an entity moved (`config/doctrine/`,
      suffix per `persistence.mapper`: `.orm.xml` for `doctrine-orm`,
      `.mongodb.xml` for `doctrine-odm`)
- [ ] Validator config references updated (`config/validator/*.yaml`, if a
      validation target moved)
- [ ] Hardcoded config values extracted to `.env` if applicable
- [ ] Targets mapped by `make.psalm`, `make.deptrac`, and `make.tests` pass

```yaml # profile-example
# Upstream reference profile values this skill reads:
architecture:
  source_root: src
  bounded_contexts: [User, OAuth]
  shared_context: Shared
framework:
  name: symfony
  api_platform: "4.2"
  graphql: true
persistence:
  mapper: doctrine-odm   # entity moves touch config/doctrine/*.mongodb.xml
make:
  ci: ci
  psalm: psalm
  deptrac: deptrac
  phpinsights: phpinsights
  tests: tests
quality:
  phpinsights: {architecture: 100, style: 100, complexity: 94}
  deptrac_violations: 0
  psalm_errors: 0
```

## Related Skills

- [ci-workflow](../ci-workflow/SKILL.md) — use code-organization principles when fixing CI failures that stem from structural issues
- [code-review](../code-review/SKILL.md) — references this skill for organization verification during PR reviews
- [complexity-management](../complexity-management/SKILL.md) — refactoring often requires reorganization; consult both skills together
- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) — DDD patterns and layer structure
- [deptrac-fixer](../deptrac-fixer/SKILL.md) — fixes architectural boundary violations (layer moves vs. file placement)
- [quality-standards](../quality-standards/SKILL.md) — maintains overall code quality metrics

## Related Documentation

See [DIRECTORY-STRUCTURE.md](DIRECTORY-STRUCTURE.md) for the complete
layer-by-layer directory reference, file naming conventions, and
step-by-step placement guides.
