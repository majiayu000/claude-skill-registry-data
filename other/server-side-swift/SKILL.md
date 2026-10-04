---
name: server-side-swift
description: Server-side Swift development with Vapor and Hummingbird. Covers project setup, routing, Fluent ORM, authentication, deployment, and shared client-server code. Use when building backends or APIs in Swift.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion]
---

# Server-Side Swift Generator

Generates and guides server-side Swift projects using Vapor or Hummingbird, including API design, database integration, authentication, deployment, and shared code with iOS clients.

## When This Skill Activates

Use this skill when the user:
- Asks to "create a backend" or "build an API" in Swift
- Mentions "Vapor", "Hummingbird", or "server-side Swift"
- Wants JWT, OAuth, or session authentication on the server
- Needs to share Codable models between an iOS app and a Swift server
- Asks about sending push notifications from a server (APNSwift)
- Wants to deploy a Swift server (Docker, Fly.io, Railway)
- Mentions Fluent ORM, database migrations, or PostgreSQL with Swift
- Asks about WebSockets or real-time features on the server
- Wants to replace CloudKit with a custom backend

## Pre-Generation Checks

### 1. Project Context Detection

- [ ] Check if a `Package.swift` already exists
- [ ] Determine if this is a new project or adding to an existing one
- [ ] Check Swift version (async/await requires Swift 5.5+, Hummingbird 2 requires Swift 6+)
- [ ] Search for existing server-side code

```
Glob: **/Package.swift, **/configure.swift, **/routes.swift, **/entrypoint.swift
Grep: "import Vapor" or "import Hummingbird" or "import Fluent"
```

### 2. Conflict Detection

Search for existing server implementations:

```
Glob: **/Controllers/*.swift, **/Migrations/*.swift, **/Models/*.swift
Grep: "RouteCollection" or "AsyncMigration" or "func routes"
```

If found, ask user:
- Extend existing server with new endpoints?
- Replace existing implementation?

### 3. iOS Client Detection

Check if an iOS client exists in the workspace:

```
Glob: **/*.xcodeproj, **/*.xcworkspace
Grep: "import SwiftUI" or "import UIKit"
```

If found, recommend SharedModels package pattern.

## Architecture Decision Gate

**Before asking about framework choice**, validate that server-side Swift is the right technology for this project. Reference **architecture-decisions.md** for the full decision framework.

### Quick Validation (ask yourself, not the user)

1. Does the user have a Swift team or iOS app? → If no, surface alternatives (Go, Node.js, Python)
2. Does client-server code sharing provide value? → Strongest signal for Swift
3. Does the project need integrations Swift lacks (Kafka, Elasticsearch, email)? → Surface ecosystem gaps honestly

If any red flags, present trade-offs from architecture-decisions.md before proceeding. Example:

> "Before we start — server-side Swift works best when you have an iOS app that can share models with the backend. Since your project is [web-only / cross-platform / ML-heavy], you might want to consider [Node.js / Go / Python] instead. Want me to explain the trade-offs, or proceed with Swift?"

### If "Help me decide" on Vapor vs Hummingbird

Don't default arbitrarily. Ask about context:
- **Team size and experience** — New to server Swift? → Vapor (more docs, bigger community)
- **Project type** — Lambda/microservice? → Hummingbird (smaller binary, first-class Lambda)
- **Compile time sensitivity** — Tight CI/CD? → Hummingbird (lighter dependency graph)
- **Feature needs** — Need ORM + auth + WebSocket out of the box? → Vapor

Reference the weighted decision matrix in **architecture-decisions.md** for detailed comparison.

## Configuration Questions

Ask user via AskUserQuestion:

