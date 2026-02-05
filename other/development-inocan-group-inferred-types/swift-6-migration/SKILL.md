---
name: swift-6-migration
description: Use when encountering Swift 6 concurrency errors, Sendable conformance warnings, actor isolation issues, "global variable is not concurrency-safe" errors, or migrating codebases to Swift 6 language mode
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# Swift 6 Migration

## Overview

Swift 6 enforces data race safety at compile time. Migration involves making implicit isolation explicit and ensuring all shared state is thread-safe through Sendable conformance, actor isolation, or explicit synchronization.

## When to Use

**Symptoms that trigger this skill:**
- Compiler error: `global variable 'X' is not concurrency-safe`
- Compiler error: `cannot pass argument of non-sendable type`
- Compiler error: `actor-isolated property cannot be referenced from non-isolated context`
- Warning: `reference to var 'X' is not concurrency-safe`
- Warning: `type 'X' does not conform to the 'Sendable' protocol`
- Need to enable `-strict-concurrency=complete` or Swift 6 mode
- Migrating from GCD/DispatchQueue to async/await

**When NOT to use:**
- General Swift syntax questions (not concurrency-related)
- iOS/macOS API usage unrelated to concurrency
- Performance optimization without concurrency issues

## Quick Reference

| Problem | Solution |
|---------|----------|
| Mutable global var | Use `let`, isolate to `@MainActor`, or wrap in actor |
| Non-Sendable class | Add `Sendable` + `@unchecked Sendable`, or make an actor |
| Actor isolation error | Add `await`, use `nonisolated`, or annotate with `@MainActor` |
| Closure capturing non-Sendable | Use `@Sendable` closure, capture explicitly, or restructure |
| Legacy callback API | Wrap with `withCheckedContinuation` or `withCheckedThrowingContinuation` |
| Third-party non-Sendable types | Use `@preconcurrency import` as temporary workaround |

## Commands

```bash
# Check Swift version
swift --version

# Build with complete concurrency checking (warnings)
swift build -Xswiftc -strict-concurrency=complete

# Build in Swift 6 mode (errors)
swift build -Xswiftc -swift-version -Xswiftc 6
```

**Package.swift settings:**
```swift
// Enable strict concurrency per target
.target(
    name: "MyTarget",
    swiftSettings: [.enableExperimentalFeature("StrictConcurrency")]
)

// Or enable Swift 6 mode
swiftLanguageVersions: [.v6]
```

## Migration Strategy

1. **Enable warnings first** - Use `-strict-concurrency=complete` before Swift 6 mode
2. **Fix from leaves inward** - Start with types that have no dependencies, work up
3. **Group related fixes** - Sendable conformance often cascades through a module
4. **Test runtime behavior** - Some changes affect execution order

## Common Mistakes

| Mistake | Why It's Wrong | Better Approach |
|---------|----------------|-----------------|
| Adding `@unchecked Sendable` everywhere | Hides real data races | Analyze actual thread safety first |
| Using `nonisolated(unsafe)` without synchronization | Compiler trusts you but runtime doesn't | Only use with actual locks/queues protecting access |
| Wrapping everything in `Task { }` | Creates unnecessary concurrency | Use `await` at natural boundaries |
| Making all classes actors | Actors have overhead and change semantics | Use actors for shared mutable state only |
| Ignoring `@preconcurrency` warnings | Technical debt accumulates | Plan to address underlying issues |

## Reference Documentation

The [migration-guide.md](migration-guide.md) file contains Apple's complete migration documentation (25 bundled files). Key sections:

| Topic | Search Pattern |
|-------|----------------|
| Common errors | `FILE: Guide.docc/CommonProblems.md` |
| Data race safety | `FILE: Guide.docc/DataRaceSafety.md` |
| Incremental adoption | `FILE: Guide.docc/IncrementalAdoption.md` |
| Swift 6 mode | `FILE: Guide.docc/Swift6Mode.md` |
| Complete checking | `FILE: Guide.docc/CompleteChecking.md` |
| Sendable examples | `FILE: Sources/Examples/ConformanceMismatches.swift` |
| Global variable patterns | `FILE: Sources/Examples/Globals.swift` |

Use grep to find specific content: `grep -n "pattern" migration-guide.md`
