---
name: orca-freq
description: ORCA frequency calculation. Computes vibrational frequencies, IR intensities, zero-point energy, and thermochemistry at specified temperature/pressure.
---

# ORCA Frequency Calculation Skill

## When to Use

Use this skill when the user wants to:
- Compute vibrational frequencies of a molecule
- Get an IR spectrum
- Calculate zero-point energy (ZPE)
- Obtain thermochemical quantities (enthalpy, entropy, Gibbs free energy)
- Verify a transition state (exactly one imaginary frequency)
- Confirm a minimum (no imaginary frequencies)

## Prerequisites

The input structure MUST be optimized at the same level of theory used for the
frequency calculation. Running frequencies on an unoptimized structure will
produce meaningless imaginary frequencies.

## MCP Tool Examples — proven Expanse submission flow

> **Use `catgo_workflow` (graph-based), NOT `catgo_workflow_engine` (task-based).**
> The graph-based tool auto-captures the viewer structure on `create` and supports
> connecting opt→freq via explicit node edges. Task-based `add_task` doesn't attach
> the viewer structure → "No input structure provided". Param keys also differ:
> graph-based uses `method`/`basis`, task-based uses `orca_method`/`orca_basis`.

### 1. Confirm structure is loaded and find Expanse session_id

```json
catgo_view(action: "get_state")
```

```bash
curl -s http://localhost:8000/api/hpc/connections
```

Copy the `session_id` for `host: login.expanse.sdsc.edu`.

### 2. Create the workflow (auto-captures viewer structure)

```json
catgo_workflow(action: "create", name: "Water frequencies B3LYP")
```

This creates a `structure_input` node with the current viewer structure.
Note its node ID.

### 3. Add the freq node (or opt → freq chain)

**Standalone freq (when structure is already optimized at the same level):**

Inject `extra_blocks: "%output jsongbwfile True jsonpropfile True end"` so
ORCA emits the JSON files OPI parses.

```json
catgo_workflow(action: "batch", workflow_id: "<wf_id>", operations: [
  {"op": "add_node", "node_type": "freq", "label": "freq1",
   "params": {
     "software": "orca",
     "method": "B3LYP",
     "basis": "def2-SVP",
     "charge": 0,
     "multiplicity": 1,
     "extra_blocks": "%output jsongbwfile True jsonpropfile True end"
   }},
  {"op": "connect", "from_id": "<structure_input_id>", "to_id": "freq1",
   "from_handle": "structure", "to_handle": "structure"}
])
```

**Opt → Freq chain (recommended — consistent PES guaranteed):**

```json
catgo_workflow(action: "batch", workflow_id: "<wf_id>", operations: [
  {"op": "add_node", "node_type": "geo_opt", "label": "opt1",
   "params": {
     "software": "orca",
     "method": "B3LYP",
     "basis": "def2-TZVP",
     "opt_convergence": "TightOpt",
     "dispersion": "D3BJ",
     "charge": 0,
     "multiplicity": 1
   }},
  {"op": "add_node", "node_type": "freq", "label": "freq1",
   "params": {
     "software": "orca",
     "method": "B3LYP",
     "basis": "def2-TZVP",
     "dispersion": "D3BJ",
     "charge": 0,
     "multiplicity": 1
   }},
  {"op": "connect", "from_id": "<structure_input_id>", "to_id": "opt1",
   "from_handle": "structure", "to_handle": "structure"},
  {"op": "connect", "from_id": "opt1", "to_id": "freq1",
   "from_handle": "structure", "to_handle": "structure"}
])
```

The freq node consumes `opt1`'s optimized structure — no separate `depends_on`
needed; the edge defines the dependency.

### 4. Optional: append a Gibbs energy node

ORCA reports thermochemistry at 298.15 K / 1 atm by default. For other
conditions, chain a `gibbs_energy` analysis node:

```json
{"op": "add_node", "node_type": "gibbs_energy", "label": "gibbs1",
 "params": {"temperature": 373.15, "phase": "gas"}},
{"op": "connect", "from_id": "freq1", "to_id": "gibbs1",
 "from_handle": "frequencies", "to_handle": "frequencies"}
```

