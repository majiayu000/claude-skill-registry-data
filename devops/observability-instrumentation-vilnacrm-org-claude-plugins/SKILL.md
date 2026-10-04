---
name: observability-instrumentation
description: Add type-safe business metrics for domain events to a PHP backend — emitted as AWS EMF (Embedded Metric Format) when `capabilities.observability_emf` is true, or through a generic metrics emitter otherwise. Use when implementing new endpoints, adding command handlers or domain events, or instrumenting business events for dashboards and KPIs.
---

# Business Metrics Instrumentation

## Profile keys consumed

- `capabilities.observability_emf`
- `project.name`
- `framework.name`
- `architecture.source_root`
- `architecture.shared_context`
- `architecture.bounded_contexts`
- `make.tests`
- `make.ci`
- `quality.infection_msi`

All make invocations go through the profile's `make` target map. A `null`
value means the capability is absent: skip with a note, never improvise a
raw repo-specific command.

## Capability gate

`capabilities.observability_emf` selects the emission backend; the
application-layer design is identical in both branches:

- **`true`** — emit metrics as AWS CloudWatch Embedded Metric Format
  (EMF) structured logs. Apply every section of this skill, including
  [AWS EMF emission](#aws-emf-emission-only-when-capabilitiesobservability_emf-true).
- **`false`** — apply the same typed-metric/event-subscriber
  architecture, but implement the emitter against the project's metrics
  backend (Prometheus, StatsD, OpenTelemetry, or a structured-log
  counter). Skip the EMF format and CloudWatch sections; see
  [Generic metrics backends](#generic-metrics-backends-when-capabilitiesobservability_emf-false).

## What this skill covers

- **Business metrics** — domain events (users created, orders placed,
  payments processed)
- **Event subscribers** — metrics emitted via domain event subscribers
  (never inside command handlers)
- **Type-safe metrics** — concrete metric classes instead of arrays
- **SOLID principles** — Single Responsibility (subscribers) +
  Open/Closed (new metric classes)

## What this skill does NOT cover

- **Infrastructure metrics** — latency, error rates, RPS. Managed
  runtimes and APM agents typically provide these out of the box; verify
  what the deployment platform already emits before duplicating it.
- **SLO/SLA metrics** — availability, response times (same reason)
- **Distributed tracing** — use the platform's tracing integration
  instead

## When to use

- Implementing new API endpoints with business significance (see the
  [api-platform-crud skill](../api-platform-crud/SKILL.md))
- Adding domain events that should trigger metric emission
- Tracking domain events for analytics and business intelligence
- Building dashboards for business KPIs

---

## Architecture overview

1. **Metric classes** — each metric type is a concrete class extending
   `BusinessMetric`
2. **Event subscribers** — metrics are emitted via domain event
   subscribers, not hardcoded in handlers
3. **Logging stack** — the emitter writes through the framework's
   logging stack (`framework.name`; e.g. a dedicated Monolog channel
   with a custom formatter for Symfony)
4. **No arrays** — all metric configuration uses typed objects
5. **Collections** — multiple metrics use `MetricCollection`, not arrays

Placement follows the layered architecture (paths below are relative to
`architecture.source_root`): the metric base classes and the emitter
**interface** live in the Application layer of
`architecture.shared_context` (when `null`, keep them in the bounded
context that first introduces metrics); the concrete emitter lives in
Infrastructure; per-context metrics and subscribers live in the owning
bounded context (one of `architecture.bounded_contexts`). Fix placement
to satisfy layer rules — never edit `deptrac.yaml` or add suppression
annotations to force a fit.

---

## SOLID principles in observability

### Single Responsibility Principle (SRP)

Each class has ONE responsibility:

| Class                           | Responsibility                           |
| ------------------------------- | ---------------------------------------- |
| `OrdersPlacedMetric`            | Define metric name, value, dimensions    |
| `OrderPlacedMetricsSubscriber`  | Listen to event, emit metric             |
| Emitter implementation          | Format and write metric output           |
| `MetricCollection`              | Hold multiple metrics for batch emission |

**Anti-pattern**: metrics emitted directly in command handlers (violates
SRP — a handler should only handle commands).

### Open/Closed Principle (OCP)

- **Open for extension**: add new metrics via new classes
- **Closed for modification**: don't change existing metric/emitter code

```php
// GOOD: add a new metric by creating a new class
final readonly class OrdersPlacedMetric extends EndpointOperationBusinessMetric { ... }

// BAD: modify the existing emitter to handle a new metric type
```

### Why event subscribers (not handler injection)

```php
// BAD: metrics in the command handler (violates SRP)
final class CreateOrderHandler
{
    public function __construct(
        private OrderRepository $repository,
        private BusinessMetricsEmitterInterface $metrics  // Wrong!
    ) {}
}

// GOOD: metrics in a dedicated event subscriber
final class OrderPlacedMetricsSubscriber implements DomainEventSubscriberInterface
{
    public function __invoke(OrderPlacedEvent $event): void
    {
        $this->metricsEmitter->emit($this->metricFactory->create());
    }
}
```

**Benefits**:

- Handler focuses on domain logic only
- Metrics emission is decoupled and testable
- Easy to add/remove metrics without touching business logic
- Multiple subscribers can react to the same event

Error handling belongs to the domain-event dispatch machinery (async
workers log failures and emit failure metrics automatically), so
subscribers stay clean and observability never breaks the main request
(AP from the CAP theorem).

---

## Type-safe metric class hierarchy

```text
BusinessMetric (abstract)
├── EndpointOperationBusinessMetric (abstract) - metrics with Endpoint/Operation dimensions
│   ├── <Entity><Action>Metric concrete classes (one per business event)
│   └── EndpointInvocationsMetric
└── (other base classes for different dimension patterns)

MetricDimensionsInterface
├── EndpointOperationMetricDimensions - Endpoint + Operation
└── (custom dimensions for specific metrics)

MetricDimensions - typed collection of MetricDimension objects
MetricDimension - key/value pair

MetricUnit (enum)
├── COUNT, NONE, SECONDS, MILLISECONDS, BYTES, PERCENT

MetricCollection - typed collection implementing IteratorAggregate, Countable
```

**Why no arrays?**

| Arrays              | Typed Classes             |
| ------------------- | ------------------------- |
| No type safety      | Full type checking        |
| No IDE autocomplete | IDE support               |
| Runtime errors      | Compile-time errors       |
| Hard to refactor    | Easy to refactor          |
| No encapsulation    | Validation in constructor |

### Base class (Application layer of the shared context)

```php
// <source_root>/<SharedContext>/Application/Observability/Metric/BusinessMetric.php
abstract readonly class BusinessMetric
{
    public function __construct(
        private float|int $value,
        private MetricUnit $unit
    ) {}

    abstract public function name(): string;
    abstract public function dimensions(): MetricDimensionsInterface;

    public function value(): float|int { return $this->value; }
    public function unit(): MetricUnit { return $this->unit; }
}
```

### Emitter interface (Application layer)

```php
// <source_root>/<SharedContext>/Application/Observability/Emitter/BusinessMetricsEmitterInterface.php
interface BusinessMetricsEmitterInterface
{
    public function emit(BusinessMetric $metric): void;
    public function emitCollection(MetricCollection $metrics): void;
}
```

The concrete emitter (EMF or otherwise) implements this interface in the
Infrastructure layer — handlers and subscribers depend only on the
interface.

---

## Creating new business metrics

### Step 1: Create the metric class

Place it in the Application layer of the owning bounded context.

```php
// <source_root>/<Context>/Application/Metric/OrdersPlacedMetric.php
final readonly class OrdersPlacedMetricDimensions implements MetricDimensionsInterface
{
    public function __construct(
        private MetricDimensionsFactoryInterface $dimensionsFactory,
        private string $paymentMethod
    ) {
    }

    public function values(): MetricDimensions
    {
        return $this->dimensionsFactory->endpointOperationWith(
            'Order',
            'create',
            new MetricDimension('PaymentMethod', $this->paymentMethod)
        );
    }
}

final readonly class OrdersPlacedMetric extends BusinessMetric
{
    public function __construct(
        private MetricDimensionsFactoryInterface $dimensionsFactory,
        private string $paymentMethod,
        float|int $value = 1
    ) {
        parent::__construct($value, MetricUnit::COUNT);
    }

    public function name(): string
    {
        return 'OrdersPlaced';
    }

    public function dimensions(): MetricDimensionsInterface
    {
        return new OrdersPlacedMetricDimensions(
            dimensionsFactory: $this->dimensionsFactory,
            paymentMethod: $this->paymentMethod
        );
    }
}
```

Metrics that only need the standard `Endpoint`/`Operation` dimensions
can simply extend `EndpointOperationBusinessMetric` and return the
endpoint (entity/resource name) and operation (CRUD action) as
constants.

### Step 2: Create the event subscriber

```php
// <source_root>/<Context>/Application/EventSubscriber/OrderPlacedMetricsSubscriber.php
final readonly class OrderPlacedMetricsSubscriber implements DomainEventSubscriberInterface
{
    public function __construct(
        private BusinessMetricsEmitterInterface $metricsEmitter,
        private OrdersPlacedMetricFactoryInterface $metricFactory
    ) {}

    public function __invoke(OrderPlacedEvent $event): void
    {
        $this->metricsEmitter->emit($this->metricFactory->create($event->paymentMethod()));
    }

    /**
     * @return array<class-string>
     */
    public function subscribedTo(): array
    {
        return [OrderPlacedEvent::class];
    }
}
```

### Step 3: For multiple metrics — use MetricCollection

```php
// Emit multiple metrics together (factories injected via constructor)
$this->metricsEmitter->emitCollection(new MetricCollection(
    $this->ordersPlacedMetricFactory->create($event->paymentMethod()),
    $this->orderValueMetricFactory->create($event->totalAmount())
));
```

Reference layout from the canonical upstream profile:

```text # profile-example
src/Shared/Application/Observability/Metric/BusinessMetric.php          # base class
src/Shared/Application/Observability/Metric/MetricUnit.php              # unit enum
src/Shared/Application/Observability/Metric/MetricCollection.php        # metrics collection
src/Shared/Application/Observability/Emitter/BusinessMetricsEmitterInterface.php
src/Shared/Infrastructure/Observability/AwsEmfBusinessMetricsEmitter.php # EMF implementation
src/Shared/Infrastructure/Observability/EmfLogFormatter.php             # Monolog formatter
src/User/Application/Metric/UsersCreatedMetric.php                      # Endpoint=User, Operation=create
src/User/Application/EventSubscriber/UserCreatedMetricsSubscriber.php
config/packages/monolog.yaml                                            # EMF channel configuration
```

---

## AWS EMF emission (only when `capabilities.observability_emf: true`)

AWS Embedded Metric Format embeds custom metrics in structured log
events; CloudWatch automatically extracts metrics from EMF-formatted
logs written to stdout. Derive the namespace from `project.name` in
PascalCase: `<ProjectName>/BusinessMetrics`.

### EMF log structure

```json
{
  "_aws": {
    "Timestamp": 1702425600000,
    "CloudWatchMetrics": [
      {
        "Namespace": "<ProjectName>/BusinessMetrics",
        "Dimensions": [["Endpoint", "Operation"]],
        "Metrics": [{ "Name": "OrdersPlaced", "Unit": "Count" }]
      }
    ]
  },
  "Endpoint": "Order",
  "Operation": "create",
  "OrdersPlaced": 1
}
```

When this log is written via the dedicated logging channel with the EMF
formatter, CloudWatch automatically extracts `OrdersPlaced` as a metric,
associates it with the namespace, and applies the `Endpoint` and
`Operation` dimensions.

See the [CloudWatch EMF specification](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html).

### Querying after deployment

```sql
-- Total endpoint invocations by resource
SELECT SUM(EndpointInvocations)
FROM "<ProjectName>/BusinessMetrics"
GROUP BY Endpoint

-- Orders placed over time
SELECT SUM(OrdersPlaced)
FROM "<ProjectName>/BusinessMetrics"
WHERE Endpoint = 'Order'
```

Canonical upstream reference (managed AWS runtime provides the
infrastructure metrics):

```text # profile-example
Namespace: UserService/BusinessMetrics      # project.name: user-service
Endpoint=User; Operations: create (registration), update (profile), request-password-reset
Infrastructure SLO/SLA metrics come from AWS AppRunner:
https://docs.aws.amazon.com/apprunner/latest/dg/monitor-cw.html
```

## Generic metrics backends (when `capabilities.observability_emf: false`)

Keep the entire application-layer design — typed metric classes,
dimensions, `MetricCollection`, event subscribers, and
`BusinessMetricsEmitterInterface` — unchanged. Only the Infrastructure
implementation differs:

- **Prometheus/OpenMetrics**: map `BusinessMetric` to counters/gauges;
  dimensions become labels (the same cardinality rules apply).
- **StatsD/OTLP**: emit one measurement per metric with dimensions as
  tags/attributes.
- **No metrics backend**: write structured log lines (one JSON object
  per metric with name, value, unit, dimensions) through the framework's
  logging stack so a backend can be attached later without code changes.

Do not bake backend specifics into metric classes or subscribers —
swapping backends must touch only the emitter implementation and its
service wiring.

---

## Dimension best practices

### Recommended dimensions

| Dimension       | Description       | Cardinality |
| --------------- | ----------------- | ----------- |
| `Endpoint`      | API resource name | Low         |
| `Operation`     | CRUD action       | Very Low    |
| `PaymentMethod` | Payment type      | Low         |
| `UserType`      | User segment      | Low         |

### Avoid high-cardinality dimensions

**Don't use**: user IDs, order IDs, session IDs, timestamps. These
create too many unique metric streams and inflate metrics-backend costs
(CloudWatch billing, Prometheus series explosion).

## Metric naming conventions

Format: `{Entity}{Action}` in PascalCase.

| Good                | Bad                   |
| ------------------- | --------------------- |
| `OrdersPlaced`      | `orders.placed.count` |
| `PaymentsProcessed` | `payment-processed`   |

- Use PascalCase for metric names
- Use plural nouns for counters (`OrdersPlaced`, not `OrderPlaced`)
- Use past tense for completed actions

---

## Testing business metrics

### Use a spy in tests

```php
final class OrderPlacedMetricsSubscriberTest extends TestCase
{
    public function testEmitsMetricOnOrderPlaced(): void
    {
        $metricsSpy = new BusinessMetricsEmitterSpy();
        $dimensionsFactory = new MetricDimensionsFactory();
        $metricFactory = new OrdersPlacedMetricFactory($dimensionsFactory);

        $subscriber = new OrderPlacedMetricsSubscriber($metricsSpy, $metricFactory);

        ($subscriber)(new OrderPlacedEvent($orderId, 'card'));

        self::assertSame(1, $metricsSpy->count());

        foreach ($metricsSpy->emitted() as $metric) {
            self::assertSame('OrdersPlaced', $metric->name());
            self::assertSame(1, $metric->value());
            self::assertSame('Order', $metric->dimensions()->values()->get('Endpoint'));
            self::assertSame('create', $metric->dimensions()->values()->get('Operation'));
        }

        // Or use the assertion helper
        $metricsSpy->assertEmittedWithDimensions(
            'OrdersPlaced',
            new MetricDimension('Endpoint', 'Order'),
            new MetricDimension('Operation', 'create')
        );
    }
}
```

### Test service configuration

In the test service configuration (e.g. `config/services_test.yaml` for
Symfony), alias the emitter interface to the spy and mark the spy
public so tests can inspect it.

Run the suite via the target mapped by `make.tests`. Subscriber and
metric tests must assert names, values, and dimensions precisely —
weak assertions leave escaped mutants, and the mutation score must stay
at or above `quality.infection_msi` (canonical default 100; raise-only,
never lower). For failure debugging see the
[testing-workflow skill](../testing-workflow/SKILL.md).

---

## What NOT to track

When the deployment platform or an APM agent already provides
infrastructure metrics (always the case when
`capabilities.observability_emf` is true — the managed AWS runtime
supplies SLO/SLA metrics), do not duplicate them.

**Don't track**: request latency, error rates, response times, HTTP
status codes, memory usage, CPU usage.

**Do track**: business events (orders placed, accounts created),
business values (order amounts, payment totals), domain-specific
actions (logins, uploads, exports).

---

## Success criteria

- Each domain event that needs tracking has a corresponding metric
  subscriber
- Metrics use typed classes (not arrays)
- Metrics are emitted via event subscribers (not hardcoded in handlers)
- Dimensions provide meaningful, low-cardinality segmentation
- Unit tests verify metric emission (names, values, dimensions)
- No infrastructure metrics duplicated from the platform
- The full local suite mapped by `make.ci` passes at the profile's
  protected `quality.*` thresholds (raise-only — fix code, never lower
  thresholds, never add suppression annotations, never edit
  `deptrac.yaml`)

### SOLID compliance checklist

- [ ] **SRP**: each metric class defines exactly one metric type
- [ ] **SRP**: event subscriber only emits metrics (no business logic)
- [ ] **OCP**: new metrics added via new classes (no emitter changes)
- [ ] **OCP**: new event subscribers added without changing existing code
- [ ] **LSP**: all metrics properly extend the `BusinessMetric` base class
- [ ] **ISP**: `MetricDimensionsInterface` stays minimal (only `values()`)
- [ ] **DIP**: handlers depend on the event bus interface, not concrete
      metrics; subscribers depend on `BusinessMetricsEmitterInterface`,
      not the EMF/backend implementation

### Type safety checklist

- [ ] NO arrays for metric configuration — use typed classes
- [ ] NO arrays for metric collections — use `MetricCollection`
- [ ] All dimensions via `MetricDimensionsInterface` implementations
- [ ] Arrays allowed only at infrastructure boundaries (JSON
      serialization, PSR-3 log context)
- [ ] The `MetricUnit` enum used for all units
