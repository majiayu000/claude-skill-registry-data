---
name: testing-debugging
description: Test and debug Meta Wearables DAT and Meta Ray-Ban Display apps, including MockDeviceKit, Developer Mode, registration, device discovery, sessions, camera streams, callbacks, and lifecycle issues.
---

# Testing and Debugging Meta Wearables

Use a state-first debugging process. Do not jump directly to camera code.

## Diagnostic order

Check in this order:

1. SDK version and app build compatibility.
2. Developer Mode enabled where required.
3. Meta AI app installed/configured on the test phone.
4. App registration state.
5. URL/deep-link callback reaches the app.
6. Device appears in the SDK's available-device stream/list.
7. Session reaches its started/connected state.
8. Required permission is granted.
9. Requested capability is actually supported by the selected device.
10. Stream/display capability starts successfully.
11. Frames/events are consumed and not blocked by app lifecycle or thread starvation.

## MockDeviceKit

Use MockDeviceKit when:

- Hardware is unavailable.
- CI needs deterministic state transitions.
- Registration/permission/session UI needs repeatable tests.
- A failure state is hard to trigger reliably on physical glasses.

Do not claim MockDeviceKit perfectly reproduces hardware timing, RF behavior, thermal constraints or every display feature. Validate critical flows on real hardware before release.

## Logging

Add structured logs for:

- SDK initialization.
- Registration state transitions.
- Device additions/removals.
- Session state changes.
- Permission requests/results.
- Stream start/stop/failure.
- Capture requests/results.
- App background/foreground events.

Avoid logging captured image content, tokens, credentials or sensitive transcripts.

## Typical failure classes

- Deep link callback misconfigured.
- Development credentials mixed with production/release configuration.
- Missing/incorrect Bluetooth permission on newer Android versions.
- iOS Info.plist key missing or conflicting with existing URL schemes.
- Session created before registration/device availability is ready.
- Capability requested on a device that does not support it.
- UI thread overloaded by per-frame image conversion.
- Stream listener/token released too early.
- Session/stream not restarted after lifecycle transition when required.

## Validation output

When debugging a user's repository, report:

- Root cause if confirmed.
- Evidence from logs/code.
- Exact files changed.
- A minimal reproduction/test path.
- Remaining hardware/account uncertainties.
