---
name: ios
description: iOS mobile development
license: MIT
compatibility: opencode
metadata:
  audience: mobile-developers
  category: mobile-development
---

## What I do

- Develop native iOS applications using Swift and SwiftUI
- Build user interfaces with UIKit and SwiftUI
- Work with Apple frameworks (Foundation, AVFoundation, CoreData, etc.)
- Implement iOS-specific patterns and conventions
- Handle iOS device testing and provisioning
- Optimize for Apple platform guidelines
- Prepare apps for App Store submission

## When to use me

Use me when:
- Building native iOS applications
- Creating apps requiring tight Apple integration
- Need optimal performance on iOS devices
- Apps targeting iPadOS, watchOS, or tvOS
- Implementing AR/ML features with Apple frameworks
- Following Apple Human Interface Guidelines

## Key Concepts

### Swift Programming
Modern, safe, fast language for iOS development:

```swift
import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = CounterViewModel()
    
    var body: some View {
        VStack {
            Text("\(viewModel.count)")
                .font(.largeTitle)
            
            Button(action: { viewModel.increment() }) {
                Label("Increment", systemImage: "plus.circle")
            }
            .buttonStyle(.borderedProminent)
        }
    }
}

@MainActor
class CounterViewModel: ObservableObject {
    @Published var count: Int = 0
    
    func increment() {
        count += 1
    }
}
```

### UIKit vs SwiftUI
- **UIKit**: Programmatic UI, mature, full control
- **SwiftUI**: Declarative UI, less code, modern approach
- Often used together (UIHostingController embeds SwiftUI in UIKit)

### iOS Architecture Patterns
- **MVC**: Traditional Model-View-Controller
- **MVVM**: Modern with ObservableObjects
- **Coordinator**: Navigation management
- **VIPER**: Complex app architecture

### Key Frameworks
- **SwiftUI**: Declarative UI framework
- **Combine**: Reactive programming
- **Core Data**: Data persistence
- **CloudKit**: iCloud sync
- **ARKit**: Augmented reality
- **Core ML**: Machine learning
