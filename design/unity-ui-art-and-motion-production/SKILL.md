---
name: unity-ui-art-and-motion-production
description: Use when new or revised Unity UI visuals, icons, panels, 9-slice sprites, component states, HUD or menu layouts, popup motion, screen transitions, or flattened UI screenshot decomposition must be produced through Figma and integrated into uGUI, NGUI, or UI Toolkit; not for UI debugging, localization-only work, character animation, or general art-pipeline audits.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [unity]
  versions: [2021.3+, 2022.3+, 2023.2+, 6000+]
  platforms: [windows, linux, macos, console, mobile, web]
metadata:
  studio:
    type: workflow
    lifecycle_stage: build
    risk_level: medium
    packs: [content-production]
    side_effects: files
    artifact: ui-art-motion-production.json
    required_evidence: [figma-revision, design-brief, decomposition-manifest, asset-manifest, motion-manifest, art-qc, import-plan, runtime-evidence]
    owner: HoaTV Studio
    reviewer: Art Lead
    maturity: experimental
    last_reviewed: 2026-08-21
    provenance:
      derived_from:
        repo: 50kg/image-to-slice
        path: src/core/slice-detection/prompt-builder.js; src/core/background-decomposition/prompt-builder.js; tests/ui-ai-inpaint-results.test.js
        commit: 402c20542f73e41f2393b6dfe3a5096c8c1a9521
        license: MIT
      patterns_from: [Figma export provenance, Unity UI import evidence, safe-project-mutation, image-to-slice decomposition and repair contract]
      copied_text: none
---
# Unity UI Art and Motion Production

## Overview

Turn an approved Figma visual direction and, where permitted, AI-assisted raster
art into Unity UI assets and small, readable UI motion. Figma owns approved
visual intent; Unity owns runtime layout, state, input, accessibility, and
performance behavior. The workflow supports uGUI, NGUI, and UI Toolkit in one
evidence contract and remains `experimental` until governed studio dogfood is
observed.

## When to use

Use for new or revised HUDs, menus, panels, icons, 9-slice frames, atlas-ready
sprites, component states, popup transitions, screen transitions, and UI
micro-motion with an identified Unity stack. Use it also when a flattened or
AI-generated UI screenshot must be decomposed into reviewed raster/native UI
candidates before Figma export. Read `references/design-brief.md`
before generating or iterating visual candidates, `references/figma-ai.md` when
the visual source or AI provenance is in scope, and
`references/flattened-ui-decomposition.md` for screenshot decomposition, and
`references/visual-iteration.md` when a candidate needs bounded variants or
static QC. Read the stack-specific reference (`ugui.md`, `ngui.md`, or
`ui-toolkit.md`) before selecting import settings or motion drivers.

## When NOT to use

Do not use for diagnosing an already invisible or clipped UI item (route to
`unity-ui-rendering-debugging`), character or skeletal animation, general art
asset preflight, localization authority, gameplay logic, 3D assets, shaders,
non-UI VFX, package installation, bulk reimport, bundle publishing, or a
runtime PASS without runtime evidence.

## Required inputs and context discovery

Collect project and Unity identity, active stack(s), design brief, optional source screenshot and
decomposition manifest, Figma file/page/node and
revision, approved component/variant/token references, export files and
SHA-256 hashes, AI provider/model/prompt/reference/output provenance when used,
target prefabs or UXML/USS/controller paths, owners, reviewer, dependency
state, performance tier, reduced-motion requirement, baseline hashes, backup
root, restore objective, and exact verification commands. Treat missing Figma
access, export hash, rights, Unity project, or runtime runner as `BLOCKED`.

## Safety and risk level

This is a medium-risk file workflow. Default to report-only planning. Use the
bundled Python 3.11+ helpers (`scripts/ui_art_motion.py` and
`scripts/ui_art_qc.py`) with `jsonschema` to validate the closed design brief,
asset, and motion manifests, bind source exports to hashes, detect or explicitly
select one stack, and emit a stable plan digest plus static art-QC report. Apply
only through `safe-project-mutation` after a reviewer,
backup/restore manifest, baseline, and exact target scope are recorded. Never
install DOTween, LeanTween, Rive, Spine, or another tween/runtime package.

## Workflow

1. **Write the design brief.** Bind goal, format, layout hierarchy, type system,
   color/material language, references, exact copy policy, negative constraints,
   and one-variable variants. Completion criterion: the closed design-brief
   schema passes and a reviewer can identify the visual system.
2. **Bind visual authority.** If a flattened screenshot was used, validate the
   decomposition manifest first: source hash/dimensions, original-pixel bboxes,
   raster/native decisions, overlay intersections, retained restoration
   variants, and reviewer approval. Then capture the Figma revision, component states,
   tokens, export names, rights, and reviewer; record AI provenance and hashes.
   Completion criterion: `figma-ai.md` evidence is complete or the item is
   explicitly `BLOCKED`.
