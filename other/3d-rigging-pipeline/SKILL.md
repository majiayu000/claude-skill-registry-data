---
name: 3d-rigging-pipeline
description: >
  Headless Blender/bpy authoring pipeline for character rigging, corrective shape keys, cross-armature retargeting, and glTF export compression — the AUTHORING half of SkyyRose's 3D character pipeline. Use when doing headless Blender/bpy rigging, fixing a skin-weight or shape-key defect, retargeting (or gating whether to retarget) a skeleton onto a new character, or exporting/compressing a rigged GLB for the mascot, Love Hurts Girl, or any future SkyyRose character. Do NOT use for runtime morph-target wiring during three.js playback (that is `threejs-animation`), and do NOT use for post-export visual fidelity grading of a finished render (that is the render-QA / mockup-pipeline skills).
---

# 3D Rigging Pipeline (Blender/bpy Authoring)

## Scope boundary — read this before anything else

- **This skill = AUTHORING.** Headless Blender/bpy: computing, baking, and exporting a
  correction or a rig.
- **`threejs-animation` = RUNTIME.** Wiring morph-target influence during three.js playback
  in the browser. It already names this skill by this exact name for the Blender-side half
  of the same problem (`threejs-immersive.md` in `skyyrose-wp-platform` cross-references it).
- **Render-QA / mockup-pipeline skills = POST-EXPORT.** Output-fidelity grading after a GLB
  already exists.
- Hand off at the GLB file boundary. Never duplicate another skill's half of the problem.

## When to use

Use when any of these is observably true:

- A `.blend` or `.glb` under `renders/3d/` needs a rig, a re-weight, a corrective shape key,
  or a re-export — e.g. `renders/3d/girl-love-hurts/love-hurts-girl-rig.blend`.
- A mesh shows LBS candy-wrapper collapse, an armpit/elbow crease defect, or a shape key
  leaking a nonzero rest weight into the exported GLB.
- You are about to retarget a walk/idle clip from one armature onto another and have not yet
  run the rest-direction precondition gate.
- A rigged GLB is about to ship and has not been draco-compressed / texture-normalised.

**Do NOT use when:**

- The defect appears only during browser playback and the GLB itself is clean — that is
  `threejs-animation` (runtime morph wiring), not this skill.
- The question is "does this render look like the right garment/character" — that is the
  render-QA / product-image-fidelity gate, which reads pixels, not bones.
- You only need to *view* a GLB. Reading a file is not authoring.

## Inputs

| Required before starting | How to confirm it | If absent |
|---|---|---|
| The target `.blend` / `.glb`, by real path | `ls -la renders/3d/<character>/` | **STOP.** Never author against a path you have not listed. Never create a placeholder mesh to "unblock". |
| A reference/backup of the pre-edit file for any non-idempotent script | `ls renders/3d/<character>/*backup*.blend` + `md5` | **STOP.** `add_armpit_gusset.py`-class scripts are non-idempotent; a blind re-run silently double-applies. |
| Blender available headless, when a step imports `bpy` | `blender --version` | **STOP** for that step. The pure-python gates in `scripts/` do NOT need Blender and can still run — say which half is blocked, do not report the whole task blocked. |
| `npx @gltf-transform/cli` reachable, for export checks | `npx @gltf-transform/cli --version` | **STOP** the export-verify step. A bare `gltf-transform` binary does NOT resolve in this environment — it maps to a different, nonexistent npm package. |

Absent input is a stop, never a default. A gate that runs against a substituted input is the
fail-open pattern (bug-230, ×6).

## Procedure

1. **Read the doctrine first.** `reference/doctrine.md` — numeric gates only (a printed number
   from a real run this session), and verification from a source structurally independent of
   whatever produced the artifact. No harness grades its own output.
2. **List the real files.** `ls -la renders/3d/<character>/` — every later claim cites a path
   from this listing, not from memory or a prior writeup.
3. **Re-derive, never inherit.** Any prior "confirmed" number (a gate result, a bone count, a
   pass) is re-run against the CURRENT file before you act on it. See the reuse-vs-re-derive
   table in `reference/love-hurts-worked-example.md`.
