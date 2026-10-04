---
name: swift
description: "Write Swift with optionals, value types, protocols, async/await, and actors; manage state in SwiftUI workflows."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["swift", "async-await", "swiftui", "ios", "actors", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Swift Language AI Skill Guide

## Overview & Engine Architecture

Swift emphasizes safe value semantics (`struct`/`enum`), optionals instead of null, and structured concurrency (`async`/`await`, `Task`, `actor`). Agents prefer value types for models, isolate mutable shared state in actors, avoid force-unwraps, and keep SwiftUI views thin by moving logic into models/observables.

```
Task / async call
      |
  await suspension
      |
  actor-isolated state (optional)
      |
  UI update on MainActor
```

## When to use this skill

- Writing iOS/macOS application logic in Swift
- Adopting async/await over completion handlers
- Designing protocols and generics idiomatically
- Fixing data races and main-thread UI violations

## Operational directives

1. Prefer `struct` + `Codable` for models; use `class` when identity/sharing is required.
2. Mark UI-facing models `@MainActor` when they publish to SwiftUI.
3. Use `async throws` APIs; map errors at the boundary for user display.
4. Avoid `!` force unwraps; use `guard let` / `if let` / nil-coalescing deliberately.
5. Sendable-check shared concurrent data; use actors for mutable isolation.

## Async sketch

```swift
struct Item: Identifiable, Codable, Sendable {
  let id: String
  let sku: String
  let qty: Int
}

enum ItemsError: Error {
  case invalidResponse
}

actor ItemStore {
  private var cache: [Item] = []

  func load(from url: URL) async throws -> [Item] {
    let (data, response) = try await URLSession.shared.data(from: url)
    guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
      throw ItemsError.invalidResponse
    }
    let items = try JSONDecoder().decode([Item].self, from: data)
    cache = items
    return items
  }
}
```

## Commands

```bash
swift build
swift test
xcodebuild -scheme Inventory -destination 'platform=iOS Simulator,name=iPhone 16' test
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| UI updates off main actor | Crashes / warnings | `@MainActor` |
| Retain cycles in closures | Leaks | `[weak self]` |
| Overusing classes | Unexpected sharing | Value types |
| Swallowing errors as optional | Silent failures | Propagate `throws` |

## Best practices

- Use `Result` only when bridging non-throwing APIs; prefer `throws` in new code.
- Prefer protocol existential erasure carefully - generics often clearer.
- Keep access control (`internal`/`public`) intentional for modules.
- Write XCTest/Swift Testing coverage for parsing and state transitions.

## Limitations

- ABI/module stability matters when shipping binary frameworks.
- Swift Concurrency migration from GCD can be gradual and mixed.
- Server-side Swift exists but differs from Apple platform tooling.

## Related skills

- `@xcode-ios` - Xcode signing, schemes, archives
- `@kotlin` - peer language for Android
- `@firebase` - common iOS backend SDKs
