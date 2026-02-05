---
name: ios-reviewer
description: |
  WHEN: iOS Swift/SwiftUI code review, UIKit patterns, Combine/async-await checks, MVVM structure analysis
  WHAT: SwiftUI best practices + Combine patterns + Memory management + Performance optimization + Architecture patterns
  WHEN NOT: Cross-platform → flutter-reviewer, Android → kotlin-android-reviewer
---

# iOS Reviewer Skill

## Purpose
Reviews iOS Swift code for SwiftUI, UIKit, Combine, and Swift Concurrency best practices.

## When to Use
- iOS Swift project code review
- "SwiftUI", "UIKit", "Combine", "async/await" mentions
- iOS performance, memory management inspection
- Projects with `.xcodeproj` or `.xcworkspace`

## Project Detection
- `.xcodeproj` or `.xcworkspace` exists
- `Package.swift` with iOS platform
- `Info.plist` exists
- `*.swift` files present

## Workflow

### Step 1: Analyze Project
```
**Swift**: 5.9+
**iOS Target**: 15.0+
**UI Framework**: SwiftUI / UIKit
**Architecture**: MVVM / TCA / Clean Architecture
**Package Manager**: SPM / CocoaPods / Carthage
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full iOS pattern check (recommended)
- SwiftUI view patterns
- UIKit lifecycle/memory
- Combine/async-await usage
- Architecture patterns
multiSelect: true
```

## Detection Rules

### SwiftUI Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Heavy computation in body | Move to ViewModel or task modifier | HIGH |
| Missing @State/@StateObject distinction | Use @StateObject for owned objects | HIGH |
| ObservableObject without @Published | Add @Published to observed properties | HIGH |
| Missing EnvironmentObject injection | Ensure parent provides object | MEDIUM |
| Large View body | Extract to smaller Views | MEDIUM |

```swift
// BAD: Heavy computation in body
struct MyView: View {
    var body: some View {
        let result = expensiveCalculation()  // Called every render
        Text(result)
    }
}

// GOOD: Move to ViewModel or use task
struct MyView: View {
    @StateObject var viewModel = MyViewModel()
    var body: some View {
        Text(viewModel.result)
            .task { await viewModel.calculate() }
    }
}

// BAD: @State for reference type
struct MyView: View {
    @State var viewModel = MyViewModel()  // Won't observe changes
}

// GOOD: @StateObject for reference type
struct MyView: View {
    @StateObject var viewModel = MyViewModel()
}

// BAD: Missing @Published
class MyViewModel: ObservableObject {
    var data: [String] = []  // Changes won't trigger view update
}

// GOOD: Add @Published
class MyViewModel: ObservableObject {
    @Published var data: [String] = []
}
```

### UIKit Patterns
| Check | Issue | Severity |
|-------|-------|----------|
| Strong delegate reference | Retain cycle risk | CRITICAL |
| Missing removeObserver | Memory leak | HIGH |
| Force unwrap IBOutlet | Crash risk | HIGH |
| viewDidLoad network call | UX issue | MEDIUM |
| Main thread UI update missing | Undefined behavior | CRITICAL |

```swift
// BAD: Strong delegate
class MyViewController: UIViewController {
    var delegate: MyDelegate?  // Strong reference!
}

// GOOD: Weak delegate
class MyViewController: UIViewController {
    weak var delegate: MyDelegate?
}

// BAD: Missing removeObserver
override func viewDidLoad() {
    super.viewDidLoad()
    NotificationCenter.default.addObserver(self, ...)
}

// GOOD: Remove in deinit
deinit {
    NotificationCenter.default.removeObserver(self)
}

// BAD: Force unwrap IBOutlet
@IBOutlet var titleLabel: UILabel!
func setup() {
    titleLabel.text = "Hello"  // Crash if not connected
}

// GOOD: Safe unwrap
@IBOutlet weak var titleLabel: UILabel?
func setup() {
    titleLabel?.text = "Hello"
}
```

### Combine Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing store in cancellables | Subscription lost | CRITICAL |
| receive(on:) missing for UI | Threading issue | HIGH |
| PassthroughSubject without type erasure | Exposes implementation | MEDIUM |
| Chain without error handling | Silent failures | MEDIUM |

