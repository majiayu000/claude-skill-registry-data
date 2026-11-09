---
name: phaserjs-build-ui
description: Implement Phaser HUD scenes, drawn controls and DOM companions with safe-area layout, focus navigation and synchronized game state.
engines: [PHASERJS]
---

# Build Phaser UI

## When to use

Build Phaser menus, HUDs, modal screens or world prompts. Compose with `build-game-ui` for engine-independent hierarchy and interaction rules.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh phaserjs-build-ui`; require compatibility and honor task override scope. Read the Phaser revision, Scale Manager settings, screen/input contract, browser targets and art pipeline. Use selected host packages; third-party widget libraries and DOM integrations are explicit choices.

## Workflow

1. Choose dedicated HUD/menu scenes, `Text`/`BitmapText`, images and containers, or semantic DOM according to layout/accessibility needs. Containers group transforms, not automatic layout, focus or accessibility. Treat font/atlas load failure explicitly.
2. Define a logical UI coordinate space, viewport/safe-area constraints and resize/orientation policy. A fixed-camera HUD and world-space prompt need different camera/scroll-factor handling. Measure long text, text scale, touch target sizes and localization.
3. Build navigation and focus models for keyboard/controller input. Route actions to the top active modal; coordinate scene Input Plugins and world controls to prevent click-through. Restore focus or a valid fallback after close, scene replacement or data removal.
4. Provide DOM semantic controls/companions for essential drawn interactions when required. Keep labels, values, disabled state and activation synchronized. If using Phaser's `DOMElement`, verify its configured DOM container, scaling and camera limitations in the host revision.
5. Initialize the HUD from a gameplay snapshot and subscribe to bounded updates. Unsubscribe on shutdown; reopen must show current state. Bind prompts to the active player's remapped controls and guard against duplicate event subscriptions after restart.
6. Own UI animations, textures and external listeners; closing a screen cancels its pending effects without resetting unrelated gameplay timers.

## Output and verification

Deliver UI/state adapters and screen/input ownership evidence. Test keyboard-only/controller paths, nested modals, portrait/landscape, browser zoom, long labels and HUD reopen after background state changes. Inspect semantic roles and focus; a screenshot cannot certify navigation or accessibility. Use the [Phaser input contract](https://docs.phaser.io/phaser/concepts/input) and selected version's Game Object APIs.
