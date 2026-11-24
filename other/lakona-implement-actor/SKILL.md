---
name: lakona-implement-actor
description: Create or update Lakona game actors across stable Server.App state shells and reloadable Server.Hotfix behavior. Use when modeling long-lived mutable game state, declaring an Actor NodeRole, adding messages or lifecycle hooks, choosing actor keys and Local Route Place or Startup access, implementing cross-actor calls, or fixing Lakona actor and Hotfix analyzer errors.
---

# Implement a Lakona Actor

Model one long-lived mutable game entity as a stable actor state shell plus one
reloadable Hotfix behavior. Keep the actor boundary explicit and preserve
sequential turn execution.

Use HotfixComponent for tools whose ordinary calls may run concurrently and need
no actor identity or mailbox. Use Actor + Behavior for serialized mutable state
and timers; a Startup Actor is not a general resource-initialization mechanism.

## Workflow

1. Read `AGENTS.md`, the project README, and scoped repository instructions.
2. Identify the business identity, state ownership, commands, queries,
   lifecycle, placement role, persistence needs, and callers. Confirm that an
   actor is the right concurrency boundary rather than an RPC DTO, transient
   service, or database record. Actor memory is not persistence: state which
   must survive process loss belongs in an application-owned store.
3. Inspect existing actors, App-side message DTOs, Hotfix behavior classes,
   startup declarations, serializer conventions, and tests.
4. Search for an existing actor and `[HotfixBehaviorOf]` binding. Extend the
   existing pair rather than creating duplicate state or a second behavior
   class.
5. Read [actor-shapes.md](references/actor-shapes.md) before choosing the key,
   creating App contracts, selecting Local versus Route versus Place versus
   Startup, or adding lifecycle hooks.
6. Define stable identity, state, and cross-boundary message DTOs in
   `Server.App`. Mark the Actor with exactly one `[NodeRole("...")]` matching
   the processes allowed to host it. Keep the actor class focused on state;
   place game decisions in `Server.Hotfix`.
7. Implement public behavior entry methods on the unique class marked
   `[HotfixBehaviorOf(typeof(...))]`. Use the target actor as the first
   parameter and a stable request DTO as the second. Do not add a
   `CancellationToken` parameter: caller cancellation only stops waiting.
8. Call other actors through generated selectors with a direct static lambda.
   Use the selector whose routing semantics match known ownership.
9. Manage a logical actor lifecycle through generated
   `ActorAccess.Place<TActor>(key)`: use `CreateAsync` when absence is required,
   `EnsureAsync` when an existing activation is acceptable, and `DestroyAsync`
   for an external lifecycle decision. An actor ending its own business
   lifetime requests post-turn cleanup through
   `self.Context.RequestDeactivation()`.
10. Add `[ActorStart]` and `[ActorStop]` hooks only for real lifecycle work.
    Release application-owned long-lived handles during cleanup. Activation
    shutdown automatically cancels its timers; use `DestroyTimer` only when
    business logic needs early cancellation. Do not add `[ActorStop]` solely
    to destroy timers.
11. Reuse focused tests for affected state transitions, replies, lifecycle,
    placement assumptions, and failure behavior; add or update tests only where
    meaningful coverage is missing.
12. Build the Hotfix project and run the focused actor tests. Treat analyzer
    diagnostics as boundary violations to fix, not warnings to suppress.

## Non-Negotiable Boundaries

- Hotfix business exceptions deriving directly or indirectly from `System.Exception`
  are created with `new` using runtime error data. They need no role or DI
  registration; `[HotfixComponent]` is for DI-owned helpers. Remove a mistaken
  marker reported by `LAKONA20060`. If an older framework reports `LAKONA20037`
  on an exception, upgrade and verify compilation plus Hotfix loading before
  removing temporary suppressions. Ordinary classes still require a role.
- Use a stable business key. Do not encode a node, endpoint, transport,
  callback, RPC Session, or incidental connection in an actor ID.
- Every stable Actor declares exactly one `[NodeRole]`. Do not infer placement
  from connection strings or repeat role policy in Hotfix registration.
- Keep long-lived in-memory state on the stable App actor. Do not store it in
  Hotfix instance fields, static fields, callbacks, or background tasks. Use an
  application Store when state must survive process or cluster loss.
- Do not put business methods on the stable actor merely to bypass Hotfix.
- Mutate non-public actor state only from the actor itself or its unique Hotfix
  behavior. Do not make fields public just to evade `LAKONA20031`.
- Do not self-call through `ActorAccess`. Continue the current actor turn
  directly when operating on the same actor.
- Use `Route<TActor>(key)` for the normal distributed business path. Use
  `Local<TActor>(key)` only after proving current-node ownership. Use
  `Startup(key)` only for a declared startup actor group.
- Use `Place<TActor>(key)` for cluster-aware creation, ensure, and logical
  destruction. External coordinators use `DestroyAsync`; an actor deciding its
  own lifetime uses `self.Context.RequestDeactivation()` during its active turn.
  Do not inject the internal `ActorHosting` service, expose current-node
  destruction, or mutate the actor directory or cache. Normal calls and timer
  callbacks must not implicitly create missing actors.
- Use `CallAsync` when the caller needs completion or a reply. Use `PostAsync`
  only when mailbox acceptance is sufficient.
- Do not block on actor work, discard required completion, or hand-write string
  dispatch and raw route plumbing.

## Validation

Apply the validation steps to affected contracts, reusing existing coverage and
adding tests only where meaningful coverage is missing. For non-behavioral,
low-impact edits, use relevant static checks. A test command may also satisfy
the build when it covers the same graph and configuration. Once relevant checks
and required stage gates pass, stop unless new changes, failures, or a concrete
unresolved risk justify more verification. Report any unverified outcomes.

Build the discovered Hotfix project; it references the stable App project and
therefore validates both halves in the normal project shape:

```powershell
dotnet build Server/Hotfix/Server.Hotfix.csproj
```

Run existing actor or domain tests. Verify state transitions, configured role
eligibility, and lifecycle behavior, not only source shape. If routed calls are
introduced, validate the project's serializer and cluster test surface as well.
