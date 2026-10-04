---
name: pyiron
description: Integrated development environment (IDE) for computational materials science. Use when developing complex simulation protocols, managing high-throughput calculations, or building interactive materials science workflows.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

pyiron is an integrated development environment for computational materials science combining atomic structure objects, simulation codes, feedback loops, data management, visualization, and job management in a Jupyter-based platform. Developed at Max Planck Institut für Eisenforschung and ICAMS.

# Installation

## Conda (Recommended)
```bash
conda install -c conda-forge pyiron
```

## pip
```bash
pip install pyiron
```

# Quick Start

## Initialize Project

```python
from pyiron import Project

pr = Project("my_project")
pr.create_job_class()
```

## LAMMPS Molecular Dynamics

```python
from pyiron import Project

pr = Project("md_simulation")
job = pr.create_job("Lammps", "my_md_job")
job.structure = pr.create_structure("Al", "fcc", 4.05)
job.calc_md(temperature=300, n_steps=1000)
job.run()
```

## VASP DFT Calculation

```python
from pyiron import Project

pr = Project("dft_calc")
job = pr.create_job("Vasp", "my_vasp_job")
job.structure = pr.create_structure("Cu", "fcc", 3.6)
job.calc_static()
job.run()
```

# When to Use This Skill

- Building complex multi-step simulation workflows
- Managing large-scale high-throughput calculations
- Running DFT, MD, or atomistic simulations interactively
- Developing ab initio thermodynamics protocols
- Performing equation of state calculations
- Managing job databases with SQL/HDF5 storage
- Creating reusable simulation templates
- Running LAMMPS, VASP, GPAW, or Quantum ESPRESSO jobs
- Interactive materials science in Jupyter notebooks
- Prototyping and debugging simulation protocols

# Key Features

## Structure Handling

```python
structure = pr.create_structure("Al", "fcc", 4.0)
structure.plot3d()  # NGLview 3D visualization
```

## Job Management

- Object-oriented job creation
- SQL database for job tracking
- HDF5 hierarchical data storage
- Job restart and re-run capabilities
- Automatic job status tracking

## Supported Codes

| Code | Type | Job Class |
|------|------|-----------|
| LAMMPS | Molecular dynamics | `Lammps` |
| VASP | DFT | `Vasp` |
| GPAW | DFT | `GPAW` |
| Quantum ESPRESSO | DFT | `Espresso` |
| SPHInX | DFT | `Sphinx` |
| Murnaghan | Equation of state | `Murnaghan` |
| Phonopy | Phonons | `Phonopy` |

## Workflow Patterns

```python
# Master-worker pattern for high-throughput
for i in range(10):
    job = pr.create_job("Lammps", f"job_{i}")
    job.run()
```

# Workflow Examples

## Ab Initio Thermodynamics
```python
pr = Project("thermo")
job = pr.create_job("Vasp", "bulk")
job.run()

surface = pr.create_job("Vasp", "surface")
surface.structure = bulk.structure.create_surface()
surface.run()
```

## Equation of State
```python
from pyiron import Project

pr = Project("eos")
job = pr.create_job("Murnaghan", "eos_job")
job.structure = pr.create_structure("Al", "fcc", 4.05)
job.run()
job.plot()  # Display E(V) curve
```

## High-Throughput Screening
```python
from pyiron import Project

pr = Project("screening")
structures = ["Al", "Cu", "Ni", "Fe"]
for elem in structures:
    job = pr.create_job("Vasp", elem)
    job.structure = pr.create_structure(elem, "fcc")
    job.run()
```

## Phonon Calculation
```python
from pyiron import Project

pr = Project("phonons")
job = pr.create_job("Phonopy", "phonon_job")
job.structure = pr.create_structure("Al", "fcc", 4.05)
job.run()
job.plot_phonons()
```

## Molecular Dynamics with Analysis
```python
from pyiron import Project

pr = Project("md_analysis")
job = pr.create_job("Lammps", "md_job")
job.structure = pr.create_structure("Cu", "fcc", 3.6)
job.calc_md(temperature=300, n_steps=10000, save_rate=100)
job.run()

# Analyze results
job.output.mean_squared_displacement()
job.output.energy_pot.plot()
```

## Job Restart and Reuse
```python
from pyiron import Project

pr = Project("restart_demo")
job = pr.create_job("Lammps", "reusable_job")
job.structure = pr.create_structure("Al", "fcc", 4.05)
job.run()

# Later: reload job
reloaded = pr.load("reusable_job")
print(reloaded.output.energy_pot)

# Create similar job from existing
new_job = pr.create_job("Lammps", "new_job")
new_job.input = reloaded.input
new_job.run()
```

## Database Queries
```python
from pyiron import Project

pr = Project("database_demo")
# List all jobs
pr.list_jobs()

# Filter jobs by status
pr.job_table(status="finished")

# Query specific properties
pr.job_table(filter={"hamilton": "Vasp"})
```

# Best Practices

- Use `Project` to organize calculations hierarchically
- Name jobs descriptively for easy retrieval
- Use `job.run()` for execution, `job.status` for monitoring
- Store results in HDF5 format for persistence
- Use `pr.pack()` and `pr.unpack()` for archiving projects
- Enable `job.server.cores` for parallel execution
- Use `pr.create_group()` for logical job grouping
- Check `job.status` before accessing outputs
- Use `job.interactive_open()` for large output datasets

```python
# Project organization
pr = Project("study")
pr_group = pr.create_group("high_temp")
pr_group.create_job("Lammps", "md_500K")
pr_group.create_job("Lammps", "md_600K")

# Archive project
pr.pack("study_archive.h5")
```

# Troubleshooting

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| VASP executable not found | PATH not configured | Set `VASP_COMMAND` or configure `.pyiron` |
| Job hangs | Queue system issue | Check `job.status` and queue manager |
| HDF5 file errors | Corrupted storage | Use `pr.job_table()` to identify issues |
| Memory issues | Large structures | Use chunked processing |
| Import errors | Missing optional dependency | Install with extras: `pip install pyiron[lammps]` |

## Configuration

Create `~/.pyiron` configuration:
```bash
# .pyiron file
[DEFAULT]
PROJECT_PATHS = ~/pyiron_projects

[VASP]
VASP_COMMAND = mpirun -np 4 vasp_std

[LAMMPS]
LAMMPS_COMMAND = lmp_mpi
```

## Debugging Jobs

```python
# Check job status
print(job.status)  # initialized, running, finished, aborted

# View job log
job.view_log()

# Check for errors
if job.status == "aborted":
    print(job.error_message)

# Access raw output
job["output/energy_tot"]
```

# Visualization

```python
structure.plot3d()              # 3D structure view
job.output.plot_energy()        # Energy plots
job.plot()                      # Job-specific plots
job.animate_structures()        # Animation for MD
```

# Metadata

| Property | Value |
|----------|-------|
| License | BSD-3-Clause |
| Language | Python |
| Developers | Max Planck Institute, ICAMS |
| Dependencies | ASE, numpy, pandas, h5py |
| Storage | SQL + HDF5 |

# Resources

- GitHub: https://github.com/pyiron/pyiron
- Homepage: https://pyiron.org
- Documentation: https://pyiron.readthedocs.io
- Paper: Janssen et al., Comput. Mater. Sci. 163, 24-36 (2019)