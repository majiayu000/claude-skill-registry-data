---
name: mumax3
description: Write, review, debug, and parameterize MuMax3 .mx3 simulations, including geometry, materials, fields, initial states, OVF output, Python batch workflows, and paper-guided phenomenon reconstruction.
metadata:
  short-description: Write and parameterize mumax3 scripts
---

# mumax3

Use native MuMax3 for `.mx3` simulations. Python can handle case generation, analysis and plotting when useful; keep existing workflows unless the request calls for a change.

## Start with the requested work

Read the target script and relevant task instructions. Use current source and input records to resolve parameters; generic examples and historical plans are not evidence of what ran. Do not load an entire project history for a local edit.

- **Edit or generate a script:** check the identifiers and patterns you need in [api_index.md](references/api_index.md) and [api_patterns.md](references/api_patterns.md), not both files in full by default.
- **Syntax uncertainty:** use [language_subset.md](references/language_subset.md) and [anti_patterns.md](references/anti_patterns.md). MuMax3 is Go-like, not full Go. Do not redeclare built-ins such as `mu0`, `t`, `m`, or `B_ext`.
- **Missing/disputed API:** search [api_full.md](references/api_full.md); consult [compatibility_notes.md](references/compatibility_notes.md) and the official API for version-sensitive behavior. Do not invent identifiers.
- **Model-specific help:** choose [structures.md](references/structures.md) or [examples.md](references/examples.md).
- **Rebuild a phenomenon from a paper or figure:** use [paper_reconstruction.md](references/paper_reconstruction.md); start with an exploratory model and the main trend.
- **Complete modeling and analysis examples:** use [worked_workflows.md](references/worked_workflows.md) for continuous hysteresis, Standard Problem 4, and macrospin FMR, including output checks and parameter changes.
- **Output or sampling design:** use [output_and_reproducibility.md](references/output_and_reproducibility.md).
- **Parameter scans:** use [parameter_sweep.md](references/parameter_sweep.md) to choose native sequential sweeps or external case orchestration.
- **Installation or missing engine/GPU:** use [installation.md](references/installation.md) for environment checks and an authorized MuMax3 setup; skip it for ordinary script work.

## Scientific and execution principles

- **Single writer:** coordinate concurrent changes to the same output; independent outputs need not serialize. Use the project's existing mechanism when present.
- **Traceable inputs:** keep reused inputs and derived results identifiable; content identity alone does not establish physical compatibility.
- **Adequate evidence:** choose quantities and sampling for the scientific question. Orientation or switching may need vector evidence over a time window; a display image need not show every component.
- **Human/automatic separation:** distinguish execution, automated findings and human interpretation; automatic results do not silently replace a human classification.

## Check the changed behavior

For physical edits, check SI units, mesh/cell size, geometry and region assignments, field/mask interactions, and required outputs. Reused states should fit the mesh, geometry and physical role of the new stage. Scope the checks to what changed.

`scripts/check_mx3_static.py path/to/file.mx3` provides conservative warnings, not proof of valid physics. Use engine `mumax3 -vet` when syntax/API changes warrant it; report unavailable checks. Numerical convergence and scientific acceptance require task-appropriate evidence, not a blanket checklist.

## Helpers

- `scripts/render_template.py`: render `assets/templates/*.mx3.template` using JSON or `KEY=VALUE` parameters.

Project-specific state schemas, monitoring schedules, storage/prune protocols, and agent assignments belong in project guidance, not in this skill's default workflow.

