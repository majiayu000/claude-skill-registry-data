---
name: ecosim-trait-correction-short-run
description: Correct the PFT parameters selected by an existing EcoSIM namelist through isolated five-day simulations and plant_trait.desc checks. Use for iterative trait correction and parameter-file compatibility repair; history analysis and seasonal calibration are outside the default workflow.
---

# EcoSIM Short-Run Trait Correction

Verify that supported parameter corrections reach the model's printed plant
traits. Default to **five simulated days**, unless the user specifies another
duration. Evaluate `plant_trait.desc`; do not inspect, plot, or scan history
output unless explicitly requested. Existing history settings may remain in the
test namelist.

This is an agent-guided workflow using existing tools, not a separate simulation
driver. It does not change the two-year default for new-site smoke tests.

## Dependencies and scope

Read these canonical skills as needed:

- [Plant-trait sanity check](../ecosim-plant-trait-sanity-check/SKILL.md):
  physiological checks, site/species evidence, units, and root hydraulics.
- [PFT parameter editor](../ecosim-pftpar-editor/SKILL.md): `ParEditor`, backups,
  read-back, and JSONL change logs.
- [Data readiness](../ecosim-data-readiness/SKILL.md): focused checks of selected
  inputs; reuse this session's inventory when still applicable.
- [Site run tracker](../ecosim-site-run-tracker/SKILL.md): record the site-run
  request, executable, short-test result, and unresolved trait findings.

Operate on the existing case. Do not regenerate site inputs, run two years, or
start a full simulation merely because another workflow normally does so. Use
repository build/environment guidance if a build is necessary.

## Prepare an isolated test

1. Resolve the supplied namelist and actual PFT parameter path from its execution
   directory. Inspect Git status and applicable repository instructions. Preserve
   staged contents and existing simulation outputs.
2. Identify the executable and active source revision. Check input availability,
   forcing coverage for the test, management/PFT codes, and whether grid Koppen
   settings replace PFT suffixes. Record executable path/hash and source commit
   separately; source inspection does not prove an executable's revision.
3. Create a unique workspace under `result/<CASE>_trait_correction_<STAMP>/`,
   with `input/` and separate `round_00/`, `round_01/`, ... directories. Preserve
   a pristine PFT backup and a parameter snapshot for each round. Resolve other
   read-only input paths from the original case directory, not the new working
   directory. Do not copy existing outputs or restart pointers.
4. In each test namelist, preserve start date, forcing/spinup mapping, processes,
   management, timestep, and case configuration. Set:

   ```fortran
   continue_run = .false.
   disp_planttrait = .true.
   stop_option = 'ndays'
   stop_n = 5
   ```

   Point `pft_file_in` to that round's snapshot. Keep the original case duration
   unchanged. Run in a fresh directory so the model never overwrites an existing
   `.desc` or restart. Capture stdout/stderr.

## Check reader compatibility

Compare variables and dimensions in the selected PFT file with the **active
reader**, including required fields beyond RVSR and ARSRA. Trace related read
paths rather than assuming missing fields have safe defaults. A successful run
can print misleading values when parameter variables are missing. An isolated
baseline may help diagnose this, but label its affected traits unreliable.

Repair missing schema in the case copy, not a shared parameter template:

- Reuse a compatible template for variable structures, dimensions, and metadata.
  `ParEditor` edits existing values; it cannot add missing variables. Add only
  required structures with NetCDF tools, then initialize through `ParEditor`.
- Match donors by exact PFT code. Inspect and justify alternatives, recording
  each donor mapping and its limits. Do not silently replace whole records or
  introduce unrelated climate codes.
- Separate schema initialization from scientific correction. Template defaults
  are **model defaults**, not site measurements or literature calibration. Mark
  unsupported choices unresolved even when the checker passes.
- Read back added fields: active entries must be finite, unmasked, dimensionally
  compatible, and in the reader's units. Preserve existing values unless a
  separately documented correction requires a change.

## Run, inspect, correct, and repeat

For each round:

