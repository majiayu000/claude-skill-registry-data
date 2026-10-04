---
name: long-running-tasks
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P029
  - P036
  - P037
  - P038
  - P073
  - P075
  - P076
  - P077
  - P078
  - P079
  - P082
  - P140
  - P141
  - P142
  - P143
  - P144
  - P145
  - P146
  - P187
  - P210
  - P211
  - P212
  - P213
  - P214
  - P215
  - P246
  - P253
  claims:
  - C00245
  - C00628
  - C00249
  - C00250
  - C00253
  - C00254
  - C00280
  - C00281
  - C00292
  - C00293
  - C00283
  - C00284
  - C00257
  - C00259
  - C00258
  - C00275
  - C00261
  - C00262
  - C00272
  - C00273
  - C00299
  - C00300
  - C00302
  - C00303
  - C00244
  - C00247
  - C00267
  - C00268
  - C00265
  - C00266
  - C00263
  - C00279
  - C00297
  - C00298
  - C00270
  - C00271
  - C00287
  - C00288
  - C00307
  - C00308
  - C00306
  - C00291
  - C00269
  - C00274
  - C00282
  - C00305
  - C00296
  - C00260
  evidence:
  - E00243
  - E00616
  - E00245
  - E00246
  - E00249
  - E00250
  - E00275
  - E00276
  - E00287
  - E00288
  - E00278
  - E00279
  - E00253
  - E00255
  - E00254
  - E00271
  - E00257
  - E00258
  - E00268
  - E00269
  - E00294
  - E00295
  - E00297
  - E00298
  - E00242
  - E00244
  - E00263
  - E00264
  - E00261
  - E00262
  - E00259
  - E00274
  - E00292
  - E00293
  - E00266
  - E00267
  - E00282
  - E00283
  - E00302
  - E00303
  - E00301
  - E00286
  - E00265
  - E00270
  - E00277
  - E00300
  - E00291
  - E00256
  source_anchors:
  - 8df00bee0b51-c0000
  - 4f99907b2686-c0000
  - 8df00bee0b51-c0001
  authored_from_digest: aad9cc5a5ba23653010dcb36680e004aa8209291734e512d5f2cfd5d72d9f85a
---

# Long Running Tasks

Treat tasks as an experimental, capability-gated, two-phase exchange. This skill packages 28
grounded principles the mcp-protocol-advisor applies when this layer of the Model Context Protocol
is in scope. Each finding names the rule, the protocol revision it belongs to, the failure or
interoperability break it prevents, the conforming behaviour, and the trade-off or residual risk.

## When this applies

- Building against the 2025-11-25 task specification.
- Auditing task-like durable request support against revision 2025-11-25..
- Initializing a session.
- Deciding whether to send a task-augmented request.
- A client is about to invoke a server tool via tools/call.
- Sending or handling any request, response, or notification tied to a task.
- A receiver rejects a task operation with an error.
- A requestor cancels a task or a receiver handles tasks/cancel.
- A receiver accepts a task-augmented request.
- Setting or relying on a task's retention window.
- A requestor is awaiting a task result.
- A task cannot complete without further requestor input (e.g. an elicitation).
- An authorization context is available for task operations.
- Running in an environment without authorization or requestor identification.
- Designing a task-augmented MCP client or server.
- The operation is expensive, batched, or backed by an external job API.
- A receiver dispatches an incoming request that may carry task metadata.
- Designing how a requestor learns of status changes.
- Implementing or consuming tasks/result.
- The wrapped request does not complete successfully.
- Updating or validating a task's status.
- Representing or interpreting task state.
- Operating task-augmented clients or servers that require auditability.
- Operating a receiver that retains task state.
- Deciding how to signal a task failure.
- A receiver creates a new task.
- Returning any task response.
- Implementing or consuming tasks/list.
- Exposing task endpoints to callers.
- Retrieving a task or result after its ttl may have elapsed.
- A task wraps a tools/call and the host wants to return control to the model.

