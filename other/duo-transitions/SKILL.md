---
name: duo-transitions
description: "Makes fold, unfold, partial fold and rotation on iPhone Duo, Apple's foldable, feel like one app instead of a reload. Use when a screen flashes, blinks, jumps, reloads, pops or moves its controls as the phone opens or closes, or when writing or reviewing SwiftUI or UIKit code that animates a resize: AnyLayout, stable ForEach IDs, matchedGeometryEffect, geometryGroup, .animation(_:value:), transaction, withAnimation, contentTransition, accessibilityReduceMotion, viewWillTransition(to:with:), animate(alongsideTransition:completion:), UIView.animate with a SwiftUI spring, and 120 Hz ProMotion frame budgets."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-transitions

Opening or closing iPhone Duo resizes your app, the same way a person resizes it in iPhone Mirroring ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=142)). People do it often, so Apple asks for an app that stays predictable and consistent inside and out ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=479)). This skill makes the change read as the same screen taking a new shape, not a new screen loading.

Load other skills for neighbouring work: `duo-continuity` (scroll, selection, typing and playback that must survive), `duo-patterns` (layouts, and displacement off the fold), `duo-layout` (size classes, reserved regions), `duo-navigation` (bars move on their own).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1), pressing Device Hub's pose buttons; see [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. *Device only* means the simulator can't show it. Everything else comes from Apple's pages, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## What each change hands your app

All *measured*:

| Change | Window | Size class | UIKit coordinator | SwiftUI transaction |
|---|---|---|---|---|
| Open | 466 × 678 → 951 × 669 pt, other display | compact → regular. From closed portrait: same update as the new size (2 runs). From closed sideways: about 16 ms *before* it (1 run) | not animated, duration 0 | no animation |
| Close | 951 × 669 → 466 × 678 pt, other display | regular → compact, 25 to 70 ms *before* the new size | not animated, duration 0 | no animation |
| Partially open | no change | no change | no call | the fold region turns active once the hinge settles |
| Rotate | width and height swap | vertical class flips on the closed phone | animated, 0.3 s | no animation |

- A fold keeps your app running: one root view, no relaunch, and the scene never left the active state.
- On open and close the system adds no motion to your layout. Any motion there is motion you add.
- Sizes arrive in steps. On open, a full-width view went 382 → 466 → 951 → 867 pt wide within 50 to 250 ms, as safe area insets changed around the resize.
- The trait change and the size transition come in no fixed order. Never write code that expects one first.

## How SwiftUI animates a resize

