---
name: game-export
description:
  "For GameGen projects, prepare and verify Godot exports for the configured platform and delivery stage, including
  reproducible local builds and signing when device or store delivery is requested."
---

# Export the configured game delivery

Read [shared context](../../references/shared-context.md), ready preferences and the selected delivery stage. Inspect
the installed Godot version/export templates and platform toolchain. Use current official documentation for export and
signing details that vary by version. Do not expand an editor preview request into store distribution.

For editor delivery, verify the runnable scene, controls and source files. For local builds, configure the appropriate
export preset and create a reproducible package. For device/store delivery, use already authorized signing configuration
and resolve genuinely missing account/toolchain access. Keep credentials and signing secrets in their supported local
stores, outside preferences and the plugin.

## Package deliberately

Use the configured minimum OS/device, orientation, rendering path, input methods and resolution strategy. Verify that
required textures, animations, audio, localization and data resources enter the export while source art, diagnostic
videos, test saves and secrets remain outside the runtime package.

Preserve the project main scene and resource identifiers. Document or script the actual reproducible export command with
configurable paths. Do not pretend export templates, provisioning or connected devices are available before checking
them.

## Verify the packaged result

Launch the actual exported application or deploy to the authorized test device. Test startup, the core loop, controls,
pause/resume, audio, save persistence and resource loading. For mobile, verify lifecycle interruptions and the intended
landscape/portrait behavior. An editor test alone is insufficient evidence of packaged behavior.

Record the build hash/version, platform, engine/toolchain, command and test result. Report what remains unverified, such
as physical-device behavior or store submission. Publishing or sending a build follows the current user authorization;
producing a local reviewable package does not itself publish it.
