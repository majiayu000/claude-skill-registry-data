---
name: duo-camera
description: "Camera capture on iPhone Duo, Apple's foldable. Use when an app takes photos or video, runs a video call or shows a camera preview, and must work closed (outer display), open (inner display), partly folded (book, tabletop), open and turned around (flipped) and through fold and unfold. Covers the virtual front camera (.builtInWideAngleCamera or .builtInUltraWideCamera at .front; shared features only, up to 1080p at 60 fps, no depth), the physical front cameras (.builtInOuterUltraWideCamera, .builtInInnerUltraWideCamera), choosing a camera by the way it faces with AVCaptureDeviceDirectionCoordinator (AVKit) and AVCaptureDeviceDescriptor, mirroring a rear-camera selfie, AVCaptureDevice.RotationCoordinator across displays, the square front sensor and dynamicAspectRatio, a subject preview on the outer display with CameraCaptureAccessory, tabletop hands-free capture, and Split View interruptions. The simulator has no camera: the code typechecks; capture is unverified on a device."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-camera

iPhone Duo has a front camera above each display, rear cameras, and a hinge that turns them around. Which way a camera points depends on the display your app is on. This skill tells you which camera to use, how to follow it through a fold, and how to lay out capture for each pose.

Load neighbours when the task needs them: `duo-scenes` (the camera capture accessory's lifecycle and UIKit registration), `duo-postures` (tabletop and flipped layouts), `duo-layout` (reserved regions, including the inner camera's occlusion), `duo-continuity` (state through a fold).

> **No camera in the simulator.** The iPhone Duo simulator has no camera. *Measured* (20 Oct 2026): every discovery session returned no device, and a direction coordinator kept an empty map and never called its handler (we watched for up to 2 minutes). So every capture behaviour in this skill comes from Apple's pages and is unverified on a device. All Swift code here typechecks against the iOS 27.1 SDK; none of it has run with a real camera.

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1). *Derived* means reasoning from Apple's numbers or our measurements. *Unverified* means we could not check it. Everything else comes from Apple, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## Rules

1. Start with the virtual front camera. Front-camera code you already have works on Duo unchanged.
2. Use the physical cameras only when capture is the app's main job, or when you need what one camera alone has: 4K or 120 fps on the outer camera, depth, a rear-camera selfie.
3. With physical cameras, ask `AVCaptureDeviceDirectionCoordinator` which way each one faces. Never infer it from `position` or the device type.
4. One coordinator per preview view. A preview on each display needs one each.
5. No AVFoundation calls in the coordinator's handler. Hand the descriptor to the actor that owns the session.
6. Mirror by direction: mirror a rear camera that faces the person; don't mirror a front camera that faces away.
7. Make a new rotation coordinator after every camera switch. Then turn off sensor orientation compensation.
8. Keep the shutter and every control out of the fold and away from the inner camera, which occludes the view while it runs.
9. The app works without the outer-display accessory, in Split View, and on iPhones with one display.

## 1. The cameras

| Camera | How to get it | Faces | What it gives you |
|---|---|---|---|
| Virtual front camera | `.builtInWideAngleCamera` or `.builtInUltraWideCamera` at `.front`. `isVirtualDevice` is `true`. | The display your app is on: inner when open, outer when closed | Only what both front cameras share: up to 1080p at 60 fps, no depth. The system switches for you ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=148)). |
| Outer front | `.builtInOuterUltraWideCamera` | The same way as the outer display | Square sensor. Up to 4K and 120 fps per the talk; Apple's [spec page](https://www.apple.com/iphone-duo/specs/) lists 4K up to 60 fps and 120 fps slo-mo at 1080p. |
| Inner front | `.builtInInnerUltraWideCamera` | The same way as the inner display. Under the display, hidden until it runs. | Square sensor, 1080p up to 60 fps ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=130)) |
| Rear | Your usual rear types, `position == .back` | Away from the person on the inner display; toward them when the phone is turned around | As on other iPhones |

- Depth comes only through the physical cameras ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=160)). Check a format's `supportedDepthDataFormats` before you rely on it.
- Both physical front cameras report `position == .front`. That is where a camera sits, not where it points ([guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces)).
- `AVCaptureDevice.h` says the outer and inner types can only be discovered with a discovery session, so use one rather than `AVCaptureDevice.default(_:for:position:)`. Both are iOS 27.1 and unavailable on Mac Catalyst.
- The talk and the spec page disagree on the outer camera's frame rate. Read `formats` at run time; never hard-code either number. Helpers: [references/cameras.md](references/cameras.md).

## 2. Virtual front camera or physical cameras

