---
name: godot-build-controls
description: Implement Godot action input, event propagation, player-device pairing, and bounded haptic feedback.
engines: [GODOT]
---

# Godot Build Controls

## When to use

Implement Godot action input, event propagation, player-device pairing, and bounded haptic feedback. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-build-controls` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Record Godot version, project language, target platforms, InputMap actions, local players, pointer/touch policy, binding preferences and haptic support requirements. Match API names to GDScript or C# rather than mixing language conventions.

## Workflow

1. Define actions and dead zones in InputMap, preserving analog magnitude where required. Sample gameplay intent into a bounded buffer; distinguish just-pressed edges, held actions and pointer deltas.
2. Choose _input, _gui_input and _unhandled_input by responsibility. Control.accept_event and Viewport.set_input_as_handled affect event propagation, while polling Input state still needs an explicit gameplay/UI ownership gate.
3. Handle keyboard/controller/pointer switching, remapping and binding-aware prompts. Touch-to-mouse emulation requires an intentional policy so a single gesture cannot produce duplicate gameplay requests.
4. Assign connected joypad device IDs to local players explicitly and track joy_connection_changed. Device IDs are runtime handles, not durable player identities; reconnect must revalidate pairing and clear stale held actions.
5. Coordinate focus changes, mouse capture and modal transitions. Stop gameplay actions when the UI owns input and restore valid focus/capture without replaying the event that closed the screen.
6. Route start_joy_vibration and stop_joy_vibration through the paired player's supported device using explicit finite duration, bounded intensity and cancellation ownership. Mobile vibrate_handheld is a separately checked platform capability.
7. Stop effects on pause, focus loss, disconnect, scene exit or superseding events; unsupported or failed vibration remains a presentation result. Never change simulation outcomes or reassign old patterns to a newly connected device.

## Verification

- Exercise action edges, analog dead zones, text entry, UI propagation, touch emulation and remapping in native fixtures.
- Test two-player pairing, disconnect/reconnect during held input, focus loss during vibration, intensity zero and overlapping/cancelled patterns.
- Record physical-device tactile checks separately from API tests and any web-build checks; simulated calls cannot prove felt feedback.

## Output

InputMap/preferences and adapters, input/context and pairing contracts, bounded haptic routing and target-device evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not assume every joypad or mobile platform supports vibration. New device mappings, native plugins and permission changes remain explicit project decisions. Independent services and tools retain their architecture contracts.

## References

- [Godot Input API](https://docs.godotengine.org/en/stable/classes/class_input.html). Select the documentation matching the project release.
- [Godot input event propagation](https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html). Select the documentation matching the project release.

