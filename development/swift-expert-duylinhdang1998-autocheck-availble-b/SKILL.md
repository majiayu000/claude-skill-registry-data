---
name: swift-expert
description: iOS development mastery with Swift from Apple. Build native iOS apps with SwiftUI, UIKit, and Apple's design principles. Expertise from the iOS Platform Team.
expert_level: 10/10
source_company: Apple (iOS Platform Team)
specialist: apple-ios-lead
related:
  - ios-architecture
---

# Swift Expert - Apple iOS Development

**Expert**: David Park (Apple iOS Platform Team, 15 years)
**Level**: 10/10 - Contributed to iOS Camera app, SwiftUI framework

## Overview

Swift and iOS development from Apple - the company that created both. Build apps that feel native, respect user privacy, and deliver Apple-quality design.

## Skill Levels

### Level 10/10 - Apple iOS Platform Engineer
- Contributed to iOS frameworks (SwiftUI, UIKit)
- Built apps used by billions (Camera, Photos, Messages)
- Designed API used by millions of developers
- Deep understanding of iOS internals

### Level 9/10 - Senior iOS Lead
- Architect complex iOS apps
- Expert in performance optimization
- Deep SwiftUI and Combine knowledge
- Mentor iOS teams

### Level 8/10 - Senior iOS Engineer
- Build production iOS apps independently
- Implement complex UI/UX
- Handle state management, networking, persistence
- Write maintainable Swift code

## Core Competencies

### 1. SwiftUI (Modern Apple UI)

**Apple's declarative UI framework**:
```swift
import SwiftUI

// Apple-quality SwiftUI app
struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()
    @Environment(\.colorScheme) var colorScheme

    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVStack(spacing: 16) {
                    ForEach(viewModel.items) { item in
                        ItemRow(item: item)
                            .onTapGesture {
                                viewModel.selectItem(item)
                            }
                    }
                }
                .padding()
            }
            .navigationTitle("Items")
            .searchable(text: $viewModel.searchText)
            .refreshable {
                await viewModel.refresh()
            }
        }
    }
}

// MVVM pattern (Apple recommended)
@MainActor
class ContentViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var searchText: String = ""

    func refresh() async {
        do {
            items = try await APIClient.shared.fetchItems()
        } catch {
            // Handle error
        }
    }
}
```

### 2. Concurrency (async/await)

**Modern Swift concurrency**:
```swift
// Apple's async/await pattern
actor ImageCache {
    private var images: [String: UIImage] = [:]

    func image(for url: URL) async throws -> UIImage {
        if let cached = images[url.absoluteString] {
            return cached
        }

        let (data, _) = try await URLSession.shared.data(from: url)
        guard let image = UIImage(data: data) else {
            throw ImageError.invalidData
        }

        images[url.absoluteString] = image
        return image
    }
}

// Usage
Task {
    do {
        let image = try await imageCache.image(for: url)
        imageView.image = image
    } catch {
        // Handle error
    }
}
```

### 3. Apple Design Principles

**Human Interface Guidelines**:
- **Clarity**: Text legible, icons precise, functionality obvious
- **Deference**: Content takes center stage, UI recedes
- **Depth**: Distinct visual layers convey hierarchy

**SF Symbols** (Apple's icon system):
```swift
Image(systemName: "heart.fill")
    .symbolRenderingMode(.multicolor)
    .font(.largeTitle)
```

## Apple Frameworks

- **SwiftUI**: Declarative UI framework
- **UIKit**: Traditional UI framework
- **Combine**: Reactive programming
- **CoreData**: Persistence
- **CloudKit**: iCloud sync
- **HealthKit**: Health data
- **ARKit**: Augmented reality
- **Core ML**: Machine learning

## Related Skills

- **[ios-architecture](../ios-architecture/SKILL.md)** - iOS app architecture

---

**Last Updated**: 2026-02-03
**Expert**: David Park (Apple, 15 years) - iOS Camera app, SwiftUI contributor
