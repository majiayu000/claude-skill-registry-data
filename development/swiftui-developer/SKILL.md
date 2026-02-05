---
name: swiftui-developer
description: Develop SwiftUI applications for iOS/macOS. Use when writing SwiftUI views, managing state, or building Apple platform UIs.
version: 1.0.0
---

# SwiftUI Developer

## Overview

Expert guidance for building professional SwiftUI applications targeting iOS 17+/macOS 14+ with modern patterns, accessibility compliance, and optimal performance.

## Instructions

When writing SwiftUI code, follow this workflow:

### 1. Assess Requirements

- Target platform (iOS, macOS, visionOS, watchOS)
- Minimum OS version (determines available APIs)
- Complexity level (simple view vs. full feature)

### 2. Choose Architecture

**For simple views:**
- Use `@State` for local state
- No ViewModel needed for pure display views

**For complex features:**
- Use MVVM with `@Observable` macro (iOS 17+)
- Keep ViewModel logic separate from View
- Use `@Environment` for shared data

### 3. Apply State Management

```swift
// iOS 17+ Modern Pattern
@Observable
class FeatureViewModel {
    var items: [Item] = []
    @ObservationIgnored var cache: Cache? // Non-observed
}

struct FeatureView: View {
    @State private var viewModel = FeatureViewModel()
    var body: some View { ... }
}
```

**Property Wrapper Selection:**
| Wrapper | Use Case |
|---------|----------|
| `@State` | Local value types, simple state, @Observable objects |
| `@Binding` | Two-way connection to parent state |
| `@Environment` | Shared app-wide data, system values |
| `@Observable` | Modern observable objects (iOS 17+) |

### 4. Follow HIG Principles

- Touch targets: minimum 44×44 points
- Text: 17pt body minimum, support Dynamic Type
- Colors: use semantic colors (`.primary`, `.secondary`)
- Accessibility: add `.accessibilityLabel`, `.accessibilityHint`

### 5. Optimize Performance

- Extract reusable subviews
- Use `LazyVStack`/`LazyHStack` for lists
- Avoid heavy computation in `body`
- Keep state minimal and locally scoped

## Examples

### Example: Settings Screen with Toggle

**Input:**
"Create a settings view with dark mode toggle and notification preferences"

**Output:**
```swift
import SwiftUI

@Observable
class SettingsViewModel {
    var isDarkMode: Bool {
        didSet { UserDefaults.standard.set(isDarkMode, forKey: "darkMode") }
    }
    var notificationsEnabled: Bool {
        didSet { UserDefaults.standard.set(notificationsEnabled, forKey: "notifications") }
    }

    init() {
        isDarkMode = UserDefaults.standard.bool(forKey: "darkMode")
        notificationsEnabled = UserDefaults.standard.bool(forKey: "notifications")
    }
}

struct SettingsView: View {
    @State private var viewModel = SettingsViewModel()

    var body: some View {
        Form {
            Section("Appearance") {
                Toggle("Dark Mode", isOn: $viewModel.isDarkMode)
                    .accessibilityHint("Switches between light and dark appearance")
            }

            Section("Notifications") {
                Toggle("Enable Notifications", isOn: $viewModel.notificationsEnabled)
                    .accessibilityHint("Allows the app to send you notifications")
            }
        }
        .navigationTitle("Settings")
    }
}
```

### Example: List with Navigation

**Input:**
"Create a list of items with detail navigation"

**Output:**
```swift
import SwiftUI

struct Item: Identifiable {
    let id = UUID()
    let title: String
    let subtitle: String
}

struct ItemListView: View {
    let items: [Item]

    var body: some View {
        List(items) { item in
            NavigationLink(value: item) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(item.title)
                        .font(.headline)
                    Text(item.subtitle)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
                .padding(.vertical, 4)
            }
            .accessibilityLabel("\(item.title), \(item.subtitle)")
        }
        .navigationTitle("Items")
        .navigationDestination(for: Item.self) { item in
            ItemDetailView(item: item)
        }
    }
}
```

### Example: Async Data Loading

**Input:**
"Create a view that loads data from an API"

**Output:**
```swift
import SwiftUI

@Observable
class DataViewModel {
    var items: [Item] = []
    var isLoading = false
    var errorMessage: String?

    func loadData() async {
        isLoading = true
        errorMessage = nil

        do {
            items = try await APIService.shared.fetchItems()
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }
}

struct DataView: View {
    @State private var viewModel = DataViewModel()

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView("Loading...")
            } else if let error = viewModel.errorMessage {
                ContentUnavailableView(
                    "Error",
                    systemImage: "exclamationmark.triangle",
                    description: Text(error)
                )
            } else {
                List(viewModel.items) { item in
                    Text(item.title)
                }
            }
        }
        .task {
            await viewModel.loadData()
        }
        .refreshable {
            await viewModel.loadData()
        }
    }
}
```

## Guidelines

### Do

- Use `@Observable` for iOS 17+ projects (better performance)
- Support Dynamic Type with `.font(.body)` etc.
- Add accessibility labels to interactive elements
- Use `LazyVStack`/`LazyHStack` for large collections
- Extract complex subviews to prevent unnecessary redraws
- Use semantic colors for automatic dark mode support

### Don't

- Use `@State` with reference types (causes memory leaks)
- Use `@ObservedObject` to create objects in view (use `@StateObject` or `@State`)
- Put heavy computation in `body` property
- Hardcode colors/sizes (breaks accessibility)
- Ignore the 44×44pt minimum touch target
- Skip accessibility labels on buttons/images

### iOS 18+ Features

- Floating tab bar with sidebar flexibility
- `.presentationSizing(.form)` for sheets
- Zoom navigation transitions
- Control Center widgets
- `@Entry` macro for environment keys
- Mesh gradients

## Additional Resources

See `reference/` directory for:
- `state-management.md` - Property wrapper decision guide
- `hig-checklist.md` - HIG compliance checklist
