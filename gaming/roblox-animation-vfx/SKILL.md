---
name: roblox-animation-vfx
description: "Use when adding, changing, or fixing Roblox animations, particles, beams, trails, tweens, camera shake, or other visual effects."
when_to_use: "Also when an effect is invisible, too weak, laggy or doesn't clean up, an animation won't play or blend, and when reviewing game feel or hit feedback."
last_reviewed: 2026-10-14
sources:
  - https://create.roblox.com/docs/reference/engine/classes/AnimationTrack
  - https://create.roblox.com/docs/animation/using
  - https://create.roblox.com/docs/reference/engine/classes/Animator
  - https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter
  - https://create.roblox.com/docs/effects/particle-emitters
  - https://create.roblox.com/docs/tutorials/use-case-tutorials/vfx/create-volcanoes
  - https://create.roblox.com/docs/tutorials/use-case-tutorials/vfx/create-waterfalls
  - https://create.roblox.com/docs/reference/engine/classes/TweenService
  - https://create.roblox.com/docs/projects/server-authority
  - https://create.roblox.com/docs/projects/server-authority/techniques
  - original
  - https://raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/reference/engine/classes/Instance.yaml
---

# roblox animation and vfx

## When to Load

Load when implementing character animation, particle or beam effects, tweens, camera feedback, or visual cleanup.

## Quick Reference

- Load tracks through an `Animator` on a `Humanoid` or `AnimationController`; set `AnimationTrack.Priority` deliberately.
- Use `GetMarkerReachedSignal()` for named gameplay or presentation cues, then disconnect or replace the listener when the track ends.
- Track lifecycle: `Ended` is post-fade cleanup; `Stopped` includes explicit stops. Same-priority tracks blend by weight; see full.md for control and loading guards.
- A burst `ParticleEmitter` usually has `Rate = 0` and uses `:Emit(count)` with a bounded lifetime; use pooling for frequent effects.
- Shape each effect as readable phases: warning, contact, brief peak, and fade. Give impact a clear silhouette before adding secondary particles, light, sound, or camera feedback.
- Use native particle flipbooks for animated textures; choose OneShot for a single impact or vary start frames for organic repetition. Custom mesh/image flipbooks may need their own playback code.
- Beams and trails need two attachments with a stable world-space relationship and a cleanup owner.
- Tween a bounded set of properties with `TweenService:Create`; cancel or destroy temporary effects when their owner ends, and use `Debris:AddItem` for simple lifetimes.
- In Server Authority projects, keep synchronized animation logic in `RunService:BindToSimulation()` (requires `Workspace.UseFixedSimulation` enabled in Studio), query current tracks instead of caching handles across rollback, and make predicted effects reversible.
- Profile particle counts, lights, post-processing, and per-frame camera work on the target device class.

**Need the details?** Load `references/full.md` for animation and effect recipes.
