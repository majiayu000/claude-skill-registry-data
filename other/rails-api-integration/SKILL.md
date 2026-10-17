---
name: rails-api-integration
description: Use when designing, implementing, reviewing, or debugging Rails API contracts and external integrations across inbound HTTP, outbound HTTP clients, webhooks, versioning, idempotency, retries, rate limits, serialization, and failure boundaries.
license: MIT
---

# Rails API & Integration Architecture

## Purpose

Treat every API or integration as a compatibility boundary with explicit contracts for inputs, outputs, errors, authentication, retries, idempotency, observability, and evolution.

Core flow:

classify boundary
-> inspect existing contract
-> define wire contract
-> isolate transport
-> validate at the boundary
-> normalize external data
-> execute domain behavior
-> map result/errors
-> test failure and replay behavior
-> observe
-> evolve compatibly

Compose this skill with the repository's routing, controller, authentication, security, observability, Active Job, Ruby API, HTTP, and dependency-injection skills.

## Activate when

- designing or changing a JSON/REST API contract;
- adding API versioning or deprecation;
- changing serialization/content negotiation;
- implementing outbound HTTP clients;
- adding HTTP timeout/retry/backoff behavior;
- handling rate limits;
- consuming webhooks or provider callbacks;
- verifying webhook signatures;
- making webhook processing replay-safe;
- adding idempotency keys to mutations;
- normalizing third-party errors;
- adding provider adapters;
- changing integration authentication;
- adding API contract/integration tests;
- reviewing compatibility, failure, replay, or rollout behavior.

Do not activate merely because a controller returns JSON. Use the smallest relevant integration skill.

## Repository inspection

Inspect:

1. Ruby/Rails versions;
2. routes, namespaces, and API versioning convention;
3. serializers/presenters/responders;
4. authentication and authorization;
5. request/response/error conventions;
6. HTTP client and adapter dependencies;
7. timeout/retry/rate-limit configuration;
8. webhook routes, signature verification, and event identity;
9. idempotency/deduplication storage;
10. Active Job conventions;
11. request IDs/correlation IDs and logging;
12. API schemas/OpenAPI artifacts when present;
13. request/contract/integration tests;
14. provider quotas and delivery semantics when documented.

Never invent a second API, auth, or versioning convention when the repository already has one.

## Boundary classification

Classify the boundary before designing it:

### Inbound API
The application owns the wire contract and clients depend on it.

### Outbound integration
A provider owns the wire protocol; the application owns an adapter and normalized internal contract.

### Webhook
A provider initiates an untrusted request; authenticity, replay resistance, and duplicate delivery are primary concerns.

### Internal service API
Multiple owned applications depend on a contract; compatibility and rollout sequencing matter.

### Asynchronous integration
Delivery timing, retries, queueing, and eventual completion become part of correctness.

## API contract design

Define explicitly:

- request/response media types;
- required and optional fields;
- types and nullability;
- status codes;
- error shape;
- pagination;
- authentication expectations;
- authorization behavior;
- versioning/deprecation;
- idempotency for mutations.

Prefer a small stable wire contract over exposing internal Active Record attributes.

Do not return third-party payloads directly from an owned API when the provider schema is not part of your public contract.

## Compatibility

Potentially breaking changes include removing/renaming fields, changing field types/nullability, changing status semantics, changing pagination semantics, making optional input required, changing authentication requirements, or narrowing accepted values.

Classify compatibility impact before implementation. Inspect callers and rollout order.

Never call a change backward compatible merely because the server still boots.

## API versioning

Version only a real contract boundary.

Use the repository's established mechanism:

- URL namespace;
- media type;
- headers;
- separate application boundary.

When a version changes:

1. identify the behavior that actually differs;
2. isolate the version boundary;
3. keep shared domain behavior shared where safe;
4. test old and new contracts while they coexist;
5. document deprecation/removal;
6. migrate consumers before removing old behavior.

Do not duplicate the entire domain for a representation change.

Use the `api-contract-versioning` pattern.

## Serialization and normalization

Inbound:

request
-> parse
-> validate
-> authenticate
-> authorize
-> normalize
-> domain operation

Outbound:

domain result
-> explicit presentation mapping
-> stable JSON
-> HTTP response

