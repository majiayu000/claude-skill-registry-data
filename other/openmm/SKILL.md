---
name: openmm
description: Build, review, debug, and automate OpenMM molecular dynamics workflows. Use when working with OpenMM Python scripts, force field selection, integrator configuration, platform selection (CUDA/OpenCL/HIP/CPU), simulation types (equilibrium MD, enhanced sampling, minimization), trajectory output, or HPC execution and checkpoint/restart issues.
metadata:
  skill-author: MindSpore Science Team
---

# HPC OpenMM Skill

Treat OpenMM as a staged molecular dynamics workflow built around a valid Python script and explicit checkpoint/restart policy.

## Quick Start

### Typical Workflow
1. Write Python script (imports, topology, force field, system, integrator) —see [references/01-python-api-structure.md](references/01-python-api-structure.md)
2. Select force field and water model —see [references/02-force-fields.md](references/02-force-fields.md)
3. Choose simulation type (equilibrium MD, minimization, annealing, enhanced sampling) —see [references/03-simulation-types.md](references/03-simulation-types.md)
4. Configure integrator and thermostats —see [references/04-integrators.md](references/04-integrators.md)
5. Select platform (CUDA, OpenCL, HIP, CPU) —see [references/05-platforms.md](references/05-platforms.md)
6. Load input files (PDB, AMBER, GROMACS, CHARMM) —see [references/06-file-formats.md](references/06-file-formats.md)
7. Add solvent model if needed —see [references/07-solvent-models.md](references/07-solvent-models.md)
8. Configure checkpoint/restart for multi-step workflows —see [references/03-simulation-types.md](references/03-simulation-types.md)
9. Submit to HPC cluster —see [references/08-cluster-execution.md](references/08-cluster-execution.md)
10. Handle errors —see [references/error-recovery.md](references/error-recovery.md)

## Skill Map

```
User Requirements
├─ Script Authoring
│ ├─ Imports (openmm.app, openmm, openmm.unit) →01-python-api-structure.md
│ ├─ Topology loading (PDB, AMBER, GROMACS) →06-file-formats.md
│ ├─ Force field selection →02-force-fields.md
│ └─ System creation →01-python-api-structure.md
├─ Simulation Types
│ ├─ Energy minimization →03-simulation-types.md
│ ├─ Equilibrium MD →03-simulation-types.md
│ ├─ Simulated annealing →03-simulation-types.md
│ ├─ Enhanced sampling →03-simulation-types.md
│ └─ Custom forces/restraints →03-simulation-types.md
├─ Integrators & Thermostats
│ ├─ Langevin integrators →04-integrators.md
│ ├─ Verlet integrator →04-integrators.md
│ ├─ Nose-Hoover integrator →04-integrators.md
│ └─ Barostats (Monte Carlo) →04-integrators.md
├─ Platforms
│ ├─ CUDA platform →05-platforms.md
│ ├─ OpenCL platform →05-platforms.md
│ ├─ HIP platform →05-platforms.md
│ ├─ CPU platform →05-platforms.md
│ └─ Platform properties (precision, device index) →05-platforms.md
├─ Solvent Models
│ ├─ Explicit solvent (TIP3P, TIP4P, OPC) →07-solvent-models.md
│ └─ Implicit solvent (GBSA, GBn2) →07-solvent-models.md
├─ Trajectory & Output
│ ├─ DCDReporter, PDBReporter →01-python-api-structure.md
│ ├─ StateDataReporter →01-python-api-structure.md
│ └─ CheckpointReporter →03-simulation-types.md
└─ HPC Cluster Execution
   ├─ SLURM/PBS job scripts →08-cluster-execution.md
   ├─ Multi-GPU parallelization →08-cluster-execution.md
   └─ Checkpoint/restart →08-cluster-execution.md
```

## Reference Documents

