---
name: lakona-integrate-game-client
description: Integrate or update a generated Lakona Game client in Unity, Godot, or .NET applications, including connection progress, business login, automatic recovery, callback dispatch, and disposal. Use for client connection UI or reconnect behavior; server session cleanup belongs to the session lifecycle skill.
---

# Integrate a Lakona Game Client

Use the project's generated `LakonaGameClient` as the connection owner. Keep
framework connectivity, business authentication, session phase, and game-state
synchronization as separate decisions.

## Workflow

1. Follow the project instructions and applicable README sections. Inspect the
   installed runtime and generator versions, generated facade, transport and
   serializer setup, callback receiver, client owner, and existing tests. Reuse
   material already read. Do not assume this repository or a sample namespace
   exists in the user's project.
2. Update the existing client owner in place. Locate the business login response,
   session snapshot, engine dispatch loop, cancellation, and logout/reset paths
   before changing connection behavior.
3. For automatic recovery, construct `LakonaGameClientOptions` with a
   `Func<ITransport>` that creates a fresh, correctly configured transport for
   every connection generation. Returning the same transport defeats recovery.
   Keep the serializer and application-owned logger factory consistent across
   generations; dispose the logger factory at application shutdown.
4. Await `ConnectAsync` for framework initialization, then invoke the project's
   business login through `gameClient.Api`. Enter authenticated UI only after
   the business response succeeds; enter gameplay only after the application's
   required state synchronization. Do not call `StartSessionAsync` or send
   framework acknowledgements from normal generated-client application code.
5. Subscribe to the generated facade's `ConnectionStateChanged` before connecting,
   and read `ConnectionState` for initial rendering. Marshal event payloads to the
   engine's main thread. Inspect `Snapshot` and business responses separately.
   Catch failure from each RPC even when `IsConnected` was true immediately
   before the call.
6. Let the generated Game client own transient recovery. Retain resumable game
   state while reconnecting; do not start another connection, call login again,
   or destroy the match merely because connectivity is temporarily unavailable.
   Apply terminal recovery failure and explicit logout according to product
   policy, then await disposal before abandoning the old client owner.
7. Reuse focused client tests and validate the affected engine build. Exercise
   the real connection/recovery path when changing its wiring; compilation
   alone does not prove recovery or main-thread UI behavior.

## Connection States

State properties require `Lakona.Game.Client 0.5.13`, `Lakona.Rpc.Client 0.14.6`,
and the corresponding `Lakona.Rpc.Core 0.14.9` generator line. The state event
requires `Lakona.Game.Client 0.5.15`, `Lakona.Rpc.Client 0.14.8`, and
`Lakona.Rpc.Core 0.14.11`. Detect compatibility
from the project's actual dependencies and generated output. Upgrade a matching
dependency set and rebuild when the required members are absent; do not invent APIs
for older projects or infer compatibility from the installed Tool/Hub version.

| `LakonaGameConnectionState` | Application handling |
| --- | --- |
| `Created` | Connection has not started. Allow the initial connect action. |
| `Connecting` | Transport and Game handshake are pending. Show progress and block duplicate connect requests. |
| `Connected` | Game initialization or recovery confirmation completed. Decide login and gameplay readiness from business state. |
| `Reconnecting` | Recovery includes old-generation draining, retry delays, handshake, and confirmation. Show recovery progress and retain resumable state. |
| `Disconnected` | Automatic recovery ended through rejection or expiry. Render a terminal failure and offer a product-defined fresh connection/login path. |
| `Disposed` | Disposal has started. Await `DisposeAsync` to observe cleanup completion; this client cannot be reused. |

`IsConnected` is exactly `ConnectionState == Connected`. A false value alone
does not distinguish initial connection, recovery, terminal failure, or disposal.
State reads are synchronized and follow the current connection generation, but
they describe locally known state rather than remote liveness. `ConnectionState`
and `Snapshot.Phase` are not one atomic snapshot.

Initial connection failure or cancellation automatically disposes the Game
client. Inspect the exception and `Snapshot.Failure`, and create a new client,
options, and transport factory for an initial retry. A recovery `Disconnected`
event reports terminal recovery failure, not each transient transport loss.

Read [references/client-ui-shapes.md](references/client-ui-shapes.md) when wiring
connection progress into an engine UI or reviewing an existing reconnect flow.

## Ownership and Callback Rules

- Query the generated Game client rather than a saved `options.Transport`;
  recovery can replace that transport. API proxies may remain stable across
  generations, but retaining a proxy does not prove connection availability.
- `ConnectionStateChanged` supplies `LakonaGameConnectionStateChange` with
  `PreviousState` and `CurrentState`, ordered on the thread pool outside lifecycle
  locks. It does not replay state on subscription. The property may already be
  newer than the payload. Never update engine UI directly from the handler.
  Keep handlers short; enqueue work rather than blocking or using `async void`.
  Exceptions are isolated and logged. Lifecycle operations do not await handlers.
  Unsubscribe when releasing the owner; already queued notifications may still
  arrive, so validate ownership when applying them. For older compatible clients
  without the event, use the existing main-thread presenter to query state.
  Do not use terminal `Disconnected` as a transient progress feed or assume an
  ordering between that callback and asynchronous state notifications.
- Marshal callbacks and async results through the engine's established main
  thread dispatcher or a thread-safe inbox. Ignore callbacks/results from a
  superseded client owner when applying them after logout or a fresh login.
- Keep pending UI requests separate from connectivity. Block duplicate input,
  give immediate feedback, and finish each request on its actual response or
  failure. Restored connectivity does not complete a pending business request.
- The plain generated `RpcClient` and `RpcClientRuntime` own one connection,
  not Game recovery. Runtime states are `Created`, `Connecting`, `Connected`,
  `Stopped`, and `Disposed`; terminal stop may precede disconnect-event draining.
  Use a fresh plain RPC client for reconnect. Do not map `Stopped` to Game
  `Reconnecting` or copy Game recovery policy into the RPC layer.
- Explicit product logout is a business operation when the project has one.
  Await its required confirmation and dispose the client; transport disposal
  alone does not prove immediate server-side session termination.

## Validation

Select existing checks for the changed behavior, adding coverage only where a
meaningful contract is missing: initial connect/login failure, duplicate input,
transient loss retaining game state, resumed traffic, terminal rejection/expiry,
and logout/disposal ignoring stale callbacks. Use the project's real transport
or process E2E when changing recovery wiring. For skill/text-only updates, check
metadata, references, API names, and distribution instead of rerunning gameplay.
After relevant checks and applicable stage gates pass, stop unless a new change
or concrete unresolved risk justifies more checks. Report unverified outcomes.
