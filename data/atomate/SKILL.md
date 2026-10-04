---
name: atomate
description: Materials science workflows framework built on FireWorks and pymatgen, developed at LBNL. Use when orchestrating complex DFT workflows, managing computational jobs, or building automated materials discovery pipelines.
metadata:
    skill-author: MindSpore Science Team
---

# When to Use This Skill

1. **High-throughput DFT calculations** - Running hundreds or thousands of VASP calculations with automated workflow management
2. **Materials property prediction** - Computing band structures, elastic tensors, dielectric properties, or phase diagrams automatically
3. **Building computational materials databases** - Creating searchable databases of calculated materials properties
4. **Custom VASP workflow development** - Creating multi-step calculations with dependencies (optimization → static → NSCF)
5. **Error recovery in long-running jobs** - Leveraging custodian integration for automatic error detection and correction
6. **HPC cluster job management** - Submitting and monitoring calculations across queue systems (SLURM, PBS)
7. **Reproducible computational workflows** - Ensuring calculations are documented and repeatable
8. **Integrating with Materials Project data** - Using pymatgen/MP integration for structure retrieval and comparison

# Best Practices

- **Use env_chk variables** (`>>vasp_cmd<<`, `>>db_file<<`) instead of hardcoding paths to ensure portability across computing environments
- **Apply powerups consistently** - Create a standard set of powerups (priority, tracking, fworker) in your workflow configuration
- **Set up proper directory structures** - Use dedicated directories for config files, logs, and calculation outputs
- **Configure scratch directories** - Set `scratch_dir` in fworker config for temporary calculation directories
- **Use reservation mode sparingly** - `qlaunch -r rapidfire` can create many queue jobs; monitor with `qlaunch -m` limits
- **Version your VASP pseudopotentials** - Organize POTCAR files by functional (PBE, LDA, PW91) for reproducibility
- **Test with single-firework workflows first** - Validate configuration with `wf_structure_optimization` before complex workflows
- **Monitor with web GUI** - Use `lpad webgui` for visual workflow status tracking on large projects
- **Back up MongoDB regularly** - Use `mongodump` to back up workflow and calculation databases

# Troubleshooting

| Problem | Solution |
|---------|----------|
| Cannot connect to LaunchPad | Verify MongoDB is running: `mongod --fork`. Check `my_launchpad.yaml` credentials and host. |
| Job fizzled immediately | Check `lpad get_fws -i <id> -d all` for error details. Verify VASP executable path and pseudopotential directory. |
| VASP input files not generated | Ensure `PMG_VASP_PSP_DIR` is set in `~/.pmgrc.yaml`. Check INCAR/KPOINTS settings in input set. |
| Workflows stuck in WAITING | Parent Firework may have failed. Run `lpad detect_fizzled` and check dependencies with `lpad get_wflows -d more`. |
| Queue jobs not submitting | Verify `my_qadapter.yaml` queue type matches your system (SLURM, PBS). Test with `qlaunch singleshot`. |
| Results not in database | Check `db.json` connection. Verify `db_file` is passed to workflow via `env_chk`. |
| Memory errors in large calculations | Increase job memory in qadapter. Use `add_modify_incar` to reduce KPOINTS or use gamma-only for large cells. |
| Duplicate calculations running | Use workflow namespacing or check for duplicate structures before adding workflows. |

# Overview

Atomate is a Python framework for designing and executing materials science workflows, particularly for density functional theory (DFT) calculations. It combines FireWorks for workflow management, pymatgen for materials analysis, and custodian for error handling.

# Installation

## Prerequisites

1. **MongoDB database** - for storing workflows and calculation results
2. **VASP executable** - with valid license and access
3. **Python 3.6+** - virtual environment recommended

## Install Atomate

```bash
pip install atomate
```

## Directory Structure

```bash
mkdir -p atomate/config atomate/logs
```

## FireWorks Configuration Files

