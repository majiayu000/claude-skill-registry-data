---
name: duo-postures
description: "Designs iPhone Duo screens for every pose Apple shows: closed on the outer display, open flat (wide or tall), partly folded like a book, propped on a table like a laptop (tabletop), standing like a tent, and open and turned around (flipped, rear cameras facing the user). Use it when a screen must work half folded, when you build a tabletop media player or video call (video on top, the same controls below the fold), a book-pose layout with two regions, or a hinge effect. There is no posture API: read size classes and the .division reserved region (active only when partly folded) with FoldGeometry and FoldRegionsLayout, and keep onHingeChange and UIHingeInteraction for effects, with Reduce Motion and accessibility rules."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# Duo postures

Use this skill to decide what a screen does in each way people hold or set down iPhone Duo, then build it. It covers closed, open flat, book, tabletop, tent and flipped, the two layouts Apple singles out (half folded like a book, and set on a table), and the hinge as a source of effects.

Load neighbours when the task needs them: `duo-layout` (size classes, safe areas, reserved regions in depth), `duo-patterns` (which layout pattern a screen uses), `duo-navigation` (bars and sheets), `duo-continuity` (state through a fold).

## Words

Apple calls these "device poses" and describes them with comparisons: "partially folded, like a book", "seated on a table like a laptop", "folded like a tent", "open, turned around". It never says "posture", "tabletop" or "tent mode". Duology uses **book**, **tabletop**, **tent** and **flipped** as shorthand for those descriptions. None of them is an API, an enum case or a Device Hub button. Never write code that pretends the system reports them. Labels below: *measured* means we ran it on the iPhone Duo simulator; *unverified* means we could not confirm it.

## Rules

1. **Design two layouts, not six.** Build one for compact width (the outer display) and one for regular width (the inner display). Together they cover every pose. Let the layout grow; don't design one per pose ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Device-poses), [talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=230)).
2. **There is no posture API.** Read the size class, the view's own size and the `.division` reserved region. Active division means partly folded. Its shape tells you which way the fold runs ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=433), [api-index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#not-in-the-sdk)).
3. **Same controls and hierarchy in every pose.** Tabletop is the one optional special layout Apple suggests, and it keeps every control ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=276)).
4. **Nothing interactive in the fold** when it is active. Scrolling content may cross it ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)).
5. **Small moves.** Move only what must move, keep groups together, and keep each view's identity so state survives ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions)).
6. **The hinge is for effects.** Never lay out from the hinge angle or status. Hinge input is a novelty: opt-in, with an on-screen alternative, and off with Reduce Motion ([talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=154)).
7. **Check every pose in Device Hub** before you call a screen done.

## Tell the poses apart from layout inputs

Add `FoldGeometry` and `FoldRegionsLayout` from [references/fold-regions.md](references/fold-regions.md) once per app. If the app already has a `FoldGeometry` (`duo-patterns` adds one), keep a single copy, and make sure its `init(_:)` filters with `liesInside(_:of:)` as fold-regions.md shows. A copy taken from `duo-patterns` before v0.2 may lack the filter; add it. Then read the fold with `.onFoldChange { fold = $0 }` on the view you lay out.

| Pose (Duology word) | Apple's words | Your app is on | Size classes (width, height) | `.division` region | `FoldGeometry` |
|---|---|---|---|---|---|
| Closed | closed | Outer display | compact, regular in portrait; compact, compact in landscape ([111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=187)) | none | `frame == nil` |
| Tent | "folded like a tent", "standing on its edges" | Outer display, held sideways (our reading of Apple's drawing and talk 111461; unverified) | compact, compact | none | `frame == nil` |
| Open, flat | "open in a wide layout", "open in a tall layout" | Inner display | regular, regular (*measured* held wide) | inactive | `frame != nil && !isActive` |
| Book | "partially folded, like a book" | Inner display, held wide | regular width expected (unverified) | active, top to bottom | `isActive && isVertical` |
| Tabletop | "seated on a table like a laptop" | Inner display, held tall | regular width expected (unverified) | active, side to side | `isActive && !isVertical` |
| Flipped | "open, turned around" | Outer display, phone still open (camera apps) | compact width (derived; unverified) | none | `frame == nil` |

What this means for code:

- A view sees its size, its size class and its regions. That is all a layout needs. "Book" is just "an active fold runs top to bottom through this view".
- Tent looks like the closed phone held sideways, and flipped looks like the closed phone. Don't try to tell them apart.
- Hinge status says how open the phone is, not which display you are on. When flipped, the phone is open but your app is on the outer display. Never pick a layout from `DeviceHinge.Status`.

## What to do in each pose

### Closed (outer display)

- Use your compact-width layout: one column, with the system's vertical bars on the side.
- Keep the same features and state as open. Open may add one level of hierarchy, as Mail adds the message beside the list ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)).
- Support landscape on the outer display. Apple suggests it because people may set the phone down like a tent ([111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=210)).
- The outer camera always occludes part of the view. Bars already avoid it; custom corner controls read `.occlusion` (see `duo-layout`).

