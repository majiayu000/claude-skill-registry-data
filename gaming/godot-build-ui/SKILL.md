---
name: godot-build-ui
description: Build Godot Control-based game interfaces with responsive layout, reliable focus, and lifecycle-safe HUD binding.
engines: [GODOT]
---

# Godot Build UI

## When to use

Build Godot Control-based game interfaces with responsive layout, reliable focus, and lifecycle-safe HUD binding. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-build-ui` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Read Godot version, GDScript/C# choice, target surfaces, local input ownership, theme/typography, safe areas, localization and accessibility requirements. Identify existing screen stack and signal/state architecture.

## Workflow

1. Compose Control nodes with Containers, anchors, offsets, size flags and minimum sizes deliberately. Container-managed children should not fight manual positioning; theme overrides need clear local versus shared ownership.
2. Define screens, overlays and modals as a lifecycle with one input owner. Handle show/hide, pause, dismissal and return focus; a hidden screen must not keep processing gameplay-facing actions.
3. Set keyboard/controller focus neighbors and valid initial/fallback focus. Use grab_focus only at the correct activation point, recover when nodes are removed/disabled and preserve pointer interaction without losing controller navigation.
4. Separate _gui_input event consumption from global Input polling. Gate gameplay actions explicitly while UI owns input, and prevent accept/cancel from activating both the screen and the world.
5. Initialize HUD from an authoritative snapshot and connect signals once. Disconnect on teardown, handle respawn/player changes and avoid retaining freed Nodes through callbacks or awaited operations.
6. Generate prompts from active bindings/device ownership and support text expansion, scale, safe areas and localization. Keep settings such as reduced motion and haptic intensity independent.
7. Use version-supported accessibility properties and target assistive-technology behavior. Godot web exports can use browser QA, while native Control accessibility requires native evidence.

## Verification

- Test nested modals, accept/cancel leakage, focus restoration, dynamic lists and pointer/controller switching.
- Exercise aspect ratios, safe areas, long/localized text, text scale and loading/empty/error states.
- Repeat HUD open/close, scene reload and respawn to catch duplicate signals or stale state; record native interaction and accessibility results.

## Output

Control scenes/themes and adapters, screen/focus/input contract, HUD signal lifecycle, layout matrix and target UI evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not infer accessibility support from appearance or web evidence alone. Missing native/device checks stay blocked or not run, and selected language remains unchanged. Independent services and tools retain their architecture contracts.

## References

- [Godot Control UI nodes](https://docs.godotengine.org/en/stable/classes/class_control.html). Select the documentation matching the project release.
- [Keyboard and controller navigation](https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html). Select the documentation matching the project release.

