---
name: neb_ts
description: ORCA NEB-TS transition state search. Requires reactant and product structures. Handles NEB parameters, image count, and CI-NEB settings.
---

# ORCA NEB-TS Transition State Skill

## When to Use

Use this skill when the user wants to:
- Find a transition state between two structures
- Calculate a reaction barrier
- Map a minimum energy path (MEP) between reactant and product

Requirements: the user MUST provide both a reactant and a product structure.
If only one structure is available, ask for the other before proceeding.

## How NEB-TS Works

1. ORCA interpolates images between reactant and product geometries
2. NEB optimization finds the minimum energy path
3. Climbing-image NEB (CI-NEB) refines the highest-energy image
4. The TS is characterized by exactly one imaginary frequency

## MCP Tool Examples — proven Expanse submission flow

> **Use `catgo_workflow` (graph-based), NOT `catgo_workflow_engine` (task-based).**
> NEB-TS needs TWO structure inputs (reactant + product) wired to separate input
> ports. The graph-based tool lets you build that wiring explicitly. Param keys
> also differ: graph-based uses `method`/`basis`, task-based uses
> `orca_method`/`orca_basis`.

### Step 1: Load both structures and capture their JSON

NEB-TS needs reactant **and** product. The `create` action auto-captures only
the viewer structure, so capture each one separately and pass them inline.

Load reactant into viewer (file or PubChem):

```json
catgo_structure(action: "load_file", file_content: "<reactant xyz>", file_format: "xyz")
```

Capture its JSON:

```json
catgo_view(action: "get_state")
```
Save the resulting structure JSON as `<reactant_json>`.

Then load and capture the product the same way → `<product_json>`.

### Step 2: Find Expanse session_id

```bash
curl -s http://localhost:8000/api/hpc/connections
```

Copy the `session_id` for `host: login.expanse.sdsc.edu`.

### Step 3: Create the workflow

```json
catgo_workflow(action: "create", name: "NEB-TS Cl- + CH3Br")
```

Note the auto-created `structure_input` node ID. You'll either reuse it for
the reactant (and add a second structure_input for the product) or remove it
and add two fresh ones.

### Step 4: Wire reactant + product → orca_neb_ts

```json
catgo_workflow(action: "batch", workflow_id: "<wf_id>", operations: [
  {"op": "add_node", "node_type": "structure_input", "label": "reactant",
   "params": {"structure_json": "<reactant_json>"}},
  {"op": "add_node", "node_type": "structure_input", "label": "product",
   "params": {"structure_json": "<product_json>"}},
  {"op": "add_node", "node_type": "orca_neb_ts", "label": "neb",
   "params": {
     "software": "orca",
     "method": "B3LYP",
     "basis": "def2-SVP",
     "dispersion": "D4",
     "charge": -1,
     "multiplicity": 1,
     "nimages": 8,
     "ts_opt": true,
     "neb_cycles": 100
   }},
  {"op": "connect", "from_id": "reactant", "to_id": "neb",
   "from_handle": "structure", "to_handle": "structure"},
  {"op": "connect", "from_id": "product", "to_id": "neb",
   "from_handle": "structure", "to_handle": "structure_product"}
])
```

The two `connect` ops are critical — `to_handle` must be `structure` for the reactant edge and `structure_product` for the product edge. (Verify with `node_details(orca_neb_ts)` — input handles are `["structure", "structure_product"]`.) If both go to `structure` the neb task sees a list and uses only the first.

### Step 5: Optional — chain a freq node to verify the TS

```json
{"op": "add_node", "node_type": "freq", "label": "freq_ts",
 "params": {"software": "orca", "method": "B3LYP", "basis": "def2-SVP", "charge": -1, "multiplicity": 1}},
{"op": "connect", "from_id": "neb", "to_id": "freq_ts",
 "from_handle": "structure", "to_handle": "structure"}
```

A valid TS shows exactly one imaginary frequency.

### Step 6: Run with the full HPC run_config

NEB-TS is much more expensive than a single opt — bump `walltime` accordingly,
and consider `partition: "shared"` or `"compute"` instead of `"debug"` (which
caps at 30 min). Read `server/templates/orca_generic.sh` and pass its contents
as `default_template`.

```json
catgo_workflow(action: "run", workflow_id: "<wf_id>", run_config: {
  "execution_mode": "hpc",
  "default_session_id": "<expanse_session_id>",
  "base_work_dir": "/expanse/lustre/projects/sdp126/jyang25/ORCA/catgo",
  "default_job_params": {
    "nodes": 1, "ntasks": 8, "cpus_per_task": 1,
    "walltime": "08:00:00", "partition": "shared"
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
        "walltime": "08:00:00", "partition": "shared"
      }
    }
  }
})
```

The local-scratch template stages I/O to `$TMPDIR/orca_$SLURM_JOB_ID` and
copies results back. Required on Expanse — Lustre kills ORCA's many-small-file
I/O during the per-image SCFs.

### Step 7: Monitor and pull results

```json
catgo_workflow(action: "status", workflow_id: "<wf_id>")
```

```bash
mkdir -p ./local_run
for f in ORCA.out ORCA_MEP_trj.xyz ORCA.NEB.log \
         ORCA.property.json ORCA.json; do
  curl -s -X POST http://localhost:8000/api/hpc/files/read-content \
    -H 'Content-Type: application/json' \
    -d "{\"session_id\":\"<expanse_session_id>\",\"file_path\":\"<work_dir>/$f\"}" \
    > ./local_run/$f
done
```

### Step 8: Parse with OPI

OPI gives a per-image energy curve and the converged-TS imaginary-frequency
check without regex. Requires `pip install orca-pi`.

