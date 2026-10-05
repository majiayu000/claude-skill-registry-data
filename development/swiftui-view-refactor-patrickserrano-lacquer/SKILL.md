---
name: swiftui-view-refactor
description: Refactor a SwiftUI view file for consistent property ordering, MV patterns, view model handling, and Observation usage; split an oversized body via same-file computed view properties or MARK-organized extensions. Use when asked to clean up a SwiftUI view's layout, reorder its properties, or standardize dependency/view-model initialization. For extracting reusable subviews, @ViewBuilder, container patterns, AnyView, or ZStack vs overlay/background composition, use swiftui-expert-skill instead.
---

# SwiftUI View Refactor

## View Ordering (top to bottom)

1. Environment properties
2. `private`/`public` `let` constants
3. `@State` / other stored properties
4. Computed `var` (non-view)
5. `init`
6. `body`
7. Computed view builders / view helpers
8. Helper / async functions

## Core Guidelines

### 1) Prefer MV (Model-View) Patterns

- Default to MV: views are lightweight state expressions; models/services own business logic
- Favor `@State`, `@Environment`, `@Query`, `task`, and `onChange` for orchestration
- Inject services and shared models via `@Environment`
- Split large views into smaller views instead of introducing a view model

### 2) Split Large Bodies

If `body` grows beyond a screen or has multiple logical sections, split it within this file:

```swift
var body: some View {
    VStack(alignment: .leading, spacing: 16) {
        HeaderSection(title: title, isPinned: isPinned)
        DetailsSection(details: details)
        ActionsSection(onSave: onSave, onCancel: onCancel)
    }
}
```

Or use computed view properties in the same file:

```swift
var body: some View {
    List {
        header
        filters
        results
        footer
    }
}

private var header: some View {
    VStack(alignment: .leading, spacing: 6) {
        Text(title).font(.title2)
        Text(subtitle).font(.subheadline)
    }
}

private var filters: some View {
    ScrollView(.horizontal, showsIndicators: false) {
        HStack {
            ForEach(filterOptions, id: \.self) { option in
                FilterChip(option: option, isSelected: option == selectedFilter)
                    .onTapGesture { selectedFilter = option }
            }
        }
    }
}
```

### 3) View Model Handling (only if already present)

- Do not introduce a view model unless the request or existing code clearly calls for one
- If a view model exists, make it non-optional when possible
- Pass dependencies to the view via `init`, then into the view model

```swift
@State private var viewModel: SomeViewModel

init(dependency: Dependency) {
    _viewModel = State(initialValue: SomeViewModel(dependency: dependency))
}
```

### 4) Observation Usage

- For `@Observable` reference types, store them as `@State` in the root view
- Pass observables down explicitly as needed
- Avoid optional state unless required

## Refactor Workflow

1. Reorder the view to match the ordering rules
2. Favor MV: move orchestration into the view using `@State`, `@Environment`, `task`, `onChange`
3. If a view model exists, replace optional with non-optional `@State` initialized in `init`
4. Confirm Observation usage: `@State` for root `@Observable`, no redundant wrappers
5. Keep behavior intact: do not change layout or business logic unless requested

## Large-View Handling

When a SwiftUI view file exceeds ~300 lines:

1. Split using extensions to group related helpers
2. Move async functions into dedicated `private` extensions
3. Use `// MARK: -` comments (e.g., `// MARK: - Actions`, `// MARK: - Subviews`)
4. Keep main `struct` focused on stored properties, init, and `body`

```swift
struct LargeView: View {
    @Environment(Store.self) private var store
    @State private var items: [Item] = []

    var body: some View {
        List {
            content
        }
        .task { await loadItems() }
    }
}

// MARK: - Subviews
private extension LargeView {
    var content: some View {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}

// MARK: - Actions
private extension LargeView {
    func loadItems() async {
        items = await store.fetchItems()
    }
}
```

Keep extracted sections in this file. Once a section needs its own `@ViewBuilder` API, container/composition logic, or reuse across files, move it out and hand off to the `swiftui-expert-skill` skill.

## Checklist

- [ ] Properties ordered correctly (Environment → let → @State → computed → init → body)
- [ ] Large body split into subviews or computed view properties
- [ ] No unnecessary ViewModels introduced
- [ ] Existing ViewModels are non-optional where possible
- [ ] `@Observable` types stored as `@State` in root view
- [ ] Dependencies injected via `@Environment`
- [ ] File organized with MARK comments if >300 lines
- [ ] Behavior unchanged unless explicitly requested