```swift
// BAD: Missing store
class MyViewModel {
    func subscribe() {
        publisher.sink { value in
            print(value)
        }  // Immediately cancelled!
    }
}

// GOOD: Store in cancellables
class MyViewModel {
    private var cancellables = Set<AnyCancellable>()

    func subscribe() {
        publisher
            .sink { value in print(value) }
            .store(in: &cancellables)
    }
}

// BAD: Missing receive(on:) for UI
publisher
    .sink { self.label.text = $0 }  // May not be on main thread
    .store(in: &cancellables)

// GOOD: Explicit main thread
publisher
    .receive(on: DispatchQueue.main)
    .sink { self.label.text = $0 }
    .store(in: &cancellables)
```

### Swift Concurrency (async/await)
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Blocking call in async context | Use async alternative | HIGH |
| Missing @MainActor for UI | Threading issue | HIGH |
| Task without cancellation handling | Resource leak | MEDIUM |
| Unstructured Task in SwiftUI | Use .task modifier | MEDIUM |

```swift
// BAD: Blocking in async
func fetchData() async -> Data {
    return URLSession.shared.dataTask(...)  // Blocking!
}

// GOOD: Async alternative
func fetchData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}

// BAD: Missing @MainActor for UI
class MyViewModel: ObservableObject {
    @Published var items: [Item] = []

    func load() async {
        items = await fetchItems()  // May not be on main thread!
    }
}

// GOOD: @MainActor
@MainActor
class MyViewModel: ObservableObject {
    @Published var items: [Item] = []

    func load() async {
        items = await fetchItems()  // Guaranteed main thread
    }
}

// BAD: Unstructured Task in SwiftUI
struct MyView: View {
    var body: some View {
        Text("Hello")
            .onAppear {
                Task { await load() }  // Not cancelled on disappear
            }
    }
}

// GOOD: Use .task modifier
struct MyView: View {
    var body: some View {
        Text("Hello")
            .task { await load() }  // Auto-cancelled
    }
}
```

### Memory Management
| Check | Problem | Solution |
|-------|---------|----------|
| Strong self in closure | Retain cycle | [weak self] or [unowned self] |
| Circular reference | Memory leak | Break cycle with weak |
| Large image in memory | OOM risk | Use thumbnails, purge cache |
| Uncancelled Task | Resource leak | Store and cancel |

```swift
// BAD: Strong self in closure
class MyViewController: UIViewController {
    func setup() {
        service.fetch { result in
            self.update(result)  // Strong capture!
        }
    }
}

// GOOD: Weak self
class MyViewController: UIViewController {
    func setup() {
        service.fetch { [weak self] result in
            self?.update(result)
        }
    }
}
```

## Response Template
```
## iOS Code Review Results

**Project**: [name]
**Swift**: 5.9 | **iOS Target**: 15.0+
**UI Framework**: SwiftUI/UIKit
**Files Analyzed**: X

### SwiftUI Patterns
| Status | File | Issue |
|--------|------|-------|
| HIGH | Views/HomeView.swift | Heavy computation in body (line 45) |
| MEDIUM | Views/ProfileView.swift | Large view body, extract components |

### UIKit/Memory
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | Controllers/DetailVC.swift | Strong delegate reference (line 23) |
| HIGH | Controllers/ListVC.swift | Missing removeObserver in deinit |

### Combine/Async
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | Services/DataService.swift | Missing cancellable store |
| HIGH | ViewModels/MainVM.swift | Missing @MainActor |

### Recommended Actions
1. [ ] Add [weak self] to closures
2. [ ] Use @StateObject for owned ObservableObjects
3. [ ] Add @MainActor to ViewModels
4. [ ] Replace Task with .task modifier
```

## Best Practices
1. **SwiftUI**: Prefer small, composable Views with proper state ownership
2. **UIKit**: Always use weak delegates, clean up observers
3. **Combine**: Store subscriptions, handle threading explicitly
4. **Concurrency**: Use structured concurrency, @MainActor for UI
5. **Memory**: Use weak captures, profile with Instruments

## Integration
- `code-reviewer` skill: General Swift code quality
- `test-generator` skill: iOS XCTest generation
- `security-scanner` skill: iOS security checks

## Notes
- Based on Swift 5.9+, iOS 15+
- Supports SwiftUI and UIKit projects
- Includes Swift Concurrency patterns (async/await)