3. **Preflight the export.** Validate dimensions, alpha, color space, scale,
   pivot, 9-slice borders, atlas group, compression, ownership, and safe
   source/target paths against the asset manifest schema.
   Completion criterion: every export hash matches and no target escapes the
   approved project root.
4. **Choose the Unity stack.** Detect uGUI, NGUI, and UI Toolkit markers; if
   more than one is present, require an explicit stack selection and matching
   manifests.
   Completion criterion: exactly one stack and one source revision are bound.
5. **Author state and motion.** Define states, triggers, interruption,
   reduced-motion behavior, duration, easing, driver, and verification cases.
   Prefer Animator/AnimationClip, existing NGUI components, USS transitions,
   or a project controller according to the stack. External tween drivers are
   allowed only with evidence that the dependency already exists.
   Completion criterion: motion manifest validates and contains no installation
   request.
6. **Review the report-only plan.** Sort operations, record baseline hashes,
   conflict/duplicate targets, restore actions, dependency evidence, and the
   deterministic plan digest. Share the plan with the named reviewer.
   Completion criterion: the reviewer approves the exact manifest and scope.
7. **Apply through the safety gate.** Run report-only first, create the backup
   manifest, then apply only the reviewed operations using
   `safe-project-mutation`; do not edit generated helper copies by hand.
   Completion criterion: after-hashes and restore paths match the manifest.
8. **Verify static and runtime behavior.** Run design-brief/art-QC and
   stack-specific static checks, import/build checks, screen-size and
   reduced-motion scenarios, interruption
   scenarios, and performance sampling. Record screenshots/video, logs, device
   tier, sample count, and known limitations.
   Completion criterion: output hashes, runtime evidence, and acceptance
   criteria are all present; otherwise return `BLOCKED`.

## Motion policy

Use the native driver matrix: uGUI permits Animator, AnimationClip, or a
project controller; NGUI permits existing NGUI tween components, AnimationClip,
or a project controller; UI Toolkit permits USS transitions or a project
controller. A DOTween/LeanTween entry must name existing dependency evidence;
the workflow never adds that dependency. Keep micro-motion short, interruptible,
reduced-motion aware, allocation-free in repeated paths, and within the
declared budget.

## Evidence and output contract

Produce `ui-art-motion-production.json` with identity, scope, owners, Figma
revision, design brief, asset and motion manifests, static art-QC report, plan
digest, baseline/after hashes, backup and restore paths, static/runtime commands
and exit codes, screenshots
or video, performance evidence, Verified facts, Snapshot assumptions,
Unverified hypotheses, BLOCKED items, limitations, reviewer decision, and next
actions. A plan is not proof of an applied or runtime-successful change.

## Handoff contract

Record repository and project path, branch, goal, owned scope, do-not-touch
scope, files changed, generated resources, commands and exit codes, evidence
artifacts, restore command, reviewer, blockers, unresolved risks, next owner,
and a reactivation prompt.

## Pitfalls and anti-rationalization

- Missing Figma/AI/Unity/runtime evidence is `BLOCKED`, never PASS.
- Do not treat a screenshot, compile result, or plan digest as proof of full
  device coverage or motion quality.
- Do not overwrite source exports, localization authority, unrelated gameplay,
  or generated adapters.
- Do not broaden the scope from UI art/motion into character, 3D, shader, or
  non-UI VFX production.

## Verification checklist

- [ ] Figma revision, rights, reviewer, and AI provenance are recorded.
- [ ] Optional decomposition source hash, original-pixel bboxes, overlay masks,
  restoration variants, and human review status are recorded.
- [ ] Design brief, prompt lineage, variant status, and negative constraints are recorded.
- [ ] Both manifests pass closed-schema validation and source revision parity.
- [ ] Static art QC passes dimensions, alpha, text policy, and variant checks.
- [ ] Export and target paths are contained, unique, and hash-bound.
- [ ] One stack and an approved native/existing driver are selected.
- [ ] Report-only digest, baseline, backup, and restore evidence exist.
- [ ] Static/runtime/performance evidence is fresh or explicitly BLOCKED.
- [ ] No package installation, bulk reimport, localization edit, or publish occurred.

## References and scripts

- `references/figma-ai.md`: visual authority, export and AI provenance.
- `references/flattened-ui-decomposition.md`: screenshot classification,
  original-pixel bboxes, background repair, and variant retention.
- `references/design-brief.md`: design-system prompt structure and variant contract.
- `references/visual-iteration.md`: bounded variants, static art QC, and evidence boundary.
- `references/ugui.md`: Canvas, Sprite/Atlas, Animator, and uGUI runtime checks.
- `references/ngui.md`: UIPanel/atlas/tween component checks.
- `references/ui-toolkit.md`: UXML/USS, transition, panel settings, and runtime checks.
- `scripts/ui_art_motion.py`: isolated report-only manifest planner and verifier.
- `scripts/ui_art_qc.py`: isolated design-brief and static export QC helper.
