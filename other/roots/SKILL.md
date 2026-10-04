---
name: roots
kind: skill
status: ready
provenance:
  principles:
  - P043
  - P051
  - P089
  - P090
  - P091
  - P105
  - P106
  - P153
  - P154
  - P247
  claims:
  - C00368
  - C00373
  - C00387
  - C00388
  - C00367
  - C00385
  - C00375
  - C00376
  - C00380
  - C00382
  - C00384
  - C00386
  - C00369
  - C00370
  - C00371
  - C00372
  - C00377
  - C00381
  - C00379
  evidence:
  - E00362
  - E00367
  - E00381
  - E00382
  - E00361
  - E00379
  - E00369
  - E00370
  - E00374
  - E00376
  - E00378
  - E00380
  - E00363
  - E00364
  - E00365
  - E00366
  - E00371
  - E00375
  - E00373
  source_anchors:
  - 992d141a6f75-c0000
  authored_from_digest: 81bead56521b4a0967d43913fea20e8747cf832b74661fea915eebe149e94a17
---

# Roots

Treat roots as hard operational boundaries kept in sync and access-safe. This skill packages 10
grounded principles the mcp-protocol-advisor applies when this layer of the Model Context Protocol
is in scope. Each finding names the rule, the protocol revision it belongs to, the failure or
interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- A server needs to know which roots it may operate within.
- A client mediates user-owned filesystem access to a server.
- A server performs filesystem operations under MCP.
- The client has exposed one or more roots.
- The client advertised listChanged support.
- The exposed root set can change at runtime.
- A client is deciding which roots to expose to a server.
- A server relies on roots to scope its work.
- Designing how roots are surfaced to users or fetched by a server.
- Implementing or reviewing an MCP client that exposes roots.
- Constructing, accepting, or exposing a root URI.
- A client must respond to a roots request it cannot fulfil.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P043 (high confidence).** Discover roots via the `roots/list` request/response and treat its `roots` array (each entry a `uri` plus optional display `name`) as the authoritative current set.
2. **P089 (high confidence).** Treat MCP roots as hard operational boundaries: a server must confine its filesystem operations to the directories and files exposed by the client as roots.
3. **P090 (high confidence).** Keep the root set in sync via notifications: a client advertising `listChanged` must send `notifications/roots/list_changed` on any change, and a server must react by re-issuing `roots/list`.
4. **P091 (high confidence).** A client must enforce access safety before and while exposing roots: expose only roots it has permission for, apply proper access controls, and continuously monitor root accessibility.
5. **P153 (high confidence).** A client that supports roots must declare the `roots` capability at initialization, and set `listChanged: true` only if it will actually emit change notifications.
6. **P154 (high confidence).** Constrain and validate root URIs: a root `uri` must be a `file://` URI under the current spec, and a client must validate every root URI to prevent path-traversal.
7. **P051 (medium confidence).** A client should keep the user in control of roots: obtain consent before exposing roots, provide a clear root-management UI, verify a root's accessibility before exposing it, and monitor for subsequent changes.
8. **P105 (medium confidence).** A server should be defensive about roots at runtime: check the roots capability before using roots, validate all paths against the provided roots, and handle roots that become unavailable without failing catastrophically.
9. **P106 (medium confidence).** Do not couple root handling to a specific UI: the protocol mandates no user-interaction model, so expose roots through whatever workspace/project interface fits, and cache root information appropriately instead of re-fetching needlessly.
10. **P247 (medium confidence).** Return standard JSON-RPC errors for roots failures: `-32601` (method not found) when the client does not support roots, and `-32603` for internal errors.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P043, P051, P089, P090, P091, P105, P106, P153, P154, P247. Every cited claim, evidence
record, and source anchor resolves in this package's distilled spine (`analysis/claims.jsonl`,
`evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context Protocol specification is
distillation-only here: paraphrased, never quoted.