4. **Pick the authoring path** and read only its reference file:
   - corrective / pose-driven shape keys → `reference/shape-keys.md`
   - cross-armature retargeting → `reference/retargeting.md` (run its rest-direction
     precondition gate BEFORE building any constraint — bug-195)
   - export + compression → `reference/export-pipeline.md`
5. **Run the script, headless.** `blender -b <file>.blend -P <script>.py` for bpy steps.
   Non-idempotent scripts: md5 the backup first, then run exactly once.
6. **Gate the result numerically** with the independent checkers in `scripts/` (below).
   A printed number, not an eyeball.
7. **Record the outcome** — bug id, script, numeric result — in `.wolf/buglog.json` and
   `.wolf/memory.md` in the same change as the fix.

### Quick start — locating a mesh's shape keys in bpy

```python
import bpy
mesh_obj = bpy.data.objects["YourMesh"]
if mesh_obj.data.shape_keys:
    for kb in mesh_obj.data.shape_keys.key_blocks:
        print(kb.name, kb.value)  # kb.value == REST/default weight -- must be 0.0 unless
                                   # this key is deliberately held active for a full clip
```

This is illustrative only — the full corrective-shape-key computation is in
`reference/shape-keys.md`, not here.

## Verification

Two independent checks. Both are pure-python/CLI and share no code with the Blender export
path, per `reference/doctrine.md`'s independent-authority rule.

1. Export-contract gate — the discriminating one:

```bash
cd /Users/theceo/DevSkyy && python3 \
  .claude/skills/3d-rigging-pipeline/scripts/gltf_export_verify.py \
  renders/3d/girl-love-hurts/love-hurts-girl-v1.glb \
  --width 1024 --height 1024 --format jpeg --require-draco
```

**PASS:** prints `PASS` and exits 0 — `KHR_draco_mesh_compression` present in
`extensionsUsed`/`extensionsRequired` AND every texture reported at 1024x1024 `image/jpeg`.
Evidence: `[repro]`

2. Shape-key rest-weight gate — parses the GLB JSON chunk directly, never imports bpy:

```bash
cd /Users/theceo/DevSkyy && python3 \
  .claude/skills/3d-rigging-pipeline/scripts/assert_shape_key_rest_weight.py \
  renders/3d/girl-love-hurts/love-hurts-girl-v1.glb
```

**PASS:** exits 0 AND the `Checked N` count is greater than 0 with every rest weight `0.0`
(or matching a declared `--expect-nonzero` override). `Checked 0` is NOT a pass — see the SKIP
rule below. Evidence: `[repro]`

**A SKIP is not a PASS.** `Checked 0 shape-key rest weight(s) … PASS` means the file carries no
shape keys at all: the parser ran, nothing was proven. Treat that as SKIP, name the rigging
author as the person who closes it against a GLB that *does* carry shape keys, and never let it
stand in for check 2.

**A gate that dies is not a gate that passed.** If `npx` times out, the network is down, or
Blender segfaults, the zero-findings output is an artifact — re-run by hand before claiming
anything (bug-230).

**Attribute before claiming a finding is yours.** A defect found in a `.glb` you just rebuilt may
predate your change. Extract the pristine tree and re-run the same gate against it:
`git archive HEAD renders/3d/<character> | tar -x -C <scratch>`. **Never `git stash`** — the
stash stack is shared across worktrees.

## Worked example

Run against the real Love Hurts Girl export, 2026-07-28, in `/Users/theceo/DevSkyy`:

```bash
$ ls renders/3d/girl-love-hurts/*.glb
renders/3d/girl-love-hurts/girl-mascot-raw.glb                 25.5M
renders/3d/girl-love-hurts/girl-mascot-raw.walk-dwell-fix.glb  25.5M
renders/3d/girl-love-hurts/love-hurts-girl-v1.glb              25.5M

$ python3 .claude/skills/3d-rigging-pipeline/scripts/gltf_export_verify.py \
    renders/3d/girl-love-hurts/love-hurts-girl-v1.glb \
    --width 1024 --height 1024 --format jpeg --require-draco
… ANIMATIONS
  0  GirlWalk_Baked   72 channels  72 samplers  duration 1  374 keyframes  5.61 KB
  1  GirlWalk_Source  72 channels  72 samplers  duration 1  374 keyframes  5.49 KB

FAIL -- 3 check(s) did not match:
  KHR_draco_mesh_compression not found in extensionsUsed/Required
  no texture reported at 1024x1024 resolution
  no texture reported with mimeType image/jpeg
```

