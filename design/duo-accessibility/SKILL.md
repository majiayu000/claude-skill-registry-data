---
name: duo-accessibility
description: "Makes iPhone Duo apps work with VoiceOver, Dynamic Type, Reduce Motion, Increase Contrast, hardware keyboards, Switch Control and Voice Control on both displays. Use it when VoiceOver reads two panes row by row or loses its place after the phone folds or unfolds, when text truncates or clips on the 5.4-inch outer display at large text sizes, when a hinge effect or resize animation ignores Reduce Motion, when colours fail contrast, when keyboard shortcuts or focus don't work, or when you add accessibility labels, identifiers or audits. Covers accessibilityElement(children: .contain), accessibilitySortPriority, AccessibilityFocusState with a delayed move after a size-class change, AnyLayout and ViewThatFits reflow with isAccessibilitySize, ScaledMetric, accessibilityReduceMotion with onHingeChange, colorSchemeContrast, keyboardShortcut, accessibilityInputLabels, modifiers before .position, Accessibility Inspector, performAccessibilityAudit and XCUIDevice voiceOverService UI tests on the iPhone Duo simulator."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-accessibility

iPhone Duo changes shape while people use it. One pane becomes two, a row of text gets about twice the width, the window jumps to another display. Accessibility settings don't change with it: the same VoiceOver user, text size and Reduce Motion setting meet every layout. This skill makes each layout work for them.

Load neighbours for depth: `duo-design-system` (type scale, colour tokens, contrast checks), `duo-transitions` (animating the resize), `duo-postures` (hinge effects), `duo-ergonomics` (44 pt targets), `duo-testing` (UI test setup), `duo-shared-screen` (two people, one screen).

Labels: *measured* means we ran it in a probe app with UI tests on the shared iPhone Duo simulator (Xcode 27.1, iOS 27.1, 18 October 2026). *Unverified* means we could not confirm it. Everything else links to Apple. Details: [references/evidence.md](references/evidence.md).

## Rules

1. Make each pane a VoiceOver container. Two panes side by side are read row by row otherwise.
2. Keep the pane order stable in every pose. Change it only with `accessibilitySortPriority`, never by pose.
3. After a fold or unfold, put VoiceOver back where the person was. Wait for the new layout first.
4. Reflow at large text sizes. Never truncate or clip. Design the closed outer display at the largest size first.
5. Under Reduce Motion: no hinge effects, no moving or zooming resize animations. Fades only.
6. Check every custom colour with Increase Contrast on, in light and dark. Never show state with colour alone.
7. Give every main command a keyboard shortcut and a label. Every drag, swipe and hinge input needs a button or a named action.
8. Use system controls. Give icon-only buttons a title (`Label`), because vertical bars hide it on screen and VoiceOver, Voice Control and the overflow menu still need it. Give your own icon-only buttons a 44 pt frame inside the label.
9. Put accessibility modifiers, `contentShape` and gestures before `.position`.
10. Test closed, open and partly folded: Accessibility Inspector by hand, `performAccessibilityAudit` and a VoiceOver walk in UI tests.

## 1. VoiceOver order across two panes

