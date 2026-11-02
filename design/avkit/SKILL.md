---
name: avkit
description: "Create media playback experiences using AVKit. Use when adding video players with AVPlayerViewController, enabling Picture-in-Picture, routing media with AirPlay, using SwiftUI VideoPlayer views, configuring transport controls, displaying subtitles and closed captions, or integrating AVFoundation playback with system UI."
---

# AVKit

High-level media playback UI built on AVFoundation. Provides system-standard
video players, Picture-in-Picture, AirPlay routing, transport controls, and
subtitle/caption display. Targets Swift 6.3 / iOS 26+.

## Contents

- [Setup](#setup)
- [AVPlayerViewController](#avplayerviewcontroller)
- [SwiftUI VideoPlayer](#swiftui-videoplayer)
- [Picture-in-Picture](#picture-in-picture)
- [AirPlay](#airplay)
- [Transport Controls and Playback Speed](#transport-controls-and-playback-speed)
- [Subtitles and Closed Captions](#subtitles-and-closed-captions)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Audio Session Configuration

Configure the audio session and background modes before any playback. Without
this, PiP and background audio fail silently.

1. Add the `audio` background mode to `UIBackgroundModes` in Info.plist
2. Set the audio session category to `.playback`

```swift
import AVFoundation

func configureAudioSession() {
    let session = AVAudioSession.sharedInstance()
    do {
        try session.setCategory(.playback, mode: .moviePlayback)
        try session.setActive(true)
    } catch {
        print("Audio session configuration failed: \(error)")
    }
}
```

### Imports

```swift
import AVKit          // AVPlayerViewController, VideoPlayer, PiP
import AVFoundation   // AVPlayer, AVPlayerItem, AVAsset
```

## AVPlayerViewController

`AVPlayerViewController` is the standard UIKit player. It provides system
playback controls, PiP, AirPlay, subtitles, and frame analysis out of the box.
Do not subclass it.

### Basic Presentation (Full Screen)

```swift
import AVKit

func presentPlayer(from viewController: UIViewController, url: URL) {
    let player = AVPlayer(url: url)
    let playerVC = AVPlayerViewController()
    playerVC.player = player

    viewController.present(playerVC, animated: true) {
        player.play()
    }
}
```

### Inline (Embedded) Playback

Add `AVPlayerViewController` as a child view controller for inline playback.
Call `addChild`, add the view with constraints, then call `didMove(toParent:)`.

```swift
func embedPlayer(in parent: UIViewController, container: UIView, url: URL) {
    let playerVC = AVPlayerViewController()
    playerVC.player = AVPlayer(url: url)

    parent.addChild(playerVC)
    container.addSubview(playerVC.view)
    playerVC.view.translatesAutoresizingMaskIntoConstraints = false
    NSLayoutConstraint.activate([
        playerVC.view.leadingAnchor.constraint(equalTo: container.leadingAnchor),
        playerVC.view.trailingAnchor.constraint(equalTo: container.trailingAnchor),
        playerVC.view.topAnchor.constraint(equalTo: container.topAnchor),
        playerVC.view.bottomAnchor.constraint(equalTo: container.bottomAnchor)
    ])
    playerVC.didMove(toParent: parent)
}
```

### Key Properties

```swift
playerVC.showsPlaybackControls = true                    // Show/hide system controls
playerVC.videoGravity = .resizeAspect                    // .resizeAspectFill to crop
playerVC.entersFullScreenWhenPlaybackBegins = false
playerVC.exitsFullScreenWhenPlaybackEnds = true
playerVC.updatesNowPlayingInfoCenter = true              // Auto-updates MPNowPlayingInfoCenter
```

Use `contentOverlayView` to add non-interactive views (watermarks, logos)
between the video and transport controls.

### Delegate

Adopt `AVPlayerViewControllerDelegate` to respond to full-screen transitions,
PiP lifecycle events, interstitial playback, and media selection changes.
Use the transition coordinator's `animate(alongsideTransition:completion:)` to
synchronize your UI with full-screen animations.

### Display Readiness

Observe `isReadyForDisplay` before showing the player to avoid a black flash:

```swift
let observation = playerVC.observe(\.isReadyForDisplay) { observed, _ in
    if observed.isReadyForDisplay {
        // Safe to show the player view
    }
}
```

## SwiftUI VideoPlayer

The `VideoPlayer` SwiftUI view wraps AVKit's playback UI.

### Basic Usage

```swift
import SwiftUI
import AVKit

struct PlayerView: View {
    @State private var player: AVPlayer?

    var body: some View {
        Group {
            if let player {
                VideoPlayer(player: player)
                    .frame(height: 300)
            } else {
                ProgressView()
            }
        }
        .task {
            let url = URL(string: "https://example.com/video.m3u8")!
            player = AVPlayer(url: url)
        }
    }
}
```

### Video Overlay

Add a non-interactive SwiftUI overlay on top of video content.

```swift
VideoPlayer(player: player) {
    VStack {
        Spacer()
        HStack {
            Image("logo")
                .resizable()
                .frame(width: 40, height: 40)
                .padding()
            Spacer()
        }
    }
}
```

### UIKit Hosting for Advanced Control

`VideoPlayer` does not expose all `AVPlayerViewController` properties. For PiP
configuration, delegate callbacks, or playback speed control, wrap
`AVPlayerViewController` in a `UIViewControllerRepresentable`. See the full
pattern in [references/avkit-patterns.md](references/avkit-patterns.md).

## Picture-in-Picture

PiP lets users watch video in a floating window while using other apps.
`AVPlayerViewController` supports PiP automatically once the audio session is
configured. For custom player UIs, use `AVPictureInPictureController` directly.

### Prerequisites

1. Audio session category set to `.playback` (see [Setup](#setup))
2. `audio` background mode in `UIBackgroundModes`

### Standard Player PiP

PiP is enabled by default on `AVPlayerViewController`. Control automatic
activation and inline-to-PiP transitions:

```swift
let playerVC = AVPlayerViewController()
playerVC.player = player

// PiP enabled by default; set false to disable
playerVC.allowsPictureInPicturePlayback = true

// Auto-start PiP when app backgrounds (for inline/non-fullscreen players)
playerVC.canStartPictureInPictureAutomaticallyFromInline = true
```

### Restoring the UI When PiP Stops

When the user taps the restore button in PiP, implement the delegate method to
re-present your player. Call the completion handler with `true` to signal the
system to finish the restore animation.

```swift
func playerViewController(
    _ playerViewController: AVPlayerViewController,
    restoreUserInterfaceForPictureInPictureStopWithCompletionHandler completionHandler: @escaping (Bool) -> Void
) {
    // Re-present or re-embed the player view controller
    present(playerViewController, animated: false) {
        completionHandler(true)
    }
}
```

### Custom Player PiP

For custom player UIs, use `AVPictureInPictureController` with an `AVPlayerLayer`
or sample buffer content source. Check `isPictureInPictureSupported()` first.
See [references/avkit-patterns.md](references/avkit-patterns.md) for full custom player and sample buffer
PiP patterns.

```swift
guard AVPictureInPictureController.isPictureInPictureSupported() else { return }
let pipController = AVPictureInPictureController(playerLayer: playerLayer)
pipController.delegate = self
pipController.canStartPictureInPictureAutomaticallyFromInline = true
```

### Linear Playback During Ads

Prevent seeking during ads or legal notices by toggling `requiresLinearPlayback`:

```swift
// During an ad
playerVC.requiresLinearPlayback = true

// After the ad completes
playerVC.requiresLinearPlayback = false
```

## AirPlay

`AVPlayerViewController` supports AirPlay automatically. No additional code is
required when using the standard player. The system displays the AirPlay button
in the transport controls when AirPlay-capable devices are available.

### AVRoutePickerView

Add a standalone AirPlay route picker button outside the player UI:

```swift
import AVKit

func addRoutePicker(to containerView: UIView) {
    let routePicker = AVRoutePickerView(frame: CGRect(x: 0, y: 0, width: 44, height: 44))
    routePicker.activeTintColor = .systemBlue
    routePicker.prioritizesVideoDevices = true  // Show video-capable routes first
    containerView.addSubview(routePicker)
}
```

### Enabling External Playback

Ensure `AVPlayer` allows external playback (enabled by default):

```swift
player.allowsExternalPlayback = true
player.usesExternalPlaybackWhileExternalScreenIsActive = true
```

## Transport Controls and Playback Speed

### Custom Playback Speeds

Provide user-selectable playback speeds in the player UI:

```swift
let playerVC = AVPlayerViewController()
playerVC.speeds = [
    AVPlaybackSpeed(rate: 0.5, localizedName: "Half Speed"),
    AVPlaybackSpeed(rate: 1.0, localizedName: "Normal"),
    AVPlaybackSpeed(rate: 1.5, localizedName: "1.5x"),
    AVPlaybackSpeed(rate: 2.0, localizedName: "Double Speed")
]
```

Use `AVPlaybackSpeed.systemDefaultSpeeds` to restore the default speed options.

### Skipping Behavior

Configure forward/backward skip controls:

```swift
playerVC.isSkipForwardEnabled = true
playerVC.isSkipBackwardEnabled = true
```

### Now Playing Integration

`AVPlayerViewController` updates `MPNowPlayingInfoCenter` automatically by
default. Disable this if you manage Now Playing info manually:

```swift
playerVC.updatesNowPlayingInfoCenter = false
```

## Subtitles and Closed Captions

AVKit handles subtitle and closed caption display automatically when the media
contains appropriate text tracks. Users control subtitle preferences in
Settings > Accessibility > Subtitles & Captioning.

### Restricting Subtitle Languages

```swift
// Only show English and Spanish subtitle options
playerVC.allowedSubtitleOptionLanguages = ["en", "es"]
```

### Requiring Subtitles

Force subtitles to always display (the user cannot turn them off):

```swift
playerVC.requiresFullSubtitles = true
```

### Media Selection (Delegate)

Respond to the user changing subtitle or audio track selection:

```swift
func playerViewController(
    _ playerViewController: AVPlayerViewController,
    didSelect mediaSelectionOption: AVMediaSelectionOption?,
    in mediaSelectionGroup: AVMediaSelectionGroup
) {
    if let option = mediaSelectionOption {
        print("Selected: \(option.displayName)")
    }
}
```

### Providing Subtitle Tracks in HLS

Subtitles and closed captions are embedded in HLS manifests. AVKit reads them
from `AVMediaSelectionGroup` on the `AVAsset`. For local files, use
`AVMutableComposition` to add `AVMediaCharacteristic.legible` tracks.

## Common Mistakes

### DON'T: Subclass AVPlayerViewController

Apple explicitly states this is unsupported. It may cause undefined behavior or
crash on future OS versions.

```swift
// WRONG
class MyPlayerVC: AVPlayerViewController { } // Unsupported

// CORRECT: Use composition with delegation
let playerVC = AVPlayerViewController()
playerVC.delegate = coordinator
```

### DON'T: Skip audio session configuration for PiP

PiP fails silently if the audio session is not set to `.playback`. Background
audio also stops working.

```swift
// WRONG: Default audio session
let playerVC = AVPlayerViewController()
playerVC.player = player // PiP won't work

// CORRECT: Configure audio session first
try AVAudioSession.sharedInstance().setCategory(.playback, mode: .moviePlayback)
try AVAudioSession.sharedInstance().setActive(true)
let playerVC = AVPlayerViewController()
playerVC.player = player
```

### DON'T: Forget the PiP restore delegate or its completion handler

Without `restoreUserInterfaceForPictureInPictureStopWithCompletionHandler`, the
system cannot return the user to your player. Failing to call
`completionHandler(true)` leaves the system in an inconsistent state.

```swift
// WRONG: No delegate method or missing completionHandler call
// User taps restore in PiP -> nothing happens or animation hangs

// CORRECT
func playerViewController(
    _ playerViewController: AVPlayerViewController,
    restoreUserInterfaceForPictureInPictureStopWithCompletionHandler completionHandler: @escaping (Bool) -> Void
) {
    present(playerViewController, animated: false) {
        completionHandler(true)
    }
}
```

### DON'T: Create AVPlayer in a SwiftUI view's init

Creating the player eagerly causes performance issues. SwiftUI may recreate the
view multiple times.

```swift
// WRONG: Created on every view init
struct PlayerView: View {
    let player = AVPlayer(url: videoURL) // Re-created on every view evaluation

    var body: some View { VideoPlayer(player: player) }
}

// CORRECT: Use @State and defer creation
struct PlayerView: View {
    @State private var player: AVPlayer?

    var body: some View {
        VideoPlayer(player: player)
            .task { player = AVPlayer(url: videoURL) }
    }
}
```

## Review Checklist

- [ ] Audio session category set to `.playback` with `mode: .moviePlayback`
- [ ] `audio` background mode added to `UIBackgroundModes` in Info.plist
- [ ] `AVPlayerViewController` is not subclassed
- [ ] PiP restore delegate method implemented and calls `completionHandler(true)`
- [ ] `AVPlayer` deferred to `.task` in SwiftUI (not created eagerly)
- [ ] `canStartPictureInPictureAutomaticallyFromInline` set for inline players
- [ ] `requiresLinearPlayback` toggled only during required ad/legal segments
- [ ] `allowsExternalPlayback` enabled on `AVPlayer` for AirPlay support
- [ ] Subtitle language restrictions tested with actual media tracks
- [ ] Video gravity set appropriately (`.resizeAspect` vs `.resizeAspectFill`)
- [ ] `isReadyForDisplay` observed before showing the player view
- [ ] Error handling for network-streamed content (HLS failures, timeouts)

## References

- Advanced patterns (custom player UI, interstitials, background playback, error handling): [references/avkit-patterns.md](references/avkit-patterns.md)
- [AVKit framework](https://sosumi.ai/documentation/avkit)
- [AVPlayerViewController](https://sosumi.ai/documentation/avkit/avplayerviewcontroller)
- [VideoPlayer (SwiftUI)](https://sosumi.ai/documentation/avkit/videoplayer)
- [AVPictureInPictureController](https://sosumi.ai/documentation/avkit/avpictureinpicturecontroller)
- [AVRoutePickerView](https://sosumi.ai/documentation/avkit/avroutepickerview)
- [AVPlaybackSpeed](https://sosumi.ai/documentation/avkit/avplaybackspeed)
- [Configuring your app for media playback](https://sosumi.ai/documentation/avfoundation/configuring-your-app-for-media-playback)
- [Adopting Picture in Picture in a Standard Player](https://sosumi.ai/documentation/avkit/adopting-picture-in-picture-in-a-standard-player)
- [Playing video content in a standard user interface](https://sosumi.ai/documentation/avkit/playing-video-content-in-a-standard-user-interface)
