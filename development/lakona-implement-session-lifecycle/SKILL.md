---
name: lakona-implement-session-lifecycle
description: Implement or update Lakona Game Session lifecycle policy in Server.Hotfix using IGameSessionLifecycle. Use when handling disconnect, resume-window retention, expiration, application-defined session ownership, stale lifecycle events, presence or room cleanup, or fixing Hotfix lifecycle binding and tests.
---

# Implement a Lakona Session Lifecycle

Implement product cleanup policy around Lakona's resumable Game Session. Keep connection loss, recovery-window expiration, explicit termination, and product-level player sessions as distinct events.

## Workflow

1. Read the repository instructions and the project's session, Hotfix, actor, and testing documentation before editing.
2. Locate the existing `IGameSessionLifecycle` binding, session configuration, current framework-session ownership and application-defined mappings, business actors, room or matchmaking cleanup paths, and lifecycle tests.
3. Locate the handler selected at each affected `StartSessionAsync<TLifecycle>` call. Update that implementation in place, or add a handler when the requested policy needs one. Multiple `IGameSessionLifecycle` implementations are supported; there is no global default. Non-generic session creation selects no business lifecycle handler.
4. Read [references/session-lifecycle-shapes.md](references/session-lifecycle-shapes.md) before designing event behavior.
5. Write down the intended policy for each event before changing code:
   - disconnected inside the resume window
   - resumed after a replacement connection completes the recovery heartbeat replay step
   - expired after the resume window
   - effects on any other application sessions linked by product policy
   - stale events for a superseded session
   - explicit termination, if requested
6. Use business actors or application services as the current ownership
   authority. Persist state through an application Store when it must survive
   process loss. Read current ownership before mutating it.
7. Verify that the lifecycle event's session ID still matches the specific current ownership slot or mapping targeted by the cleanup. Treat a stale event as an idempotent no-op.
8. Keep disconnect handling compatible with reconnection. Perform irreversible room, match, presence, or actor cleanup on expiration unless the product explicitly requires an earlier transition.
9. Reuse established constructor injection, generated actor selectors, logging, cancellation, and error-handling conventions.
10. Build the Hotfix project and run focused lifecycle tests, including disconnect, expiration, reconnection, stale-event, and application-role cases relevant to the change.

## Required Binding

Use the project's current API shape. Each selected handler implements the framework interface and carries a parameterless attribute:

```csharp
[HotfixLifecycle]
public sealed class GameSessionLifecycle : IGameSessionLifecycle
```

Implement all three methods: `SessionDisconnectedAsync`, `SessionResumedAsync`, and `SessionExpiredAsync`, accepting `HotfixLifecycleCall<TRequest>` with the corresponding framework request type. Select the handler through `StartSessionAsync<GameSessionLifecycle>` at session creation. Do not expose this contract in Shared or name the class as an RPC `*Service`.

Recovery preserves the selected handler identity. Active sessions and pending expiration callbacks prevent publishing a generation that removes or renames their handler. Keep per-session state out of generation-owned handler fields.

## Lifecycle Boundaries

- An RPC Session is one live connection. A Game Session can outlive that connection and resume during its recovery window. A product Player Session is a separate domain concept.
- `SessionDisconnectedAsync` means the connection was lost but the Game Session remains resumable. Avoid durable removal or user-visible offline transitions that would make recovery inconsistent.
- `SessionResumedAsync` runs once per committed replacement binding after its recovery heartbeat completes the replay send step. Initial login and failed recovery do not trigger it; replay completion does not imply client acknowledgement. Restore matching product presence idempotently.
- `SessionExpiredAsync` means the recovery window ended and Lakona removed framework session state. Perform durable product cleanup here, subject to explicit product policy.
- Explicit administrative or product termination uses `ILakonaGameServer.TerminateSessionAsync`. Do not simulate it by invoking a lifecycle handler or closing a raw RPC connection.
- Names such as control and realtime describe optional application traffic roles, not Lakona Session types, identity fields, configuration values, or routing semantics.
- Multiple Game Sessions are independent by default. Do not clear another session merely because one expired unless product policy explicitly links them.

## Safety Rules

- Constructor injection applies to lifecycle handlers and DI-owned helpers.
  Business exceptions deriving directly or indirectly from `System.Exception`
  may stay in Hotfix and use `new` with runtime error codes and inner exceptions.
  They need no role or DI registration. Remove a mistaken `[HotfixComponent]`
  marker reported by `LAKONA20060`; for older frameworks reporting `LAKONA20037`
  on exceptions, upgrade and verify compilation plus Hotfix loading before
  removing temporary suppressions. This does not change lifecycle policy.
- Do not subscribe directly to `RpcSession.Disconnected`, depend on endpoint names, add an App-to-Hotfix bridge, or duplicate the framework lifecycle contract.
- Do not store callbacks, transports, actor references, or durable game state in session items. Session items are a small scalar cache. Lifecycle calls expose only `Request`, containing `OwnerKey`, `SessionId`, and `ConnectionId`; they provide no item snapshot or call-context services. Constructor-inject dependencies.
- Lifecycle callbacks are in-process notifications, not durable events. Failures are logged and contained without automatic retry or rollback of recovery. Use an application-owned durable mechanism when cleanup must survive callback failure or process loss.
- Make cleanup idempotent. Missing actors, already-left rooms, repeated events, and superseded sessions need deliberate behavior.
- Do not swallow cancellation or concrete cleanup failures. Follow project logging policy and avoid reporting success for incomplete durable cleanup.
- Keep Hotfix lifecycle methods thin. Route business mutations through their owning actor or application service.

## Validation

Apply the validation steps to affected contracts, reusing existing coverage and
adding tests only where meaningful coverage is missing. For non-behavioral,
low-impact edits, use relevant static checks. A test command may also satisfy
the build when it covers the same graph and configuration. Once relevant checks
and required stage gates pass, stop unless new changes, failures, or a concrete
unresolved risk justify more verification. Report any unverified outcomes.

For implementation changes, validate the discovered Hotfix build directly or
through tests that build the same graph and configuration. Reuse focused tests
for the following affected contracts; add tests only where coverage is missing:

- disconnect retaining resumable state
- expiration performing the intended durable cleanup
- reconnection before expiration
- per-session handler selection, no handler for non-generic creation, and resumed callback behavior
- a stale event not clearing a replacement session
- application-defined multi-session handling, when the product has it
- repeated cleanup and missing-state behavior
- explicit termination remaining separate from disconnect and expiration

Report the policy implemented, files changed, validation commands, and any product choice that remains unresolved. Compilation validates the binding shape; only behavioral evidence validates cleanup semantics.
