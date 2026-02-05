---
name: fosmvvm-viewmodel-generator
description: Generate FOSMVVM ViewModels - the bridge between server-side data and client-side Views. Use when creating new screens, pages, components, or any UI that displays data.
---

# FOSMVVM ViewModel Generator

Generate ViewModels following FOSMVVM architecture patterns.

## Conceptual Foundation

> For full architecture context, see [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md)

A **ViewModel** is the bridge in the Model-View-ViewModel architecture:

```
┌─────────────┐      ┌─────────────────┐      ┌─────────────┐
│    Model    │ ───► │    ViewModel    │ ───► │    View     │
│   (Data)    │      │  (The Bridge)   │      │  (SwiftUI)  │
└─────────────┘      └─────────────────┘      └─────────────┘
```

**Key insight:** In FOSMVVM, ViewModels are:
- **Created by a Factory** (either server-side or client-side)
- **Localized during encoding** (resolves all `@LocalizedString` references)
- **Consumed by Views** which just render the localized data

---

## First Decision: Hosting Mode

**This is a per-ViewModel decision.** An app can mix both modes - for example, a standalone iPhone app with server-based sign-in.

Ask: **Where does THIS ViewModel's data come from?**

| Data Source | Hosting Mode | Factory |
|-------------|--------------|---------|
| Server/Database | Server-Hosted | Hand-written |
| Local state/preferences | Client-Hosted | Macro-generated |

### Server-Hosted Mode

When data comes from a server:
- Factory is **hand-written** on server (`ViewModelFactory` protocol)
- Factory queries database, builds ViewModel
- Server localizes during JSON encoding
- Client receives fully localized ViewModel

**Examples:** Sign-in screen, user profile from API, dashboard with server data

### Client-Hosted Mode

When data is local to the device:
- Use `@ViewModel(options: [.clientHostedFactory])`
- Macro **auto-generates** factory from init parameters
- Client bundles YAML resources
- Client localizes during encoding

**Examples:** Settings screen, onboarding, offline-first features

### Hybrid Apps

Many apps use both:
```
┌─────────────────────────────────────────┐
│            iPhone App                    │
├─────────────────────────────────────────┤
│ SettingsViewModel      → Client-Hosted  │
│ OnboardingViewModel    → Client-Hosted  │
│ SignInViewModel        → Server-Hosted  │
│ UserProfileViewModel   → Server-Hosted  │
└─────────────────────────────────────────┘
```

**Same ViewModel patterns work in both modes** - only the factory creation differs.

### Core Responsibility: Shaping Data

A ViewModel's job is **shaping data for presentation**. This happens in two places:

1. **Factory** - *what* data is needed, *how* to transform it
2. **Localization** - *how* to present it in context (including locale-aware ordering)

**The View just renders** - it should never compose, format, or reorder ViewModel properties.

### What a ViewModel Contains

A ViewModel answers: **"What does the View need to display?"**

| Content Type | How It's Represented | Example |
|--------------|---------------------|---------|
| Static UI text | `@LocalizedString` | Page titles, button labels (fixed text) |
| Dynamic enum values | `LocalizableString` (stored) | Status/state display (see Enum Localization Pattern) |
| Dynamic data in text | `@LocalizedSubs` | "Welcome, %{name}!" with substitutions |
| Composed text | `@LocalizedCompoundString` | Full name from pieces (locale-aware order) |
| Formatted dates | `LocalizableDate` | `createdAt: LocalizableDate` |
| Formatted numbers | `LocalizableInt` | `totalCount: LocalizableInt` |
| Dynamic data | Plain properties | `content: String`, `count: Int` |
| Nested components | Child ViewModels | `cards: [CardViewModel]` |

### What a ViewModel Does NOT Contain

