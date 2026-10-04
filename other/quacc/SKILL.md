---
name: quacc
description: Python platform for high-throughput computational materials science and quantum chemistry. Use when automating DFT workflows, running database-driven calculations, or dispatching jobs across computing environments.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

quacc is a flexible platform for computational materials science and quantum chemistry built for the automation era. Provides pre-made workflows dispatchable locally, on HPC, cloud, or hybrid environments. Maintained by the Rosen Research Group at Princeton University.

# Installation

```bash
pip install quacc
quacc set WORKFLOW_ENGINE None  # For local execution
```

For workflow engines (choose one):
```bash
pip install quacc[parsl]    # Parsl executor
pip install quacc[dask]     # Dask executor
pip install quacc[prefect]  # Prefect executor
pip install quacc[covalent] # Covalent executor
```

# Quick Start

## Simple EMT Relaxation

```python
from ase.build import bulk
from quacc.recipes.emt.core import relax_job

atoms = bulk("Cu")
result = relax_job(atoms)
print(result["energy"])
```

## Mixed-Code Workflow

```python
from ase.build import bulk
from quacc.recipes.emt.core import relax_job
from quacc.recipes.tblite.core import static_job

atoms = bulk("Cu")
relaxed = relax_job(atoms)
result = static_job(relaxed["atoms"], method="GFN2-xTB")
```

## VASP Relaxation

```python
from ase.build import bulk
from quacc.recipes.vasp.core import relax_job

atoms = bulk("Cu")
result = relax_job(atoms)
```

# When to Use This Skill

- Automating DFT calculations (VASP, Quantum ESPRESSO, GPAW)
- Running high-throughput materials screening
- Building multi-step computational workflows
- Dispatching calculations to HPC clusters or cloud
- Combining different quantum chemistry codes in one workflow
- Computing phonons, elastic constants, or defect properties
- Setting up automated relaxation and static calculations
- Running machine learning potential calculations
- Performing molecular dynamics simulations

# Key Features

## Recipe Categories

| Recipe | Description | Key Jobs |
|--------|-------------|----------|
| emt | EMT calculator (testing/fast) | `relax_job`, `static_job` |
| vasp | VASP DFT calculations | `relax_job`, `static_job`, `mp_prerelax_job` |
| tblite | GFN-xTB semi-empirical | `relax_job`, `static_job`, `freq_job` |
| espresso | Quantum ESPRESSO | `relax_job`, `static_job`, `bands_job` |
| gaussian | Gaussian quantum chemistry | `relax_job`, `static_job`, `freq_job` |
| orca | ORCA quantum chemistry | `relax_job`, `static_job`, `freq_job` |
| psi4 | Psi4 quantum chemistry | `relax_job`, `static_job` |
| phonons | Phonon calculations | `phonon_job` |
| defects | Defect calculations | Various defect workflows |
| elastic | Elastic property calculations | `elastic_job` |
| mlp | Machine learning potentials | `relax_job`, `md_job` |

## Job Functions

- `relax_job`: Structure relaxation
- `static_job`: Single-point energy calculation
- `freq_job`: Frequency calculation
- `phonon_job`: Phonon spectrum
- `md_job`: Molecular dynamics

# Workflow Engines

Unified interface to multiple executors:
- Parsl, Dask, Prefect, Covalent

```python
from quacc import flow, job

@job
def my_calc(atoms):
    return relax_job(atoms)

@flow
def my_workflow(atoms):
    result1 = my_calc(atoms)
    return static_job(result1["atoms"])
```

# Workflow Examples

## High-Throughput Screening
```python
from quacc.recipes.emt.core import relax_job
from ase.build import bulk

structures = [bulk("Cu"), bulk("Al"), bulk("Ni")]
results = [relax_job(s) for s in structures]
```

## Multi-Step Workflow with Flow
```python
from quacc import flow, job
from quacc.recipes.emt.core import relax_job, static_job
from ase.build import bulk

@job
def relax_and_analyze(atoms):
    result = relax_job(atoms)
    return result

@flow
def screening_workflow(elements):
    results = []
    for elem in elements:
        atoms = bulk(elem)
        relaxed = relax_and_analyze(atoms)
        static = static_job(relaxed["atoms"])
        results.append(static)
    return results

# Run workflow
results = screening_workflow(["Cu", "Al", "Ni"])
```

## VASP with Custodian Error Handling
```python
from ase.build import bulk
from quacc.recipes.vasp.core import relax_job

atoms = bulk("Cu")
result = relax_job(atoms)  # Automatically uses custodian for error handling
```

## Custom Parameters
```python
result = relax_job(atoms,
                   relax_cell=True,
                   opt_params={"fmax": 1e-3})
```

## Phonon Calculation
```python
from ase.build import bulk
from quacc.recipes.phonons.core import phonon_job

atoms = bulk("Cu")
result = phonon_job(atoms)
```

## Defect Calculations
```python
from quacc.recipes.defects.core import defect_relax_job
from ase.build import bulk

base_structure = bulk("Cu")
# Create vacancy and relax
result = defect_relax_job(base_structure)
```

# Best Practices

- Start with `WORKFLOW_ENGINE None` for local testing
- Use EMT recipes for workflow development and testing
- Set appropriate `fmax` for convergence criteria
- Use `quacc set` commands to configure settings
- Store results in a database for large-scale runs
- Use `@job` decorator for parallel execution
- Use `@flow` decorator for dependent job chains
- Set `quacc.set <KEY> <VALUE>` for configuration

```python
# Configuration example
import os
os.environ["QUACC_WORKFLOW_ENGINE"] = "prefect"

# Or use CLI
# quacc set WORKFLOW_ENGINE prefect
# quacc set RESULTS_DIR ./results
```

# Troubleshooting

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Import errors | Missing optional dependency | Install with extras: `pip install quacc[vasp]` |
| VASP not found | VASP not in PATH | Set `QUACC_VASP_PARALLEL_CMD` |
| Workflow not running | Engine not configured | Run `quacc set WORKFLOW_ENGINE <engine>` |
| Memory issues | Large structures | Use chunked processing |
| Timeout errors | Long calculations | Increase job timeout settings |

## Configuration Tips

```python
# Set environment variables
import os
os.environ["QUACC_VASP_PARALLEL_CMD"] = "mpirun -np 4 vasp_std"
os.environ["QUACC_RESULTS_DIR"] = "./calc_results"

# Or use settings file
# ~/.quacc.yaml
# VASP_PARALLEL_CMD: mpirun -np 4 vasp_std
# RESULTS_DIR: ./calc_results
```

# Metadata

| Property | Value |
|----------|-------|
| License | BSD-3-Clause |
| Language | Python 3.9+ |
| Maintainer | Rosen Research Group, Princeton |
| Dependencies | ASE, pymatgen, custodian (optional) |

# Resources

- GitHub: https://github.com/Quantum-Accelerators/quacc
- Documentation: https://quantum-accelerators.github.io/quacc
- Citation: Rosen et al. (2023)