---
name: apple-networking
description: "Implement or audit URLSession clients, authentication, retries, cancellation, pagination, image loading, caching, and truthful offline SwiftUI state."
---

# Networking, caching, and remote state

## Inputs

Identify endpoint and trust boundaries, HTTP contract, authentication owner, data sensitivity, cancellation owner, retry/idempotency policy, caching rules, and offline behavior.

## Rules

- **NET-001 — Validate the response contract.** Check status, content expectations, decoding, and domain validity; receiving bytes is not success.
- **NET-002 — Bound remote work.** Limit concurrency, payload sizes, retries, cache growth, and pagination. Cancellation and resource cleanup must have owners.
- **NET-003 — Retry only safely.** Distinguish transport failure from authentication, validation, rate limiting, and uncertain writes; honor server retry/idempotency contracts.
- **NET-004 — Protect secrets and transport.** Use platform security defaults and appropriate credential storage. Do not bypass certificate validation or log tokens/private payloads.
- **NET-005 — Expose remote state truthfully.** Distinguish cached, stale, refreshing, failed, empty, cancelled, and authenticated states where they matter.

## Workflow

1. Put network behavior behind a small injectable client boundary.
2. Map transport/HTTP/decoding/domain errors into actionable feature states.
3. Implement cancellation and latest-request checks at the publication boundary.
4. Define cache key, freshness, account scope, invalidation, and eviction.
5. Test controlled responses and real integration separately.

## Verify

Test non-2xx responses, malformed/oversized payloads, cancellation, stale results, retry exhaustion, token expiry, pagination duplication, cache invalidation, offline startup, and account replacement.

## Output

Return the client/state contract, security and retry decisions, deterministic tests, and unverified service assumptions.

## References

Read the [playbook](references/networking-patterns.md) for decisions, failure cases, and source links.

For transport, pagination, images, and cache identity, read the [focused reference](references/transport-and-cache-boundaries.md).