Two things this proves at once. **(a)** `love-hurts-girl-v1.glb` is a raw, uncompressed export —
25.5 MB, no draco, textures never normalised. It is not shippable to the web as-is; run the
`reference/export-pipeline.md` compression sequence before any theme wires it. **(b)** The gate
itself can return red on a real file — that is rule 3 satisfied by observation, not by assertion.
`[repro]`

The companion run is the honest counter-case:

```bash
$ python3 .claude/skills/3d-rigging-pipeline/scripts/assert_shape_key_rest_weight.py \
    renders/3d/girl-love-hurts/love-hurts-girl-v1.glb
Checked 0 shape-key rest weight(s) in …/love-hurts-girl-v1.glb:

PASS -- all rest weights are 0.0 or match a declared --expect-nonzero override.
```

`Checked 0` — this GLB has no shape keys, so the "PASS" proves the parser executes and nothing
more. Reporting it as a rest-weight pass would be exactly the fail-open defect this skill exists
to prevent. Recorded as SKIP, owner = rigging author, closed only against a shape-keyed GLB.
`[repro]`

## Failure modes

| Symptom | Root cause | Do this |
|---|---|---|
| `gltf-transform: command not found` | The bare binary maps to a different, nonexistent npm package | Always invoke the scoped package: `npx @gltf-transform/cli inspect <file>` (documented in `scripts/gltf_export_verify.py`'s docstring) |
| Retarget produces twisted limbs even though both armatures have identical bone names/hierarchy | Hierarchy match ≠ rest-direction match | **bug-195** — run `renders/3d/girl-love-hurts/gate_bone_direction.py` FIRST. It failed 15/24 bones on this very pair; the build correctly pivoted to a hand-keyframed clip instead of retargeting |
| Skin-weight self-check reports FAIL on monotonic transitions that are monotonic by construction | Verification sampled ALL vertices with nonzero weight on a bone, mixing two independently-monotonic populations | **bug-196** — filter samples to the same chain/segment classification the weighting pass used. A verification checking its own sampling assumption is the self-grading trap |
| A gusset/mesh edit appears applied twice | `add_armpit_gusset.py` is non-idempotent, and "pre-existing vertices" recomputed as `len(v.groups) > 0` silently widens after run 1 | md5 against `*.pre-gusset-backup.blend` before any re-run; persist the marker as a custom ID property and read it back rather than recomputing |
| Shape key visibly applied at rest in the browser | Nonzero rest weight leaked through export | Run check 2 above; fix in Blender, re-export, re-run — do not compensate at runtime |
| A cited "9-phase plan" or "bug-215" | Fabricated citations — neither exists anywhere in this repo | Delete the citation. `reference/love-hurts-worked-example.md` documents both corrections |

## What this skill will not do

It will not assert a bug ID, a script's behavior, or a "confirmed" numeric result that wasn't
re-derived from a real file or a real script run in the session that touched this skill. Every
reference file says explicitly which of its claims are grounded on-disk and which are flagged as
unverified — carry that distinction forward, don't flatten it.

## Reference files

| Read this | For |
|---|---|
| `reference/doctrine.md` | The numeric-gate + independent-verification rule every other file inherits |
| `reference/shape-keys.md` | Corrective/pose-driven shape keys for LBS candy-wrapper collapse, plus the rest-weight-leak export assertion |
| `reference/retargeting.md` | Local-Space Copy Rotation retargeting AND the mandatory rest-direction precondition gate that a real run already needed |
| `reference/export-pipeline.md` | The confirmed gltf-transform compression sequence and its `--formats` gotcha |
| `reference/love-hurts-worked-example.md` | The actual, currently-on-disk Love Hurts Girl build — real scripts, not a fabricated phase count |

`scripts/` holds the runnable checks each reference file calls out by name:
`assert_shape_key_rest_weight.py`, `gltf_export_verify.py`, `lbs_numeric_gate.py`,
`retarget_local_space_gate.py`.
