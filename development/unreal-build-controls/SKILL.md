---
name: unreal-build-controls
description: Implement Unreal player input contexts and device-specific haptic feedback with explicit possession and cancellation ownership.
engines: [UNREAL]
---

# Unreal Build Controls

## When to use

Implement Unreal player input contexts and device-specific haptic feedback with explicit possession and cancellation ownership. Use this feature for Unreal-owned game code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-controls` before edits or tool launches. Continue only when the effective engine is `UNREAL` and `compatible: true`. Skill selection never selects the engine. Revalidate any task override and its permitted isolated output scope before writes. Record observed context and evidence only in the resolved `.hephaera/.cache/tasks/<task>/`; `ENGINE.md` remains the selector.

Read Unreal version, selected input plugins/backend, local player topology, action definitions, binding settings, platform device requirements and feedback policy. Enhanced Input must be an explicit compatible project selection.

## Workflow

1. Define Input Actions with correct value types, triggers and modifiers. Bind the intended Started, Triggered, Completed and Canceled transitions through the project's supported Enhanced Input component rather than treating every callback as a new button press.
2. Add and remove Mapping Contexts through the owning LocalPlayer subsystem with deliberate priorities. Separate on-foot, vehicle, UI and cinematic contexts; remove only contexts owned by this feature.
3. Bridge action values into bounded gameplay intent and the chosen movement/controller authority. Distinguish camera look deltas from rates, preserve sensitivity/inversion settings and avoid frame-rate-dependent movement.
4. Handle possession, unpossession, respawn and player/controller reassignment. Context installation and callback binding must be idempotent; held actions must not stick after a pawn or device disappears.
5. Route modal UI through the intended input mode, focus owner and cursor policy. Closing a screen must restore valid player focus and must not replay the same submit event into gameplay.
6. Implement haptic feedback through the owning PlayerController using version-supported force-feedback or device APIs. Assign effect tags/handles, bounded duration, priorities, explicit gameplay/real-time clock and user intensity; stop the owned effect on cancellation, pause, focus loss, travel or disconnect.
7. Keep unsupported devices and failed feedback calls as presentation outcomes. Reconnection must not replay expired patterns or target a different local player's device; provide equivalent visible/audio cues.

## Verification

- Test action phases, chord/hold cancellation, context priorities, remapping and gameplay/UI leakage in the real runtime.
- Exercise local-player ownership, possession changes, disconnect/reconnect and focus loss during active feedback.
- Use physical supported hardware for tactile acceptance; engine callbacks and automated input simulations prove routing only.

## Output

Input Action/Mapping Context assets and bindings, context/possession lifecycle rules, haptic ownership and cancellation policy, device-specific acceptance evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not enable plugins, invent console SDK APIs or assume mobile/controller capabilities. Device and native platform checks remain separate from browser evidence. Independent tools and services retain their own architecture contracts.

## References

Read [input and device lifecycle](references/input-device-lifecycle.md) when implementing context transitions, remapping or haptic cancellation.

- [Enhanced Input](https://dev.epicgames.com/documentation/unreal-engine/enhanced-input-in-unreal-engine). Match the documentation version to the project.
- [Unreal force feedback](https://dev.epicgames.com/documentation/en-us/unreal-engine/force-feedback-in-unreal-engine). Match the documentation version to the project.

