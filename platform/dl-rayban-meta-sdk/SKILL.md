---
name: dl-rayban-meta-sdk
description: Build, integrate, review, or debug iOS and Android applications for Meta AI glasses with the Meta Wearables Device Access Toolkit (DAT). Use for Ray-Ban Meta Gen 1/2 camera and mobile integrations, and route display work only to confirmed display-capable glasses.
---

# Ray-Ban Meta SDK

Use this skill for mobile applications that integrate with Meta AI glasses.
Inspect the existing app before changing its architecture, build tooling, or
permissions. Verify the current SDK API and device capability with Meta's
official Wearables documentation before writing version-specific code.

## Choose the supported device path

| Target | Supported development path |
| --- | --- |
| Ray-Ban Meta Gen 1 or Gen 2 | DAT in a paired iOS or Android application; camera support is the initial documented SDK path. |
| Ray-Ban Meta Display | DAT for native mobile integration; Web Apps only when a standalone display experience is appropriate. |
| Unknown model | Do not assume a display. Identify the device first, then select the documented capability. |

Ray-Ban Meta Gen 1 is supported for the DAT mobile path, subject to the
current country, Developer Mode, Meta AI app pairing, account, OS, and SDK
requirements. It does not have an on-glasses display and must not receive
Display Web App code. Microphone and speaker integration for Gen 1 uses the
documented iOS or Android Bluetooth audio path; confirm the current platform
requirements before implementation. See
[Gen 1 compatibility](references/gen1-compatibility.md) before promising a
feature or release path.

## Implementation baseline

1. Confirm the exact glasses model, paired phone OS, Meta AI app state,
   Developer Mode, target country/account eligibility, and desired capability.
2. Read the project configuration and add only the DAT modules and permissions
   required by the feature.
3. Implement registration, device discovery, session/stream lifecycle, denied
   permission, disconnect, and background/resume states.
4. Keep camera processing off the UI thread, use bounded work, and stop streams
   deterministically.
5. Treat captured media and audio as sensitive: minimize retention, disclose
   cloud processing, and never embed privileged secrets in the client.
6. Test with Mock Device Kit where suitable, then validate critical flows with
   a physical compatible device.

## References

- Read `references/gen1-compatibility.md` for the capability boundary and
  official sources for Ray-Ban Meta Gen 1.
- Read `plugins/rayban-meta-sdk/references/capability-matrix.md` for routing
  between standard Ray-Ban Meta and display-capable devices.
- Use the specialized guides under `plugins/rayban-meta-sdk/skills/` only for
  the selected platform or capability; their API snapshots must be verified
  against live official documentation.
