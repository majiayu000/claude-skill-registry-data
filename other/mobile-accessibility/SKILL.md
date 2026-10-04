---
name: mobile-accessibility
category: mobile
description: Use when building or changing any interactive mobile UI - VoiceOver/TalkBack labels, grouping, headings, focus order, Dynamic Type/font scale, reduce motion, contrast, and the automated check for each stack.
source: ehmo/platform-design-skills (MIT), twostraws/SwiftUI-Agent-Skill (MIT), skydoves/android-testing-skills (Apache-2.0), adapted
---
# Mobile Accessibility

## Overview

VoiceOver and TalkBack are not an edge case — they're how a meaningful share of your users, and every store review, go through the screen. Every control that is interactive needs a label a screen reader can speak; every screen needs a sane reading and focus order; text needs to scale.

**Core principle:** build it accessible the first time — retrofitting labels after the fact means re-testing the whole screen.

## Per-stack API table

| Concern | Flutter | Compose | SwiftUI |
|---|---|---|---|
| Label | `Semantics(label:)` / `tooltip` / `semanticLabel` on `Image`/`Icon` | `contentDescription` (`null` = decorative) | `accessibilityLabel` / `Button("…", systemImage:)` |
| Grouping | `MergeSemantics` | `Modifier.semantics(mergeDescendants = true)` | `.accessibilityElement(children: .combine)` |
| Heading | `Semantics(header: true)` | `semantics { heading() }` | `.accessibilityAddTraits(.isHeader)` |
| Hidden/decorative | `ExcludeSemantics` | `Modifier.clearAndSetSemantics {}` | `Image(decorative:)` |
| Custom action | `CustomSemanticsAction` | `Modifier.semantics { customActions = … }` | `.accessibilityAction(named:)` |
| Live region | `Semantics(liveRegion: true)` | `Modifier.semantics { liveRegion = … }` | `.accessibilityAddTraits(.updatesFrequently)` |

Rules that apply everywhere:
- Every interactive control (button, icon button, tappable row) has a non-empty, human-readable label — never a bare icon with no text or label.
- Don't rely on a swipe-only gesture for something achievable another way; add a custom action or a visible control alongside it.
- Group a composite control (e.g. an icon + label that act as one tap target) with the merge/combine API so a screen reader announces it once, not as separate stops.
- Headings get the heading trait so screen-reader users can jump by section.
- `@ScaledMetric` (SwiftUI) / theme text styles (Flutter, Compose) everywhere text appears — never a hardcoded point/sp size that ignores the system font-scale setting.
- Respect reduce-motion: `MediaQuery.disableAnimationsOf(context)` (Flutter), `LocalAccessibilityManager`/animation duration checks (Compose), `@Environment(\.accessibilityReduceMotion)` (SwiftUI) — skip or shorten a decorative animation, never a functional state change.
- Contrast: body text ≥4.5:1, large text ≥3:1 against its background in both light and dark — check this when picking theme token values, not per-screen.

## Automated checks

- **Flutter (verified):** `meetsGuideline` — `androidTapTargetGuideline` (48×48), `iOSTapTargetGuideline` (44×44), `labeledTapTargetGuideline`, `textContrastGuideline`. Run all four against any new interactive widget's test (see `mobile-visual-self-review`'s worked example).
- **Compose:** `rule.enableAccessibilityChecks()` (`ui-test-junit4-accessibility`) runs the Accessibility Test Framework before every UI-mutating test action. It requires an API 34+ device/emulator — on Robolectric it only warns, so a Robolectric-only pass is inconclusive and must be said so in the closing message. `tryPerformAccessibilityChecks()` for a manual, one-off gate inside a test.
- **XCUITest:** `try app.performAccessibilityAudit()` (Xcode 15+) inside a UI test — fails the test on a real finding (e.g. insufficient contrast, missing label).

## The device proxy

When you have a device but not a screen reader to drive, `mobile_read_ui {filter: "clickable=\"true\""}` is your proxy for "what would TalkBack/VoiceOver say here": every line needs a non-empty `text` or `content-desc`, and the bounds must meet the tap-target floor. This is not a substitute for the automated checks above — it catches missing labels, not contrast or reading order.

## Worked Example

```
❌ IconButton(icon: Icon(Icons.delete), onPressed: delete)                 // no label at all
✅ IconButton(
     icon: const Icon(Icons.delete),
     tooltip: 'Delete task',                                               // spoken by TalkBack/VoiceOver
     onPressed: delete,
   )
```

```swift
// ❌ Button(action: delete) { Image(systemName: "trash") }                 // icon-only, silent
// ✅
Button("Delete task", systemImage: "trash", action: delete)
    .labelStyle(.iconOnly)                                                 // visually icon-only, still spoken
```

## Common Mistakes

- An icon-only button with no `tooltip`/`contentDescription`/`accessibilityLabel`.
- Hardcoding a font size instead of a scalable text style, so Dynamic Type/font-scale does nothing.
- Treating a Robolectric-only `enableAccessibilityChecks()` pass as a verified result.
- A decorative animation that ignores the reduce-motion setting.
- A composite row (icon + title + chevron) left as three separate screen-reader stops instead of merged into one.

## Red Flags

- `Icon`/`Image` used as the entire content of a tappable control with no label anywhere in the diff.
- A contrast value picked without checking it against both light and dark theme backgrounds.
- A swipe-to-reveal action with no equivalent reachable another way.
