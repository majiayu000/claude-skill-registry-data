---
name: Memory Leak Diagnosis Skill
description: Diagnose, explain, and fix Swift and Apple-platform memory leaks, unexpected object retention, deinit failures, heap growth, retain cycles, runaway caches, task and AsyncSequence lifetimes, timer/delegate/closure ownership, jetsam, and ARC issues using Xcode Memory Graph and Instruments Allocations, Leaks, and VM tools. Use when objects do not deallocate, memory rises across repeated workflows, or weak/unowned and capture-list choices are unclear. Do not enable Zombies for leak measurement, call every temporary retention a leak, or use unowned without a proven lifetime invariant.
---

# Swift Memory Diagnosis

Prove the lifetime bug before changing capture lists. “Memory grew,” “deinit has not run yet,” “an object is retained,” and “an allocation is leaked” describe different evidence.

## Compatibility baseline

ARC, weak references, and Xcode’s core memory tools apply across currently supported Swift/Apple-platform projects. State version requirements for the specific APIs in the inspected code:

- Structured concurrency and `Task` require Swift 5.5 and the corresponding platform concurrency runtime.
- The task example in this skill uses duration-based sleep, available with Swift 5.7-era toolchains and iOS 16 / macOS 13.
- Observation, SwiftData, Combine, and framework-specific lifetime rules depend on the app’s declared deployment targets.
- Xcode and Instruments UI labels change. Describe goals and inspected relationships, not assumed arrow colors or displayed reference-count numbers.

## Classify the symptom

| Observation | Likely category | Best first tool |
| --- | --- | --- |
| A dismissed screen remains reachable | Unwanted retention / ownership bug | Memory Graph |
| Heap grows after repeating one workflow | Persistent allocations, cache, or leak | Allocations generations |
| Leaks instrument reports unreachable blocks | Heap leak | Leaks + allocation backtrace |
| Memory falls after pressure or cache purge | Cache / transient high-water mark | Allocations + signposts |
| Process is killed under memory pressure | Excess footprint / jetsam | Organizer report, VM Tracker, Allocations |
| Crash after replacing `weak` with `unowned` | Lifetime invariant violation | Crash backtrace + ownership graph |

The Leaks instrument does not find every strongly retained object. A retain cycle can remain reachable from framework or application roots and appear only in Memory Graph or repeated Allocations generations.

## Evidence-first workflow

1. Reproduce one bounded lifecycle: present/use/dismiss, start/stop, subscribe/unsubscribe, or load/purge.
2. Add temporary `deinit` probes to expected owners and dependencies.
3. Repeat the lifecycle several times. Record settled footprint after idle, not only peak memory.
4. Capture Memory Graph after the object should be gone. Inspect incoming strong paths back to roots.
5. Use Allocations generation marks before and after each repetition. Look for instance counts that monotonically persist.
6. Run Leaks for unreachable allocations and inspect their allocation backtraces.
7. Inspect tasks, streams, timers, observers, sessions, display links, delegates, and caches that cross the lifecycle boundary.
8. Fix the ownership or cancellation contract, not merely the nearest closure.
9. Repeat the identical workflow and verify deinitialization, stable generation counts, and acceptable footprint.

Use Zombies only to diagnose messaging/use-after-free. Zombies intentionally preserve deallocated objects and invalidate leak and footprint measurements.

Read [examples/example_instruments_leaks.md](examples/example_instruments_leaks.md) for a repeatable capture and verification procedure.

## ARC rules

- Strong is the default for ownership.
- Use `weak` when the referenced object may deallocate first. A weak property must be optional and becomes `nil` automatically.
- Use `unowned` only when the referenced object is guaranteed to outlive every access. A violated invariant traps; “avoids optional handling” is not a valid reason.
- Delegates are commonly weak because the delegate often owns the delegating object, but verify the actual graph.
- A closure forms a cycle only when an owner stores the closure and that closure strongly captures the owner (directly or through another path).
- A queue or task may retain a captured object only until work finishes. That can be harmful delayed release, but it is not automatically a permanent cycle.

### Correct delegate graphs

```swift
protocol DataDelegate: AnyObject {}

final class StrongDelegateManager {
    var delegate: (any DataDelegate)?
}

final class ScreenOwner: DataDelegate {
    let manager = StrongDelegateManager()
    init() { manager.delegate = self }
}
```