### 5. Run with the full HPC run_config

`run_config` MUST include `module_loads`, `orca_dir`, `account`, `partition`,
`walltime`, and the local-scratch SLURM template. Read
`server/templates/orca_generic.sh` and pass its contents as `default_template`.

```json
catgo_workflow(action: "run", workflow_id: "<wf_id>", run_config: {
  "execution_mode": "hpc",
  "default_session_id": "<expanse_session_id>",
  "base_work_dir": "/expanse/lustre/projects/sdp126/jyang25/ORCA/catgo",
  "default_job_params": {
    "nodes": 1, "ntasks": 4, "cpus_per_task": 1,
    "walltime": "00:30:00", "partition": "debug"
  },
  "cluster_configs": {
    "<expanse_session_id>": {
      "account": "sdp126",
      "partition": "debug",
      "module_loads": "module load cpu/0.17.3b\nmodule load gcc/10.2.0/npcyll4\nexport PATH=$HOME/openmpi-4.1.8/bin:$PATH\nexport LD_LIBRARY_PATH=$HOME/openmpi-4.1.8/lib:$LD_LIBRARY_PATH",
      "orca_dir": "/home/jyang25/orca_6_1_1_RRP8",
      "default_template": "<contents of server/templates/orca_generic.sh>",
      "default_job_params": {
        "nodes": 1, "ntasks": 4, "cpus_per_task": 1,
        "walltime": "00:30:00", "partition": "debug"
      }
    }
  }
})
```

For freq jobs longer than 30 min, bump `walltime` and switch `partition` to
`shared` or `compute`. The local-scratch template stages I/O to
`$TMPDIR/orca_$SLURM_JOB_ID` — necessary on Expanse (Lustre kills ORCA's
many-small-file I/O during numerical Hessians).

### 6. Monitor

```json
catgo_workflow(action: "status", workflow_id: "<wf_id>")
```

### 7. Pull results when COMPLETED

Pull the outputs into a local directory, including the OPI JSON files:

```bash
mkdir -p ./local_run
for f in ORCA.out ORCA.hess ORCA.property.json ORCA.json; do
  curl -s -X POST http://localhost:8000/api/hpc/files/read-content \
    -H 'Content-Type: application/json' \
    -d "{\"session_id\":\"<expanse_session_id>\",\"file_path\":\"<work_dir>/$f\"}" \
    > ./local_run/$f
done
```

Parsed result fields (when fetched via `catgo_workflow get_result` or the
results-enriched endpoint):
- `frequencies`: list of vibrational frequencies in cm⁻¹
- `intensities`: IR intensities in km/mol
- `is_imaginary`: boolean flags for each frequency
- `zpe`: zero-point energy in eV
- `thermochemistry`: dict with H, S, G at standard conditions

### 8. Parse with OPI

Replaces the hand-grep'd thermochemistry block. Requires `pip install orca-pi`.

```python
import sys
sys.path.insert(0, ".claude/skills")  # for the _shared helper
from _shared.orca_opi import parse_local

out = parse_local("./local_run")

# IR table — replaces frequencies + intensities + is_imaginary trio
ir = out.get_ir()  # dict[int, IrMode]
for mode_idx, mode in ir.items():
    print(mode_idx, mode.wavenumber, mode.intensity, mode.dipole)

# Thermochemistry (units: hartree, hartree/K)
thermo = {
    "zpe_eh":           out.get_zpe(),
    "inner_energy_eh":  out.get_inner_energy(),
    "enthalpy_eh":      out.get_enthalpy(),
    "entropy_eh_per_K": out.get_entropy(),
    "free_energy_eh":   out.get_free_energy(),
    "G_minus_Eel_eh":   out.get_free_energy_delta(),
}

# Imaginary check from the raw frequency list (negatives = imaginary)
freqs = out.results_properties.geometries[0].thermochemistry_energies[0].freq
n_imag = sum(1 for f in freqs if f < 0)
print(f"Imaginary modes: {n_imag}")
```

### Viewing the IR spectrum in the IDE

