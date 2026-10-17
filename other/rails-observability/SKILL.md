---
name: rails-observability
description: Use when implementing or reviewing Rails request lifecycle, API error handling, request IDs, logging, Rails.error, ActiveSupport::Notifications, health checks, or production diagnostics.
license: MIT
---

# Rails Request Lifecycle & Observability

## Purpose
Treat a Rails request as an observable contract: routing, middleware, controller/domain work, persistence/external calls, response, logging, instrumentation, and error reporting.

Primary references:
- https://guides.rubyonrails.org/action_controller_overview.html
- https://guides.rubyonrails.org/error_reporting.html
- https://guides.rubyonrails.org/active_support_instrumentation.html
- https://guides.rubyonrails.org/configuring.html
- https://guides.rubyonrails.org/debugging_rails_applications.html

## Activate when
- changing controller request/response behavior
- designing API error responses or exception mappings
- adding `rescue_from`
- changing request IDs or correlation
- changing logging, log tags, or parameter filtering
- adding `Rails.error` reporting
- adding `ActiveSupport::Notifications` events/subscribers
- adding structured event reporting with `Rails.event`
- changing health/liveness/readiness endpoints
- modifying middleware affecting request observability
- diagnosing production request failures

## Repository inspection
Resolve Ruby/Rails version first. Inspect routes, ApplicationController, controller hierarchy, config/environments, config/initializers, logger/formatter, log_tags, filter_parameters, Rails.error subscribers, Notifications subscribers, middleware ordering, health routes, auth boundaries, and existing metrics/tracing/error integrations.

Do not invent a new error or log format before inspecting repository conventions.

## Request lifecycle
Reason about:
```text
request -> router -> middleware -> before_action -> action -> render/redirect -> response
```
Lifecycle and callback details are version-sensitive; use the target Rails version as authority.

Keep cross-cutting concerns in their owning boundary instead of duplicating them in controllers.

## HTTP error contract
For APIs define success, validation, authentication, authorization, not-found, conflict/domain failures, unexpected 5xx behavior, content type, and correlation identifier.

Use narrow exception mappings such as `rescue_from` when they match repository conventions.

Never rescue StandardError broadly and return success. Never expose backtraces, internal exception details, credentials, or sensitive payloads to clients.

Keep the external error schema stable even if internal exception classes change.

## Rails.error
Rails provides a standard error reporter with `Rails.error.handle`, `record`, and `report`, plus subscribers implementing `report`.

Use explicit reporting when a handled condition still needs operational visibility. Do not swallow an exception just because it was reported.

Choose severity based on operator action and impact. Expected 404/validation conditions should not automatically become incident-level error signals.

Useful context may include request ID, controller/action, job ID, tenant/account identifier when permitted, dependency name, and deployment metadata.

Never put passwords, access tokens, session secrets, authorization headers, or unnecessary sensitive payloads into error context.

Reference: https://guides.rubyonrails.org/error_reporting.html

## Request IDs and correlation
Rails provides request IDs through ActionDispatch::RequestId and exposes the request UUID and response header.

Preserve one correlation chain:
```text
HTTP request -> logs -> database context -> job enqueue -> job execution -> external call
```
Reuse repository conventions instead of generating unrelated IDs in each layer.

Reference: https://guides.rubyonrails.org/configuring.html

## Logging
Rails supports log tags and TaggedLogging. Use them for request ID and other bounded correlation fields.

Useful request log fields include timestamp, request/job ID, operation, status, duration, failure class, and permitted actor/tenant context.

Use config.filter_parameters for sensitive fields. Do not log complete request bodies by default. Avoid uncontrolled user strings as metrics dimensions.

References:
- https://guides.rubyonrails.org/configuring.html
- https://guides.rubyonrails.org/debugging_rails_applications.html

## ActiveSupport::Notifications
Use ActiveSupport::Notifications for meaningful application/framework events. Rails exposes events such as controller processing and database activity.

Example:
```ruby
ActiveSupport::Notifications.instrument("checkout.completed", order_id: order.id) do
  checkout.call
end
```

Use stable `event.library` names, minimal payloads, and side-effect-free subscribers. Instrument boundaries, not every method.

Reference: https://guides.rubyonrails.org/active_support_instrumentation.html

## Metrics
Prefer low-cardinality dimensions such as operation, controller/action, status class, and dependency name.

