---
name: servicex
description: Write ServiceX queries in func_adl against ATLAS xAOD data (PHYSLITE/PHYS) and provide guidance for dataset selection, filtering, and deliver usage. Use when asked to build, edit, or debug ServiceX/func_adl queries, ATLAS xAOD skims, or rucio dataset fetches.
---

# ServiceX

## Overview

Provide concise, correct func_adl query patterns for ServiceX on ATLAS xAOD, with best practices for selections, outputs, and deliver usage.

## Workflow

1. Identify the dataset type and base query.
   - Use `FuncADLQueryPHYSLITE` for PHYSLITE or OpenData.
   - Use `FuncADLQueryPHYS` for PHYS or other derivations.
2. Build a top-level `Select` that gathers all required collections and singletons.
   - Apply object-level filters with nested `.Where` inside this `Select`.
   - Do not pick columns yet.
3. Apply event-level filtering with a top-level `.Where` after the collections `Select`.
4. Create a final top-level `Select` that returns a single dictionary of output columns.
   - Convert units to standard LHC units (GeV, meters, etc.).
   - Never return a nested dictionary.
5. Use `deliver` once with `NFiles=1` by default and appropriate dataset source(s).
6. Make sure that the layout of the data that will be returned is remembered - downstream tasks that want to work with the data will need to understand it.

## Core Rules

- Prefer two top-level `Select` calls: collections first, output columns second.
- Filter objects with nested `.Where`; filter events with a top-level `.Where`.
- Use a single final `Select` that returns a dictionary of outputs.
- Do not use `awkward` functions inside ServiceX queries.
- Use `dataset.Rucio` for rucio DIDs and `dataset.FileList` for URL lists.
- Always set `NFiles=1` in `deliver` by default.
- If a transform fails and logs are required, respond with `HELP USER`.
- Ensure `func_adl_servicex_xaodr25` is listed as a dependency in the active project and installed in the current virtual environment before running or generating code that uses it.

## References

- Load `references/servicex-hints.md` for overall ServiceX query patterns, best practices, and error handling, and template code.
- Load only the relevant xAOD data model topic file(s) to keep context small. Naming convention: `references/datamodel-xaod-*.md`.
- xAOD topics:
  - `references/datamodel-xaod-units.md` (standard ATLAS units (energy, etc))
  - `references/datamodel-xaod-objects.md` (jets, electrons, muons)
  - `references/datamodel-xaod-tau.md`
  - `references/datamodel-xaod-missing-et.md`
  - `references/datamodel-xaod-tools-btagging.md`
  - `references/datamodel-xaod-event-weights.md`
  - `references/datamodel-xaod-tlorentzvector.md`