Use the shared helper to plot a stick spectrum and surface the PNG inline.

```python
from _shared.orca_opi import quick_plot_ir, show_png
png = quick_plot_ir(out)             # writes ./local_run/ir_spectrum.png
show_png(png, "IR spectrum")         # prints `![IR spectrum](local_run/ir_spectrum.png)`
```

After running this, **reply to the user with the markdown link** the script printed so Claude Code renders the figure inline in chat.

### Submission gotchas (real failures we hit)

- `catgo_workflow_engine.add_task` doesn't auto-attach the viewer structure → "No input structure provided".
- `partition=workq` (Shaheen default) is invalid on Expanse → use `debug` or `shared`.
- Missing `account=sdp126` → "Invalid account or account/partition combination".
- Missing `module_loads` + `orca_dir` → `orca` not on PATH; numerical Hessians silently produce nothing.
- After re-connecting to Expanse, the session_id changes — re-discover via `/api/hpc/connections` and update `default_session_id` + `cluster_configs` key.
- Engine doesn't regenerate `submit.sh` on `retry` alone — call `run` with the new `run_config` to get a fresh script.

## Interpreting Results

### Minima verification
- All frequencies should be real (positive)
- Small negative frequencies (<50 cm-1) are numerical noise, usually harmless
- Large imaginary frequencies indicate the structure is NOT a minimum

### Transition state verification
- Exactly ONE imaginary frequency (negative value)
- The imaginary mode should correspond to the expected reaction coordinate
- Use `catgo_view` to visualize the mode

### Thermochemistry output

ORCA prints a thermochemistry block with:

| Quantity | Symbol | Units |
|---|---|---|
| Zero-point energy | ZPE | eV (or kcal/mol) |
| Thermal energy | U | eV |
| Enthalpy | H = U + pV | eV |
| Entropy | S | eV/K |
| Gibbs free energy | G = H - TS | eV |

For catalysis, feed the DFT energy and frequencies into `gibbs_energy`:
- `phase: "adsorbed"` -- harmonic approximation (no translational/rotational)
- `phase: "gas"` -- ideal gas (includes translation, rotation, vibration)

## Frequency Scaling Factors

DFT frequencies are systematically overestimated. Common scaling factors:

| Method | Scaling factor |
|---|---|
| B3LYP/def2-SVP | 0.9813 |
| B3LYP/def2-TZVP | 0.9654 |
| PBE/def2-SVP | 0.9948 |
| HF-3c | 0.86 |

These are applied automatically by the `gibbs_energy` task when available.

## Common Mistakes

- Running freq on unoptimized geometry (will show spurious imaginary modes)
- Using different method/basis for opt and freq (inconsistent PES)
- Ignoring imaginary frequencies and proceeding with thermochemistry
- Not using TightOpt for the preceding optimization (loose opt can leave
  residual forces that appear as small imaginary frequencies)

## Canonical params (what the engine actually reads)

| Parameter | Default | Description |
|---|---|---|
| `method` | B3LYP | DFT functional |
| `basis` | def2-SVP | Basis set |
| `charge` / `multiplicity` | 0 / 1 | Charge and 2S+1 |
| `dispersion` | (none) | `D4` \| `D3BJ` \| `D3` \| `none`. **Use this field, NOT `extra_keywords`.** |
| `grid` | DefGrid2 | `DefGrid1/2/3` |
| `wavefunction`, `uno`, `uco` | — | Open-shell tweaks |
| `num_cores` / `max_core_mb` | 4 / 4000 | `%pal nprocs` / `%maxcore` |

> ⚠️ `extra_keywords` and `extra_blocks` are NOT read by the engine. Forcing `NumFreq`, adding `CPCM(Water)`, etc. via those keys silently does nothing. These are current node-def gaps for freq.

## ORCA-Specific Notes

- ORCA uses analytical frequencies when available, numerical otherwise
- For large molecules (>100 atoms), frequencies become very expensive
- ORCA output lists frequencies as negative values for imaginary modes
  (not "i" notation)
- Forcing `NumFreq` is currently a gap — analytical Hessians are used by default for whatever functional supports them
