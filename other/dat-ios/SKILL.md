---
name: dat-ios
description: Build, integrate, review, or debug iPhone/iPad apps using Meta Wearables Device Access Toolkit (DAT) with Ray-Ban Meta and other supported Meta AI glasses.
---

# Meta Wearables DAT — iOS

Use this skill for Swift/SwiftUI/UIKit integrations.

## Current snapshot

As of 2026-09-22, the official iOS repository README references DAT **0.9.0**. The package is installed with Swift Package Manager from:

```text
https://github.com/facebook/meta-wearables-dat-ios
```

Verify the current release/tag before pinning a version.

Common modules in the official SDK include `MWDATCore`, `MWDATCamera`, and display/mock-device modules where applicable. Verify exact product names for the selected release.

## Setup checklist

A complete integration may require:

- SPM dependency and target products.
- URL scheme for Meta AI registration callbacks.
- External accessory / Bluetooth-related Info.plist entries required by current docs.
- `MWDAT` configuration dictionary.
- App startup `Wearables.configure()` or current equivalent.
- `.onOpenURL` / application callback forwarding to the SDK.
- Registration flow.
- Device selector and session lifecycle.
- Feature capability (camera/display) attachment.

Do not paste an old Info.plist wholesale into an app. Merge keys with the project's existing URL schemes/background modes and verify current requirements.

## Architecture

Prefer a dedicated `WearablesClient` / `WearablesService` owned by an Observable model or app service layer.

Keep these concerns separate:

- Registration state.
- Device availability.
- Device session state.
- Camera stream state.
- UI rendering.
- AI/network processing.

Use `@MainActor` only for state that updates UI. Keep frame conversion/inference/network operations off the main actor when possible.

## Camera frame handling

For live camera streams:

- Retain/cancel listener tokens correctly.
- Do not convert every frame to `UIImage` unless required.
- Throttle frames sent to external AI services.
- Stop stream/session when leaving the feature unless background operation is explicitly supported and required.
- Treat captured frames as sensitive data.

## Registration credentials

Official preview examples have used development values such as `MetaAppID = 0` with Developer Mode. Production or release-channel builds may require Wearables Developer Center values, client tokens and Apple Team ID depending on the current SDK. Verify current docs before generating release configuration.

## Verification

Use `search_dat_docs` against the official Wearables MCP whenever available before writing exact current Swift APIs. Preview API surface can change.