| The app is | Use |
|---|---|
| A video call, a social selfie, a face scan, any app that already uses the front camera | The virtual front camera |
| A camera app, or anything that needs 4K or 120 fps on the outer camera, depth, or a rear-camera selfie | The physical cameras, with a direction coordinator |

The virtual front camera is the discovery you already write. It streams from the camera above the display your app is on, and follows it when the phone opens or closes ([guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces)).

```swift
import AVFoundation

/// The front camera most apps ask for. On iPhone Duo it is the virtual front camera.
func usualFrontCamera() -> AVCaptureDevice? {
    AVCaptureDevice.DiscoverySession(
        deviceTypes: [.builtInWideAngleCamera, .builtInUltraWideCamera],
        mediaType: .video, position: .front
    ).devices.first      // nil in the simulator
}
```

Read `activePrimaryConstituent` to see which physical camera streams; it is `nil` until the session runs. Code that already handles the dual camera handles this virtual device too.

## 3. Follow the direction (physical cameras)

`AVCaptureDeviceDirectionCoordinator` lives in **AVKit**, not AVFoundation. It takes the view that shows your preview as its frame of reference and sorts the cameras you list into forward facing (the same way as that view) and backward facing ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=231)).

| Your preview view is on | Forward facing | Backward facing |
|---|---|---|
| The outer display, phone closed | Outer front | Rear |
| The inner display, phone open | Inner front | Outer front, rear |
| The outer display, phone open and turned around | Rear, outer front | Apple doesn't say |
| Both displays at once (accessory) | Each view's own coordinator: the rear cameras face forward from the outer view and backward from the inner view | |

Source: [talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=253). Apple doesn't say where the inner camera lands while the phone is closed.

```swift
import AVKit
import UIKit

// requires: CaptureService (references/direction-and-mirroring.md)

#if !targetEnvironment(macCatalyst)   // the outer and inner types don't exist there
@available(iOS 27.1, *)
@MainActor
final class FrontCameraFollower {
    private let capture: CaptureService
    private var coordinator: AVCaptureDeviceDirectionCoordinator?
    private(set) var cameraID: String?

    init(capture: CaptureService) { self.capture = capture }

    /// Call once the preview view exists. Keep this object while the view is on screen.
    func follow(_ previewView: UIView) {
        coordinator = AVCaptureDeviceDirectionCoordinator(
            view: previewView,
            // Both physical front cameras, never the virtual one, plus the rear camera.
            deviceTypes: [.builtInOuterUltraWideCamera, .builtInInnerUltraWideCamera, .builtInDualWideCamera]
        ) { [weak self] map in
            self?.directionsChanged(map)      // main queue; no AVFoundation calls here
        }
    }

    private func directionsChanged(_ map: AVCaptureDeviceDirectionMap) {
        let forward = map.forwardFacingDeviceDescriptors
        if let cameraID, forward.contains(where: { $0.uniqueID == cameraID }) { return }
        guard let next = forward.first(where: { $0.position == .front }) ?? forward.first else { return }
        cameraID = next.uniqueID
        Task { await capture.useCamera(withID: next.uniqueID) }   // descriptors are Sendable
    }
}
#endif
```

What to know:

- The handler runs on the main queue, soon after you create the coordinator and again on every change. `deviceDirections` is empty until that first call (`AVCaptureDeviceDirectionCoordinator.h`).
- List every built-in camera you capture from, rear ones included. The coordinator ignores the virtual front camera, so list the two physical front cameras instead ([guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces)).
- A descriptor names a camera; it doesn't reserve it. `AVCaptureDevice(uniqueID:)` can return `nil` by the time your actor runs. Handle that.
- Reconfigure one video input. Don't run both cameras in a multi-camera session for this (guide).
- Frames from the old camera reach the screen while the new one starts. Cover the preview when the handler fires; uncover it when the switch is done.

Full code: the capture actor, a watcher that prefers a rear camera when the person asks, and the UIKit wiring: [references/direction-and-mirroring.md](references/direction-and-mirroring.md).

## 4. Mirror by direction

A preview connection mirrors any camera whose `position` is `.front`. On Duo that is wrong twice: a rear camera facing the person should look like a mirror, and a front camera facing away should not ([guide](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces), [talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=394)).

```swift
import AVKit

/// Mirror by where a camera points, not by where it sits.
/// Returns nil when the connection's automatic mirroring is already right.
@available(iOS 27.1, *)
func previewMirroring(for camera: AVCaptureDeviceDescriptor, in map: AVCaptureDeviceDirectionMap) -> Bool? {
    let facesViewer = map.forwardFacingDeviceDescriptors.contains { $0.uniqueID == camera.uniqueID }
    let facesAway = map.backwardFacingDeviceDescriptors.contains { $0.uniqueID == camera.uniqueID }
    if camera.position == .back && facesViewer { return true }    // a rear-camera selfie
    if camera.position == .front && facesAway { return false }    // a front camera looking away
    return nil
}
```

