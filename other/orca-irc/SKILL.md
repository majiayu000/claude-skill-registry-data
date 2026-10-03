---
name: orca-irc
description: Generate ORCA input files for IRC (Intrinsic Reaction Coordinate) calculations and post-process the results. Use this skill whenever the user asks about IRC calculations, reaction path following, confirming transition state connectivity, or tracing a minimum energy path from a TS in ORCA. Also trigger when the user mentions IRC endpoints, forward/backward reaction paths, or needs to verify that a TS connects to expected reactants and products.
---

# ORCA IRC Calculation Skill

This skill handles the full IRC workflow: generating an ORCA input file from a confirmed transition state geometry, and post-processing the output to extract the reaction-path energy profile and endpoint geometries.

**Scope:** Input generation, local post-processing, and (optionally) HPC submission via the CatGo workflow engine. The "Submitting to HPC" section below covers the proven Expanse flow. If the user is running on their own non-CatGo infrastructure, just generate the input file from the template in Stage 1 and skip the submission section.

**Target version:** ORCA 6.x. The parser and defaults below are written against the ORCA 6 output layout used by CatGo's own parser (`server/catgo/utils/orca_output.py::OrcaIrcOutput`).

## Prerequisites

IRC requires a transition state geometry that has been confirmed by a frequency calculation showing exactly one imaginary frequency corresponding to the reaction coordinate.

If the user has not run a frequency calculation on the candidate TS, suggest the `orca-freq` skill before generating an IRC input. Running IRC on a geometry that isn't a true first-order saddle point produces meaningless paths. This is a suggestion, not a hard stop — if the user confirms they know what they're doing and still wants the input, generate it.

## Stage 1: Input Generation

Before generating the input, gather from the user:

- **TS geometry** — file path or pasted XYZ coordinates
- **Method and basis set** — must match whatever was used for the TS optimization and frequency calculation. Method/basis consistency across Opt → Freq → IRC is critical; mixing levels means the TS may not be a stationary point on the new surface.
- **Charge and multiplicity**
- **Number of cores** (`%pal nprocs`)
- **Memory per core** (`%maxcore`, in MB)

Optional (apply only if user specifies):

- Solvent model (CPCM). Gas-phase IRC is standard practice for confirming connectivity; solvation mainly affects barrier heights, not topology.
- Dispersion correction — again, match whatever was used for the TS search.

### Hessian Handling (important — read all of this)

IRC moves downhill from the TS along the imaginary-frequency mode. To identify that mode, ORCA needs a Hessian **at the TS geometry**. Getting this step right is the single biggest factor in whether the IRC gives a sensible path.

**What the Hessian is used for, concretely:**