This graph cycles: owner → manager → delegate → owner. Making `delegate` weak breaks it. If `delegate` is already weak, the delegate relationship is not the cycle; inspect stored callbacks, tasks, and external owners instead.

### Correct bidirectional graph

Both links below are strong, so the graph cycles:

```swift
final class Person { var car: Car? }
final class Car { var owner: Person? }
```

If the car does not own its person, make `Car.owner` weak. Do not then describe that weak link as incrementing a retain count.

Read [examples/example_retain_cycle.swift](examples/example_retain_cycle.swift) for compiling stored-closure, delegate, bidirectional, value-container, and task-lifetime examples.

## Closure and task lifetimes

Do not add `[weak self]` mechanically. Decide whether work should:

- keep the owner alive until a finite operation completes;
- stop when the owner disappears; or
- be owned by a longer-lived service independent of the UI.

For indefinite work owned by a screen or model, store a task/token, cancel it in an explicit `stop`, and make the task avoid a strong capture across suspension points. A weak capture followed by `guard let self` outside an infinite loop still promotes `self` for the task’s entire remaining lifetime.

For `AsyncStream`, define who finishes the continuation and set `onTermination` when producer cleanup is required. For Combine, retain cancellables only for the intended owner lifetime. For `NotificationCenter` block observers, retain and remove the returned token. Invalidate `Timer` and `CADisplayLink`; invalidate URL sessions whose delegate lifetime should end.

Deliver UI-facing delegate callbacks and state mutations on `MainActor` rather than calling UIKit/AppKit from a background queue.

## Value types are not a blanket escape hatch

Structs and enums do not have identity under ARC, but they can contain reference-typed storage or escaping closures. A class can strongly own a struct that owns a closure that strongly captures the class. Standard-library collections also use internal reference storage. Analyze the complete graph rather than declaring value types incapable of participating in cycles.

## Memory Graph

1. Reproduce and pause after the owner should be released.
2. Open Debug Memory Graph.
3. Search for the concrete type and compare instance count with the expected count.
4. Select a stale instance and follow incoming strong references toward a root.
5. Separate framework roots that are expected to persist from application ownership that should have ended.
6. Capture the path and lifecycle that created it before editing code.

Do not depend on a particular arrow color, UI icon, or exact reference count; those presentations vary by Xcode release and compiler optimization.

## Instruments

- **Allocations:** mark generations around repeated workflows; compare persistent instance counts, allocation sites, and backtraces.
- **Leaks:** inspect reported unreachable allocations; absence of a report does not prove a dismissed controller was released.
- **VM Tracker:** investigate image buffers, mapped files, graphics surfaces, and other virtual-memory categories outside ordinary object counts.
- **Points of Interest / signposts:** align allocation changes with user actions.

Distinguish bounded caches from leaks by documenting their limit, eviction trigger, response to memory pressure, and observed steady state. An unbounded cache is still a memory defect even if every object remains intentionally reachable.

## Common ownership audit

- Stored closures and completion handlers
- `Task`, task groups, actors, and continuations
- `AsyncStream` producers and consumers
- Combine subscriptions and notification tokens
- Timers, display links, animation callbacks, and run-loop sources
- Delegates and data sources
- URLSession delegates and outstanding requests
- KVO/context observations
- Image/data caches and autorelease-heavy loops
- SwiftUI state models, environment values, hosting controllers, and presentation closures
- Core Data / SwiftData contexts and fetched object graphs

## Review checklist

- The reported stale type has a documented expected lifetime.
- There is a reproducible workflow and a baseline instance count.
- Incoming strong paths identify a root; no conclusion relies only on memory rising once.
- Weak and unowned choices state the actual lifetime invariant.
- Finite asynchronous work is distinguished from indefinite retained work.
- Cleanup has an explicit owner and can run on cancellation and error paths.
- Caches have bounds and memory-pressure behavior.
- The same workflow was repeated after the fix and reached a stable steady state.

## Supporting material

- [README.md](README.md) summarizes the diagnostic model.
- [examples/example_retain_cycle.swift](examples/example_retain_cycle.swift) contains strict-concurrency-safe ownership examples.
- [examples/example_instruments_leaks.md](examples/example_instruments_leaks.md) provides an Instruments and Memory Graph workflow.
- [examples/prompts.md](examples/prompts.md) contains representative activation prompts.
