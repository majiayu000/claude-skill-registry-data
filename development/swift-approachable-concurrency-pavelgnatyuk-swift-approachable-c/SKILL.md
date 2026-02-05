---
name: swift-approachable-concurrency
description: Expert guidance on Swift 6.2 Approachable Concurrency for iOS 26+. Use when working with async/await, Tasks, actors, MainActor, Sendable, isolation domains, migrating to Swift 6, fixing concurrency compiler errors, or understanding @concurrent. Provides mental models, migration strategies, and safe concurrent Swift patterns.
---

# Swift 6.2 Approachable Concurrency Guide

Expert guidance on Swift's concurrency system for iOS 26+ apps.

## Core Mental Model: The Office Building

Think of your app as an office building where **isolation domains** are private offices with locks:

- **MainActor** = Front desk (handles all UI interactions, only one exists)
- **actor** types = Department offices (each protects its own data)
- **nonisolated** code = Hallways (shared space, no private documents)
- **Sendable** types = Photocopies (safe to share between offices)
- **Non-Sendable** types = Original documents (must stay in one office)

You can't barge into someone's office. You knock (`await`) and wait.

## The Core Shift: "Stay on the Caller"

**Swift 6.0**: Non-isolated `async` functions ran on the global background executor.
**Swift 6.2**: Non-isolated `async` functions inherit the caller's isolation by default.

```swift
// Swift 6.0 - needed manual MainActor.run
func loadData() async {
    let result = await fetchData()
    await MainActor.run { self.items = result }  // Required!
}

// Swift 6.2 - stays on caller
func loadData() async {
    let result = await fetchData()
    self.items = result  // Safe! Inherits MainActor from caller
}
```

## Async/Await

An `async` function can pause. Use `await` to suspend until work finishes. For parallel work, use `async let`:

```swift
async let avatar = fetchImage("avatar.jpg")
async let banner = fetchImage("banner.jpg")
return Profile(avatar: try await avatar, banner: try await banner)
```

## Tasks: Managed vs Unmanaged

### ⚠️ Unmanaged Tasks Are an Anti-Pattern

Tasks created with `Task { }` or `Task.detached { }` are **unmanaged** — you can't cancel them, know when they finish, or access results.

```swift
// ❌ BAD - unmanaged
Task { await fetchUsers() }

// ✅ GOOD - SwiftUI managed, auto-cancels
.task { avatar = await downloadAvatar() }

// ✅ GOOD - restarts when ID changes
.task(id: userID) { avatar = await downloadAvatar(for: userID) }

// ✅ GOOD - structured parallel work
async let users = fetchUsers()
async let posts = fetchPosts()
let (u, p) = await (users, posts)

// ✅ GOOD - dynamic parallel work
try await withThrowingTaskGroup(of: Void.self) { group in
    group.addTask { avatar = try await downloadAvatar() }
    group.addTask { bio = try await fetchBio() }
}
```

**When `Task { }` is acceptable**: Button taps where `.task(id:)` is impractical.

## Isolation Domains

Swift asks "**who can access this data?**" not "which thread?".

### MainActor
For UI. Everything UI-related should be here:
```swift
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
}
```

### Actors
Protect their own mutable state with exclusive access:
```swift
actor BankAccount {
    var balance: Double = 0
    func deposit(_ amount: Double) { balance += amount }
}
await account.deposit(100)  // Must await from outside
```

