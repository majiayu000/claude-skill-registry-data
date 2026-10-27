---
name: ecosim-runfolder-summary
description: Summarize an existing EcoSIM run folder by following its namelist inputs and explaining topography, hydrology and lateral water exchange, soil profiles, vegetation/PFTs, management, forcing coverage, and run controls. Use for questions about how a case is configured; this does not create, modify, or run the case.
---

# EcoSIM Run-folder Summary

Produce a readable description of what the selected case actually configures,
with source variables, units, active-record selection, and unresolved inputs.
Read the run folder and referenced inputs without changing them. Do not launch
EcoSIM or infer successful completion from output filenames.

## Gather evidence

1. Locate the requested folder. Search locally first; a case may be nested, as
   in `SOAP/SOAP_share/`. Enumerate namelists; summarize each separately or use
   the user's selected one. Never silently choose among multiple namelists.
2. Use Python with `numpy` and `netCDF4`. From the EcoSIM repository root:

   ```bash
   python3 ecosim-agent/.agents/skills/ecosim-runfolder-summary/scripts/summarize_runfolder.py \
     SOAP --source-root .
   ```

   The helper finds a unique nested namelist and writes `summary.md` and
   `evidence.json` into a new timestamped directory under
   `ecosim-agent/result/runfolder_summary/`. Use `--namelist PATH` for an
   explicit choice, `--run-cwd PATH` if the launch working directory differs
   from the namelist's directory, and `--output-dir PATH` for a chosen new
   destination. It refuses to overwrite reports. Default to Markdown and JSON;
   produce HTML only when requested.
3. Inspect the warnings and evidence before writing the final explanation.
   The helper supports ordinary scalar/list namelist assignments, quoted
   strings, comments, D exponents, and repetition counts. Indexed assignments,
   null values, complex constants, and other unsupported syntax fail explicitly;
   use a proper Fortran namelist parser or inspect manually in those cases.
4. Treat paths relative to the launch directory, strip Fortran trailing spaces,
   and distinguish disabled `NO`, missing paths, unreadable files, and omitted
   settings. Do not substitute a nearby file with a similar name. Defaults not
   explicitly supplied require inspection of the selected driver/API.

## Explain the case

Use [reader-notes.md](references/reader-notes.md) for the mappings and reader
caveats demonstrated by SOAP. Source code in the user's selected model version
takes precedence over metadata and these notes. The helper preserves small
input arrays and metadata as evidence; it is not a complete EcoSIM validator.

- **Run controls:** case name, process switches, start date, restart mode,
  forcing triplets and cycles, timestep, stop settings, solver cycles, history
  and restart frequencies. Keep simulation years separate from forcing years.
  Report conflicting duration settings without promising an end date until
  driver/time-manager behavior is established.
- **Topography:** grid bounds, `topo_grid`, rectangle extents, cell widths,
  aspect and slope, latitude/elevation, water table and boundary conditions.
  `NH1:NH2` are columns; `NV1:NV2` are rows, despite some incorrect metadata.
  State if `first_topou` restricts the units read. Give cell footprint area
  only when widths and mapping support it; do not call it sloping surface area.
- **Soil:** per-unit `NUI`, `NJ`, `NL1`, `NL2`, active layer-bottom depths,
  bulk density, texture, hydraulic properties, pH, C/N/P, initial water/ice,
  and litter. Distinguish supplied layers from extra initialized layers and
  unused stored slots. Preserve declared units; soil concentrations are not
  ecosystem stocks without density, thickness, and area conversions.
- **Hydrology:** always include a dedicated hydrology section, even when some
  controls are missing. Read [hydrology.md](references/hydrology.md) for the
  source mappings and interpretation limits. Explain `grid_mode`, internal
  neighbor connections, aspect-dependent surface routing, and every external
  surface/subsurface/bottom coefficient and external-water-table distance.
  Distinguish a zero coefficient from an omitted value and a dormant direction
  from a nonzero conditional flux. Describe natural/artificial water-table
  modes, reference depth versus terrain-adjusted local depth, and whether the
  external table is stationary/mobile. Include `SCNH/SCNV`, macropore controls,
  FC/WP estimation flags, and THW/THI initialization semantics. Report explicit
  fixed-water-level, drainage-formulation and solver controls; label omitted
  defaults unverified. Derived initial geometry assumes a fresh run with the
  documented reader equations; it is not a runtime flux result or restart state.
- **Vegetation:** decode only the first `NZ` slots of each enabled rectangle.
  Honor `pft_dflag` record selection; constant files may lack a `year` variable.
  Explain raw and effective PFT codes, using grid `IETYPG` for the Koppen
  suffix and the namelist-selected parameter file for names and existence.
  If a plant rectangle crosses grid units with different climate codes, check
  every covered cell instead of assigning a single suffix. State omitted
  plant selectors or unverified runtime filters when relevant.
- **Management:** decode planting `DDMMYYYY`, population per m², depth in m,
  optional maximum population, and only `nmgnts` event rows. Group identical
  schedules across units, preserving all dates and values in JSON. Explain
  harvest/fire/grazing and termination codes using `ElmIDMod.F90`. A zero
  harvest code alone does not prove that thinning is absent. Separate PFT
  removal fractions from conditional ecosystem export fractions. Establishment
  density/reserves do not specify an initialized mature stand.
- **Soil management and forcing:** distinguish `soil_mgmt_in='NO'` from plant
  disturbances; inspect fertilizer/tillage/irrigation selector targets when
  present, using the sibling soil-management skill for field meanings. Report
  meteorological, GHG, chemistry, and adjustment inputs, available coordinate
  years, and coverage of positively cycled forcing periods. Coverage checks do
  not validate all timesteps or values. Avoid loading large history arrays.

## Deliver and verify

Lead with the landscape and vegetation configuration, then explain hydrology,
the run schedule and management. Use compact tables where units or PFTs differ. Link
the report and JSON evidence, cite file/variable names for key facts, and list
missing or unverified inputs separately from confirmed settings.

For a new installation or helper change, run it against the supplied example
and check [soap-example.md](references/soap-example.md). Exercise meaningful
edge cases with `python3 -m unittest discover -s <skill>/scripts -p 'test_*.py'`.
Summary generation needs no model build. Do not turn configuration inspection
into a scientific validation claim or update run trackers for an inspection-only
request.
