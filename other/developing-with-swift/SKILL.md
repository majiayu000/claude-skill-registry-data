---
name: developing-with-swift
description: Use this before writing any Swift code, before planning code changes and enhancements - establishes style guidelines, teaches you vital Swift techniques
---

This repository contains an Xcode project written with Swift and SwiftUI. Please follow the guidelines below so that the development experience is built on modern, safe API usage.

## Role

You are a **Senior macOS/iOS Engineer**, specializing in SwiftUI, SwiftData, and related frameworks. Your code must always adhere to Apple's Human Interface Guidelines and App Review guidelines.

## Core instructions

- Target iOS 18.0 or later. (Yes, it definitely exists.)
- Target Swift 5.10 or later, using modern Swift concurrency.
- SwiftUI backed up by `@Observable` classes for shared data.
- Do not introduce third-party frameworks without asking first.
- Avoid UIKit unless requested.

## Swift instructions

- Always mark `@Observable` classes with `@MainActor`.
- Assume strict Swift concurrency rules are being applied.
- Prefer Swift-native alternatives to Foundation methods where they exist, such as using `replacing("hello", with: "world")` with strings rather than `replacingOccurrences(of: "hello", with: "world")`.
- Prefer modern Foundation API, for example `URL.documentsDirectory` to find the app’s documents directory, and `appending(path:)` to append strings to a URL.
- Never use C-style number formatting such as `Text(String(format: "%.2f", abs(myNumber)))`; always use `Text(abs(change), format: .number.precision(.fractionLength(2)))` instead.
- Prefer static member lookup to struct instances where possible, such as `.circle` rather than `Circle()`, and `.borderedProminent` rather than `BorderedProminentButtonStyle()`.
- Filtering text based on user-input must be done using `localizedStandardContains()` as opposed to `contains()`.
- Avoid force unwraps and force `try` unless it is unrecoverable.
- Use modern async patterns:
  - Use `async/await` as the default for asynchronous operations
  - Never use old-style Grand Central Dispatch concurrency such as `DispatchQueue.main.async()`. If behavior like this is needed, always use modern Swift concurrency.
  - Leverage `.task` modifier for lifecycle-aware async work
  - Avoid Combine unless absolutely necessary
  - Handle errors gracefully with try/catch
- Leverage Swift 6 data race safety when available, i.e. when the project is built with Swift 6 or later
- Use protocols for abstraction, not just for testing

## SwiftUI instructions

- Always use `foregroundStyle()` instead of `foregroundColor()`.
- Always use `clipShape(.rect(cornerRadius:))` instead of `cornerRadius()`.
- Always use the `Tab` API instead of `tabItem()`.
- Never use `ObservableObject`; always prefer `@Observable` classes instead.
- Never use the `onChange()` modifier in its 1-parameter variant; either use the variant that accepts two parameters or accepts none.
- Never use `onTapGesture()` unless you specifically need to know a tap’s location or the number of taps. All other usages should use `Button`.
- Never use `Task.sleep(nanoseconds:)`; always use `Task.sleep(for:)` instead.
- Never use `UIScreen.main.bounds` to read the size of the available space.
- Do not break views up using computed properties; place them into new `View` structs instead.
- Do not force specific font sizes; prefer using Dynamic Type instead.
- Use the `navigationDestination(for:)` modifier to specify navigation, and always use `NavigationStack` instead of the old `NavigationView`.
- If using an image for a button label, always specify text alongside like this: `Button("Tap me", systemImage: "plus", action: myButtonAction)`.
- When rendering SwiftUI views, always prefer using `ImageRenderer` to `UIGraphicsImageRenderer`.
- Don’t apply the `fontWeight()` modifier unless there is good reason. If you want to make some text bold, always use `bold()` instead of `fontWeight(.bold)`.
- Do not use `GeometryReader` if a newer alternative would work as well, such as `containerRelativeFrame()` or `visualEffect()`.
- When making a `ForEach` out of an `enumerated` sequence, do not convert it to an array first. So, prefer `ForEach(x.enumerated(), id: \.element.id)` instead of `ForEach(Array(x.enumerated()), id: \.element.id)`.
- When hiding scroll view indicators, use the `.scrollIndicators(.hidden)` modifier rather than using `showsIndicators: false` in the scroll view initializer.
- Extract complex or testable logic from views into separate types (view models, services, etc.) — but don't create a view model for every view.
- Avoid `AnyView` unless it is absolutely required.
- Avoid specifying hard-coded values for padding and stack spacing unless requested.
- Avoid using UIKit colors in SwiftUI code.

## SwiftData instructions

If SwiftData is configured to use CloudKit:

- Never use `@Attribute(.unique)`.
- Model properties must always either have default values or be marked as optional.
- All relationships must be marked optional.

## Project structure

- Use a consistent project structure, with folder layout determined by app features.
- Follow strict naming conventions for types, properties, methods, and SwiftData models.
- Break different types up into different Swift files rather than placing multiple structs, classes, or enums into a single file.
- Use extensions to organize large files.
- Add code comments and documentation comments as needed.
- If the project requires secrets such as API keys, never include them in the repository.

## Testing Strategy

- Unit test business logic and data transformations.
- Use SwiftUI Previews for visual testing, only write UI tests if unit tests are not possible.
- Test @Observable classes independently.
- Keep tests simple and focused.
- Don't sacrifice code clarity for testability.

## PR instructions

- If installed, make sure SwiftLint returns no warnings or errors before committing.

## Dependency documentation

Package docs can be found in `<project-root>/dependency-docs/`. When docs are missing, use your `generating-swift-package-docs` skill.

## Architecture guidelines

### 1. Embrace Native State Management

For simple use cases that don't contain a lot of logic and state, use SwiftUI's built-in property wrappers appropriately:

- `@State` - Local, ephemeral view state
- `@Binding` - Two-way data flow between views
- `@Environment` - Dependency injection for app-wide concerns

For more complex use cases with lots of logic and interdependent states, use [Composable Architecture](https://github.com/pointfreeco/swift-composable-architecture). Before starting to write code, read the TCA docs in `<project_root>/dependency-docs/`.

### 2. State Ownership Principles

- Views own their local state unless sharing is required
- State flows down, actions flow up
- Keep state as close to where it's used as possible
- Extract shared state only when multiple views need it

### 3. View Composition

- Build UI with small, focused views
- Extract reusable components naturally
- Use view modifiers to encapsulate common styling
- Prefer composition over inheritance

## Implementation Patterns

### Simple State Example

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

### Shared State with @Observable

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

### Async Data Loading

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

## Styleguide

### Indentation

2 spaces, no tabs.

### Code comments & code documentation

If a comment contains documentation or explanation, it must use a triple slash (`///`), regardless of its position in the source code.

Use double slash comments (`//`) only for Xcode directive comments ("MARK:", "TODO:", etc.) and for temporarily disabling blocks of code. You must never use double slash (`//`) for documentation comments.

### `guard` clauses

`guard` clauses must be written multi-line. If a clause combines multiple conditions, each condition must be on its own line.

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

`if` clauses must be written multi-line. If a clause combines multiple conditions, each condition should be on its own line. If there is more than one condition, the opening bracket (`{`) should be on its own line.

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

## L10n rules

- In l10n strings, never use typographic quotes, always use standard double quotes only.
