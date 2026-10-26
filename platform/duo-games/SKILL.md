---
name: duo-games
description: "Builds games for iPhone Duo, Apple's foldable. The game fills the closed outer display, the open inner display, book pose and tabletop by changing its aspect ratio instead of letterboxing, as Apple's HIG asks; touch controls stay off the fold; and in tabletop the world sits above the fold with the controls below it, like a handheld console. Use when you build or port a SpriteKit, Metal or SwiftUI game, when a game letterboxes, restarts or loses input on fold or unfold, or when you add touch controls or game controller support. Covers SKScene .resizeFill with a camera that keeps the play area in view, one scene or renderer that survives every fold (measured), MTKView drawableSizeWillChange, a UIWindowScene display link that follows the scene to the other display, TouchZones split at the .division reserved region, GameLayout for tabletop, GCController and the simulator's own Gamepad, GCVirtualController and Touch Controller placement, orientation locks the inner display ignores, and two-player games."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-games

A game on iPhone Duo resizes every time someone opens, closes, rotates or folds the phone, often in the middle of play. This skill keeps the game running through all of it, fills every pose, keeps thumbs off the fold, and turns the bottom half into a controller when the phone sits on a table.

Load neighbours when the task needs them: `duo-shared-screen` and `recipe-two-player-game` (two people on one phone), `duo-postures` (every pose, and hinge effects), `duo-layout` (reserved regions in depth), `duo-continuity` (state through a fold), `duo-ergonomics` (thumb reach).

"Book" and "tabletop" are Duology's words for Apple's "partially folded, like a book" and "seated on a table like a laptop". No API reports them. Labels: *measured* means we ran it in a probe app on the iPhone Duo simulator (Xcode 27.1, iOS 27.1, 20 Oct 2026); logs in [references/measurements.md](references/measurements.md). *Unverified* means we could not confirm it. Everything else links to Apple.

## Rules

1. **Fill the screen in every pose.** Change the aspect ratio: show more or less of the world. Letterbox only when you can't avoid it, and then put artwork in the bars ([HIG: iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)).
2. **Keep text and controls the same size in every pose.** Size them in points, outside the world, not in world units that a camera scales ([HIG: iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)).
3. **One game per window, owned above every layout switch.** A fold resizes the scene or the drawable. It never makes a new scene, renderer or game state.
4. **Resize, don't restart.** Size callbacks only recompute what depends on size: the camera, the projection, size-matched textures.
5. **Nothing touchable in the fold.** Movement on the leading side, actions on the trailing side, and the whole `.division` frame, margins included, belongs to neither, flat or folded ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)).
6. **Tabletop: the world in the top region, the controls in the bottom region,** and the same controls as every other pose. Apple suggests this split for media on a table; it fits games too ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=283)).
7. **Handle tall and wide in every build.** You may lock the orientation, but the inner display ignores the lock ([talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=222)).
8. **Touch always works.** A game controller is an extra. Hide touch controls only after the player uses a controller ([HIG: Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Physical-controllers)).
9. **Pause on the scene phase, never on a fold.** Folding is part of play. Set the scene's own `isPaused`: `SpriteView(isPaused:)` didn't resume the game (*measured*).
10. **No hinge as a game input** unless the player turns it on and an on-screen control does the same job (`duo-postures`).

## What the game gets in each pose

*Measured* with the code below: the world ignores the safe area, the controls stay inside it.

| Pose | Window | Scene (world) | Touch controls | `.division` seen by the controls |
|---|---|---|---|---|
| Closed | 466 × 678 pt | 466 × 678 pt | 382 × 644 pt (84 pt trailing and 34 pt bottom inset) | none |
| Open, flat, held wide | 951 × 669 pt | 951 × 669 pt | 951 × 635 pt | inactive, 40 × 669 pt at x = 455.5 |
| Book | 951 × 669 pt | 951 × 669 pt | 951 × 635 pt | active, same frame |
| Tabletop | 669 × 951 pt | 669 × 455.7 pt, above the fold | 669 × 421.5 pt, below the fold | none: the fold lies outside the controls |