1. **Which framework do you want to use?**
   - Vapor (batteries-included, Fluent ORM, larger community — 78% market share)
   - Hummingbird (lightweight, pure structured concurrency, modular — ideal for microservices/Lambda)
   - Help me decide (I'll ask about your project context)

2. **What database do you need?**
   - PostgreSQL (recommended for production)
   - SQLite (development/lightweight)
   - None (stateless API)
   - MongoDB

3. **What authentication method?**
   - JWT (stateless, recommended for mobile APIs)
   - Session-based (web apps)
   - Sign in with Apple (server-side validation)
   - Bearer token (simple)
   - None

4. **Do you need shared models with an iOS client?**
   - Yes, create a SharedModels package
   - No, server-only project

## Generation Process

### Step 1: Project Scaffolding

Generate the project structure based on framework choice:

**Vapor:**
```
Sources/App/
├── Controllers/
├── Migrations/
├── Models/
├── DTOs/
├── configure.swift
├── entrypoint.swift
└── routes.swift
Tests/AppTests/
Package.swift
Dockerfile
docker-compose.yml
.env
.gitignore
```

**Hummingbird:**
```
Sources/App/
├── Controllers/
├── Models/
├── Application+build.swift
└── App.swift
Tests/AppTests/
Package.swift
Dockerfile
```

### Step 2: Core Files

Generate based on configuration:
1. `Package.swift` - Dependencies for chosen framework + database + auth
2. `configure.swift` / `Application+build.swift` - App configuration
3. Entry point with environment detection
4. Basic health check endpoint

### Step 3: Database Layer (if selected)

1. Model files with Fluent property wrappers
2. Migration files with `AsyncMigration`
3. Database configuration in `configure.swift`

### Step 4: Authentication (if selected)

1. Auth middleware and authenticators
2. Token/session model and migration
3. Protected route groups
4. Login/register endpoints

### Step 5: Shared Models (if selected)

1. `SharedModels/` package with DTOs
2. Update both `Package.swift` files to depend on SharedModels
3. API endpoint protocol definitions

### Step 6: Deployment Files

1. Multi-stage `Dockerfile`
2. `docker-compose.yml` with database service
3. `.env` template with required variables

## Swift 6 Concurrency Notes

### Vapor 4 Async/Await

All new code should use async/await exclusively:
```swift
app.get("users") { req async throws -> [User] in
    try await User.query(on: req.db).all()
}
```

### Hummingbird 2 Pure Concurrency

Hummingbird 2 is built entirely on structured concurrency with no EventLoopFuture APIs:
```swift
router.get("users") { request, context async throws -> [UserDTO] in
    try await userRepository.findAll()
}
```

### Sendable Compliance

All DTOs shared between client and server must be `Sendable`:
```swift
public struct UserDTO: Codable, Sendable {
    public let id: UUID?
    public let name: String
    public let email: String
}
```

## Output Format

### Files Created

```
YourProject/
├── Sources/App/
│   ├── Controllers/
│   │   └── TodoController.swift    # Route collection
│   ├── Migrations/
│   │   └── CreateTodo.swift        # Database migration
│   ├── Models/
│   │   └── Todo.swift              # Fluent model
│   ├── DTOs/
│   │   └── TodoDTO.swift           # Request/response DTO
│   ├── configure.swift             # App configuration
│   ├── entrypoint.swift            # Entry point
│   └── routes.swift                # Route registration
├── Tests/AppTests/
│   └── TodoTests.swift             # Integration tests
├── Package.swift                   # Dependencies
├── Dockerfile                      # Multi-stage build
├── docker-compose.yml              # App + database
└── .env                            # Environment variables
```

### Integration Steps

**Run locally:**
```bash
# Start database
docker-compose up db -d

# Run migrations
swift run App migrate --yes

# Start server
swift run App serve --hostname 0.0.0.0 --port 8080
```

**Connect from iOS client:**
```swift
let client = URLSessionAPIClient(
    configuration: .init(baseURL: URL(string: "http://localhost:8080/api/v1")!)
)
let todos = try await client.request(ListTodosEndpoint())
```

### Testing

```swift
@Suite("API Tests", .serialized)
struct TodoTests {
    @Test("Create todo returns 200")
    func createTodo() async throws {
        try await withApp(configure: configure) { app in
            let dto = TodoDTO(title: "Test")
            try await app.testing().test(.POST, "api/v1/todos", beforeRequest: { req in
                try req.content.encode(dto)
            }, afterResponse: { res async throws in
                #expect(res.status == .ok)
                let created = try res.content.decode(TodoDTO.self)
                #expect(created.title == "Test")
            })
        }
    }
}
```

## References

- **architecture-decisions.md** - When to use server-side Swift, Vapor vs Hummingbird decision matrix, ecosystem gaps, pitfalls
- **vapor-patterns.md** - Routing, controllers, middleware, configuration
- **hummingbird-patterns.md** - Hummingbird 2 patterns and Vapor vs Hummingbird decision
- **database-patterns.md** - Fluent ORM, migrations, queries, relationships
- **auth-patterns.md** - JWT, sessions, Bearer, Sign in with Apple server-side
- **deployment-patterns.md** - Docker, Fly.io, Railway, production setup
- **shared-code-patterns.md** - SharedModels, DTOs, APNSwift
- **testing-patterns.md** - VaporTesting, Swift Testing, integration tests
- [Vapor Documentation](https://docs.vapor.codes/)
- [Hummingbird Documentation](https://docs.hummingbird.codes/)
- [Swift on Server](https://www.swift.org/documentation/server/)
