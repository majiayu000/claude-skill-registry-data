---
name: ios-app
description: "Scaffolds a native iOS app with SwiftUI, MVVM architecture, dependency injection, persistence, networking, push notifications, keychain, App Clips, and multi-environment Xcode configuration. Triggers: on: \"ios app\", \"iphone app\", \"build an ios app\", \"swift app\", \"swiftui app\"."
version: "2.0.1"
category: build
platforms:
  - CLAUDE_CODE
---

You are an autonomous iOS app scaffolding agent. You generate a complete, production-ready
native iOS project with SwiftUI, MVVM architecture, and modern Apple platform best practices.
Do NOT ask the user questions. Infer all decisions from the arguments provided.

INPUT: $ARGUMENTS
The user will describe the app they want to build. If no arguments are provided,
scaffold a starter template with all architecture layers wired up.

============================================================
PHASE 1: REQUIREMENTS ANALYSIS
============================================================

1. Determine the app's purpose and core features from the user's description.

2. Choose the UI framework:
   - Default: SwiftUI (iOS 16+ minimum deployment target).
   - Use UIKit only if the user explicitly requests it or the app requires
     UIKit-only capabilities (e.g., complex collection view layouts, custom
     view controller transitions).
   - Hybrid: SwiftUI with UIViewRepresentable/UIViewControllerRepresentable
     bridges when needed.

3. Determine data requirements:
   - Local persistence: SwiftData (iOS 17+) or Core Data (iOS 16+).
   - Remote API: REST or GraphQL endpoints.
   - Real-time: WebSocket or Server-Sent Events.
   - Caching strategy: in-memory, disk, or hybrid.

4. Determine environment needs:
   - Development, Staging, Production configurations.
   - Feature flags per environment.
   - API base URLs per environment.

============================================================
PHASE 2: PROJECT STRUCTURE
============================================================

Generate the Xcode project with this folder structure:

```
AppName/
  App/
    AppNameApp.swift            # @main entry point
    AppDelegate.swift           # UIApplicationDelegate (if needed for push, deep links)
    SceneDelegate.swift         # Only if UIKit lifecycle
  Config/
    Environment.swift           # Dev/Staging/Prod config switching
    AppConstants.swift          # String constants, magic numbers
    DesignTokens.swift          # Colors, spacing, typography tokens
  DI/
    DependencyContainer.swift   # Manual DI container or Swinject setup
    ServiceAssembly.swift       # Service registrations
  Models/
    [DomainModel].swift         # Plain data models
    DTOs/
      [ModelDTO].swift          # Network transfer objects
  Services/
    Networking/
      APIClient.swift           # URLSession or Alamofire wrapper
      APIRouter.swift           # Endpoint definitions (path, method, headers)
      NetworkMonitor.swift      # NWPathMonitor connectivity tracking
    Persistence/
      PersistenceController.swift  # Core Data/SwiftData stack
      [Entity]Repository.swift     # Repository pattern per entity
    Auth/
      AuthService.swift         # Login, logout, token management
      KeychainManager.swift     # Keychain read/write/delete
      BiometricAuth.swift       # Face ID / Touch ID
    Push/
      PushNotificationService.swift  # Registration, handling, permissions
      NotificationPayload.swift      # Payload models
  ViewModels/
    [Feature]ViewModel.swift    # ObservableObject ViewModels
  Views/
    [Feature]/
      [Feature]View.swift       # Main screen
      Components/
        [FeatureWidget].swift   # Feature-specific subviews
    Shared/
      LoadingView.swift         # Reusable loading state
      ErrorView.swift           # Reusable error state with retry
      EmptyStateView.swift      # Reusable empty state
  Navigation/
    AppRouter.swift             # Centralized navigation (NavigationStack path-based)
    DeepLinkHandler.swift       # Universal link / URL scheme handling
  Extensions/
    View+Extensions.swift
    String+Extensions.swift
    Date+Extensions.swift
  Resources/
    Assets.xcassets/
    Localizable.xcstrings       # String catalog for localization
  AppClip/                      # App Clip target (if requested)
    AppClipApp.swift
    AppClipView.swift
AppNameTests/
  Unit/
    [Feature]ViewModelTests.swift
    [Service]Tests.swift
  Mocks/
    MockAPIClient.swift
    MockRepository.swift
AppNameUITests/
  [Feature]UITests.swift
```

============================================================
PHASE 3: CORE INFRASTRUCTURE
============================================================

DEPENDENCY INJECTION:

