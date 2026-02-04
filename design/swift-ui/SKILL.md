---
name: swift-ui
description: SwiftUI implementation patterns for building polished iOS/macOS apps. Use when building views, managing state, creating layouts, implementing animations, or structuring app architecture in SwiftUI.
---

# swift-ui

SwiftUI implementation patterns for building distinctive iOS and macOS interfaces.

## Scope

This skill covers **SwiftUI implementation**—the views, modifiers, state management, and patterns needed to build polished native apps. For design theory (typography, color, hierarchy), see `design-principles`. For App Store submission, see `design-review`.

## Routing

Based on what you're building, I'll reference the appropriate implementation guide:

### View Composition
**When**: Building views, applying modifiers, structuring components
**Reference**: `references/views.md`
- View composition patterns
- Modifier ordering
- Custom view modifiers
- ViewBuilder and generics

### State Management
**When**: Managing data flow, handling state
**Reference**: `references/state.md`
- Property wrappers (@State, @Binding, @StateObject, etc.)
- Data flow patterns
- Observable objects
- Environment values

### Layout Patterns
**When**: Creating layouts, grids, responsive design
**Reference**: `references/layout.md`
- Stack patterns (VStack, HStack, ZStack)
- LazyStacks and LazyGrids
- GeometryReader and layout priorities
- Adaptive layouts

### Animation
**When**: Adding motion, transitions, gestures
**Reference**: `references/animation.md`
- Implicit vs explicit animation
- Transitions
- Spring animations
- Gesture-driven animation

### Accessibility
**When**: VoiceOver, Dynamic Type, accessibility
**Reference**: `references/accessibility.md`
- Accessibility modifiers
- VoiceOver optimization
- Dynamic Type support
- Accessibility traits and actions

### Architecture (No MVVM)
**When**: App structure, data flow patterns, questioning if you need ViewModels
**Reference**: `references/architecture.md`
- Views as pure state expressions
- Environment for dependency injection
- `.task(id:)` and `.onChange()` as mini reducers
- SwiftData direct-in-view patterns
- Testing strategies without ViewModels

### Data Persistence (SwiftData)
**When**: Storing data locally, Core Data replacement, iOS 17+
**Reference**: `references/swiftdata.md`
- @Model macro for defining entities
- @Query for reactive data fetching in views
- ModelContainer and ModelContext setup
- Relationships, predicates, migrations
- Direct SwiftUI integration (no ViewModel layer)

## Quick Reference

### Essential Patterns

```swift
// MARK: - View Composition

struct ContentView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                ItemRow(item: item)
            }
            .navigationTitle("Items")
        }
    }
}

// MARK: - State Management (No ViewModel needed)

struct ItemDetailView: View {
    @Environment(APIClient.self) private var client
    @Environment(\.dismiss) private var dismiss
    @State private var item: Item?

    var body: some View {
        Form {
            // content
        }
        .task { await loadItem() }
    }
}

// MARK: - Animation

Button("Animate") {
    withAnimation(.spring(response: 0.3, dampingFraction: 0.6)) {
        isExpanded.toggle()
    }
}
```

### HIG Quick Reference

| Element | iOS Standard |
|---------|-------------|
| Touch target | 44pt minimum |
| Navigation bar | 44pt height |
| Tab bar | 49pt height |
| Toolbar | 44pt height |
| Corner radius | 10-20pt for cards |
| Standard margin | 16pt |

### Color System

```swift
// Use semantic colors
Color.primary       // Adapts to dark mode
Color.secondary
Color.accentColor
Color(uiColor: .systemBackground)
Color(uiColor: .secondarySystemBackground)
```

## Anti-Patterns

- Force unwrapping in views
- Massive view bodies (extract into subviews, not ViewModels)
- Business logic in views (move to services in Environment)
- Ignoring @MainActor for UI updates
- Not supporting Dynamic Type
- Hardcoded colors instead of semantic
- Using ViewModels when @State + Environment suffices

## Related Skills

- **swift-lang** - Swift language features (macros, concurrency, testing)
- **design-principles** - Theory behind the choices
- **web-design** - Web/CSS implementation
- **design-review** - App Store submission prep