## Procedure

Identify the negotiated protocol revision first, then apply the principles below that are in scope,
highest-risk first. For each one: name the rule and its revision, state the failure or
interoperability break it prevents, give the conforming behaviour, and state the trade-off or
residual risk. Never invent behaviour the spec does not define, and never weaken a consent or
security requirement below what the spec supports.

1. **P008 (high confidence).** Treat MCP tasks (introduced 2025-11-25) as an experimental capability: expect the design and behaviour to evolve and avoid hard-coding assumptions about unstable details.
2. **P029 (high confidence).** Gate task augmentation on capability negotiation: a peer that supports tasks must declare a structured `tasks` capability at initialization, requestors must only augment a request when the receiver declared the matching capability, treat `capabilities.tasks.requests` as exhaustive, and never create tasks when…
3. **P036 (high confidence).** Honour per-tool `execution.taskSupport` on top of the `tasks.requests.tools.call` capability: never augment tools when that capability is absent; when it is present, forbid task invocation for tools that omit it or set `forbidden` (returning -32601), allow either mode for `optional`, and require task invocation for…
4. **P037 (high confidence).** Correlate every task-related message with `io.modelcontextprotocol/related-task` (matching `taskId`) in `_meta`, including the `tasks/result` response whose body lacks the ID; but omit that metadata on `tasks/get`, `tasks/list`, and `tasks/cancel` (where the `taskId` is already the source of truth) and ignore it if a…
5. **P038 (high confidence).** Return the specified JSON-RPC error codes for task protocol errors: -32602 (Invalid params) for an invalid/nonexistent `taskId` in get/result/cancel, an invalid cursor in `tasks/list`, or cancelling an already-terminal task; -32603 (Internal error) for internal failures; optionally -32600 (Invalid request) when a…
6. **P073 (high confidence).** Enforce cancellation semantics: reject cancellation of an already-terminal task with -32602, and on a valid cancel attempt to stop execution, transition the task to `cancelled` before responding, and keep it `cancelled` even if execution later finishes; since a cancelled task may be deleted at any time, requestors…
7. **P075 (high confidence).** Implement task-augmented requests as a strict two-phase exchange: return a `CreateTaskResult` carrying only task data immediately (as soon as possible after acceptance) and never the operation result, and deliver the real result exclusively through `tasks/result` after the task completes.
8. **P076 (high confidence).** Treat `ttl` as advisory, not a guarantee: requestors may request a lifetime, receivers may override it and must report the actual `ttl` (or null for unlimited) in `tasks/get`, and once the `ttl` elapses the receiver may delete the task and its results regardless of status.
9. **P077 (high confidence).** Poll task status via `tasks/get`, respect the returned `pollInterval`, and keep polling until a terminal status or `input_required`; do not assume that calling `tasks/result` removes the need to keep polling.
10. **P078 (high confidence).** Use `input_required` for mid-task input: the receiver moves the task to `input_required` and tags the input request with related-task metadata, the requestor preemptively calls `tasks/result` to receive that request, and the task returns to `working` once the input is supplied.
11. **P079 (high confidence).** Treat the task ID as an access-control credential: because holding a task ID grants access to task state and results, bind tasks to the requestor's authorization context when one exists and reject get/result/cancel for tasks outside that context while filtering `tasks/list` to the requestor's own tasks.
12. **P082 (high confidence).** Harden unauthenticated deployments: when tasks cannot be bound to an authorization context, clearly document that results may be reachable by anyone who guesses the ID, generate cryptographically secure high-entropy task IDs, prefer shorter TTLs, and do not declare the `tasks.list` capability if requestors cannot be…
13. **P140 (high confidence).** Model long-running or deferrable MCP work as requestor-driven durable tasks: the requestor owns augmenting the request and polling for the result, while the receiver decides which request types are task-eligible and owns each task's lifecycle.
14. **P141 (high confidence).** Match task handling to declared capability: process requests normally and ignore task metadata for request types where task capability was not declared, and only reject non-task-augmented requests for types where it was declared.
15. **P142 (high confidence).** Treat `notifications/tasks/status` as an optional optimization only: receivers may push full-state notifications on status changes, but requestors must not depend on receiving them and must continue polling `tasks/get`.
16. **P143 (high confidence).** Make `tasks/result` return exactly what the underlying request would have returned, matching its result type: block the response while the task is `working` or `input_required`, and on a terminal task return either the successful result or the identical original JSON-RPC error.
17. **P144 (high confidence).** On execution failure move the task to `failed` — including JSON-RPC errors during execution and, for tool calls, a tool result with `isError` true — include a diagnostic `statusMessage`, and have `tasks/result` return the identical successful result or JSON-RPC error the underlying request produced.
18. **P145 (high confidence).** Enforce the task status state machine: every task starts in `working`, only the allowed transitions to and from `input_required` are permitted, and a task in a terminal status (`completed`, `failed`, or `cancelled`) must never transition again.
19. **P146 (high confidence).** Model task state with the standard fields (`taskId`, `status`, optional `statusMessage`, `createdAt`, `ttl`, `pollInterval`, `lastUpdatedAt`) and the five defined statuses — `working`, `input_required`, `completed`, `failed`, `cancelled` — treating a tool result with `isError` true as `failed`.
20. **P210 (high confidence).** Manage task resources deliberately: cap concurrent tasks per requestor and maximum `ttl`, clean up expired tasks promptly, document the supported limits, and monitor and alert on task resource usage.
21. **P211 (high confidence).** Report task problems through the correct channel: use standard JSON-RPC protocol errors for protocol-level issues and surface underlying-execution failures through the task status rather than as protocol errors.
22. **P212 (high confidence).** Generate task IDs as receiver-side strings that are unique across every task the receiver controls; never let the requestor supply the task ID.
23. **P213 (high confidence).** Include ISO 8601 `createdAt` and `lastUpdatedAt` timestamps on every task response so requestors can track creation and last-update times.
24. **P214 (high confidence).** Support opaque, cursor-based pagination for `tasks/list`: emit `nextCursor` whenever more tasks remain, require requestors to treat cursors as opaque tokens, and keep list visibility consistent with `tasks/get` (anything gettable is listable for that requestor).
25. **P215 (high confidence).** Rate-limit task operations to defend against denial-of-service and task-ID enumeration attacks.
26. **P187 (medium confidence).** Log task lifecycle for audit on both sides: receivers should record creation, completion, and retrieval events with auth context and watch for suspicious patterns (e.g. many failed lookups or excessive polling), and requestors should log lifecycle events and track task IDs with their operations.
27. **P246 (medium confidence).** Do not assume indefinite task retention: a receiver may purge an expired task and it is compliant to answer a later lookup with a 'task not found' error, so requestors must not depend on retrieval after expiry.
28. **P253 (low confidence).** A server may return an `io.modelcontextprotocol/model-immediate-response` placeholder in the `CreateTaskResult` `_meta` so the model can proceed while a task runs, but this is provisional, non-binding guidance and must not be relied on as stable protocol behaviour.

## Anti-patterns to flag

- Using a feature the peer never advertised, or skipping the initialization handshake and capability negotiation.
- Judging behaviour against the newest specification when an older revision was negotiated, or rejecting deprecated-but-present behaviour before its removal window.
- Inventing protocol behaviour the specification does not define, or presenting a proprietary extension as standard.
- Omitting the failure a rule prevents, the applicable revision, or the trade-off and residual risk.

## Grounding

Principles: P008, P029, P036, P037, P038, P073, P075, P076, P077, P078, P079, P082, P140, P141,
P142, P143, P144, P145, P146, P187, P210, P211, P212, P213, P214, P215, P246, P253. Every cited
claim, evidence record, and source anchor resolves in this package's distilled spine
(`analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context
Protocol specification is distillation-only here: paraphrased, never quoted.

