---
name: privacy-release
description: Apply privacy, data-minimization, analytics/crash-reporting, developer-preview, testing-channel, and release considerations to Meta Wearables apps.
---

# Privacy, Telemetry and Release

Treat camera, microphone and location data from wearable devices as sensitive inputs.

## Data minimization

- Request only the permissions required by the feature.
- Process locally when practical.
- Do not retain raw photos/video/audio unless the feature explicitly needs retention.
- Make cloud processing visible in product UX/privacy policy.
- Separate operational logs from captured media.
- Do not put secrets or long-lived privileged credentials in the client.

## SDK telemetry

The official Android/iOS repositories document analytics and SDK crash-reporting controls. Their exact configuration keys can change, so verify current docs before editing production settings.

At the 2026-09-22 snapshot:

- Android docs describe manifest opt-out flags for analytics and SDK crash reporting.
- iOS docs describe `MWDAT` Info.plist opt-out dictionaries for analytics and crash reporting.

Do not silently change telemetry policy in an existing app. Preserve the product team's intended setting unless asked.

## Developer Preview and publishing

Do not promise public App Store/Play Store or Wearables publishing solely because a build works locally. The Wearables platform has used Developer Preview and release-channel restrictions. Verify the current publishing rules before release guidance.

## Pre-release checklist

- Current SDK version pinned intentionally.
- Required Meta developer project/app configured.
- Development credentials removed/replaced where required.
- Privacy policy covers wearable camera/microphone/location behavior.
- Error UI exists for registration/device/permission failures.
- Physical-device test completed for critical flows.
- Background/lifecycle behavior tested.
- Telemetry settings reviewed.
- Cloud endpoints use HTTPS and no privileged secret is embedded in the app.
