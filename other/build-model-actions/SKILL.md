---
name: build-model-actions
description: Compose reviewed animation clips into ordered model actions with transitions, timed effects and selected-engine playback. Use for dance patterns, prescribed combinations, charge/cast sequences and action-level revisions or review.
engines: [AGNOSTIC]
---

# Build Model Actions

## When to use

Use when several individual clips must play as one named sequence with coordinated model-attached effects. Use MODEL_TO_ANIMATION for creating or retargeting the individual clips; use the engine gameplay/ability owner for authoritative combat, targeting and movement.

## Workflow

1. Resolve ENGINE.md, this skill and applicable engine skills. Read STYLE.md and `.styles/.workflows/model-to-action/WORKFLOW.md`; keep the primary art pipeline and engine selection intact.
2. Inspect source motion readiness and rights. Preserve the exact model/rig/clip package and human selection evidence. Inspect configured libraries first and work only on project-local copies. Missing source clips route to `build-model-animations` before composition.
3. Read [sequence-contract.md](references/sequence-contract.md) and record action-phase intent before authoring the native recipe. Define explicit trims, rate, repetition occurrence and adjacent blends; resolve every cue/marker against its actual source clip and step. Preserve legacy v1 cues; select recipe v2 explicitly for reviewed reusable effect packages, exact resources/profiles/correspondences and declared transforms, target, trail and lifetime policies. Use native `inspect-effects` for current source subjects/allocation facts; its `accepted: false` result is not a production or acceptance gate.
4. Use `model-to-action.sh` for native inspect, compose, export and full review. Preserve hashes and immutable attempts. Require actual compound motion and re-imported exports; do not replace source review with a label, strip inventory or midpoint render.
5. Read [presentation-and-review.md](references/presentation-and-review.md) for rig/clock ownership, attached effects and target/outcome presentation. For THREEJS v2 read `./.hephaera/.engine/threejs/actions/README.md` and use actual delivered clips/anchors with fresh native source-export admission. Explicitly choose review/runtime admission and rehearsal/host-outcomes playback. Integrate through the compatible engine owner and record actual playback, interruption and resource evidence.
6. Record action selection, independent review and separate human runtime acceptance. Validate current ancestry and promote only with explicit task authority and current evidence. Revisions invalidate affected outputs/acceptance; preserve previous attempts.

## Output

- Actual compound animations, editable source and an explicitly versioned `hephaera-action-package/v1` or `/v2` timeline. V1 retains its original reader, cues, timing and historical primitive backend; v2 binds the complete native effect closure and shared Three.js/Quarks scheduler.
- Original clip ancestry, resolved steps/markers/cues, actual engine integration and full-sequence evidence.
- Separate review/runtime acceptance and explicit promotion history.

## Guardrails

- The initial shared composer requires in-place source clips. Route extracted movement to an explicitly supported controller adapter or author a reviewed in-place counterpart.
- The host arbitrates one presentation owner for the rig; this workflow adds no implicit IK, upper-body layer or authoritative aiming/combat system.
- Fixed-target projectiles and markers are presentation. Gameplay owns collisions, hits, damage, costs, cooldowns, travel and target validation.
- V2 borrows one Scene FX owner/clock; actor pause/cancel cannot globally pause/clear unrelated effects. Bound the union of actors, ambient FX and tails, with explicit exceptional/hidden/resume policy and no backlog replay. Release rig writes at motion end while bounded tails finish; hard interruption retires the generation.
- Use the actual read-only native source-export admission helper. Runtime mode requires current native action/independent/human approvals; it does not grant promotion or implement verification of promoted/rebound destination packages. Receiving metadata remains pending native review. Read `./.hephaera/docs/MODEL_TO_ACTION.md` for the technical guide.
- Use only fixed audited/hash-bound Blender composition scripts on working copies. Missing prerequisites remain blocked; never select a fallback, install software or claim another engine's acceptance silently.
- Adobe integrations remain excluded. Models, providers, uploads, paid libraries and license acceptance remain separate decisions.