Provider response:

provider payload
-> validate
-> normalize
-> internal result/object
-> domain behavior

Keep provider field names at the adapter boundary unless they are intentionally part of the domain.

## Error contracts

Separate transport, protocol, domain, authorization, and configuration failures.

Map each failure to an explicit application contract.

Do not rescue `StandardError` and return one generic response for every failure.

Do not expose credentials, authorization headers, or sensitive upstream bodies in errors.

## Outbound HTTP clients

The client boundary should own base URL, authentication, headers, timeout, serialization, status classification, response parsing, provider-error translation, retry policy, rate-limit handling, and safe correlation metadata.

Keep raw HTTP calls out of controllers/models.

Inject the transport when replacement/isolation matters so tests do not require a live network.

Use the `resilient-http-client` pattern.

## Timeout and retry policy

Every outbound call needs bounded failure behavior.

A timeout is not automatically retryable.

Retry only when the operation is safe to replay or an idempotency mechanism exists, the failure is plausibly transient, the retry budget is finite, and provider limits permit it.

Usually retryable: connection reset, timeout, selected 5xx, and provider throttling when provider semantics allow.

Usually not retryable: malformed request, authentication/authorization failure, validation failure, unsupported endpoint, deterministic domain rejection.

Use finite exponential backoff with jitter when justified.

Never use unbounded retries or retry an ambiguous non-idempotent mutation without deduplication.

## Rate limits

Inspect provider quotas, burst/sustained limits, Retry-After, response headers, and concurrent-request limits.

Coordinate with `ruby-concurrency` and `rails-performance`.

Do not solve rate limits by blindly increasing concurrency or retries.

## Idempotency

For every mutation ask: "Can the same logical request arrive twice?"

If yes, define idempotency key, key scope, request fingerprint, durable storage, replay/result semantics, concurrent duplicate behavior, and retention/expiry.

Reject key reuse with different request semantics when required.

Idempotency is not the same as uniqueness validation. Use the `idempotent-request` pattern.

## Webhook ingestion

Treat webhooks as untrusted inbound integrations:

receive
-> verify authenticity
-> validate envelope
-> derive event identity
-> deduplicate
-> persist receipt state
-> enqueue/process
-> acknowledge according to provider semantics

Verify the signature over the representation required by the provider.

Do not mark an event processed before required durable state exists.

Assume duplicate, delayed, and retried delivery. If processing is asynchronous, distinguish "accepted" from "domain work completed".

Use the `webhook-ingestion` pattern.

## Webhook ordering

Do not assume delivery order unless the provider guarantees it.

Where ordering matters, model event sequence/version and define behavior for stale or future events.

## Integration authentication

Provider mechanisms may include API keys, bearer tokens, OAuth, mTLS, signed requests, or provider-specific HMAC.

Use the repository's secret/configuration system.

Never log raw authorization headers or secret material.

Webhook authenticity is not the same as end-user authorization.

## Contract testing

Inbound tests: request schema, authentication, authorization, status, response shape, and error shape.

Outbound tests: method/path/headers/body, success normalization, non-success mapping, malformed response, timeout/retry behavior.

Webhook tests: valid signature, invalid signature, duplicate event, malformed event, and retry/replay behavior.

Prefer focused wire-boundary tests over reproducing the whole application for every integration failure.

## Observability

Propagate correlation where applicable across:

inbound request
-> domain operation
-> outbound dependency
-> webhook/job

Record safe structured metadata such as provider, operation, status class, latency, retry count, request/correlation ID, and non-secret idempotency identifiers.

Do not log credentials, signatures, authorization headers, or unnecessary raw payloads.

Use `rails-observability` for the logging/instrumentation contract.

## Rollout compatibility

Consider old/new clients, old/new webhook processors, and old/new queued payloads during rolling deployment.

For provider migrations, isolate provider-specific behavior behind an adapter instead of spreading conditionals through the domain.

## References

Load only when needed; the reference is one level deep. Consult a listed pattern only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change adds or alters a `graphql-ruby` schema, type, field, mutation, resolver, or data source | [references/graphql.md](references/graphql.md) | Schema as contract; object, field, mutation, and list authorization; Dataloader batching; query depth and complexity limits; transport and verification | none |

