---
name: clean-archi-swiftui
description: Clean Architecture patterns for Swift/SwiftUI iOS projects. Use when working on Swift/SwiftUI projects that follow Clean Architecture with bounded contexts, ports/adapters pattern, and layered separation (domain/UI). Triggers for creating features, use cases, refactoring to bounded contexts, reviewing architecture compliance, or understanding project structure.
---

# Clean Architecture for Swift/SwiftUI

## Project Structure

```
root/
├── domain/                          # Pure Swift, no UI dependencies
│   ├── {BoundedContext}/            # e.g., Session/, Group/, Auth/
│   │   ├── Entities/
│   │   ├── UseCases/
│   │   ├── Ports/                   # Shared abstractions
│   │   └── Errors/
│   ├── Adapters/                    # Shared implementations
│   ├── DI/
│   ├── Constants/
│   └── Utilities/
├── {app}/                           # e.g., retime/, widget/
│   ├── Views/
│   ├── ViewModels/
│   ├── Ports/                       # UI-specific abstractions
│   ├── Adapters/                    # UI-specific implementations (RevenueCat, etc.)
│   └── {App}App.swift
├── {extension}/                     # Same structure as app
└── Secrets/
```

### Bounded Context Structure

Each bounded context is self-contained:

```
domain/Session/
├── Entities/
│   └── Session.swift
├── UseCases/
│   ├── StartSessionUseCase.swift
│   └── StopSessionUseCase.swift
├── Ports/
│   └── SessionRepositoryProtocol.swift
└── Errors/
    └── SessionError.swift
```

## Layer Rules

### Domain Layer (Pure Swift)

- **NO** SwiftUI, UIKit, or any UI framework imports
- **NO** concrete infrastructure (UserDefaults, Network, etc.)
- **ONLY** Foundation and pure Swift
- Contains: Entities, UseCases, Ports (protocols), Errors

### App/Extension Layer (SwiftUI)

- Imports domain module
- Contains: Views, ViewModels, UI-specific Ports/Adapters
- Adapters implement domain Ports

### Dependency Direction

```
Views → ViewModels → UseCases → Ports ← Adapters
                                  ↑
                            (protocols)
```

## Ports & Adapters Pattern

### Port (Protocol in domain/)

```swift
// domain/Session/Ports/SessionRepositoryProtocol.swift
protocol SessionRepositoryProtocol {
    func save(_ session: Session) async throws
    func getCurrent() async throws -> Session?
    func delete(_ id: String) async throws
}
```

### Adapter (Implementation)

```swift
// domain/Adapters/UserDefaultsSessionRepository.swift (shared)
// OR
// retime/Adapters/RevenueCatPaymentAdapter.swift (UI-specific)

class UserDefaultsSessionRepository: SessionRepositoryProtocol {
    private let monitor: MonitorProtocol
    
    init(monitor: MonitorProtocol) {
        self.monitor = monitor
    }
    
    func save(_ session: Session) async throws {
        // Implementation
    }
}
```

### Placement Rules

| Adapter Type | Location | Example |
|--------------|----------|---------|
| Shared across apps/extensions | `domain/Adapters/` | UserDefaultsRepository, DeviceActivityManager |
| UI-specific | `{app}/Adapters/` | RevenueCatAdapter, StoreKitAdapter |

## Error Handling

### When to Use `throws`

- Single operation with clear success/failure
- Errors propagate up naturally
- Caller handles error immediately

```swift
func startSession(config: SessionConfig) async throws -> Session {
    guard config.isValid else {
        throw SessionError.invalidConfiguration
    }
    // ...
}
```

### When to Use `Result<T, E>`

- Multiple possible outcomes beyond success/failure
- Caller needs to pattern match on specific cases
- Chaining operations with different error types

```swift
func validateAndStart(config: SessionConfig) -> Result<Session, SessionValidationError> {
    switch validate(config) {
    case .valid:
        return .success(createSession(config))
    case .invalidDuration(let reason):
        return .failure(.invalidDuration(reason))
    case .conflictingSession(let existing):
        return .failure(.conflict(existing))
    }
}
```