- Database relationships (`@Parent`, `@Siblings`)
- Business logic or validation (that's in Fields protocols)
- Raw database IDs exposed to templates (use typed properties)
- Unlocalized strings that Views must look up

### Anti-Pattern: Composition in Views

```swift
// ❌ WRONG - View is composing
Text(viewModel.firstName) + Text(" ") + Text(viewModel.lastName)

// ✅ RIGHT - ViewModel provides shaped result
Text(viewModel.fullName)  // via @LocalizedCompoundString
```

If you see `+` or string interpolation in a View, the shaping belongs in the ViewModel.

## ViewModel Protocol Hierarchy

```swift
public protocol ViewModel: ServerRequestBody, RetrievablePropertyNames, Identifiable, Stubbable {
    var vmId: ViewModelId { get }
}

public protocol RequestableViewModel: ViewModel {
    associatedtype Request: ViewModelRequest
}
```

**ViewModel** provides:
- `ServerRequestBody` - Can be sent over HTTP as JSON
- `RetrievablePropertyNames` - Enables `@LocalizedString` binding (via `@ViewModel` macro)
- `Identifiable` - Has `vmId` for SwiftUI identity
- `Stubbable` - Has `stub()` for testing/previews

**RequestableViewModel** adds:
- Associated `Request` type for fetching from server

## Two Categories of ViewModels

### 1. Top-Level (RequestableViewModel)

Represents a full page or screen. Has:
- An associated `ViewModelRequest` type
- A `ViewModelFactory` that builds it from database
- Child ViewModels embedded within it

```swift
@ViewModel
public struct DashboardViewModel: RequestableViewModel {
    public typealias Request = DashboardRequest

    @LocalizedString public var pageTitle
    public let cards: [CardViewModel]  // Children
    public var vmId: ViewModelId = .init()
}
```

### 2. Child (plain ViewModel)

Nested components built by their parent's factory. No Request type.

```swift
@ViewModel
public struct CardViewModel: Codable, Sendable {
    public let id: ModelIdType
    public let title: String
    public let createdAt: LocalizableDate
    public var vmId: ViewModelId = .init()
}
```

---

## Display vs Form ViewModels

ViewModels serve two distinct purposes:

| Purpose | ViewModel Type | Adopts Fields? |
|---------|----------------|----------------|
| **Display data** (read-only) | Display ViewModel | No |
| **Collect user input** (editable) | Form ViewModel | Yes |

### Display ViewModels

For showing data - cards, rows, lists, detail views:

```swift
@ViewModel
public struct UserCardViewModel {
    public let id: ModelIdType
    public let name: String
    @LocalizedString public var roleDisplayName
    public let createdAt: LocalizableDate
    public var vmId: ViewModelId = .init()
}
```

**Characteristics:**
- Properties are `let` (read-only)
- No validation needed
- No FormField definitions
- Just projects Model data for display

### Form ViewModels

For collecting input - create forms, edit forms, settings:

```swift
@ViewModel
public struct UserFormViewModel: UserFields {  // ← Adopts Fields!
    public var id: ModelIdType?
    public var email: String
    public var firstName: String
    public var lastName: String

    public let userValidationMessages: UserFieldsMessages
    public var vmId: ViewModelId = .init()
}
```

**Characteristics:**
- Properties are `var` (editable)
- **Adopts a Fields protocol** for validation
- Gets FormField definitions from Fields
- Gets validation logic from Fields
- Gets localized error messages from Fields

### The Connection

```
┌─────────────────────────────────────────────────────────────────┐
│                    UserFields Protocol                          │
│        (defines editable properties + validation)               │
│                                                                 │
│  Adopted by:                                                    │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ CreateUserReq   │  │ UserFormVM      │  │ User (Model)    │ │
│  │ .RequestBody    │  │ (UI form)       │  │ (persistence)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
│  Same validation logic everywhere!                              │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Decision Guide

Ask: **"Is the user editing data in this ViewModel?"**

- **No** → Display ViewModel (no Fields)
- **Yes** → Form ViewModel (adopt Fields)

| ViewModel | User Edits? | Adopt Fields? |
|-----------|-------------|---------------|
| `UserCardViewModel` | No | No |
| `UserRowViewModel` | No | No |
| `UserDetailViewModel` | No | No |
| `UserFormViewModel` | Yes | `UserFields` |
| `CreateUserViewModel` | Yes | `UserFields` |
| `EditUserViewModel` | Yes | `UserFields` |
| `SettingsViewModel` | Yes | `SettingsFields` |

---

## When to Use This Skill

- Creating a new page or screen
- Adding a new UI component (card, row, modal, etc.)
- Displaying data from the database in a View
- Following an implementation plan that requires new ViewModels

## What This Skill Generates

### Server-Hosted: Top-Level ViewModel (4 files)

| File | Location | Purpose |
|------|----------|---------|
| `{Name}ViewModel.swift` | `{ViewModelsTarget}/` | The ViewModel struct |
| `{Name}Request.swift` | `{ViewModelsTarget}/` | The ViewModelRequest type |
| `{Name}ViewModel.yml` | `{ResourcesPath}/` | Localization strings |
| `{Name}ViewModel+Factory.swift` | `{WebServerTarget}/` | Factory that builds from DB |

### Client-Hosted: Top-Level ViewModel (2 files)

| File | Location | Purpose |
|------|----------|---------|
| `{Name}ViewModel.swift` | `{ViewModelsTarget}/` | ViewModel with `clientHostedFactory` option |
| `{Name}ViewModel.yml` | `{ResourcesPath}/` | Localization strings (bundled in app) |

*No Request or Factory files needed - macro generates them!*

### Child ViewModels (1-2 files, either mode)

| File | Location | Purpose |
|------|----------|---------|
| `{Name}ViewModel.swift` | `{ViewModelsTarget}/` | The ViewModel struct |
| `{Name}ViewModel.yml` | `{ResourcesPath}/` | Localization (if has `@LocalizedString`) |

## Project Structure Configuration

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{ViewModelsTarget}` | Shared ViewModels SPM target | `ViewModels` |
| `{ResourcesPath}` | Localization resources | `Sources/Resources` |
| `{WebServerTarget}` | Server-side target | `WebServer`, `AppServer` |

## Generation Process

### Step 1: Determine Hosting Mode

Ask: **Where does this ViewModel's data come from?**
- **Server/database** → Server-Hosted (hand-written factory)
- **Local state** → Client-Hosted (macro-generated factory)

### Step 2: Understand What the View Needs

Clarify:
1. **What is this View displaying?** (page, modal, card, row?)
2. **What data does it need?** (from database? from AppState?)
3. **What static text does it have?** (titles, labels, buttons)
4. **Does it contain child ViewModels?**
5. **Is it top-level or a child?**

### Step 3: Design the ViewModel

Determine:
- **Properties** - What does the View need to render?
- **Localization** - Which properties are `@LocalizedString`?
- **Identity** - Singleton (`vmId = .init(type: Self.self)`) or instance (`vmId = .init(id: id)`)?

### Step 4: Generate Files

**Server-Hosted Top-Level:**
1. ViewModel struct (with `RequestableViewModel`)
2. Request type
3. YAML localization
4. Factory implementation

**Client-Hosted Top-Level:**
1. ViewModel struct (with `clientHostedFactory` option)
2. YAML localization

**Child (either mode):**
1. ViewModel struct
2. YAML localization (if needed)

## Key Patterns

### The @ViewModel Macro

Always use the `@ViewModel` macro - it generates the `propertyNames()` method required for localization binding.

**Server-Hosted** (basic macro):
```swift
@ViewModel
public struct MyViewModel: RequestableViewModel {
    public typealias Request = MyRequest
    @LocalizedString public var title
    public var vmId: ViewModelId = .init()
    public init() {}
}
```

**Client-Hosted** (with factory generation):
```swift
@ViewModel(options: [.clientHostedFactory])
public struct SettingsViewModel {
    @LocalizedString public var pageTitle
    public var vmId: ViewModelId = .init()

    public init(theme: Theme, notifications: NotificationSettings) {
        // Init parameters become AppState properties
    }
}

// Macro auto-generates:
// - typealias Request = ClientHostedRequest
// - struct AppState { let theme: Theme; let notifications: NotificationSettings }
// - class ClientHostedRequest: ViewModelRequest { ... }
// - static func model(context:) async throws -> Self { ... }
```

### Stubbable Pattern

All ViewModels must support `stub()` for testing and SwiftUI previews:

```swift
public extension MyViewModel {
    static func stub() -> Self {
        .init(/* default values */)
    }
}
```

### Identity: vmId

Every ViewModel needs a `vmId` for SwiftUI's identity system:

**Singleton** (one per page): `vmId = .init(type: Self.self)`
**Instance** (multiple per page): `vmId = .init(id: id)` where `id: ModelIdType`

### Localization

Static UI text uses `@LocalizedString`:

```swift
@LocalizedString public var pageTitle
```

With corresponding YAML:
```yaml
en:
  MyViewModel:
    pageTitle: "Welcome"
```

### Dates and Numbers

Never send pre-formatted strings. Use localizable types:

```swift
public let createdAt: LocalizableDate    // NOT String
public let itemCount: LocalizableInt     // NOT String
```

The client formats these according to user's locale and timezone.

### Enum Localization Pattern

For dynamic enum values (status, state, category), use a **stored `LocalizableString`** - NOT `@LocalizedString`.

`@LocalizedString` always looks up the same key (the property name). A stored `LocalizableString` carries the dynamic key from the enum case.

```swift
// Enum provides localizableString
public enum SessionState: String, CaseIterable, Codable, Sendable {
    case pending, running, completed, failed

    public var localizableString: LocalizableString {
        .localized(for: Self.self, propertyName: rawValue)
    }
}

// ViewModel stores it (NOT @LocalizedString)
@ViewModel
public struct SessionCardViewModel {
    public let state: SessionState                // Raw enum for data attributes
    public let stateDisplay: LocalizableString   // Localized display text

    public init(session: Session) {
        self.state = session.state
        self.stateDisplay = session.state.localizableString
    }
}
```

```yaml
# YAML keys match enum type and case names
en:
  SessionState:
    pending: "Pending"
    running: "Running"
    completed: "Completed"
    failed: "Failed"
```

**Constraint:** `LocalizableString` only works in ViewModels encoded with `localizingEncoder()`. Do not use in Fluent JSONB fields or other persisted types.

### Child ViewModels

Top-level ViewModels contain their children:

```swift
@ViewModel
public struct BoardViewModel: RequestableViewModel {
    public let columns: [ColumnViewModel]
    public let cards: [CardViewModel]
}
```

The Factory builds all children when building the parent.

### Codable and Computed Properties

Swift's synthesized `Codable` only encodes **stored properties**. Since ViewModels are serialized (for JSON transport, Leaf rendering, etc.), computed properties won't be available.

```swift
// Computed - NOT encoded, invisible after serialization
public var hasCards: Bool { !cards.isEmpty }

// Stored - encoded, available after serialization
public let hasCards: Bool
```

**When to pre-compute:**

For Leaf templates, you can often use Leaf's built-in functions directly:
- `#if(count(cards) > 0)` - no need for `hasCards` property
- `#count(cards)` - no need for `cardCount` property

Pre-compute only when:
- Direct array subscripts needed (`firstCard` - array indexing not documented in Leaf)
- Complex logic that's cleaner in Swift than in template
- Performance-sensitive repeated calculations

See [fosmvvm-leaf-view-generator](../fosmvvm-leaf-view-generator/SKILL.md) for Leaf template patterns.

## File Templates

See [reference.md](reference.md) for complete file templates.

## Naming Conventions

| Concept | Convention | Example |
|---------|------------|---------|
| ViewModel struct | `{Name}ViewModel` | `DashboardViewModel` |
| Request class | `{Name}Request` | `DashboardRequest` |
| Factory extension | `{Name}ViewModel+Factory.swift` | `DashboardViewModel+Factory.swift` |
| YAML file | `{Name}ViewModel.yml` | `DashboardViewModel.yml` |

## Collaboration Protocol

1. Understand what the View needs to display
2. Confirm whether it's top-level or child
3. **Display or Form?** - If form, use fields-generator first to create Fields protocol
4. Identify which properties need localization
5. Generate files one at a time with feedback

## See Also

- [FOSMVVMArchitecture.md](../../docs/FOSMVVMArchitecture.md) - Full FOSMVVM architecture
- [fosmvvm-fields-generator](../fosmvvm-fields-generator/SKILL.md) - For form validation
- [fosmvvm-fluent-datamodel-generator](../fosmvvm-fluent-datamodel-generator/SKILL.md) - For Fluent persistence layer
- [fosmvvm-leaf-view-generator](../fosmvvm-leaf-view-generator/SKILL.md) - For Leaf templates that render ViewModels
- [reference.md](reference.md) - Complete file templates

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-24 | Initial skill |
| 2.0 | 2024-12-26 | Complete rewrite from architecture; generalized from Kairos-specific |
| 2.1 | 2024-12-26 | Added Client-Hosted mode support; per-ViewModel hosting decision |
| 2.2 | 2024-12-26 | Added shaping responsibility, @LocalizedSubs/@LocalizedCompoundString, anti-pattern |
| 2.3 | 2025-12-27 | Added Display vs Form ViewModels section; clarified Fields adoption |
| 2.4 | 2026-01-08 | Added Codable/computed properties section. Clarified when to pre-compute vs use Leaf built-ins. |
| 2.5 | 2026-01-19 | Added Enum Localization Pattern section. Clarified @LocalizedString is for static text only; stored LocalizableString for dynamic enum values. |