### Open, flat (wide or tall)

- Use your regular-width layout: two panes, a sidebar, more columns. Don't stretch the phone layout.
- The fold is inactive, so nothing needs to move. Still put seams and gutters on the fold line, read with `.includeInactive`, so folding later moves nothing.
- Use an even column count in grids ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=456)).
- Held tall, the inner display keeps horizontal bars; every other pose puts them on the side ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=327)).

### Book (partly folded, held wide)

- Detect it with `fold.isActive && fold.isVertical`.
- Let the system do its part. Sheets slide off the fold. Alerts, menus and toolbar buttons move aside. Split views even out to 50/50 ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=557), [talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=340)).
- Move your own controls out of the fold frame, to the trailing region. That is near where they sit once the phone closes, and where the system puts alerts ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=249)).
- Fit images, cards and text to one region. Nothing reads well across the curve ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=101)).
- Two pieces of content: one per region. One centred column: decide which region it lives in, or make it two columns.
- Recipe: [Book pose: two regions](#recipe-book-pose-two-regions).

### Tabletop (partly folded, held tall, propped on a table)

- Detect it with `fold.isActive && !fold.isVertical` (the frame is wider than tall).
- This is the one optional per-pose layout. Things to watch from a distance go in the top region: video, the other person in a call, a timer. Things to touch go in the bottom region, the stable base ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=283), [talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=263)).
- Keep every control and the same hierarchy. Never add a feature that only exists here ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=295)).
- The inner camera sits on the right edge of the bottom region (*measured* region frame, below). In a video call it is active: keep controls clear of it.
- Held tall, the inner display keeps the familiar horizontal bars ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=327)), so navigation bar items sit at the top, in the top region (*measured*, gallery list-detail screen). Keep playback or call controls in your own bottom-region view, not in a bar.
- Recipe: [Tabletop media](#recipe-tabletop-media).

### Tent (standing on its edges)

- Apple's material shows the tent only as an illustration: a drawing among the six poses, plus passing mentions ("standing on its edges", "set the phone down like a tent"). The only guidance attached is to support landscape on the outer display ([111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=215)). Device Hub has no tent button, and no API reports it.
- Make sure your closed layout works held sideways (compact width, compact height). Build nothing tent-specific.
- Test it as Closed plus a rotation in Device Hub.

### Flipped (open, turned around)

- A camera case. Open and turned around, the rear cameras and the outer display face the person, and a camera app can move to the outer display to take a selfie with a rear camera ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=277), [camera direction guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces)).
- Layout: nothing new. Your app gets the outer display's compact size.
- Camera: ask `AVCaptureDeviceDirectionCoordinator` (AVKit) which cameras face forward. Mirror the preview yourself when a rear camera faces the person. Never infer direction from `position == .back` ([api-index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#camera)).
- Device Hub has no flip control, so check this case on a device.

## Recipe: tabletop media

Video in the top region and the same controls in the bottom region when the phone sits folded on a table. Folded like a book, the video goes leading and the controls trailing. Closed or flat, the controls float over the video. One layout, so neither view is rebuilt.

```swift
import AVFoundation
import SwiftUI

// requires: FoldGeometry, FoldRegionsLayout (references/fold-regions.md)
// requires: PlayerSurface, PlayerControls (references/tabletop-media.md)

@available(iOS 27.1, *)
struct TabletopPlayer: View {
    let player: AVPlayer
    @State private var fold = FoldGeometry()
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        FoldRegionsLayout(fold: fold, unfolded: .overlay) {
            PlayerSurface(player: player)   // first: what people watch
                .ignoresSafeArea()
            PlayerControls(player: player)  // second: what people touch
        }
        .onFoldChange { fold = $0 }
        // A short slide. With Reduce Motion the controls move without animating.
        .animation(reduceMotion ? nil : .smooth(duration: 0.3), value: fold)
        .background(.black)
    }
}
```

Full code, the video call variant (remote video on top, self view and call controls below) and the system alternative (`ArrangementView` with `.overlay`): [references/tabletop-media.md](references/tabletop-media.md).

## Recipe: book pose, two regions

What people read goes leading and what they touch goes trailing, with the fold as the divider. Flat, the same split sits on the fold line, so folding changes nothing but the gap. Closed, the two views stack, or sit side by side in landscape.

```swift
import SwiftUI

// requires: FoldGeometry, FoldRegionsLayout (references/fold-regions.md)
// requires: CountdownFace, CountdownControls (references/book-two-region.md)

@available(iOS 27.1, *)
struct CountdownScreen: View {
    @State private var fold = FoldGeometry()
    @State private var remaining = 300
    @State private var isRunning = false

    var body: some View {
        FoldRegionsLayout(fold: fold, unfolded: .split) {
            CountdownFace(remaining: remaining)
            CountdownControls(remaining: $remaining, isRunning: $isRunning)
        }
        .onFoldChange { fold = $0 }
        .task(id: isRunning) {
            guard isRunning else { return }
            while remaining > 0 {
                // Cancelled (paused, or the view went away): stop, keep the time.
                do { try await Task.sleep(for: .seconds(1)) } catch { return }
                remaining -= 1
            }
            isRunning = false
        }
    }
}
```

When to pick `.split` or `.overlay`, and the full code: [references/book-two-region.md](references/book-two-region.md).

## The hinge: effects, and input only as a novelty

`onHingeChange(isEnabled:_:)` (SwiftUI) and `UIHingeInteraction` (UIKit) report a status (`closed`, `partiallyOpen`, `fullyOpen`) and a live angle. Apple shows them driving a wallpaper zoom and a guitar's pitch bend, and keeps layout for regions and arrangements ([talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=49)).

- Decoration only. The app must work the same with the effect off, on a phone without a hinge, and when the phone sits still.
- Turn it off with Reduce Motion. Zooming and scaling are the motion that setting asks you to cut ([HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Cognitive)).
- Hinge input needs an on-screen control that does the same job, and the person turns the hinge on. Some people can't fold the phone, or use it on a mount ([HIG Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)).
- Never trigger an action when the hinge crosses an angle. Folds happen by accident, in a pocket or a shifting grip.
- `hinge` is `nil` without a hinge. Reset the effect when the status is not `partiallyOpen`.
- Prefer `status`. The angle's update rate and precision are system policy (UIKit's `UIHinge.h`).

```swift
import SwiftUI

@available(iOS 27.1, *)
struct HingeZoomArtwork: View {
    let image: Image
    @State private var zoom: CGFloat = 1
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        // Color.clear takes the space offered; the image fills it and is clipped to it.
        Color.clear
            .overlay {
                image
                    .resizable()
                    .scaledToFill()
                    .scaleEffect(reduceMotion ? 1 : zoom)
            }
            .clipped()
            .accessibilityHidden(true)
            .onHingeChange(isEnabled: !reduceMotion) { _, context in
                guard let hinge = context.hinge, hinge.status == .partiallyOpen else {
                    zoom = 1
                    return
                }
                // 180 degrees is flat. Up to 8 percent larger as the phone closes.
                zoom = 1 + 0.08 * (1 - min(max(hinge.angle.degrees / 180, 0), 1))
            }
    }
}
```

Hinge input with an on-screen alternative, UIKit, and testing angles: [references/hinge.md](references/hinge.md).

## Measured fold frames

iOS 27.1 iPhone Duo simulator, read from the reserved regions with the gallery app's region overlay and our probes (16 to 19 October 2026). Frames are in a view that fills the window. Full detail: [`duo-patterns` two-page measurements](https://github.com/Kimeur/duology/blob/main/plugins/duology-design/skills/duo-patterns/references/two-page.md#what-we-measured) and [references/measurements.md](references/measurements.md).

| Pose | Window | `.division` region | Camera (`.occlusion`, our reading) |
|---|---|---|---|
| Closed | 466 × 678 pt | none | outer camera, active, 37 × 37 pt at (400, 29) |
| Open, flat, held wide | 951 × 669 pt | inactive, 40 × 669 pt at (455, 0) | inner camera, inactive, 58 × 37 pt at (677, 21) |
| Book | 951 × 669 pt | active, 40 × 669 pt at (455, 0) | inner camera, inactive, 58 × 37 pt at (677, 21) |
| Tabletop | 669 × 951 pt | active, 669 × 40 pt at (0, 455) | inner camera, inactive, 37 × 58 pt at (611, 677): right edge, bottom half |

- Folding flips `isActive`; the frame stays put. Read it with `.includeInactive` and a split lands in the same place flat and folded.
- The 40 pt is a zero-width fold line plus 20 pt of margins on each side. Keep controls out of the whole frame.
- The default query returned only active regions, and the first layout pass returned none. React with `onGeometryChange`; don't read once in `onAppear`.
- Device Hub's Partially Open settles the hinge at 127° held wide and 128° held tall (*measured*, 19 October 2026).
- Not yet measured: size classes in book and tabletop, and the fold width at other angles.

## UIKit

Read `traitCollection` size classes and query `reservedRegions(kind: .division, options: .includeInactive)` in the view's own `layoutSubviews`. That is enough: UIKit runs that `layoutSubviews` again when the fold turns active or inactive (*measured*; `viewDidLayoutSubviews` not yet checked). Don't trigger layout from `UIHingeInteraction`; when folding, the status changes 0.7 to 0.9 s before the region does. Keep the hinge for effects. Code: [references/uikit.md](references/uikit.md) and [references/hinge.md](references/hinge.md#uikit).

## Test every pose

In Device Hub, under the bezel: Closed, Partially Open, Open, and the rotate buttons. Option-drag the slider for any angle ([Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)).

| Pose | Device Hub |
|---|---|
| Closed, then tent | Closed; then rotate for landscape |
| Open, wide and tall | Open; rotate for tall |
| Book | Partially Open, held wide |
| Tabletop | Partially Open, then Rotate Right once (Rotate Right three more times returns to wide) |
| Hinge effects | Partially Open, then Option-drag the slider |
| Flipped | Not in Device Hub; use a device |

`simctl` has no pose command. Device Hub's buttons can be pressed through the macOS Accessibility API, but only after the user gives that permission ([AGENTS.md](https://github.com/Kimeur/duology/blob/main/AGENTS.md#rules-that-apply-everywhere)). Otherwise ask the user to press the pose.

## Checklist

- [ ] One compact-width and one regular-width layout; no layout per pose.
- [ ] Layout reads size class, the view's size and `.division`. No hinge status or angle, device orientation, `UIScreen.main` or idiom picks a layout.
- [ ] Book: no button, slider or text field in the active fold frame; your controls sit in the trailing region.
- [ ] Tabletop, if built: watch-from-afar content in the top region, every control in the bottom region, clear of the inner camera.
- [ ] Every control exists in every pose, in the same hierarchy.
- [ ] Views keep their identity across poses (one `Layout`, no `if` swapping view trees).
- [ ] Closed layout works in landscape (tent).
- [ ] Flipped camera apps use the direction coordinator and mirror a forward-facing rear camera.
- [ ] Hinge effects are decoration, off with Reduce Motion, reset when not `partiallyOpen`, and safe when `hinge` is `nil`.
- [ ] Hinge input is opt-in and has an on-screen control that does the same job.
- [ ] iOS 27.1 APIs sit behind `@available` or `if #available` when the app deploys lower.
- [ ] Checked in Device Hub: Closed (portrait and landscape), Open (wide and tall), book, tabletop, Option-drag angles, Split View, and with Reduce Motion on.
