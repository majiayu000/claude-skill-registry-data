---
name: macos-local-ipc-integrity
description: Use when designing or reviewing macOS MCP/JSON-RPC, stdio, or Unix-socket IPC for framing, replay, authorization, backpressure, and commit integrity.
license: "MIT"
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# macOS Local IPC Integrity

Separate transport/decode/admission from authoritative commit/observation. Only the authority proves commit—not writes, send completions, or `accepted`.

## Inspect and Define

Trace identity/ownership, framing/EOF/teardown, queue bounds, reconnect/replay, authorization/opaque resources, suspensions, single-writer commit, and fresh verification. For an Apple-native same-host service, evaluate `NSXPCConnection` first; this skill's byte-stream contracts apply when MCP stdio or a custom Unix-socket transport is the intended boundary.

Use Xcode MCP `DocumentationSearch` for Apple API behavior; see [Apple documentation](references/apple-documentation.md).

Define version, framing/limits/overload, correlation versus stable operation ID/digest, resource preconditions, and distinct `rejected`, `accepted`, `committed`, `duplicate`, `conflicted`, `failed`, and `unknown`.

## Preserve Invariants

- Stream reads are arbitrary chunks: apply the selected transport's framing incrementally; cap before allocation; decode complete frames; keep stdout protocol-only; closure is EOF; serialize writes; bound per-peer/global bytes and work. Never silently discard an admitted command or outcome: overload and disconnect must have an explicit result or an `unknown` state recoverable through operation lookup.
- JSON-RPC `id` is correlation, not idempotency; notifications cannot prove commit and batches are not transactions. Preserve MCP negotiation. See [framing/reconnect/flow](references/framing-reconnect-and-flow.md).
- Post-submission disconnect is `unknown`. Retry only the same operation ID/digest. Commit restart-safe replay evidence atomically with the mutation; return matching duplicates without reapplying. Query after reconnect; bound backoff.
- Reachability is not authorization. At the authority, check principal/method/resource, resolve opaque IDs, prevent path-based confused deputies, and revalidate capability, identity, policy, revision, and duplicates after every suspension. Keep delegated tokens narrow/unlogged.
- Use **prepare → revalidate → write → commit**. Return `committed` only after durable mutation, revision, operation ID, digest, and replayable result. Hold no locks/transactions across external awaits. See [authorization/commit](references/authorization-and-commit.md).

## Verify and Report

Exclude payloads, tokens, text, paths, identifiers, environments, stderr, and parse fragments from logs/errors. Run framing, partial-I/O, slow-peer, queue, commit-cut, cross-principal, revocation, and privacy-canary [tests](references/failure-and-privacy-tests.md). Prove commit from freshly queried authoritative state, not mocks.

Report contracts, bounds, authorization, commit/replay, privacy/fault evidence, and ambiguity.

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

macOS stream handling, transport lifecycle, and local IPC integrity guidance was reviewed with Xcode MCP `DocumentationSearch`; see [Apple documentation evidence](references/apple-documentation.md).
