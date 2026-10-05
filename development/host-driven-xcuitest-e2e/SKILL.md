---
name: host-driven-xcuitest-e2e
description: 'Wire and debug launch-the-app XCUITest E2E tests in a Tuist project: a native `.uiTests` target needs its own scheme with `testAction: .targets([...])`, not `.xctestplan` membership; a name that does not collide with an SPM UITests package target; window-frame-anchored clicks for SwiftUI on macOS where `element.tap()` fails. Use when `xcodebuild test` reports no test bundles available to test, when XCUITest taps do not land on a macOS window, when adding a first E2E target, or when pinning a Simulator audit finding as a CI regression test. Manual exploration → interactive-simulator-ux-audit.'
---

# Host-Driven XCUITest E2E

"Host-driven" means the test process launches the real app and drives it through the
Simulator or a Mac window via `XCUIApplication` — distinct from unit/snapshot tests, which
never launch a process at all. This is the automated, CI-runnable sibling of
`interactive-simulator-ux-audit`: use that skill to *find* a flow bug by hand, this one to
*pin* it as a regression test.

## When to invoke

- Wiring a first host-driven E2E target in a Tuist-generated project.
- `xcodebuild test` reports "There are no test bundles available to test" for a target that
  otherwise builds cleanly.
- Driving a SwiftUI macOS (AppKit-hosted) window with XCUITest and taps aren't landing.
- Naming a new UI test target and avoiding a collision with an existing package test target.

## Scope

Assumes a Tuist-generated project; a hand-maintained `.xcodeproj` adds the same dedicated
scheme directly in Xcode's scheme editor instead of via `Project.swift`. Owns: Tuist
scheme/target wiring for native XCUITest targets, and the macOS driving mechanics below.
Does **not** own: manual/interactive Simulator exploration → `interactive-simulator-ux-audit`;
unit/snapshot test framework choice → `swift-testing-baseline`; general navigation architecture
under test → `swiftui-navigation-architecture`.

## Tuist wiring: a dedicated scheme, not a test plan

A Tuist `.uiTests` product target needs **its own scheme** with an explicit
`testAction: .targets([...])` — not membership in an existing scheme's `.xctestplan`.

```swift
// Project.swift
let e2eTarget = Target.target(
    name: "MyAppE2ETests",
    destinations: .iOS,
    product: .uiTests,
    bundleId: "com.example.myapp.e2etests",
    sources: ["E2ETests/**"],
    dependencies: [.target(name: "MyApp")]
)

let e2eScheme = Scheme.scheme(
    name: "MyApp-E2E",
    shared: true,
    buildAction: .buildAction(targets: ["MyApp", "MyAppE2ETests"]),
    testAction: .targets(["MyAppE2ETests"])   // NOT .testPlans([...])
)
```

| Situation | Do | Not |
|---|---|---|
| New native `.uiTests` target | Dedicated scheme with `testAction: .targets([...])` | Add it to an existing scheme's `.testPlans([...])` — builds the scheme but produces no `.xctest` bundle; `xcodebuild test` fails with "no test bundles available to test" |
| Naming the E2E target | `<App>E2ETests` | `<App>UITests`, if an SPM snapshot/unit target already uses that suffix (e.g. `MyAppUITests`) — Xcode name collision |
| Diagnostic output in the test runner | `print()` — lands in the `xcodebuild` log directly | Write to `/tmp` — the runner's sandbox usually blocks it |
| `-only-testing:` scope | `TestTarget[/TestClass[/TestMethod]]` (per `man xcodebuild`), only as many segments as the intended scope | — |
| UI test target lives in a different SwiftPM package than the app (cross-package) | An `.xctestplan` referencing both packages' schemes; verify empirically | Assume the dedicated-scheme rule above always wins |

