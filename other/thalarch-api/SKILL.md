---
name: thalarch-api
description: >
  Contract-first API engineering for HTTP/REST, RPC, event-driven interfaces, and service
  boundaries. Use for new endpoints, API changes, client/server integrations, pagination,
  idempotency, errors, retries, compatibility, or externally consumed contracts.
---

# Thalarch API

An API is a compatibility contract, not merely a controller function.

## Contract first

Identify:

- caller(s) and trust boundary;
- request/response or message schema;
- success and error semantics;
- authentication vs authorization;
- idempotency/retry behavior;
- pagination/order/filter semantics;
- timeouts/cancellation;
- compatibility/versioning requirements;
- observability expectations.

Reuse the repository's existing API conventions before introducing a new envelope, error format,
version strategy, or serialization stack.

## Input and schema

Validate untrusted input at the boundary. Distinguish malformed input, invalid domain state,
authentication failure, authorization failure, conflict, missing resource, rate limiting, and
server failure according to the protocol/framework in use.

Do not expose internal exception text, stack traces, secrets, or database details as public error
contracts.

## Idempotency and retries

For operations that may be retried, define whether repeating the request is safe and how duplicate
side effects are prevented. Do not add automatic retries to non-idempotent operations without a
safe key/transaction/deduplication model.

Retries require bounded attempts, backoff/jitter where appropriate, cancellation, and a clear list
of retryable failures.

## Pagination and ordering

For paginated data:

- define a stable ordering;
- avoid offset pagination when data churn/scale makes it incorrect or expensive;
- treat cursor contents as protocol data;
- validate page-size limits;
- test empty/first/last/concurrent-change cases.

## Compatibility

Before changing an existing public contract, inspect callers and rollout constraints.

Prefer additive/compatible evolution where possible. If a breaking change is required, make the
migration/version boundary explicit rather than silently changing semantics.

## Distributed boundaries

Review:

- timeout budgets;
- cancellation propagation;
- partial failures;
- duplicate delivery;
- out-of-order events;
- eventual consistency;
- schema evolution;
- circuit/rate-limit behavior;
- correlation/tracing identifiers.

Do not claim exactly-once behavior unless the underlying system genuinely proves it.

## Testing

Use a mix appropriate to the contract:

- handler/unit tests for validation/domain mapping;
- schema/serialization tests;
- integration tests for real framework/database boundaries;
- contract tests when independent clients/services depend on the API;
- retry/idempotency/error-path tests;
- browser/device tests when the API behavior is only meaningful through a client flow.

## Verification

A controller unit test does not prove deployed/client compatibility. State which layer was
actually exercised and mark untested integration contracts `UNVERIFIED`.