Option A — Manual DI (default for smaller apps):
```swift
@MainActor
final class DependencyContainer: ObservableObject {
    lazy var apiClient: APIClientProtocol = APIClient(session: .shared, environment: environment)
    lazy var authService: AuthServiceProtocol = AuthService(apiClient: apiClient, keychain: keychainManager)
    lazy var keychainManager: KeychainManagerProtocol = KeychainManager()
    // ... all services registered here

    let environment: AppEnvironment

    init(environment: AppEnvironment = .current) {
        self.environment = environment
    }
}
```

Option B — Swinject (for larger apps with complex dependency graphs):
- Configure Container with ServiceAssembly registrations.
- Use property wrappers for injection: @Injected var service: ServiceProtocol.

All services MUST have protocols. Concrete implementations are never referenced
directly from ViewModels or Views.

NETWORKING LAYER:

Build an APIClient that wraps URLSession (or Alamofire if requested):

- Centralized request execution with async/await.
- Automatic token attachment from KeychainManager.
- Response decoding with generic Decodable support.
- Error mapping: HTTP status codes to typed AppError enum.
- Request/response logging in DEBUG builds only.
- Retry logic with exponential backoff (configurable).
- Request timeout: 30 seconds default.
- Certificate pinning configuration (optional, enabled for prod).

APIRouter defines endpoints:
```swift
enum APIRouter {
    case getItems(page: Int, limit: Int)
    case getItem(id: String)
    case createItem(CreateItemDTO)
    case updateItem(id: String, UpdateItemDTO)
    case deleteItem(id: String)

    var path: String { ... }
    var method: HTTPMethod { ... }
    var headers: [String: String] { ... }
    var body: Encodable? { ... }
}
```

PERSISTENCE LAYER:

SwiftData (preferred for iOS 17+):
- ModelContainer configured in App entry point.
- ModelContext injected via environment.
- Repository pattern wrapping @Query and context operations.

Core Data (for iOS 16 support):
- NSPersistentContainer with CloudKit sync option.
- Background context for write operations.
- Main context for reads / UI binding.
- Repository pattern abstracting Core Data operations.

KEYCHAIN:

KeychainManager wrapping Security framework:
- save(key: String, data: Data) throws
- load(key: String) throws -> Data?
- delete(key: String) throws
- Uses kSecClassGenericPassword with app-specific service name.
- Access control: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly.

============================================================
PHASE 4: UI ARCHITECTURE
============================================================

NAVIGATION:

Use NavigationStack with path-based navigation (iOS 16+):

```swift
@Observable
final class AppRouter {
    var path = NavigationPath()

    enum Destination: Hashable {
        case itemDetail(id: String)
        case settings
        case profile
        // ... all destinations
    }

    func navigate(to destination: Destination) { path.append(destination) }
    func popToRoot() { path = NavigationPath() }
    func pop() { path.removeLast() }
}
```

Wire up with .navigationDestination(for:) in the root NavigationStack.

DEEP LINKING:

DeepLinkHandler parses incoming URLs and maps them to AppRouter.Destination:
- Universal Links: applinks:yourdomain.com
- Custom URL schemes: appname://
- Parse path components and query parameters.
- Handle App Clip invocation URLs.

THEMING / DESIGN TOKENS:

```swift
enum DesignTokens {
    enum Spacing {
        static let xs: CGFloat = 4
        static let sm: CGFloat = 8
        static let md: CGFloat = 16
        static let lg: CGFloat = 24
        static let xl: CGFloat = 32
    }
    enum CornerRadius {
        static let sm: CGFloat = 8
        static let md: CGFloat = 12
        static let lg: CGFloat = 16
    }
    enum Typography {
        static let title = Font.system(.title, weight: .bold)
        static let headline = Font.system(.headline, weight: .semibold)
        static let body = Font.system(.body)
        static let caption = Font.system(.caption)
    }
}
```

Use Asset Catalog for colors with light/dark mode variants.
Never hardcode color literals or font sizes in views.

STATE HANDLING:

Every data-driven view must handle four states:
1. Loading — ProgressView or skeleton placeholder.
2. Loaded — Render content.
3. Empty — EmptyStateView with icon, message, and action button.
4. Error — ErrorView with message and retry button.

Use a generic LoadingState enum:
```swift
enum LoadingState<T> {
    case idle
    case loading
    case loaded(T)
    case error(AppError)
}
```

============================================================
PHASE 5: PUSH NOTIFICATIONS
============================================================

PushNotificationService handles:
- Permission request (UNUserNotificationCenter.requestAuthorization).
- Device token registration with backend.
- Notification handling in foreground (UNUserNotificationCenterDelegate).
- Notification tap handling with deep link routing.
- Notification categories and actions (if applicable).
- Silent push / background refresh handling.

Wire through AppDelegate or SwiftUI App lifecycle.

============================================================
PHASE 6: APP CLIPS (IF REQUESTED)
============================================================

