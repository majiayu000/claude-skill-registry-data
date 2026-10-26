---
name: duo-media
description: "Video and audio playback on iPhone Duo, Apple's foldable. Use when an app plays video or audio and must keep playing through fold, unfold and rotation, when you build a tabletop player (video above the fold, the same controls below) or a book-pose player, an up next queue, Picture in Picture, Now Playing or background audio. Covers one AVPlayer owned above the layout switch (VideoPlayer, AVPlayerViewController, AVPlayerLayer), ArrangementView with .overlay and overlayArrangementZIndex for up next (measured on the simulator in every pose), when to pick .split instead, toolbarVerticalBehavior(.disabled) for a full-screen player, AVPictureInPictureController and canStartPictureInPictureAutomaticallyFromInline, the pinned Picture in Picture video that takes half the screen when folded, MPNowPlayingSession and remote commands, the .playback audio session, and what to test in Device Hub and on a device."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-media

People open, close and fold iPhone Duo while something plays. The video must not stop, restart or flash, and the controls must land where hands can reach them in every pose. This skill covers players, the tabletop layout, "up next", Picture in Picture, Now Playing and the audio session.

Load neighbours when the task needs them: `duo-continuity` (where state lives, for every kind of state), `duo-postures` (every pose, and the tabletop recipe with `FoldRegionsLayout`), `duo-layout` (`ArrangementView` in depth), `duo-scenes` (Split View and windows), `duo-camera` (capture).

"Tabletop" and "book" are Duology's words for what Apple describes as the phone seated on a table like a laptop, and partly folded like a book. Neither is an API. Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1); *derived* means reasoning from Apple's words or our measurements; *unverified* means we could not check it. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Rules

1. One `AVPlayer` per window, in a model owned above every layout switch. Views only show it.
2. Never pause, reload or reset playback because of a fold, a resize or `onDisappear`.
3. Start with the system player. Use your own controls when you want them below the fold in tabletop, and then bring back what the system player gave you.
4. Tabletop: the video in the top region, the same controls in the bottom region. Book: the video leading, the controls trailing. No control exists only when folded.
5. "Up next" that floats over the video: an overlay arrangement. "Up next" that must never be covered: a split.
6. Support Picture in Picture. Expect your window to get shorter when a video is pinned on top, and shorter still when the phone is partly folded.
7. Own the audio session and Now Playing in the model, not in views.
8. A full-screen player turns the vertical bar off with `toolbarVerticalBehavior(.disabled)`, as a fixed choice for that screen.
9. Folding is not a request to play. Never start playback because the phone folded or opened.

## 1. One player above the layout switch

A fold resizes the window, often changes its size class, and rebuilds the views below a layout switch. A player created in one of those views starts again from zero ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=135), `duo-continuity`).

```swift
import AVKit
import SwiftUI

// requires: PlaybackModel (references/player-ownership.md)

struct PlayerRoot: View {
    @State private var playback = PlaybackModel()     // the window root owns the player

    var body: some View {
        VideoPlayer(player: playback.player)           // a view of the player, nothing more
            .ignoresSafeArea()
    }
}
```

- `PlaybackModel` holds the player, the queue, Picture in Picture and Now Playing. Its `play(_:)` ignores the item already playing, so a view that calls it again after a fold restarts nothing.
- `AVPlayer` is main-actor isolated in the iOS 27.1 SDK (`AVPlayer.h`), so the model is `@MainActor`.
- *Measured* (20 Oct 2026): a model-owned player kept playing through book, tabletop and closing, and its `AVPlayerLayer` view was created once. `duo-continuity` measured the same with `VideoPlayer` rebuilt on each flip.

The model, the root, what to avoid, and UIKit: [references/player-ownership.md](references/player-ownership.md).

## 2. System player or your own controls

| | System player (`AVPlayerViewController`, `VideoPlayer`) | Your controls on an `AVPlayerLayer` |
|---|---|---|
| Controls | Drawn over the video | Wherever you put them, below the fold included |
| Picture in Picture | `AVPlayerViewController`: built in once the audio session and background mode are set. Apple's guides don't cover `VideoPlayer`. | `AVPictureInPictureController` |
| Now Playing | `AVPlayerViewController` updates it by default | `MPNowPlayingSession` from your model |
| Captions, AirPlay | In the system controls | Yours to add (`AVRoutePickerView` for AirPlay) |
| Apple's advice | Prefer it ([HIG: Playing video](https://developer.apple.com/design/human-interface-guidelines/playing-video)) | Match the system player's behaviour if you build one |

