---
name: unreal-build-ui
description: Build Unreal UMG and Slate game interfaces with explicit local-player input, focus, and HUD lifecycle ownership.
engines: [UNREAL]
---

# Unreal Build UI

## When to use

Build Unreal UMG and Slate game interfaces with explicit local-player input, focus, and HUD lifecycle ownership. Use this feature for Unreal-owned game code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-ui` before edits or tool launches. Continue only when the effective engine is `UNREAL` and `compatible: true`. Skill selection never selects the engine. Honor any validated task override and its permitted isolated output scope.

Record Unreal version, UMG/Slate boundaries, selected optional UI plugins, target surfaces, local players, safe zones, DPI/localization and accessibility requirements. CommonUI or MVVM is not assumed merely because available.

## Workflow

1. Assign UUserWidget/Widget Blueprint composition and native Slate responsibilities deliberately. Keep game state outside visual widgets and expose a bounded snapshot/event or selected view-model adapter.
2. Create screens through the owning local player and intended viewport layer. Distinguish per-player presentation from global viewport UI and prevent one player's modal from consuming another player's controls.
3. Define screen stack, modal ordering, input mode, cursor and focus restoration under one owner. Consume submit/cancel consistently and preserve pause ownership rather than unconditionally unpausing on close.
4. Use anchors, containers, DPI scaling and safe-zone rules for target layouts. Test localized text expansion, text scale and world-space WidgetComponent legibility separately.
5. Implement explicit keyboard/controller navigation and focus fallback when widgets are hidden, disabled, removed or rebuilt. Pointer interaction and selection feedback must remain consistent with action rebinding.
6. Bind HUD state on construction/activation using an authoritative initial snapshot; unbind delegates on teardown and handle possession, respawn and world travel. Avoid unbounded per-frame property binding for static values.
7. Apply the engine's supported accessibility structure and alternative cue channels. Native assistive-technology behavior needs target evidence; browser tooling cannot certify native UMG or Slate.
8. Read the [native UI integration reference](references/native-ui-integration.md) for UMG/Slate input ownership, optional CommonUI/MVVM, subscription lifetime and measurable verification.

## Verification

- Exercise nested modals, back/cancel, lost selection, pointer/controller switching, split-screen ownership and focus restoration.
- Test aspect ratios, safe zones, localization, text scaling and HUD rebuild across possession and travel.
- Run a real packaged/native UI session and measure UI layout/tick cost; record unsupported accessibility checks explicitly.

## Output

UMG/Slate assets and adapters, screen/input/focus state map, HUD subscription contract, layout matrix and target interaction/accessibility evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not add CommonUI or another plugin implicitly. Widget screenshots establish appearance, not full navigation, synchronization or accessibility correctness. Independent tools and services retain their own architecture contracts.

## References

- [UMG UI design](https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-ui-designer-for-unreal-engine). Match the documentation version to the project.
- [Slate UI framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/slate-ui-framework-in-unreal-engine). Match the documentation version to the project.
- [Native UI integration](references/native-ui-integration.md): local-player focus, modal lifetime, data flow and target acceptance.

