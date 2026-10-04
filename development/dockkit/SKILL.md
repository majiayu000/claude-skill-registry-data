---
name: dockkit
description: "Control motorized camera docks and enable intelligent subject tracking using DockKit. Use when discovering DockKit-compatible accessories, implementing camera subject tracking for faces or bodies, controlling dock motors for pan and tilt, configuring framing behavior, setting regions of interest, or building video apps with automatic camera tracking."
---

# DockKit

Framework for integrating with motorized camera stands and gimbals that
physically track subjects by rotating the iPhone. DockKit handles motor
control, subject detection, and framing so camera apps get 360-degree pan
and 90-degree tilt tracking with no additional code. Apps can override
system tracking to supply custom observations, control motors directly,
or adjust framing. iOS 17+, Swift 6.3.

## Contents

- [Setup](#setup)
- [Discovering Accessories](#discovering-accessories)
- [System Tracking](#system-tracking)
- [Custom Tracking](#custom-tracking)
- [Framing and Region of Interest](#framing-and-region-of-interest)
- [Motor Control](#motor-control)
- [Animations](#animations)
- [Tracking State and Subject Selection](#tracking-state-and-subject-selection)
- [Accessory Events](#accessory-events)
- [Battery Monitoring](#battery-monitoring)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

Import DockKit:

```swift
import DockKit
```

DockKit requires a physical DockKit-compatible accessory and a real device.
The Simulator cannot connect to dock hardware.

DockKit itself requires no special entitlements or DockKit-specific
Info.plist keys. Camera apps that use device cameras still need normal
camera privacy handling, including `NSCameraUsageDescription`. The framework
communicates with paired accessories automatically through the DockKit
system daemon.

The app must use AVFoundation camera APIs. DockKit hooks into the camera
pipeline to analyze frames for system tracking.

## Discovering Accessories

Use `DockAccessoryManager.shared` to observe dock connections:

```swift
import DockKit

func observeAccessories() async throws {
    for await stateChange in try DockAccessoryManager.shared.accessoryStateChanges {
        switch stateChange.state {
        case .docked:
            guard let accessory = stateChange.accessory else { continue }
            // Accessory is connected and ready
            configureAccessory(accessory)
        case .undocked:
            // iPhone removed from dock
            handleUndocked()
        @unknown default:
            break
        }
    }
}
```

`accessoryStateChanges` emits `DockAccessory.StateChange` values with `state`,
`accessory`, and `trackingButtonEnabled`. Use `accessory.identifier` for the
name, category, and UUID; hardware details are available via `firmwareVersion`
and `hardwareModel`.

## System Tracking

System tracking is DockKit's default mode. When enabled, the system
analyzes camera frames through built-in ML inference, detects faces and
bodies, and drives the motors to keep subjects in frame. Any app using
AVFoundation camera APIs benefits automatically.

### Enable or Disable

```swift
// Enable system tracking (default)
try await DockAccessoryManager.shared.setSystemTrackingEnabled(true)

// Disable system tracking for custom control
try await DockAccessoryManager.shared.setSystemTrackingEnabled(false)
```

System tracking state does not persist across app termination, reboots,
or background/foreground transitions. Set it explicitly whenever the app
needs a specific value.

### Tap to Select Subject

Allow users to select a specific subject by tapping:

```swift
// Select the subject at a unit point in video-frame coordinates
try await accessory.selectSubject(at: CGPoint(x: 0.5, y: 0.5))

// Select specific subjects by identifier
try await accessory.selectSubjects([subjectUUID])

// Clear selection (return to automatic selection)
try await accessory.selectSubjects([])
```

## Custom Tracking

Disable system tracking and provide your own observations when using
custom ML models or the Vision framework.

### Providing Observations

Construct `DockAccessory.Observation` values from your inference output
and pass them to the accessory at 10-30 fps:

```swift
import DockKit
import AVFoundation

func processFrame(
    _ sampleBuffer: CMSampleBuffer,
    accessory: DockAccessory,
    activeDevice: AVCaptureDevice
) async throws {
    let cameraInfo = DockAccessory.CameraInformation(
        captureDevice: activeDevice.deviceType,
        cameraPosition: activeDevice.position,
        orientation: .corrected,
        cameraIntrinsics: frameIntrinsics(from: sampleBuffer),
        referenceDimensions: frameDimensions(from: sampleBuffer)
    )

    let detection = try await detector.detect(sampleBuffer)
    let observationType: DockAccessory.Observation.ObservationType = switch detection.kind {
    case .face: .humanFace
    case .body: .humanBody
    case .object: .object
    }

    let observation = DockAccessory.Observation(
        identifier: detection.id,
        type: observationType,
        rect: detection.rect,       // normalized, lower-left origin
        faceYawAngle: detection.faceYawAngle
    )

    try await accessory.track([observation], cameraInformation: cameraInfo)
}
```

### Observation Types

When reviewing custom tracking, explicitly choose among the only supported
`ObservationType` cases: `.humanFace`, `.humanBody`, and `.object`.
Do not answer with only `.humanFace` when body or object detections are possible.

The `rect` uses normalized coordinates with a lower-left origin (same
coordinate system as Vision framework -- no conversion needed).

### Camera Information

`DockAccessory.CameraInformation` describes the active camera; do not hardcode
placeholder device, intrinsics, or frame-size values. Set orientation to
`.corrected` when coordinates are already relative to the bottom-left corner.
In review answers, reject opaque optional `cameraInfo` placeholders and show
construction from the active `AVCaptureDevice` plus the current `CMSampleBuffer`.

Track variants also accept `[AVMetadataObject]` instead of observations.
Use the `image: CVPixelBuffer` overloads when DockKit should combine
observations or metadata with the captured image buffer; the image argument
is required in those overloads.

## Framing and Region of Interest

### Framing Modes

Control how the system frames tracked subjects:

```swift
try await accessory.setFramingMode(.automatic) // documented default
try await accessory.setFramingMode(.center)    // explicit opt-in
```

| Mode | Behavior |
|---|---|
| `.automatic` | Documented default; system decides optimal framing |
| `.center` | Explicit opt-in mode to keep subject centered |
| `.left` | Frame subject in left third |
| `.right` | Frame subject in right third |

Default system behavior often centers the primary subject, but `.center` is
never the default-like mode; `.automatic` is. Use `.left` or `.right` when
graphic overlays occupy part of the frame.

### Region of Interest

Constrain tracking to a specific area of the video frame:

```swift
// Normalized coordinates, origin at upper-left
let squareRegion = CGRect(x: 0.25, y: 0.0, width: 0.5, height: 1.0)
try await accessory.setRegionOfInterest(squareRegion)
```

Use region of interest when cropping to a non-standard aspect ratio
(e.g., square video for conferencing) so subjects stay within the
visible area.

## Motor Control

Disable system tracking before controlling motors directly.

### Angular Velocity

Set continuous rotation speed in radians per second:

```swift
import Spatial

// Pan right at 0.2 rad/s, tilt down at 0.1 rad/s
let velocity = Vector3D(x: 0.1, y: 0.2, z: 0.0)
try await accessory.setAngularVelocity(velocity)

// Stop all motion
try await accessory.setAngularVelocity(Vector3D())
```

Axes:
- `x` -- pitch (tilt). Positive tilts down on iOS.
- `y` -- yaw (pan). Positive pans right.
- `z` -- roll (if supported by hardware).

### Set Orientation

Move to a specific position over a duration:

```swift
let target = Vector3D(x: 0.0, y: 0.5, z: 0.0)  // Yaw 0.5 rad
let progress = try accessory.setOrientation(
    target,
    duration: .seconds(2),
    relative: false
)
```

Also accepts `Rotation3D` for quaternion-based orientation. Set
`relative: true` to move relative to the current position. The returned
`Progress` object tracks completion.

### Motion State

Monitor the accessory's current position and velocity:

```swift
for await state in try accessory.motionStates {
    let positions = state.angularPositions   // Vector3D
    let velocities = state.angularVelocities // Vector3D
    let time = state.timestamp
    if let error = state.error {
        // Motor error occurred
    }
}
```

### Setting Limits

Restrict range of motion and maximum speed per axis:

```swift
let yawLimit = try DockAccessory.Limits.Limit(
    positionRange: -1.0 ..< 1.0,   // radians
    maximumSpeed: 0.5               // rad/s
)
let limits = DockAccessory.Limits(yaw: yawLimit, pitch: nil, roll: nil)
try accessory.setLimits(limits)
```

## Animations

Built-in character animations that move the dock expressively:

```swift
// Disable system tracking before animating
try await DockAccessoryManager.shared.setSystemTrackingEnabled(false)

let progress = try await accessory.animate(motion: .kapow)

// Wait for completion
while !progress.isFinished && !progress.isCancelled {
    try await Task.sleep(for: .milliseconds(100))
}

// Restore system tracking
try await DockAccessoryManager.shared.setSystemTrackingEnabled(true)
```

| Animation | Effect |
|---|---|
| `.yes` | Nodding motion |
| `.no` | Shaking motion |
| `.wakeup` | Startup-style motion |
| `.kapow` | Dramatic pendulum swing |

Animations start from the accessory's current position and execute
asynchronously. Always restore tracking state after completion. Keep
`animate(motion:)` and `setOrientation(_:duration:relative:)` calls to no
more than twice per second; higher call rates can throw `.frameRateTooHigh`.

## Tracking State and Subject Selection

iOS 18+ exposes ML-derived tracking signals through the throwing
`trackingStates` async sequence. Each state has `time` and `trackedSubjects`
(`.person` or `.object`); persons include `identifier`, `rect`,
`speakingConfidence`, `lookingAtCameraConfidence`, and `saliencyRank`
(lower rank is more salient).

```swift
if #available(iOS 18.0, *) {
    for await state in try accessory.trackingStates {
        var speaker: UUID?
        var engaged: UUID?
        var salient: (id: UUID, rank: Int)?
        for subject in state.trackedSubjects {
            switch subject {
            case .person(let person):
                let id = person.identifier, rect = person.rect
                let speaking = person.speakingConfidence
                let looking = person.lookingAtCameraConfidence
                let rank = person.saliencyRank
                updateSubjectOverlay(id: id, rect: rect)
                if let speaking, speaking > 0.7 { speaker = id }
                if let looking, looking > 0.7 { engaged = id }
                if let rank, salient == nil || rank < salient!.rank { salient = (id, rank) }
            case .object(let object):
                let id = object.identifier, rect = object.rect
                let rank = object.saliencyRank
                updateSubjectOverlay(id: id, rect: rect)
                if let rank, salient == nil || rank < salient!.rank { salient = (id, rank) }
            }
        }
        if let id = speaker ?? engaged ?? salient?.id { try await accessory.selectSubjects([id]) }
    }
}
```

Use `selectSubjects(_:)` to lock tracking by UUID; pass `[]` to return to
automatic selection. Use `speakingConfidence` for speakers,
`lookingAtCameraConfidence` for engagement, `rect` for overlays, and lower
`saliencyRank` values as fallback.
In review answers, consume `lookingAtCameraConfidence` and `rect` in code, not
just prose.

## Accessory Events

Physical buttons on the dock trigger events through the throwing
`accessoryEvents` async sequence (iOS 17.4+):

```swift
if #available(iOS 17.4, *) {
    for await event in try accessory.accessoryEvents {
        switch event {
        case .cameraShutter: break
        case .cameraFlip: break
        case .cameraZoom(factor: let factor): break
        case .button(id: let id, pressed: let pressed): break
        @unknown default: break
        }
    }
}
```

Third-party apps receive these events and implement behavior through
AVFoundation.

## Battery Monitoring

Monitor the dock's battery status through the throwing `batteryStates` async
sequence (iOS 18+). A dock can report multiple batteries, each identified by
`name`:

```swift
if #available(iOS 18.0, *) {
    var batteryRows: [String: (Double, DockAccessory.BatteryChargeState, Bool)] = [:]
    for await battery in try accessory.batteryStates {
        batteryRows[battery.name] = (battery.batteryLevel, battery.chargeState, battery.lowBattery)
    }
}
```

## Common Mistakes

### DON'T: Control motors without disabling system tracking

```swift
// WRONG -- system tracking fights manual commands
try await accessory.setAngularVelocity(velocity)

// CORRECT -- disable system tracking first
try await DockAccessoryManager.shared.setSystemTrackingEnabled(false)
try await accessory.setAngularVelocity(velocity)
```

### DON'T: Assume tracking state persists across lifecycle events

```swift
// WRONG -- state may have reset after backgrounding
func applicationDidBecomeActive() {
    // Assume custom tracking is still active
}

// CORRECT -- re-set tracking state on foreground
func applicationDidBecomeActive() {
    Task {
        try await DockAccessoryManager.shared.setSystemTrackingEnabled(false)
    }
}
```

### DON'T: Call track() outside the recommended rate

```swift
// WRONG -- calling once per second is too slow
try await accessory.track(observations, cameraInformation: cameraInfo)
// (called at 1 fps)

// CORRECT -- call at 10-30 fps
// Hook into AVCaptureVideoDataOutputSampleBufferDelegate for per-frame calls
```

### DON'T: Spam orientation or animation calls

DockKit can throw `.frameRateTooHigh` if `animate(motion:)` or
`setOrientation(_:duration:relative:)` is called more than twice per second.
Set a trajectory, observe its `Progress`, and avoid tight command loops.

### DON'T: Forget to restore tracking after animations

```swift
// WRONG -- tracking stays disabled after animation
try await DockAccessoryManager.shared.setSystemTrackingEnabled(false)
let progress = try await accessory.animate(motion: .kapow)

// CORRECT -- restore tracking when animation completes
try await DockAccessoryManager.shared.setSystemTrackingEnabled(false)
let progress = try await accessory.animate(motion: .kapow)
while !progress.isFinished && !progress.isCancelled {
    try await Task.sleep(for: .milliseconds(100))
}
try await DockAccessoryManager.shared.setSystemTrackingEnabled(true)
```

### DON'T: Use DockKit in Simulator

DockKit requires a physical DockKit-compatible accessory. Guard
initialization and provide fallback behavior when no accessory is
available.

## Review Checklist

- [ ] `import DockKit` present where needed
- [ ] Subscribed to `accessoryStateChanges` to detect dock/undock events
- [ ] Handled both `.docked` and `.undocked` states
- [ ] System tracking disabled before custom tracking or motor control
- [ ] System tracking restored after animations complete
- [ ] Custom observations supplied at 10-30 fps
- [ ] `animate` and `setOrientation` commands limited to 2 calls per second
- [ ] Observation `rect` uses normalized coordinates (lower-left origin)
- [ ] Camera information is built inline from the active `AVCaptureDevice` and current sample buffer
- [ ] Observation type choice names `.humanFace`, `.humanBody`, and `.object`
- [ ] `@unknown default` handled in all switch statements over DockKit enums
- [ ] Motion limits set if restricting accessory range of motion
- [ ] Tracking state re-applied after app returns to foreground
- [ ] `accessoryEvents` guarded with `#available(iOS 17.4, *)`
- [ ] `trackingStates` and `batteryStates` guarded with `#available(iOS 18.0, *)`
- [ ] Battery UI preserves `BatteryState.name` for multi-battery docks
- [ ] No DockKit code paths executed in Simulator builds

## References

- Extended patterns (Vision integration, service architecture, custom animations): [references/dockkit-patterns.md](references/dockkit-patterns.md)
- [DockKit framework](https://sosumi.ai/documentation/dockkit)
- [DockAccessoryManager](https://sosumi.ai/documentation/dockkit/dockaccessorymanager)
- [DockAccessory](https://sosumi.ai/documentation/dockkit/dockaccessory)
- [Controlling a DockKit accessory using your camera app](https://sosumi.ai/documentation/dockkit/controlling-a-dockkit-accessory-using-your-camera-app)
- [Track custom objects in a frame](https://sosumi.ai/documentation/dockkit/track-custom-objects-in-a-frame)
- [Modify rotation and positioning programmatically](https://sosumi.ai/documentation/dockkit/modify-rotation-and-positioning-behavior-programmatically)
- [Integrate with motorized iPhone stands using DockKit -- WWDC23](https://sosumi.ai/videos/play/wwdc2023/10304/)
- [What's new in DockKit -- WWDC24](https://sosumi.ai/videos/play/wwdc2024/10164/)
