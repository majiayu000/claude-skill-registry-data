---
name: ios-architecture
description: iOS app architecture design with SwiftUI and MVVM from Apple's iOS Platform Team. Use when designing scalable iOS app structure, implementing MVVM/Clean Architecture in Swift, organizing Xcode projects, setting up navigation patterns, managing dependencies with Swift Package Manager, or planning data flow with Combine/async-await. Triggers on iOS architecture, SwiftUI app structure, MVVM pattern, iOS project setup, or Swift app design.
---

# iOS Architecture - SwiftUI & MVVM

**Purpose**: Design scalable iOS applications with clean architecture patterns

**Agent**: Apple iOS Lead
**Use When**: Building iOS apps with SwiftUI, architecting app structure, or managing state

---

## MVVM Pattern

### Model

```swift
struct User: Identifiable, Codable {
    let id: Int
    let name: String
    let email: String
}

struct Post: Identifiable, Codable {
    let id: Int
    let title: String
    let body: String
    let userId: Int
}
```

### ViewModel

```swift
@MainActor
class UserViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let repository: UserRepository

    init(repository: UserRepository = UserRepository()) {
        self.repository = repository
    }

    func loadUsers() async {
        isLoading = true
        errorMessage = nil

        do {
            users = try await repository.fetchUsers()
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }
}
```

### View

```swift
struct UserListView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        NavigationView {
            Group {
                if viewModel.isLoading {
                    ProgressView()
                } else if let error = viewModel.errorMessage {
                    Text("Error: \(error)")
                        .foregroundColor(.red)
                } else {
                    List(viewModel.users) { user in
                        NavigationLink(destination: UserDetailView(user: user)) {
                            UserRow(user: user)
                        }
                    }
                }
            }
            .navigationTitle("Users")
            .task {
                await viewModel.loadUsers()
            }
        }
    }
}

struct UserRow: View {
    let user: User

    var body: some View {
        VStack(alignment: .leading) {
            Text(user.name)
                .font(.headline)
            Text(user.email)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
    }
}
```

---

## Networking Layer

```swift
protocol APIService {
    func fetchUsers() async throws -> [User]
    func fetchUser(id: Int) async throws -> User
    func createUser(_ user: User) async throws -> User
}

class NetworkService: APIService {
    private let baseURL = "https://api.example.com"

    func fetchUsers() async throws -> [User] {
        let url = URL(string: "\(baseURL)/users")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode([User].self, from: data)
    }

    func fetchUser(id: Int) async throws -> User {
        let url = URL(string: "\(baseURL)/users/\(id)")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return try JSONDecoder().decode(User.self, from: data)
    }

    func createUser(_ user: User) async throws -> User {
        let url = URL(string: "\(baseURL)/users")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(user)

        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(User.self, from: data)
    }
}
```

---

## Repository Pattern

```swift
class UserRepository {
    private let networkService: APIService
    private let cacheService: CacheService

    init(
        networkService: APIService = NetworkService(),
        cacheService: CacheService = CacheService()
    ) {
        self.networkService = networkService
        self.cacheService = cacheService
    }

    func fetchUsers() async throws -> [User] {
        // Try cache first
        if let cached = cacheService.getUsers() {
            return cached
        }

        // Fetch from network
        let users = try await networkService.fetchUsers()

        // Update cache
        cacheService.saveUsers(users)

        return users
    }
}
```

---

## Dependency Injection

```swift
// Protocol-based dependency injection
protocol UserRepositoryProtocol {
    func fetchUsers() async throws -> [User]
}

class UserViewModel: ObservableObject {
    private let repository: UserRepositoryProtocol

    init(repository: UserRepositoryProtocol) {
        self.repository = repository
    }
}

// In preview/tests, inject mock
class MockUserRepository: UserRepositoryProtocol {
    func fetchUsers() async throws -> [User] {
        return [
            User(id: 1, name: "Test User", email: "test@example.com")
        ]
    }
}

struct UserListView_Previews: PreviewProvider {
    static var previews: some View {
        UserListView(viewModel: UserViewModel(repository: MockUserRepository()))
    }
}
```

---

## State Management

```swift
// @State for local view state
struct Counter: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") { count += 1 }
        }
    }
}

// @StateObject for view model
struct UserListView: View {
    @StateObject private var viewModel = UserViewModel()
}

// @ObservedObject for passed-in view model
struct DetailView: View {
    @ObservedObject var viewModel: UserViewModel
}

// @EnvironmentObject for app-wide state
class AppState: ObservableObject {
    @Published var isLoggedIn = false
    @Published var currentUser: User?
}

@main
struct MyApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
    }
}

struct ProfileView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        if let user = appState.currentUser {
            Text("Welcome, \(user.name)")
        }
    }
}
```

---

## Best Practices

- Use MVVM for separation of concerns
- ViewModels should not import SwiftUI
- Repository pattern for data layer
- Protocol-based dependency injection
- Async/await for networking
- `@Published` for observable properties
- Environment objects for global state
- Preview providers for UI development

---

**Remember**: SwiftUI is declarative. Think in terms of state and views that react to changes.

**Created**: 2026-02-04
**Maintained By**: Apple iOS Lead