1. Every update runs in a transaction. When an animatable value changes (a frame, an offset, an opacity), SwiftUI checks the transaction for an animation. With one, it interpolates from the old value to the new one. Without one, the value jumps ([WWDC23 Explore SwiftUI animation](https://developer.apple.com/videos/play/wwdc2023/10156/?time=280)).
2. `withAnimation` puts an animation in the transaction of a state change *you* make. A fold is not your state change. The system resizes the window and updates `horizontalSizeClass`; none of your code runs first, so there is nothing to wrap. *Measured:* open, close and rotation all reached SwiftUI with no animation, even though a rotation runs `body` inside UIKit's 0.3 s animation.
3. So read the size class, or the view's size, in `body` and build the layout from it. The layout then changes in the very update that brings the new size class.
4. Opt in with [`animation(_:value:)`](https://developer.apple.com/documentation/swiftui/view/animation(_:value:)). When `value` changes in an update, the views below the modifier animate in that update. Key it on a discrete value: the width class, a column count, the fold's active state. Never on the raw size. *Measured:* the opt-in interpolated on open, close, rotation and partial fold; a probe without it jumped.
5. Opt out below an animation: `.animation(nil, value:)` for a subtree, [`transaction(_:)`](https://developer.apple.com/documentation/swiftui/view/transaction(_:)) with `$0.animation = nil` for one leaf (Apple says to use it on leaf views), and [`contentTransition(.identity)`](https://developer.apple.com/documentation/swiftui/contenttransition/identity) to stop a text or symbol cross-fade while its frame still moves. *Measured:* both opt-outs stopped the opt-in.
6. Frames animate at the leaf views that draw. An opt-out on a container also stops that container's frame. [`geometryGroup()`](https://developer.apple.com/documentation/swiftui/view/geometrygroup()) makes a group animate as one frame.

```swift
import SwiftUI

struct NowPlayingScreen: View {
    @Environment(\.horizontalSizeClass) private var widthClass
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        // Read in body, so the arrangement changes in the update that brings the size class.
        let isWide = widthClass == .regular
        let layout = isWide
            ? AnyLayout(HStackLayout(alignment: .center, spacing: 24))
            : AnyLayout(VStackLayout(spacing: 16))
        layout {
            Artwork()            // the same view in both layouts: it moves, it doesn't reload
            PlaybackControls()
        }
        // Opt in: short, no bounce, keyed on a discrete value. Nil under Reduce Motion.
        .animation(reduceMotion ? nil : .smooth(duration: 0.3), value: isWide)
    }
}
```

### Should open and close animate?

Open and close move your window to the other display, and nothing animates unless you ask. With the opt-in above, SwiftUI moves each view from where it sat in the old window to its new place. On open, the closed layout starts in the left part of the inner display, about as wide as the outer display, and grows into the open layout. That follows from how SwiftUI interpolates; we have not recorded it (*unverified*).

- Apple's motion guidance says to avoid adding motion to interactions people repeat often, and not to make people wait for an animation ([HIG, Motion](https://developer.apple.com/design/human-interface-guidelines/motion#Providing-feedback)). People open and close iPhone Duo often.
- So: a short spring (0.3 s, no bounce) or none. Never a long or bouncy one, never a delayed one.
- Whether the short spring reads as "the app unfolds with the phone" or as lag is *device only*. Until you have tested on hardware, keep it short.
- Continuity comes first from identity: the same views, the same controls in the same order and style, the reader's place kept. Motion only helps people follow what moved.
- Rotation, a partial fold and Split View stay on one display. There, motion helps. The system already animates rotation; animate controls you move off the fold yourself (`duo-patterns`, displacement).

### Don't copy the size class into state

```swift
// Bad: a second source of truth, and wrong at launch.
struct NowPlayingScreenCopy: View {
    @Environment(\.horizontalSizeClass) private var widthClass
    @State private var isWide = false          // a copy of the size class

    var body: some View {
        let layout = isWide ? AnyLayout(HStackLayout()) : AnyLayout(VStackLayout())
        layout {
            Artwork()
            PlaybackControls()
        }
        .onChange(of: widthClass) { _, newClass in
            withAnimation(.smooth) { isWide = newClass == .regular }
        }
    }
}
```

- *Measured:* the copy started animating in the same frame as `.animation(_:value:)`, so lateness is not the problem.
- The problems: an app launched open shows the stacked layout until the next fold, because `onChange` without `initial: true` never ran; two values that can disagree; and a second `body` pass on every fold.
- The same goes for `DispatchQueue.main.asyncAfter`, `Task.sleep` before a state change, or an animation started in `onAppear`: each animates *after* the resize, so people see the window change and then the content move. One measured exception isn't an animation: long text that reflows while the margins arrive late needs a scroll back to its saved paragraph after the width settles (`duo-continuity` section 4, the gallery's fold transition screen).
- When a value only exists after layout (the fold's frame, an exact width), use [`onGeometryChange(for:of:action:)`](https://developer.apple.com/documentation/swiftui/view/ongeometrychange(for:of:action:)). Return a small value (a column count, a fold flag), write it in one cheap action, and key the animation on it. *Measured:* on the two opens from closed portrait, its action ran in the same millisecond as the size-class update. On the open from the closed phone held sideways, it ran about 16 ms after it, once the width changed.

## Rules

1. **Same views, new places.** Switch layouts with `AnyLayout`, `ArrangementView` or one container, and give `ForEach` stable IDs. A branch on size class, a `ViewThatFits` that swaps children, or an `.id` fed by layout creates new views. New views can't move from their old frame: they fade or pop, and lose their state ([AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout), [WWDC21 Demystify SwiftUI](https://developer.apple.com/videos/play/wwdc2021/10022/?time=661), `duo-continuity`).
2. **Change with the size, not after it.** Derive layout in `body`. In UIKit, change layout inside the coordinator's alongside block.
3. **Controls keep their place and their look.** Same symbol, title, order, style and tint at every size. Keep their positions relative to each other as similar as you can across poses ([HIG, Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)). Keep a control's edge: bottom stays bottom. Move one only to clear the fold, to the nearest region (`duo-patterns`, displacement).
4. **Small moves, one property at a time.** Favour small adjustments over rearranging ([HIG, Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)). Moving an element far from where it was weakens its link to the content ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=206)). Don't change a control's position, size and style in one change.
5. **No reload flash.** See the table below.
6. **Keep the reader's place.** Scrolling content is not displaced ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=225)). Anchor scroll views by item ID; keep selection in a model (`duo-continuity`).
7. **Let the system animate its own parts.** Sheets, alerts, menus and toolbar buttons move off the fold on their own ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=571)), and split view columns adapt their widths ([HIG, Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)). Don't animate them again.
8. **Respect Reduce Motion.** See below.
9. **Keep each update cheap.** At 120 Hz a frame has about 8.3 ms ([Understanding hitches](https://developer.apple.com/documentation/xcode/understanding-hitches-in-your-app)), and a fold lays out the whole window at once.

## No reload flash

| You see | Usual cause | Fix |
|---|---|---|
| A blank or white frame | A background that differs by size class, or a view rebuilt before it has content | One background for every size; stable identity |
| A spinner or placeholder | A fetch in `onAppear` or `.task` that runs again because the view was rebuilt, or `.task(id:)` keyed on size | Load once, in a model (`duo-continuity`) |
| Images blink | `AsyncImage` rebuilt, so it starts empty and loads again | Stable identity; keep loaded images in a model or cache |
| Everything fades in | `onAppear { withAnimation { opacity = 1 } }` on a layout view | No appearance animation on views a fold rebuilds |
| The list jumps to the top | New identity, or a saved offset restored | `ScrollPosition` by item ID (`duo-continuity`) |
| UIKit cells flash | `reloadData()` or new child view controllers on a trait change | Invalidate the layout inside the coordinator |

## SwiftUI patterns

Full code for each, and the measured transaction rules: [references/swiftui.md](references/swiftui.md).

| Need | Pattern |
|---|---|
| Stacked closed, side by side open | `AnyLayout` and `.animation(_:value:)`, above |
| A pane that only exists open | `if isWide` inside a container that never changes, `.transition(.opacity)` |
| One picture that changes container (mini player artwork into a player pane) | [`matchedGeometryEffect`](https://developer.apple.com/documentation/swiftui/view/matchedgeometryeffect(id:in:properties:anchor:issource:)) on that stateless element only |
| Grid columns | Stable `ForEach` IDs, the animation keyed on the column count |
| Controls off the fold | `FoldGeometry` and `.animation(.smooth, value: fold)`, from `duo-patterns` |
| Text that changes with the size | `.contentTransition(.identity)`, or `.interpolate` for a size change of the same string |
| A part that must snap | `.animation(nil, value:)` on it, under the animated parent |
| Check what a change hands a view | `AnimationProbe`, a debug-only `Animatable` modifier |

## UIKit

```swift
import UIKit

final class PlayerViewController: UIViewController {
    private var tallConstraints: [NSLayoutConstraint] = []
    private var wideConstraints: [NSLayoutConstraint] = []

    override func viewWillTransition(to size: CGSize, with coordinator: any UIViewControllerTransitionCoordinator) {
        super.viewWillTransition(to: size, with: coordinator)
        let isWide = size.width > size.height          // decide from the size you are handed
        coordinator.animate(alongsideTransition: { _ in
            self.applyLayout(isWide: isWide)           // same views, new constraints
            self.view.layoutIfNeeded()                 // rotation: rides the system's animation
        })
    }

    private func applyLayout(isWide: Bool) {
        NSLayoutConstraint.deactivate(isWide ? tallConstraints : wideConstraints)
        NSLayoutConstraint.activate(isWide ? wideConstraints : tallConstraints)
    }
}
```

- [`viewWillTransition(to:with:)`](https://developer.apple.com/documentation/uikit/uicontentcontainer/viewwilltransition(to:with:)) runs before the size changes. Always call `super`. Blocks you pass to [`animate(alongsideTransition:completion:)`](https://developer.apple.com/documentation/uikit/uiviewcontrollertransitioncoordinator/animate(alongsidetransition:completion:)) run in the transition's own animation context.
- *Measured:* on rotation that context lasts 0.3 s, so the layout glides with the window. On open and close the coordinator says `isAnimated` `false` with duration 0, so the layout lands at once, together with the resize.
- Collection views: invalidate the layout inside the alongside block. Never call `reloadData()` there. Keep the top item in view as `duo-continuity` shows.
- A partial fold has no coordinator. Read reserved regions in the `layoutSubviews` of the view that lays out around the fold. UIKit runs that pass again when the fold turns active or inactive (*measured* in [duo-postures](https://github.com/Kimeur/duology/blob/main/plugins/duology-design/skills/duo-postures/references/measurements.md#uikit-layout-passes-on-a-fold)). Don't trigger layout from `UIHingeInteraction`: when folding, the status changes 0.7 to 0.9 s before the region does. Work out the place on every pass, because a resize moves it too. Animate only when the fold changed and the window kept its size, with [`UIView.animate(_:changes:completion:)`](https://developer.apple.com/documentation/uikit/uiview/animate(_:changes:completion:)) (iOS 18), which takes a SwiftUI `Animation`. It is declared in SwiftUI, so the file needs `import SwiftUI`.
- Optional motion on open and close, the partial-fold recipe and Reduce Motion: [references/uikit.md](references/uikit.md).

## Reduce Motion

- Apple's guidance: replace movement along x, y and z with fades, tighten springs, avoid animating depth and blur, and let animations track gestures directly ([HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive)).
- Read it: SwiftUI [`accessibilityReduceMotion`](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion), and [`accessibilityPrefersCrossFadeTransitions`](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityprefersCrossFadeTransitions) from iOS 26.4. UIKit `UIAccessibility.isReduceMotionEnabled` and `UIAccessibility.prefersCrossFadeTransitions`.
- For a fold: layout moves get no animation, so views take their new place at once. A pane that appears gets a short fade. Effects driven by the hinge angle (zoom, parallax, tilt) turn off.

```swift
extension Animation {
    /// The animation for a layout change caused by a fold or a resize.
    /// Nil under Reduce Motion: views take their new place at once.
    static func resize(reduceMotion: Bool) -> Animation? {
        reduceMotion ? nil : .smooth(duration: 0.3)
    }
}
```

*Measured:* a transition with its own `.animation(_:)` ran its full length on a size-class change that carried no animation. So `.transition(.opacity.animation(.easeInOut(duration: 0.2)))` still fades a new pane when the layout animation is `nil`.

## 120 Hz ProMotion

- Both displays have ProMotion up to 120 Hz ([specs](https://www.apple.com/iphone-duo/specs/)). SwiftUI, UIKit and Core Animation pace their animations for it on their own ([Optimizing ProMotion](https://developer.apple.com/documentation/quartzcore/optimizing-iphone-and-ipad-apps-to-support-promotion-displays)). A `.smooth` spring needs no extra code.
- The budget is the hard part: about 8.3 ms per frame for your main thread. Keep `body` free of sorting, filtering, formatting and image decoding. Don't put a `GeometryReader` in every row. Use lazy stacks for long content.
- Custom per-frame drawing with `CADisplayLink`: set `preferredFrameRateRange`, pace by `targetTimestamp`, and add `CADisableMinimumFrameDurationOnPhone` to Info.plist, or iPhone stays at its default rate for it. Code: [references/performance.md](references/performance.md).
- The hinge angle streams continuously. Use it for effects, never to run layout every update ([talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=154)).
- The simulator reports `maximumFramesPerSecond` = 60 ([device facts](https://github.com/Kimeur/duology/blob/main/reference/device-facts.md#displays)). It can't show 120 Hz or hitches.

## What not to animate

| Don't animate | Why | Instead |
|---|---|---|
| Scroll position, or a feed moving between halves | Scrolling content already adapts; moving it breaks continuity | Anchor by item ID; let it reflow |
| Sheets, alerts, menus, bars, split view columns | The system moves them already; a second motion fights it | Nothing |
| The raw window size | It arrives in several steps per fold (measured); each one retargets | A discrete key: width class, column count, fold state |
| Layout from the hinge angle | A continuous stream, meant for effects | Reserved regions and arrangements |
| First appearance after a fold | Reads as a reload | Nothing; a short fade only for a pane that is new |
| A different background or font size per display | A flash, and text that cross-fades | One background; the same type size |
| Position, size and style of one control together | Hard to follow | Move it; keep its look |
| Zoom, 3D or blur on resize | Uncomfortable, and Reduce Motion asks you not to | A plain move or a fade |

## What only a real device shows

- What the hardware shows while the displays hand over, and whether your first frame on the new display looks continuous with it. The simulator can't show the hardware hand-over.
- Whether a short spring on open and close reads as unfolding or as lag.
- Smoothness at 120 Hz and hitches during open and close. The simulator tops out at 60.
- How a spring feels at the speed people really open the phone.
- Frame rates that drop in Low Power Mode or when the phone is hot ([Optimizing ProMotion](https://developer.apple.com/documentation/quartzcore/optimizing-iphone-and-ipad-apps-to-support-promotion-displays)).

Until Duology has run on hardware, its `metadata.verified` says `device: no`. Say so in your own review notes.

## Test it

1. In Device Hub, choose Device > Slow Animations ([Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)). Press Closed, Open and Partially Open, rotate, and drag the app into Split View.
2. Record the display that lights up: start `xcrun simctl io <UDID> recordVideo --display=primary-1 --force open.mov`, press Open, then stop it with Ctrl-C. Use `--display=primary` for Closed. Step through it frame by frame. Look for a blank frame, a pop then a glide, a jump to the top, a control that vanishes and comes back.
3. While debugging, add `AnimationProbe` ([references/swiftui.md](references/swiftui.md#see-what-a-change-hands-you)) to see whether a change reaches a view animated.
4. Turn on Reduce Motion in the simulator's Settings and repeat steps 1 and 2.
5. On a device, profile open and close with the Hitches instrument ([references/performance.md](references/performance.md#test-it)).

## Red flags in review

- `withAnimation` in `onChange(of: horizontalSizeClass)` that copies the size class into `@State`
- `.animation(_:value:)` keyed on `proxy.size`, a width or a `CGSize`; a long or bouncy spring on a size-class change
- `if sizeClass == .compact { A } else { B }` with the same views in both branches; `.id(sizeClass)`
- `DispatchQueue.main.asyncAfter`, `Task.sleep` or `onAppear` animations after a size change
- A background colour, font size or button style chosen by size class
- UIKit: layout changes in the coordinator's completion block on rotation; `reloadData()` in `viewWillTransition(to:with:)` or a trait handler; code that expects the trait change before the size change, or after it
- No `accessibilityReduceMotion` or `isReduceMotionEnabled` check next to custom motion

## Checklist

- [ ] Layout comes from the size class or the view's size, read in `body`; no copy of the size class in `@State`.
- [ ] Layout switches keep identity: `AnyLayout`, `ArrangementView` or one container; stable `ForEach` IDs; no `.id` fed by layout.
- [ ] Every `.animation(_:value:)` is keyed on a discrete value, never on the raw size.
- [ ] Open and close get a short spring (about 0.3 s, no bounce) or no animation; never a delayed one.
- [ ] Parts that must snap opt out with `.animation(nil, value:)`, a leaf `transaction`, or `contentTransition(.identity)`.
- [ ] Controls keep their symbol, title, order, style and tint at every size, and keep their edge.
- [ ] No blank frame, spinner, blinking image or fade-in after close, open or rotate.
- [ ] Scroll position and selection survive (`duo-continuity`).
- [ ] UIKit layout changes run inside `animate(alongsideTransition:completion:)`; no `reloadData()` on a resize; no assumed order of trait and size changes.
- [ ] Reduce Motion: no movement, short fades only; hinge effects off.
- [ ] `body` does no heavy work; custom display links use `preferredFrameRateRange` and `targetTimestamp`.
- [ ] Checked in Device Hub with Slow Animations and in a recording of each display. Smoothness at 120 Hz and the feel of open and close left for a device, and said so.
