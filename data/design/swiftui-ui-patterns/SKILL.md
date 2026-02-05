---
name: swiftui-ui-patterns
description: Best practices and example-driven guidance for building SwiftUI views and components. Use when creating or refactoring SwiftUI UI, designing tab architecture with TabView, composing screens, or needing component-specific patterns and examples.
version: 1.0.0
---

# SwiftUI UI Patterns

## Quick Start

Choose a track based on your goal:

### Existing project

- Identify the feature or screen and the primary interaction model (list, detail, editor, settings, tabbed).
- Find a nearby example in the repo with `rg "TabView\("` or similar, then read the closest SwiftUI view.
- Apply local conventions: prefer SwiftUI-native state, keep state local when possible, and use environment injection for shared dependencies.
- Build the view with small, focused subviews and SwiftUI-native data flow.

### New project scaffolding

- Start with TabView + NavigationStack + sheets wiring.
- Add a minimal `AppTab` and `RouterPath` based on the provided skeletons.
- Expand the route and sheet enums as new screens are added.

---

## General Rules

- Use modern SwiftUI state (`@State`, `@Binding`, `@Observable`, `@Environment`) and avoid unnecessary view models.
- Prefer composition; keep views small and focused.
- Use async/await with `.task` and explicit loading/error states.
- Maintain existing legacy patterns only when editing legacy files.
- Follow the project's formatter and style guide.

---

## Workflow for a New SwiftUI View

1. Define the view's state and its ownership location.
2. Identify dependencies to inject via `@Environment`.
3. Sketch the view hierarchy and extract repeated parts into subviews.
4. Implement async loading with `.task` and explicit state enum if needed.
5. Add accessibility labels or identifiers when the UI is interactive.
6. Validate with a build and update usage callsites if needed.

---

## App Architecture Patterns

### Tab-based Navigation

```swift
enum AppTab: String, CaseIterable {
    case home, search, profile
    
    var title: String {
        rawValue.capitalized
    }
    
    var icon: String {
        switch self {
        case .home: return "house"
        case .search: return "magnifyingglass"
        case .profile: return "person"
        }
    }
}

struct ContentView: View {
    @State private var selectedTab: AppTab = .home
    
    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(AppTab.allCases, id: \.self) { tab in
                NavigationStack {
                    tabContent(for: tab)
                }
                .tabItem {
                    Label(tab.title, systemImage: tab.icon)
                }
                .tag(tab)
            }
        }
    }
    
    @ViewBuilder
    private func tabContent(for tab: AppTab) -> some View {
        switch tab {
        case .home: HomeView()
        case .search: SearchView()
        case .profile: ProfileView()
        }
    }
}
```

### Router Pattern

```swift
enum Route: Hashable {
    case detail(id: String)
    case settings
    case edit(item: Item)
}

@Observable
class Router {
    var path = NavigationPath()
    
    func navigate(to route: Route) {
        path.append(route)
    }
    
    func pop() {
        path.removeLast()
    }
    
    func popToRoot() {
        path.removeLast(path.count)
    }
}

struct RootView: View {
    @State private var router = Router()
    
    var body: some View {
        NavigationStack(path: $router.path) {
            HomeView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .detail(let id):
                        DetailView(id: id)
                    case .settings:
                        SettingsView()
                    case .edit(let item):
                        EditView(item: item)
                    }
                }
        }
        .environment(router)
    }
}
```

### Sheet Management

```swift
enum Sheet: Identifiable {
    case newItem
    case editItem(Item)
    case settings
    
    var id: String {
        switch self {
        case .newItem: return "newItem"
        case .editItem(let item): return "edit-\(item.id)"
        case .settings: return "settings"
        }
    }
}

struct ParentView: View {
    @State private var activeSheet: Sheet?
    
    var body: some View {
        Button("New Item") {
            activeSheet = .newItem
        }
        .sheet(item: $activeSheet) { sheet in
            switch sheet {
            case .newItem:
                NewItemSheet()
            case .editItem(let item):
                EditItemSheet(item: item)
            case .settings:
                SettingsSheet()
            }
        }
    }
}
```

---

## Component Patterns

### List with Loading States

```swift
enum LoadingState<T> {
    case idle
    case loading
    case loaded(T)
    case error(Error)
}

struct ItemListView: View {
    @State private var state: LoadingState<[Item]> = .idle
    
    var body: some View {
        Group {
            switch state {
            case .idle:
                Color.clear
            case .loading:
                ProgressView()
            case .loaded(let items):
                List(items) { item in
                    ItemRow(item: item)
                }
            case .error(let error):
                ErrorView(error: error, retry: loadItems)
            }
        }
        .task { await loadItems() }
    }
    
    private func loadItems() async {
        state = .loading
        do {
            let items = try await fetchItems()
            state = .loaded(items)
        } catch {
            state = .error(error)
        }
    }
}
```

