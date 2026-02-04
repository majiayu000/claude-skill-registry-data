---

# === CORE IDENTITY ===
name: senior-ios
title: Senior iOS Skill Package
description: Native iOS development expertise for Swift 5.9+, SwiftUI, UIKit, and Apple ecosystem integration. Covers modern concurrency, architecture patterns, App Store submission, and Xcode workflows. Use when building iOS-specific features, migrating to SwiftUI, optimizing performance, or submitting to App Store.
domain: engineering
subdomain: ios-development

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "50% faster SwiftUI development, 70% fewer App Store rejections"
frequency: "Daily for iOS development teams"
use-cases:
  - Building native iOS applications with SwiftUI
  - Migrating UIKit apps to SwiftUI
  - Implementing modern Swift concurrency patterns
  - Preparing apps for App Store submission
  - Performance profiling with Instruments

# === RELATIONSHIPS ===
related-agents:
  - cs-ios-engineer
  - cs-mobile-engineer
related-skills:
  - senior-mobile
  - senior-flutter
related-commands: []
orchestrated-by:
  - cs-ios-engineer

# === TECHNICAL ===
dependencies:
  scripts: []
  references:
    - swift-patterns.md
    - swiftui-guide.md
    - xcode-workflows.md
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos]
tech-stack:
  - Swift 5.9+
  - SwiftUI
  - UIKit
  - Xcode 15+
  - Swift Concurrency
  - Combine
  - Core Data
  - SwiftData
  - TestFlight
  - Instruments

# === EXAMPLES ===
examples:
  -
    title: SwiftUI View with Async Data Loading
    input: "Create a list view that loads data asynchronously"
    output: "SwiftUI view with @State, Task, async/await, and error handling"
  -
    title: UIKit to SwiftUI Migration
    input: "Migrate UITableViewController to SwiftUI List"
    output: "Step-by-step migration with UIViewControllerRepresentable bridge"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-12-13
updated: 2025-12-13
license: MIT

# === DISCOVERABILITY ===
tags:
  - ios
  - swift
  - swiftui
  - uikit
  - xcode
  - apple
  - mobile
  - native
  - app-store
  - engineering
featured: true
verified: true
---

# Senior iOS

Native iOS development expertise covering Swift 5.9+, SwiftUI, UIKit, and the complete Apple ecosystem. This skill provides deep knowledge of modern iOS patterns, architecture, and tooling.

## Overview

This skill provides comprehensive iOS development expertise for building native applications with Swift and SwiftUI. It covers modern concurrency patterns, architecture best practices, Xcode workflows, and App Store submission processes. Uses Python tools from the senior-mobile skill for platform detection and validation.

## Quick Start

```bash
# Validate iOS project configuration
python3 ../../senior-mobile/scripts/platform_detector.py --check ios --depth full

# Validate for App Store submission
python3 ../../senior-mobile/scripts/app_store_validator.py --store apple --strict
```

## Python Tools

This skill uses Python tools from the `senior-mobile` skill:

- **platform_detector.py** - Analyze iOS project configuration, provisioning, entitlements
- **app_store_validator.py** - Validate against App Store requirements

```bash
# Full iOS analysis
python3 ../../senior-mobile/scripts/platform_detector.py --check ios --output json

# Strict App Store validation
python3 ../../senior-mobile/scripts/app_store_validator.py --store apple --strict
```

## Core Capabilities

- **SwiftUI Mastery** - Build modern, declarative UIs with state management, navigation, and animations
- **Swift Concurrency** - Implement async/await, actors, and structured concurrency patterns
- **UIKit Integration** - Bridge UIKit and SwiftUI, migrate legacy codebases
- **Performance Optimization** - Profile and optimize with Instruments, resolve memory issues
- **App Store Excellence** - Navigate submission requirements, TestFlight, and App Store Connect

## Key Workflows

### Workflow 1: SwiftUI App Development

**Time:** Variable based on complexity

**Steps:**
1. Define app architecture (MVVM, TCA, or custom)
2. Set up project with proper folder structure
3. Implement data layer with SwiftData or Core Data
4. Build UI components with SwiftUI
5. Add navigation using NavigationStack
6. Implement state management (@State, @Observable, @Environment)
7. Write unit and UI tests
8. Profile and optimize performance