Do not use request IDs, raw URLs containing arbitrary identifiers, or user-generated strings as metric labels.

## Health checks
Current Rails generated applications include a built-in `/up` health endpoint. It indicates that the application booted without exceptions; it is not a full dependency-health check.

When adding application-specific health/readiness checks, explicitly separate:
```text
liveness   = process should stay running
readiness  = instance can serve traffic
dependency = a specific dependency is available
```

Do not make liveness depend on every third-party service unless that restart policy is intentional.

A health endpoint reachable from outside the application should report pass or fail without naming which dependency failed: enumerating failures exposes topology, and a probe that fans out to every dependency converts a partial outage into a full one under polling.

Reference: https://guides.rubyonrails.org/action_controller_overview.html

## Middleware
When changing middleware inspect stack order, request-ID availability, exception interception, instrumentation order, and security interactions. Test success and failure paths.

Do not add middleware merely because it is convenient.

## Ownership map
```text
input validation       -> controller/model boundary
domain failure          -> domain/application layer
HTTP exception mapping  -> controller/rescue_from
global error reporting  -> Rails.error subscriber
request metrics         -> instrumentation
global request concern  -> middleware/framework configuration
```

## Debugging procedure
```text
1. identify request/job ID
2. locate ingress/request log
3. correlate controller/action
4. inspect status and duration
5. inspect error report
6. inspect instrumentation events
7. inspect DB/dependency calls
8. inspect job enqueue/perform when async
9. compare runtime/deployment versions
10. reproduce at the narrowest failing boundary
```

Do not respond to a production incident by adding random logs to every method.

## Testing
At the request boundary, test the applicable contract: response status/body, exception mapping, request ID propagation, parameter filtering, health status, instrumentation events, error reporting, and structured logging where it is an operational contract.

Prefer structured assertions over brittle full-log snapshots.

## Agent review checklist
- [ ] runtime/version resolved
- [ ] existing HTTP error contract inspected
- [ ] 4xx/5xx semantics are explicit
- [ ] request correlation is preserved
- [ ] sensitive data is filtered
- [ ] error severity is justified
- [ ] instrumentation names/payloads are stable
- [ ] metric dimensions are bounded
- [ ] middleware ordering is understood
- [ ] health/readiness semantics are explicit
- [ ] tests cover the touched operational behavior

## Anti-patterns
- rescue StandardError and return 200
- expose exception details to clients
- log credentials or full request payloads
- use request IDs as metric labels
- instrumentation subscribers that mutate domain state
- liveness coupled to every dependency
- duplicate error formatting in every controller
- swallow failures after reporting them

## Verification
Never claim production observability is complete from a passing controller test alone. Verify the request boundary, failure behavior, correlation, filtering, instrumentation, and health semantics actually changed.

## Rails 8.1 current framework considerations

- Rails 8.1 adds structured Event Reporting through `Rails.event`. Treat structured events as an explicit operational contract rather than parsing human-oriented log text.
- Keep event payloads bounded, correlation-aware, and free of secrets or sensitive request data; continue to use the owning instrumentation/error boundary for durable application telemetry.

## Source foundation

Primary Rails guidance:
- Action Controller Overview: https://guides.rubyonrails.org/action_controller_overview.html
- Error Reporting in Rails Applications: https://guides.rubyonrails.org/error_reporting.html
- Active Support Instrumentation: https://guides.rubyonrails.org/active_support_instrumentation.html
- Configuring Rails Applications: https://guides.rubyonrails.org/configuring.html
- Debugging Rails Applications: https://guides.rubyonrails.org/debugging_rails_applications.html

Use the target Rails version as the compatibility authority when request lifecycle, controller, middleware, error-reporting, or health behavior differs across releases.

## Rails request lifecycle/observability changes

For request and production-diagnostics changes:
- resolve Rails version first;
- inspect existing HTTP error, logging, request-ID, and health conventions;
- keep exception-to-response mappings narrow;
- preserve correlation identifiers across request/job/dependency boundaries;
- filter sensitive data before logs/error context;
- use Rails.error for error reporting and ActiveSupport::Notifications for meaningful instrumentation;
- keep instrumentation subscribers observational;
- distinguish liveness from readiness and dependency health;
- verify request/error/health contracts with focused tests.