- The fold's frame runs from x = 455.5 to 495.5. That is centred in a full-width 951 pt game, but not in a view that a vertical bar narrows: in an 867 pt view the middle is 22 pt left of the fold (*measured* in `duo-reading`). Split at the fold frame, never at `width / 2`.
- Open, held tall, and Split View were not measured with this game. Plan for any size.

## 1. Fill the screen: resize the scene, move the camera

`.resizeFill` makes the scene exactly the size of its view ([`resizeFill`](https://developer.apple.com/documentation/spritekit/skscenescalemode/resizefill)). A camera then scales so the play area always fits; spare room shows more world. Every pose we measured is less wide than the 16:10 play area below, so it fills the width and the spare room shows above and below it: a lot on the closed phone held upright, little in book and tabletop (*derived* from the measured sizes).

```swift
import SpriteKit

/// What the touch controls and a game controller write, and the scene reads every frame.
@MainActor
final class GameInput {
    var move = CGVector.zero        // -1...1 on each axis
    var isFiring = false
}

/// The game world. `.resizeFill` makes the scene exactly the size of its view, so a
/// fold, a rotation or Split View changes the aspect ratio instead of letterboxing.
/// The camera keeps the whole play area in view; spare room shows more world.
final class ArenaScene: SKScene {
    /// The part of the world every size must show, in world points.
    let playArea = CGSize(width: 640, height: 400)
    let input: GameInput
    private let eye = SKCameraNode()

    init(input: GameInput) {
        self.input = input
        super.init(size: playArea)
        scaleMode = .resizeFill
    }

    required init?(coder: NSCoder) { nil }

    override func didMove(to view: SKView) {
        guard camera == nil else { return }    // can run again; build the world once
        addChild(eye)
        camera = eye
        // Add the world's nodes here, around (0, 0).
    }

    /// Runs on every fold, unfold, rotation and Split View change. Never rebuild the world here.
    override func didChangeSize(_ oldSize: CGSize) {
        super.didChangeSize(oldSize)
        guard size.width > 0, size.height > 0 else { return }
        // Scale so the play area fits on both axes. Never crop it.
        eye.setScale(max(playArea.width / size.width, playArea.height / size.height))
    }

    override func update(_ currentTime: TimeInterval) {
        // Read `input` here: it keeps its values through a resize.
    }
}
```

- Draw the world beyond the play area, in every direction. A view wider than the play area's shape (Split View, or a different play area) shows the extra at the sides instead.
- Put the score, menus and labels in SwiftUI over the scene, in points. A camera scale would make them grow and shrink with each fold.
- Keep `didChangeSize(_:)` cheap and safe to repeat. *Measured:* it ran twice for every size change, and once with a passing size (466 × 455.7 pt) when the phone closed from tabletop.
- Can't change the aspect ratio? Letterbox with artwork in the bars. Code: [references/scene-and-renderer.md](references/scene-and-renderer.md#when-you-must-letterbox).

## 2. One game through every fold

Create the session once per window, above every layout switch. The same `SpriteView` and scene stay on screen in every pose; only their size changes.

```swift
import Observation
import SpriteKit
import SwiftUI

// requires: FoldGeometry (references/fold-geometry.md)
// requires: GameInput, ArenaScene (SKILL.md)
// requires: GameLayout (references/tabletop-controller.md), TouchControls (references/touch-controls.md)
// requires: ControllerAware (references/controllers.md)

/// One game per window. Create it in the window's root view, above every layout
/// switch, so a fold never makes a new scene.
@MainActor @Observable
final class GameSession {
    let input = GameInput()
    let scene: ArenaScene
    var isPaused = false

    init() { scene = ArenaScene(input: input) }
}

@available(iOS 27.1, *)
struct GameScreen: View {
    let session: GameSession
    @State private var fold = FoldGeometry()
    @Environment(\.scenePhase) private var phase

    var body: some View {
        GameLayout(fold: fold) {
            // The same SpriteView and scene in every pose: only its size changes.
            SpriteView(scene: session.scene, preferredFramesPerSecond: 120)
                .ignoresSafeArea()
            ControllerAware(input: session.input) {
                TouchControls(input: session.input)      // hidden while a controller is in use
            }
        }
        .onFoldChange { fold = $0 }
        // Pause the scene itself. SpriteView's isPaused argument paused the scene
        // but didn't resume it when it turned false again (measured).
        .onChange(of: session.isPaused || phase != .active, initial: true) { _, paused in
            session.scene.isPaused = paused
        }
        .background(.black)
        .toolbarVisibility(.hidden, for: .statusBar)
        .persistentSystemOverlays(.hidden)
    }
}
```

- *Measured:* one scene object from launch to the end of the run, through closed, open, book, tabletop and closed again. `didMove(to:)` ran once, and the frame counter kept counting through every change.
- Pause only when `scenePhase` leaves `.active`. Opening or closing the phone kept the app active (*measured*: frames kept counting), so a fold never pauses the game.
- Pause the scene, not the `SpriteView`. *Measured:* with `SpriteView(isPaused:)` bound to the phase, a game launched while the app was still inactive stayed frozen once it became active (0 frames in 4 s), and so did a pause button turned off again: the argument set the scene's `isPaused` but didn't clear it. Setting `scene.isPaused` in `onChange` ran in every case, and again after a trip to the Home Screen.
- `.ignoresSafeArea()` on the world only. Controls, score and menus stay in the safe area, clear of the outer camera and the Home indicator ([HIG: Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls)).
- `persistentSystemOverlays(.hidden)` and `toolbarVisibility(.hidden, for: .statusBar)` during play only. Show them again on menus ([`persistentSystemOverlays(_:)`](https://developer.apple.com/documentation/swiftui/view/persistentsystemoverlays(_:)), [`toolbarVisibility(_:for:)`](https://developer.apple.com/documentation/swiftui/view/toolbarvisibility(_:for:))). The `.statusBar` placement is new in iOS 27.0; the iOS 27.1 SDK marks `statusBarHidden(_:)` to be deprecated in its favour. Deploying below iOS 27 (the recipes target iOS 26.0), `.statusBar` doesn't build without a check (*measured*), so keep the old call for older versions:

```swift
import SwiftUI

extension View {
    /// Hides the status bar: the `.statusBar` placement on iOS 27, statusBarHidden() before.
    @ViewBuilder func playStatusBarHidden() -> some View {
        if #available(iOS 27.0, *) {
            toolbarVisibility(.hidden, for: .statusBar)
        } else {
            statusBarHidden()
        }
    }
}
```

## 3. Touch controls off the fold

Movement goes on the leading side and actions on the trailing side, as players expect ([HIG: Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls)). On the inner display held wide, that line is the fold. `TouchZones` puts the fold's whole frame between the zones, flat or folded, so folding moves nothing.

```swift
import SwiftUI

// requires: FoldGeometry (references/fold-geometry.md)

/// Movement on the leading side of the fold, actions on the trailing side.
/// Without a top-to-bottom fold the line is the middle. The fold's frame, margins
/// included, belongs to neither zone, flat or folded, so folding moves nothing.
@available(iOS 27.1, *)
nonisolated struct TouchZones: Equatable, Sendable {
    var move: CGRect
    var act: CGRect

    init(size: CGSize, fold: FoldGeometry) {
        let gap = fold.isVertical ? fold.frame : nil
        let lead = gap?.minX ?? size.width / 2
        let trail = gap?.maxX ?? size.width / 2
        move = CGRect(x: 0, y: 0, width: lead, height: size.height)
        act = CGRect(x: trail, y: 0, width: size.width - trail, height: size.height)
    }
}
```

- *Measured* in book: movement 0 to 455.5 pt, actions 495.5 to 951 pt. Closed, the line is the middle of the 382 pt control area; in tabletop, the middle of the bottom region.
- *Measured* by UI test: in book, a drag from x = 445 pt moved the stick and a drag from the fold's centre did nothing; fire and the stick worked closed, in book and in tabletop.
- Show the stick where the thumb lands, not at a fixed spot. Buttons at least 44 × 44 pt, with a pressed look, a haptic and a symbol that says what they do ([HIG: Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls)).
- Read the fold in the controls' own view. Frames are in that view's space ([`ReservedRegion`](https://developer.apple.com/documentation/swiftui/reservedregion)).
- *Measured:* the first layout pass reported no fold. The zones then split at the middle for one pass. React to changes; don't read once.

`TouchControls` (stick and fire button) and `PressButton`, plus Apple's `GCVirtualController` and Touch Controller on iPhone Duo: [references/touch-controls.md](references/touch-controls.md).

## 4. Tabletop: the bottom half is the controller

Propped on a table, the phone becomes a small console: the world in the top region, every control in the bottom region. In every other pose the controls lie over the world. One `Layout` does both, so neither view is rebuilt ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=263)).

- *Measured:* tabletop gave the scene 669 × 455.7 pt above the fold and the controls 669 × 421.5 pt below it.
- Without this layout, the play area crossed the fold in tabletop (*measured* with `GCVirtualController` over a full-window scene).
- The inner camera sits on the right edge of the bottom region (`duo-postures`). It is inactive unless your game runs it. Keep the fire button clear of it anyway.
- Held tall and flat (no active fold), the layout keeps the overlay.

`GameLayout` and its variants: [references/tabletop-controller.md](references/tabletop-controller.md).

## 5. Metal and UIKit

- `MTKView` resizes its drawable with the view by default ([`autoResizeDrawable`](https://developer.apple.com/documentation/metalkit/mtkview/autoresizedrawable)). Rebuild the projection in [`mtkView(_:drawableSizeWillChange:)`](https://developer.apple.com/documentation/metalkit/mtkviewdelegate/mtkview(_:drawablesizewillchange:)). Keep the device, queue, pipelines and game state.
- *Measured:* the drawable went from 1398 × 2034 px closed to 2853 × 2007 px open and 2007 × 2853 px in tabletop. Folding into book didn't call it: the size didn't change.
- UIKit loop: get the display link from `UIWindowScene.displayLink(target:selector:)` (iOS 27). Apple's doc says it follows the scene when the scene moves to another display, as it does when the phone opens or closes ([doc](https://developer.apple.com/documentation/uikit/uiwindowscene/displaylink(target:selector:))). `UIScreen`'s display link is deprecated in iOS 27.

Code for `MTKView`, a `CAMetalLayer` view controller and Touch Controller: [references/scene-and-renderer.md](references/scene-and-renderer.md).

## 6. Game controllers

`ControllerAware` shows the touch controls until the player uses a controller, then hides them, and brings them back on the next touch. Code: [references/controllers.md](references/controllers.md).

- *Measured:* the iPhone Duo simulator reported a connected controller named "Gamepad" (product category MFi, not attached to the device) shortly after every launch, with no controller on the Mac. A game that hides touch controls as soon as a controller connects would hide them on every simulator run. Wait for input.
- *Measured:* `GCVirtualController` drew its stick bottom left and its buttons bottom right in book, clear of the fold. In tabletop its buttons sat below the fold. It doesn't know about the fold; check it in every pose.
- *Measured:* `TCTouchController.isSupported` was `false` on the simulator. Test Apple's Touch Controller on a device.

## 7. Orientation locks

The outer display honours your supported orientations; the inner display doesn't ([talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=222)). Apple lets games lock to portrait or landscape, as long as they fill the screen as the pose changes ([HIG: iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)).

- *Measured* with a landscape-only build: on the closed phone held upright the game ran sideways (678 × 466 pt), as on any iPhone. In tabletop it got a tall 669 × 951 pt window, lock or not.
- So build every screen for both shapes, even with a lock. The play area and `GameLayout` above already do.
- Never read `UIDevice.orientation` or the interface orientation to choose a layout. Use the view's size.

What a landscape-only build got in each pose: [references/measurements.md](references/measurements.md#landscape-only-build).

## 8. Two players on one phone

Use the two-player frame, not this skill's controls:

- [`recipe-two-player-game`](https://github.com/Kimeur/duology/blob/main/plugins/duology-recipes/skills/recipe-two-player-game/SKILL.md) creates a new project: one half per player in every pose, an engine tested on the Mac, and UI tests for the Duo simulator.
- [`duo-shared-screen`](https://github.com/Kimeur/duology/blob/main/plugins/duology-design/skills/duo-shared-screen/SKILL.md) adds the same to an existing game: `SharedSplit`, face-to-face seating, input gated per seat.
- Not `ArrangementView`: closed and held sideways it shows only its first view (*measured* in `duo-layout`).
- Two controllers: give each player one, by `playerIndex`, and keep touch for both. [references/controllers.md](references/controllers.md#two-controllers).

## Frame rate, system gestures and haptics

- Ask for 120 frames per second (`preferredFramesPerSecond`), and add `CADisableMinimumFrameDurationOnPhone` to Info.plist, or iPhone stays at 60 ([ProMotion guide](https://developer.apple.com/documentation/quartzcore/optimizing-iphone-and-ipad-apps-to-support-promotion-displays)). The simulator ran at 60 (*measured*: 300 frames every 5 s). Check 120 Hz on a device.
- Controls near an edge: `defersSystemGestures(on:)` during play, so a swipe that starts at that edge reaches the game before the system ([doc](https://developer.apple.com/documentation/swiftui/view/deferssystemgestures(on:))).
- Haptics shake the whole phone. Keep them short, and offer a switch ([HIG: Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)).

## Test it

In Device Hub, under the bezel: Closed, Open, Partially Open, and Rotate Right for tabletop ([Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)).

1. Start a round closed. Open, fold, rotate into tabletop and close while it plays. The round never restarts, and the score and positions stay.
2. Book: no stick, button or menu inside the fold frame (455.5 to 495.5 pt held wide).
3. Tabletop: the world above the fold, every control below it.
4. Every pose: the whole play area shows; nothing is cut off and no plain black bars appear.
5. Controller: touch controls stay visible until you press a button, and come back on touch. On the simulator, expect the "Gamepad" controller to be connected already.
6. Split View on the inner display, on both sides: the game fills its half.
7. Screenshots: `xcrun simctl io <UDID> screenshot --display=primary outer.png` (closed) and `--display=primary-1 inner.png` (open).

## Checklist

- [ ] The scene uses `.resizeFill` (or the renderer follows the drawable size); nothing letterboxes without artwork.
- [ ] A camera or projection keeps the whole play area visible at every aspect ratio.
- [ ] Score, menus and touch controls are sized in points, outside the world, and keep their size in every pose.
- [ ] One session, scene and renderer per window, created above the layout; nothing is rebuilt on a fold.
- [ ] Size callbacks are cheap, repeatable and never reset game state.
- [ ] Touch zones split at the `.division` frame read with `.includeInactive`; no control inside it, flat or folded.
- [ ] Tabletop: the world above the fold, the same controls below it.
- [ ] The game pauses on `scenePhase` by setting the scene's `isPaused`, never on a fold.
- [ ] Touch controls stay until a controller is used, and come back on touch.
- [ ] The game works tall and wide on the inner display, whatever orientation it locks.
- [ ] Two players use `recipe-two-player-game` or `duo-shared-screen`, not `ArrangementView`.
- [ ] iOS 27.1 APIs are behind `@available` or `if #available` when the game deploys lower.
- [ ] Checked in Device Hub: Closed (portrait and landscape), Open (wide and tall), book, tabletop, Split View.
