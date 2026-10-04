---
name: cache-management
description: Implement production-grade caching with cache keys/TTLs/consistency classes per query, SWR (stale-while-revalidate), event-driven invalidation, HTTP cache headers, and comprehensive testing for stale reads and cache warmup. Use when adding caching to queries or repositories, implementing cache invalidation, configuring HTTP caching, or ensuring cache consistency and performance.
---

# Cache Management Skill

## Profile keys consumed

- `framework.name`, `framework.api_platform`
- `persistence.mapper`, `persistence.engine`
- `architecture.source_root`, `architecture.bounded_contexts`, `architecture.shared_context`
- `make.ci`, `make.tests`
- `quality.phpinsights.complexity`, `quality.infection_msi`

## Context (Input)

Use this skill when:

- Adding caching to repositories or expensive queries
- Implementing cache invalidation via domain events
- Defining cache keys, TTLs, and consistency requirements
- Implementing stale-while-revalidate (SWR) pattern
- Configuring HTTP cache headers (Cache-Control, ETag, Vary)
- Testing cache behavior (stale reads, cold start, invalidation)
- Reducing database load with caching
- Setting up async event-driven cache invalidation

## Task (Function)

Implement production-ready caching with proper key design, TTL management, event-driven invalidation, HTTP cache headers, and comprehensive testing.

**Success Criteria**:

- Cache policy declared for each query (key, TTL, consistency class)
- Decorator pattern: `Cached{Entity}Repository` wraps the persistence-specific repository (see "Repository naming")
- Event-driven invalidation via domain event subscribers
- Marker interface pattern for auto-binding cache pools
- Best-effort invalidation (try/catch, never fail business operations)
- HTTP cache headers configured (Cache-Control, ETag for API responses)
- Async event processing via message queue (AP from CAP theorem)
- Comprehensive unit tests for all cache paths
- Cache observability (hit/miss/error logging)
- The target mapped by `make.ci` exits `0`

---

## CRITICAL CACHE POLICY

```text
ALWAYS use Decorator Pattern for caching (wrap repositories)
ALWAYS use CacheKeyBuilder service (prevent key drift)
ALWAYS invalidate via Domain Events (decouple from business)
ALWAYS use TagAwareCacheInterface for cache tags
ALWAYS wrap cache ops in try/catch (best-effort, no failures)
ALWAYS use Marker Interface for auto-binding cache pools
ALWAYS process invalidation async (AP from CAP theorem)

FORBIDDEN: Caching inside the base repository, implicit invalidation
REQUIRED:  Decorator pattern, event-driven invalidation
```

## CAP Theorem: Why We Choose AP (Availability + Partition Tolerance)

Cache invalidation follows **AP from CAP theorem** - we prioritize:

- **Availability**: Business operations never fail due to cache issues
- **Partition Tolerance**: System works even when cache is unavailable

**Trade-off**: Brief staleness is acceptable over blocking writes.

**Implementation**:

- Cache errors fallback to database (try/catch everywhere)
- Invalidation processed asynchronously via message queue
- Exceptions in subscribers are logged + emit metrics (self-healing)
- Business operations complete even if cache invalidation fails

**Non-negotiable requirements**:

