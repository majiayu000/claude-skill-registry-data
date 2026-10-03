---
name: orca-opt
description: ORCA geometry optimization. Handles method/basis selection, dispersion corrections, solvent models, and convergence settings.
---

# ORCA Geometry Optimization Skill

## When to Use

Use this skill when the user wants to:
- Optimize a molecular geometry with ORCA
- Find the minimum energy structure of a molecule
- Relax a molecular cluster or complex

Do NOT use for periodic systems (use VASP or CP2K instead).

## Node Parameters (canonical names — these are what the engine actually reads)

| Parameter | Default | Description |
|---|---|---|
| `method` | B3LYP | DFT functional (e.g. `B3LYP`, `PBE0`, `wB97X-D4`, `r2SCAN-3c`) |
| `basis` | def2-SVP | Basis set (omit for composite methods like `r2SCAN-3c`) |
| `charge` | 0 | Total charge |
| `multiplicity` | 1 | Spin multiplicity (2S+1) |
| `dispersion` | (none) | `D4` \| `D3BJ` \| `D3` \| `none`. **Put D4/D3BJ HERE, not in `method`.** |
| `three_body_dispersion` | false | Adds ABC term (D3-class only; ignored for D4) |
| `grid` | DefGrid2 | `DefGrid1/2/3` — emitted only when ≠ default |
| `wavefunction` | (none) | e.g. `UKS` for unrestricted |
| `uno`, `uco` | false | Unrestricted natural / corresponding orbital tweaks |
| `num_cores` | 4 | `%pal nprocs` |
| `max_core_mb` | 4000 | `%maxcore` |
| `opt_convergence` | (none) | e.g. `TightOpt`, `VeryTightOpt` |

> ⚠️ **`extra_keywords` and `extra_blocks` are NOT read by the ORCA workflow engine.** Earlier versions of this skill recommended them; anything passed via those keys is silently dropped. Use the dedicated fields above. CPCM solvation, `SlowConv`/`SOSCF`, and `NumFreq` currently have no first-class field on the opt/freq/neb_ts/irc nodes — that is a node-def gap, not a usage problem.

## MCP Tool Examples — proven Expanse submission flow

> **Use `catgo_workflow` (graph-based), NOT `catgo_workflow_engine` (task-based).**
> The graph-based tool auto-captures the viewer structure on `create`. The task-based
> tool's `add_task` does not, so jobs fail with "No input structure provided".
> Param keys differ too: graph-based uses `method`/`basis`, task-based uses
> `orca_method`/`orca_basis`.

### 1. Confirm structure is loaded

```json
catgo_view(action: "get_state")
```

### 2. Find the Expanse session_id

Session IDs are volatile — they change on every reconnect. Discover the current one:

```bash
curl -s http://localhost:8000/api/hpc/connections
```

Look for the entry with `host: login.expanse.sdsc.edu` and copy its `session_id`.

### 3. Create the workflow (auto-captures viewer structure)

```json
catgo_workflow(action: "create", name: "Benzene optimization")
```

Returns a workflow with one `structure_input` node containing the current viewer
structure. Note its node ID (e.g., `n1777012885-iode`).

### 4. Add the geo_opt node and connect it

Inject `extra_blocks: "%output jsongbwfile True jsonpropfile True end"` so ORCA
emits the JSON files OPI parses on the way back. Without this, OPI parsing
falls back to grepping `ORCA.out` (still works, just less rich).

```json
catgo_workflow(action: "batch", workflow_id: "<wf_id>", operations: [
  {"op": "add_node", "node_type": "geo_opt", "label": "opt",
   "params": {
     "software": "orca",
     "method": "B3LYP",
     "basis": "def2-SVP",
     "charge": 0,
     "multiplicity": 1,
     "extra_blocks": "%output jsongbwfile True jsonpropfile True end"
   }},
  {"op": "connect", "from_id": "<structure_input_id>", "to_id": "opt",
   "from_handle": "structure", "to_handle": "structure"}
])
```

### 5. Run with the full HPC run_config

Real opt jobs on non-trivial molecules can run for hours — default to
`partition: "shared"` with a generous walltime. Use `debug` only for tiny
sanity checks (≤ a couple of heavy atoms, single-point or quick test). Read
`server/templates/orca_generic.sh` and pass its contents as `default_template`.

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

For a quick sanity check (e.g., H2O / methane / single small molecule),
override to `partition: "debug"`, `walltime: "00:30:00"`, `ntasks: 4`. The
debug partition caps at 30 min — anything bigger will be rejected after the
limit.

The local-scratch template stages I/O to `$TMPDIR/orca_$SLURM_JOB_ID` and copies
results back to the Lustre work_dir. Required on Expanse — Lustre is bad for
ORCA's many small temp files.

### 6. Common parameter variations

For dispersion (non-covalent systems, dimers, π-stacking, H-bonding):
```json
"params": {"method": "B3LYP", "basis": "def2-TZVP", "dispersion": "D3BJ", "charge": 0, "multiplicity": 1}
```

For D4 (newer Grimme correction, slightly better for metals):
```json
"params": {"method": "B3LYP", "basis": "def2-SVP", "dispersion": "D4", "charge": 0, "multiplicity": 1}
```

For implicit solvation:
> CPCM is currently a node-def gap on opt/freq/neb_ts/irc — there's no first-class `solvation`/`solvent` field, and `extra_keywords` is not read. UV-Vis is the exception (it has dedicated `solvation`/`solvent` fields). Until this is fixed, single-point CPCM on a gas-phase optimized geometry, or running on a non-CatGo input file, is the workaround.

