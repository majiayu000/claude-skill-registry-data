---
name: game-audio-vfx
description:
  "For GameGen projects, create and integrate game music, sound and visual feedback with coherent style, synchronized
  action timing, accessibility and runtime budgets."
---

# Create sound and visual feedback

Read [shared context](../../references/shared-context.md), ready preferences and the relevant gameplay/animation events.
Use the configured audio and image routes, credit limits and required delivery. Load a provider's audio/video skill only
when it actually matches the requested output. For the `local` audio route, use
[game-audio-procedural](../game-audio-procedural/SKILL.md) for synthesis, sonic identity, loudness, loops and audio
records; this skill still owns the cue list, integration and evidence.

Make a small cue list for the scoped loop: action, success/failure, interaction, ambience, UI and music as appropriate.
Distinguish cues the player needs to react to from decoration. Avoid creating a large library before verifying how the
representative sounds work in-game.

## Sound

Retain editable sources and export runtime formats that suit the target platform. Trim silence deliberately, avoid
clicks at loop boundaries and check levels together in the scene. Use buses for music, effects and UI where useful, with
independent player settings. Check repeated short cues, polyphony, distance falloff and clipping. Match musical loops
and transitions to the intended pacing.

Use original or appropriately licensed material and retain provenance. Generated output does not remove the need to
inspect artifacts, loop quality or the applicable usage terms. Keep purchased assets and service credits within the
approved budget.

## Visual effects

Tie effects and hit/impact feedback to the action-event markers that game-animation records in the manifest, or to
gameplay events that have no animation. Verify the actual contact/apex moment rather than aligning a particle burst only
to the start of a clip. Keep the actor silhouette and gameplay area readable, with clear directional and non-color
information where needed.

Choose particles, meshes, sprites or shaders based on the presentation and renderer. Limit transparent overlap, lights
and emission to the target budget. Test effects on varied backgrounds, at the intended camera size, under repeated
actions and pause/resume. Always honor the platform reduced-motion setting, plus the project's saved accessibility
choices, and flashing constraints.

For Blender-authored effect meshes or rendered particle/simulation sequences, use the
[local CLI workflow](../../references/blender-cli.md). Save the procedural source and bake stateful simulations before
independent frame renders. Export suitable geometry or sprite sheets; author interactive runtime particles and shaders
in Godot as needed rather than assuming Blender's node graphs or simulation caches transfer through GLB.

Provide a short actual engine capture with sound or clear timing evidence. Record source/export paths, cue/event
mapping, loop behavior and any remaining limits. Do not describe a silent render or isolated sound preview as a verified
integrated mix.