- Use Decorator Pattern: `Cached{Entity}Repository` wraps the persistence-specific repository
- Use centralized `CacheKeyBuilder` service (in the shared context's Infrastructure layer)
- Invalidate via Domain Event Subscribers (one subscriber per event)
- Use Marker Interface for auto-binding cache pools via `_instanceof`
- Process cache invalidation asynchronously via message queue
- Wrap ALL cache operations in try/catch (never fail business operations)
- Use `TagAwareCacheInterface` (not `CacheInterface`) for tag support
- Configure test cache pools with `tags: true` in `config/packages/test/cache.yaml`
- Log cache operations for observability

## Repository Naming

The decorator is **always** named `Cached{Entity}Repository`. The inner class it wraps is the persistence-specific implementation; derive its name from the profile:

- `persistence.mapper` / `persistence.engine` determine the concrete repository: by convention either plain `{Entity}Repository` or engine-prefixed `{Engine}{Entity}Repository` (PascalCase of the `persistence.engine` value, e.g. engine `postgresql` produces a `Postgresql`-prefixed repository). Follow whichever convention the repository already uses — do not rename existing classes.
- The decorator **implements the domain interface** (`{Entity}RepositoryInterface`) and receives the inner repository through that interface. It never extends the concrete class, and its code never references engine-specific APIs — all persistence stays in the inner repository.
- The domain interface alias in `config/services.yaml` points at `Cached{Entity}Repository`; the concrete inner repository remains registered for direct consumers (e.g. API Platform collection providers).

## File Locations

`{Context}` must be one of `architecture.bounded_contexts`; `<source_root>` is `architecture.source_root`; `<Shared>` is `architecture.shared_context` (when `null`, place shared cache services in the owning bounded context instead).

| Component                    | Typical Location                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| CacheKeyBuilder              | `<source_root>/<Shared>/Infrastructure/Cache/CacheKeyBuilder.php`                                      |
| Cached{Entity}Repository     | `<source_root>/{Context}/Infrastructure/Repository/Cached{Entity}Repository.php`                       |
| Base repository (inner)      | `<source_root>/{Context}/Infrastructure/Repository/*Repository.php`                                    |
| Marker interface             | `<source_root>/{Context}/Application/EventSubscriber/{Entity}CacheInvalidationSubscriberInterface.php` |
| Invalidation subscriber      | `<source_root>/{Context}/Application/EventSubscriber/{Event}CacheInvalidationSubscriber.php`           |
| Cache pool config            | `config/packages/cache.yaml`                                                                           |
| Test cache config            | `config/packages/test/cache.yaml`                                                                      |
| Service wiring / aliases     | `config/services.yaml`                                                                                 |
| HTTP cache tests             | `tests/Integration/*HttpCacheTest.php`                                                                 |
| Unit tests                   | `tests/Unit/**`                                                                                        |
| Integration tests (optional) | `tests/Integration/**`                                                                                 |

---

## TL;DR - Cache Management Checklist

**Before Implementing Cache:**

- [ ] Identified slow query worth caching
- [ ] Cache policy declared (key pattern, TTL, consistency class)
- [ ] Cache tags defined for invalidation strategy
- [ ] Domain events defined for cache invalidation triggers
- [ ] HTTP cache headers strategy defined (if API endpoint)

**Architecture Setup:**

- [ ] Created `Cached{Entity}Repository` decorator class
- [ ] Created `CacheKeyBuilder` service (or extended existing one)
- [ ] Created marker interface for cache invalidation subscribers
- [ ] Created cache invalidation event subscribers (one per event)
- [ ] Configured `services.yaml` with `_instanceof` for auto-binding cache pools
- [ ] Configured async event processing via message bus

**During Implementation:**

- [ ] Decorator wraps inner repository (not extends)
- [ ] CacheKeyBuilder used for all cache keys (prevents drift)
- [ ] Cache operations wrapped in try/catch (best-effort)
- [ ] Event subscribers use same CacheKeyBuilder for tags
- [ ] Logging added for cache hits/misses/errors
- [ ] Repository uses `TagAwareCacheInterface` (required for tags)

**Testing:**

- [ ] Test cache pool configured with `tags: true`
- [ ] Unit tests for cache invalidation subscribers
- [ ] Integration tests for stale reads after writes (if valuable)
- [ ] Test: Cache error fallback to database works
- [ ] HTTP cache tests for Cache-Control headers and ETag validation

**Before Merge:**

- [ ] All cache tests pass (target mapped by `make.tests`)
- [ ] Cache observability verified (logs present)
- [ ] HTTP cache headers verified (if API endpoint)
- [ ] Target mapped by `make.ci` passes
- [ ] No cache-related stale data issues
- [ ] No `quality.*` threshold lowered (floors are raise-only: `quality.phpinsights.complexity` default 94, `quality.infection_msi` default 100)

---

## Quick Start: Cache in 9 Steps

The `Customer` entity below is illustrative; namespaces follow the PSR-4 prefix of `architecture.source_root`, with `{Context}` from `architecture.bounded_contexts` and `Shared` standing for `architecture.shared_context`.

### Step 1: Declare Cache Policy

**Before writing code, declare the complete policy:**

```php
/**
 * Cache Policy for Customer By ID Query
 *
 * Key Pattern: customer.{id}
 * TTL: 600s (10 minutes)
 * Consistency: Stale-While-Revalidate
 * Invalidation: Via domain events (CustomerCreated/Updated/Deleted)
 * Tags: [customer, customer.{id}]
 * HTTP Cache: Cache-Control: max-age=600, public, s-maxage=600
 * Notes: Read-heavy operation, tolerates brief staleness
 */
```

### Step 2: Create CacheKeyBuilder Service

**Location**: `<source_root>/<Shared>/Infrastructure/Cache/CacheKeyBuilder.php`

```php
final readonly class CacheKeyBuilder
{
    public function __construct(private SerializerInterface $serializer)
    {
    }

    public function build(string $namespace, string ...$parts): string
    {
        return $namespace . '.' . implode('.', $parts);
    }

    public function buildCustomerKey(string $customerId): string
    {
        return $this->build('customer', $customerId);
    }

    public function buildCustomerEmailKey(string $email): string
    {
        return $this->build('customer', 'email', $this->hashEmail($email));
    }

    /**
     * Build cache key for collections (filters normalized + hashed)
     * @param array<string, string|int|float|bool|array|null> $filters
     */
    public function buildCustomerCollectionKey(array $filters): string
    {
        ksort($filters);  // Normalize key order
        return $this->build(
            'customer',
            'collection',
            hash('sha256', $this->serializer->serialize($filters, JsonEncoder::FORMAT))
        );
    }

    /**
     * Hash email consistently (lowercase + SHA256)
     * - Lowercase normalization (email case-insensitive)
     * - SHA256 hashing (fixed length, prevents key length issues)
     */
    public function hashEmail(string $email): string
    {
        return hash('sha256', strtolower($email));
    }
}
```

### Step 3: Create Cached Repository Decorator

**Location**: `<source_root>/{Context}/Infrastructure/Repository/Cached{Entity}Repository.php`

```php
final class CachedCustomerRepository implements CustomerRepositoryInterface
{
    public function __construct(
        private CustomerRepositoryInterface $inner,  // Persistence-specific repository
        private TagAwareCacheInterface $cache,
        private CacheKeyBuilder $cacheKeyBuilder,
        private LoggerInterface $logger
    ) {}

    /**
     * Proxy all other method calls to inner repository
     * Required for API Platform's collection provider compatibility
     * @param array<int, mixed> $arguments
     */
    public function __call(string $method, array $arguments): mixed
    {
        return $this->inner->{$method}(...$arguments);
    }

    public function find(mixed $id, int $lockMode = 0, ?int $lockVersion = null): ?Customer
    {
        $cacheKey = $this->cacheKeyBuilder->buildCustomerKey((string) $id);

        try {
            return $this->cache->get(
                $cacheKey,
                fn (ItemInterface $item) => $this->loadCustomerFromDb($id, $lockMode, $lockVersion, $cacheKey, $item),
                beta: 1.0
            );
        } catch (\Throwable $e) {
            $this->logCacheError($cacheKey, $e);
            return $this->inner->find($id, $lockMode, $lockVersion);
        }
    }

    public function save(Customer $customer): void
    {
        $this->inner->save($customer);
        // NO cache invalidation here - handled by domain event subscribers
    }

    private function loadCustomerFromDb(mixed $id, int $lockMode, ?int $lockVersion, string $cacheKey, ItemInterface $item): ?Customer
    {
        $item->expiresAfter(600);
        $item->tag(['customer', "customer.{$id}"]);

        $this->logger->info('Cache miss - loading customer from database', [
            'cache_key' => $cacheKey,
            'customer_id' => $id,
            'operation' => 'cache.miss',
        ]);

        return $this->inner->find($id, $lockMode, $lockVersion);
    }

    private function logCacheError(string $cacheKey, \Throwable $e): void
    {
        $this->logger->error('Cache error - falling back to database', [
            'cache_key' => $cacheKey,
            'error' => $e->getMessage(),
            'operation' => 'cache.error',
        ]);
    }
}
```

### Step 4: Create Marker Interface for Auto-Binding

**Location**: `<source_root>/{Context}/Application/EventSubscriber/{Entity}CacheInvalidationSubscriberInterface.php`

**Purpose**: Enables automatic cache pool injection via `_instanceof` in services.yaml.

```php
<?php

declare(strict_types=1);

namespace App\Customer\Application\EventSubscriber;

use App\Shared\Domain\Bus\Event\DomainEventSubscriberInterface;

/**
 * Marker interface for customer cache invalidation subscribers.
 *
 * Used to auto-bind the customer cache pool via _instanceof configuration.
 */
interface CustomerCacheInvalidationSubscriberInterface extends DomainEventSubscriberInterface
{
}
```

### Step 5: Create Event Subscribers for Invalidation

**Location**: `<source_root>/{Context}/Application/EventSubscriber/{Event}CacheInvalidationSubscriber.php`

**IMPORTANT**: Create ONE subscriber per event. Implement the marker interface.

```php
/**
 * Customer Updated Event Cache Invalidation Subscriber
 *
 * ARCHITECTURAL DECISION: Processed via the async event bus.
 * This subscriber runs in message-queue workers. Exceptions propagate to
 * the event message handler which catches, logs, and emits failure metrics.
 * We follow AP from CAP theorem (Availability + Partition tolerance over Consistency).
 */
final readonly class CustomerUpdatedCacheInvalidationSubscriber implements
    CustomerCacheInvalidationSubscriberInterface
{
    public function __construct(
        private TagAwareCacheInterface $cache,
        private CacheKeyBuilder $cacheKeyBuilder,
        private LoggerInterface $logger
    ) {}

    public function __invoke(CustomerUpdatedEvent $event): void
    {
        $tagsToInvalidate = $this->buildTagsToInvalidate($event);
        $this->cache->invalidateTags($tagsToInvalidate);
        $this->logSuccess($event);
    }

    /** @return array<class-string> */
    public function subscribedTo(): array
    {
        return [CustomerUpdatedEvent::class];
    }

    /** @return array<string> */
    private function buildTagsToInvalidate(CustomerUpdatedEvent $event): array
    {
        $tags = [
            'customer.' . $event->customerId(),
            'customer.email.' . $this->cacheKeyBuilder->hashEmail($event->currentEmail()),
            'customer.collection',
        ];

        if ($event->emailChanged() && $event->previousEmail() !== null) {
            $tags[] = 'customer.email.' . $this->cacheKeyBuilder->hashEmail($event->previousEmail());
        }

        return $tags;
    }

    private function logSuccess(CustomerUpdatedEvent $event): void
    {
        $this->logger->info('Cache invalidated after customer update', [
            'event_id' => $event->eventId(),
            'email_changed' => $event->emailChanged(),
            'operation' => 'cache.invalidation',
            'reason' => 'customer_updated',
        ]);
    }
}
```

### Step 6: Configure services.yaml with Marker Interface

**CRITICAL**: Use `_instanceof` with the marker interface for auto-binding cache pools. The inner repository class name follows the "Repository naming" rule above (shown here as `{Persistence}CustomerRepository`).

```yaml
services:
  # Base repository - used by API Platform for collections
  # Concrete class name derived from persistence.mapper/persistence.engine
  App\Customer\Infrastructure\Repository\{Persistence}CustomerRepository:
    public: true

  # Cached repository - wraps base repository with caching
  App\Customer\Infrastructure\Repository\CachedCustomerRepository:
    arguments:
      $inner: '@App\Customer\Infrastructure\Repository\{Persistence}CustomerRepository'
      $cache: '@cache.customer'

  # Alias interface to cached repository for dependency injection
  App\Customer\Domain\Repository\CustomerRepositoryInterface:
    alias: App\Customer\Infrastructure\Repository\CachedCustomerRepository
    public: true

  # Auto-bind cache pool to all cache invalidation subscribers via marker interface
  _instanceof:
    App\Customer\Application\EventSubscriber\CustomerCacheInvalidationSubscriberInterface:
      bind:
        $cache: '@cache.customer'

    App\Shared\Domain\Bus\Event\DomainEventSubscriberInterface:
      tags: ['app.event_subscriber']

  # Async event bus for cache invalidation (AP from CAP theorem)
  App\Shared\Domain\Bus\Event\EventBusInterface:
    alias: App\Shared\Infrastructure\Bus\Event\Async\AsyncEventBus
```

### Step 7: Configure Cache Pools

**Production** - `config/packages/cache.yaml`:

```yaml
framework:
  cache:
    app: cache.adapter.redis
    default_redis_provider: '%env(resolve:REDIS_URL)%'

    pools:
      cache.customer:
        adapter: cache.adapter.redis
        default_lifetime: 600
        provider: '%env(resolve:REDIS_URL)%'
        tags: true
```

**Test** - `config/packages/test/cache.yaml`:

```yaml
framework:
  cache:
    pools:
      cache.customer:
        adapter: cache.adapter.array
        provider: null
        tags: true
```

### Step 8: Configure HTTP Cache Headers

Branch on `framework.api_platform`:

- **Version string** — declare `cacheHeaders` on the resource operations (below).
- **`false`** — no API Platform layer: set the same headers via the framework's response layer (e.g. a `kernel.response` listener or controller `Response` configuration per `framework.name`); the header values and rationale are identical.

```yaml
# config/api_platform/resources/customer.yaml
App\Customer\Domain\Entity\Customer:
  operations:
    get:
      class: ApiPlatform\Metadata\Get
      cacheHeaders:
        max_age: 600
        shared_max_age: 600
        public: true
        vary: ['Accept', 'Accept-Language']

    get_collection:
      class: ApiPlatform\Metadata\GetCollection
      cacheHeaders:
        max_age: 300
        shared_max_age: 600
        public: true
        vary: ['Accept', 'Accept-Language']
```

**HTTP Cache Headers Explained**:

| Header     | Single Resource         | Collection              | Purpose              |
| ---------- | ----------------------- | ----------------------- | -------------------- |
| `max-age`  | 600s (10 min)           | 300s (5 min)            | Browser cache TTL    |
| `s-maxage` | 600s                    | 600s                    | CDN/proxy cache TTL  |
| `public`   | true                    | true                    | Allow shared caching |
| `Vary`     | Accept, Accept-Language | Accept, Accept-Language | Cache key variants   |
| `ETag`     | Auto-generated          | Auto-generated          | Conditional requests |

**ETag Behavior**:

- ETag is automatically generated based on resource content
- ETag changes after resource modification
- Clients can use `If-None-Match` for conditional requests
- Returns `304 Not Modified` if resource unchanged

### Step 9: Verify with CI

Run the target mapped by `make.ci`; it must exit `0`.

---

## Cache Policy Decision Rules

### Cache key design

Format: `{namespace}.{entity}.{identifier}.{variation}` — lowercase, dot-separated, short, predictable, versioned (`customer.v2.{id}`) when the cached structure changes. Never put special characters or sensitive data (raw emails, tokens) in keys — hash them. Never exceed ~100 chars or use unpredictable patterns.

### TTL selection matrix

| Data freshness requirement | TTL range     | Use cases                          |
| -------------------------- | ------------- | ---------------------------------- |
| Real-time                  | No cache      | Live notifications, stock prices   |
| Near real-time             | 1-10 seconds  | Live dashboards, active sessions   |
| Fresh                      | 30-60 seconds | Search results, recommendations    |
| Moderately fresh           | 5-15 minutes  | User profiles, entity details      |
| Stable                     | 1-6 hours     | Catalogs, category lists           |
| Static                     | 1-7 days      | Configuration, rarely-changed data |

Factors: change frequency, business impact of staleness, query cost (expensive queries earn longer TTL + invalidation), traffic (high traffic earns longer TTL).

### Consistency classes

1. **Strong (no cache)** — real-time, security-sensitive, financial, inventory.
2. **Eventual** — read-heavy, tolerates brief staleness, non-critical.
3. **Stale-While-Revalidate (SWR)** — high-traffic queries wanting fast responses and fresh data. In Symfony-contracts caches, pass `beta: 1.0` to `TagAwareCacheInterface::get()` (probabilistic early expiration); this also prevents cache stampedes at TTL expiry. Do NOT use SWR for financial/critical or security-sensitive reads.

### Invalidation strategy matrix

| Strategy      | When to use                       | Complexity | Consistency |
| ------------- | --------------------------------- | ---------- | ----------- |
| Write-through | Single entity CRUD                | Low        | Strong      |
| Tag-based     | Batch invalidation, related data  | Low        | Strong      |
| Event-driven  | Complex domain events, decoupling | Medium     | Strong      |
| Time-based    | Static data, aggregations         | Low        | Eventual    |
| Manual        | One-off operations, bulk imports  | Low        | User-driven |

Core principle: **explicit over implicit** — never rely on TTL alone for data that changes via write commands. Prefer tag-based + event-driven; combine SWR for reads with explicit invalidation for writes.

**Anti-patterns**: clearing all cache without reason (`$cache->clear()`); over-invalidation (whole-namespace tag for a single-entity update); invalidating inside the repository `save()` when domain events already exist.

---

## HTTP Cache Testing

Test HTTP cache headers in integration tests:

```php
final class CustomerHttpCacheTest extends ApiTestCase
{
    public function testGetCustomerReturnsCacheControlHeaders(): void
    {
        $client = self::createClient();
        $customer = $this->createTestCustomer();

        $client->request('GET', "/api/customers/{$customer->getUlid()}");

        self::assertResponseIsSuccessful();
        self::assertResponseHeaderSame('Cache-Control', 'max-age=600, public, s-maxage=600');
        self::assertResponseHasHeader('ETag');
    }

    public function testGetCustomerCollectionReturnsCacheControlHeaders(): void
    {
        $client = self::createClient();
        $this->createTestCustomer();

        $client->request('GET', '/api/customers');

        self::assertResponseIsSuccessful();
        self::assertResponseHeaderSame('Cache-Control', 'max-age=300, public, s-maxage=600');
    }

    public function testETagChangesAfterModification(): void
    {
        $client = self::createClient();
        $customer = $this->createTestCustomer();

        // First request to get initial ETag
        $response1 = $client->request('GET', "/api/customers/{$customer->getUlid()}");
        $etag1 = $response1->getHeaders()['etag'][0] ?? null;
        self::assertNotNull($etag1);

        // Modify customer
        $client->request('PATCH', "/api/customers/{$customer->getUlid()}", [
            'json' => ['initials' => 'Updated Name'],
            'headers' => ['Content-Type' => 'application/merge-patch+json'],
        ]);

        // Request again to get new ETag
        $response2 = $client->request('GET', "/api/customers/{$customer->getUlid()}");
        $etag2 = $response2->getHeaders()['etag'][0] ?? null;

        // ETag should change after modification
        self::assertNotEquals($etag1, $etag2);
    }
}
```

---

## Async Event Processing Architecture

Cache invalidation is processed asynchronously for resilience:

```text
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  Domain Event   │────▶│ Async Event          │────▶│   Message Queue     │
│  (Published)    │     │ Dispatcher           │     │                     │
└─────────────────┘     └──────────────────────┘     └─────────┬───────────┘
                                                               │
                        ┌──────────────────────┐               │
                        │  Domain Event        │◀──────────────┘
                        │  Message Handler     │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  Cache Invalidation  │
                        │  Subscriber          │
                        └──────────────────────┘
```

**Resilience Layers**:

1. **Layer 1**: The async event dispatcher catches queue send failures
2. **Layer 2**: The domain event message handler catches subscriber failures
3. **All failures**: Logged + emit metrics (self-healing pipeline)

---

## Constraints

### NEVER

- Cache inside the base repository — caching lives only in the decorator
- Invalidate implicitly (TTL-only) for command-written data
- Let cache failures break business operations
- Edit `deptrac.yaml` or add suppression annotations to silence violations introduced by cache classes — fix the code placement instead
- Lower any `quality.*` threshold to land cache code; floors are raise-only (shipped defaults: `quality.phpinsights.complexity` 94, `quality.infection_msi` 100)

### ALWAYS

- Keep the decorator persistence-agnostic (interface-typed `$inner`)
- Run the target mapped by `make.tests` for cache test suites and the target mapped by `make.ci` before finishing

---

## Related Skills

- [testing-workflow](../testing-workflow/SKILL.md) - Running and debugging the cache test suites
- [query-performance-analysis](../query-performance-analysis/SKILL.md) - Identify slow queries worth caching
- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - Domain events and subscriber patterns
- [api-platform-crud](../api-platform-crud/SKILL.md) - Resource configuration that hosts `cacheHeaders`

## Additional Resources

- End-to-end example: `examples/cache-implementation.md`
- Tests guide: `examples/cache-testing.md`
