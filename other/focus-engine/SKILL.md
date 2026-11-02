---
name: focus-engine
description: "Implements keyboard, directional, and scene-level focus behavior across SwiftUI and UIKit. Use when managing @FocusState, defaultFocus, focused values, focusable interactions, focus sections, tvOS geometric focus model and Siri Remote navigation, watchOS Digital Crown focus, visionOS gaze/hover and RealityKit InputTargetComponent, macOS key view loop and Full Keyboard Access, focus restoration after presentation changes, custom focus routing with UIFocusGuide, or debugging focus with UIFocusDebugger."
---

# Focus Engine

Focus behavior for SwiftUI and UIKit apps targeting iOS 26+, iPadOS, macOS, and tvOS. Covers keyboard focus, directional focus, scene-focused values, focus restoration, and UIKit focus guides. `focusSection()` guidance in this skill applies to macOS and tvOS. Accessibility-specific focus for VoiceOver and Switch Control lives in the `ios-accessibility` skill.

## Contents

- [SwiftUI FocusState](#swiftui-focusstate)
- [Default Focus](#default-focus)
- [Focused Values and Scene Values](#focused-values-and-scene-values)
- [Focusable Interactions](#focusable-interactions)
- [Focus Sections](#focus-sections)
- [Focus Restoration](#focus-restoration)
- [UIKit Focus Guides](#uikit-focus-guides)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## SwiftUI FocusState

Use `@FocusState` to read and write focus placement inside a scene. Use `Bool` for a single target or an optional `Hashable` enum for multiple targets.

```swift
struct LoginView: View {
    enum Field: Hashable { case email, password }

    @State private var email = ""
    @State private var password = ""
    @FocusState private var focusedField: Field?

    var body: some View {
        Form {
            TextField("Email", text: $email)
                .focused($focusedField, equals: .email)

            SecureField("Password", text: $password)
                .focused($focusedField, equals: .password)
        }
        .onAppear { focusedField = .email }
        .onSubmit {
            switch focusedField {
            case .email: focusedField = .password
            case .password, nil: submit()
            }
        }
    }
}
```

Keep focus state local to the view that owns the focusable controls.

## Default Focus

Use `.defaultFocus` to set the preferred initial focus region or control when a view appears or when focus is reassigned automatically.

```swift
struct SidebarView: View {
    enum Target: Hashable { case library, settings }
    @FocusState private var focusedTarget: Target?

    var body: some View {
        VStack {
            Button("Library") { }
                .focused($focusedTarget, equals: .library)

            Button("Settings") { }
                .focused($focusedTarget, equals: .settings)
        }
        .defaultFocus($focusedTarget, .library)
    }
}
```

Prefer one clear default destination per screen or focus region.

## Focused Values and Scene Values

Use focused values to expose state from the currently focused view. Use scene-focused values when commands or scene-wide UI should keep access to the value even after focus moves within that scene.

```swift
struct SelectedRecipeKey: FocusedValueKey {
    typealias Value = Binding<Recipe>
}

extension FocusedValues {
    var selectedRecipe: Binding<Recipe>? {
        get { self[SelectedRecipeKey.self] }
        set { self[SelectedRecipeKey.self] = newValue }
    }
}

struct RecipeDetailView: View {
    @Binding var recipe: Recipe

    var body: some View {
        Text(recipe.title)
            .focusedSceneValue(\.selectedRecipe, $recipe)
    }
}
```

Use this pattern for menus, commands, and toolbars that need to act on the focused scene's current content.

## Focusable Interactions

Use `.focusable(_:interactions:)` on custom SwiftUI views that should participate in keyboard or directional focus.

```swift
struct SelectableCard: View {
    let title: String
    let action: () -> Void
    @FocusState private var isFocused: Bool

    var body: some View {
        Button(action: action) {
            RoundedRectangle(cornerRadius: 12)
                .fill(isFocused ? Color.accentColor.opacity(0.15) : .clear)
                .overlay { Text(title) }
        }
        .buttonStyle(.plain)
        .focusable(interactions: .activate)
        .focused($isFocused)
    }
}
```

Use `.activate` for button-like controls. Reserve broader interactions for views that genuinely need editing or multiple focus-driven behaviors.

## Focus Sections

Use `focusSection()` on macOS 13+ and tvOS 15+ to guide directional movement across groups of focusable descendants in uneven layouts.

```swift
struct TVLibraryView: View {
    var body: some View {
        HStack {
            VStack {
                Button("Recent") { }
                Button("Favorites") { }
                Button("Downloaded") { }
            }
            .focusSection()

            VStack {
                Button("Featured") { }
                Button("Top Picks") { }
                Button("Continue Watching") { }
            }
            .focusSection()
        }
    }
}
```

Use focus sections on macOS and tvOS when default left/right or up/down movement skips the intended group.

## Focus Restoration

After dismissing a sheet, popover, or transient overlay, return focus to a stable trigger or logical next target.

```swift
struct FiltersView: View {
    @State private var showSheet = false
    @FocusState private var isFilterButtonFocused: Bool

    var body: some View {
        Button("Filters") { showSheet = true }
            .focused($isFilterButtonFocused)
            .sheet(isPresented: $showSheet) {
                FilterEditor()
                    .onDisappear {
                        Task { @MainActor in
                            isFilterButtonFocused = true
                        }
                    }
            }
    }
}
```

Restore focus intentionally whenever presentation changes would otherwise leave users disoriented.

## UIKit Focus Guides

Use `UIFocusGuide` when UIKit or tvOS layouts need custom routing across empty space or awkward geometry.

```swift
final class DashboardViewController: UIViewController {
    private let focusGuide = UIFocusGuide()
    @IBOutlet private weak var leadingButton: UIButton!
    @IBOutlet private weak var trailingButton: UIButton!

    override func viewDidLoad() {
        super.viewDidLoad()

        view.addLayoutGuide(focusGuide)
        focusGuide.preferredFocusEnvironments = [trailingButton]

        NSLayoutConstraint.activate([
            focusGuide.leadingAnchor.constraint(equalTo: leadingButton.trailingAnchor),
            focusGuide.trailingAnchor.constraint(equalTo: trailingButton.leadingAnchor),
            focusGuide.topAnchor.constraint(equalTo: leadingButton.topAnchor),
            focusGuide.bottomAnchor.constraint(equalTo: leadingButton.bottomAnchor)
        ])
    }
}
```

`UIFocusGuide` is invisible and not a view. Use it to redirect focus without adding decorative UI.

## Common Mistakes

1. Mixing accessibility focus and keyboard or directional focus in the same mental model.
2. Storing `@FocusState` in shared models instead of the owning view.
3. Setting multiple competing default focus targets on one screen.
4. Using `.focusable()` on decorative views.
5. Forgetting focus restoration after sheets, popovers, or custom overlays.
6. Reaching for `UIFocusGuide` before trying `focusSection()` on macOS or tvOS, or better layout grouping in SwiftUI.
7. Using gesture handlers for primary actions on custom focusable controls instead of a semantic `Button` when possible.

## Review Checklist

- [ ] `@FocusState` is local to the view that owns the controls
- [ ] Initial focus target is explicit when the screen needs one
- [ ] Focus movement between fields or groups is deterministic
- [ ] `focusedSceneValue` or related focused-value APIs are used when commands need current scene state
- [ ] Custom controls opt into focus only when they are truly interactive
- [ ] `focusSection()` is used for uneven directional layouts on macOS or tvOS before dropping to UIKit
- [ ] Focus returns to a stable element after temporary presentations dismiss
- [ ] `UIFocusGuide` geometry and preferred destinations match the intended route
- [ ] Accessibility focus concerns are handled in `ios-accessibility`, not mixed into keyboard-directional focus logic

## References

- Detailed patterns: [references/focus-patterns.md](references/focus-patterns.md)
- Multi-platform focus (tvOS, watchOS, visionOS, macOS): [references/multi-platform-focus.md](references/multi-platform-focus.md)
- Focus debugging and anti-patterns: [references/focus-debugging.md](references/focus-debugging.md)
