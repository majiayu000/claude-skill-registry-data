---
name: ios-navigation
description: >
  iOS navigation guidance. Triggers on: navigation, tab bar, NavigationStack,
  sheets, modals, app structure, routing, TabView, NavigationSplitView, deep linking.
---

# iOS Navigation — App Structure, Routing & Adaptive Layout

---

## 1. Navigation Patterns

Choose the right container for each context:

| Pattern | When to Use |
|---|---|
| `NavigationStack` | Push/pop within a section. Most common. |
| `TabView` | Top-level app sections (3–5 tabs). Glass tab bar in iOS 26. |
| `.sheet(item:)` | Focused task or detail. Preferred over `isPresented:` — drives from data. |
| `.fullScreenCover` | Immersive flows (onboarding, media playback, composition). |
| `NavigationSplitView` | Multi-column layout for iPad/macOS. Sidebar + detail. |
| `.inspector` | Secondary detail panel — supplementary info without leaving context. |
| `.popover` | Quick info or actions on iPad. Falls back to sheet on iPhone. |

### Decision Guide
- **"Where am I in the app?"** → TabView
- **"Go deeper into content"** → NavigationStack push
- **"Do a focused task, then come back"** → Sheet
- **"Show two things side by side"** → NavigationSplitView
- **"Quick action on this item"** → Context menu or popover

---

## 2. iOS 26 Glass Navigation

iOS 26 automatically applies glass materials to system navigation elements:

### Glass Tab Bar
```swift
TabView {
    Tab("Home", systemImage: "house") {
        HomeView()
    }
    Tab("Search", systemImage: "magnifyingglass") {
        SearchView()
    }
    Tab("Profile", systemImage: "person") {
        ProfileView()
    }
}
```
The tab bar gets glass treatment automatically. Don't fight it with custom tab bars.

### Glass Navigation Bar
```swift
NavigationStack {
    ContentView()
        .navigationTitle("Feed")
        .toolbarBackgroundVisibility(.automatic) // Let glass show
}
```

### Scroll Extension Under Sidebar
```swift
NavigationSplitView {
    SidebarView()
} detail: {
    DetailView()
        .scrollExtensionMode(.underSidebar) // Content extends under glass sidebar
}
```

---

## 3. App Scaffolding Pattern

Standard wiring for a multi-tab app with navigation and sheets:

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        TabView {
            Tab("Home", systemImage: "house") {
                HomeNavigationStack()
            }
            Tab("Search", systemImage: "magnifyingglass") {
                SearchNavigationStack()
            }
            Tab("Profile", systemImage: "person") {
                ProfileNavigationStack()
            }
        }
    }
}
```

### Per-Tab Navigation Stack
```swift
struct HomeNavigationStack: View {
    @State private var path = NavigationPath()
    @State private var presentedSheet: SheetDestination?

    var body: some View {
        NavigationStack(path: $path) {
            HomeView(path: $path, presentedSheet: $presentedSheet)
                .navigationDestination(for: Post.self) { post in
                    PostDetailView(post: post)
                }
                .navigationDestination(for: User.self) { user in
                    UserProfileView(user: user)
                }
        }
        .sheet(item: $presentedSheet) { destination in
            destination.view
        }
    }
}
```

### Sheet Routing Enum
```swift
enum SheetDestination: Identifiable {
    case compose
    case settings
    case editProfile(User)

    var id: String {
        switch self {
        case .compose: "compose"
        case .settings: "settings"
        case .editProfile(let user): "editProfile-\(user.id)"
        }
    }

    @ViewBuilder
    var view: some View {
        switch self {
        case .compose:
            ComposeView()
        case .settings:
            SettingsView()
        case .editProfile(let user):
            EditProfileView(user: user)
        }
    }
}
```

---

## 4. Sheet Best Practices

- **Use `item:` over `isPresented:`** — sheets driven by data are easier to reason about
- **Sheets own their dismissal** — call `@Environment(\.dismiss)` inside the sheet, not a callback
- **Don't pass closures for actions** — the sheet should perform its own save/cancel logic
- **Size sheets appropriately**:
  ```swift
  .sheet(item: $item) { item in
      DetailView(item: item)
          .presentationDetents([.medium, .large])
          .presentationDragIndicator(.visible)
  }
  ```
- **Sheets get their own NavigationStack** if they need a toolbar:
  ```swift
  NavigationStack {
      ComposeView()
          .toolbar {
              ToolbarItem(.cancellationAction) { Button("Cancel") { dismiss() } }
              ToolbarItem(.confirmationAction) { Button("Save") { save(); dismiss() } }
          }
  }
  ```

---

## 5. Adaptive Layout

### Size Classes
```swift
@Environment(\.horizontalSizeClass) private var horizontalSizeClass

var body: some View {
    if horizontalSizeClass == .regular {
        // iPad / landscape — two-column layout
        NavigationSplitView {
            SidebarView()
        } detail: {
            DetailView()
        }
    } else {
        // iPhone — single column
        NavigationStack {
            ListView()
        }
    }
}
```

### ViewThatFits
```swift
// Automatically picks the first child that fits
ViewThatFits {
    HStack { /* wide layout */ }
    VStack { /* narrow layout */ }
}
```

### iPad Considerations
- Use `NavigationSplitView` for primary/detail patterns
- Support multiple windows with `@Environment(\.supportsMultipleWindows)`
- Pointer/keyboard: add `.hoverEffect()`, support keyboard shortcuts
- Don't assume full-screen — iPad runs apps in split view

---

## 6. Deep Linking

### URL Routing
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onOpenURL { url in
                    handleDeepLink(url)
                }
        }
    }

    func handleDeepLink(_ url: URL) {
        // Parse URL components and navigate
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: false),
              let host = components.host else { return }

        switch host {
        case "post":
            if let id = components.queryItems?.first(where: { $0.name == "id" })?.value {
                // Navigate to post
            }
        case "profile":
            // Navigate to profile tab
        default:
            break
        }
    }
}
```

### Programmatic Navigation with NavigationPath
```swift
@State private var path = NavigationPath()

// Push programmatically
path.append(somePost)       // Pushes PostDetailView
path.append(someUser)       // Pushes UserProfileView

// Pop to root
path = NavigationPath()

// Pop one level
path.removeLast()
```

Use `NavigationPath` for type-erased heterogeneous paths. Use `[SomeType]` for homogeneous paths (simpler, Codable by default).

### State Restoration
```swift
// Save navigation state
@SceneStorage("navigationPath") private var pathData: Data?

// Encode/decode NavigationPath for persistence
// NavigationPath supports Codable when all pushed types are Codable
```
