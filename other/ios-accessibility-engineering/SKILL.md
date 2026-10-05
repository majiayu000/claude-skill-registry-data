---
name: ios-accessibility-engineering
description: Implement and audit VoiceOver (`accessibilityLabel` / `Value` / `Hint`, traits, `accessibilityElement(children:)`, `AccessibilityNotification`), Dynamic Type (text styles, caps, AX5), 44pt touch targets, and Reduce Motion / Transparency for SwiftUI and UIKit, with a WCAG 2.2 mapping. Use when asked to make a screen accessible, when VoiceOver reads the wrong thing, for a pre-submission a11y audit or Accessibility Inspector pass, when wiring `performAccessibilityAudit()` as a CI gate, or an accessibility App Review rejection. Not Rotor / `AccessibilityFocusState` depth; live Simulator driving → interactive-simulator-ux-audit.
---

# iOS Accessibility Engineering

## When to invoke

- Adding accessibility to a new or changed user-facing View (labels, Dynamic Type, hit targets).
- Running a pre-submission accessibility audit against App Store Review guidelines.
- User says "make this accessible", "check a11y", "VoiceOver doesn't read this", or "does this pass WCAG".
- Reviewing a PR for accessibility regressions.

## VoiceOver: labelling and semantics

**Labels, values, and hints** are three distinct channels:

- `.accessibilityLabel("Done")` — the noun identifying the element. Keep it short; VoiceOver reads it first.
- `.accessibilityValue("3 of 9")` — the current state or quantity. Changes without re-reading the label.
- `.accessibilityHint("Double-tap to submit")` — what happens on activation. Users can turn hints off; never put essential info here.

In UIKit, set `accessibilityLabel`, `accessibilityValue`, and `accessibilityHint` on any `UIView`. In SwiftUI, use the `.accessibilityLabel(_:)`, `.accessibilityValue(_:)`, and `.accessibilityHint(_:)` modifiers.

**Traits** communicate the element's role and state. Common SwiftUI traits:

```swift
.accessibilityAddTraits(.isButton)     // tappable action
.accessibilityAddTraits(.isHeader)     // section heading — VoiceOver lets users jump by heading
.accessibilityAddTraits(.updatesFrequently)  // live score, timer — suppresses constant interruptions
.accessibilityAddTraits(.isSelected)   // toggle / tab selection state
```

**Grouping** — combine several sub-views into one focusable element so VoiceOver reads it as a single sentence:

```swift
HStack { thumbnail; title; subtitle }
    .accessibilityElement(children: .combine)
```

Use `.accessibilityElement(children: .ignore)` when the children are redundant and you supply a custom label on the container. Use `.accessibilityElement(children: .contain)` to keep individual children focusable inside a group (e.g. a toolbar).

**Hiding decorative content:**

```swift
Image("confetti-background")
    .accessibilityHidden(true)   // purely decorative; skip in VoiceOver rotor
```

Meaningful images need a label: `Image("trophy").accessibilityLabel("Achievement unlocked")`.

**Announcing dynamic changes** — when content updates in place without a navigation event:

```swift
AccessibilityNotification.Announcement("Level complete").post()
// or for a layout change (the initializer takes the element unlabeled):
AccessibilityNotification.LayoutChanged(focusTarget).post()
// or for a screen change (modal, full replacement):
AccessibilityNotification.ScreenChanged(focusTarget).post()
```

In UIKit: `UIAccessibility.post(notification: .announcement, argument: "Level complete")`.

## Dynamic Type

- Use `Font.body`, `.headline`, `.caption` etc. (text styles), or `UIFont.preferredFont(forTextStyle:)` in UIKit. Never hard-code `Font.system(size: 17)` without a text style.
- SwiftUI text styles scale automatically. If a control must cap scaling (compact digit grids, icon labels), apply `.dynamicTypeSize(...DynamicTypeSize.xLarge)` — this clamps only sizes above `.xLarge`; default `.large` stays byte-identical and snapshot baselines are unaffected.
- Test at AX5 (`accessibility-extra-extra-extra-large`) in Simulator: `xcrun simctl ui <udid> content_size accessibility-extra-extra-extra-large`.
- **`minimumScaleFactor` is width-only** — it won't rescue a glyph that overflows *vertically* (a tall digit clips blank in a short cell); cap the size instead. In `fullScreenCover` / `sheet` modals `@Environment(\.dynamicTypeSize)` can read stale — use geometry-driven layout (`ViewThatFits`). See `swiftui-interaction-footguns` for both traps in full.
- Avoid fixed `frame(height:)` on text containers; prefer `frame(minHeight:)` with unlimited vertical growth.

## Touch targets

- Apple HIG: **44 × 44 pt** is the iOS default control size (Buttons: a hit region of "at least 44x44 pt" as a general rule); the HIG Accessibility table's minimum is 28 × 28 pt. Ship 44. A visually small button (e.g. a 20pt icon) passes if its hit region is padded to 44pt.
- `.contentShape(Rectangle())` enlarges the hit region for `.buttonStyle(.plain)` containers or custom `onTapGesture` views where Spacers don't automatically expand the hit area.
- Voice Control and Switch Control rely on `accessibilityLabel` to identify targets by name; if two same-named buttons exist on screen, add `.accessibilityInputLabels(["Submit order", "Submit"])` to disambiguate.

