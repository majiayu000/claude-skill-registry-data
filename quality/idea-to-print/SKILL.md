---
name: idea-to-print
description: Turn an idea or uploaded image into a reviewable 3D sculpture and an authorized FDM print. Coordinate design selection, mesh refinement, evidence-based validation, slicing and resumable printing handoff.
---

# Idea or image → printable object

For iterative pet and mythical-creature jobs, use the
[V2 bounded workflow](references/workflow-v2.md): one resumable ledger,
reference → form → detail checks, limited attempts, and an explicit diagnostic
handoff when quality does not converge. Existing models enter at import;
simple edits need only their relevant stage.

Coordinate the bundled sibling skills `printable-modeling` and
`3d-print-workflow`; read their instructions when reaching that stage. Inspect
available image, filesystem, rendering and desktop-control tools before using
them. This skill is an agent workflow, not a hosted upload page or a daemon.

When installed, resolve helpers relative to this actual `SKILL.md` and sibling
skills, not the user's current working directory. Read adjacent
`runtime.local.json` if present for the dependency-installed Python path; verify
it still exists and has the needed packages. The installer records the interpreter
that ran it. If skills were copied manually, choose/configure a suitable Python.
Use absolute script and job paths when working outside the repository. Code
examples in references use repository-root paths only for readability.

## Choose the correct starting point

- **Uploaded image or local image path:** inspect the actual image, preserve its
  bytes, and treat it as selected when the user asks to model that image. Skip
  concept generation and candidate selection. Use `scripts/prepare_image.py`
  to create a new local job from PNG, JPEG or WebP, recording dimensions/hash.
  See [image input](references/image-input.md). Multiple attachments require
  identifying whether they are candidates or views of the same object.
- **Text idea:** use the host's available image-generation tool to produce
  concepts; follow its installed skill if available. Normally offer three
  meaningfully different silhouettes for an open brief, one when requested.
  Keep stable candidate IDs and actual working image previews. Stop for a
  selection unless the user delegates it. See the [design recipe](references/design.md).
- **Existing GLB/STL/3MF or a model link:** preserve source and license; start
  with `printable-modeling` or `3d-print-workflow` at the needed stage. Avoid
  generating a new design merely to resize an existing object.

Use a user-chosen working directory; `jobs/<unique-job>/` is a useful default.
Record inputs, the exact selected image/version, units, target size, material,
source/raw mesh/editable/final/sliced artifacts, checks, authorization and
dispatch evidence in `job.json`. See [job continuity](references/job-record.md).
Keep job images and device credentials out of public repositories.

## Track a refinement job

Use `Design → Generate → Inspect → Refine → Validate → Slice → Manufacture`
as stage names, not a demand to rerun completed work. An existing validated model
can enter at sizing/slicing. Keep separate fidelity, geometry and slice results;
each result is `PASS`, `FAIL` or `UNKNOWN` for a stated scope and revision.
Read [refinement and validation](../printable-modeling/references/refinement-and-validation.md)
for generated organic meshes or a repair/validator workflow.

Use `scripts/refinement_job.py` to record revisions and evidence hashes when
maintaining this workflow. It is bookkeeping, not a sculptor, validator or printer
approval. Preserve actual user choices and existing applicable authorization.
A repair report cannot grant itself visual acceptance or printing permission.

## Selected image → real geometry

Follow `printable-modeling` for the image-to-3D provider and local repair route.
The official Hunyuan3D 3.1 website provides an optional high-poly draft route when
its account, quota and host browser tools are available. The bundled Hunyuan
helper is a separate optional 2.1 public-demo adapter. The optional
[official 3.1 API adapter](../printable-modeling/references/hunyuan31-api.md)
has explicit configuration, bounded attempts and recovery. The 2.1 helper
submits the chosen local image to its demo. Explain that transfer for a new user of this route and
honor local-only or privacy constraints. A local-only request cannot be fulfilled
by silently using this hosted adapter. Service/account constraints are checked
when used; access is not granted by installing a skill.

Preserve the reference. Use image-editing tools for optional background cleanup
without changing the intended object, retaining a separate result. Inspect the
raw mesh from front/side/back/underside. Unseen surfaces are inferred: catch
unexpected slabs, missing limbs, fused negative space and disconnected details.
Save editable source, repair the actual geometry, then render the final exported
model for review. Major changes to pose, silhouette or assembly need a design
decision; faithful routine repair does not need repeated approval.

Scale proportionally in millimetres. If a size lacks an axis, state the default
as the longest overall dimension including the base; explicit height/width/body
size overrides that assumption. Keep the original and recheck after changes.
Do not hardcode a printer, color, 160 mm target or style preference for all users.

## Geometry → slice → requested print

Use `3d-print-workflow` to match the actual machine/nozzle/plate/material, inspect
first-layer contact, thin tips and support escape paths, and verify the complete
printable envelope including supports/brim. Report dimensions, time, separate
model/support weight when known, and retained warnings. Deliver the exact checked
ready package with its hash. A tree-support setting does not establish easy removal.

A model-only request stops with usable files and actual previews. If this exact
job is already authorized for printing, continue after its required current
physical facts are established. Selection, printing authorization and clearance
may all be given in one sentence; do not ask again without a meaningful change.
Record an owner's explicit acceptance of unknown remaining filament instead of
requiring them to prove a minimum spool weight repeatedly.

Use an available official slicer/device UI or a separately validated integration
for dispatch. This repository's scripts do not start a printer. If desktop
automation is unavailable, hand over the checked file with precise manual steps;
do not claim automatic dispatch. One executing agent records intent before Send,
sends once, and verifies the new task identity, expected layers and actual phase.
An uncertain attempt requires reconciliation before any retry.

## Resume and feedback

Resume the same job and first incomplete stage. Recover cached model results
before requesting another generation; reconcile any outstanding print attempt
before sending. Do not schedule or monitor unless asked using a supported mechanism.

Keep concept/fidelity quality, scoped geometry results, sliced readiness, device
completion and physical acceptance separate. Unsupported or unrun checks remain
`UNKNOWN`; a report without observed faults is not evidence of full printability. Feedback on resemblance, stability, broken details,
support removal and contact marks determines future improvements. Never upgrade
device FINISH into a claim of an inspected good-quality object.
