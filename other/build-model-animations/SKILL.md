---
name: build-model-animations
description: Produce reviewed skinned, articulated, rigid or mechanical assembly animation packages through native Blender authoring or compatible motion retargeting. Use for MODEL_TO_ANIMATION preparation, clip revisions, runtime handoff and motion/effect verification.
engines: [AGNOSTIC]
---

# Build Model Animations

## When to use

Use after model production when an asset needs rigging/hierarchy preparation, a motion set, retargeting, complete motion review or selected-engine animation/effect handoff. Existing engine playback edits may only need that engine's animation skill.

For a dance pattern, chained combination or charge/cast sequence assembled from reviewed clips, use `build-model-actions` after individual clip production. Keep source clip ancestry and separate composed-action review; missing source clips return here for authoring or retargeting.

## Workflow

1. Resolve the project engine and this skill; read architecture, STYLE.md and `.styles/.workflows/model-to-animation/WORKFLOW.md`. This downstream workflow does not replace the primary art pipeline, select another engine or install dependencies.
2. Preserve the reviewed model and editable source ancestry. Inspect configured libraries first and use only project-local copies. Read [motion-profiles.md](references/motion-profiles.md) to choose skinned, articulated, rigid or preserve-only mechanical assembly ownership, assess actual readiness and record a short motion-intent brief before authoring or retargeting.
3. Inspect command help and use `model-to-animation.sh` for native operations. Supply explicit rights, recipe, coordinates, actual required clips, budgets and the existing Blender4.5 installation. No provider-specific auto-rigging, hidden downloads or Adobe integration is available.

   For reviewed SCHEMATIC_TO_MODEL assemblies, initialize the `mechanical-assembly` profile with the exact reviewed `--handoff` and rest `--model`, including assemblies with zero flexible rigs. Preserve every component, pivot, hierarchy and any separately owned flexible rig. Current package/review/source-state hashes are required; diagnostic motion and input review create no downstream approvals. This profile preserves rigs and rejects retargeting or new rig creation. Inspect hidden hardware through the bound editable assembly or suitable isolated/sectioned views before making a visual acceptance claim.
4. Inspect/prepare the model and author or preserve its real rig/hierarchy. Review fit, joints, weights, independent mechanical parts/pivots and anchors. Record current rig approval before authoring or retargeting.
5. Author declared motion or retarget explicitly mapped owned/cleared source clips. Keep original clip rights, rest-axis corrections and skeleton identity. Use targeted `author --revision JSON` when supported; preserve unaffected motion hashes and previous attempts rather than replacing the set silently.
6. Bake, export and independently re-import actual channels, actions and bindings. Read [review-and-delivery.md](references/review-and-delivery.md) for full-range clip/transition review and separate motion, independent and human runtime acceptance. Passing inventories or a midpoint still cannot accept a motion set.
7. Read [engine-presentation.md](references/engine-presentation.md) for the selected engine handoff, controller ownership, speed parameters and warp/effect phases. Resolve compatible engine skills before APIs or native tooling; actual runtime results remain required.
8. Validate current hashes and applicable evidence, retain failed/revised attempts, then promote only with explicit task authority and current independent/human acceptance. Missing prerequisites remain blocked/not-run; never fabricate native success or switch authoring/provider paths silently.

## Output

- Immutable source/model/rig/clip ancestry and a profiled `hephaera-motion-package/v1` package.
- Editable Blender source, real baked/exported animation, complete motion review frames and declared sample/renderer limits.
- Selected-engine motion/effect implementation, actual runtime/performance evidence and separate acceptance/promotion lineage.

## Guardrails

- Rigid vehicles do not require fake skins, combat clips or combat colliders. Preserve old rigged-actor/v1 consumers and use the profiled motion contract where appropriate.
- Only the workflow's fixed audited/hash-bound Blender batch scripts may author declared working copies. This does not expand standalone BLENDER or PROOF_TO_MODEL exceptions.
- Animation and VFX do not independently decide movement, collisions, damage, death or travel arrival. Apply extracted root motion through the controller once.
- Adobe products/services/adapters and declared excluded source providers are unsupported. Optional nonexcluded tools or libraries need separate audit/selection; approval of a workflow is not license acceptance, upload permission or spending authority.
