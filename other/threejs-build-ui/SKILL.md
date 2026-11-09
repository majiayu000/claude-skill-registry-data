---
name: threejs-build-ui
description: Implement Three.js game HUDs, world anchors and browser interface adapters with accessible equivalents and consistent input ownership.
engines: [THREEJS]
---

# Build Three.js UI

## When to use

Integrate game interfaces with Three.js cameras, picking and scenes. Compose with `build-game-ui` for shared hierarchy and navigation decisions.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh threejs-build-ui`; require compatibility and honor task override scope. Inspect the Three.js version, browser surface, screen contract, scale settings and art pipeline. Three.js has no complete accessible widget toolkit: select DOM, canvas textures or world geometry deliberately without implicitly adding a framework.

## Workflow

1. Use semantic DOM for menus and important controls where appropriate. CSS2D/CSS3D addons and canvas labels are rendering choices, not automatic keyboard/screen-reader support. Match addon revisions to core.
2. Project world anchors through the active camera and viewport. Define behind-camera, offscreen and occlusion policy; clamp indicators to safe areas and support split views. Separate decorations from actionable objects and stable gameplay IDs.
3. Give the top screen/modal sole action ownership. Coordinate DOM focus, pointer capture/lock and picking so menu clicks do not attack. Define controller navigation, cancel/back and focus restoration, including a fallback when the opener disappeared.
4. Bind the HUD to an initial snapshot and bounded updates; unsubscribe on close/unmount. Reopened screens show current state without replaying old notifications. Prompts follow the active player's device and remaps.
5. Separate CSS layout pixels from render pixels. Measure localization, browser zoom, touch targets and high-DPI scaling. Dispose UI textures/materials, anchor observers and DOM listeners according to ownership.

## Output and verification

Deliver screen/input ownership, anchor behavior and state binding with browser evidence. Check keyboard/gamepad operation, modal nesting, resize, long text, hidden objects, camera switching and HUD reopen after state changes. Inspect semantic roles and DOM focus; screenshots alone cannot prove accessibility or event isolation. Use the [Raycaster API](https://threejs.org/docs/pages/Raycaster.html) for world interaction details.