| Document | Content |
|----------|---------|
| [references/01-python-api-structure.md](references/01-python-api-structure.md) | Python script anatomy: imports, topology loading, system creation, simulation setup, reporters |
| [references/02-force-fields.md](references/02-force-fields.md) | Amber19, Amber14, CHARMM36, AMOEBA force fields; water models; implicit solvent |
| [references/03-simulation-types.md](references/03-simulation-types.md) | Minimization, equilibrium MD, annealing, enhanced sampling, custom forces, checkpoint/restart |
| [references/04-integrators.md](references/04-integrators.md) | Langevin, Verlet, Nose-Hoover, Brownian integrators; thermostats; barostats |
| [references/05-platforms.md](references/05-platforms.md) | CUDA, OpenCL, HIP, CPU platforms; precision modes; device selection |
| [references/06-file-formats.md](references/06-file-formats.md) | PDB, AMBER (prmtop/inpcrd), GROMACS (gro/top), CHARMM (psf), Tinker |
| [references/07-solvent-models.md](references/07-solvent-models.md) | Explicit solvent models (TIP3P, TIP4P, OPC, SPC/E); implicit solvent (GBSA, GBn2) |
| [references/08-cluster-execution.md](references/08-cluster-execution.md) | SLURM scripts, GPU allocation, checkpoint/restart, job sizing |
| [references/error-recovery.md](references/error-recovery.md) | Input, platform, memory, convergence, trajectory errors; recovery workflow |

## Key Decision Points

| Question | Guide | Summary |
|----------|-------|---------|
| Minimization, MD, or enhanced sampling? | [03-simulation-types.md](references/03-simulation-types.md) | Minimize, equilibrate, or production MD |
| Which force field and water model? | [02-force-fields.md](references/02-force-fields.md) | Amber19, CHARMM36, AMOEBA with appropriate water |
| Which platform and precision? | [05-platforms.md](references/05-platforms.md) | CUDA/HIP for GPU, mixed/single/double precision |
| Implicit or explicit solvent? | [07-solvent-models.md](references/07-solvent-models.md) | PME for explicit, GBSA for implicit |
| Which integrator? | [04-integrators.md](references/04-integrators.md) | LangevinMiddle for NVT, Nose-Hoover for NPT |

## Guardrails

- Do not invent force field XML file names —consult [02-force-fields.md](references/02-force-fields.md)
- Do not mix incompatible force field and water model XML files —use matching pairs
- Do not run simulations without energy minimization first —see [03-simulation-types.md](references/03-simulation-types.md)
- Do not modify the System after creating the Simulation —forces added later have no effect
- Do not forget to set platform properties for GPU simulations —see [05-platforms.md](references/05-platforms.md)

## Outputs

Always report:

- simulation type (minimization, equilibrium MD, production)
- force field and water model selection
- platform and precision mode
- integrator type and parameters (temperature, friction, timestep)
- expected outputs (.dcd, .pdb, checkpoint files) and next stage

## Template Files

Template files in `assets/templates/` are ready-to-use starting scaffolds that can be copied and modified:

| Template | Type | Use Case | Reference |
|----------|------|---------|-----------|
| [assets/templates/simulate_pdb.py](assets/templates/simulate_pdb.py) | Python script | Equilibrium MD from PDB file | [01-python-api-structure.md](references/01-python-api-structure.md), [02-force-fields.md](references/02-force-fields.md) |
| [assets/templates/simulate_amber.py](assets/templates/simulate_amber.py) | Python script | Equilibrium MD from AMBER files | [06-file-formats.md](references/06-file-formats.md) |
| [assets/templates/simulate_gromacs.py](assets/templates/simulate_gromacs.py) | Python script | Equilibrium MD from GROMACS files | [06-file-formats.md](references/06-file-formats.md) |
| [assets/templates/openmm-slurm.sh](assets/templates/openmm-slurm.sh) | Batch script | SLURM submission for OpenMM | [08-cluster-execution.md](references/08-cluster-execution.md) |

## Error Recovery

Consult [references/error-recovery.md](references/error-recovery.md) for structured diagnosis of:

- Input file errors (missing atoms, topology mismatch)
- Platform initialization failures (GPU driver, CUDA version)
- Memory and resource errors
- Integration and convergence issues
- Trajectory and checkpoint errors
- Runtime errors (segmentation fault, timeout)