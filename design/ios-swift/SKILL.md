---
name: ios-swift
description: Expertise in developing and maintaining the Swift/SwiftUI iOS application.
---

# iOS (Swift/SwiftUI) Development Skill

## Main Instructions

When working on the iOS app (`apps/ios/`), you MUST follow these instructions:

### 1. Before Writing Any Code
- Understand the project structure:
  - `Core/` — Shared infrastructure (DI, Network, Extensions, Domain Entities, UI Components).
  - `Features/` — Feature modules, each with its own `Data/`, `Domain/`, `Presentation/` layers.
  - `App/` — App entry point and root configuration.
- Identify which feature and layer the change belongs to.

### 2. Feature Module Structure (ALWAYS Follow)
Every feature in `Features/` MUST use this 3-layer convention:
```
Features/MyFeature/
├── Data/           # Repositories, API data sources
├── Domain/         # Entities, domain models
└── Presentation/   # ViewModels, SwiftUI Views
```

### 3. When Adding a New Feature
1. Create a new subfolder in `Features/` following the 3-layer structure above.
2. Define domain models in `Domain/`.
3. Create the repository in `Data/` (implement `APIClientProtocol` for networking).
4. Implement the ViewModel in `Presentation/`.
5. Build SwiftUI Views in `Presentation/`.
6. Register any new services/repositories in `Core/DI/DependencyContainer`.
7. Run `make ios-sync` to sync the new files into the Xcode project.

### 4. When Modifying Existing Code
1. Check which feature and layer the change belongs to.
2. Keep changes within the correct layer boundaries.
3. If modifying shared components, update in `Core/UI/Components/`.
4. If modifying networking logic, update in `Core/Network/`.

### 5. Coding Standards
- Use **SwiftUI** for all UI development.
- Use **modern Swift Concurrency** (async/await) for all asynchronous operations.
- Follow the [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/).
- Use the `DependencyContainer` (`Core/DI/`) for all dependency injection.
- Use `APIClientProtocol` (`Core/Network/`) for all network requests.
- Ensure all UI components have accessibility labels and support dynamic text sizes.

### 6. Building & Running
- Open the project: `make ios-open` (from root).
- Sync new files into Xcode: `make ios-sync`.
- Connect to the backend using the Mac's **LAN IP address** (not `localhost`) for simulator testing.

## Reference Examples
- [examples/feature_reference.md](examples/feature_reference.md): Full end-to-end guide for adding a new feature module (Entity → Protocol → Repo → UseCase → ViewModel → View → DI), based on the actual Tasks implementation.