- Set `automaticallyAdjustsVideoMirroring = false` before `isVideoMirrored`. The other order raises an exception.
- Apply it after every map change and after every input change: a new input makes a new preview connection without your setting.
- Apple's guidance covers the preview. Whether saved photos are mirrored is your product choice; keep it the same for every camera.

## 5. Rotation

Adopt `AVCaptureDevice.RotationCoordinator` (iOS 17) for the preview and for captured media. On Duo its angles also change when the app moves to the other display ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=488)).

- A rotation coordinator serves one camera and one preview layer. Make a new one after each switch, and one per preview layer when the subject view shows a second preview.
- Once it runs, set `isCameraSensorOrientationCompensationEnabled` to `false` on `AVCapturePhotoOutput` (iOS 26). It is on for every front camera on Duo and costs performance ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=517)).

Code that observes both angles on the capture actor: [references/rotation-and-preview.md](references/rotation-and-preview.md).

## 6. The preview on each display

- **Rear camera, inner display.** The full field of view leaves space around the preview. Either move the preview to one side and group controls in the space left, or fill the display with `videoGravity = .resizeAspectFill` ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=430)).
- **Front cameras.** Both sensors are square. On the inner display, ask for a landscape frame with `setDynamicAspectRatio(_:completionHandler:)` (iOS 26) when the format supports it, so the preview fills the wide display ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=464), [WWDC26 session 341](https://developer.apple.com/videos/play/wwdc2026/341/)).
- **The inner camera covers the view while it runs.** Its occlusion region turns active ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)). Keep the shutter clear of it: use a system container, or read `.occlusion` regions (`duo-layout`).
- **The outer camera always occludes** a corner of the outer display. Bars already avoid it; your own corner controls must too.
- **Partly folded,** keep controls out of the active `.division` frame. A preview may cross the fold, but nothing people tap.