Create these files in `atomate/config/`:

### db.json (Calculation Results Database)

```json
{
    "host": "mongodb_hostname",
    "port": 27017,
    "database": "atomate_db",
    "collection": "tasks",
    "admin_user": "admin_user",
    "admin_password": "admin_password",
    "readonly_user": "readonly_user",
    "readonly_password": "readonly_password",
    "aliases": {}
}
```

### my_launchpad.yaml (FireWorks Workflow Database)

```yaml
host: mongodb_hostname
port: 27017
name: atomate_db
username: admin_user
password: admin_password
ssl_ca_file: null
logdir: null
strm_lvl: INFO
user_indices: []
wf_user_indices: []
```

### my_fworker.yaml (Worker Configuration)

```yaml
name: my_worker
category: ''
query: '{}'
env:
    db_file: /path/to/atomate/config/db.json
    vasp_cmd: "mpirun -n 16 vasp_std"
    scratch_dir: null
```

### my_qadapter.yaml (Queue Adapter for SLURM)

```yaml
_fw_name: CommonAdapter
_fw_q_type: SLURM
rocket_launch: rlaunch -c /path/to/atomate/config rapidfire
nodes: 2
walltime: 24:00:00
queue: null
account: null
job_name: null
pre_rocket: null
post_rocket: null
logdir: /path/to/atomate/logs
```

### FW_config.yaml

```yaml
CONFIG_FILE_DIR: /path/to/atomate/config
```

## pymatgen Configuration

Create `~/.pmgrc.yaml`:

```yaml
PMG_VASP_PSP_DIR: /path/to/pseudopotentials
PMG_MAPI_KEY: your_materials_project_api_key
```

Pseudopotential directory structure:
```
pseudopotentials/
├── POT_GGA_PAW_PBE/
│   ├── POTCAR.Ac.gz
│   ├── POTCAR.Ag.gz
│   └── ...
├── POT_GGA_PAW_PW91/
└── POT_LDA_PAW/
```

## Environment Setup

```bash
export FW_CONFIG_FILE=/path/to/atomate/config/FW_config.yaml
source /path/to/atomate_env/bin/activate
```

## Verify Installation

```bash
lpad reset  # Initialize/reset database
lpad version  # Check FireWorks connection
```

# Built-in Workflows

## VASP Workflows (Presets)

| Workflow | Description |
|----------|-------------|
| `wf_bandstructure` | Band structure + DOS |
| `wf_structure_optimization` | Structure relaxation |
| `wf_elastic_constant` | Full elastic tensor |
| `wf_dielectric_constant` | Dielectric & piezoelectric |
| `wf_piezoelectric_constant` | Piezoelectric tensor |
| `wf_ferroelectric` | Ferroelectric switching |
| `wf_nmr` | NMR chemical shifts |
| `wf_neb` | Nudged elastic band |
| `wf_gibbs_free_energy` | Gibbs free energy via QHA |
| `wf_boltztrap` | BoltzTraP transport |
| `wf_raman` | Raman spectroscopy |

## FEFF Workflows

- XAS (X-ray absorption spectroscopy)
- EELS (electron energy loss spectroscopy)
- ELNES spectra

# Quick Start Examples

## Band Structure Workflow

```python
from pymatgen.core import Structure
from fireworks import LaunchPad
from atomate.vasp.workflows.presets.core import wf_bandstructure

struct = Structure.from_file('POSCAR')
wf = wf_bandstructure(struct)

lpad = LaunchPad.auto_load()
lpad.add_wf(wf)
```

## Structure Optimization

```python
from pymatgen.core import Structure
from fireworks import LaunchPad
from atomate.vasp.workflows.presets.core import wf_structure_optimization

struct = Structure.from_file('POSCAR')
wf = wf_structure_optimization(struct)

lpad = LaunchPad.auto_load()
lpad.add_wf(wf)
```