On Duo the difference is tabletop. The system player draws its controls over the video; Apple's tabletop advice wants them on the bottom half. Whether the system player moves them when the phone is partly folded is not measured yet ([references/testing.md](references/testing.md#the-system-player-in-each-pose)).

## 3. Tabletop and book

Apple names one optional layout for a single pose: the phone on a table, media in the top region, tappable controls on the stable bottom region, with the same controls and hierarchy as every other pose ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=283), [Tech Talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=263)).

An `ArrangementView` with `.overlay` does it with no fold code. *Measured* on the simulator (20 Oct 2026):

| Pose | Window | Primary (controls, up next) | Secondary (video) | `overlayArrangementZIndex` read in the primary |
|---|---|---|---|---|
| Closed | 466 × 678 pt | Floats over the video, whole window | Whole window | 1 |
| Open, flat | 951 × 669 pt | Floats over the video, whole window | Whole window | 1 |
| Book | 951 × 669 pt | Trailing region, 455 pt wide | Leading region | 0 |
| Tabletop | 669 × 951 pt | Bottom region, 455 pt tall | Top region | 0 |

```swift
import AVKit
import SwiftUI

// requires: PlaybackModel (references/player-ownership.md)
// requires: NowPlayingPanel, VideoSurface (references/tabletop-and-up-next.md)

@available(iOS 27.1, *)
struct TabletopWatchScreen: View {
    let playback: PlaybackModel                         // owned by the window root

    var body: some View {
        ArrangementView {
            NowPlayingPanel(playback: playback)          // primary: what people touch
        } secondary: {
            VideoSurface(playback: playback)             // secondary: what people watch
                .ignoresSafeArea()
        }
        .arrangementViewStyle(.overlay)
        .background(.black)
        .toolbarVerticalBehavior(.disabled)              // fixed for this screen, never toggled
    }
}
```

- The primary covers the whole window while it floats. Align its content to the bottom edge.
- Don't put an arrangement inside a `List`, a `ScrollView` or a `NavigationSplitView` ([overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)). Present the player full screen or inside a `NavigationStack`.
- Gate it with `if #available(iOS 27.1, *)` when the app deploys lower. Below 27.1 keep the controls over the video.
- The other way to build it, with placement you control: `FoldRegionsLayout` in [duo-postures](https://github.com/Kimeur/duology/blob/main/plugins/duology-design/skills/duo-postures/references/tabletop-media.md), used by the gallery's [tabletop player screen](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/DuologyGallery/Patterns/TabletopPlayerView.swift). Screenshots of it closed, open, in book and in tabletop: [gallery README](https://github.com/Kimeur/duology/blob/main/samples/DuologyGallery/README.md#screenshots).

## 4. "Up next" as an overlay arrangement

Apple's layouts talk builds exactly this: a player and an "up next" view in an overlay arrangement, with a collapsed "up next" while it floats and an expanded one once the phone folds, switched by `overlayArrangementZIndex` ([Tech Talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=821)).

```swift
import SwiftUI

// requires: PlaybackModel (references/player-ownership.md), UpNextList (references/tabletop-and-up-next.md)

/// Pass this as the arrangement's primary. The view you pass in reads default
/// arrangement values, so read them one view down (duo-layout).
@available(iOS 27.1, *)
struct UpNextPrimary: View {
    let playback: PlaybackModel

    var body: some View {
        ZStack { UpNextPanel(playback: playback) }
    }
}

@available(iOS 27.1, *)
struct UpNextPanel: View {
    let playback: PlaybackModel
    @Environment(\.overlayArrangementZIndex) private var zIndex

    var body: some View {
        // Measured: 1 while floating over the video, 0 once side by side or stacked.
        UpNextList(playback: playback, limit: zIndex > 0 ? 1 : 6)
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottomLeading)
    }
}
```

- Same queue in every pose; only how much of it shows changes.
- Closing from tabletop, the z-index went 1, 0, 1 within 0.06 s (*measured*). Treat it as state; don't run work on every change.
- Choose by the relationship ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=879)): overlay when the video is the background and the queue may cover part of it; split when the queue or a transcript is detail that must never be covered. For an audio app the talk picks split.

The full panel with transport controls, the video surface and UIKit: [references/tabletop-and-up-next.md](references/tabletop-and-up-next.md).

## 5. Picture in Picture

On Duo people can pin a Picture in Picture video to the top of the screen. The app below resizes to the space left, and when the phone is partly folded the pinned video grows to half the screen ([Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=201)).

