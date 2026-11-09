---
name: unity-build-controls
description: Implement Unity action input and player-device ownership with lifecycle-safe controller and haptic feedback.
engines: [UNITY]
---

# Unity Build Controls

## When to use

Implement Unity action input and player-device ownership with lifecycle-safe controller and haptic feedback. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-build-controls` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Record the selected Unity version, input backend and package version, supported devices, local player count, action map, update mode, rebinding persistence and accessibility requirements. Preserve a deliberately selected legacy input backend rather than installing Input System automatically.

## Workflow

1. Translate controls into gameplay actions with explicit pressed, held and released semantics. For the selected Input System, use InputAction assets and a consistent PlayerInput or InputUser ownership strategy; do not broadcast one device to every local player.
2. Choose dynamic, fixed or manual input processing deliberately. Sample intent once into a bounded buffer consumed by the authoritative simulation; pointer deltas, analog axes and button edges require different handling.
3. Separate gameplay, UI and cinematic contexts. Switch maps on a single screen/input owner, clear pending held actions at transitions, and prevent submit or cancel from also firing a gameplay action.
4. Implement dead zones, sensitivity, inversion, hold/toggle settings and rebinding conflict handling. Save binding overrides as validated preferences and update prompts from the current binding and paired device.
5. Handle device loss, regain, user switching, focus loss and scene teardown. Unsubscribe callbacks and disable owned actions; reconnecting must not replay expired input or silently assign another player's controller.
6. Route haptic feedback through the owning player's paired supported device. Bound Gamepad motor intensity and duration, apply user settings and priorities, and stop/reset effects on cancellation, pause, focus loss, disconnect or destruction.
7. Keep visual/audio equivalents for tactile cues. Handle unsupported or failed haptic operations without changing gameplay results; global haptic APIs require an application-level owner so one local player cannot unexpectedly stop every device.

## Verification

- Test action edges, buffered presses, context switches, rebinding and device reassignment using the project's selected input test facilities.
- Exercise two local players, controller disconnect/reconnect during a held action, focus loss during vibration, overlapping effects and disabled intensity.
- Record physical-device checks separately from API simulations; native input behavior and tactile output need a real player/device session.

## Output

Action assets or backend adapters, device and context ownership rules, validated binding preferences, bounded haptic routing, and device-specific test evidence. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Input System, platform-specific controller support and mobile haptics are explicit dependencies. Do not claim that a mocked motor call proves vibration was felt. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Input System Player Input component](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/PlayerInput.html). Use the documentation matching the installed project version.
- [Gamepad haptic APIs](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/Gamepad.html). Use the documentation matching the installed project version.

