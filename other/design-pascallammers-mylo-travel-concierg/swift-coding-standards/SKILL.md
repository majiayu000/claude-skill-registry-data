---
name: swift-coding-standards
category: coding-standards
difficulty: intermediate
estimated_time: 45 minutes
description: Master Swift coding standards with Apple's guidelines, protocol-oriented design, and modern concurrency patterns
version: 1.0.0
tags: [swift, ios, macos, mobile, apple]
related_skills: [kotlin-coding-standards, typescript-coding-standards]
---

# Swift Coding Standards

> **Learn Once, Write Anywhere**: Master Swift coding standards for iOS, macOS, watchOS, and tvOS development with protocol-oriented design, value semantics, and modern concurrency.

## Level 1: Quick Reference

### Optionals Cheat Sheet

```swift
// Optional binding (safe unwrapping)
if let name = name { print("Hello, \(name)") }

// Guard statement (early exit)
guard let age = age else { return }

// Nil coalescing (default value)
let displayName = name ?? "Anonymous"

// Optional chaining
let count = user?.profile?.posts?.count
```

### Essential Patterns

```swift
// Protocol definition with default implementation
protocol Drawable {
    var color: Color { get set }
    func draw()
}

extension Drawable {
    func draw() { print("Drawing with \(color)") }
}

// Struct with protocol conformance
struct Circle: Drawable {
    var color: Color
    var radius: Double
}

// Closure syntax
let doubled = numbers.map { $0 * 2 }

// Property wrapper
@State private var isPresented = false
```

### Naming Conventions

```swift
// Types: PascalCase
class UserProfileViewController { }
struct NetworkRequest { }
protocol DataSource { }

// Variables/Functions: camelCase
var userName: String
func fetchUserProfile() { }

// Booleans: use is/has/should prefix
var isLoading: Bool
var hasCompletedOnboarding: Bool
```

### Pre-Commit Checklist

- [ ] SwiftLint passes with zero warnings
- [ ] All optionals handled safely (no force unwrapping)
- [ ] Access control specified (private, internal, public)
- [ ] Memory cycles avoided (weak/unowned references)
- [ ] Unit tests cover happy and error paths

---

## Level 2: Implementation Guide

### 1. Optionals and Safety

Swift's optional system eliminates null pointer exceptions through compile-time safety.

```swift
// Safe unwrapping patterns
if let unwrapped = optionalValue {
    print(unwrapped)
}

// Multiple bindings
if let name = userName, let age = userAge, age >= 18 {
    print("\(name) is an adult")
}

// Guard for early exit
func processUser(_ user: User?) {
    guard let user = user else { return }
    print(user.name)
}

// Optional map/flatMap
let uppercasedName = userName.map { $0.uppercased() }
let userID = userIDString.flatMap { Int($0) }
```

### 2. Protocol-Oriented Design

Swift favors composition over inheritance through protocols.

```swift
// Define capabilities through protocols
protocol DataStore {
    func save<T: Codable>(_ item: T, key: String) throws
    func load<T: Codable>(key: String) throws -> T?
}

// Protocol extension for default behavior
extension Collection {
    func chunked(into size: Int) -> [[Element]] {
        stride(from: 0, to: count, by: size).map {
            Array(self[$0..<Swift.min($0 + size, count)])
        }
    }
}

// Associated types for flexibility
protocol Repository {
    associatedtype Item
    func fetchAll() async throws -> [Item]
    func save(_ item: Item) async throws
}
```

### 3. Value Types vs Reference Types

```swift
// Use struct (value type) for:
// - Simple data models, independent copies
struct User {
    var name: String
    var email: String
}

// Use class (reference type) for:
// - Shared mutable state, object identity matters
class NetworkManager {
    static let shared = NetworkManager()
}

// Use enum for:
// - Finite set of options, state machines
enum LoadingState {
    case idle, loading
    case success(Data)
    case failure(Error)
}
```

### 4. Memory Management with ARC

```swift
// Breaking cycles with weak
class Apartment {
    weak var tenant: Person?  // weak breaks the cycle
}

// Closure capture lists
onComplete = { [weak self] in
    self?.processResult()  // Safe optional call
}

// Use unowned when reference should never be nil
class CreditCard {
    unowned let customer: Customer  // Card can't exist without customer
}
```

### 5. Error Handling

```swift
enum NetworkError: Error {
    case invalidURL
    case noConnection
    case serverError(statusCode: Int)
}

func fetchUser(id: Int) throws -> User {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        throw NetworkError.invalidURL
    }
    // ... implementation
}

// Calling throwing functions
do {
    let user = try fetchUser(id: 123)
} catch NetworkError.serverError(let code) {
    print("Server error: \(code)")
} catch {
    print("Unknown error: \(error)")
}
```

### 6. Modern Concurrency (async/await)

```swift
// Async functions
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Parallel execution with TaskGroup
func fetchAllUsers(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask { try await fetchUser(id: id) }
        }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}

// Actors for thread-safe state
actor BankAccount {
    private var balance: Double = 0
    func deposit(_ amount: Double) { balance += amount }
    func getBalance() -> Double { balance }
}

// MainActor for UI updates
@MainActor
class ViewModel: ObservableObject {
    @Published var isLoading = false
    @Published var users: [User] = []
}
```

### 7. Testing with XCTest

```swift
import XCTest
@testable import MyApp

final class UserManagerTests: XCTestCase {
    var sut: UserManager!
    var mockStore: MockDataStore!

    override func setUp() {
        super.setUp()
        mockStore = MockDataStore()
        sut = UserManager(store: mockStore)
    }

    func testFetchUser_Success() async throws {
        // Arrange
        mockStore.userToReturn = User(id: 1, name: "John")

        // Act
        let user = try await sut.fetchUser(id: 1)

        // Assert
        XCTAssertEqual(user.name, "John")
        XCTAssertTrue(mockStore.fetchUserCalled)
    }
}
```

---

## Level 3: Deep Dive Resources

For comprehensive examples and advanced patterns, see [REFERENCE.md](./REFERENCE.md).

### Advanced Topics Covered in REFERENCE.md

- **Generics**: Type constraints, associated types, type erasure
- **Property Wrappers**: @State, @Binding, custom wrappers
- **Result Builders**: Creating custom DSLs
- **SwiftUI Architecture**: MVVM, state management, navigation
- **Performance Optimization**: Instruments profiling, COW patterns
- **Complete Code Examples**: Network layer, repositories, mocks

### Quick Setup

```bash
# Install SwiftLint
brew install swiftlint

# Add to Xcode build phase
if which swiftlint >/dev/null; then swiftlint; fi

# Run manually
swiftlint lint --config .swiftlint.yml
```

### Official Documentation

- [Swift Language Guide](https://docs.swift.org/swift-book/)
- [API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- [Swift Evolution Proposals](https://github.com/apple/swift-evolution)

### Learning Path

1. **Week 1-2**: Optionals, protocols, value/reference types
2. **Week 3-4**: Memory management, error handling, testing
3. **Week 5-6**: Async/await, actors, structured concurrency
4. **Week 7-8**: SwiftUI, Combine, advanced patterns

### Bundled Resources

- `config/.swiftlint.yml` - SwiftLint configuration
- `templates/ViewModel.swift` - MVVM template
- `templates/NetworkService.swift` - Async network layer
- `templates/TestCase.swift` - XCTest template

---

*Remember: Swift is designed for safety, speed, and expressiveness. Embrace optionals, leverage protocols, and write tests.*