## Reference example

An external client whose timeout is explicit, whose failure is a typed error, and whose retry/idempotency policy lives at the transport layer.

```ruby
class ExternalBillingClient
  TIMEOUT = 5.seconds

  def initialize(transport:)
    @transport = transport
  end

  def charge(order)
    @transport.post("/charges", timeout: TIMEOUT) do |request|
      request.headers["Idempotency-Key"] = "order-#{order.id}"
      request.body = { order_id: order.id, amount_cents: order.total_cents }
    end
  end

  def charge!(order)
    response = charge(order)
    raise ApiError.new(:provider_declined, :unprocessable_entity) unless response.success?

    response
  end
end

# Controllers depend on the typed error, not on transport exceptions:
#   rescue_from ApiError -> { |e| render json: { error: e.code }, status: e.status }
```

## Agent review checklist

- [ ] boundary classified
- [ ] existing route/version/auth conventions inspected
- [ ] request/response/error contract explicit
- [ ] compatibility impact classified
- [ ] external schema validated before domain use
- [ ] provider schema normalized at one boundary
- [ ] outbound timeout bounded
- [ ] retryability classified
- [ ] retry budget bounded
- [ ] mutation idempotency considered
- [ ] provider rate limits considered
- [ ] webhook authenticity verified
- [ ] webhook replay/deduplication handled
- [ ] errors mapped at the correct boundary
- [ ] secrets excluded from logs/errors
- [ ] correlation propagated where applicable
- [ ] failure-path contract tests exist
- [ ] rollout compatibility considered

## Anti-patterns

- raw HTTP scattered through controllers/models;
- exposing third-party payloads directly;
- unbounded retries;
- retrying ambiguous non-idempotent mutations;
- API versioning without a real contract difference;
- duplicating the whole domain per API version;
- accepting webhooks before signature verification;
- assuming exactly-once webhook delivery;
- marking webhook work complete before durable receipt state;
- one generic `rescue StandardError` for integration failures;
- retry loops without deadline/budget;
- provider-specific fields leaking into the domain;
- logging secrets or sensitive payloads;
- tests that never exercise the actual wire contract.

## Verification

Verify the smallest owning boundary:

```
public API
-> request/contract tests
-> failure-path tests

external client
-> fake-transport tests
-> provider contract/integration tests where available

webhook
-> signature/replay/idempotency tests
-> async processing tests when applicable
```

Report boundary, contract, failure modes tested, replay/idempotency, authn/authz, observability, and rollout compatibility.

Never claim provider interoperability merely because a fake transport test passes.

## Source foundation

- Rails Action Controller Overview: https://guides.rubyonrails.org/action_controller_overview.html
- Rails API-only applications: https://guides.rubyonrails.org/api_app.html
- Rails Testing Applications: https://guides.rubyonrails.org/testing.html
- Ruby documentation: https://ruby-doc.org/
- Repository foundations: rails-routing, rails-action-controller, rails-authentication, rails-security, rails-observability, rails-active-job, ruby-api-design, ruby-gems-io-services, ruby-dependency-injection

## Rails API and integration changes

For API and integration changes:
- classify the boundary as inbound API, outbound provider, webhook, internal API, or asynchronous integration;
- resolve Rails/Ruby versions and existing routing, versioning, serializer, authentication, security, and error conventions;
- treat inbound and third-party payloads as untrusted;
- define request/response/error contracts explicitly;
- classify changes as additive or breaking before implementation;
- isolate provider-specific schemas behind adapters rather than leaking them into the domain;
- require bounded network timeouts for outbound HTTP;
- classify retryable versus permanent failures and never use unbounded retries;
- never retry ambiguous non-idempotent mutations without an idempotency mechanism;
- verify webhook authenticity before domain processing and make duplicate/replay behavior explicit;
- make idempotency key scope, persistence, fingerprinting, and duplicate-result semantics explicit;
- preserve correlation identifiers across request/dependency/job/webhook boundaries where applicable;
- exclude credentials, signatures, authorization headers, and sensitive payloads from logs/errors;
- test wire contracts and failure paths with fake transports/request tests;
- consider old/new client, worker, and webhook compatibility during rollout.