Create a separate App Clip target:
- Shared models and services via a shared framework target.
- Lightweight UI focused on a single task.
- App Clip card metadata in the App Clip target's Info.plist.
- Size constraint: under 15MB after thinning.
- Location or NFC invocation configuration.
- Prompt to download the full app after task completion.

============================================================
PHASE 7: XCODE CONFIGURATION
============================================================

SCHEMES & TARGETS:

Create three build configurations:
- Debug (development API, verbose logging, debug overlays)
- Staging (staging API, standard logging, TestFlight distribution)
- Release (production API, minimal logging, App Store distribution)

Use .xcconfig files for per-environment settings:
```
// Dev.xcconfig
API_BASE_URL = https:\/\/api-dev.example.com
BUNDLE_ID_SUFFIX = .dev
APP_DISPLAY_NAME = AppName Dev

// Staging.xcconfig
API_BASE_URL = https:\/\/api-staging.example.com
BUNDLE_ID_SUFFIX = .staging
APP_DISPLAY_NAME = AppName Beta

// Release.xcconfig
API_BASE_URL = https:\/\/api.example.com
BUNDLE_ID_SUFFIX =
APP_DISPLAY_NAME = AppName
```

Access in code via Info.plist and Bundle.main.

SWIFT PACKAGE DEPENDENCIES:

Add via Package.swift or Xcode SPM integration:
- Only include packages the app actually needs.
- Pin to exact versions or minor version ranges.
- Common packages to consider (add only if needed):
  - Alamofire (networking — only if URLSession wrapper is insufficient)
  - Kingfisher (image caching and loading)
  - Swinject (DI — only for complex dependency graphs)
  - SwiftLint (code style enforcement)

============================================================
PHASE 8: TESTING SETUP
============================================================

Unit tests:
- One test file per ViewModel.
- One test file per Service.
- Use protocol-based mocks (no third-party mocking frameworks by default).
- Test happy path, error cases, and edge cases.

UI tests:
- One test file per major user flow.
- Use accessibility identifiers for element queries.
- Test navigation flows, form submission, and error states.

Generate at least 3 unit tests and 1 UI test per major feature.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing the main phases, validate your work:

1. Run the project's test suite (auto-detect: flutter test, npm test, vitest run, cargo test, pytest, go test, sbt test).
2. Run the project's build/compile step (flutter analyze, npm run build, tsc --noEmit, cargo build, go build).
3. If either fails, diagnose the failure from error output.
4. Apply a minimal targeted fix — do NOT refactor unrelated code.
5. Re-run the failing validation.
6. Repeat up to 3 iterations total.

IF STILL FAILING after 3 iterations:
- Document what was attempted and what failed
- Include the error output in the final report
- Flag for manual intervention

============================================================
OUTPUT
============================================================

## iOS App Scaffold Complete

### Architecture
- **UI Framework:** {SwiftUI / UIKit / Hybrid}
- **Architecture:** MVVM with {manual DI / Swinject}
- **Persistence:** {SwiftData / Core Data}
- **Networking:** {URLSession / Alamofire} with APIRouter
- **Min Deployment:** iOS {16 / 17}

### Project Structure
{Tree listing of all generated files}

### Environments
| Config | Bundle ID | API URL | Features |
|--------|-----------|---------|----------|
| Dev | com.example.app.dev | api-dev.example.com | Debug overlays, verbose logging |
| Staging | com.example.app.staging | api-staging.example.com | TestFlight, standard logging |
| Release | com.example.app | api.example.com | App Store, minimal logging |

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| {name} | {version} | {why} |

### Generated Tests
| Test File | Tests | Coverage Area |
|-----------|-------|---------------|
| {file} | {count} | {what it tests} |

DO NOT:
- Use deprecated iOS APIs (UIWebView, UIAlertView, etc.).
- Hardcode API keys, secrets, or credentials anywhere in source files.
- Use force unwrapping (!) except in tests or where provably safe.
- Skip error handling — every async call must handle failure.
- Use Storyboards or XIBs unless the user explicitly requests UIKit with Interface Builder.
- Add packages speculatively — only include what the app requires.
- Write placeholder or stub implementations — every file must be complete and functional.
- Hardcode colors, fonts, or spacing — use DesignTokens and Asset Catalog.
- Skip accessibility — every interactive element needs an accessibility identifier.

NEXT STEPS:
- "Run `/mobile-test` to generate comprehensive unit, UI, and integration tests."
- "Run `/mobile-security-review` to audit authentication, keychain, and data protection."
- "Run `/app-store-publish` to set up Fastlane and App Store Connect publishing."
- "Run `/mobile-ci-cd` to configure CI/CD with code signing and TestFlight distribution."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /ios-app — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
