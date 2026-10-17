---
name: rails-rack-middleware-engineering
description: Design and review Rack and Rails middleware as explicit request/response, ordering, failure, security, observability, and concurrency boundaries.
license: MIT
---
# Rails Rack / Middleware Engineering

## Purpose

Use this skill when a Rails change crosses the Rack middleware stack or introduces, removes, reorders, or modifies middleware. Treat middleware as infrastructure around the Rails application boundary, not as an alternative application/service layer.

## Activate when

Activate for:

- Rack middleware and `call(env)`
- `config.middleware`, `insert_before`, `insert_after`, `swap`, `delete`, and stack inspection
- custom Rack middleware
- request/response wrapping or short-circuiting
- request IDs, correlation, logging, tracing, metrics, and instrumentation at the Rack boundary
- proxy, host, SSL, CORS, compression, static-file, or rate-limit middleware
- middleware exception propagation or rescue behavior
- middleware thread/fiber safety
- production middleware ordering or environment-specific stacks
- middleware performance and allocation regressions
- Rack-level integration and contract tests

Do not activate merely because a controller, model, job, or service happens to run during a request.

## Core contract

A Rack application is invoked with an environment and returns a three-part response:

`[status, headers, body]`

Middleware wraps an application and must preserve the Rack contract unless it deliberately terminates the request with a valid response. The stack is ordered composition: placement changes behavior.

Treat these as separate responsibilities:

- **Rack boundary** — environment, response shape, body lifecycle, stack composition.
- **Middleware** — cross-cutting transport/infrastructure behavior.
- **Rails controller/application layer** — authentication, authorization, business rules, resource semantics.
- **Observability** — correlation and telemetry semantics that should remain consistent across request boundaries.
- **Security engineering** — trust boundaries and threat analysis.
- **Reliability engineering** — capacity, overload, failure containment, and dependency behavior.

## Repository inspection

Before changing middleware:

1. Resolve Ruby, Rails, and Rack versions from repository evidence.
2. Inspect `config/application.rb`, environment configs, initializers, `config.ru`, and any engine/railtie configuration.
3. Inspect the actual middleware stack in development, test, and production where relevant.
4. Search for existing middleware classes and their registration order.
5. Identify proxy/load-balancer, server, CDN, and platform headers that affect the boundary.
6. Inspect request-ID, logging, tracing, security, CORS, compression, static-file, and rate-limit conventions before adding another mechanism.
7. Inspect tests that assert headers, redirects, status codes, exceptions, or request context.
8. Inspect deployment/runtime differences before assuming the same stack exists in every environment.

Useful evidence includes `bin/rails middleware`, `config.middleware`, environment-specific configuration, and focused integration/system tests.

## Stack ordering

Middleware order is part of the runtime contract.

Reason explicitly about:

- what must execute before the Rails application
- what must observe the response after downstream processing
- which middleware must see authenticated or unauthenticated requests
- exception handling and whether a given layer can observe failures
- request-ID/correlation initialization before logs and traces consume it
- security controls before untrusted work
- compression/caching after the response representation is known
- proxy/header normalization before consumers trust those values

Never reorder middleware only to make the stack visually simpler. Record the behavioral dependency when order matters.

## Custom middleware design

A custom middleware should:

1. Have one clearly named cross-cutting responsibility.
2. Accept the downstream application through `initialize(app, ...)`.
3. Implement `call(env)` without owning domain state.
4. Use Rack environment keys deliberately and avoid collisions.
5. Return a valid response or explicitly delegate downstream.
6. Preserve response headers and body semantics when wrapping a response.
7. Avoid hidden global mutable state.
8. Keep configuration explicit and immutable after boot where possible.
9. Emit bounded, structured telemetry rather than logging sensitive request data.
10. Be independently testable at the Rack boundary.

Prefer an existing Rails/Rack middleware when it already satisfies the repository contract. Do not create a custom middleware to hide controller authorization or business invariants.

## Short-circuiting

Short-circuit only when the middleware owns the decision.

A short-circuit response must define:

- status
- required headers
- body type and lifecycle
- whether downstream execution is intentionally skipped
- logging/telemetry behavior
- security implications
- cache semantics

Examples include an intentionally rejected request, a static response owned by infrastructure, or a bounded rate-limit response. A middleware must not silently swallow downstream work that another layer owns.

## Exceptions and failure propagation

Do not use middleware as a generic exception sink.

Before rescuing an exception, determine:

- which layer owns classification
- whether Rails error handling should observe it
- whether the client response must differ by environment
- whether telemetry will still capture the failure
- whether retries or upstream behavior depend on the status

Preserve the original exception unless the middleware is explicitly responsible for translating it. Avoid broad rescue clauses that turn programmer errors into false-success responses.

## Request context and observability

Request identifiers and correlation metadata should be initialized once and propagated consistently.

- Reuse the repository's request-ID/correlation mechanism.
- Do not create parallel IDs for the same request without a documented purpose.
- Never trust client-supplied identity fields as authenticated identity.
- Keep secrets, credentials, cookies, and sensitive payloads out of logs.
- Ensure timing/metrics include short-circuited and exceptional paths when those paths matter operationally.
- Preserve downstream trace/correlation context according to the repository's telemetry contract.

## Security boundaries

Middleware can enforce transport-level or infrastructure-level controls such as:

- trusted-host validation
- HTTPS/security headers
- CORS policy where the middleware is the established owner
- request-size or rate limits
- proxy/header normalization
- static/public resource controls