## Motion, transparency, and contrast

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion
// Skip or replace animations when true:
withAnimation(reduceMotion ? nil : .easeInOut) { state.toggle() }
```

- `\.accessibilityReduceTransparency` — remove blur / frosted-glass effects when true; use an opaque fill instead. Apple does not guarantee that SwiftUI `.background(.ultraThinMaterial)` automatically drops its blur when Reduce Transparency is on — the conservative approach is to branch on `\.accessibilityReduceTransparency` yourself and substitute a solid background rather than rely on the material.
- `\.accessibilityDifferentiateWithoutColor` — never rely on color alone to convey state; add an icon or label.
- `\.colorSchemeContrast` (`.increased`) — if you draw custom backgrounds, check this and raise contrast when set.

## Verification and testing

**Accessibility Inspector** (Xcode → Open Developer Tool → Accessibility Inspector): point the inspector at your app in Simulator, run the automated audit (the triangle icon), and fix every reported issue before submission. It surfaces missing labels, low-contrast text, small touch targets, and missing traits.

**Snapshot tests do not verify Dynamic Type or VoiceOver.** An `NSHostingView` in a headless test process has no live AX client; `accessibilityLabel` / `accessibilityChildren` traversal returns empty trees. Injecting `DynamicTypeSize.accessibility3` into an `NSHostingView` bypasses the modal env-propagation path, giving a false pass. Reliable verification requires a booted simulator with idb or `xcrun simctl`:

```bash
# Set content size to AX5 and screenshot
xcrun simctl ui <udid> content_size accessibility-extra-extra-extra-large
idb screenshot --udid <udid> after-ax5.png
# Tap through the UI with VoiceOver via idb ui tap / idb ui describe-all
```

**CI a11y gate**: in XCUITest, call `try app.performAccessibilityAudit()` (iOS 17 / macOS 14 / Xcode 15+; narrow with `for:` to specific audit types such as `.dynamicType`, `.contrast`, `.hitRegion`) to fail CI on accessibility violations — this is Apple's own runtime audit gate. Supplement with `cvs-health/ios-swiftui-accessibility-techniques`'s `a11y-check`, a **static scanner** (not a runtime audit runner), as a complementary lint-layer check. Treat both as complements to, not replacements for, manual Accessibility Inspector review. Xcode 27 / iOS 27 runtime, above this catalog's 26 floor: [`XCUIVoiceOverService`](https://developer.apple.com/documentation/xcuiautomation/xcuivoiceoverservice) (via `XCUIDevice`'s `voiceOverService`) drives VoiceOver from UI tests to validate focus, spoken output, and navigation.

## WCAG 2.2 mapping for App Review

Ship to 44×44pt (HIG iOS default control size); 24px AA is the floor, not the target.

| WCAG criterion | What it requires | How it surfaces in iOS |
|---|---|---|
| 1.1.1 Non-text content | Meaningful images have text alternatives | `accessibilityLabel` on `Image` |
| 1.4.3 Contrast (minimum) | ≥ 4.5:1 for normal text, 3:1 for large text | Check in Accessibility Inspector |
| 1.4.4 Resize text | Text reflows up to 200% without loss of content | Dynamic Type + `ViewThatFits` |
| 2.5.8 Target size (Minimum) — **AA** | Interactive targets ≥ 24×24 CSS px (WCAG 2.2 new AA criterion) | `.contentShape` + padding; the **AA conformance gate** |
| 2.5.5 Target size (Enhanced) — AAA | Interactive targets ≥ 44×44 CSS px (≈44pt on 1× devices) | Apple HIG iOS default control size (the HIG minimum is 28×28 pt); stronger than AA — aim for this |

App Review does not formally audit against WCAG, but the Human Interface Guidelines cite these thresholds and reviewers reject apps that are obviously unusable with VoiceOver or at accessibility text sizes.

## Verification checklist

- All interactive controls have an `accessibilityLabel`; decorative images have `accessibilityHidden(true)`.
- Dynamic type tested at AX5 on a booted simulator — not only at default `.large`.
- No fixed `frame(height:)` on text containers; `minimumScaleFactor` is not used as a substitute for layout flexibility.
- Touch targets ≥ 44pt; `.contentShape` applied wherever Spacers or padding would otherwise shrink the hit region.
- `AccessibilityNotification` posted for in-place content changes.
- `accessibilityReduceMotion` checked before all non-trivial animations.
- Accessibility Inspector automated audit passes with zero errors.
- VoiceOver reading order verified manually (not inferred from visual order alone).

## Related skills

- `swiftui-interaction-footguns`: Dynamic Type / modal env footguns and the `minimumScaleFactor` pitfall in detail.
- `swift-testing-baseline`: headless AX-tree limitation and why sim verification is the reliable gate.
- `interactive-simulator-ux-audit`: the live-simulator drive/tap/screenshot loop this skill's verification steps rely on.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.

## External references

- [`dadederk/iOS-Accessibility-Agent-Skill`](https://github.com/dadederk/iOS-Accessibility-Agent-Skill)
  (Daniel Devesa Derksen-Staats, MIT) — a complementary, high-authority a11y skill. It goes
  deeper on **Large Content Viewer** (`UILargeContentViewerItem`), **`accessibilityRotor` /
  `accessibilityRepresentation` / `AccessibilityFocusState`**, **Full Keyboard Access**, and
  VoiceOver **custom actions** — areas this skill keeps brief. This skill's strength is the
  runtime-verification pitfalls (the `minimumScaleFactor` vertical-clip trap, headless-AX-tree
  false passes, idb/simctl sim-verify, WCAG 2.2 mapping). Use both.
