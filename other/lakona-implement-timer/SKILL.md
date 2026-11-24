---
name: lakona-implement-timer
description: Create or update framework-owned Lakona Hotfix timers, stable timer arguments, callbacks, and actor lifecycle integration. Use when adding one-shot or periodic jobs, storing or destroying TimerId values, executing timer ticks in actors, repairing timer cleanup, or fixing Lakona timer callback and serialization errors.
---

# Implement a Lakona Timer

Implement scheduled work with Actor timers so callbacks resolve against the
active Hotfix generation and long-lived ownership remains in stable state.

## Workflow

1. Read `AGENTS.md`, the project README, and scoped repository instructions.
2. Define the schedule, owner, first due time, repeat period, callback action,
   cancellation behavior, and cleanup condition. Decide whether the operation
   is one-shot or periodic. Lakona timers are process-memory scheduling: if the
   schedule must survive restart, use an application-selected persistent
   scheduler or Store instead of treating Actor timers as durable.
3. Inspect existing timer argument DTOs, `[ActorTimer]` Behavior methods,
   `TimerId` fields, actor lifecycle hooks, and timer-focused tests.
4. Search for an existing timer with the same responsibility. Update its
   complete lifecycle instead of creating a competing schedule.
5. Read [timer-shapes.md](references/timer-shapes.md) before defining arguments,
   choosing callback placement, creating the timer, or writing cleanup.
6. Choose whether the callback needs a creation-time business snapshot. If it
   only needs `self`, use the argument-free overload; do not create an empty DTO
   or repeat the owning Actor ID. Put any needed argument DTO and stored
   `TimerId` in stable App state/types. Keep callbacks and scheduling in Hotfix.
7. Define an instance Behavior method marked `[ActorTimer]`, returning
   `ValueTask` and accepting `(ActorType self, TimerTick tick)` without business
   arguments, or `(ActorType self, TimerTick<TArgs> tick)` with arguments. Private
   callbacks are supported and excluded from RPC generation.
8. Create the timer in its owning Actor turn and active Hotfix scope with a direct static
   typed callback selector. Store the returned ID when later destruction or
   duplicate prevention is required.
9. Make periodic creation idempotent for its owner. Activation shutdown cancels
   timers automatically. Store IDs only for early cancellation or duplicate
   prevention, and clear stored IDs before explicit cancellation.
10. Access mutable Actor state directly through `self` in the callback. Do not
    forward a call to the same Actor. Ticks expose no cancellation token;
    timer destruction prevents pending and future callbacks without interrupting
    a callback already running. Choose any downstream cancellation policy explicitly.
11. Build the Hotfix project and run timer, actor lifecycle, and domain tests
    that cover creation, dispatch, repetition, and cleanup.

## Non-Negotiable Boundaries

- Exceptions created inside Hotfix callbacks may remain in Hotfix when they
  derive directly or indirectly from `System.Exception`. Construct them with
  `new` using runtime data; they are neither timer argument DTOs nor DI components.
  Remove `[HotfixComponent]` when `LAKONA20060` reports it. For older frameworks
  reporting `LAKONA20037` on exceptions, upgrade and verify compilation plus
  Hotfix loading before removing temporary suppressions.
- Use `self.CreateOnceTimer` or `self.CreatePeriodicTimer`. Do not introduce `System.Threading.Timer`,
  `PeriodicTimer`, fire-and-forget delay loops, or `Task.Run` schedulers for
  Hotfix business work.
- Create and destroy timers only inside an active Hotfix execution scope. Do
  not call Actor timer extensions from stable App code, constructors, or work that
  escaped the scope.
- Use a static typed selector such as
  `static (RoomBehavior behavior) => behavior.TickAsync`. Do not retain
  a Hotfix delegate or dispatch by a hand-written method-name string.
- Keep timer arguments stable, concrete, bounded, and serializable. Do not put
  actors, services, callbacks, cancellation tokens, or arbitrary object graphs
  in timer arguments.
- Cancel early with `self.DestroyTimer(timerId)` in the owning activation's
  active Hotfix turn. Other activations cannot cancel its registered timers.
- Store cancellable timer ownership as `TimerId` in stable state. Do not
  manufacture IDs.
- Keep mutable game state on the stable Actor. The callback already runs in
  its owning activation's mailbox.
- Do not retain transport callbacks, session callback objects, or old Hotfix
  generation objects across ticks.
- Explicit destruction stops queued and future callbacks. A running callback
  completes normally; destruction does not await it, so self-cancellation cannot deadlock.
- `TimerTick` exposes only `TimerId`; `TimerTick<TArgs>` exposes `TimerId` and
  `Args`. Parameters are creation-time snapshots, not mutable state shared across
  ticks. Resolve dependencies by
  injection and obtain business time in the callback.
- Lakona does not persist timers or rebuild them after process loss. Integrate
  a persistent scheduler as an application resource when the product requires
  durable calendar jobs; do not add persistence semantics to Actor timers.

## Validation

Apply the validation steps to affected contracts, reusing existing coverage and
adding tests only where meaningful coverage is missing. For non-behavioral,
low-impact edits, use relevant static checks. A test command may also satisfy
the build when it covers the same graph and configuration. Once relevant checks
and required stage gates pass, stop unless new changes, failures, or a concrete
unresolved risk justify more verification. Report any unverified outcomes.

Build the discovered Hotfix project:

```powershell
dotnet build Server/Hotfix/Server.Hotfix.csproj
```

For the contracts affected by the change, reuse focused tests that prove the
timer fires the intended callback, periodic
creation is not duplicated, one-shot versus periodic behavior is correct, the
argument round trip succeeds when arguments are used, and cleanup removes the timer. A successful build
alone does not prove scheduling semantics. Add tests only where meaningful
coverage is missing.
