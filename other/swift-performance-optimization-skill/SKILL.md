---
name: Swift Performance Optimization Skill
description: Use when investigating measured Swift or Apple-platform regressions in CPU, memory, launch, scrolling, animation hitches, image processing, energy, networking, or concurrency, or when designing performance tests and Instruments experiments. Do not use for speculative micro-optimization, ordinary refactoring, or a functional bug without performance evidence.
---

# Swift Performance Optimization Skill

Optimize from evidence. Preserve behavior, accessibility, data correctness, and lifecycle safety while changing performance characteristics.

## Baseline

The copy-ready examples use Xcode 16, Swift 6 language mode with strict concurrency, and iOS 17. Most principles apply to older targets; verify each API against the app's actual minimum. Material from the OS 27 development cycle is beta relative to stable Xcode 26.6 and requires an explicit request, beta labeling, stable fallback, and availability gate.

## Measurement workflow

1. Define a user-visible symptom and a reproducible scenario.
2. Record device, OS, build configuration, dataset, thermal state, and network conditions.
3. Measure an optimized Release build on representative hardware. Simulator-only timing is not release evidence.
4. Select the instrument that answers the hypothesis.
5. Save a baseline trace or metric, change one variable, then repeat the same scenario.
6. Confirm that the bottleneck moved and no memory, energy, correctness, or accessibility regression appeared.
7. Add a regression threshold where the workload is stable enough to automate.

Useful tools include:

| Symptom | First evidence source |
|---|---|
| CPU-bound work | Time Profiler; inspect heavy stacks and self time |
| SwiftUI update cost | SwiftUI instrument plus Time Profiler |
| Scroll or animation stalls | Animation Hitches, Core Animation, signposts |
| Growth or leaks | Allocations, Leaks, Memory Graph, memgraphs |
| Slow launch | App Launch template and launch signposts |
| Battery or thermal issues | Energy Log and device testing |
| Field regressions | MetricKit payloads and app-specific telemetry |

Use `os_signpost` or signposter intervals around important operations so traces answer product questions rather than only showing raw symbols.

## Lifetime and memory safety

- A capture is a cycle only when the closure is retained along a path back to its owner. Do not add `[weak self]` mechanically to every closure.
- Use `weak` when the owner may legitimately disappear before the callback. Use `unowned` only when the lifetime invariant is proven and documented; a wrong assumption traps.
- Prefer structured `async` functions over storing completion closures.
- Cancel owned tasks and invalidate repeating timers when the owner stops needing them and during teardown.
- Never use `[unowned self]` in a repeating timer merely to silence a cycle.

```swift
import Foundation

@MainActor
final class PollingModel {
    private var task: Task<Void, Never>?
    private(set) var tickCount = 0

    func start() {
        stop()
        task = Task { [weak self] in
            while !Task.isCancelled {
                do {
                    try await Task.sleep(for: .seconds(1))
                } catch {
                    return
                }
                guard let self else { return }
                tickCount += 1
            }
        }
    }

    func stop() {
        task?.cancel()
        task = nil
    }

    deinit {
        task?.cancel()
    }
}
```

If a Foundation `Timer` is required, capture its owner weakly, store the timer, invalidate the old instance before starting another, and invalidate it on stop/deinit.

See [the lifecycle-safe example](examples/example_memory_management.swift).

## Concurrency

- Swift concurrency is the default for new asynchronous flows, but Dispatch and operation queues remain supported interoperability and scheduling tools.
- Keep UI state on `@MainActor`. Move only verified expensive, concurrency-safe work away from it.
- Avoid spawning an unbounded task per item. Use task groups with deliberate limits, an actor, an async sequence, or a bounded worker design.
- Check cancellation before expensive phases and before publishing results.
- Do not trade actor safety for speed without race-focused tests and trace evidence.

## Collections and computation

- Pick structures by operation: a `Set` or dictionary can replace repeated linear membership searches.
- Avoid accidental copy-on-write churn in hot paths, but prove it with Allocations or profiling.
- Reserve capacity only when the final scale is reasonably known.
- Cache only expensive, repeatable results with a clear invalidation rule and a bounded memory policy.
- Benchmark optimized code with representative data; debug-build microbenchmarks are misleading.

## SwiftUI

- Stable identity is mandatory for mutable collections. Prefer model IDs, not offsets or a new UUID computed during rendering.
- `List` already realizes rows lazily. `ScrollView` plus `LazyVStack` offers different styling and interaction behavior; it is not inherently faster.
- A `body` evaluation is value computation, not proof that all descendants were redrawn. Use the SwiftUI instrument to identify expensive updates.
- Keep work out of `body`: precompute formatting, filtering, decoding, and image processing at the correct layer.
- Extract views for responsibility and data-flow clarity. Do not claim extraction alone establishes an isolated rendering boundary.
- Use `.equatable()`/`EquatableView` only after measurement, and include every visible input in equality.
- Prefer `.task(id:)` for work tied to a view and input. It cancels prior work when the ID changes.

See [the list identity example](examples/example_list_optimization.swift).

## Images and reusable cells

- Decode and downsample to the rendered pixel size rather than decoding full-resolution assets for thumbnails.
- Validate HTTP responses, cancel obsolete requests, and check both cancellation and represented URL before assigning an image.
- Reset image, identity, and task in `prepareForReuse()`.
- Lay out with constraints or `layoutSubviews`; a one-time frame set during initialization will not follow cell resizing.
- Use a bounded cache whose cost reflects decoded pixels. Add collection-view prefetching only after measuring its value and cancel prefetches when appropriate.
- Register cell classes/nibs, implement item counts, and avoid force-casting dequeued cells in copy-ready examples.

See [the complete downsampling and reuse example](examples/example_image_loading.swift).

## Shipping checks

- Compare percentile metrics, not only averages.
- Set thresholds that account for device classes and natural variance.
- Keep before/after traces with the scenario and build identifier.
- Re-test memory warnings, background/foreground transitions, cancellation, large accessibility text, and low-power/thermal conditions.
- State what was not measured; never market an optimization as proven from code inspection alone.

## Resources

- [List performance example](examples/example_list_optimization.swift)
- [Task lifetime example](examples/example_memory_management.swift)
- [Image downsampling and cell reuse](examples/example_image_loading.swift)
- [Performance investigation prompts](examples/prompts.md)