### Search with Debouncing

```swift
struct SearchView: View {
    @State private var query = ""
    @State private var results: [Result] = []
    @State private var searchTask: Task<Void, Never>?
    
    var body: some View {
        List(results) { result in
            ResultRow(result: result)
        }
        .searchable(text: $query)
        .onChange(of: query) { _, newValue in
            searchTask?.cancel()
            searchTask = Task {
                try? await Task.sleep(for: .milliseconds(300))
                guard !Task.isCancelled else { return }
                results = await search(newValue)
            }
        }
    }
}
```

### Pull to Refresh

```swift
struct RefreshableListView: View {
    @State private var items: [Item] = []
    
    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
        .refreshable {
            items = await fetchItems()
        }
        .task {
            items = await fetchItems()
        }
    }
}
```

### Swipe Actions

```swift
struct SwipeableRow: View {
    let item: Item
    let onDelete: () -> Void
    let onArchive: () -> Void
    
    var body: some View {
        Text(item.title)
            .swipeActions(edge: .trailing) {
                Button(role: .destructive, action: onDelete) {
                    Label("Delete", systemImage: "trash")
                }
            }
            .swipeActions(edge: .leading) {
                Button(action: onArchive) {
                    Label("Archive", systemImage: "archivebox")
                }
                .tint(.blue)
            }
    }
}
```

### Context Menu

```swift
struct ContextMenuRow: View {
    let item: Item
    
    var body: some View {
        ItemRow(item: item)
            .contextMenu {
                Button {
                    // Copy action
                } label: {
                    Label("Copy", systemImage: "doc.on.doc")
                }
                
                Button {
                    // Share action
                } label: {
                    Label("Share", systemImage: "square.and.arrow.up")
                }
                
                Divider()
                
                Button(role: .destructive) {
                    // Delete action
                } label: {
                    Label("Delete", systemImage: "trash")
                }
            }
    }
}
```

---

## Form Patterns

### Validated Form

```swift
struct SignUpForm: View {
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    
    private var isEmailValid: Bool {
        email.contains("@") && email.contains(".")
    }
    
    private var isPasswordValid: Bool {
        password.count >= 8
    }
    
    private var passwordsMatch: Bool {
        password == confirmPassword
    }
    
    private var isFormValid: Bool {
        isEmailValid && isPasswordValid && passwordsMatch
    }
    
    var body: some View {
        Form {
            Section {
                TextField("Email", text: $email)
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                
                if !email.isEmpty && !isEmailValid {
                    Text("Please enter a valid email")
                        .font(.caption)
                        .foregroundStyle(.red)
                }
            }
            
            Section {
                SecureField("Password", text: $password)
                SecureField("Confirm Password", text: $confirmPassword)
                
                if !password.isEmpty && !isPasswordValid {
                    Text("Password must be at least 8 characters")
                        .font(.caption)
                        .foregroundStyle(.red)
                }
                
                if !confirmPassword.isEmpty && !passwordsMatch {
                    Text("Passwords don't match")
                        .font(.caption)
                        .foregroundStyle(.red)
                }
            }
            
            Section {
                Button("Sign Up") {
                    // Submit
                }
                .disabled(!isFormValid)
            }
        }
    }
}
```

### Settings Form

```swift
struct SettingsView: View {
    @AppStorage("notifications") private var notificationsEnabled = true
    @AppStorage("darkMode") private var darkModeEnabled = false
    @AppStorage("fontSize") private var fontSize = 14.0
    
    var body: some View {
        Form {
            Section("Preferences") {
                Toggle("Notifications", isOn: $notificationsEnabled)
                Toggle("Dark Mode", isOn: $darkModeEnabled)
            }
            
            Section("Display") {
                Slider(value: $fontSize, in: 12...24, step: 1) {
                    Text("Font Size")
                }
                Text("Preview: \(Int(fontSize))pt")
                    .font(.system(size: fontSize))
            }
            
            Section {
                Button("Reset to Defaults", role: .destructive) {
                    notificationsEnabled = true
                    darkModeEnabled = false
                    fontSize = 14.0
                }
            }
        }
        .navigationTitle("Settings")
    }
}
```

---

## Accessibility

### Basic Accessibility

```swift
struct AccessibleButton: View {
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Image(systemName: "heart.fill")
        }
        .accessibilityLabel("Add to favorites")
        .accessibilityHint("Double-tap to add this item to your favorites")
    }
}
```

### Grouped Accessibility

```swift
struct StatCard: View {
    let title: String
    let value: Int
    
    var body: some View {
        VStack {
            Text(title)
                .font(.caption)
            Text("\(value)")
                .font(.title)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(title): \(value)")
    }
}
```

---

## Notes

- Always test on multiple device sizes
- Use SF Symbols for icons when possible
- Prefer system colors for automatic dark mode support
- Keep animations subtle and respect reduced motion settings