Do not move resource authorization, tenant ownership, or business permission checks into generic middleware merely because middleware runs early. Those decisions belong at the authenticated resource/action boundary unless a repository-specific architecture explicitly assigns otherwise.

Treat forwarded headers and proxy metadata as untrusted until the deployment's trusted-proxy contract establishes which values are authoritative.

## Concurrency and lifecycle

Middleware instances can be reused across requests. Do not assume per-request instance state.

- Keep request-specific state local to `call`.
- Protect or eliminate shared mutable state.
- Do not use class variables or global collections as an implicit request store.
- Review thread and fiber safety under the actual server/runtime configuration.
- Ensure response bodies are not leaked or double-closed when wrapping downstream bodies.
- Make shutdown and resource ownership explicit for middleware that opens external resources.

## Performance

Middleware sits on the hot request path.

Measure before optimizing. Review:

- allocations per request
- synchronization contention
- body buffering
- header copying
- repeated parsing
- external calls
- logging volume
- compression and large-response behavior
- work performed for requests that will be rejected later

Do not introduce middleware that performs database or network work for every request without evidence and explicit capacity analysis.

## Testing strategy

Use the narrowest executable boundary that proves the contract:

- Rack request tests for custom middleware behavior
- integration/request tests for Rails stack composition and headers
- system tests for user-visible browser behavior
- concurrency tests for shared-state hazards
- failure-path tests for exception propagation and short-circuiting
- stack inspection tests when ordering is itself a contract

At minimum test:

- normal delegation
- short-circuit behavior when applicable
- response/status/header preservation
- body lifecycle
- exception behavior
- request context/correlation
- security-sensitive headers or trusted-proxy behavior
- environment-specific registration when applicable

## Anti-patterns

Avoid:

- middleware for domain authorization
- middleware that silently mutates unrelated response semantics
- broad exception swallowing
- request state in global/class mutable variables
- trusting arbitrary forwarded headers
- duplicated request-ID systems
- unbounded in-memory rate-limit state in multi-process deployments
- network/database work on every request without capacity evidence
- environment-specific stack changes with no test coverage
- assuming middleware order is cosmetic
- claiming thread safety without exercising the shared state
- Do not use middleware to compensate for a missing application-layer abstraction

## Reference example

A middleware that observes the environment and decorates the response without touching the app it wraps.

```ruby
# lib/middleware/tenant_header.rb
class TenantHeader
  def initialize(app)
    @app = app
  end

  def call(env)
    status, headers, body = @app.call(env)
    headers["X-Tenant"] = env["app.tenant"].to_s if env["app.tenant"]
    [status, headers, body]
  end
end

# config/application.rb
#   config.middleware.insert_after Rack::Runtime, TenantHeader
#
# Contract: middleware must not raise on missing env keys, must not buffer large
# response bodies, and must return the exact [status, headers, body] triple.
```

## Agent review checklist

- [ ] Ruby, Rails, and Rack versions resolved
- [ ] actual middleware stack inspected
- [ ] ordering dependencies documented
- [ ] Rack response/body contract preserved
- [ ] short-circuit and exception ownership explicit
- [ ] request state is concurrency-safe
- [ ] proxy/header trust assumptions verified
- [ ] domain authorization remains at the resource/action boundary
- [ ] focused Rack and stack tests exist
- [ ] production/runtime differences considered

## Verification

Before reporting completion:

1. Confirm the intended middleware stack and order.
2. Run the focused Rack/request/system tests.
3. Exercise short-circuit and exception paths where applicable.
4. Verify headers and body behavior.
5. Verify concurrency/shared-state behavior for stateful middleware.
6. Run the repository's normal regression suite for behavior changes.
7. Inspect the final diff for unnecessary stack changes.
8. Record exact verification evidence; do not claim middleware correctness from static inspection alone.

## Source foundation

- Rack SPEC: https://rack.github.io/rack/3.2/SPEC_rdoc.html
- Rails Configuration guide: https://guides.rubyonrails.org/configuring.html
- Rails Security guide: https://guides.rubyonrails.org/security.html
- Rails Testing guide: https://guides.rubyonrails.org/testing.html

## Related skills

- rails-observability
- rails-security-engineering
- rails-security
- rails-reliability-engineering
- rails-production-runtime
- rails-performance
- rails-routing
- rails-action-controller
- rails-test-engineering
- ruby-concurrency
- ruby-runtime-compatibility

## Rails Rack/middleware changes

Review middleware ordering explicitly before changing the stack.

For Rack and middleware changes:
- resolve Ruby, Rails, Rack, server, and proxy/runtime versions before implementation;
- inspect the actual middleware stack in relevant environments and use `bin/rails middleware` or equivalent evidence;
- treat middleware order as behavior, not formatting;
- keep custom middleware narrowly cross-cutting and out of domain authorization/business-rule ownership;
- preserve the Rack `[status, headers, body]` contract and body lifecycle;
- make short-circuit responses explicit about downstream execution, headers, telemetry, and security;
- preserve intentional exception ownership and do not use broad middleware rescue as a generic error sink;
- keep request state local and review shared state for thread/fiber/process safety;
- reuse the repository's authoritative request-ID/correlation and telemetry mechanisms;
- treat forwarded/proxy headers as untrusted until the deployment trust boundary establishes their authority;
- ensure rate limiting accounts for worker/process/instance topology and bounded shared state;
- test middleware directly and test registration/order when stack composition is contractual;
- verify environment-specific stacks and production proxy behavior where relevant;
- report measured verification evidence rather than claiming correctness from static inspection.
