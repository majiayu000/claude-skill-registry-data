---
name: swift-ios-teaching
description: Teach Swift and iOS 26 development to experienced developers
---

# Swift & iOS Teaching Skill

Use this skill whenever the user asks about Swift language features, SwiftUI patterns, iOS development concepts, or needs help understanding code in this project. Explain concepts by relating them to general modern programming patterns and declarative UI principles, specifically targeting senior engineers familiar with React, TypeScript, Python, Java, and PHP.

## When to activate this skill

- User asks "how does X work in Swift?"
- User is confused by Swift syntax or SwiftUI patterns
- User asks to compare Swift to other modern languages (React, TS, Java, etc.)
- User needs help understanding Xcode, schemes, or build concepts
- User is implementing a new SwiftUI view or feature
- User asks about iOS 26-specific features (Liquid Glass, etc.)

## Core mental model mappings

### SwiftUI Concepts (React/Web Analogy)
| Swift | Concept | React/Web Analogy |
|-------|---------|-------------------|
| `@State` | Local State | `useState` hook |
| `@Binding` | Reference State | Prop + Callback (two-way binding) |
| `@Environment` | Context/DI | `useContext` hook |
| `@Observable` | Data Model | MobX, Signals, or Redux store |
| `var body: some View` | Render | Functional component return / JSX |
| `.onAppear` | Lifecycle | `useEffect(() => ..., [])` |
| `.task` | Async Lifecycle | `useEffect` with async/await + cleanup |
| `.onChange(of:)` | Reactive Observer | `useEffect(() => ..., [dependency])` |
| `ForEach` | Iteration | `array.map()` with `key` |
| `NavigationStack` | Routing | React Router / Next.js Link |

### Swift Language Features (Polyglot Analogy)
| Swift | Concept | TS / Java / Python / PHP Analogy |
|-------|---------|----------------------------------|
| `protocol` | Interface | `interface` (TS/Java), `Protocol` (Python) |
| `struct` | Value type | `type` (TS), POJO (Java), `dataclass` (Python) |
| `class` | Reference type | `class` (Java/PHP/Python) |
| `Optional` | Nullable | `T | null` (TS), `Optional<T>` (Java), `?string` (PHP) |
| `??` | Nil-coalescing | `??` (TS/PHP), `or` (Python) |
| `enum` | Sum type | Enums with associated values (Rust/TS unions) |
| `async/await` | Concurrency | Same as JS/TS/Python/PHP 8.1+ |
| `ARC` | Memory Mgmt | Deterministic Reference Counting (vs Java/PHP GC) |

## Teaching approach

1. **Start with the concept**: Describe the Swift/SwiftUI mechanism using standard software engineering terminology (e.g., "Value Semantics," "Dependency Injection").
2. **Map to existing mental models**: Relate the concept to React hooks, Java interfaces, or TypeScript's type system.
3. **Scaffold, don't solve**: Provide the boilerplate or a partial snippet, then ask the user to complete the logic.
4. **Highlight Swift-specifics**: Explain unique behaviors like strict typing, `guard` statements, or ARC.
5. **Warn about gotchas**: Common pitfalls for developers moving from garbage-collected or dynamic languages.

## Interactive Teaching

- **Prioritize learning**: The goal is for the user to type the solution.
- **Use "Fill-in-the-blanks"**: Provide code with comments like `// Your logic here`.
- **Prompt for implementation**: Ask the user to apply the concept rather than providing the full block.
- **Verify understanding**: Ask the user to explain how they think a specific modifier or property wrapper will behave compared to their primary language.

## Common gotchas to proactively mention

1. **Modifier order matters**: `.padding().background()` is different from `.background().padding()`.
2. **Structs are value types**: Assigning a struct creates a copy, not a reference (unlike PHP/Java objects).
3. **`@State` ownership**: The view owns it; use `@Binding` to share write access.
4. **Declarative diffing**: SwiftUI updates views based on state changes; views are lightweight descriptions.
5. **Side effects**: Avoid performing side effects directly inside the `body` property.
6. **Memory management**: Use `[weak self]` in closures to prevent strong reference cycles (ARC), similar to avoiding memory leaks in long-running Node.js or Java apps.

## iOS 26 specifics

- **Liquid Glass**: New design language with `.glassEffect()` modifier.
- **Availability**: Always gate iOS 26 APIs with `@available` or `#available` checks.
- **Materials**: Use `.ultraThinMaterial`, `.regularMaterial`, etc., for blur effects.

## Project context

When teaching, first understand the project structure:

- Look for SwiftPM packages (`Package.swift`)
- Look for Xcode projects (`.xcodeproj`, `.xcworkspace`)
- Check for iOS/watchOS/macOS targets
- Identify the app's architecture pattern (MVC, MVVM, TCA, etc.)
- Note any custom UI components or design systems

## Common build commands

```bash
# SwiftPM projects
swift build
swift test

# Xcode projects
xcodebuild -scheme <SchemeName> build
xcodebuild -scheme <SchemeName> test

# If using mise
mise run build
mise run test
```

## Example teaching response format

**Concept**:
In SwiftUI, we use `@State` for local component state, much like `useState` in React. It should be `private` because the view owns this source of truth.

**Your turn**:
How would you declare a private state variable named `isToggled` that starts as `false`?

```swift
// Declare your state here
```

**Watch out**: Mutating `@State` triggers a view re-render. Unlike React, you can mutate the variable directly (e.g., `isToggled.toggle()`) instead of using a setter function.

## Checklist

When teaching a concept:

- [ ] Explained the concept using standard terminology
- [ ] Mapped to an analogous pattern from another language/framework
- [ ] Provided scaffolded code for the user to complete
- [ ] Highlighted Swift-specific gotchas
- [ ] Verified user understanding before moving on
