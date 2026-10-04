---
name: apple-uikit-max
description: Review or migrate UIKit code for modern APIs, architecture, accessibility, and performance. Use for view controllers, table or collection views, Auto Layout, and programmatic UIKit; not SwiftUI-only work.
license: MIT
metadata:
  author: tgomareli
  version: "1.0"
---

Review Swift and UIKit code for correctness, modern API usage, and adherence to project conventions. Report only genuine problems — do not nitpick or invent issues.

Review process:

1. Check for deprecated API using `references/api.md`.
1. Check that views, subclassing, and composition patterns follow best practices using `references/views.md`.
1. Validate Auto Layout usage and constraint patterns using `references/layout.md`.
1. Ensure view controller lifecycle and architecture are correct using `references/controllers.md`.
1. Ensure navigation patterns are modern and maintainable using `references/navigation.md`.
1. Validate UITableView and UICollectionView usage using `references/tableview-collectionview.md`.
1. Ensure the code uses designs that are accessible and compliant with Apple's Human Interface Guidelines using `references/design.md`.
1. Validate accessibility compliance including Dynamic Type, VoiceOver, and traits using `references/accessibility.md`.
1. Ensure the code runs efficiently using `references/performance.md`.
1. Check concurrency and thread safety using `references/concurrency.md`.
1. Quick validation of Swift code using `references/swift.md`.
1. Final code hygiene check using `references/hygiene.md`.

If doing a partial review, load only the relevant reference files.


## Core Instructions

- iOS 26 exists and is the latest iOS version. Target iOS 17 or later as the minimum deployment target for new code, unless the project specifies otherwise.
- Target Swift 6.2 or later, using modern Swift concurrency.
- **Respect the project's deployment target.** Before suggesting a modern API, check its availability. If the project targets an older iOS version, recommend the best available alternative and wrap newer APIs in `if #available` checks. Reference files mark key APIs with their iOS version (e.g., "iOS 15+"). Do not suggest APIs unavailable at the project's minimum target without providing a fallback.
- As a UIKit developer, the user expects UIKit patterns. Do not suggest SwiftUI replacements unless explicitly requested.
- Do not introduce third-party frameworks without asking first.
- Break different types up into different Swift files rather than placing multiple classes, structs, or enums into a single file.
- Use a consistent project structure, with folder layout determined by app features.
- Prefer programmatic UI with Auto Layout anchors over Storyboards and XIBs for new code, unless the project already uses Interface Builder extensively.


## Output Format

Organize findings by file. For each issue:

1. State the file and relevant line(s).
2. Name the rule being violated (e.g., "Use `UIAlertController` instead of `UIAlertView`").
3. Show a brief before/after code fix.

Skip files with no issues. End with a prioritized summary of the most impactful changes to make first.

Example output:

### ProfileViewController.swift

**Line 8: Use `UIAlertController` instead of deprecated `UIAlertView`.**

```swift
// Before
let alert = UIAlertView(title: "Error", message: msg, delegate: self, cancelButtonTitle: "OK")
alert.show()

// After
let alert = UIAlertController(title: "Error", message: msg, preferredStyle: .alert)
alert.addAction(UIAlertAction(title: "OK", style: .default))
present(alert, animated: true)
```

**Line 24: Batch constraint activation with `NSLayoutConstraint.activate`.**

```swift
// Before
label.topAnchor.constraint(equalTo: view.topAnchor).isActive = true
label.leadingAnchor.constraint(equalTo: view.leadingAnchor).isActive = true

// After
NSLayoutConstraint.activate([
    label.topAnchor.constraint(equalTo: view.topAnchor),
    label.leadingAnchor.constraint(equalTo: view.leadingAnchor)
])
```

**Line 42: Set `translatesAutoresizingMaskIntoConstraints = false` before adding constraints.**

```swift
// Before
view.addSubview(label)
label.topAnchor.constraint(equalTo: view.topAnchor).isActive = true

// After
label.translatesAutoresizingMaskIntoConstraints = false
view.addSubview(label)
NSLayoutConstraint.activate([
    label.topAnchor.constraint(equalTo: view.topAnchor)
])
```

### Summary

1. **Deprecated API (high):** `UIAlertView` on line 8 must be replaced with `UIAlertController`.
2. **Layout (medium):** Individual constraint activation on line 24 should use `NSLayoutConstraint.activate`.
3. **Layout (medium):** Missing `translatesAutoresizingMaskIntoConstraints` on line 42 causes constraint conflicts.

End of example.


## References

- `references/api.md` — deprecated UIKit APIs and their modern replacements.
- `references/views.md` — UIView lifecycle, composition, subclassing, and custom drawing.
- `references/layout.md` — Auto Layout, layout anchors, UIStackView, intrinsic content size, Safe Area.
- `references/controllers.md` — UIViewController lifecycle, container controllers, avoiding Massive View Controller.
- `references/navigation.md` — navigation controllers, tab bars, coordinator pattern, modal presentation.
- `references/tableview-collectionview.md` — diffable data sources, compositional layout, cell configuration, prefetching.
- `references/design.md` — Human Interface Guidelines, UIAppearance, trait collections, Dark Mode, adaptive layouts.
- `references/accessibility.md` — VoiceOver, Dynamic Type, accessibility traits, labels, and hints.
- `references/performance.md` — off-screen rendering, layer optimization, image caching, main thread performance.
- `references/concurrency.md` — main thread safety, async/await, DispatchQueue migration, background tasks.
- `references/swift.md` — modern Swift code, Swift concurrency, Objective-C interop.
- `references/hygiene.md` — memory management, retain cycles, KVO/notification cleanup, deinit patterns.