```python
import sys
sys.path.insert(0, ".claude/skills")  # for the _shared helper
from _shared.orca_opi import parse_local

out = parse_local("./local_run")

# Per-image energy curve — geometries[i] holds each image's properties
energies_eh = [
    g.single_point_data.finalenergy
    for g in out.results_properties.geometries
]
print("MEP energies (Eh):", energies_eh)
print("Barrier (Eh):", max(energies_eh) - energies_eh[0])

# Converged TS imaginary check (after NEB-TS refinement step)
ts_freqs = out.results_properties.geometries[-1].thermochemistry_energies[0].freq
n_imag = sum(1 for f in ts_freqs if f < 0)
assert n_imag == 1, f"Expected 1 imaginary mode, got {n_imag}"
print("Imaginary mode (cm^-1):", min(ts_freqs))
```

NEB does not always produce a thermochemistry block (depends on whether NEB-TS
finished its frequency confirmation step). If `thermochemistry_energies` is
missing, run a follow-up `freq` node on the converged TS structure.

### Viewing the MEP curve in the IDE

```python
from _shared.orca_opi import quick_plot_neb_mep, show_png
png = quick_plot_neb_mep(out)            # writes ./local_run/neb_mep.png
show_png(png, "NEB-TS MEP")              # prints `![NEB-TS MEP](local_run/neb_mep.png)`
```

After running this, **reply to the user with the markdown link** the script printed so Claude Code renders the figure inline in chat.

### Submission gotchas (real failures we hit)

- `catgo_workflow_engine.add_task` doesn't auto-attach structures → "No input structure provided".
- Connecting both reactant and product to `to_handle: "structure"` (default) → neb task sees a list, uses only the first → garbage path. Use `reactant` and `product` handles explicitly.
- `partition=workq` (Shaheen default) is invalid on Expanse → use `debug`/`shared`/`compute`.
- `partition=debug` capped at 30 min — use `shared` for any real NEB-TS run.
- Missing `account=sdp126` → "Invalid account or account/partition combination".
- Missing `module_loads` + `orca_dir` → `orca` not on PATH; per-image SCFs silently produce nothing.
- After re-connecting to Expanse, the session_id changes — re-discover via `/api/hpc/connections` and update `default_session_id` + `cluster_configs` key.

## Canonical NEB-TS node params (what the engine actually reads)

| Parameter | Default | Description |
|---|---|---|
| `method` | r2SCAN-3c | DFT functional |
| `basis` | def2-SVP | Basis set (omit for composite methods) |
| `charge` / `multiplicity` | 0 / 1 | |
| `dispersion` | (none) | `D4` \| `D3BJ` \| `D3` — **use this field, NOT `extra_keywords`** |
| `grid` | DefGrid2 | `DefGrid1/2/3` |
| `nimages` | 8 | Number of interpolated images |
| `ts_opt` | true | Switch to CI-NEB after convergence |
| `neb_cycles` | 100 | NEB iteration cap |
| `interpolation` | "IDPP" | Initial-path interpolation method |
| `num_cores` / `max_core_mb` | 8 / 4000 | |

> ⚠️ `extra_keywords`, `extra_blocks`, `neb_images`, `neb_convergence` are NOT read by the engine — they're phantom params from earlier skill versions. Use the names above. There is no `neb_convergence` knob currently exposed.

### About OPI input builders

OPI (`pip install orca-pi`) ships a typed `BlockNeb` builder. **However, the catgo backend's `orca_neb_ts` node already emits its own `%neb` block from node params (`neb_images`, `neb_convergence`, etc.).** Pasting an OPI-built `%neb` block via `extra_blocks` would produce **two `%neb` blocks** in the same `.inp`, which is undefined behavior.

For this skill, **stick with node params** for `%neb` content and use `extra_blocks` only for `%output`. The OPI parsing wins (per-image energy curve, TS imaginary-mode check) still apply. If you need a knob `BlockNeb` exposes that the node params don't (`interpolation`, `springconst`, `ts_inputhess`, `zoom_*`, etc.), open that as a node-def gap rather than dual-emitting blocks.

### Image count guidelines

| System size | Recommended images |
|---|---|
| Small molecule (<15 atoms) | 6-8 |
| Medium molecule (15-50 atoms) | 8-12 |
| Large molecule (>50 atoms) | 12-16 |

More images = smoother path but higher cost (each image is a full DFT calc).

## Common Reaction Types

### SN2 reaction
- Charge: -1 (incoming nucleophile)
- Check that leaving group bond elongates along path

### Bond dissociation / formation
- Usually neutral, singlet
- Consider if radical pathway needs multiplicity: 3 (triplet)

### Proton transfer
- Include dispersion: `dispersion: "D3BJ"` (or `"D4"` for newer Grimme correction)
- Solvent: CPCM is currently a node-def gap on neb_ts (no first-class field, and `extra_keywords` is unread). Workaround: gas-phase NEB-TS, then refine TS energy with a CPCM single-point.

## Troubleshooting

### NEB does not converge
- Increase `neb_images` (more interpolation points)
- Use a better starting path (optimize reactant and product first)
- Try `neb_convergence: "loose"` for initial run, then tighten

### Wrong TS found
- Check the imaginary frequency mode -- does it correspond to the expected
  bond breaking/forming?
- Try different initial interpolation (reorder atoms so they correspond)

### Too expensive
- Screen with `HF-3c` or `orca_method: "PBE", orca_basis: "def2-SVP"` first
- Refine with better method only on the TS geometry (single-point)

## Important Notes

- Reactant and product MUST have the same atoms in the same order
- Both structures should be pre-optimized at the same level of theory
- ORCA NEB-TS automatically switches to CI-NEB after initial convergence
- The barrier height is the energy difference between the TS and the reactant