## Elastic Tensor Workflow

```python
from pymatgen.core import Structure
from atomate.vasp.workflows.presets.core import wf_elastic_constant

struct = Structure.from_file('POSCAR')
wf = wf_elastic_constant(struct)
lpad = LaunchPad.auto_load()
lpad.add_wf(wf)
```

## Using Materials Project Structures

```python
from pymatgen.ext.matproj import MPRester
from atomate.vasp.workflows.presets.core import wf_bandstructure

with MPRester() as mpr:
    struct = mpr.get_structure_by_material_id('mp-149')  # Silicon

wf = wf_bandstructure(struct)
lpad = LaunchPad.auto_load()
lpad.add_wf(wf)
```

# Custom Workflow Creation

## Creating from Fireworks

```python
from fireworks import Firework, Workflow
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet
from atomate.vasp.fireworks.core import OptimizeFW, StaticFW, NonSCFFW

struct = Structure.from_file('POSCAR')

fws = [
    OptimizeFW(structure=struct, name="optimization"),
    StaticFW(structure=struct, parents=fws[0], name="static"),
    NonSCFFW(structure=struct, parents=fws[1], mode="line", name="nscf_line"),
    NonSCFFW(structure=struct, parents=fws[1], mode="uniform", name="nscf_uniform")
]

wf = Workflow(fws, name="custom_bandstructure")
```

## Gibbs Free Energy Workflow Example

```python
from pymatgen.analysis.elasticity.strain import Deformation
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet
from fireworks import Firework, Workflow
from atomate.vasp.fireworks.core import OptimizeFW, TransmuterFW
from atomate.vasp.firetasks.parse_outputs import GibbsFreeEnergyTask

def wf_gibbs_free_energy(structure, deformations, vasp_cmd="vasp", db_file=None):
    vis_relax = MPRelaxSet(structure, force_gamma=True)

    fws = [OptimizeFW(structure=structure, vasp_input_set=vis_relax,
                      vasp_cmd=vasp_cmd, db_file=db_file)]

    vis_static = MPStaticSet(structure, force_gamma=True,
                             user_incar_settings={"ISIF": 2})

    deformations = [Deformation(d) for d in deformations]
    for n, deformation in enumerate(deformations):
        fw = TransmuterFW(
            structure=structure,
            transformations=['DeformStructureTransformation'],
            transformation_params=[{"deformation": deformation.tolist()}],
            vasp_input_set=vis_static,
            parents=fws[0],
            vasp_cmd=vasp_cmd, db_file=db_file
        )
        fws.append(fw)

    fw_analysis = Firework(
        GibbsFreeEnergyTask(db_file=db_file),
        name="gibbs_analysis", parents=fws[1:]
    )
    fws.append(fw_analysis)

    wf = Workflow(fws)
    wf.name = f"{structure.composition.reduced_formula}:gibbs"
    return wf
```

# Powerups

Powerups modify workflows after creation:

```python
from atomate.vasp.powerups import (
    add_modify_incar,
    add_priority,
    add_namefile,
    add_trackers,
    set_fworker,
    modify_to_soc
)

wf = wf_bandstructure(struct)

# Modify INCAR settings
wf = add_modify_incar(wf, modify_incar_params={'incar_update': {'EDIFFG': -0.05}},
                      fw_name_constraint='optimization')

# Add priority to ensure workflows complete
wf = add_priority(wf, priority=100)

# Add tracking for monitoring running jobs
wf = add_trackers(wf)

# Set specific FireWorker
wf = set_fworker(wf, fworker_name="high_memory_worker")

# Enable spin-orbit coupling
wf = modify_to_soc(wf)
```

# VASP/DFT Setup Examples

## Custom Input Set (Different Functional)

```python
from pymatgen.io.vasp.sets import MPRelaxSet
from pymatgen.core import Structure

struct = Structure.from_file('POSCAR')
my_input_set = MPRelaxSet(struct, potcar_functional='LDA')
```

