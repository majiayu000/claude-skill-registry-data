---
name: swift
description: Use when writing Swift for iOS, macOS, or server-side. Covers value semantics, optionals, protocol-oriented design, structured concurrency with async/await and actors, and SwiftUI state management.
metadata:
  category: languages
  version: 1.0.0
  tags: [swift, ios, concurrency, actors, swiftui]
---

# Swift

## Purpose

Write Swift that leans on value semantics and the concurrency model rather than fighting them: structs by default, actors for shared mutable state, and no force-unwrapping.

## When to Use

- Writing Swift for Apple platforms or server-side Swift.
- Migrating callback or Combine code to async/await.
- Resolving data-race warnings under strict concurrency checking.
- Designing SwiftUI state and view models.
- Diagnosing retain cycles and memory growth.

## Capabilities

- Value vs reference semantics and copy-on-write.
- Optional handling: `guard let`, optional chaining, `Result` types.
- Protocol-oriented design with associated types and generics.
- Structured concurrency: `async let`, task groups, actors, `Sendable`.
- SwiftUI: `@State`, `@Observable`, and unidirectional data flow.

## Inputs

- Source target, Swift version, minimum deployment target.
- Concurrency checking level (minimal, targeted, complete).

## Outputs

- Code free of force-unwraps and implicit unwrapped optionals.
- Concurrency that compiles cleanly under strict checking.
- View models with a single source of truth.

## Workflow

1. **Prefer structs** — Reach for a class only when identity or shared mutation is required.
2. **Eliminate optionals early** — Unwrap once at the boundary with `guard`; the rest of the function works with non-optionals.
3. **Isolate mutable state** — Any shared mutable state becomes an actor or is confined to the main actor.
4. **Model async explicitly** — Replace completion handlers with `async` functions; use task groups for concurrency.
5. **Gate** — Build with strict concurrency checking and treat warnings as errors.

## Best Practices

- `!` is a crash waiting for a user to find it. The only acceptable uses are IBOutlets and genuinely proven invariants with a comment.
- Capture lists (`[weak self]`) on every escaping closure that captures `self` in a class.
- Mark types `Sendable` deliberately; suppressing the warning with `@unchecked Sendable` requires a documented reason.
- SwiftUI views are cheap and disposable — put logic in the model, not the view body.
- Prefer `async let` for a fixed set of concurrent calls; use `TaskGroup` when the count is dynamic.
- Long-running work never runs on the main actor.

## Examples

**Actor-isolated cache with concurrent loading:**

```swift
actor ImageCache {
    private var cache: [URL: UIImage] = [:]
    private var inFlight: [URL: Task<UIImage, Error>] = [:]

    func image(for url: URL) async throws -> UIImage {
        if let cached = cache[url] { return cached }
        if let existing = inFlight[url] { return try await existing.value }

        let task = Task<UIImage, Error> {
            let (data, _) = try await URLSession.shared.data(from: url)
            guard let image = UIImage(data: data) else { throw CacheError.decodeFailed(url) }
            return image
        }
        inFlight[url] = task

        defer { inFlight[url] = nil }
        let image = try await task.value
        cache[url] = image
        return image
    }
}
```

## Notes

- The actor above deduplicates concurrent requests for the same URL — a common source of redundant network traffic in image-heavy screens.
- Strict concurrency checking is noisy on legacy code. Enable it target by target rather than repository-wide.
- `@Observable` (iOS 17+) replaces `ObservableObject` and only invalidates views that actually read the changed property.
