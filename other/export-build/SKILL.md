---
name: export-build
description: Prepare and validate Godot export builds by checking export presets, target-platform requirements, resources, plugins/native dependencies, permissions, signing/packaging inputs, startup behavior, and reproducible runtime proof.
---
# Godot Export Build

Use when a Godot project must produce a distributable build for desktop, mobile, web, server/headless, console, or another supported target.

## Procedure
1. Confirm the Godot version and target platform/architecture, export preset, renderer/features, and current official export requirements before changing project settings or build tooling.
2. Inspect the preset and project for target-specific configuration: package/application identity, versioning, icons/assets, orientation/window behavior, permissions/entitlements, environment/features, and included/excluded resources as relevant.
3. Inventory plugins, GDExtensions/native libraries, third-party SDKs, platform services, custom templates, and external files that must exist for the target architecture and export mode.
4. Ensure runtime resources are discovered/included through supported import/export mechanisms. Avoid relying on editor filesystem paths, development-only files, or absolute machine paths.
5. Separate credentials/signing/notarization/store secrets from project source and ordinary artifacts. Use the release/platform's controlled mechanism and verify what can be tested without production signing authority.
6. Build from a clean/reproducible enough environment and record source revision, Godot/export-template version, preset/configuration, architecture, and resulting artifact identity.
7. Launch/test the exported artifact outside the editor. Verify startup, main flow, scene/resource loading, input, files/storage, networking, permissions, audio/rendering, and platform integration relevant to the product.
8. Inspect runtime logs/crash output and test missing/first-run data, clean install/update, quit/restart, and any platform lifecycle paths implicated by the application.
9. Validate artifact/package contents and size; make sure debug/test assets, secrets, development endpoints, or unnecessary source data are not included accidentally.
10. Automate export/validation in CI or release tooling when repeatability matters, while keeping platform credentials and store submission authority outside the profile/package.

## Decision rules
- Running correctly in the editor is not proof that exported resource paths, native libraries, permissions, or platform lifecycle work.
- Export requirements are version/platform-specific; verify current official Godot/platform documentation during implementation.
- Do not hardcode a build machine or Fleet node; declare toolchain/platform requirements so an eligible builder can be selected.
- Store release/submission governance belongs to Release/DevOps roles after the Godot artifact itself is proven.

## Quality gate
The export is ready when a clean compatible environment produces a traceable target artifact, required resources/native dependencies/platform configuration are present, the artifact runs through representative target flows outside the editor, sensitive/development-only material is excluded, and the remaining signing/store/release handoff is explicit.