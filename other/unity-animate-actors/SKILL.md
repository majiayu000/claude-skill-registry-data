---
name: unity-animate-actors
description: Integrate Unity actor animation with explicit Animator ownership, root motion, gameplay events, and interruption behavior.
engines: [UNITY]
---

# Unity Animate Actors

## When to use

Integrate Unity actor animation with explicit Animator ownership, root motion, gameplay events, and interruption behavior. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-animate-actors` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Record Unity and animation package versions, rig/import settings, available clips, Animator Controller or selected Playables strategy, root-motion policy, simulation clocks and animation budgets. Animation Rigging is optional and must already be selected.

## Workflow

1. Inspect Avatar compatibility, scale, bone mapping, clip import ranges and loop settings. Preserve source model provenance and identify animation-only reimports that could change clips or bindings.
2. Define Animator parameters, states, transitions, layers, masks and blend trees around gameplay state. Name the owner that writes each parameter; avoid competing scripts issuing incompatible transitions.
3. Choose in-place or root-driven movement per state. With root motion, use OnAnimatorMove and the selected controller/physics integration deliberately; do not apply both authored displacement and an independent movement displacement.
4. Separate authoritative action windows from animation-only cues. If Animation Events or StateMachineBehaviour callbacks emit gameplay requests, validate action identity and lifetime so skipped, repeated or interrupted transitions cannot duplicate hits.
5. Specify cancellation, crossfade duration, layer recovery and completion semantics for attacks, death, stun and scene unloading. A disabled Animator or culled actor must not strand an authoritative action.
6. Handle attachments, IK and procedural adjustments in the proper evaluation phase. Pool or release transient objects and remove Playables graphs, callbacks and rig references on teardown.
7. Synchronize sound, VFX and bounded haptic cues through shared event identities. Give each presentation channel an explicit scaled or unscaled clock and keep reduced-motion settings independent of gameplay timing.

## Verification

- Inspect transitions at slow playback and normal speed; test missing clips, incompatible Avatars, interrupted attacks and repeated state entry.
- Check root-motion distance against collisions and moving platforms, then test offscreen culling, pause and Animator disable/re-enable.
- Measure animation CPU and memory on representative actor counts and include native footage of blend seams, feet and attachment alignment.

## Output

Animator/clip/rig configuration, parameter and movement ownership map, interruption and event contracts, native animation captures and performance measurements. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not claim production animation from an imported skeleton alone. New clips, rigging changes or package adoption require their own asset and dependency review. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Unity Animator controllers](https://docs.unity3d.com/6000.0/Documentation/Manual/class-AnimatorController.html). Use the documentation matching the installed project version.
- [Root motion handling](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.OnAnimatorMove.html). Use the documentation matching the installed project version.