**When to create an actor** (Matt Massicotte's rule):
1. You have non-`Sendable` state
2. Operations must be atomic
3. Those operations can't run on an existing actor

If you can't justify all three → use `@MainActor` instead.

### Nonisolated
Opts out of actor isolation. Cannot access actor's protected state:
```swift
actor BankAccount {
    nonisolated func bankName() -> String { "Acme Bank" }
}
```

## Isolation Inheritance

With Approachable Concurrency, isolation flows from MainActor through your code:
- **Functions**: Inherit caller's isolation unless explicitly marked
- **Closures**: Inherit from context where defined
- **Task { }**: Inherits actor isolation from creation site
- **Task.detached { }**: No inheritance (avoid it)

## Build Settings

| Setting | Swift 5 Mode | Swift 6 Mode |
|---------|--------------|--------------|
| Language Version | Swift 5 | Swift 6 |
| Strict Concurrency | Complete | (default) |
| Approachable Concurrency | Yes | Yes |
| Default Actor Isolation | MainActor | MainActor |

**Swift 5**: Concurrency issues are warnings (gradual migration).
**Swift 6**: Concurrency issues are errors (full safety).

For detailed migration steps, see [references/migration-checklist.md](references/migration-checklist.md).

## New Keywords (iOS 26 / Swift 6.2)

```swift
@concurrent           // Force background execution
func heavyWork() async -> Result { }

sending               // Transfer non-Sendable safely  
func create() async -> sending NonSendableType { }

nonisolated(nonsending)  // Inherit caller isolation (now default)

Task(name: "debug-id")   // Named tasks for debugging
```

## Sendable

Marks types safe to pass across isolation boundaries.

**Automatically Sendable**: Structs/enums with Sendable properties, Actors, @MainActor types.

```swift
// ✅ Sendable - value type
struct User: Sendable { let id: Int; let name: String }

// ❌ Non-Sendable - mutable class
class Counter { var count = 0 }

// ⚠️ Use sparingly - compiler won't verify
final class ThreadSafeCache: @unchecked Sendable { }
```

## Common Patterns

```swift
@MainActor
final class PhotoViewModel: ObservableObject {
    @Published var photos: [Photo] = []
    
    func loadPhotos() async {
        let data = await networkService.fetchPhotos()
        let processed = await processPhotos(data)
        photos = processed
    }
}

@concurrent
private func processPhotos(_ data: [Data]) async -> [Photo] {
    data.compactMap { Photo(data: $0) }
}
```

## Common Mistakes

For detailed error messages and fixes, see [references/troubleshooting.md](references/troubleshooting.md).

| Mistake | Fix |
|---------|-----|
| Thinking async = background | Use `@concurrent` for CPU-heavy work |
| Creating too many actors | Use `@MainActor` unless you need isolated state |
| Unnecessary `MainActor.run` | Annotate function with `@MainActor` instead |
| Blocking cooperative pool | Never use `DispatchSemaphore.wait()` in async code |
| Unmanaged `Task { }` | Use `.task`, `async let`, or `TaskGroup` |
| Overusing `@unchecked Sendable` | Use `sending` or make properly Sendable |

## Quick Reference

| Keyword | Purpose |
|---------|---------|
| `async` / `await` | Pause and resume |
| `.task { }` | SwiftUI managed, auto-cancels |
| `async let` | Parallel work |
| `TaskGroup` | Dynamic parallel work |
| `@MainActor` | Main thread isolation |
| `actor` | Custom isolation domain |
| `nonisolated` | Opt out of isolation |
| `Sendable` | Safe to cross boundaries |
| `@concurrent` | Force background (Swift 6.2) |
| `sending` | Transfer non-Sendable (Swift 6.2) |

## When the Compiler Complains

Trace the isolation:
1. Where did the isolation come from?
2. Where is the code trying to run?
3. What data is crossing a boundary?

## Skill References

- [references/migration-checklist.md](references/migration-checklist.md) - Step-by-step migration guide
- [references/migration-examples.md](references/migration-examples.md) - Before/after code examples
- [references/troubleshooting.md](references/troubleshooting.md) - Common errors and fixes

## External References

- [Fucking Approachable Swift Concurrency](https://fuckingapproachableswiftconcurrency.com) - Mental models
- [Matt Massicotte's Blog](https://www.massicotte.org/) - Deep expertise
- [Swift Concurrency Docs](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/)

### Swift Evolution Proposals

- [SE-0461](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md) - Async function isolation
- [SE-0430](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md) - sending parameters
- [SE-0466](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-infer-main-actor-by-default.md) - Default MainActor inference
- [SE-0470](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0470-isolated-protocol-conformances.md) - Isolated conformances