- Your layout must work in a short, wide window. In tabletop with a pinned video, your app has roughly the bottom half (*derived*).
- For your own video, set `canStartPictureInPictureAutomaticallyFromInline` when it is the main thing on screen, so it floats when people leave the app.
- A fold doesn't send the app to the background (`scenePhase` stayed `active`, `duo-scenes`), so a fold shouldn't start Picture in Picture (*derived*).
- Both need the playback audio category and the "Audio, AirPlay, and Picture in Picture" background mode ([Configuring your app for media playback](https://developer.apple.com/documentation/avfoundation/configuring-your-app-for-media-playback)).
- *Measured:* `isPictureInPictureSupported()` returned `false` on the iPhone Duo simulator. Test it on a device.

Code for a custom player, and what the restore callback needs: [references/pip-and-audio.md](references/pip-and-audio.md).

## 6. Now Playing and the audio session

- Category `.playback`, mode `.moviePlayback` for video. Set it before playback; an `AVPlayer` activates the session itself when it starts (`AVPlayer.h`).
- `AVPlayerViewController` keeps Now Playing up to date by default. With your own controls, use `MPNowPlayingSession(players:)` with `automaticallyPublishesNowPlayingInfo` (iOS 16), from the model.
- After an interruption, resume only when the system recommends it. iOS 27.0 deprecates `interruptionNotification`; read `resumptionRecommendationNotification` instead (`AVAudioSessionTypes.h`). Pause when headphones come out ([HIG: Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio)).
- A fold is neither an interruption nor a route change. Nothing in the audio setup reacts to it.
- No scene accessory is meant for video on the outer display. The SDK has two: the camera capture accessory, for capture, and the external non-interactive accessory, which Apple documents for connected and AirPlay displays (`duo-scenes`). Use AirPlay for a second screen.

Details: [references/pip-and-audio.md](references/pip-and-audio.md#the-audio-session).

## 7. Split View and the closed phone

- Every app takes part in 50/50 Split View on the inner display ([Tech Talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=184)). Your player may get half the display: keep the controls usable at that width.
- Closed, the player gets the compact outer display. Keep the same controls; the overlay arrangement floats them over the video.
- The outer front camera always occludes a corner of the outer display ([overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)). Let the video run under it; keep controls clear of it.

## UIKit

Keep one `AVPlayerViewController` in a container that never goes away ([duo-continuity](https://github.com/Kimeur/duology/blob/main/plugins/duology/skills/duo-continuity/references/uikit.md#players)). For tabletop, `UIArrangementViewController` with `UIOverlayArrangement`: panel in `.primary`, video in `.secondary`, and `state(for: .primary)?.zIndex` to switch the panel. Details: [references/tabletop-and-up-next.md](references/tabletop-and-up-next.md#uikit).

## Test it

1. In Device Hub, start playback, then press Closed, Open and Partially Open, and Rotate Right for tabletop. `duo-pose` from [duo-pose-matrix](https://github.com/Kimeur/duology/blob/main/plugins/duology-ship/skills/duo-pose-matrix/SKILL.md) presses them for you if the user has given Accessibility permission.
2. After each pose: the time keeps counting, the video doesn't flash, the controls sit where the table in section 3 says, nothing interactive sits in the fold.
3. Split View on each side, with Reduce Motion on, with VoiceOver reading each control.
4. On a device: Picture in Picture (inline start, pinned, folded to half the screen), Now Playing on the Lock Screen and in Control Center, headphones out, a call coming in.

What we measured, how, and a device checklist: [references/testing.md](references/testing.md).

## Checklist

- [ ] One `AVPlayer` per window, created in a model the window root owns.
- [ ] No pause, reload or seek in `onDisappear`, `onAppear`, a size-class change or a fold.
- [ ] Playing state comes from the player (`timeControlStatus`), not a flag in a view.
- [ ] Tabletop puts the video on top and every control below; book puts the video leading and the controls trailing.
- [ ] No control exists only in one pose.
- [ ] "Up next" reads `overlayArrangementZIndex` one view down, or uses a split when it must never be covered.
- [ ] No arrangement inside a `List`, `ScrollView` or `NavigationSplitView`; iOS 27.1 APIs gated when the app deploys lower.
- [ ] A full-screen player sets `toolbarVerticalBehavior(.disabled)` once, not from view state.
- [ ] Picture in Picture works for the player you use, starts automatically from inline when the video is the main content, and the app copes with a shorter window.
- [ ] Audio category `.playback`, the background mode set, Now Playing published from the model.
- [ ] Playback never starts because the phone folded or opened.
- [ ] Checked in Device Hub in every pose and in Split View; Picture in Picture and Now Playing checked on a device.
