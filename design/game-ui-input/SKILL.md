---
name: game-ui-input
description:
  "Build or refine game interfaces and keyboard, controller or touch input from GameGen platform preferences, including
  accessible layouts and simultaneous mobile controls."
---

# Build game UI and controls

Read [shared context](../../references/shared-context.md), ready preferences and the existing interface conventions. Use
input methods, orientation, touch placement and accessibility choices from the saved configuration. Keep product flows
focused on gameplay decisions rather than implementation details.

Design around the actual device viewport and safe areas. Check readable text, contrast, focus states and sufficiently
usable targets. Preserve art identity while keeping HUD information legible over the real world scene. Use non-color
cues and scalable text. Always honor the platform reduced-motion setting, plus the project's saved accessibility
choices. Keep localization and text expansion in mind.

## Input behavior

Route keyboard, controller and touch through common gameplay actions. Support analog magnitude intentionally,
appropriate dead zones and normalized digital diagonals. Release held input on focus loss, pause, scene change and touch
cancellation. Test multiple simultaneous touches so moving and attacking can happen together.

Implement side swapping as a layout change that preserves action semantics, touch ownership and persistence. Check it
both while idle and while a control is held. Prevent menus and overlays from leaving movement stuck or activating
gameplay beneath them. Test gamepad focus and navigation through full modal flows.

For mobile, check landscape variants, safe areas, UI scaling, and on-screen keyboard behavior when text input exists.
Desktop developer controls can remain in a separate review harness; do not ship them as tiny player-facing buttons.

## UI assets and verification

For a cohesive generated UI system through SpriteCook, use `spritecook-workflow-essentials` and
`spritecook-build-ui-kits` so sheets/components share one accepted screen concept. An isolated icon can use the
appropriate configured image route. Preserve labels and interactive semantics in the engine instead of baking important
dynamic text into artwork.

Verify the real HUD, controls, menus and overlays together at the narrowest target layout. Capture the actual engine
state. Test pause/resume, touch release, switching input methods, side swapping, settings persistence and
keyboard/controller navigation when supported.
