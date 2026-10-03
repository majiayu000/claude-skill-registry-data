---
name: orca-uv-vis
description: Generate ORCA input files for TD-DFT UV-Vis calculations and parse/plot the resulting absorption spectrum. Use when the user asks about UV-Vis spectra, absorption spectra, TD-DFT calculations, excited state calculations in ORCA, or wants to plot results from an ORCA TD-DFT output file. Also trigger when the user mentions oscillator strengths, electronic transitions, or simulated UV-Vis.
---

# ORCA UV-Vis Calculation Pipeline

This skill covers two stages: generating an ORCA input file for a TD-DFT calculation, and post-processing the output to plot a Gaussian-broadened UV-Vis absorption spectrum.

**Scope:** Input generation, local post-processing, and (optionally) HPC submission via the CatGo workflow engine. The "Submitting to HPC" section below covers the proven Expanse flow. If the user is running on their own non-CatGo infrastructure, just generate the input file from the template in Stage 1 and skip the submission section.

**Target version:** ORCA 6.x. Output block layout in ORCA 5 is close but not identical; the parser below is written against the ORCA 6 format used by CatGo's own parser (`server/catgo/utils/orca_output.py::OrcaUvVisOutput`).

## Stage 1: Input Generation

Before generating the input file, ask the user for:

- XYZ geometry file path (assume already optimized; if the user hasn't optimized, route them to `orca-opt` first)
- Solvent for CPCM (e.g. hexane, water, ethanol, dichloromethane, acetonitrile)
- Charge and multiplicity (default to `0 1` if not specified)

Generate an ORCA input file with these fixed settings:

- Functional: `CAM-B3LYP`
- Basis set: `DEF2-TZVP`
- Full TD-DFT (not TDA)
- 30 roots
- CPCM solvation inline on the keyword line
- No RI / auxiliary basis
- No special SCF convergence tricks

Template:

```
!CAM-B3LYP DEF2-TZVP CPCM(HEXANE)
%TDDFT
   NROOTS   30
END
%output jsongbwfile True jsonpropfile True end
*XYZFILE 0 1 geometry.xyz
```

Substitute the user's solvent, charge, multiplicity, and XYZ path. If the user provides inline coordinates instead of a file, use `* XYZ <charge> <mult>` followed by the coordinates and close with `*`.

The `%output ... end` line makes ORCA emit the JSON files OPI's `Output.parse()` consumes during post-processing (Stage 2). Keep it.

### Building the `%tddft` block with OPI

OPI's `BlockTddft` exposes every TD-DFT knob (`nroots, iroot, irootmult, maxdim, maxiter, etol, rtol, tda, lrcpcm, cpcmeq, donto, saveunrnatorb, spinflip, soc, socgrad, triplets, ...`) as a typed Pydantic field. Bad keys raise at construction.

The catgo backend builds the route line, `%pal`, `%maxcore`, charge/multiplicity, and geometry from node params — it does **not** emit a `%TDDFT` block of its own. So OPI only contributes the `%tddft` and `%output` blocks here, which we paste into `extra_blocks` as text. Do **not** use `Calculator.write_input()` — that writes a full input file and would duplicate the route line / pal / geometry the backend already emits.

```python
from opi.input.blocks import BlockTddft, BlockOutput

tddft_block = BlockTddft(nroots=30, tda=False, triplets=False, donto=True)
output_block = BlockOutput(jsongbwfile=True, jsonpropfile=True)

extra_blocks_text = tddft_block.format_orca() + "\n" + output_block.format_orca()
# Pass extra_blocks_text into the node's `extra_blocks` param.
```

`format_orca()` emits exactly one `%...end` block per call. The result for the snippet above is:

```
%tddft
    nroots 30
    tda False
    donto True
    triplets False
end
%output
    jsonpropfile True
    jsongbwfile True
end
```

TD-DFT with 30 roots at def2-TZVP is expensive — tell the user this is a heavy calculation and that they should expect to run it on a cluster or at least overnight on a workstation, not on a laptop.

## Submitting to HPC (Expanse) — proven flow

Use this when the user wants the CatGo workflow engine to run the TD-DFT job
on Expanse. Skip if they only want the input file.

> **Use `catgo_workflow` (graph-based), NOT `catgo_workflow_engine` (task-based).**
> The graph-based tool auto-captures the viewer structure on `create`. Task-based
> `add_task` doesn't, so jobs fail with "No input structure provided". Param keys
> differ: graph-based uses `method`/`basis`, task-based uses `orca_method`/`orca_basis`.

### 1. Confirm structure is loaded and find session_id

```json
catgo_view(action: "get_state")
```

```bash
curl -s http://localhost:8000/api/hpc/connections
```

Copy the `session_id` for `host: login.expanse.sdsc.edu`.

### 2. Create the workflow

```json
catgo_workflow(action: "create", name: "UV-Vis CAM-B3LYP TD-DFT")
```

### 3. Add the TD-DFT node

Use the `orca_uvvis` node type, which has dedicated TD-DFT params (`nroots`, `triplets`, `tda`, `donto`, `solvation`, `solvent`, `calc_type`, `aux_basis`) plus the standard `dispersion` field. **Do NOT use `extra_keywords` or `extra_blocks` — they are NOT read by the engine and are silently dropped.**

```json
catgo_workflow(action: "batch", workflow_id: "<wf_id>", operations: [
  {"op": "add_node", "node_type": "orca_uvvis", "label": "tddft",
   "params": {
     "software": "orca",
     "method": "CAM-B3LYP",
     "basis": "def2-TZVP",
     "calc_type": "tddft",
     "nroots": 30,
     "tda": false,
     "triplets": false,
     "donto": true,
     "solvation": "CPCM",
     "solvent": "hexane",
     "dispersion": "D4",
     "charge": 0,
     "multiplicity": 1,
     "num_cores": 16,
     "max_core_mb": 4000
   }},
  {"op": "connect", "from_id": "<structure_input_id>", "to_id": "tddft",
   "from_handle": "structure", "to_handle": "structure"}
])
```

### Canonical UV-Vis node params (verified against [server/workflow/engines/orca.py:244-268](server/workflow/engines/orca.py#L244-L268))

| Parameter | Default | Description |
|---|---|---|
| `method` | CAM-B3LYP | Functional |
| `basis` | def2-TZVP | Basis set |
| `dispersion` | (none) | `D4` \| `D3BJ` \| `D3` |
| `calc_type` | tddft | `tddft` or `steom` (STEOM-DLPNO-CCSD) |
| `nroots` | 10 | Number of excited states |
| `tda` | true | Tamm-Dancoff approximation; pass `false` for full TD-DFT |
| `triplets` | false | Compute triplet states |
| `donto` | false | Natural transition orbitals |
| `solvation` | none | `CPCM` \| `none` |
| `solvent` | water | Any ORCA-recognised solvent name |
| `aux_basis` | def2-TZVP/C | Aux basis (used by STEOM path) |
| `num_cores` / `max_core_mb` | 4 / 4000 | |

### 4. Run with the full HPC run_config

TD-DFT with 30 roots at def2-TZVP is heavy — bump `walltime` and use `shared`
or `compute` (debug caps at 30 min). Read `server/templates/orca_generic.sh`
and pass its contents as `default_template`.

```json
catgo_workflow(action: "run", workflow_id: "<wf_id>", run_config: {
  "execution_mode": "hpc",
  "default_session_id": "<expanse_session_id>",
  "base_work_dir": "/expanse/lustre/projects/sdp126/jyang25/ORCA/catgo",
  "default_job_params": {
    "nodes": 1, "ntasks": 16, "cpus_per_task": 1,
    "walltime": "12:00:00", "partition": "shared"
  },
  "cluster_configs": {
    "<expanse_session_id>": {
      "account": "sdp126",
      "partition": "shared",
      "module_loads": "module load cpu/0.17.3b\nmodule load gcc/10.2.0/npcyll4\nexport PATH=$HOME/openmpi-4.1.8/bin:$PATH\nexport LD_LIBRARY_PATH=$HOME/openmpi-4.1.8/lib:$LD_LIBRARY_PATH",
      "orca_dir": "/home/jyang25/orca_6_1_1_RRP8",
      "default_template": "<contents of server/templates/orca_generic.sh>",
      "default_job_params": {
        "nodes": 1, "ntasks": 16, "cpus_per_task": 1,
        "walltime": "12:00:00", "partition": "shared"
      }
    }
  }
})
```

The local-scratch template stages I/O to `$TMPDIR/orca_$SLURM_JOB_ID` and copies
results back. Required on Expanse — Lustre kills ORCA's many-small-file I/O during
the 30-root TD-DFT response solver.

### 5. Monitor

```json
catgo_workflow(action: "status", workflow_id: "<wf_id>")
```

### 6. Pull files for post-processing

When status is COMPLETED, pull `ORCA.out` plus the JSON files OPI parses,
then run the parser/plotter from Stage 2 below against the local copy:

```bash
mkdir -p ./local_run
for f in ORCA.out ORCA.property.json ORCA.json; do
  curl -s -X POST http://localhost:8000/api/hpc/files/read-content \
    -H 'Content-Type: application/json' \
    -d "{\"session_id\":\"<expanse_session_id>\",\"file_path\":\"<work_dir>/$f\"}" \
    > ./local_run/$f
done
```

### Submission gotchas

- `catgo_workflow_engine.add_task` doesn't auto-attach the viewer structure → "No input structure provided".
- `partition=workq` (Shaheen default) is invalid on Expanse → use `debug`/`shared`/`compute`.
- `partition=debug` capped at 30 min — TD-DFT/30-roots almost always needs more.
- Missing `account=sdp126` → "Invalid account or account/partition combination".
- Missing `module_loads` + `orca_dir` → `orca` not on PATH; the response solver silently produces nothing.
- After re-connecting to Expanse, the session_id changes — re-discover via `/api/hpc/connections` and update both `default_session_id` and the `cluster_configs` key.

## Stage 2: Post-Processing

### Reading the Spectrum via OPI

OPI surfaces the absorption spectrum as `output.results_properties.geometries[-1].absorption_spectrum` — a `list[Spectrum]` keyed by `representation` (`"Length"` / `"Velocity"`) and `pointgroup`. This replaces the regex parser entirely:

- The `rfind`-vs-`find` STEOM-DLPNO-CCSD workaround is unnecessary; the model returns one entry per (representation, pointgroup) and you pick the one you want.
- The "STEOM rows have state labels, TD-DFT rows don't" branch is unnecessary; both produce the same `Spectrum` shape.
- Bonus: ECD rotational strengths come for free at `geometries[-1].ecd_spectrum`.

`Spectrum.excitationenergies` is a list of rows; columns are unnamed in the model but the order for ORCA 6.1.1 is fixed at `[energy_eV, energy_cm, wavelength_nm, fosc, |mu|^2]`. The shared helper exposes this as `UVVIS_COLS`.

### Reference Parser and Plotter

```python
import sys
sys.path.insert(0, ".claude/skills")  # for the _shared helper
import numpy as np
import matplotlib.pyplot as plt
from _shared.orca_opi import parse_local, UVVIS_COLS


def parse_orca_tddft(work_dir="./local_run"):
    out = parse_local(work_dir)
    spectra = out.results_properties.geometries[-1].absorption_spectrum
    if not spectra:
        raise ValueError("No absorption_spectrum block found — check ORCA.property.json")
    # Prefer length representation; fall back to whatever's first.
    target = next((s for s in spectra if s.representation == "Length"), spectra[0])

    wl_col = UVVIS_COLS["wavelength_nm"]
    f_col = UVVIS_COLS["fosc"]
    wavelengths = np.array([row[wl_col] for row in target.excitationenergies])
    fosc = np.array([row[f_col] for row in target.excitationenergies])
    return wavelengths, fosc


def gaussian(x, center, height, sigma=15):
    return height * np.exp(-0.5 * ((x - center) / sigma) ** 2)


def plot_uv_vis(wavelengths, fosc, output_png="uv_vis_spectrum.png"):
    x = np.linspace(200, 800, 2000)
    spectrum = sum(gaussian(x, w, f) for w, f in zip(wavelengths, fosc))
    peak = spectrum.max()
    if peak > 0:
        spectrum = spectrum / peak

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, spectrum, color="#2563eb", linewidth=1.5, label="Broadened")
    f_peak = fosc.max() if fosc.size and fosc.max() > 0 else 1.0
    ax.vlines(wavelengths, 0, fosc / f_peak, color="#ef4444", alpha=0.7, label="Transitions")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Normalized Absorbance")
    ax.set_xlim(200, 800)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(output_png, dpi=150)
    print(f"Spectrum saved to {output_png}")


if __name__ == "__main__":
    work_dir = sys.argv[1] if len(sys.argv) > 1 else "./local_run"
    png_name = sys.argv[2] if len(sys.argv) > 2 else "uv_vis_spectrum.png"
    wl, f = parse_orca_tddft(work_dir)
    plot_uv_vis(wl, f, png_name)
```

### Viewing the spectrum in the IDE

After `plot_uv_vis(...)` writes the PNG, surface it inline with the shared helper:

```python
from _shared.orca_opi import show_png
show_png("uv_vis_spectrum.png", "UV-Vis spectrum")
# prints `![UV-Vis spectrum](uv_vis_spectrum.png)`
```

Then **reply to the user with that markdown link** so Claude Code renders the figure inline in chat.

### Plotting Defaults

- Wavelength grid: 200–800 nm, 2000 points
- Gaussian broadening: σ = 15 nm in wavelength space (simple and visually reasonable for most organic chromophores; call out that eV-space broadening is more physically correct if the user cares about vibronic lineshapes)
- Envelope normalized to max = 1
- Sticks normalized by the maximum oscillator strength so they sit on the same axis as the envelope
- Figure size 8×5, DPI 150
- Colors: envelope `#2563eb` (blue), sticks `#ef4444` (red) — matches CatGo's red-TS / blue-accent conventions

### Requesting eV on the x-axis

If the user asks for eV instead of nm, convert via `E_eV = 1240 / wavelength_nm` and rebuild the x-grid from (e.g.) 1.5–6.5 eV. Broadening σ of ~0.3 eV is a sensible default in eV space.