### Error Definition

```swift
// domain/Session/Errors/SessionError.swift
enum SessionError: Error, LocalizedError {
    case notFound
    case alreadyActive
    case invalidConfiguration
    case storageFailed(underlying: Error)
    
    var errorDescription: String? {
        switch self {
        case .notFound: return "Session not found"
        case .alreadyActive: return "A session is already active"
        case .invalidConfiguration: return "Invalid session configuration"
        case .storageFailed(let error): return "Storage failed: \(error.localizedDescription)"
        }
    }
}
```

## Dependency Injection

### Container Registration

```swift
// domain/DI/ServiceRegistration.swift
extension DIContainer {
    public func configureServices() {
        // Infrastructure
        register(MonitorProtocol.self, implementation: AppleLogMonitor())
        register(TrackerProtocol.self, implementation: AppleLogTracker())
        
        // Repositories (resolve dependencies)
        let monitor = try! resolve(MonitorProtocol.self)
        register(
            SessionRepositoryProtocol.self,
            implementation: UserDefaultsSessionRepository(monitor: monitor)
        )
    }
}
```

### Two Composition Roots

#### 1. App Composition Root (`{App}App.swift`)

```swift
@main
struct retimeApp: App {
    @StateObject var sessionViewModel: SessionViewModel
    
    init() {
        // Configure DI
        let container = DIContainer.shared
        container.configureServices()
        
        // Resolve Ports
        let sessionRepository = try! container.resolve(SessionRepositoryProtocol.self)
        let shieldManager = try! container.resolve(ShieldManagerProtocol.self)
        let monitor = try! container.resolve(MonitorProtocol.self)
        
        // Inject Ports into ViewModels
        _sessionViewModel = StateObject(
            wrappedValue: SessionViewModel(
                sessionRepository: sessionRepository,
                shieldManager: shieldManager,
                monitor: monitor
            )
        )
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(sessionViewModel)
        }
    }
}
```

#### 2. Extension Composition Root (`{Extension}.swift`)

Extensions cannot use `DIContainer` (different process). Instantiate dependencies manually:

```swift
class DeviceActivityMonitorExtension: DeviceActivityMonitor {
    private let startSession: StartSessionUseCase
    private let stopSession: StopSessionUseCase
    
    override init() {
        // Manual instantiation (no DIContainer in extensions)
        let monitor = AppleLogMonitor()
        let tracker = AppleLogTracker()
        let sessionRepository = UserDefaultsSessionRepository(monitor: monitor, tracker: tracker)
        let shieldManager = ShieldManager(monitor: monitor, tracker: tracker)
        
        // Create UseCases
        self.startSession = StartSessionUseCase(
            sessionRepository: sessionRepository,
            shieldManager: shieldManager,
            monitor: monitor
        )
        self.stopSession = StopSessionUseCase(
            sessionRepository: sessionRepository,
            shieldManager: shieldManager,
            monitor: monitor
        )
        
        super.init()
    }
    
    override func intervalDidStart(for activity: DeviceActivityName) {
        super.intervalDidStart(for: activity)
        Task {
            _ = await startSession.execute(sessionId: extractSessionId(from: activity))
        }
    }
}
```

## ViewModel Pattern

### When to Use UseCase vs Port Direct

| Situation | Use | Example |
|-----------|-----|---------|
| Business logic, orchestration, validation | **UseCase** | `startSession.execute()` |
| Simple read/write, no transformation | **Port direct** | `repository.getAll()` |

### Standard Pattern

ViewModels receive **Ports** via init, create **UseCases** internally when needed:

