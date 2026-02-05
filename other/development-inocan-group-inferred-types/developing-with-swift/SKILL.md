---
name: developing-with-swift
description: Use when you work with Swift code or Xcode tooling - establishes style guidelines, teaches you vital Swift techniques, and how to use Xcode build tools
---

## Swift Styleguide

### Indentation

2 spaces, no tabs.

### Code comments & code documentation

If a comment contains documentation or explanation, it must use a triple slash
(`///`), regardless of its position in the source code.

Use double slash comments (`//`) only for Xcode directive comments ("MARK:",
"TODO:", etc.) and for temporarily disabling blocks of code. You must never use
double slash (`//`) for documentation comments.

### `guard` clauses

`guard` clauses must be written multi-line. If a clause combines multiple
conditions, each condition must be on its own line.

#### Examples

```swift
// ❌ Bad
guard somethingCondition else { return }

// ✅ Good
guard somethingCondition else {
  return
}

// ❌ Bad
guard !somethingCondition1, let something else { return }

// ✅ Good
guard !somethingCondition1,
      let something
else {
  return
}
```

Any `guard` clause must be followed by a blank line.

### `if` blocks

`if` clauses must be written multi-line. If a clause combines multiple
conditions, each condition should be on its own line. If there is more than one
condition, the opening bracket (`{`) should be on its own line.

#### Examples

```swift
// ❌ Bad
if !somethingCondition1, let something {
  return
}

// ✅ Good
if !somethingCondition1,
   let something
{
  return
}
```

### `switch/case`

Every `case` block must be followed by a blank line.


## Modern Swift

Write idiomatic SwiftUI code following Apple's latest architectural
recommendations and best practices.

### Core Philosophy

- SwiftUI is the default UI paradigm for Apple platforms - embrace its
  declarative nature
- Avoid legacy UIKit patterns and unnecessary abstractions
- Focus on simplicity, clarity, and native data flow
- Let SwiftUI handle the complexity - don't fight the framework

### Architecture Guidelines

#### 1. Embrace Native State Management

For simple use cases that don't contain a lot of logic and state, use SwiftUI's
built-in property wrappers appropriately:

- `@State` - Local, ephemeral view state
- `@Binding` - Two-way data flow between views
- `@Observable` - Shared state (iOS 17+)
- `@ObservableObject` - Legacy shared state (pre-iOS 17)
- `@Environment` - Dependency injection for app-wide concerns

For more complex use cases with lots of logic and interdependent states, use
[Composable Architecture](https://github.com/pointfreeco/swift-composable-architecture).
Before starting to write code, read the TCA documentation (see section 
_"Read SDK/ package/ library/ framework documentation"_).

#### 2. State Ownership Principles

- Views own their local state unless sharing is required
- State flows down, actions flow up
- Keep state as close to where it's used as possible
- Extract shared state only when multiple views need it

#### 3. Modern Async Patterns

- Use `async/await` as the default for asynchronous operations
- Leverage `.task` modifier for lifecycle-aware async work
- Avoid Combine unless absolutely necessary
- Handle errors gracefully with try/catch

#### 4. View Composition

- Build UI with small, focused views
- Extract reusable components naturally
- Use view modifiers to encapsulate common styling
- Prefer composition over inheritance

#### 5. Code Organization

- Organize by feature, not by type (avoid Views/, Models/, ViewModels/ folders)
- Keep related code together in the same file when appropriate
- Use extensions to organize large files
- Follow Swift naming conventions consistently

### Implementation Patterns

#### Simple State Example

```swift
struct CounterView: View {
  @State private var count = 0

  var body: some View {
    VStack {
      Text("Count: \(count)")
      Button("Increment") {
        count += 1
      }
    }
  }
}
```

#### Shared State with @Observable

```swift
@Observable
class UserSession {
  var isAuthenticated = false
  var currentUser: User?

  func signIn(user: User) {
    currentUser = user
    isAuthenticated = true
  }
}

struct MyApp: App {
  @State private var session = UserSession()

  var body: some Scene {
    WindowGroup {
      ContentView()
        .environment(session)
    }
  }
}
```

#### Async Data Loading

```swift
struct ProfileView: View {
  @State private var profile: Profile?
  @State private var isLoading = false
  @State private var error: Error?

  var body: some View {
    Group {
      if isLoading {
        ProgressView()
      } else if let profile {
        ProfileContent(profile: profile)
      } else if let error {
        ErrorView(error: error)
      }
    }
    .task {
      await loadProfile()
    }
  }

  private func loadProfile() async {
    isLoading = true
    defer { isLoading = false }

    do {
      profile = try await ProfileService.fetch()
    } catch {
      self.error = error
    }
  }
}
```

### Best Practices

#### Do

- Write self-contained views when possible
- Use property wrappers as intended by Apple
- Test logic in isolation, preview UI visually
- Handle loading and error states explicitly
- Keep views focused on presentation
- Use Swift's type system for safety

#### Do not

- Create ViewModels for every view
- Move state out of views unnecessarily
- Add abstraction layers without clear benefit
- Use Combine for simple async operations
- Fight SwiftUI's update mechanism
- Overcomplicate simple features

### Testing Strategy

- Unit test business logic and data transformations
- Use SwiftUI Previews for visual testing
- Test @Observable classes independently
- Keep tests simple and focused
- Don't sacrifice code clarity for testability

### Modern Swift Features

- Use Swift Concurrency (async/await, actors)
- Leverage Swift 6 data race safety when available, i.e. when the project is
  built with Swift 6 or later
- Utilize property wrappers effectively
- Embrace value types where appropriate
- Use protocols for abstraction, not just for testing

### Summary

Write SwiftUI code that looks and feels like SwiftUI. The framework has matured
significantly - trust its patterns and tools. Focus on solving user problems
rather than implementing architectural patterns from other platforms.


## Building Xcode projects

Pipe `xcodebuild` output directly to `xcsift` to get clean, readable results for
use by LLM:

```bash
xcodebuild [flags] 2>&1 | xcsift
```

Important: Always use `2>&1` to redirect STDERR to STDOUT. This ensures all
compiler errors, warnings, and build output are captured, removing noise and
providing clean, structured JSON output.
