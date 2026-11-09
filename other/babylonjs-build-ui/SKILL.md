---
name: babylonjs-build-ui
description: Build Babylon.js GUI HUDs and world interfaces with screen ownership, accessible companions and lifecycle-safe state binding.
engines: [BABYLONJS]
---

# Build Babylon.js UI

## When to use

Implement Babylon GUI screens, HUD overlays, world-linked labels or mesh interfaces. Compose with `build-game-ui` for shared hierarchy and navigation design.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh babylonjs-build-ui`; require compatibility and honor task override scope. Inspect the locked core/GUI versions, chosen browser surface, screen contract and selected art pipeline. Use the host GUI package and authorized assets; do not introduce a CDN or UI framework implicitly.

## Workflow

1. Choose `AdvancedDynamicTexture.CreateFullscreenUI` or mesh texture mode deliberately. Define control ownership and GUI render scale/ideal dimensions independently from world resolution; bound texture size and re-layout cost.
2. Use controls such as `Grid`, `StackPanel`, `TextBlock` and `Button` to implement measured hierarchy and navigation. World labels using `linkWithMesh` need behind-camera, occlusion and disposal behavior; mesh GUI interactions need explicit picking policy.
3. Set pointer-blocking behavior and coordinate scene camera inputs with the top screen/modal. A control activation must not also fire a world action. Own navigation repeat, back/cancel, selected-item visibility and focus restoration.
4. Provide semantic DOM companions or another verified accessible interaction path where Babylon's drawn controls cannot expose the required semantics. A GUI button name alone is not proof of browser accessibility. Keep companion and rendered control state synchronized without double activation.
5. Bind the HUD from a snapshot plus updates, unsubscribe on close/disposal, and refresh on reopen. Prompts track the active player's current bindings. Remove control observers and dispose owned GUI textures at the correct scene boundary.

## Output and verification

Deliver GUI/screen adapters, semantic equivalents and browser evidence. Check controller/keyboard operation, nested modals, safe areas, localization, zoom, scene transitions and state changes while hidden. Test click-through and duplicate subscriptions. Screenshot comparisons cannot prove focus or event ownership. Check the [official GUI guide](https://github.com/BabylonJS/Documentation/blob/master/content/features/featuresDeepDive/gui/gui.md) against the host version.