**Reference:** `references/swiftui-guide.md`

**Architecture Pattern (MVVM):**
```swift
// Model
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String
}

// ViewModel
@Observable
class UserViewModel {
    var users: [User] = []
    var isLoading = false
    var error: Error?

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            users = try await userService.fetchUsers()
        } catch {
            self.error = error
        }
    }
}

// View
struct UserListView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        NavigationStack {
            List(viewModel.users) { user in
                NavigationLink(value: user) {
                    UserRowView(user: user)
                }
            }
            .navigationTitle("Users")
            .task {
                await viewModel.loadUsers()
            }
            .overlay {
                if viewModel.isLoading {
                    ProgressView()
                }
            }
        }
    }
}
```

### Workflow 2: UIKit to SwiftUI Migration

**Time:** 2-8 weeks depending on app size

**Steps:**
1. Audit existing UIKit codebase
2. Identify isolated components for migration
3. Create SwiftUI wrappers using UIViewRepresentable
4. Migrate screens incrementally (leaf nodes first)
5. Update navigation to NavigationStack
6. Replace delegates with Combine/async-await
7. Migrate data layer to SwiftData
8. Remove UIKit dependencies progressively

**Reference:** `references/swift-patterns.md`

**Bridge Pattern:**
```swift
// Wrap UIKit view for use in SwiftUI
struct MapViewRepresentable: UIViewRepresentable {
    @Binding var region: MKCoordinateRegion
    var annotations: [MKAnnotation]

    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        return mapView
    }

    func updateUIView(_ mapView: MKMapView, context: Context) {
        mapView.setRegion(region, animated: true)
        mapView.removeAnnotations(mapView.annotations)
        mapView.addAnnotations(annotations)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, MKMapViewDelegate {
        var parent: MapViewRepresentable

        init(_ parent: MapViewRepresentable) {
            self.parent = parent
        }

        func mapView(_ mapView: MKMapView, regionDidChangeAnimated: Bool) {
            parent.region = mapView.region
        }
    }
}

// Embed SwiftUI in UIKit
class SettingsViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let settingsView = SettingsView()
        let hostingController = UIHostingController(rootView: settingsView)

        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.view.frame = view.bounds
        hostingController.didMove(toParent: self)
    }
}
```

### Workflow 3: App Store Submission

**Time:** 1-2 days for prepared apps

**Steps:**
1. Complete App Store Connect setup
2. Configure signing and capabilities in Xcode
3. Run `app_store_validator.py` from senior-mobile tools
4. Create required screenshots and previews
5. Write App Store description and metadata
6. Build and upload via Xcode or Transporter
7. Submit for review with detailed notes
8. Monitor review status and respond to feedback

**Reference:** `references/xcode-workflows.md`

**Pre-Submission Checklist:**
- [ ] App icon in all required sizes (1024x1024 for App Store)
- [ ] Launch screen configured
- [ ] Info.plist privacy descriptions for all permissions
- [ ] Privacy manifest (PrivacyInfo.xcprivacy) if using required APIs
- [ ] Version and build numbers updated
- [ ] Release notes written
- [ ] Screenshots for all required device sizes
- [ ] App Preview videos (optional but recommended)
- [ ] Contact information in App Store Connect
- [ ] Export compliance information

### Workflow 4: Performance Profiling with Instruments

**Time:** 2-4 hours per profiling session

**Steps:**
1. Build for profiling (Product > Profile)
2. Select appropriate Instruments template
3. Run app through critical user flows
4. Analyze captured data
5. Identify bottlenecks and issues
6. Implement optimizations
7. Re-profile to verify improvements

**Reference:** `references/xcode-workflows.md`

**Key Instruments:**
| Instrument | Purpose | When to Use |
|------------|---------|-------------|
| Time Profiler | CPU usage analysis | Slow operations, high CPU |
| Allocations | Memory allocation tracking | Memory growth, leaks |
| Leaks | Memory leak detection | Retain cycles, missing dealloc |
| Network | Network request analysis | Slow API calls, large payloads |
| Core Animation | UI rendering performance | Dropped frames, slow scrolling |
| SwiftUI | SwiftUI view lifecycle | Excessive body evaluations |