1. Run from its directory. Confirm normal exit, completion of the requested days
   from the log/restart completion message, and a newly generated trait file for
   the case/start year. A fresh five-day hourly run ends at step 120; derive the
   count from the actual timestep otherwise. Do not use history files to judge
   completion. Stop correction work on a failed or incomplete run and retain
   its log.
2. Run the existing strict checker. From the ecosim-agent root:

   ```bash
   python .agents/skills/ecosim-plant-trait-sanity-check/scripts/check_plant_trait_desc.py \
     /absolute/path/to/round/CASE.plant_trait.desc.YEAR \
     --strict-physiology --web-evidence /absolute/path/to/evidence.json --json
   ```

   Omit `--web-evidence` for the initial deterministic pass if evidence is not
   ready. Save JSON and a human-readable review. A nonzero checker exit for
   findings is distinct from model failure. Review all PFTs in the first grid
   (`NY=1, NX=1`) by default, per the sanity-check skill. Report checked versus
   total blocks. Verify changes in repeated grid blocks using the same PFT record
   without claiming a full ecological review there.
3. Gather or refresh site/species literature evidence following the sanity-check
   skill. Record evidence level, URL, units, conversions, and applicability to
   species/root order/cohort. Separate conditional screening envelopes from
   defensible correction targets.
4. Reuse `ecosim-plant-trait-sanity-check/scripts/trait_corrections.py` functions
   `read_pft_values`, `plan_corrections`, and `apply_corrections`. Inspect the plan
   before applying it. Composite findings such as `RVSR/RRAD2M` are not literal
   NetCDF variable names: trace which variable needs correction and supply a
   documented plan entry for it. Apply reviewed changes through `ParEditor`,
   retain its JSONL log, and read values back. Never edit or manufacture a
   replacement `.desc`.
5. Run another fresh five-day round with the revised snapshot. Confirm the values
   in the model-generated `.desc`, not only in the NetCDF.

Use four simulation rounds as the default upper bound. Stop earlier when no
supported correction remains, no parameter changes, or findings persist unchanged
after a correction. Report unresolved findings instead of repeating identical
runs. If no rerun slot remains, retain further changes as proposals; do not apply
and present them as verified. Every adopted correction needs a fresh model trait
read-back.

## Scientific decisions

- Correct impossible values, reader mismatches, and demonstrated model/category
  inconsistencies first. Do not tune values solely to eliminate warnings.
- Numeric corrections need applicable literature evidence or an explicit user
  value. Label model conventions and inherited user defaults, including the
  sanity-check skill's C3-tree CHL rule, separately from measured values. Review
  planner special rules, including SLA scaling, against source units and
  applicability. Its `satisfied_by_rule` result does not validate a trait itself.
- Preserve jointly constrained kinetics/allocations unless evidence supports a
  coordinated correction. Jmax:Vcmax is formulation-sensitive; do not adjust CHL
  or ETMX merely to hit its screening interval.
- Verify root equations in the selected source revision. RVSR is literal mean
  conduit lumen radius in meters; ARSRA represents nonideal axial resistance;
  RSRR is radial resistivity. Do not substitute effective hydraulic radii or use
  one resistance to compensate for another. Report each PFT's RSRR and
  `1/(3600*RSRR)` in `m s-1 MPa-1`.
- Five early days establish loading and printed trait consistency, not resistance
  partitioning, drought response, mature-stand productivity, or seasonal
  calibration. Leave findings requiring those analyses unresolved. Do not expand
  into history analysis by default.

## Deliver the tested correction

For an authorized case-correction request, save a versioned case-specific PFT
copy and update the original namelist's PFT path to that tested copy, preserving
its duration and other settings. Back up the namelist, check original input
hashes for intervening edits, and verify the published parameter copy matches
the tested snapshot. For a review/proposal, leave the original case unchanged.
Do not update shared templates or other cases without instructions.

Keep original/final paths and hashes, executable/source provenance, per-round
completion and checker results, old/new/read-back values with citations,
schema donors/defaults, parameter logs, and unresolved findings in the result
workspace. Report tracker status with the five-day override explicit; leave
full-run and history/benchmark work skipped when outside scope. Lead the final
response with changes and trait read-back, then disclose remaining warnings and
unvalidated defaults.