Measured region frames for the inner camera, and the code: [references/rotation-and-preview.md](references/rotation-and-preview.md#the-preview-and-the-reserved-regions).

## 7. A preview for the subject on the outer display

Fully open, with the rear camera running and your app full screen on the inner display, the system can show your `CameraCaptureAccessory` on the outer display, which faces the subject ([guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo), [talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=300)). `duo-scenes` covers registration, availability and the UIKit version. The camera side:

- Show what the subject needs: a countdown, how much of them the camera sees, a script. Never a control the photographer needs.
- A live preview there is a second `AVCaptureVideoPreviewLayer` on the same session. Give its view its own direction coordinator: from the outer display the rear camera faces forward, so mirror that preview, and leave the photographer's preview unmirrored (talk 111465). *Unverified:* a second preview layer on one session on a device; the AVFoundation header for `deferredStartEnabled` (iOS 26) talks about apps with several preview layers.
- Apple's conditions say fully open. Closed, it goes away (`duo-scenes` measured this). Partly folded is unclear: in the simulator, with no capture session, it was available in book at 128° (*measured*; [references/testing.md](references/testing.md#the-accessory-in-each-pose)). On a device, unverified. Put the countdown in the main UI as well, so it never depends on the accessory.

Code: [references/outer-display-and-tabletop.md](references/outer-display-and-tabletop.md#subject-preview-on-the-outer-display).

## 8. Flipped: a selfie with the rear camera

Open and turned around, the rear cameras and the outer display face the person, and a camera app can move to the outer display. The rear and the outer front cameras then both face forward ([talk 111465](https://developer.apple.com/videos/play/tech-talks/111465/?time=277)).

- Let people pick between the rear camera and the outer front camera. Never decide from `position`.
- Mirror the rear preview (section 4).
- The layout is your compact, closed layout. Device Hub has no flip control, so test it on a device.

## 9. Tabletop: hands-free capture

Apple names one optional layout worth designing for a single pose: the phone seated on a table, good for hands-free use. What people watch goes in the top region, what they tap goes in the bottom region, and every control stays the same as in other poses ([talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=283), [talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=263)). For a camera:

- The preview goes in the top region; shutter, self-timer and mode go in the bottom region.
- Add a self-timer. Show the countdown large on the preview, so it reads from across the table.
- An `ArrangementView` with `.overlay` does this with no fold code. *Measured* with a video in its place (20 Oct 2026): flat or closed, the primary view floated over the secondary; in tabletop the primary took the bottom region and the secondary the top; in book, trailing and leading.
- *Derived from the simulator:* after Device Hub's Partially Open and Rotate Right, the inner camera's region sat on the right edge of the bottom region (`duo-postures` measurements). On a table that half lies flat, so the inner camera would point at the ceiling. Ask the coordinator what faces forward; never assume. *Unverified* on a device.

```swift
import SwiftUI

// requires: CameraModel, CaptureControls, TimerBadge, SubjectPreview (references/outer-display-and-tabletop.md)
// requires: CameraPreview (references/rotation-and-preview.md)

#if !targetEnvironment(macCatalyst)
/// One camera screen for every pose. Flat or closed, the controls float over the
/// preview. Partly folded, they move to the bottom region (tabletop) or trailing region (book).
@available(iOS 27.1, *)
struct CaptureScreen: View {
    @State private var model = CameraModel()          // above the arrangement: a fold never rebuilds it

    var body: some View {
        ArrangementView {
            CaptureControls(model: model)                // primary: what people tap
        } secondary: {
            CameraPreview(source: model.capture.previewSource) { model.attachMain($0) }
                .overlay { if model.isSwitching { Color.black } }    // hide the old camera's frames
                .overlay { TimerBadge(secondsLeft: model.secondsLeft) }
                .ignoresSafeArea()
        }
        .arrangementViewStyle(.overlay)
        .background(.black)
        .sceneAccessory {                                // section 7: the subject's view, outer display
            CameraCaptureAccessory { SubjectPreview(model: model) }
        }
    }
}
#endif
```

## 10. Split View and interruptions

- Every app takes part in Split View on the inner display ([talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=184)). `AVCaptureSession.h` says a session can be interrupted with `.videoDeviceNotAvailableWithMultipleForegroundApps` in a multi-app layout. *Unverified* on Duo: expect it, show why the preview stopped, and resume on `interruptionEndedNotification`.
- `isMultitaskingCameraAccessSupported` is `true` for video-call apps (the `voip` background mode) and for apps with the multitasking camera entitlement ([Apple](https://developer.apple.com/documentation/avkit/accessing-the-camera-while-multitasking-on-ipad)). Set `isMultitaskingCameraAccessEnabled` before the session starts.
- The accessory needs the app full screen, so Split View also hides it.

Code: [references/direction-and-mirroring.md](references/direction-and-mirroring.md#interruptions).

## Deploying below iOS 27.1

- The virtual front camera needs no new API. It works with your current code and deployment target.
- The outer and inner types and the direction coordinator are iOS 27.1. Put that code behind `@available(iOS 27.1, *)` and `if #available(iOS 27.1, *)`. On older iOS, keep using the discovery session above.
- The outer and inner types are unavailable on Mac Catalyst. Wrap their code in `#if !targetEnvironment(macCatalyst)`.
- `setDynamicAspectRatio` and sensor orientation compensation are iOS 26; `videoRotationAngleRelative(toDeviceOrientation:)` is iOS 27.0.

## Test it

| Where | What you can check |
|---|---|
| Simulator | Layout only: controls in every pose, the accessory view at the outer display's size, nothing in the fold. Discovery returns no camera (*measured*), so guard every `nil`. |
| Real iPhone Duo | Everything else: open and close with each strategy, the switch mask, mirroring on both displays, flipped selfies, rotation on both displays, the accessory with capture running, Split View, tabletop with the timer. |

Checklists for both and how to fake a camera in the simulator: [references/testing.md](references/testing.md).

## Checklist

- [ ] The app starts from the virtual front camera; physical cameras only where the app needs them.
- [ ] No camera choice reads `position` or the device type to decide which way a camera points.
- [ ] One `AVCaptureDeviceDirectionCoordinator` per preview view, created on the main actor and kept alive while the view is on screen.
- [ ] The handler only reads descriptors; the session actor resolves `AVCaptureDevice(uniqueID:)` and handles `nil`.
- [ ] The preview is covered during a switch.
- [ ] Mirroring follows the direction map, set after each map change and each new input, with automatic mirroring turned off first.
- [ ] A new rotation coordinator per camera and per preview layer; sensor orientation compensation off after that.
- [ ] Shutter and controls clear of the fold and of the inner camera's occlusion.
- [ ] The outer-display accessory carries no essential control; its countdown also shows in the main UI.
- [ ] Tabletop: preview on top, the same controls below, a self-timer.
- [ ] Interruptions in Split View show a message and recover.
- [ ] iOS 27.1 and Mac Catalyst gates in place; `nil` cameras handled (the simulator returns none).
- [ ] Checked on a real iPhone Duo before release.