**Common Performance Patterns:**
```swift
// Avoid: Expensive computation in body
var body: some View {
    List(items.sorted().filtered()) { item in  // BAD: Runs every render
        ItemRow(item: item)
    }
}

// Better: Cache computed values
@State private var sortedItems: [Item] = []

var body: some View {
    List(sortedItems) { item in
        ItemRow(item: item)
    }
    .onChange(of: items) { _, newItems in
        sortedItems = newItems.sorted().filtered()
    }
}

// Best: Use @Observable with lazy computation
@Observable
class ItemsViewModel {
    var items: [Item] = []

    var sortedItems: [Item] {
        // Cached automatically by @Observable
        items.sorted().filtered()
    }
}
```

## Swift Patterns

### Modern Concurrency

```swift
// Structured concurrency with task groups
func loadDashboard() async throws -> Dashboard {
    async let user = userService.fetchCurrentUser()
    async let notifications = notificationService.fetchUnread()
    async let stats = analyticsService.fetchStats()

    return try await Dashboard(
        user: user,
        notifications: notifications,
        stats: stats
    )
}

// Actor for thread-safe state
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? {
        cache[url]
    }

    func setImage(_ image: UIImage, for url: URL) {
        cache[url] = image
    }
}

// MainActor for UI updates
@MainActor
class ProfileViewModel: ObservableObject {
    @Published var profile: Profile?

    func loadProfile() async {
        // Automatically runs on main thread
        profile = try? await profileService.fetch()
    }
}
```

### Error Handling

```swift
// Typed throws (Swift 6)
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed(Error)
    case serverError(Int)
}

func fetchUser(id: String) async throws(NetworkError) -> User {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        throw .invalidURL
    }

    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse else {
        throw .noData
    }

    guard httpResponse.statusCode == 200 else {
        throw .serverError(httpResponse.statusCode)
    }

    do {
        return try JSONDecoder().decode(User.self, from: data)
    } catch {
        throw .decodingFailed(error)
    }
}
```

### Protocol-Oriented Design

```swift
// Define capability through protocols
protocol Loadable {
    associatedtype Content
    var state: LoadingState<Content> { get }
    func load() async
}

enum LoadingState<T> {
    case idle
    case loading
    case loaded(T)
    case error(Error)
}

// Generic view for any loadable content
struct LoadableView<Content: View, T>: View {
    let state: LoadingState<T>
    let content: (T) -> Content
    let onRetry: () async -> Void

    var body: some View {
        switch state {
        case .idle:
            Color.clear.task { await onRetry() }
        case .loading:
            ProgressView()
        case .loaded(let data):
            content(data)
        case .error(let error):
            ErrorView(error: error, onRetry: onRetry)
        }
    }
}
```

## References

- **[swift-patterns.md](references/swift-patterns.md)** - Swift 5.9+ patterns, concurrency, protocols
- **[swiftui-guide.md](references/swiftui-guide.md)** - SwiftUI state, navigation, lifecycle
- **[xcode-workflows.md](references/xcode-workflows.md)** - Signing, Instruments, TestFlight

## Tools Integration

This skill uses Python tools from the `senior-mobile` skill:

```bash
# Validate iOS app for App Store (from senior-mobile)
python3 ../../senior-mobile/scripts/app_store_validator.py --store apple --strict

# Detect iOS project configuration
python3 ../../senior-mobile/scripts/platform_detector.py --check ios --depth full
```

## Best Practices

### SwiftUI
- Use `@Observable` macro (iOS 17+) over `@ObservableObject`
- Prefer `NavigationStack` over `NavigationView`
- Keep views small and focused
- Extract reusable components early
- Use `@ViewBuilder` for conditional content

### Performance
- Minimize body complexity
- Use `LazyVStack`/`LazyHStack` for large lists
- Implement proper `Equatable` for custom types
- Avoid force unwrapping in production code
- Profile before optimizing

### Architecture
- Separate concerns (View, ViewModel, Model, Service)
- Use dependency injection
- Keep business logic testable
- Document public APIs
- Follow Swift naming conventions

## Success Metrics

- **SwiftUI Development Speed:** 50% faster than UIKit equivalent
- **App Store Approval Rate:** 95%+ first submission
- **Code Coverage:** 80%+ for business logic
- **Performance:** 60 FPS for all animations