VoiceOver reads top to bottom, then leading to trailing, the way people read the language ([HIG, VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover#Navigation)). Two panes side by side break that. *Measured*, closed and open, with two plain panes in an `HStack`:

```text
Inbox, Heading | Message, Heading | Left 1 | Right 1 | Left 2 | Right 2 | Left 3 | Right 3
```

- Moving the right pane 20 pt lower did not help. `ArrangementView` with `.split` read row by row too, open; closed, it showed only the primary (*measured*).
- `NavigationSplitView` already reads the sidebar, then the detail (*measured* open). Leave it alone.

Make each pane a container with `accessibilityElement(children: .contain)`. VoiceOver then visits all of one container's children before the next container ([doc](https://developer.apple.com/documentation/swiftui/accessibilitychildbehavior/contain)).

```swift
import SwiftUI

extension View {
    /// One VoiceOver container per pane: the whole pane is read before the next one.
    /// A higher priority is read first; the default is 0, leading pane first.
    func accessibilityPane(_ label: LocalizedStringKey, priority: Double = 0) -> some View {
        accessibilityElement(children: .contain)
            .accessibilityLabel(label)
            .accessibilitySortPriority(priority)
    }
}

@available(iOS 27.1, *)
struct ArticleWithComments: View {
    var body: some View {
        ArrangementView {
            ScrollView { Text("Article text") }
                .accessibilityPane("Article")
        } secondary: {
            List(1...20, id: \.self) { Text("Comment \($0)") }
                .accessibilityPane("Comments")
        }
    }
}
```

*Measured* with containers labelled "Inbox pane" and "Message pane": `Inbox, Heading | Left 1 | Left 2 | Left 3 | Message pane, Message, Heading | Right 1 | ...`. VoiceOver spoke the second pane's label (the probe's own text; VoiceOver adds no "pane") as it entered it, but not the first pane's label at the start. With `accessibilitySortPriority(1)` on the right pane, VoiceOver read it first. Higher numbers go first; the default is 0 ([doc](https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:))).

- Add a heading trait (`.accessibilityAddTraits(.isHeader)`) to each pane's title so the rotor can jump between panes.
- The fold is not an element. Content that crosses it needs nothing. In a two-page layout, make each page a container ("Page 12").
- Don't hide a visible pane with `accessibilityHidden`. Closed, a pane that is not on screen is already gone.
- UIKit, recipes for each pattern, and the rotor: [references/voiceover-order.md](references/voiceover-order.md).

## 2. Focus after fold and unfold

When the window resizes, views come and go, and VoiceOver can lose its place. *Measured*, real fold in Device Hub, with VoiceOver on a list row that only exists open:

| Code | Where VoiceOver landed after Closed |
|---|---|
| Nothing | `Back, Button`, the first element on screen |
| Focus set at once in `onChange(of: horizontalSizeClass)` | `Back, Button`: the request was lost |
| Focus set 0.3 s later | `Lunch on Friday, Heading`, the target |

So wait for the new layout, then move focus once, to the element that holds the person's place.

```swift
import SwiftUI

/// Moves VoiceOver to `target` after a fold, unfold or Split View change
/// switches the width class. Measured: a move made at once was ignored.
struct RefocusAfterResize<Value: Hashable>: ViewModifier {
    let focus: AccessibilityFocusState<Value?>.Binding
    let target: () -> Value?
    var delay: Duration = .milliseconds(500)
    @Environment(\.horizontalSizeClass) private var widthClass

    func body(content: Content) -> some View {
        content.task(id: widthClass) {
            // .task restarts on every change and cancels a pending move.
            guard (try? await Task.sleep(for: delay)) != nil, let value = target() else { return }
            focus.wrappedValue = value
        }
    }
}

struct MessageScreen: View {
    enum Spot: Hashable { case row(Int), title }
    @AccessibilityFocusState private var spot: Spot?
    @State private var lastSpot: Spot?
    @Environment(\.horizontalSizeClass) private var widthClass

    var body: some View {    // accessibilityPane: section 1
        HStack(alignment: .top) {
            if widthClass == .regular {
                List(1...4, id: \.self) { row in
                    Text("Row \(row)").accessibilityFocused($spot, equals: .row(row))
                }
                .accessibilityPane("Messages")
            }
            VStack(alignment: .leading) {
                Text("Lunch on Friday").font(.title)
                    .accessibilityAddTraits(.isHeader)
                    .accessibilityFocused($spot, equals: .title)
                Text("See you at noon.")
            }
            .accessibilityPane("Message")
        }
        .onChange(of: spot) { _, new in if let new { lastSpot = new } }
        .modifier(RefocusAfterResize(focus: $spot) {
            // Closed, the list is gone: fall back to the title.
            if case .row = lastSpot, widthClass != .regular { return .title }
            return lastSpot
        })
    }
}
```

- The task runs on first appear too. With nothing focused yet, `lastSpot` is nil and it does nothing.
- Move focus only to keep the person's place. Apple allows a move to a nearby item when the focused one disappears ([HIG, Focus](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Best-practices)). Don't announce it.
- Our run used `onChange` and a 0.3 s sleep. This modifier does the same with `.task(id:)` and 0.5 s; it was not run on a real fold or on hardware, and unfold (closed to open) was not measured (*unverified*). Test both the same way.
- UIKit (`UIAccessibility.post(notification: .layoutChanged, argument:)`), `@FocusState` for text fields, and the full measurements: [references/focus-after-fold.md](references/focus-after-fold.md).

## 3. Dynamic Type at both display sizes

One text size meets two very different widths. The narrow cases: the closed outer display, 382 pt of safe-area width (*measured* by `duo-design-system`), and, open, the pane beside the vertical bar, about 371 pt (*derived*, [references/dynamic-type.md](references/dynamic-type.md#two-panes-at-large-sizes)). Apple asks you to show as much text at the largest accessibility size as at the largest standard size, and to stack items when they crowd ([HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography#Supporting-Dynamic-Type)).

```swift
import SwiftUI

struct MessageRow: View {
    let subject: String
    let date: String
    @Environment(\.dynamicTypeSize) private var typeSize
    @ScaledMetric(relativeTo: .body) private var avatar = 32.0

    var body: some View {
        let stacked = typeSize.isAccessibilitySize
        let layout = stacked
            ? AnyLayout(VStackLayout(alignment: .leading, spacing: 4))
            : AnyLayout(HStackLayout(alignment: .center, spacing: 8))
        layout {
            Circle().fill(.tint).frame(width: avatar, height: avatar)
                .accessibilityHidden(true)
            Text(subject)                       // no lineLimit, no fixed height
            if !stacked { Spacer(minLength: 8) }
            Text(date).foregroundStyle(.secondary)
        }
        .accessibilityElement(children: .combine)
    }
}
```

*Measured* closed, with a row built the same way: 348 × 42 pt at Large, 297 × 370 pt at AX5, no audit issues. The same row with `lineLimit(1)` and `frame(height: 30)` got two "Text clipped" issues, at the default size and at AX5.

- `AnyLayout` keeps view identity, so state survives the switch ([doc](https://developer.apple.com/documentation/swiftui/anylayout)).
- `ViewThatFits` picks the first child that fits, for short strips of controls ([doc](https://developer.apple.com/documentation/swiftui/viewthatfits)).
- Size icons, avatars and spacing with `@ScaledMetric`, never fixed numbers ([doc](https://developer.apple.com/documentation/swiftui/scaledmetric)).
- Open, cap line length and use fewer, wider columns at accessibility sizes (`readableWidth` and `span` in `duo-design-system`).
- Custom views in a vertical bar can't grow; the bar has a fixed width ([talk 111462](https://developer.apple.com/videos/play/tech-talks/111462/?time=611)). Give them `accessibilityShowsLargeContentViewer()` ([doc](https://developer.apple.com/documentation/swiftui/view/accessibilityshowslargecontentviewer(_:))).
- More recipes, UIKit and what to test: [references/dynamic-type.md](references/dynamic-type.md).

## 4. Reduce Motion, Increase Contrast, Reduce Transparency

Reduce Motion asks you to cut zooming, scaling and peripheral motion, and to swap slides for fades ([HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive)). On Duo that means the hinge and the resize.

```swift
import SwiftUI

@available(iOS 27.1, *)
struct HingeParallax: ViewModifier {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var lift = 0.0

    func body(content: Content) -> some View {
        content
            .offset(y: reduceMotion ? 0 : lift)          // resets at once if the setting turns on
            .onHingeChange(isEnabled: !reduceMotion) { _, new in
                guard let hinge = new.hinge, hinge.status == .partiallyOpen else { lift = 0; return }
                lift = (180 - hinge.angle.degrees) / 10  // decoration only, never layout
            }
    }
}
```

- Resize, as in `duo-transitions`: `.animation(reduceMotion ? nil : .smooth(duration: 0.3), value: widthClass)` on the stack, so nothing moves or resizes under Reduce Motion. A pane that appears gets `.transition(reduceMotion ? .opacity.animation(.easeInOut(duration: 0.2)) : .opacity.combined(with: .move(edge: .trailing)))`: the fade carries its own animation, so it still fades (*measured* by `duo-transitions`). iOS 26.4 adds `accessibilityPrefersCrossFadeTransitions` for the finer setting ([doc](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityprefersCrossFadeTransitions)).
- No VoiceOver announcement and no haptic per hinge angle. Hinge input needs an on-screen control that does the same job (`duo-postures`).
- Increase Contrast: read `colorSchemeContrast == .increased` and give custom colours high-contrast variants. Text needs 4.5:1, or 3:1 at 18 pt or bold ([HIG](https://developer.apple.com/design/human-interface-guidelines/accessibility#Vision)). *Measured:* the audit failed `Color(white: 0.85)` text on white and said "nearly passed" for `.secondary` text.
- Reduce Transparency gives the vertical bar a background. Custom bar content must read on both ([talk 111462](https://developer.apple.com/videos/play/tech-talks/111462/?time=652)).
- Differentiate Without Color: add a shape, symbol or `.isSelected` trait to the selected pane or row.
- UIKit and full recipes: [references/motion-and-contrast.md](references/motion-and-contrast.md).

## 5. Keyboard, Switch Control and Voice Control

People can drive any iPhone from a hardware keyboard, and Full Keyboard Access lets them reach every control from it ([Testing system accessibility features](https://developer.apple.com/documentation/accessibility/testing-system-accessibility-features-in-your-app)).

```swift
import SwiftUI

struct ReplyControls: View {
    let reply: () -> Void
    let archive: () -> Void

    var body: some View {
        HStack {
            iconButton("Reply", "arrowshape.turn.up.left", reply)
                .keyboardShortcut("r", modifiers: .command)
                .accessibilityInputLabels(["Reply", "Answer"])
            iconButton("Archive", "archivebox", archive)
                .keyboardShortcut("e", modifiers: .command)
        }
    }

    /// Icon only; the title stays for VoiceOver and Voice Control. 44 pt hit area, as in duo-ergonomics.
    private func iconButton(_ title: LocalizedStringKey, _ symbol: String, _ action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Label(title, systemImage: symbol).labelStyle(.iconOnly)
                .frame(minWidth: 44, minHeight: 44).contentShape(.rect)  // inside: outside, the audit flagged it
        }
    }
}
```

- Use Command shortcuts and don't take over standard ones ([HIG, Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards#Best-practices)).
- *Measured* closed, in UI tests: `UIFocusSystem.focusSystem(for:)` was nil in every run and Tab never reached `focusable()` views. Tab moved between two text fields in one run, not in another. Command shortcuts worked. Inner display: *unverified*. `focusSection()` is unavailable on iOS (iOS 27.1 SDK): use `@FocusState`, `focused(_:equals:)` and `defaultFocus(_:_:priority:)`.
- `accessibilityInputLabels` gives Voice Control and Full Keyboard Access other names, most important first ([doc](https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:))).
- Switch Control and Voice Control need a tap path for every drag: a button or `accessibilityAction(named:_:)`.
- Details, UIKit `UIKeyCommand`, and Full Keyboard Access checks: [references/keyboard-and-switch.md](references/keyboard-and-switch.md).

## 6. Accessibility modifiers before .position

`.position` returns a view as large as its parent. A `contentShape` or gesture after it covers that whole area, and the accessibility element grows with it. *Measured*: a 60 pt circle with `contentShape(Rectangle())`, a tap gesture and its accessibility element after `.position` got a 382 × 103 pt element, and a tap at the far left of the area counted. With those modifiers before `.position`: 60 × 60 pt. An accessibility element alone after `.position` stayed 60 × 60 pt; keep the order anyway. A `contentShape` and tap on a container also stretched its child's element to the container (*measured*, as in `recipe-two-player-game`). Prefer a `Button` when you can: placed with `.position`, it kept its own 51 × 20 pt frame (*measured*); give it a 44 pt label frame as in section 5.

```swift
import SwiftUI

struct Target: View {
    let hit: () -> Void

    var body: some View {
        GeometryReader { proxy in
            Circle()
                .frame(width: 56, height: 56)
                .contentShape(Circle())            // hit area: the circle
                .onTapGesture(perform: hit)
                .accessibilityElement()
                .accessibilityLabel("Target")
                .accessibilityAddTraits(.isButton)
                .accessibilityAction { hit() }     // VoiceOver and Switch Control activate
                .position(x: proxy.size.width / 2, y: proxy.size.height / 2) // last
        }
    }
}
```

## 7. Test on the iPhone Duo simulator

1. **Settings.** `xcrun simctl ui <UDID> content_size accessibility-extra-extra-extra-large` and `increase_contrast enabled`. Reduce Motion, Reduce Transparency, Bold Text and Full Keyboard Access: Accessibility Inspector's Settings pane or the Settings app. Put every setting back on a shared simulator.
2. **Accessibility Inspector** (Xcode > Open Developer Tool). Pick the simulator and your app. Use the navigation play button to hear the reading order, then run an audit. Repeat closed, open and partly folded ([Inspecting screens](https://developer.apple.com/documentation/accessibility/inspecting-the-accessibility-of-screens)).
3. **UI tests.** [`performAccessibilityAudit(for:_:)`](https://developer.apple.com/documentation/xcuiautomation/xcuiapplication/performaccessibilityaudit(for:_:)) in each pose and text size, and a VoiceOver walk with [`XCUIDevice.shared.voiceOverService`](https://developer.apple.com/documentation/xcuiautomation/xcuidevice/voiceoverservice) (iOS 27). The query order of XCUI elements is not VoiceOver's order (*measured* on a split view), so test order with the VoiceOver service.
4. **Poses.** No test API changes the pose. Use `duo-pose set closed` from `duo-pose-matrix`, or ask the person to press the pose in Device Hub. `duo-pose` refuses while any UI test runs, your own fold-focus test included: check that the only test processes are yours (`pgrep -fl "xctrunner|xcodebuild.*test"`), then pass `--force` with the user's OK. Otherwise ask the person to press Closed.

Test file, launch arguments, cleanup if VoiceOver stays on, and the audit results we got: [references/testing.md](references/testing.md).

## Checklist

- [ ] Each custom pane is an `accessibilityElement(children: .contain)` with a label; the order is the same closed, open and partly folded.
- [ ] Pane titles have the header trait.
- [ ] After fold and unfold, VoiceOver lands on the person's place, moved once, after the layout settles.
- [ ] At AX5 on the closed display and in the open pane beside the vertical bar, nothing truncates, clips or overlaps; rows stack; no `lineLimit(1)` on content, no fixed text heights.
- [ ] Icons and spacing use `@ScaledMetric`; custom bar items have a large content view.
- [ ] Reduce Motion turns off hinge effects and moving resize animations; fades remain.
- [ ] Custom colours pass 4.5:1 (3:1 at 18 pt or bold) in light, dark and Increase Contrast; state never relies on colour alone.
- [ ] Main commands have Command shortcuts; icon-only buttons have titles and a 44 pt hit area; drags and hinge input have a button or named action.
- [ ] Accessibility modifiers, `contentShape` and gestures come before `.position`.
- [ ] Accessibility Inspector order and audit checked closed, open and partly folded; UI tests run the audit and a VoiceOver walk.
- [ ] VoiceOver, text size and contrast are back to their defaults on the shared simulator.
