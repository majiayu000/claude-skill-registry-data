---
name: cancellation-ping-and-progress
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P018
  - P025
  - P033
  - P034
  - P035
  - P069
  - P072
  - P074
  - P132
  - P133
  - P134
  - P135
  - P136
  - P137
  - P138
  - P139
  - P186
  - P206
  - P207
  - P208
  claims:
  - C00237
  - C00238
  - C00229
  - C00230
  - C00209
  - C00210
  - C00202
  - C00203
  - C00216
  - C00217
  - C00225
  - C00226
  - C00190
  - C00191
  - C00198
  - C00199
  - C00220
  - C00221
  - C00193
  - C00194
  - C00196
  - C00197
  - C00201
  - C00207
  - C00205
  - C00206
  - C00213
  - C00214
  - C00223
  - C00224
  - C00234
  - C00235
  - C00240
  - C00243
  - C00241
  - C00242
  - C00195
  - C00215
  - C00233
  evidence:
  - E00235
  - E00236
  - E00227
  - E00228
  - E00207
  - E00208
  - E00200
  - E00201
  - E00214
  - E00215
  - E00223
  - E00224
  - E00188
  - E00189
  - E00196
  - E00197
  - E00218
  - E00219
  - E00191
  - E00192
  - E00194
  - E00195
  - E00199
  - E00205
  - E00203
  - E00204
  - E00211
  - E00212
  - E00221
  - E00222
  - E00232
  - E00233
  - E00238
  - E00241
  - E00239
  - E00240
  - E00193
  - E00213
  - E00231
  source_anchors:
  - 8f5b562e852e-c0000
  - 2702be9d7f42-c0000
  - a52208278358-c0000
  authored_from_digest: 5099fdf56017a1075b94cf87a70710ee73bc758ce4be7625856878f68236166f
---

# Cancellation Ping And Progress

Run cancellation, ping, and progress as race-tolerant connection utilities. This skill packages 21
grounded principles the mcp-protocol-advisor applies when this layer of the Model Context Protocol
is in scope. Each finding names the rule, the protocol revision it belongs to, the failure or
interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- The request is task-augmented.
- A long-running task should report progress.
- Emitting progress notifications for an accepted request.
- Implementing or reviewing an MCP client or server transport that must detect dropped or unresponsive connections.
- Cancellation and response messages may cross on the wire.
- Designing an active connection-health monitoring loop over MCP.
- A party wants to receive progress updates for a request.
- Issuing a cancellation for an in-progress MCP request.
- A receiver accepts and acts on a cancellation notification.
- Building failure-handling and observability around MCP connection health.
- Constructing a `notifications/cancelled` notification.
- The request being cancelled is task-augmented.
- A receiver cannot honour or cannot validate a cancellation notification.
- Implementing cancellation handling in an application.
- Handling an inbound `ping` request on either side of an MCP connection.
- Reviewing or designing an MCP long-running operation that may report progress.
- Depending on progress notifications in client or server logic.
- An operation or task has completed or reached a terminal status.
- Implementing a sender or receiver that handles progress notifications.
- A client considers cancelling any request.
- A sent ping has not been answered within the configured timeout window.
- Validating an outgoing or incoming progress notification.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P006 (high confidence).** For task-augmented requests, keep using the original request's progressToken for the entire task lifetime — including after CreateTaskResult is returned — and never switch tokens mid-task; the token stays valid until the task reaches a terminal status.
2. **P018 (high confidence).** Require every progress notification to echo the original progressToken and a progress value that strictly increases on each notification even when no total is known; total and message are optional, with total omittable when unknown and message intended as human-readable text.
3. **P025 (high confidence).** Support the MCP ping mechanism as a bidirectional liveness check: allow either the client or the server to send a standard JSON-RPC request with method `ping` and no parameters to confirm the peer is responsive.
4. **P033 (high confidence).** Design both sides to tolerate cancellation race conditions: because a cancellation can arrive after the request finished or its response was sent, senders should ignore any late-arriving response and both parties must treat racing cancellations as graceful no-ops, preserving the fire-and-forget semantics of…
5. **P034 (high confidence).** Issue pings periodically to detect connection health, but make the frequency configurable, tune it to the network environment, and avoid excessive pinging that adds unnecessary network overhead.
6. **P035 (high confidence).** To opt into progress updates, require a progressToken in the request's `_meta` that is a string or integer and unique across all of the sender's active requests; the sender may choose the value freely as long as uniqueness holds.
7. **P069 (high confidence).** Cancel an in-progress MCP request by sending a `notifications/cancelled` notification carrying the target `requestId` and an optional human-facing `reason`; either side of the connection may initiate cancellation, and the `reason` must never be used to drive protocol behaviour.
8. **P072 (high confidence).** On receiving a valid cancellation, a receiver should stop processing the request, free its associated resources, and refrain from sending any response for it.
9. **P074 (high confidence).** Treat ping timeouts as connection failures, allow multiple failed pings to trigger a connection reset, and log ping failures for diagnostics.
10. **P132 (high confidence).** Only emit a cancellation that references a request the sender itself issued in that direction and that the sender still believes to be in-progress; never cancel a peer's request or one already known to be finished.
11. **P133 (high confidence).** Cancel task-augmented requests through the dedicated `tasks/cancel` request (which returns the final task state), not through `notifications/cancelled`.
12. **P134 (high confidence).** Treat cancellation as best-effort: a receiver may ignore a cancellation whose request is unknown, already completed, or uncancellable, and should ignore invalid notifications (bad request IDs, completed targets, or malformed content) rather than erroring.
13. **P135 (high confidence).** Make cancellation observable: log cancellation reasons for debugging and surface in the application UI when a cancellation has been requested.
14. **P136 (high confidence).** A ping receiver MUST respond promptly with an empty JSON-RPC result (`result: {}`) that reuses the originating request's `id`, so the sender can correlate the reply.
15. **P137 (high confidence).** Treat MCP progress tracking as opt-in and bidirectional: it applies only to long-running operations, and either party may emit progress notifications only when the peer has requested updates.
16. **P138 (high confidence).** Preserve receiver discretion: a receiver may decline to send progress notifications at all and may choose any notification frequency, so never require progress as a correctness precondition.
17. **P139 (high confidence).** Stop progress notifications once the operation is done: cease notifications after completion, and for tasks stop as soon as the task reaches a terminal status of completed, failed, or cancelled.
18. **P206 (high confidence).** Never allow a client to cancel the `initialize` request.
19. **P207 (high confidence).** When a ping response does not arrive within a reasonable timeout, the sender may treat the connection as stale and terminate it or attempt reconnection; this is permitted, not mandatory.
20. **P208 (high confidence).** Only send a progress notification for a token that was supplied in a still-active request and is bound to an in-progress operation; reject or drop notifications for unknown or completed operations.
21. **P186 (medium confidence).** Apply operational hygiene to progress: track active progress tokens on both ends and rate-limit progress notifications to prevent flooding the peer.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P006, P018, P025, P033, P034, P035, P069, P072, P074, P132, P133, P134, P135, P136,
P137, P138, P139, P186, P206, P207, P208. Every cited claim, evidence record, and source anchor
resolves in this package's distilled spine (`analysis/claims.jsonl`, `evidence/evidence-
records.yaml`, `sources/anchors/`). The Model Context Protocol specification is distillation-only
here: paraphrased, never quoted.

