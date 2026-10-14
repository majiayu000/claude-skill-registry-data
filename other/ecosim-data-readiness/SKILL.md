---
name: ecosim-data-readiness
description: Inventory staged local EcoSIM data at project startup and validate input readiness for a selected site, simulation period, and preprocessing or analysis workflow. Use before data-dependent work or when relevant inputs change.
---

# EcoSIM Data Readiness

Establish what local inputs are available and what has actually been validated
for the requested workflow. Use two modes: a lightweight startup inventory and
a focused validation before data-dependent work.

## Startup inventory

- Run once per session after the repository startup notice. Search `./data`
  first, then the wider repository, including `inputs`, `example_input`,
  `templates`, and existing `result` folders when present. Honor explicitly
  supplied input paths as well.
- Prefer `rg --files` and targeted filename searches. Check whether `data` is a
  symlink and whether its target is accessible; a missing or inaccessible root
  is a finding, not evidence that data do not exist elsewhere. Avoid following
  unrelated links or scanning external storage beyond staged data roots.
- Identify candidate categories: site metadata; meteorology; soil profiles;
  plant traits/PFT parameters; plant and soil management; deposition or
  precipitation chemistry; greenhouse-gas forcing; and benchmark observations
  or model outputs. Record representative paths and apparent sites or periods.
- Keep startup inexpensive: inspect paths and existing manifests, without
  opening every large dataset, extracting archives, or validating every site.
  Label coverage inferred from filenames as unverified. Templates and example
  files are candidates, not confirmed site-specific inputs.
- If no site or task is selected, report inventory only. Do not declare global
  readiness or treat every category as required for unrelated code work.

## Workflow validation

Determine requirements from the user's task, selected site and period, relevant
workflow skill, configuration/namelist, and consuming reader or template. Check
only dependencies of that workflow: for example, output analysis may require
model output and observations without requiring all simulation input categories.
If necessary context cannot be inferred, request the missing site, period, or
input choice while continuing independent work.

For each required input, select the actual file and inspect its contents:

- **Access and identity:** Verify readability, format, required variables,
  dimensions, and site coordinates/ID. Distinguish archive members from usable
  extracted inputs. Record unresolved choices between conflicting versions.
- **Time:** Verify requested coverage, cadence, calendar, timezone, timestamp
  meaning, duplicate or missing steps, and management-event alignment. Identify
  spin-up or cycling assumptions separately from observed coverage.
- **Units and values:** Check documented units, fill values/sentinels, missing
  data and quality flags, and physical ranges appropriate to the variable.
  Distinguish flux rates from interval totals; verify conversions between mass
  and molar units, elemental and compound mass, and area/depth bases. Report
  potential mass-balance inconsistencies with the evidence available.
- **Compatibility:** Check layer depths/order, grid/site dimensions, PFT codes,
  parameter identifiers, management selectors, and cross-file consistency
  against the actual EcoSIM reader or maintained workflow conventions. Confirm
  referenced namelist paths exist when preparing a runnable case.
- **Metadata:** For NetCDF, inspect units, descriptive names, coordinates,
  calendar/time encoding, and declared CF conventions. Use standard names where
  applicable; do not invent CF names for EcoSIM-specific variables. Report
  metadata gaps separately from reader incompatibilities. Do not claim full CF
  compliance from a `Conventions` attribute alone.

Use headers and lazy reads first; inspect data arrays only as needed for the
selected validation. Reuse existing domain validators where appropriate,
reading their skill instructions when invoking them. Record unavailable tools
or incomplete checks as unverified, rather than assuming success.

## Findings and reports

Assign each relevant input one status:

| Status | Meaning |
| --- | --- |
| Found, unverified | Candidate exists; contents or required checks remain unverified. |
| Ready | Required checks passed for the stated site, period, and workflow. |
| Needs preparation | Source exists but conversion, extraction, or another documented preparation step remains. |
| Missing | No candidate was found in the searched locations for a required input. |
| Invalid | A required check failed; describe the failure and affected work. |
| Not required | This input category is outside the selected workflow's requirements. |

Summarize startup findings briefly in chat. Save a detailed inventory or
validation report under `./result/data_readiness/`, using a site/task identifier
and timestamp to avoid overwriting another assessment. Include mode, assessment
time, site/task/period (or unspecified), searched locations, actual input paths,
checks performed, evidence, assumptions, status, and concrete next steps. An
inventory report must state that content validation has not been performed.

Overall readiness requires all required inputs to be ready for the declared
scope; optional missing observations need not block a simulation. Explain which
steps are blocked by missing, invalid, unprepared, or unverified dependencies,
and proceed with independent work. A readiness assessment does not itself
authorize downloads, credential access, changing source data, or running an
expensive simulation.

Reuse the session's assessment until relevant file paths, sizes, modification
times, configurations, or task requirements change. Recheck affected inputs
after preparation or edits. Treat reused reports as dated evidence and verify
their scope and input freshness before relying on them.
