---
name: 3d-print-workflow
description: Prepare a model file, link or modeling brief for FDM printing through sizing, slicing, authorized printer dispatch and result review. Use printable-modeling when geometry must be created or edited.
---

# Model to physical print

Carry out the requested stage. Recommendations, modeling and workflow setup do not authorize a physical print. Preserve prior authorization for the selected job; do not repeatedly ask to print an already approved object.

For an installed skill, resolve scripts from this actual `SKILL.md` directory. Read adjacent `runtime.local.json` when present to locate the Python used during setup and verify it is still available. Use absolute script/job paths from an unrelated working directory; repository-root examples below are illustrative. Credentials remain local; a WSL/non-Windows interpreter needs an explicit readable Studio configuration path for the optional LAN helper.

## Start from the actual job

Preserve downloaded models and their author/license, selected profile and original files. A model download, editable slicer project and sliced print package are different artifacts. Use the companion `printable-modeling` skill for geometry creation or changes, including a user-uploaded image. Scaling someone else's sculpture is not original modeling.

Use a separate directory in the user's workspace for each job. Preserve existing queues and order; inspection of one job does not authorize another. Record the real printer build volume, nozzle, plate, material and connection method. There is no default owner's printer. For optional Bambu LAN status/camera access, read [bambu-lan.md](references/bambu-lan.md); this adapter is read-only and experimental.

## Prepare and size

For V2 jobs, `scripts/slice_pipeline.py prepare` snapshots the exact mesh,
positioned 3MF, machine/process/filament profiles and launch arguments.
`scripts/run_bambu_slice.py` is the bounded Windows host launcher for the
installed offline Bambu CLI. `slice_pipeline.py collect` verifies its actual
completion and records provenance. These helpers never send a print. Bind the
receipt and actual Studio screenshots through the
[V2 workflow](../idea-to-print/references/workflow-v2.md).

Record purpose, style, dimensions/units and finish requirements. Ask only for missing facts that materially change the result. Show actual rendered mesh previews and preserve editable source with STL/3MF; include STEP only when produced by a CAD engine.

Commands below run from the repository root:

```sh
python skills/3d-print-workflow/scripts/print_audit.py mesh jobs/example/outputs/model.stl --out jobs/example/work/mesh-check.json
python skills/3d-print-workflow/scripts/print_audit.py fit --dimensions 40 50 120 --volume 180 180 180 --clearance 10 10 5
```

The mesh checker reports STL topology and bounds assuming millimetres; STL carries no units. It does not establish self-intersections, minimum thickness, stability or accessible supports, and does not parse general 3MF scene geometry. For a complex 3MF, inspect transformed bounds in the slicer or export the intended object as STL.

Proportional fit uses currently imported dimensions and fixed orientation. `--clearance` is total reserve per axis, not per side. The example volume is illustrative: use the actual printer. Brim, support, purge areas and plate exclusions still require slicer checks. Slicer percentages may refer to the underlying mesh; report before/after dimensions and their ratio.

## Keep scoped validation explicit

For generated or substantially repaired meshes, use the configurable
`scripts/printability_gate.py` and the companion
[refinement reference](../printable-modeling/references/refinement-and-validation.md).
Retain separate geometry, fidelity and slice reports. A tool's topology result
cannot establish resemblance, support removal or unmeasured minimum thickness.
Missing coverage is `UNKNOWN`, not `PASS`. Read each check's method and coverage;
an overall status never expands them.

Configure relevant constraints from the actual part, nozzle, material and use.
Do not make speculative checks or one sculpture's dimensions universal
requirements for every existing model. Reuse current evidence for the exact
mesh/profile; changes invalidate the checks they affect. Required unresolved
manufacturing defects block readiness. Non-blocking limitations remain visible
in the handoff; honor applicable user choices rather than inventing repeated
approval for already accepted scope.

Continue diagnosis, repair and diagnostic slicing where useful. The final
ready state requires the applicable geometry/fidelity/slice evidence and an
explicit account of remaining limitations. Neither a geometry `PASS` nor
a completed slice alone authorizes Send.

## Slice and assess support removal

Match the real printer, nozzle, plate and material. Start with a suitable manufacturer/author profile and change parameters required for the model. Reslice after geometry or size changes.

Inspect actual layers for footprint, isolated starts, thin tips, bridges, seams, support contacts and removal paths. Tree support does not by itself establish easy removal. Consider reorientation or separate parts when support would be trapped. Check support and brim against the printable area, not just object bounds.

Export a uniquely named ready package and audit the selected Bambu plate:

```sh
python skills/3d-print-workflow/scripts/print_audit.py slice jobs/example/outputs/job-ready.gcode.3mf --plate 1 --out jobs/example/work/slice-check.json
```

This offline script reports metadata, material, bed-heat commands and warnings and verifies embedded G-code MD5. It is not a slicer or a machine-compatibility proof. Preserve total/model/support weights when provided. Explain unresolved warnings; never edit metadata to conceal them. Changes to G-code or settings invalidate earlier checks and the prepared dispatch record.

Check the file actually opened in the slicer. For the observed Bambu Studio editable-CLI container being re-sliced on open, read [slice-only.md](references/slice-only.md) and apply its narrowly supported conversion only when appropriate. Do not send changed toolpaths under an earlier artifact's verification.

## Dispatch once and verify

Use an available official printer/slicer send flow. In Codex, use a compatible installed computer-control tool and its instructions for desktop UI; this repository does not supply that tool. Bambu Studio, account/connection setup and printer access are external prerequisites. The included `bambu_read.py` contains telemetry/camera reads and no print, pause, calibration or motion actions; do not invent an untested MQTT start payload.

Before sending, inspect job history and live device state for a prior matching attempt. Require fresh online/idle/no-error state, selected filament and an empty plate established by a clear whole-plate view or the user's explicit confirmation for this job. Partial camera coverage or spool metadata cannot prove physical clearance or sufficient filament. Reuse still-applicable confirmation and accepted uncertainty; ask again only when a meaningful state change invalidates it.

Use one executing agent for dispatch. Record `dispatch_intent` with the verified ready-file hash before final Send, then send once. This record is bookkeeping, not an atomic concurrency lock. If the result is uncertain, inspect current task identity/state before retrying. A click, upload or old percentage is not a started print. Verify a new matching task and coherent layer count in `PREPARE`/`RUNNING`; distinguish heating/calibration from depositing layers.

If scheduling is requested, use an actual supported scheduler and record date/timezone, host availability and user conditions. A conversation wake-up is not an exact-time hardware timer. Follow stated deadlines; disclose a missed start before acting outside them. Do not test a schedule with a physical print. Stop/pause a one-shot schedule after its attempt and add monitoring only when requested.

## Close the loop

Keep a compact job manifest containing source/selection, file paths and hashes, material/size, mesh/slice evidence, authorization/plate confirmation, dispatch intent/result, device task identity and feedback. Preserve unknown existing fields. The entry skill's manifest may be reused; these specialist helpers do not automatically integrate every stage into it.

Evidence-based stages include `selected → modeled/imported → inspected → refined → validated → sliced → ready → dispatch_intent → prepare/running → completed/failed`. Skip stages already satisfied by current evidence; do not rerun generation for a resize. Record pending and unknown results explicitly, and qualify validation by its measured scope. Matching task completion and full layers establish device completion, not surface quality or easy support removal. Record physical feedback before treating a choice as a reusable preset.

Deliver source, actual preview and final package when sliced, dimensions/time/weight and specific outstanding issues. See [acceptance.md](references/acceptance.md) for evidence levels and offline regression cases.
