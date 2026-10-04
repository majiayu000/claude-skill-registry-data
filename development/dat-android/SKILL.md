---
name: dat-android
description: Build, integrate, review, or debug Android apps using Meta Wearables Device Access Toolkit (DAT) for Ray-Ban Meta and other supported Meta AI glasses.
---

# Meta Wearables DAT — Android

Use this skill for Kotlin/Android integrations.

## Current snapshot

As of the bundled 2026-09-22 snapshot, the official repository README references DAT **0.9.0** and Maven artifacts under `com.meta.wearable`, including:

- `mwdat-core`
- `mwdat-camera`
- `mwdat-display`
- `mwdat-mockdevice`

Do not blindly pin 0.9.0. Check Maven Central or official docs first when network/MCP is available.

## Setup pattern

Prefer a version catalog when the project already uses one:

```toml
[versions]
mwdat = "<verified-latest-version>"

[libraries]
mwdat-core = { group = "com.meta.wearable", name = "mwdat-core", version.ref = "mwdat" }
mwdat-camera = { group = "com.meta.wearable", name = "mwdat-camera", version.ref = "mwdat" }
mwdat-display = { group = "com.meta.wearable", name = "mwdat-display", version.ref = "mwdat" }
mwdat-mockdevice = { group = "com.meta.wearable", name = "mwdat-mockdevice", version.ref = "mwdat" }
```

Only add modules that the feature needs. The SDK is distributed from Maven Central according to the official repository snapshot.

## Required integration areas

When implementing a real feature, account for all relevant areas rather than only the happy-path stream code:

- `Application`/startup SDK initialization.
- Android manifest metadata and URL/deep-link callback path.
- Bluetooth/network permissions required by the current SDK and Android target level.
- Registration with Meta AI.
- Available device observation and device selection.
- Session creation/start/stop.
- Camera capability attachment and stream lifecycle when needed.
- Foreground/background behavior.
- Permission denied / device unavailable / disconnected states.

During Developer Mode, official examples have supported placeholder app credentials such as `0`; production/release setup must use current values from Wearables Developer Center. Verify before shipping.

## Architecture

Prefer a narrow abstraction such as:

```text
WearablesRepository
  registrationState
  devices
  sessionState
  connect()
  disconnect()
  startCamera()
  stopCamera()
  capturePhoto()
```

Expose immutable state to ViewModels. Keep Android Activities/Composables focused on UI and lifecycle signals.

## Camera pipelines

For computer vision/AI:

1. Start the DAT stream only while the feature needs it.
2. Convert only the frames selected for processing.
3. Use sampling/throttling for cloud inference.
4. Keep a single in-flight request or small bounded queue unless the use case requires more.
5. Drop old frames under backpressure.
6. Never upload continuous camera frames by default without an explicit product requirement and user-visible disclosure.

## Verification

Before finalizing changes, verify current API signatures with `search_dat_docs` when available. The official APIs have changed across preview releases, so do not infer method names from old examples.
