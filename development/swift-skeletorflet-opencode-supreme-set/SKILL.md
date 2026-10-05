---
name: swift
description: Swift language skill covering SwiftUI, async/await, optionals, protocols, Codable, and SPM. Use when building Swift/iOS applications.
trigger: swift, swiftui, ios, swift async await, codable, swift protocols, swift generics, swift package manager, spm
---

## swift

### Core Concepts
- SwiftUI: @View structs compose declaratively, @State for local state, @Binding for parent-child, @StateObject/ObservableObject for model
- Struct vs Class: structs are value types (copy on write), classes are reference types (identity + inheritance)
- Optionals: T? with if let/guard let for safe unwrapping, nil coalescing (??), optional chaining
- Protocols + Generics: protocol defines interface, associatedtype for generic protocols, protocol-oriented programming

### Async/Await
- async/await: structured concurrency with Task, TaskGroup for parallel work, async let for child tasks
- Actors: protect mutable state with actor isolation, nonisolated for safe synchronous access
- MainActor: dispatch UI updates to main thread, @MainActor attribute on types or methods

### Serialization & Package Management
- Codable: Encodable + Decodable protocols, JSONEncoder/Decoder, custom CodingKeys for mapping
- SPM: Swift Package Manager, Package.swift manifest, binary/library targets, package dependencies
- Result Builders: @ViewBuilder for conditional views, @SceneBuilder for scenes, custom result builders

### Common Patterns
- property wrappers (@Published, @AppStorage, @ScaledMetric, @FocusState)
- SwiftUI lifecycle (onAppear, onChange, task modifier for async work)
- MVVM architecture with ObservableObject and @Published
