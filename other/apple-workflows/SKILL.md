---
name: apple-workflows
description: Build, review, verify and ship Apple platform apps — iOS and macOS in Swift and SwiftUI. Covers app structure and data boundaries, SwiftUI review, shared Swift packages, macOS menu bar apps, and distribution outside the App Store.
license: MIT
---

# Apple Workflows

Choose the procedure matching the task below and read only it and the resources it names. Paths inside a procedure are relative to that procedure's folder; run its scripts from that folder when a command assumes a working directory.

Follow the user's current instructions and the target repository's conventions before Kernel defaults. Project examples are failure patterns to check for, not architecture requirements. Match verification to the change: a simulator proves logic, a device proves permissions, sensors and background behaviour. Loading a procedure does not authorize publishing, uploading, or deploying.

- [iOS app work](references/ios-app/WORKFLOW.md) — building or changing a native iOS app: structure, data invariants, test-first, layered verification, shipped-experience review.
- [SwiftUI review](references/ios-swiftui-review/WORKFLOW.md) — auditing existing views, state and design-system code against a rubric; findings first, file and line references.
- [Swift package verification](references/swift-package/WORKFLOW.md) — a package shared by a Mac app and an iPhone app, and the false "build complete" that proves nothing about iOS.
- [macOS app work](references/macos-app/WORKFLOW.md) — building or changing a macOS app, menu bar/accessory apps above all: SwiftPM + AppKit bundles, hotkeys, mic capture, TCC, settings windows, Liquid Glass, and verifying a GUI you cannot screenshot.
- [macOS distribution](references/macos-distribution/WORKFLOW.md) — Developer ID, hardened runtime, notarization, DMG, Sparkle and licensing for apps sold outside the App Store.
- [Swift style](references/swift-style/WORKFLOW.md) — Charles's Swift rules: naming, access control, value types, isolation, library-grade API design. Load it before writing or reviewing Swift.

Releasing an iOS app to TestFlight is the executable `ship-ios` package, which project automation installs and pins separately. This router does not restate that pipeline.

Cross-stack engineering laws and watchOS rules live in ponti-principles; its Swift checklist points at the style procedure above. watchOS has no procedure in this router: ponti-principles is its only coverage. Non-development Apple work — Notes, Reminders, Find My, iPhone control — is not part of this router.
