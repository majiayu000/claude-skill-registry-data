---
name: animation-systems
description: Use when designing, speccing, or reviewing a character/object motion system in ANY engine — the rig and skeleton, skinning (linear blend vs dual-quaternion, the candy-wrapper artifact), forward vs inverse kinematics, IK solvers (two-bone, FABRIK, CCD, look-at), blend trees and blend spaces (1D/2D), animation state machines, additive layers and upper/lower-body splits, ragdoll and active ragdoll, procedural IK foot placement on uneven terrain, secondary motion (spring bones, cloth, hair), motion matching, animation compression and bone-count budgets, root motion vs in-place, and the anticipation/active/recovery timing decomposition with animation-canceling. Also use to diagnose feet that slide or float, a mesh that pinches when it twists, blends that pop or moonwalk, characters that feel animation-locked, or a motion library that blows the memory budget. Triggers on "animation system", "skeletal animation", "skinning", "candy wrapper", "dual quaternion", "rigging", "inverse kinematics", "IK", "foot placement", "blend tree", "blend space", "animation state machine", "additive animation", "aim offset", "ragdoll", "active ragdoll", "spring bones", "jiggle physics", "secondary motion", "motion matching", "animation compression", "root motion", "foot sliding", "animation canceling", "animation locked".
---

# Animation Systems

How to architect the motion system that makes a character or object move: the rig and skinning underneath, the blend/state machine/IK layer that composes authored motion, the procedural and physics-driven layer that makes it fit the world, the compression/cost model that ships it, and the timing decomposition that delivers correct anticipation and follow-through at scale.

> **Tier:** technical craft (→ `gamestack-core`). Engine-agnostic motion-system architecture, the implementation layer under game-feel-and-juice's animation-timing principles.

## When to use this

- Speccing a character motion system: rig, skinning method, blend architecture, IK, procedural/physics motion
- Choosing between authored state machines, blend spaces, and motion matching for a given motion space
- Making generated characters/creatures move plausibly from a finite hand-authored clip+rig library
- Diagnosing sliding/floating feet, a twisting mesh that pinches, popping or moonwalking blends, animation-locked controls, or a motion library over the memory budget

## Scope

This skill owns **the architecture of the motion system** — rig, skinning, blending/state machines/IK, procedural and physics-driven motion, the compression/cost model, and the `(anticipation, active, recovery)` clip decomposition that delivers timing. Adjacent concerns live in sibling skills:
- The *design rules* for animation timing — the player-vs-enemy anticipation inversion, follow-through as weight-without-recovery-cost, squash/stretch, the 12 principles, the responsiveness ceiling → `game-feel-and-juice` (this skill cites *up* to it and implements it)
- Combat-specific application — telegraphing as fairness, hit-stop per damage tier, enemy/encounter feel → `combat-design`
- Pose silhouette, readability, signal color → `art-direction-and-readability`
- The rendering substrate for motion VFX (trails, dissolves, rim-light) → `shaders-and-vfx`
- Generated *content/narrative* coherence (vs generated motion) → `procedural-generation` / `procgen-review`

## How the pieces fit

- **`GUIDE.md`** — the cited *why*, in five sub-domains: skeletal fundamentals (skinning ladder, FK vs IK, solver-per-chain), blending & state architecture (blend trees/spaces, state machines, additive layers, upper/lower split), procedural & physics-driven motion (active ragdoll, foot-placement IK, spring bones, motion matching), the pipeline & cost model (bone budget, compression, root motion vs in-place), and readability & timing (the `(anticipation, active, recovery)` triplet, animation-priority vs cancellable). Each rule carries an exemplar + source, a **test-for** criterion, the named failure mode, and the **procedural/headless implication**.
- **`CHECKLIST.md`** — Do/Don't + machine-checkable **Test-for** criteria, grouped by sub-domain. Written to be enforced as validators in a generation loop.

## The two ideas to anchor on

> **1. Every motion technique is a cost/quality dial — pick per-case, not globally.** Skinning (LBS → DQS → Centers of Rotation), IK solvers (analytical two-bone vs iterative FABRIK/CCD), root motion vs in-place, authored graph vs motion matching — each has a cheap default, a costlier upgrade, and a named artifact when misapplied. Choose by the joint, the chain, the clip, and the motion space — never one setting for the whole character.

> **2. Generation composes a finite hand-authored library — it never invents the contract.** The rig, the skinning method, the clip set, the blend-space axes, the IK/spring parameters, and the per-action timing signatures are hand-authored contracts. A generator *selects and warps* within them (retarget clips, blend, IK-correct, motion-match) to make many characters move — but it must not invent bone counts, timing signatures, or uncapped physics. Skinning collapse, foot-slide, and phase-mismatched blends are invisible to a headless generator, so the contracts are enforced by validators.

> **Why this matters doubly for a generator:** a human animator sees a pinched wrist, a skating foot, or a moonwalking blend instantly; an autonomous generator does not. Hand-author the rig + clip library + blend/IK/timing parameters as inviolable contracts; let generation compose vetted parts inside them; run the rig/skin, blend-set, cost, and animation-state validators before any content is committed.

Start with `GUIDE.md`, then apply `CHECKLIST.md`.
</content>