1. Diagonalize to find the mode with a negative eigenvalue (the imaginary frequency). That eigenvector is the initial descent direction.
2. Build a mass-weighted quadratic model around the TS. The very first displacement along the mode is scaled by `Scale_Displ_SD`, chosen (via `Init_Displ_DE`) to correspond to a target drop in energy.
3. Subsequent steps use an adaptive integrator in mass-weighted coordinates; the Hessian is not re-diagonalized every step (that's what `SD` vs. `LQA` flavors are about), but the first-step quality dominates the final path.

**Consequences:**

- A Hessian with more than one negative eigenvalue means your geometry is not a clean TS. IRC will pick *one* of the negative modes and the result is arbitrary. Fix the TS first.
- A numerically noisy Hessian (bad SCF convergence, too-loose grid) can flip the sign of a small imaginary mode or rotate the eigenvector into a nearby low-frequency mode. The IRC then follows the wrong coordinate — often tumbling, rotation, or a methyl rock instead of the bond-making/breaking mode. `calc_numfreq` or `InitHess read` from a converged `AnFreq` job is the fix.
- Reusing a `.hess` file from a calculation at a *different* method/basis/grid/solvation is a silent footgun. The eigenmode numbering can differ, so "the imaginary mode" may not be the same mode on the IRC surface. **Only use `InitHess read` if the `.hess` was produced at the same level as this IRC job.**

**The three options:**

**Option A — `InitHess read` (preferred when applicable):** Read a pre-computed `.hess` file from the frequency calculation at the same level of theory. Fastest and most accurate, because the Hessian is already well-converged and you skip recomputing it. Ask the user for the filename.

```
%irc
  InitHess read
  Hess_Filename "previous_freq.hess"
end
```

**Option B — `InitHess calc_anfreq`:** Compute analytical frequencies at the start of the IRC. Use when no `.hess` file is available and the method supports analytical Hessians (common DFT functionals, HF). Cleanest and still fairly fast for small-to-medium systems.

```
%irc
  InitHess calc_anfreq
end
```

**Option C — `InitHess calc_numfreq`:** Compute numerical frequencies. Use when analytical Hessians aren't available or aren't reliable for the chosen method (some double hybrids, multireference, custom-parameter methods). Much slower (scales with 6N SCFs) but works everywhere.

```
%irc
  InitHess calc_numfreq
end
```

**Decision flow for the skill:** ask "Do you have a `.hess` file from your frequency calculation at this level of theory?" If yes → Option A with filename. If no and the method supports analytical Hessians → Option B. If no and it doesn't → Option C.

### IRC Parameters and ORCA Defaults

ORCA 6's documented defaults:

- `MaxIter` = **20** iterations per arm
- `Step` = **adaptive**, governed by `Scale_Displ_SD` (initial value derived from `Init_Displ_DE`) and dynamically rescaled — bounded to 1/16× – 4× of the initial value. There is no single fixed step-size default to quote.

The default 20 iterations is often too few to reach a clear minimum, so the recommended override is:

```
%irc
  MaxIter 70
  PrintLevel 1
  Direction both
end
```

Do **not** set `Step` unless the user specifically asks for a fixed step — the adaptive algorithm is usually better than any constant. If the path behaves badly, the right lever is usually `MaxIter`, `InitHess`, or the TS quality, not a fixed step size.

Rationale for the overrides:

- `MaxIter 70` — ORCA's default of 20 is almost always too few for a path that reaches a clear minimum. Bump to 100–150 for flat PES regions.
- `PrintLevel 1` — prints energy and gradient at each step so the run can be monitored and the path summary is written in full.
- `Direction both` — follows the path in both directions from the TS. Almost always what you want when confirming connectivity.

### Composite Methods

For composite methods like `PBEh-3c` or `r²SCAN-3c`, do NOT specify a separate basis set — the basis is built into the method keyword.

```
! PBEh-3c IRC
```

This automatically satisfies method/basis consistency since the composite method has a fixed internal basis.

### Template

```
# ORCA IRC Calculation
# Method: {method} {basis}
# TS confirmed by frequency calculation: {num_imaginary} imaginary mode(s)

%pal nprocs {nprocs} end
%maxcore {maxcore}

! {method} {basis} {dispersion} IRC

%irc
  InitHess {inithess_option}
  {hess_filename_line}
  MaxIter 70
  PrintLevel 1
  Direction both
end

%output jsongbwfile True jsonpropfile True end

* xyzfile {charge} {multiplicity} {ts_geometry_file}
```

When generating the input:

- If the user provides inline coordinates, use `* xyz {charge} {mult}` followed by the coordinates and closing `*`.
- Omit `{dispersion}` if already included in a composite method.
- Omit `{basis}` for composite methods.
- Omit the `Hess_Filename` line unless using `InitHess read`.
- Keep the `%output jsongbwfile True jsonpropfile True end` line — it makes ORCA emit the JSON files OPI's `Output.parse()` consumes during post-processing (Stage 2).

### About OPI input builders

OPI (`pip install orca-pi`) ships typed `BlockIrc` builders that validate keys at construction. **However, the catgo backend's `irc` node already emits its own `%irc` block from node params (`irc_max_iter`, `irc_direction`, `init_hess`, etc.).** Pasting an OPI-built `%irc` block via `extra_blocks` would produce **two `%irc` blocks** in the same `.inp`, which is undefined behavior.

For this skill, **stick with node params** for `%irc` content and use `extra_blocks` only for `%output`. The OPI parsing wins (Stage 2) still apply. If you need a knob `BlockIrc` exposes that the node params don't (`scale_init_displ`, `tolmaxg`, `monitor_internals`, etc.), open that as a node-def gap rather than dual-emitting blocks.

## Submitting to HPC (Expanse) — proven flow

Use this when the user wants the CatGo workflow engine to run the IRC on Expanse.
Skip if they only want the input file.

> **Use `catgo_workflow` (graph-based), NOT `catgo_workflow_engine` (task-based).**
> The graph-based tool auto-captures the viewer structure on `create` and lets
> you wire opt → freq → IRC explicitly. Param keys differ from the task-based
> API: graph-based uses `method`/`basis`, task-based uses `orca_method`/`orca_basis`.

### 1. Confirm TS structure is loaded and find session_id

```json
catgo_view(action: "get_state")
```

```bash
curl -s http://localhost:8000/api/hpc/connections
```

Copy the `session_id` for `host: login.expanse.sdsc.edu`.

### 2. Create the workflow (auto-captures the TS structure)

```json
catgo_workflow(action: "create", name: "IRC from TS")
```

### 3. Add the IRC node

```json
catgo_workflow(action: "batch", workflow_id: "<wf_id>", operations: [
  {"op": "add_node", "node_type": "irc", "label": "irc1",
   "params": {
     "software": "orca",
     "method": "B3LYP",
     "basis": "def2-SVP",
     "charge": 0,
     "multiplicity": 1,
     "dispersion": "D3BJ",
     "max_iterations": 70
   }},
  {"op": "connect", "from_id": "<structure_input_id>", "to_id": "irc1",
   "from_handle": "structure", "to_handle": "structure"}
])
```

### Canonical IRC node params (what the engine actually reads)

| Parameter | Default | Description |
|---|---|---|
| `method` | r2SCAN-3c | DFT functional |
| `basis` | 6-31G | Basis set (omit for composite methods) |
| `charge` / `multiplicity` | 0 / 1 | |
| `dispersion` | (none) | `D4` \| `D3BJ` \| `D3` — **use this field, NOT `extra_keywords`** |
| `grid` | DefGrid2 | `DefGrid1/2/3` |
| `max_iterations` | 30 | per-arm iteration cap (legacy alias: `max_irc_iterations`) |
| `num_cores` / `max_core_mb` | 4 / 4000 | `%pal nprocs` / `%maxcore` |

> ⚠️ **Hessian-source / step-control params (`init_hess`, `irc_direction`, `Init_Displ_DE`, etc.) are not currently read by the IRC engine code path** ([server/workflow/engines/orca.py:218](server/workflow/engines/orca.py#L218)). The engine emits a minimal `%irc MaxIter ... end` block from `max_iterations` only. To control Hessian source, direction, or initial displacement, either (a) extend the node-def, or (b) skip the workflow engine and run ORCA directly on a hand-edited input file using the Stage 1 template above.

### 4. Run with the full HPC run_config

IRC chains many SCFs along the path — bump `walltime` and prefer `shared`/`compute`
over `debug`. Read `server/templates/orca_generic.sh` and pass its contents as
`default_template`.

```json
catgo_workflow(action: "run", workflow_id: "<wf_id>", run_config: {
  "execution_mode": "hpc",
  "default_session_id": "<expanse_session_id>",
  "base_work_dir": "/expanse/lustre/projects/sdp126/jyang25/ORCA/catgo",
  "default_job_params": {
    "nodes": 1, "ntasks": 8, "cpus_per_task": 1,
    "walltime": "04:00:00", "partition": "shared"
  },
  "cluster_configs": {
    "<expanse_session_id>": {
      "account": "sdp126",
      "partition": "shared",
      "module_loads": "module load cpu/0.17.3b\nmodule load gcc/10.2.0/npcyll4\nexport PATH=$HOME/openmpi-4.1.8/bin:$PATH\nexport LD_LIBRARY_PATH=$HOME/openmpi-4.1.8/lib:$LD_LIBRARY_PATH",
      "orca_dir": "/home/jyang25/orca_6_1_1_RRP8",
      "default_template": "<contents of server/templates/orca_generic.sh>",
      "default_job_params": {
        "nodes": 1, "ntasks": 8, "cpus_per_task": 1,
        "walltime": "04:00:00", "partition": "shared"
      }
    }
  }
})
```

The local-scratch template stages I/O to `$TMPDIR/orca_$SLURM_JOB_ID` and copies
results back. Required on Expanse — Lustre kills ORCA's many-small-file I/O
during per-step SCFs.

### 5. Monitor

```json
catgo_workflow(action: "status", workflow_id: "<wf_id>")
```

### 6. Pull files for post-processing

When status is COMPLETED, pull the output and trajectory files referenced in
Stage 2 below:

```bash
mkdir -p ./local_run
for f in ORCA.out ORCA_IRC.dat ORCA_IRC.xyz ORCA_IRC_F.xyz ORCA_IRC_B.xyz \
         ORCA.property.json ORCA.json; do
  curl -s -X POST http://localhost:8000/api/hpc/files/read-content \
    -H 'Content-Type: application/json' \
    -d "{\"session_id\":\"<expanse_session_id>\",\"file_path\":\"<work_dir>/$f\"}" \
    > ./local_run/$f
done
```

Then run the parser/plotter from Stage 2 against the local copy.

### Submission gotchas

- `catgo_workflow_engine.add_task` doesn't auto-attach the viewer structure → "No input structure provided".
- `partition=workq` (Shaheen default) is invalid on Expanse → use `debug`/`shared`/`compute`.
- `partition=debug` capped at 30 min — IRC almost always needs more.
- Missing `account=sdp126` → "Invalid account or account/partition combination".
- Missing `module_loads` + `orca_dir` → `orca` not on PATH; per-step SCFs silently produce nothing.
- After re-connecting to Expanse, the session_id changes — re-discover via `/api/hpc/connections` and update both `default_session_id` and the `cluster_configs` key.
- A `.hess` from a different method/basis/grid is a silent footgun for `init_hess: "read"` — only reuse a `.hess` produced at exactly this IRC's level of theory.

## Stage 2: Post-Processing

After the IRC completes, ORCA produces:

| File | Contents |
|------|----------|
| `{basename}.out` | Main output with per-step energies/gradients and the `IRC PATH SUMMARY` table |
| `{basename}_IRC.dat` | Clean tabular file: step, energy (Eh), path length — easiest programmatic source when present |
| `{basename}_IRC.xyz` | Full trajectory: concatenated geometries from backward end → TS → forward end |
| `{basename}_IRC_F_trj.xyz` | Forward-arm trajectory |
| `{basename}_IRC_B_trj.xyz` | Backward-arm trajectory |
| `{basename}_IRC_F.xyz` | Final endpoint geometry (forward direction) |
| `{basename}_IRC_B.xyz` | Final endpoint geometry (backward direction) |

The forward/backward labeling is arbitrary — it depends on the sign of the initial displacement. The user identifies which endpoint is reactant vs. product by looking at the geometries.

### Parsing the Energy Profile

Parse the `IRC PATH SUMMARY` table in the main output file. OPI does not model this block as a typed object, but its grepper recipe replaces the bespoke "find marker, slice 10 KB, walk lines" boundary handling with a single call. Requires `pip install orca-pi`.

Each row has the shape:

```
<step>   <E_Eh>   <dE_kcal/mol>   <max_grad>   <rms_grad>   [<= TS]
```

Reference parser using OPI's grepper:

```python
import re
import sys
sys.path.insert(0, ".claude/skills")  # for the _shared helper
from _shared.orca_opi import grep_block

ROW_PATTERN = re.compile(
    r"(\d+)\s+([-\d.]+)\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)\s*(.*)"
)


def parse_irc_path(output_file):
    # offset=2 skips the header + ruler; count is a safe upper bound.
    lines = grep_block(output_file, "IRC PATH SUMMARY", offset=2, count=400)

    steps = []
    ts_raw_step = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = ROW_PATTERN.match(line)
        if not m:
            continue
        raw_step = int(m.group(1))
        is_ts = "<= TS" in m.group(6)
        if is_ts:
            ts_raw_step = raw_step
        steps.append({
            "step":          raw_step,
            "energy_eh":     float(m.group(2)),
            "dE_kcal_mol":   float(m.group(3)),
            "max_gradient":  float(m.group(4)),
            "rms_gradient":  float(m.group(5)),
            "is_ts":         is_ts,
        })

    # Re-index so backward steps are negative, TS = 0, forward positive
    if ts_raw_step is not None:
        for s in steps:
            s["step"] -= ts_raw_step
    return steps


# Sanity check before parsing — replaces hand-grep of "ORCA TERMINATED NORMALLY"
from opi.output.grepper.recipes import has_terminated_normally
assert has_terminated_normally(output_file)
```

### Plotting the Energy Profile

Plotting matches the style used by CatGo's `IrcPathPlot.svelte`: ΔE in kcal/mol on the y-axis, IRC step number (re-indexed relative to the TS) on the x-axis, backward arm in purple, forward arm in green, TS marked with a red point and an amber dashed vertical line.

```python
import matplotlib.pyplot as plt


BACKWARD_COLOR = "#8b5cf6"
FORWARD_COLOR = "#10b981"
TS_COLOR = "#ef4444"
TS_GUIDE = "#f59e0b"


def plot_irc_profile(steps, output_png="irc_profile.png"):
    xs = [s["step"] for s in steps]
    ys = [s["dE_kcal_mol"] for s in steps]

    ts_idx = next((i for i, s in enumerate(steps) if s["is_ts"]), None)

    fig, ax = plt.subplots(figsize=(8, 5))

    if ts_idx is not None:
        ax.plot(xs[: ts_idx + 1], ys[: ts_idx + 1], color=BACKWARD_COLOR,
                linewidth=1.5, marker="o", markersize=3, label="Backward")
        ax.plot(xs[ts_idx:], ys[ts_idx:], color=FORWARD_COLOR,
                linewidth=1.5, marker="o", markersize=3, label="Forward")
        ax.scatter([xs[ts_idx]], [ys[ts_idx]], color=TS_COLOR, s=60,
                   zorder=5, label="TS")
        ax.axvline(xs[ts_idx], color=TS_GUIDE, linestyle="--",
                   linewidth=1, alpha=0.7)
    else:
        ax.plot(xs, ys, color=FORWARD_COLOR, linewidth=1.5, marker="o",
                markersize=3)

    ax.set_xlabel("IRC Step (relative to TS)")
    ax.set_ylabel("ΔE (kcal/mol)")
    ax.legend(loc="best", frameon=False)
    fig.tight_layout()
    fig.savefig(output_png, dpi=150)
    print(f"Profile saved to {output_png}")


if __name__ == "__main__":
    import sys
    steps = parse_irc_path(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else "irc_profile.png"
    plot_irc_profile(steps, out)
```

### Viewing the IRC profile in the IDE

After `plot_irc_profile(...)` writes the PNG, surface it inline with the shared helper:

```python
sys.path.insert(0, ".claude/skills")
from _shared.orca_opi import show_png
show_png("irc_profile.png", "IRC energy profile")
# prints `![IRC energy profile](irc_profile.png)`
```

Then **reply to the user with that markdown link** so Claude Code renders the figure inline in chat.

Notes:

- `dE_kcal_mol` in the PATH SUMMARY is already relative to the TS, so TS sits at ΔE = 0 and both arms descend to negative values. No extra conversion needed.
- If the user wants path length on the x-axis instead of step number, use `{basename}_IRC.dat` as the source — it's cleaner than regex-parsing the main output.

### Extracting Endpoint Geometries

Read `{basename}_IRC_F.xyz` and `{basename}_IRC_B.xyz` to show the user the endpoint structures. Remind the user that these endpoint geometries are **not** fully optimized — they should run a follow-up geometry optimization on each endpoint to get proper reactant and product structures.

## Common Issues and Troubleshooting

**IRC terminates early / doesn't reach a minimum:** Increase `MaxIter` — try 100 or 150 for flat PES regions. Recompute with `InitHess calc_numfreq` if the initial direction looked wrong.

**IRC follows the wrong mode:** The initial Hessian is bad or the TS has extra low-lying imaginary frequencies. Use `InitHess read` with a `.hess` file from a converged frequency job at the same level, or switch from `calc_anfreq` to `calc_numfreq`. If the TS has more than one imaginary frequency, the geometry is not a true TS — fix it first.

**IRC connects to unexpected structures:** The TS probably corresponds to a different reaction than intended. Common with NEB-TS when the algorithm finds a stepwise mechanism instead of a concerted one. Re-run the TS search with a different guess geometry or a tighter NEB.

**Energy goes up instead of down:** Sign of a bad Hessian or the geometry not being a true TS. Recompute the Hessian with `NumFreq` and verify exactly one imaginary mode before rerunning IRC.

**Solvation:** Gas-phase IRC is standard for connectivity confirmation. If the user needs a solvated energy profile, single-point CPCM calculations on the gas-phase IRC geometries are more practical than running the full IRC with CPCM.
