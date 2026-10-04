---
name: godot-gameplay
description:
  "Implement or extend Godot gameplay, actor interactions, progression and persistence using the saved GameGen concept,
  scope and 2D or 3D simulation settings."
---

# Implement Godot gameplay

Read [shared context](../../references/shared-context.md), ready preferences and the repository's existing architecture.
Use current installed Godot documentation for version-dependent APIs. Follow the brief's core loop and scope rather than
importing mechanics from a previous game.

Separate input intent, simulation, presentation and persistent state where that separation helps the actual game. Use
appropriate 2D or 3D physics and world coordinates from presentation settings. A 2.5D camera does not by itself
determine the physics dimension. Reuse existing scenes/resources instead of building a parallel architecture.

## Implement the core loop

Define observable completion and failure/recovery behavior for the scoped experience. Build one interaction or challenge
through input, simulation, feedback and state update before expanding content. Keep tuning data editable and avoid
putting content tables into UI or animation scripts.

Use delta/time-based motion and cooldowns, normalize intended diagonal movement, and keep physics-driven motion in the
appropriate physics update. Camera-relative movement should project onto the intended movement plane. Consume the
root-motion ownership and action-event markers that game-animation records in the manifest for hit windows and action
timing. Gameplay owns hitbox shapes, damage and state rules; when tuning needs a different window, update the marker
through game-animation rather than hard-coding a second timing. Handle collisions and interruption explicitly rather
than relying on visual mesh positions.

Build only the configured network/player mode. For saves, store the required gameplay state with a version and
deliberate recovery behavior. Use an atomic replace/backup strategy suitable to the platform. Keep save migrations and
world restoration behavior consistent with the current scope.

## Integrate and test

Connect the selected actor asset through its import contract. An asset import or animation swap should not silently
change gameplay speed or hitboxes. Use the configured review scene for art iterations.

Test the meaningful loop, collision boundaries, state transitions, repeated inputs, loss/recovery and save/load when
applicable, following the shared verification rules. Deliver a playable scene and concise verification evidence at the
configured delivery stage.
