---
name: observability-instrumentation
description: Add type-safe client-side telemetry for user-impacting frontend signals — error boundaries, captured exceptions, web-vitals, and Apollo/HTTP failures — emitted to a real RUM/Sentry sink when `capabilities.observability` is true, or through a deferred structured-log sink otherwise. Use when adding frontend telemetry, wiring Sentry error boundaries, reporting web-vitals, or instrumenting user-impacting signals for dashboards.
---

# Frontend Observability Instrumentation

## Profile keys consumed

- `capabilities.observability`
- `project.name`
- `framework.ui`
- `framework.di`
- `framework.state`
- `framework.graphql_mock`
- `architecture.source_root`
- `architecture.modules`
- `architecture.component_prefix`
- `make.ci`
- `make.lint`
- `make.test_unit_client`
- `make.lighthouse_desktop`
- `make.lighthouse_mobile`
- `quality.mutation_msi`
- `quality.coverage_statements`
- `quality.lighthouse_desktop`
- `quality.lighthouse_mobile`

All make invocations go through the profile's `make` target map. A `null`
value means the capability is absent: skip with a note, never improvise a
raw repo-specific command (generic tooling like `gh`, `bun`, `git` may
still be invoked directly when needed).

## Capability gate

`capabilities.observability` selects the emission backend; the
application-layer design is identical in both branches:

- **`true`** — emit signals to a live Real-User-Monitoring sink:
  `@sentry/react` for errors and the `web-vitals` package for performance.
  Apply every section of this skill, including
  [Live telemetry wiring](#live-telemetry-wiring-only-when-capabilitiesobservability-true).
- **`false`** — apply the same typed-event / injectable-reporter
  architecture, but implement the reporter against a deferred
  structured-log sink. `skip` the Sentry init and RUM sections (tied to
  the `capabilities.observability` predicate — SKIPPED with a note) and
  see
  [Deferred / no-sink backends](#deferred--no-sink-backends-when-capabilitiesobservability-false).

This is a frontend SPA: instrument client-side failures and
user-impacting signals only. Do **not** copy a sibling backend service's
AWS EMF / CloudWatch patterns — infrastructure metrics belong to the
platform, not the browser.

## What this skill covers

- **Error boundaries** — route-level and top-level React boundaries that
  capture exceptions through `@sentry/react`
- **Captured exceptions** — failures surfaced through existing service
  boundaries (Apollo / HTTP clients), not scattered `try/catch` in views
- **Web-vitals** — LCP, CLS, INP reported through the `web-vitals`
  package as typed signals
- **Type-safe telemetry** — concrete event classes and an injectable
  reporter instead of ad-hoc objects and direct SDK calls
- **DI + SOLID** — Single Responsibility (boundaries / reporters) +
  Open/Closed (new event classes), wired through `framework.di`

## What this skill does NOT cover

- **Infrastructure metrics** — server latency, error rates, RPS. These
  belong to the API/platform; verify what the deployment already emits
  before duplicating it client-side.
- **Backend business metrics** — order/payment KPIs emitted server-side.
  A sibling backend service owns those; never wire AWS EMF here.
- **Distributed tracing** — use the RUM provider's tracing integration
  instead of hand-rolling spans in the SPA.

## When to use

- Adding new routes or feature modules with user-facing significance (see
  the `frontend-component-development` skill)
- Adding an error boundary at a new surface (route, app shell, lazy
  chunk)
- Shipping a change that affects page load, route transitions, heavy
  rendering, or user-perceived responsiveness (pair with the
  `frontend-performance-accessibility` skill)
- Instrumenting a user-impacting signal for dashboards and product
  analytics

---

## Architecture overview

1. **Telemetry event classes** — each signal type is a concrete class
   extending `TelemetryEvent`
2. **Boundaries / reporters** — signals are emitted at error boundaries
   and a web-vitals reporter, not hardcoded inside presentational
   components
3. **Injectable reporter** — emission writes through an `@injectable()`
   reporter resolved via `framework.di` (`tsyringe`), so the SDK is
   swappable behind a token
4. **No ad-hoc objects** — all signal configuration uses typed objects
5. **Batches** — multiple signals use a typed batch, not loose arrays

Placement follows the modular `framework.ui` architecture (paths below
are relative to `architecture.source_root`): the `TelemetryEvent` base
class and the reporter **interface** live in
`<source_root>/services/observability` (a singleton service area, not a
feature module); concrete event classes and the boundaries that emit them
live in the owning module — one of `architecture.modules` — under its
feature folder. Reusable fallback UI is a `architecture.component_prefix`
component (e.g. `UIErrorFallback`). Fix placement to satisfy the layer
rules — never edit `dependency-cruiser` config or add suppression
directives to force a fit (see the `architecture` and `code-organization`
skills).

Keep telemetry **out of the critical paint path**: initialize the SDK
lazily (dynamic `import()` from the app shell), the same way the auth
composition root defers its DI container, so observability never bloats
the first-paint chunk or regresses `quality.lighthouse_mobile`.

---

## Instance methods, not free functions (SOLID)

Non-React observability code under `<source_root>/**/*.ts` obeys the
house convention: **only classes with instance methods** — no `static`
members, no standalone/free functions, no top-level arrow consts. The
reporter is an `@injectable()` class; event types are classes. React
error boundaries (`*.tsx`, including class boundaries that need
`static getDerivedStateFromError`) and hooks are exempt — they are
components by definition.

### Single Responsibility Principle (SRP)

Each class has ONE responsibility:

| Class                   | Responsibility                             |
| ----------------------- | ------------------------------------------ |
| `LcpEvent`              | Define signal name, value, context         |
| `WebVitalsReporter`     | Subscribe to web-vitals, emit signals      |
| Reporter implementation | Format and write signal output to the sink |
| `TelemetryEventBatch`   | Hold multiple signals for batched emission |

**Anti-pattern**: telemetry SDK calls scattered through presentational
components (violates SRP — a view should render, not own observability
wiring).

### Open/Closed Principle (OCP)

- **Open for extension**: add new signals via new event classes
- **Closed for modification**: don't change the reporter or existing
  event classes

```typescript
// GOOD: add a new signal by creating a new class
export class InpEvent extends WebVitalTelemetryEvent { /* ... */ }

// BAD: modify the existing reporter to special-case a new signal type
```

### Why boundaries, not presentational components

```tsx
// BAD: telemetry reached for inside a view (violates SRP, leaks the SDK)
function ProfileCard() {
  const reporter = container.resolve(TOKENS.TelemetryReporter); // wrong!
  // ...render
}

// GOOD: a dedicated error boundary owns capture
export const RouteErrorBoundary = Sentry.withErrorBoundary(RouteOutlet, {
  fallback: <UIErrorFallback />,
  beforeCapture(scope) {
    scope.setTag('surface', 'route');
  },
});
```

**Benefits**:

- Views focus on rendering only
- Emission is decoupled and testable behind the reporter token
- Easy to add/remove signals without touching feature logic
- Telemetry is resilient: a reporter failure must never break the user
  flow (wrap the sink write so an SDK error degrades to a no-op)

---

## Type-safe telemetry event hierarchy

```text
TelemetryEvent (abstract)
├── WebVitalTelemetryEvent (abstract) — signals with a metric + rating
│   └── LcpEvent / ClsEvent / InpEvent (one per web-vital)
├── RouteTransitionEvent — duration signal, no web-vital rating
└── CapturedErrorEvent (abstract) — error signals with surface context
    ├── ApolloErrorEvent
    └── HttpErrorEvent

TelemetryContext (type-only) — feature-level, low-cardinality tags
TelemetryUnit (enum) — COUNT, MILLISECONDS, SCORE, NONE
TelemetryEventBatch — typed batch implementing Iterable
```

**Why no ad-hoc objects?** Per the type-only-files convention, all
types live in dedicated `types/` files and runtime configuration uses
typed classes:

| Loose objects          | Typed classes               |
| ---------------------- | --------------------------- |
| No type safety         | Full type checking          |
| No editor autocomplete | Editor support              |
| Runtime errors         | Compile-time (`tsc`) errors |
| Hard to refactor       | Easy to refactor            |
| No encapsulation       | Validation in constructor   |

### Base class (services/observability)

```typescript
// <source_root>/services/observability/telemetry-event.ts
export abstract class TelemetryEvent {
  protected constructor(
    private readonly value: number,
    private readonly unit: TelemetryUnit,
  ) {}

  public abstract name(): string;
  public abstract context(): TelemetryContext;

  public measuredValue(): number {
    return this.value;
  }

  public measuredUnit(): TelemetryUnit {
    return this.unit;
  }
}
```

### Reporter interface (type-only file)

```typescript
// <source_root>/services/observability/types/telemetry-reporter.ts
export interface TelemetryReporter {
  report(event: TelemetryEvent): void;
  reportBatch(events: TelemetryEventBatch): void;
}
```

The concrete reporter (Sentry/RUM or deferred) implements this interface
and is registered against `TOKENS.TelemetryReporter` — boundaries and
reporters depend only on the interface, never the SDK.

---

## Creating new telemetry signals

### Step 1: Create the event class

Place it in the owning module (one of `architecture.modules`).

```typescript
// <source_root>/modules/<module>/observability/route-transition-event.ts
export class RouteTransitionEvent extends TelemetryEvent {
  public constructor(
    durationMs: number,
    private readonly route: string,
  ) {
    super(durationMs, TelemetryUnit.MILLISECONDS);
  }

  public name(): string {
    return 'RouteTransition';
  }

  public context(): TelemetryContext {
    return { surface: 'router', route: this.route };
  }
}
```

Signals that only need the standard web-vital metric/rating context can
extend `WebVitalTelemetryEvent` and return the vital name as a constant.

### Step 2: Emit at a boundary or reporter

```typescript
// <source_root>/services/observability/web-vitals-reporter.ts
@injectable()
export class WebVitalsReporter {
  public constructor(
    @inject(TOKENS.TelemetryReporter)
    private readonly reporter: TelemetryReporter,
  ) {}

  public start(): void {
    onLCP((metric) => this.reporter.report(new LcpEvent(metric.value)));
    onCLS((metric) => this.reporter.report(new ClsEvent(metric.value)));
    onINP((metric) => this.reporter.report(new InpEvent(metric.value)));
  }
}
```

Register the reporter in `dependency-injection-config.ts` against a token
in `tokens.ts`, then resolve `WebVitalsReporter` once from the app shell
(behind a dynamic `import()` so it stays off the first-paint chunk).

### Step 3: For multiple signals — use a typed batch

```typescript
// Emit several signals together
this.reporter.reportBatch(
  new TelemetryEventBatch(
    new RouteTransitionEvent(durationMs, route),
    new InpEvent(inpValue),
  ),
);
```

Reference layout from the canonical upstream profile:

```text # profile-example
src/services/observability/telemetry-event.ts            # abstract base class
src/services/observability/telemetry-unit.ts             # unit enum
src/services/observability/telemetry-event-batch.ts      # typed batch
src/services/observability/types/telemetry-reporter.ts   # reporter interface (type-only)
src/services/observability/sentry-reporter.ts            # live RUM/Sentry implementation
src/services/observability/web-vitals-reporter.ts        # web-vitals subscription
src/components/ui-error-fallback/ui-error-fallback.tsx   # UI* fallback component
src/modules/<module>/observability/route-transition-event.ts
src/config/dependency-injection-config.ts                # reporter registration
src/config/tokens.ts                                     # TOKENS.TelemetryReporter
```

---

## Live telemetry wiring (only when `capabilities.observability: true`)

Initialize `@sentry/react` once at the app entry, derive the
environment/release tags from `project.name`, and wrap the SPA in error
boundaries at every surface (app shell, each route outlet, lazy chunks).

### Sentry boundary

```tsx
import * as Sentry from '@sentry/react';

export const AppErrorBoundary = Sentry.withErrorBoundary(App, {
  fallback: <UIErrorFallback />,
  beforeCapture(scope) {
    scope.setTag('surface', 'app');
    scope.setTag('app', PROJECT_NAME); // from project.name, PascalCase
  },
});
```

### Web-vitals + service-boundary capture

- **web-vitals**: subscribe via `onLCP` / `onCLS` / `onINP` and forward
  each metric as a typed event through `WebVitalsReporter` (Step 2).
- **Apollo / HTTP errors**: capture at the existing service boundary
  (an Apollo error link or the HTTP client wrapper), mapping each failure
  to an `ApolloErrorEvent` / `HttpErrorEvent` — never log full request
  bodies or auth headers.
- **Structured mock logs**: where the local GraphQL mock
  (`framework.graphql_mock`) needs server-side logs for development, emit
  one structured JSON line per event; this never reaches the production
  RUM sink.

Capture context is feature-level and low-cardinality (see
[Context & privacy](#context--privacy-best-practices)). The `web-vitals`
signals are calibrated against the Lighthouse audit lanes mapped by
`make.lighthouse_desktop` / `make.lighthouse_mobile`; RUM data must agree
with the lab scores, and neither lane may drop below
`quality.lighthouse_desktop` / `quality.lighthouse_mobile`.

## Deferred / no-sink backends (when `capabilities.observability: false`)

Keep the entire application-layer design — typed event classes,
`TelemetryContext`, `TelemetryEventBatch`, boundaries, and the
`TelemetryReporter` interface — unchanged. Only the reporter
implementation differs:

- **Structured-log reporter**: write one JSON object per signal (name,
  value, unit, context) through the app's logger so a sink can be
  attached later without touching call sites.
- **No-op reporter**: register a reporter whose `report` is an
  intentional no-op when no logger is configured; boundaries and the
  web-vitals reporter still wire up identically.

Do not bake SDK specifics into event classes or boundaries — swapping
from the deferred reporter to a live RUM sink must touch only the
reporter implementation and its DI registration in
`dependency-injection-config.ts`.

---

## Context & privacy best practices

### Recommended context tags

| Tag        | Description                 | Cardinality |
| ---------- | --------------------------- | ----------- |
| `surface`  | app / route / chunk         | Low         |
| `route`    | route name (not URL params) | Low         |
| `module`   | feature module name         | Low         |
| `category` | error category              | Low         |

### Avoid high-cardinality / sensitive context

**Never capture**: passwords, tokens, cookies, auth headers, raw form
values, full API payloads, or user-entered text. Avoid or minimize user
identifiers. High-cardinality tags (user IDs, session IDs, timestamps,
full URLs with params) explode RUM event streams and inflate cost — and
leaking PII is a privacy violation, not just a cost problem.

Telemetry must be **resilient**: an observability failure must never
break a user flow. Wrap every sink write so an SDK error degrades to a
silent no-op.

## Signal naming conventions

Format: `{Subject}{Action}` or the vital name, in PascalCase.

| Good                  | Bad                   |
| --------------------- | --------------------- |
| `RouteTransition`     | `route.transition.ms` |
| `ApolloError`         | `apollo-error`        |
| `LCP` / `CLS` / `INP` | `largest_paint`       |

- Use PascalCase for signal names
- Use the standard web-vitals acronyms for those metrics
- Use past tense for completed actions (`UserRegistered`)

---

## Testing telemetry

### Use a reporter spy via the DI container

```typescript
import 'reflect-metadata';
import { container } from 'tsyringe';

describe('WebVitalsReporter', () => {
  it('reports each web-vital as a typed event', () => {
    const reporterSpy = new TelemetryReporterSpy();
    container.registerInstance(TOKENS.TelemetryReporter, reporterSpy);

    container.resolve(WebVitalsReporter).start();
    // ...drive the web-vitals callbacks with seeded Faker values

    expect(reporterSpy.reported()).toHaveLength(3);
    expect(reporterSpy.reported()[0].name()).toBe('LCP');
    expect(reporterSpy.reported()[0].context().surface).toBe('app');
  });
});
```

Locate fallback UI by user-facing semantics (`getByRole`,
`getByText`) — the source ships no `data-testid`. Beware that
`container.clearInstances()` in `afterEach` discards instances captured
at module load; re-register the spy per test rather than clearing a
module-level singleton.

### Test reporter wiring

Register the reporter spy against `TOKENS.TelemetryReporter` in the test
setup and assert it captured the expected signals. Error-boundary tests
render the boundary, throw from a child, and assert the fallback renders
and the spy captured one `CapturedErrorEvent` with the right `surface`.

Run the client suite via the target mapped by `make.test_unit_client`.
Reporter and event tests must assert names, values, and context
precisely — weak assertions leave escaped mutants, and the mutation
score must stay at or above `quality.mutation_msi` (default = the
`stryker.config.mjs` `break` threshold; raise-only, never lower).
Coverage stays at `quality.coverage_statements` (default 100). For
failure debugging see the `frontend-testing-workflow` skill; fixes route
through the `react-implementer` agent.

Pair the `web-vitals` signals with the Lighthouse audit so lab and field
agree:

```bash
make lighthouse-desktop   # target mapped by make.lighthouse_desktop
make lighthouse-mobile    # target mapped by make.lighthouse_mobile
```

Use browser verification for runtime-only telemetry paths that unit
tests cannot prove (the `accessibility-auditor` agent's live-browser
probing exercises the same rendered surfaces).

---

## What NOT to track

When the platform or an APM agent already provides infrastructure
metrics, do not duplicate them in the browser.

**Don't track**: server request latency, error rates, response times,
HTTP status distributions, memory/CPU usage, backend business KPIs.

**Do track**: client-side failures (uncaught errors, Apollo/HTTP
failures surfaced at boundaries), user-perceived performance (LCP, CLS,
INP, route-transition timing), and user-impacting domain events.

---

## Success criteria

- Each user-impacting failure surface has an error boundary that captures
  through the reporter
- Web-vitals (LCP, CLS, INP) are reported as typed signals
- Signals use typed event classes (not ad-hoc objects)
- Emission happens at boundaries / reporters (not inside presentational
  components)
- Context tags are meaningful, low-cardinality, and PII-free
- Telemetry is resilient — a reporter failure degrades to a no-op
- Unit tests verify emission (names, values, context) via a reporter spy
- No infrastructure metrics duplicated from the platform
- The full local suite mapped by `make.ci` passes at the profile's
  protected `quality.*` thresholds (raise-only — fix code, never lower
  thresholds, never add `eslint-disable` / `@ts-ignore`, never edit the
  dependency-cruiser config)

### SOLID compliance checklist

- [ ] **SRP**: each event class defines exactly one signal type
- [ ] **SRP**: boundaries/reporters only emit signals (no view logic)
- [ ] **OCP**: new signals added via new classes (no reporter changes)
- [ ] **OCP**: new boundaries added without changing existing code
- [ ] **LSP**: all events properly extend `TelemetryEvent`
- [ ] **ISP**: `TelemetryReporter` stays minimal (`report`/`reportBatch`)
- [ ] **DIP**: boundaries/reporters depend on `TelemetryReporter`, not
      the `@sentry/react` / `web-vitals` SDK directly

### Type safety & convention checklist

- [ ] NO ad-hoc objects for signal configuration — use typed classes
- [ ] NO loose arrays for batches — use `TelemetryEventBatch`
- [ ] All context via the type-only `TelemetryContext` type
- [ ] No `static` members or free functions in `<source_root>/**/*.ts`
      observability code — instance methods on an injectable class
- [ ] The `TelemetryUnit` enum used for all units
- [ ] Types live in dedicated type-only files; logic files import them
      with `import type`

### Privacy checklist

- [ ] No tokens, passwords, cookies, or auth headers captured
- [ ] No raw form values or full API payloads
- [ ] User identifiers avoided or minimized
- [ ] Context is feature-level unless more detail is genuinely necessary
- [ ] Telemetry failure cannot block the user flow

Before applying this skill, confirm the active task against
[../AI-AGENT-GUIDE.md](../AI-AGENT-GUIDE.md) and
[../SKILL-DECISION-GUIDE.md](../SKILL-DECISION-GUIDE.md) so every relevant
skill is consulted and every verdict recorded.
