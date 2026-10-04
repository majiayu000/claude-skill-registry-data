---
name: mbg-design-regression
description: Reads AI-Generated-Design-Result as both working design output and regression evidence, understands the "<design>_designcontext_v2/" convention for new pipeline runs kept beside preserved baselines, and inventories the artifacts (.gds, .lvs.out, .magic.drc.rpt, .spice, REPORT.md) each design directory holds. Use before comparing a new run against a prior one, or before writing anything into AI-Generated-Design-Result. Do not use it to generate a new layout or run verification — this skill is read-only and never overwrites a previous result.
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-design-regression/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Design Regression

## Purpose

Read prior AI-generated design runs under `AI-Generated-Design-Result/`
(see `.ai/manifest.json`'s `project.generated_designs`) correctly: as both
a working deliverable and as regression evidence that later runs are
compared against, never silently replaced by.

## When to Use

- Before comparing a newly generated layout/verification result against an
  earlier run of the same design.
- Before writing any new output into `AI-Generated-Design-Result/` — to
  confirm you are creating a new, distinctly-named directory rather than
  touching an existing one.
- When asked what evidence exists for a design's DRC/LVS/PEX/simulation
  history.
- When asked to explain the difference between two directories for what
  looks like "the same" design (e.g. `ota_5t/` vs. `ota_5t_designcontext_v2/`
  vs. `ota_5t_glm_5-2/`).

## When Not to Use

- Generating a new layout — use `mbg-spice-to-gds`.
- Running DRC/LVS/PEX on a fresh GDS — use `mbg-ic-verify`.
- Deciding whether a numeric regression (e.g. area, DRC count) is
  acceptable for tapeout — report the comparison; the acceptance decision
  belongs to the design owner and `AGENTS.md`'s tapeout gate, not to this
  skill.

## Required Inputs

- The design name(s) or directory path(s) under
  `AI-Generated-Design-Result/` to inspect or compare.

## Preconditions

- Treat every existing subdirectory of `AI-Generated-Design-Result/` as
  preserved evidence, not scratch space. Confirm what already exists
  (`ls AI-Generated-Design-Result/`) before writing anything.
- Read `AI-Generated-Design-Result/README.md` for the current top-level
  narrative of what each design directory represents before trusting any
  summary here — new design runs get added over time and this skill is a
  map, not the current inventory.

## Workflow

### 1. Understand the directory shapes actually present

As of the last inspection, `AI-Generated-Design-Result/` holds, per design,
more than one directory reflecting different pipeline generations of the
same circuit — do not assume a single canonical directory per design name:

- **`<design>/`** — an earlier full run (e.g. `ota_5t/`), typically the
  richest artifact set: GDS, SVG, DRC/LVS/PEX reports, `.pex.spice`,
  pre/post-layout `.dat` simulation data, `.png` plots for AC/DC/GBW/phase
  margin/slew rate, and often a large session-log `.md` transcript.
- **`<design>_designcontext_v2/`** — the convention for a **new** run
  produced through the newer `DesignContext`/`GridRouter` pipeline path
  (see `mbg-repo-analysis`), kept **beside**, not instead of, the original.
  These directories are typically leaner: `.gds`, `.spice`,
  `.lvs.out`, `.magic.drc.rpt`, extracted netlists
  (`<design>_extracted.spice`, `<design>_extracted_flat.spice`), and a
  `baseline.lvs.out` / `baseline.magic.drc.rpt` pair — the baseline files
  are themselves a copy of the prior run's results kept alongside the new
  one specifically so the two can be diffed without re-running anything.
- **`<design>_glm_5-2/`** — a run attributed to a specific model
  (`z-ai`/GLM-5.2, interactive agent-driven flow), distinguished from a
  DeepSeek-V4-Pro run by the `_glm_5-2` suffix per the model-routing
  convention documented in `AI-Generated-Design-Result/README.md`. Holds
  its own `REPORT.md`.
- **`designcontext_v2_comparison.json`** (repo-root of
  `AI-Generated-Design-Result/`) — an explicit, checked-in old-vs-new
  regression table: per design, `old_drc`/`new_drc`, `old_lvs`/`new_lvs`,
  `old_prop_mismatch`/`new_prop_mismatch`, `old_area`/`new_area`,
  `old_t`/`new_t` (runtime), plus new-only routing metrics
  (`new_routed`, `new_opens`, `new_shorts`, `new_wire`, `new_vias`). This
  file is itself regression evidence — read it before re-deriving a
  comparison by hand, and extend it (new entries) rather than mutate
  existing rows when a further run is compared.

Confirm the current directory names with `ls AI-Generated-Design-Result/`
rather than trusting this list to be exhaustive — new suffixes may appear
as the project produces more runs.

### 2. Know what artifacts to expect and what each one is evidence of

| Artifact | Evidence of |
|---|---|
| `<design>.gds` | Final generated layout |
| `<design>.spice` | Self-contained source netlist (often with `.lib` prepended so the PDK auto-detects) |
| `<design>_extracted.spice` / `_extracted_flat.spice` | Netlist extracted back from the GDS via Magic (see `mbg-ic-verify`'s `extract_layout_netlist`) |
| `<design>.magic.drc.rpt` | Magic DRC report |
| `<design>.lvs.out` | netgen LVS report |
| `<design>.pex.spice` | Parasitic-extracted netlist |
| `baseline.magic.drc.rpt` / `baseline.lvs.out` | A copy of the *prior* run's DRC/LVS results, kept for direct diffing against the new run in the same directory |
| `REPORT.md` | Human-readable design report: specification, final SPICE, PDK-conformance checklist, and (per `AI-Generated-Design-Result/*_glm_5-2/REPORT.md`) explicit pipeline-stage provenance |
| `*.png` / `*.svg` | Simulation plots and layout preview, referenced from `REPORT.md` or the top-level `README.md` |
| session-log `.md` (e.g. `1785488132943.md`) | Full interactive transcript — primary evidence for `mbg-ai-experiment-audit`-style prompt/refinement claims |

Not every design directory has every artifact — a missing PEX or
post-layout `.dat` file means that stage was not run for that particular
directory, not that it failed silently. Report artifact absence
explicitly rather than assuming a stage passed or was skipped.

### 3. Compare a new run against a preserved baseline

1. Identify the two directories being compared (e.g. `ota_5t/` vs.
   `ota_5t_designcontext_v2/`).
2. Prefer an existing `baseline.*` file or the checked-in
   `designcontext_v2_comparison.json` entry over re-deriving numbers by
   hand, when one already exists for the pair in question.
3. Compare like-for-like fields: DRC error count, LVS match status and
   property-mismatch count, layout area, generation time, and (for the
   `DesignContext` path only) routing completeness (`new_routed`,
   `new_opens`, `new_shorts`), wire length, and via count.
4. Report the comparison as a table or explicit before/after pair per
   metric — never as a single collapsed "better" or "worse" verdict
   without the underlying numbers.
5. If no baseline or prior comparison entry exists for the pair you were
   asked to compare, say so explicitly rather than fabricating one.

### 4. The hard rule: never overwrite a previous result

- Do not write a new run's output into an existing design directory that
  already holds a preserved result. Use a new, distinctly-suffixed
  directory (following the existing `_designcontext_v2` /
  `_glm_5-2`-style convention, or a clearly new suffix if neither fits) so
  the old evidence remains intact for comparison.
- Do not delete or truncate an existing `.gds`, `.spice`, `.lvs.out`,
  `.magic.drc.rpt`, `REPORT.md`, or plot file to "clean up" — these are
  regression evidence, not scratch output, per `AGENTS.md`'s rule that
  generated files are experiment artifacts until the user explicitly
  decides they belong (or don't) in version control.
- If a genuine correction to a previous result is needed, propose adding a
  new directory or an explicit comparison entry, and let the user decide
  whether the old one should be retired — do not make that call
  unilaterally.

## Outputs

- An inventory of what artifacts exist (and are missing) for a given
  design directory.
- A field-by-field comparison between two runs of the same design, sourced
  from real files or the checked-in comparison JSON.
- An explicit statement when asked to write new output, of the new
  directory name chosen and confirmation that no existing directory was
  overwritten.

## Failure Modes

- Assuming there is exactly one directory per design name — several
  suffix conventions coexist for the same circuit.
- Treating a missing artifact (e.g. no PEX file) as a failed stage without
  checking whether that stage was simply not run for that directory.
- Overwriting or deleting an existing result directory instead of creating
  a new one — this is the one rule this skill exists to prevent violating.
- Re-deriving a comparison from scratch when `designcontext_v2_comparison.json`
  or a `baseline.*` file already holds it.
- Reporting a design as "regressed" or "improved" using only one metric
  (e.g. area) while ignoring that DRC/LVS status changed too — report the
  full set of compared fields.
