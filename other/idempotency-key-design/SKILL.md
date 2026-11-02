---
name: idempotency-key-design
description: Design idempotency keys and persistence rules for retryable API operations that may execute more than once.
---

# Idempotency Key Design

## Goal

Prevent duplicate orders, payments, jobs, or other consequential side effects when clients retry or networks fail.

## Inputs to inspect

Mutation endpoint, request identity, transaction boundary, persistence model, retention period, and retry behavior.

## Workflow

1. Identify the logical operation and the boundary at which duplicate execution would cause harm; distinguish a retry from a genuinely new operation.
2. Define key scope and ownership, how request identity is bound to normalized payload, and how key reuse with a different payload is rejected.
3. Persist operation status and result atomically with the side effect where possible; specify behavior for concurrent requests using the same key.
4. Define retention, expiration, failure recovery, and the response returned for completed, pending, or failed attempts.
5. Test concurrent duplicates, timeout after commit, worker crash before acknowledgment, key collision, expired keys, and same key with different payload.

## Validation checklist

- [ ] Two simultaneous requests with one key cannot produce duplicate committed side effects.
- [ ] Key reuse with materially different input is rejected or handled by an explicit contract.
- [ ] Operation status survives process restart and ambiguous network responses.
- [ ] Retention is long enough for realistic retries and documented to clients.
- [ ] Idempotency does not incorrectly merge two legitimate operations from different scopes.

## Required output

Deliver an idempotency contract, key-scope rules, storage/state model, concurrency tests, and retry examples.

## Boundaries and failure handling

Do not rely on an in-memory cache for financial or otherwise durable idempotency; do not promise exactly-once execution when only at-least-once delivery is guaranteed.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
