---
name: swiftui-development
description: Master SwiftUI - Declarative UI, state management, animations, modern iOS development
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 03-swiftui-development
bond_type: PRIMARY_BOND
last_updated: "2024-12"
---

# SwiftUI Development Skill

> Build modern, declarative iOS interfaces with SwiftUI

## Learning Objectives

By completing this skill, you will:
- Create declarative UIs with SwiftUI views
- Master state management (@State, @Binding, @Observable)
- Implement complex navigation with NavigationStack
- Create fluid animations and transitions
- Build production-ready SwiftUI applications

## Prerequisites

| Requirement | Level |
|-------------|-------|
| iOS Fundamentals | Completed |
| Swift | Intermediate |
| Functional programming concepts | Basic |

## Curriculum

### Module 1: SwiftUI Fundamentals (4 hours)

**Topics:**
- View protocol and body
- ViewBuilder and composition
- Modifiers and their order
- @ViewBuilder for custom containers
- Environment and preferences

**Code Examples:**
```swift
// Basic view composition
struct ProfileView: View {
    let user: User

    var body: some View {
        VStack(spacing: 16) {
            ProfileImage(url: user.avatarURL)

            Text(user.name)
                .font(.title)
                .fontWeight(.bold)

            Text(user.bio)
                .font(.body)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
    }
}

// Custom container with ViewBuilder
struct Card<Content: View>: View {
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        content
            .padding()
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 4)
    }
}
```

**Checkpoint:** Build profile card component

---

### Module 2: State Management (6 hours)

**Topics:**
- @State for local state
- @Binding for two-way binding
- @StateObject vs @ObservedObject
- @EnvironmentObject for shared state
- @Observable (iOS 17+)
- Combine integration

**State Hierarchy:**
```
@State → Local, value type
@Binding → Pass to child, two-way
@StateObject → Own the object, create once
@ObservedObject → Don't own, receive from parent
@EnvironmentObject → Shared globally
@Observable → Modern replacement (iOS 17+)
```

**Modern Approach (iOS 17+):**
```swift
@Observable
final class UserViewModel {
    var user: User?
    var isLoading = false
    var error: Error?

    private let service: UserServiceProtocol

    init(service: UserServiceProtocol = UserService()) {
        self.service = service
    }

    func loadUser() async {
        isLoading = true
        defer { isLoading = false }

        do {
            user = try await service.fetchCurrentUser()
        } catch {
            self.error = error
        }
    }
}

struct UserView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
            } else if let user = viewModel.user {
                UserContent(user: user)
            }
        }
        .task {
            await viewModel.loadUser()
        }
    }
}
```

**Checkpoint:** Build stateful form with validation

---

### Module 3: Navigation (5 hours)

**Topics:**
- NavigationStack (iOS 16+)
- NavigationPath for programmatic navigation
- NavigationSplitView for iPad
- Sheet, fullScreenCover, alert
- Deep linking with URL schemes

**Navigation Stack:**
```swift
enum Route: Hashable {
    case profile(userId: String)
    case settings
    case detail(item: Item)
}

struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeView(navigate: navigate)
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .profile(let userId):
                        ProfileView(userId: userId)
                    case .settings:
                        SettingsView()
                    case .detail(let item):
                        DetailView(item: item)
                    }
                }
        }
    }

    private func navigate(to route: Route) {
        path.append(route)
    }

    private func popToRoot() {
        path.removeLast(path.count)
    }
}
```

**Checkpoint:** Build multi-screen navigation flow

---

### Module 4: Lists & Grids (4 hours)

**Topics:**
- List and ForEach
- LazyVStack and LazyVGrid
- Swipe actions and context menus
- Searchable modifier
- Pull-to-refresh

**Grid Layout:**
```swift
struct PhotoGrid: View {
    let photos: [Photo]

    private let columns = [
        GridItem(.adaptive(minimum: 100, maximum: 150), spacing: 8)
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 8) {
                ForEach(photos) { photo in
                    AsyncImage(url: photo.thumbnailURL) { phase in
                        switch phase {
                        case .empty:
                            Rectangle()
                                .fill(.quaternary)
                        case .success(let image):
                            image
                                .resizable()
                                .scaledToFill()
                        case .failure:
                            Image(systemName: "photo")
                        @unknown default:
                            EmptyView()
                        }
                    }
                    .frame(height: 100)
                    .clipShape(RoundedRectangle(cornerRadius: 8))
                }
            }
            .padding()
        }
    }
}
```

**Checkpoint:** Build searchable photo grid

---

### Module 5: Animations (4 hours)

**Topics:**
- Implicit animations (.animation)
- Explicit animations (withAnimation)
- Transitions
- matchedGeometryEffect
- Phase animator (iOS 17+)

**Animation Examples:**
```swift
// Implicit animation
struct ExpandableCard: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Text("Title")
                .font(.headline)

            if isExpanded {
                Text("Detailed content here...")
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(.background)
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .onTapGesture {
            withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
                isExpanded.toggle()
            }
        }
    }
}

// Matched geometry effect
struct CardTransition: View {
    @Namespace private var animation
    @State private var selectedCard: Card?

    var body: some View {
        ZStack {
            if let card = selectedCard {
                DetailView(card: card)
                    .matchedGeometryEffect(id: card.id, in: animation)
                    .onTapGesture { selectedCard = nil }
            } else {
                LazyVGrid(columns: columns) {
                    ForEach(cards) { card in
                        CardView(card: card)
                            .matchedGeometryEffect(id: card.id, in: animation)
                            .onTapGesture { selectedCard = card }
                    }
                }
            }
        }
        .animation(.spring(response: 0.5), value: selectedCard)
    }
}
```

**Checkpoint:** Create hero animation transition

---

### Module 6: Custom Modifiers & Styles (3 hours)

**Topics:**
- ViewModifier protocol
- ButtonStyle, LabelStyle
- Custom environment values
- Preference keys
- View extensions

**Custom Modifier:**
```swift
struct CardStyle: ViewModifier {
    let isHighlighted: Bool

    func body(content: Content) -> some View {
        content
            .padding()
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(
                color: isHighlighted ? .accentColor.opacity(0.3) : .black.opacity(0.1),
                radius: isHighlighted ? 8 : 4
            )
            .overlay {
                if isHighlighted {
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(.accent, lineWidth: 2)
                }
            }
    }
}

extension View {
    func cardStyle(isHighlighted: Bool = false) -> some View {
        modifier(CardStyle(isHighlighted: isHighlighted))
    }
}

// Usage
Text("Content")
    .cardStyle(isHighlighted: true)
```

**Checkpoint:** Build custom button style library

---

## Assessment Criteria

| Criteria | Weight |
|----------|--------|
| View composition | 25% |
| State management | 30% |
| Navigation | 20% |
| Animation quality | 15% |
| Code organization | 10% |

## Common Mistakes

1. **@StateObject vs @ObservedObject** → Use @StateObject for creation
2. **ForEach without id** → Always use identifiable items
3. **Nested NavigationStack** → Only one per hierarchy
4. **Heavy body computation** → Extract to computed properties
5. **Missing .animation value** → Always specify animation trigger

## Debugging Tips

```swift
// Debug view updates
var body: some View {
    let _ = Self._printChanges()
    // Your view...
}

// Debug layout
view.border(.red) // Visual bounds
```

## Resources

### Official Documentation
- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

## Skill Validation

Complete these projects:
1. **Component Library**: 10 reusable SwiftUI components
2. **Stateful App**: Todo app with persistence
3. **Navigation Demo**: Deep-linkable multi-screen app
4. **Animation Showcase**: Hero transitions and gestures