## Custom KPOINTS

```python
from pymatgen.io.vasp.sets import MPRelaxSet

struct = Structure.from_file('POSCAR')
my_input_set = MPRelaxSet(struct, force_gamma=True,
                          user_kpoints_settings={"grid_density": 7000})
```

## Custom INCAR via Input Set

```python
from pymatgen.io.vasp.sets import MPRelaxSet

struct = Structure.from_file('POSCAR')
my_input_set = MPRelaxSet(struct,
                          user_incar_settings={'ENCUT': 600, 'EDIFF': 1e-6})
```

## Custom POTCAR

```python
from pymatgen.io.vasp.sets import MPRelaxSet

struct = Structure.from_file('POSCAR')
my_input_set = MPRelaxSet(struct)
my_input_set.config_dict['POTCAR']['Mg'] = 'Mg'
```

# FireWorks Integration

## env_chk for Environment Variables

Use environment variables from FireWorker config:

```python
wf = wf_bandstructure(struct, vasp_cmd='>>vasp_cmd<<', db_file='>>db_file<<')
```

Supported env_chk variables:
- `>>vasp_cmd<<`
- `>>gamma_vasp_cmd<<`
- `>>db_file<<`
- `>>scratch_dir<<`

## PassCalcLocs for Directory Tracking

Passes calculation directories between Fireworks:

```python
from atomate.common.firetasks.glue_tasks import PassCalcLocs

fw = Firework([PassCalcLocs(name="optimization")])
```

# Running Workflows

## Submit to Queue

```bash
qlaunch singleshot      # Submit one job
qlaunch rapidfire -m 1  # Keep max 1 job in queue
qlaunch -r rapidfire    # Reservation mode (auto job names)
```

## Run Locally (No Queue)

```bash
rlaunch singleshot
rlaunch rapidfire
```

## Monitor Workflows

```bash
lpad get_wflows                     # List all workflows
lpad get_wflows -d more             # Detailed view
lpad get_wflows -s READY            # Filter by state
lpad detect_fizzled                 # Find failed jobs
lpad rerun_fws -i 1                 # Rerun Firework by ID
lpad defuse_fws -i 1                # Defuse (pause) Firework
```

## Query Results

```python
from atomate.vasp.database import VaspCalcDb
from pymatgen.electronic_structure.plotter import BSPlotter, DosPlotter

db = VaspCalcDb.from_db_file('/path/to/db.json')

# Get band structure
entry = db.collection.find_one({'task_label': 'nscf line', 'formula_pretty': 'MgO'})
bs = db.get_band_structure(entry['task_id'])

# Get DOS
entry = db.collection.find_one({'task_label': 'nscf uniform', 'formula_pretty': 'MgO'})
dos = db.get_dos(entry['task_id'])

print(f"Fermi energy: {dos.efermi} eV")
print(f"Bandgap: {dos.get_gap()} eV")

bs_plotter = BSPlotter(bs)
bs_plotter.get_plot()
```

# Common Use Cases

- Running large-scale DFT calculations on HPC clusters
- Building custom materials science workflows
- Computing phase diagrams and materials stability
- Automating band structure and DOS calculations
- Managing computational materials databases
- High-throughput materials screening

# Key Capabilities

## Workflow Management

Leverage FireWorks to manage complex, multi-step computational workflows with job queuing, failure recovery, and distributed execution across computing clusters.

## Built-in Workflows

Access pre-built workflows for common DFT tasks including structure optimization, band structure calculations, elastic tensor computation, and phase diagram construction.

## Error Handling

Integrated custodian framework provides automatic error detection and correction for common DFT calculation failures.

# Resources

- Documentation: https://hackingmaterials.github.io/atomate
- GitHub: https://github.com/hackingmaterials/atomate
- Forum: https://discuss.matsci.org/c/atomate
- Language: Python