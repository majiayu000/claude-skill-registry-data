---
name: unity-build-ui
description: Implement Unity game UI with an explicit uGUI or UI Toolkit selection, player focus ownership, and reliable HUD state.
engines: [UNITY]
---

# Unity Build UI

## When to use

Implement Unity game UI with an explicit uGUI or UI Toolkit selection, player focus ownership, and reliable HUD state. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-build-ui` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Record Unity version, target player surfaces, selected uGUI or UI Toolkit runtime stack, input backend, local player count, safe areas, localization and accessibility requirements. Confirm any UI packages and their supported runtime controls. Inspect existing screens and font assets before changes; preserve serialized references and unrelated listeners.

## Workflow

1. Select the existing UI stack explicitly. For uGUI, use Canvas, RectTransform, layout components, EventSystem and the chosen input module; for UI Toolkit, use UIDocument, VisualElement, UXML/USS and the version-supported event/focus APIs.
2. Define screen lifecycle, stack order, pause behavior and one input owner per local player. A modal must capture the intended actions, block gameplay leakage and restore valid prior focus after closing.
3. Build responsive hierarchy for aspect changes, safe areas, text expansion and scale preferences. Keep world-space UI and screen-space readability budgets distinct; prevent transparent hit targets from stealing input unexpectedly.
4. Implement keyboard/controller navigation and pointer interaction together. Use EventSystem selection or UI Toolkit focus deliberately; rebuild focus when elements disappear, become disabled or are virtualized.
5. Initialize HUD from an authoritative snapshot, subscribe to changes once and unsubscribe on screen teardown. Handle player possession, respawn and scene reload without stale references or double event delivery.
6. Generate binding-aware prompts from the paired player's active control scheme. Treat settings as validated data and keep reduced motion, text scale and haptic intensity independent.
7. Provide accessible structure and nonvisual cue alternatives supported by the target platform. Do not infer native screen-reader behavior from a browser accessibility tree or Editor-only preview.

Read [stack, font and rebuild decisions](references/ui-implementation.md) when selecting bindings, text rendering or optimizing UI updates. Use a localization owner for table/locale lifetimes while this workflow retains screen and focus ownership.

## Verification

- Test modal nesting, cancel/back, focus restoration, pointer-to-controller switching and two-player input isolation.
- Test narrow/wide layouts, safe areas, long localized text, scale changes, empty/loading/error states and HUD open-close-respawn cycles.
- Measure layout/rebuild, batching and text-atlas costs in the chosen stack; include repeated screen reuse and unchanged HUD data. Avoid rebuilding the entire interface to change one value.
- Capture actual native/player evidence. Browser QA is appropriate for a Unity web build but cannot certify a native player's UI behavior.

## Output

Selected-stack UI assets and adapters, screen/focus ownership map, HUD binding lifecycle, layout matrix and target-specific interaction evidence. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not mix uGUI and UI Toolkit without a documented event/input bridge. Missing native accessibility or device tests remain explicitly blocked or not run. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Unity UI comparison](https://docs.unity3d.com/6000.0/Documentation/Manual/UI-system-compare.html). Use the documentation matching the installed project version.
- [UI Toolkit focus](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-focus-order.html). Use the documentation matching the installed project version.