A package's own SPM test targets run fine via a test plan because they're cross-linked into the
plan's buildables; a same-project native UI test target is not — the fix is the dedicated scheme
above, not a plan tweak. `TestAction`'s factory is `.targets(...)`, not `.testAction(...)`;
`TestableTarget` accepts a plain string literal target name. Give the E2E target its own build
settings (not the app's entitlement-carrying settings) so it carries no unintended app
capabilities, and keep the E2E scheme's default test action on Debug only — it should never be
part of a Release archive or the fast default test run.

## Driving SwiftUI on macOS: window-frame anchoring

On native (AppKit-hosted) macOS SwiftUI, the naive APIs don't work:

- `element.tap()` throws `point.x != INFINITY` (`NSInternalInconsistencyException`) — SwiftUI
  exposes no accessibility activation point on macOS the way it does on iOS. (Observed
  in-project; exact Xcode version unrecorded — this error text is not documented by Apple.)
- `app.coordinate(withNormalizedOffset: .zero)` resolves to `(-inf, -inf)` — the application
  element itself has no usable frame to normalize against.

**Working pattern**: element **frames** in the accessibility tree are finite and correct.
Anchor a coordinate on the main window instead of the element, and click by frame:

```swift
let window = app.windows.firstMatch

func click(_ rect: CGRect) {
    let origin = window.frame.origin
    window.coordinate(withNormalizedOffset: .zero)
        .withOffset(CGVector(dx: rect.midX - origin.x, dy: rect.midY - origin.y))
        .tap()
}

click(app.buttons["submit"].frame)
```

Other macOS-driving specifics:

- `hittable` is **not** a valid NSPredicate key in an `XCUIElementQuery` predicate
  (`XCTElementQueryInvalidPredicate` at runtime; observed in-project, exact Xcode version
  unrecorded) — `isHittable` only works as a Swift-side property check, never inside a
  predicate string.
- When dumping diagnostic state (e.g. `app.debugDescription`) via `print()` per the table
  above, don't pipe `xcodebuild` through `tail` or another filter that can drop buffered
  output before the dump is flushed.
- Tapping the *same* element across multiple steps where its accessibility label mutates
  between taps (e.g. a cell whose label changes once filled): capture `element.frame` **once**
  and convert it to an app-relative coordinate up front, rather than re-querying the element
  by its now-stale label on each subsequent tap.
- Test classes that touch `XCUIElement` APIs must be `@MainActor` under Swift 6 strict
  concurrency — those APIs are main-actor-isolated.

## Locale-stable queries

If the app ships more than one locale, query by a **stable accessibility identifier** set in
code (`accessibilityIdentifier("checkout.confirmation.title")`) rather than by visible label text —
translated strings break a hardcoded English-label query the moment a non-English locale runs
the same test. Reserve literal label matching for elements whose text is guaranteed
locale-invariant by design (e.g. digits, or an identifier deliberately not localized).

## Deterministic entry points for hard-to-reach states

A flow that's expensive or unreliable to reach through pure UI interaction (a multi-step win
condition, a rare error state) benefits from a debug-only, launch-argument-gated seam that
deterministically lands the app one step from the state under test, so the test asserts the
*transition*, not the app's own internal logic reproduced via blind taps. Keep this seam
compiled out of Release builds.

## Rationale

A host-driven E2E test is the only automated check that proves the full launch → navigate →
interact → assert path works end-to-end, including scheme/target wiring, entitlements, and
real accessibility tree resolution — none of which a unit or snapshot test exercises. It's
slower and more environment-sensitive than either, which is why it complements rather than
replaces them (see the test pyramid in `swift-testing-baseline`).

## Deviation considerations

- **Cross-package test target** (the UI test target must live in a different SwiftPM package
  than the app target): a dedicated scheme may not resolve the cross-package build graph
  cleanly — an `.xctestplan` referencing both packages' schemes can be the more reliable
  choice there; verify empirically rather than assuming the dedicated-scheme rule always wins.
- **iOS-only app with no macOS target**: skip the window-frame-anchoring section entirely;
  standard `element.tap()` works on iOS.

## Common Mistakes

1. **Adding a native `.uiTests` target to an existing test plan** instead of giving it a
   dedicated scheme — silently produces zero test bundles.
2. **Naming a new E2E target `<App>UITests`** when an SPM snapshot/unit target already uses
   that name — Xcode target collision.
3. **Calling `element.tap()` on macOS** — throws `point.x != INFINITY`; use window-frame
   anchoring instead.
4. **Putting `hittable` in an NSPredicate string** — runtime `XCTElementQueryInvalidPredicate`; use `isHittable` in Swift code.
5. **Re-querying an element by a label that mutates during the test** — capture the frame once, before the label changes.
6. **Matching on visible label text in a localized app** — breaks under any non-English locale; query by accessibility identifier instead.

## Review Checklist

- [ ] The E2E target has its own Tuist scheme with `testAction: .targets([...])`, not a `.xctestplan` membership.
- [ ] The E2E target's name doesn't collide with any SPM `<Target>UITests` package target.
- [ ] The E2E scheme is Debug-only and excluded from the Release archive action.
- [ ] macOS taps go through window-frame anchoring, not `element.tap()` / `app.coordinate(...)`.
- [ ] No `hittable` inside an NSPredicate string.
- [ ] Locale-sensitive elements are queried by accessibility identifier, not label text.
- [ ] `-only-testing:` identifiers follow `TestTarget[/TestClass[/TestMethod]]` — only as many segments as the intended scope.
- [ ] Any debug-only entry-point seam is compiled out of Release builds.

## Related skills

- `interactive-simulator-ux-audit` — the manual/exploratory sibling; find the bug there, pin it here.
- `swift-testing-baseline` — where E2E sits in the overall test pyramid.
- `swiftui-navigation-architecture` — the navigation shape these tests typically assert against.
- `swiftpm-modularization` — package/target layout that affects whether a dedicated scheme or a test plan is the right wiring.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