For tight convergence (publication quality, pre-freq):
```json
"params": {"method": "B3LYP", "basis": "def2-TZVP", "opt_convergence": "TightOpt", "dispersion": "D3BJ", "charge": 0, "multiplicity": 1}
```

For open-shell radicals:
```json
"params": {"method": "UB3LYP", "basis": "def2-SVP", "charge": 0, "multiplicity": 2}
```

### 7. Monitor

```json
catgo_workflow(action: "status", workflow_id: "<wf_id>")
```

Or query SLURM directly via the live session:

```bash
curl -s "http://localhost:8000/api/hpc/jobs/<job_id>?session_id=<expanse_session_id>"
```

### 8. Pull results when COMPLETED

Pull the ORCA outputs into a local directory, including the OPI JSON files
(`*.property.json` is the rich structured output OPI parses):

```bash
mkdir -p ./local_run
for f in ORCA.out ORCA.xyz ORCA.engrad ORCA.property.json ORCA.json; do
  curl -s -X POST http://localhost:8000/api/hpc/files/read-content \
    -H 'Content-Type: application/json' \
    -d "{\"session_id\":\"<expanse_session_id>\",\"file_path\":\"<work_dir>/$f\"}" \
    > ./local_run/$f
done
```

`ORCA.json` and `ORCA.property.json` only exist if the input had the
`%output jsongbwfile True jsonpropfile True end` block (step 4). If you
omitted it, OPI parsing falls back to grepping `ORCA.out`.

### 9. Parse with OPI

Replaces hand-walking `ORCA.xyz` / `ORCA.engrad`. Requires `pip install orca-pi`.

```python
import sys
sys.path.insert(0, ".claude/skills")  # for the _shared helper
from _shared.orca_opi import parse_local

out = parse_local("./local_run")

print("SCF converged:        ", out.scf_converged())
print("Geometry converged:   ", out.geometry_optimization_converged())
print("Final energy (Eh):    ", out.get_final_energy())
print("Optimized XYZ:\n", out.get_structure().to_xyz_block())

# Per-step trajectory (energy curve)
for i, geom in enumerate(out.results_properties.geometries):
    print(i, geom.single_point_data.finalenergy)

# Population analyses (any of these are one call now)
mulliken = out.get_mulliken()
print("HOMO/LUMO/gap (eV):", out.get_homo(), out.get_lumo(), out.get_hl_gap())
```

### Viewing the optimization curve in the IDE

Use the shared helper to plot per-step energies and surface the PNG inline.

```python
from _shared.orca_opi import quick_plot_opt_energy, show_png
png = quick_plot_opt_energy(out)            # writes ./local_run/opt_energy.png
show_png(png, "Opt energy convergence")     # prints `![Opt energy convergence](local_run/opt_energy.png)`
```

After running this, **reply to the user with the markdown link** the script printed (e.g. `![Opt energy convergence](local_run/opt_energy.png)`) so Claude Code renders the figure inline in chat.

### Submission gotchas (real failures we hit)

- `catgo_workflow_engine.add_task` doesn't auto-attach the viewer structure → "No input structure provided".
- `partition=workq` (Shaheen default) is invalid on Expanse → use `debug` or `shared`.
- Missing `account=sdp126` → "Invalid account or account/partition combination".
- Missing `module_loads` + `orca_dir` → `orca` not on PATH, job runs ORCA-not-found and silently produces nothing.
- After re-connecting to Expanse, the session_id changes — re-discover via `/api/hpc/connections` and update `default_session_id` + `cluster_configs` key.
- Engine doesn't regenerate `submit.sh` on `retry` alone — call `run` with the new `run_config` to get a fresh script with updated SBATCH headers.

## Dispersion Corrections

| Keyword | Method | When to use |
|---|---|---|
| `D3BJ` | Grimme D3 with Becke-Johnson damping | Default choice for dispersion |
| `D3` | Grimme D3 with zero damping | Legacy, use D3BJ instead |
| `D4` | Grimme D4 | Newer, slightly better for metals |

Always include dispersion for: molecular dimers, adsorption complexes,
conformational searches, anything with pi-stacking or H-bonding.

## Basis Set Ladder

| Basis | Quality | Cost | Use |
|---|---|---|---|
| def2-SVP | Double-zeta | Low | Screening, initial opt |
| def2-TZVP | Triple-zeta | Medium | Production geometry |
| def2-TZVPP | Triple-zeta+pol | High | Accurate energetics |
| def2-QZVPP | Quadruple-zeta | Very high | Benchmark only |

Strategy: optimize with def2-SVP, then single-point with def2-TZVP for energy.

## SCF Convergence Issues

ORCA SCF tweaks like `SlowConv`, `VerySlowConv`, `SOSCF`, `SmearTemp 5000` are not exposed as first-class node params (gap in the engine). For now: pre-optimize with a smaller basis (def2-SVP) and feed that geometry to a larger-basis run, or run ORCA directly on a hand-edited input file outside the workflow engine.

## Common Mistakes

- Forgetting dispersion for non-covalent systems (huge geometry errors)
- Using restricted (R) method for open-shell (use UB3LYP, not B3LYP)
- Basis set too large for optimization (optimize with SVP, refine energy with TZVP)
- Not checking for imaginary frequencies after optimization
