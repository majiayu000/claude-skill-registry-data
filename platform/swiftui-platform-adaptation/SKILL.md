---
name: swiftui-platform-adaptation
description: "Adapt SwiftUI apps for iOS, iPadOS, macOS, watchOS, tvOS, and visionOS with appropriate scenes, navigation, input, windows, focus, and lifecycle."
---

# Platform-native scenes and interaction

## Inputs

List supported platforms, actual deployment minimums, primary tasks, input devices, scene/window model, required capabilities, and feature parity expectations.

## Rules

- **PLAT-001 — Share domain logic, adapt interaction.** Platform parity means equivalent useful outcomes, not identical layouts and chrome.
- **PLAT-002 — Own state per scene.** Separate app services from window selection, navigation, and drafts. Choose the correct scene type before adding custom window behavior.
- **PLAT-003 — Respect native input.** Support touch, pointer, keyboard, focus/remote, Crown, or spatial interaction as appropriate; do not transplant phone assumptions.
- **PLAT-004 — Check capability and availability.** A shared module does not make every API or entitlement available on every platform.
- **PLAT-005 — Validate each surface.** Build and exercise every affected platform; phone success does not prove watch, television, desktop, or spatial behavior.

## Workflow

1. Choose the scene and interaction model for each supported platform.
2. Share models, commands, and reusable semantic components; isolate platform-specific presentation at narrow boundaries.
3. Design compact, resizable, focus-driven, and spatial surfaces from their primary task.
4. Handle scene activation, restoration, multiple windows, and external requests.
5. Verify platform-specific failure and input paths.

## Verify

Check resize and multiwindow behavior, keyboard commands, focus restoration, compact watch readability, tvOS focus reachability, and visionOS comfort/capability assumptions on relevant destinations.

## Output

Return a platform matrix, shared versus specialized boundaries, availability decisions, and destination-specific proof.

## References

Read the [playbook](references/platform-patterns.md) for decisions, failure cases, and source links.

For scenes, desktop behavior, and focus platforms, read the [focused reference](references/scenes-and-focus.md).
