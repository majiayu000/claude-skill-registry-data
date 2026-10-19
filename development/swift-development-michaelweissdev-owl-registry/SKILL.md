---
name: swift-development
description: >
  Architect, implement, and test modern Swift applications (Swift 5.9 / 6.0)
  following the official Swift API Design Guidelines. Use when designing value
  types with structs, implementing protocols and extensions, applying Swift
  concurrency (async/await, Actors, Sendable), configuring Package.swift, or writing
  unit tests with XCTest or Swift Testing.
compatibility: >
  Agent Skills-compatible coding agents operating on Swift 5.9+ / 6.0 codebases
  with the Swift toolchain.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "swift, ios, macos, concurrency, actors, spm, protocols, value-types"
  topics: "programming-languages, software-development"
---

# Modern Swift Development

Swift is a type-safe, expressive, and high-performance language. Modern Swift development adheres to the [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/), embraces **Value Semantics** (structs over classes), leverages protocol-oriented programming, and ensures data-race safety with **Swift Concurrency** and **Actors**.

## Core Rules

1. **Follow the Swift API Design Guidelines**: Strive for clarity at the point of call. Omit needless words, name functions after side effects (`sort()` mutating vs `sorted()` returning a copy), and label arguments intuitively.
2. **Prefer structs (Value Types) over classes (Reference Types)**: Use `struct` by default; use `class` only when identity, lifecycle management, or Objective-C interoperability is explicitly required.
3. **Never force-unwrap (`!`)**: Use `guard let`, `if let`, or nil-coalescing (`??`) to unwrap optionals safely.
4. **Use Actors for thread-safe mutable state**: Eliminate manual lock management and data races by encapsulating shared state inside `actor` types.
5. **Comply with `Sendable` requirements**: In Swift 6 mode, types crossing concurrency boundaries must be proven thread-safe at compile time.
6. **Use Swift Package Manager (SPM)**: Manage dependencies and targets declaratively in `Package.swift`.

---

## 1. Idiomatic Unwrapping and Value Types

```swift
import Foundation

public struct UserAccount: Identifiable, Equatable, Sendable {
    public let id: UUID
    public let username: String
    public let email: String?

    public init(id: UUID = UUID(), username: String, email: String? = nil) {
        self.id = id
        self.username = username
        self.email = email
    }
}

// Guard let for early exit
public func formatUserBadge(user: UserAccount?) -> String {
    guard let user else {
        return "Anonymous Guest"
    }

    let contactInfo = user.email ?? "No email provided"
    return "\(user.username) (\(contactInfo))"
}
```

---

## 2. Modern Swift Concurrency & Actors

### Actors (Data-Race Free Mutable State)
```swift
public actor SessionCache {
    private var tokens: [String: Date] = [:]

    public func store(token: String, expiresAt: Date) {
        tokens[token] = expiresAt
    }

    public func isValid(token: String) -> Bool {
        guard let expiration = tokens[token] else { return false }
        return expiration > Date()
    }
}
```

### Structured Concurrency with `TaskGroup`
```swift
public func fetchAllMetrics(endpoints: [URL]) async throws -> [MetricResult] {
    try await withThrowingTaskGroup(of: MetricResult.self) { group in
        for url in endpoints {
            group.addTask {
                let (data, _) = try await URLSession.shared.data(from: url)
                return try JSONDecoder().decode(MetricResult.self, from: data)
            }
        }

        var results: [MetricResult] = []
        for try await metric in group {
            results.append(metric)
        }
        return results
    }
}
```

---

## 3. Declarative Package Manifest (`Package.swift`)

```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "DataPipeline",
    platforms: [
        .macOS(.v13),
        .iOS(.v16)
    ],
    products: [
        .library(name: "DataPipeline", targets: ["DataPipeline"])
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-algorithms.git", from: "1.2.0")
    ],
    targets: [
        .target(
            name: "DataPipeline",
            dependencies: [
                .product(name: "Algorithms", package: "swift-algorithms")
            ]
        ),
        .testTarget(
            name: "DataPipelineTests",
            dependencies: ["DataPipeline"]
        )
    ]
)
```

---

## 4. Testing with Swift Testing or XCTest

```swift
import XCTest
@testable import DataPipeline

final class UserAccountTests: XCTestCase {
    func testBadgeFormattingWithValidUser() {
        let user = UserAccount(username: "michael", email: "dev@example.com")
        let badge = formatUserBadge(user: user)
        XCTAssertEqual(badge, "michael (dev@example.com)")
    }

    func testBadgeFormattingWithNilUserReturnsGuest() {
        let badge = formatUserBadge(user: nil)
        XCTAssertEqual(badge, "Anonymous Guest")
    }
}
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| `val = optional!` | Crashes with fatal runtime exception if nil | Use `guard let val else { return }` |
| Overusing `class` for simple data models | Unintended shared mutation side-effects | Use `struct` with immutable properties |
| Retain cycles in closures (`[weak self]`) | Memory leaks due to circular reference counting | Capture `[weak self]` in escaping closures |
| Modifying state across threads without an Actor | Data races and memory corruption | Enclose mutable state in an `actor` |
| Unnamed boolean parameters: `load(true)` | Unreadable at point of call | Use argument labels: `load(allowCache: true)` |

---

## 6. Verification Checklist

- [ ] Zero force-unwraps (`!`) in non-test source code.
- [ ] Conforms to Swift API Design Guidelines (checked with `swift-format`).
- [ ] No data races reported under strict concurrency checking (`-strict-concurrency=complete`).
- [ ] Builds and passes tests via `swift test`.
- [ ] `Package.swift` builds cleanly with zero warnings.
