---
name: mike-import
version: 0.1.0
description: Bring an EPA SWMM (.inp) or EPANET (.inp) model into MIKE+ via the mike-plus MCP server — the bridge from an INP builder such as SWMMCanada or agentic-swmm into a MIKE+ database that mike_model_info / mike_run can use. Use when the user has an .inp and wants it in MIKE+. Requires MIKE+ installed + a checked-out license (demo mode caps the model size).
---

# MIKE+ Import

Creates a **new** `.sqlite` from an `.inp`. SWMM data lands in MIKE+'s SWMM tables
(`mss_Node`, `mss_Link`, `mss_Project`, ... ; subcatchments in `msm_Catchment`) and the
tool switches the model type to **CS_SWMM** so the imported simulation setup is the
active one. `mike_model_info` then reports the `mss_*` counts and setups.

## Tool

- **`mike_import_swmm`** — `{inp, out_sqlite, kind?='swmm'|'epanet', overwrite?, srid?, projection?}` → `{sqlite, inp_used, patched_outfalls_gated[], active_model, active_simulation, unit_system, simulations[], counts{nodes,links,catchments}, inp_scan}`.

## What the tool does for you (verified on MIKE+ 2026)

- **Gated column.** MIKE+ rejects `[OUTFALLS]` rows without the optional `Gated` column (`O1 90 FREE`, valid for EPA SWMM which assumes `NO`) with an opaque "Error importing from SWMM file." The tool writes a patched COPY `<name>.mikeplus.inp` next to `out_sqlite` (adds `NO`), imports that, and lists the rows in `patched_outfalls_gated`. Your original `.inp` is never modified.
- **Model type.** Sets `m_ModelSetting.ModelNo = 2` (SWMM) so `active_model = CS_SWMM` and the imported `mss_Project` setup is active.
- **Failure hints.** On failure the error names the likely cause: gated-less outfalls, or the model is bigger than the **demo-mode limit** (more than 10 subcatchments fails when no license is checked out).

## Conventions

- Needs a real license for anything but toy models: if the error mentions the demo limit, the GUI or another process holds the seat: free it, wait, retry once; do not loop.
- `overwrite` defaults to false; the tool refuses to clobber an existing `.sqlite`.
- External files referenced by the `.inp` (`FILE "rain.dat"` time series) are not copied; keep them next to the `.inp` and check `inp_scan.TIMESERIES` vs what the model expects.
- After import: `mike_model_info` (expect `CS_SWMM`, `mss_*` counts) → copy the folder → `mike_run`. Running an imported SWMM-type model through `mike_run` has **not been verified live** yet (license); gate on `status` as always and report what you see.
- EPANET (`kind='epanet'`) uses the same call; the model type is left as MIKE+ sets it (report `active_model`).

## Orchestration

```
mike_import_swmm {inp, out_sqlite: runs/<case>/00_model/<name>.sqlite}
mike_model_info  {sqlite}                    -> CS_SWMM, setups, counts
mike_run         {sqlite}  (license)         -> result files -> mike-results / mike-plot
mike_manifest_write {model, inputs: [inp, inp_used], ...}
```