```swift
class SessionViewModel: ObservableObject {
    // State
    @Published var session: Session?
    @Published var isLoading = false
    @Published var error: SessionError?
    
    // Ports (injected)
    private let sessionRepository: SessionRepositoryProtocol
    private let shieldManager: ShieldManagerProtocol
    private let monitor: MonitorProtocol
    
    // UseCases (created internally)
    private let startSession: StartSessionUseCase
    private let stopSession: StopSessionUseCase
    
    init(
        sessionRepository: SessionRepositoryProtocol,
        shieldManager: ShieldManagerProtocol,
        monitor: MonitorProtocol
    ) {
        self.sessionRepository = sessionRepository
        self.shieldManager = shieldManager
        self.monitor = monitor
        
        // Create UseCases with injected Ports
        self.startSession = StartSessionUseCase(
            sessionRepository: sessionRepository,
            shieldManager: shieldManager,
            monitor: monitor
        )
        self.stopSession = StopSessionUseCase(
            sessionRepository: sessionRepository,
            shieldManager: shieldManager,
            monitor: monitor
        )
    }
    
    // Action using UseCase (business logic)
    func start(config: SessionConfig) {
        isLoading = true
        Task { @MainActor in
            do {
                session = try await startSession.execute(config: config)
            } catch let err as SessionError {
                error = err
            }
            isLoading = false
        }
    }
    
    // Action using Port direct (simple read)
    func loadCurrent() {
        Task { @MainActor in
            session = try? await sessionRepository.getCurrent()
        }
    }
}
```

### Complex State Pattern (Forms)

```swift
class SessionFormViewModel: ObservableObject {
    struct State {
        var duration: TimeInterval = 0
        var selectedApps: Set<AppIdentifier> = []
        var breakInterval: TimeInterval?
        var isValid: Bool { duration > 0 && !selectedApps.isEmpty }
    }
    
    @Published var state = State()
}
```

## Workflows

### Create Feature

See [references/file-templates.md](references/file-templates.md) for all templates.

1. **Create Entity** in `domain/{Context}/Entities/`
2. **Create Error** in `domain/{Context}/Errors/`
3. **Create Port** (if external dependency) in `domain/{Context}/Ports/`
4. **Create Adapter** in `domain/Adapters/` or `{app}/Adapters/`
5. **Register in DI** in `domain/DI/ServiceRegistration.swift`
6. **Create UseCase** in `domain/{Context}/UseCases/`
7. **Create ViewModel** in `{app}/ViewModels/` (receives Ports, creates UseCases)
8. **Wire ViewModel** in `{App}App.swift` composition root
9. **Create View** in `{app}/Views/`

### Create UseCase

1. Identify bounded context
2. Define input/output types
3. Identify required Ports
4. Implement UseCase class
5. Wire in ViewModel

```swift
// domain/Session/UseCases/PauseSessionUseCase.swift
class PauseSessionUseCase {
    private let repository: SessionRepositoryProtocol
    private let shieldManager: ShieldManagerProtocol
    
    init(repository: SessionRepositoryProtocol, shieldManager: ShieldManagerProtocol) {
        self.repository = repository
        self.shieldManager = shieldManager
    }
    
    func execute(sessionId: String) async throws {
        guard var session = try await repository.getCurrent() else {
            throw SessionError.notFound
        }
        session.pause()
        try await repository.save(session)
        try await shieldManager.temporarilyDisable()
    }
}
```

### Refactor to Bounded Context

1. **Identify context boundaries** - Group related entities, use cases, errors
2. **Create context directory** structure under `domain/`
3. **Move entities** first (no dependencies)
4. **Move errors** associated with entities
5. **Move ports** that serve this context
6. **Move use cases** last
7. **Update imports** across the codebase
8. **Verify compilation** after each move

#### Before

```
domain/
├── Entities/
│   ├── Session.swift
│   ├── Group.swift
│   └── User.swift
├── UseCases/
│   ├── StartSessionUseCase.swift
│   └── CreateGroupUseCase.swift
```

#### After

```
domain/
├── Session/
│   ├── Entities/Session.swift
│   ├── UseCases/StartSessionUseCase.swift
│   ├── Ports/SessionRepositoryProtocol.swift
│   └── Errors/SessionError.swift
├── Group/
│   ├── Entities/Group.swift
│   ├── UseCases/CreateGroupUseCase.swift
│   └── Errors/GroupError.swift
```

## Code Review

See [references/code-review-checklist.md](references/code-review-checklist.md) for complete checklist.

## File Templates

See [references/file-templates.md](references/file-templates.md) for copy-paste templates.
