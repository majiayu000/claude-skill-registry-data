---
name: ios-fundamentals
description: Master iOS development foundations - Architecture, lifecycle, memory, concurrency
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 01-ios-fundamentals
bond_type: PRIMARY_BOND
last_updated: "2024-12"
---

# iOS Fundamentals Skill

> Build rock-solid foundations for iOS development

## Learning Objectives

By completing this skill, you will:
- Understand iOS app lifecycle and state management
- Master architectural patterns (MVC, MVVM, Clean)
- Implement memory-safe code with ARC
- Use modern Swift concurrency (async/await, actors)
- Apply dependency injection patterns

## Prerequisites

| Requirement | Level |
|-------------|-------|
| Swift basics | Intermediate |
| Xcode familiarity | Basic |
| OOP concepts | Solid |

## Curriculum

### Module 1: App Lifecycle (4 hours)

**Topics:**
- `UIApplicationDelegate` methods
- `SceneDelegate` for multi-window (iOS 13+)
- SwiftUI App lifecycle (`@main`, `ScenePhase`)
- State transitions: Active → Inactive → Background → Suspended

**Code Example:**
```swift
.onChange(of: scenePhase) { oldPhase, newPhase in
    switch newPhase {
    case .active: resumeActivities()
    case .inactive: pauseActivities()
    case .background: saveState()
    @unknown default: break
    }
}
```

### Module 2: Architecture Patterns (6 hours)

**Pattern Comparison:**

| Pattern | Complexity | Testability | Team Size |
|---------|------------|-------------|-----------|
| MVC | Low | Poor | 1-2 |
| MVVM | Medium | Good | 2-5 |
| Clean/VIP | High | Excellent | 5+ |

### Module 3: Memory Management (4 hours)

**Topics:**
- ARC fundamentals
- Weak/unowned references
- Retain cycle prevention
- Instruments profiling

### Module 4: Swift Concurrency (6 hours)

**Topics:**
- async/await basics
- Task and TaskGroup
- Actors and Sendable
- MainActor for UI

### Module 5: Dependency Injection (3 hours)

**Topics:**
- Constructor injection
- Protocol-oriented design
- Testing with mocks

## Assessment Criteria

| Criteria | Weight |
|----------|--------|
| Architecture understanding | 30% |
| Memory management | 25% |
| Concurrency implementation | 25% |
| Code quality & patterns | 20% |

## Skill Validation

1. **State Machine App**: Proper lifecycle handling
2. **MVVM Refactor**: Convert MVC to MVVM
3. **Concurrent Downloader**: async/await image loader
