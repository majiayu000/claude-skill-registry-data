---
name: swiftui-ui-patterns
description: Best practices and patterns for building SwiftUI views and components. Use when creating or refactoring SwiftUI UI, designing tab architecture, composing screens, or needing component-specific guidance.
---

# SwiftUI UI Patterns

## Quick Start

### Existing Project
1. Identify the feature and primary interaction model (list, detail, editor, settings, tabbed)
2. Find nearby examples in the repo with `rg "TabView\("` or similar
3. Apply local conventions: prefer SwiftUI-native state, keep state local
4. Build with small, focused subviews and SwiftUI-native data flow

### New Project Scaffolding
1. Wire TabView + NavigationStack + sheets
2. Add minimal `AppTab` enum and `RouterPath`
3. Expand route and sheet enums as new screens are added

## General Rules

- Use modern SwiftUI state (`@State`, `@Binding`, `@Observable`, `@Environment`)
- Avoid unnecessary view models - prefer MV (Model-View) over MVVM
- Prefer composition; keep views small and focused
- Use async/await with `.task` and explicit loading/error states
- Follow the project's formatter and style guide

### Sheets Best Practices
- Prefer `.sheet(item:)` over `.sheet(isPresented:)` when state represents a selected model
- Avoid `if let` inside a sheet body
- Sheets should own their actions and call `dismiss()` internally

## Workflow for a New SwiftUI View

1. Define the view's state and its ownership location
2. Identify dependencies to inject via `@Environment`
3. Sketch the view hierarchy and extract repeated parts into subviews
4. Implement async loading with `.task` and explicit state enum if needed
5. Add accessibility labels or identifiers for interactive UI
6. Validate with a build and update usage callsites if needed

## MV Pattern (Preferred over MVVM)

SwiftUI views should be lightweight state expressions. Avoid ViewModels unless truly necessary.

```swift
struct FeedView: View {
    @Environment(APIClient.self) private var client

    enum ViewState {
        case loading
        case error(String)
        case loaded([Post])
    }

    @State private var viewState: ViewState = .loading

    var body: some View {
        NavigationStack {
            List {
                switch viewState {
                case .loading:
                    ProgressView("Loading...")
                case .error(let message):
                    ErrorView(message: message, retry: { await loadFeed() })
                case .loaded(let posts):
                    ForEach(posts) { post in
                        PostRow(post: post)
                    }
                }
            }
            .task { await loadFeed() }
        }
    }

    private func loadFeed() async {
        do {
            let posts = try await client.getFeed()
            viewState = .loaded(posts)
        } catch {
            viewState = .error(error.localizedDescription)
        }
    }
}
```

## Sheet Patterns

### Item-driven sheet (preferred)
```swift
@State private var selectedItem: Item?

.sheet(item: $selectedItem) { item in
    EditItemSheet(item: item)
}
```

### Sheet owns its actions
```swift
struct EditItemSheet: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(Store.self) private var store

    let item: Item
    @State private var isSaving = false

    var body: some View {
        VStack {
            Button(isSaving ? "Saving..." : "Save") {
                Task { await save() }
            }
        }
    }

    private func save() async {
        isSaving = true
        await store.save(item)
        dismiss()
    }
}
```

## App-Level Environment Setup

```swift
@main
struct MyApp: App {
    @State var client: APIClient = .init()
    @State var router: AppRouter = .init()

    var body: some Scene {
        WindowGroup {
            TabView(selection: $router.selectedTab) {
                ForEach(AppTab.allCases) { tab in
                    tab.rootView
                        .tag(tab)
                }
            }
            .environment(client)
            .environment(router)
        }
    }
}
```

## State Management Guidelines

| Wrapper | Use Case |
|---------|----------|
| `@State` | Local, ephemeral view state |
| `@Binding` | Two-way data flow from parent |
| `@Observable` | Shared state across views (iOS 17+) |
| `@Environment` | Dependency injection, app-wide concerns |
| `@Query` | SwiftData queries directly in views |

## Task and onChange Patterns

```swift
// React to state changes
.task(id: searchText) {
    guard !searchText.isEmpty else { return }
    await search(query: searchText)
}

// Respond to state transitions
.onChange(of: isActive, initial: false) {
    guard isActive else { return }
    Task { await refresh() }
}
```

## Why Not MVVM?

SwiftUI was designed without ViewModels in mind:
- Views are structs, lightweight and disposable
- `@State`, `@Environment`, `@Observable` handle all data flow needs
- ViewModels add complexity, indirection, and cognitive overhead
- SwiftData's `@Query` works directly in views

**Instead:**
- Keep views as pure expressions of state
- Put business logic in services/models injected via `@Environment`
- Test services and models, not views
- Use SwiftUI Previews for visual regression testing
