---
name: qmflows
description: Python library for input generation and workflow automation in computational chemistry. Use when building automated DFT/quantum chemistry pipelines or managing complex simulation workflows.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

QMFlows is a Python library for constructing and efficiently executing computational chemistry workflows. It automates input generation, task dependency handling, and job management for quantum chemistry calculations, enabling use of massively parallel compute environments.

# Installation

```bash
# Create conda environment
conda create -n qmflows
conda activate qmflows

# Install dependencies
conda install -c conda-forge rdkit h5py

# Install qmflows
pip install qmflows
```

# Quick Start

```python
from qmflows import templates, run
from qmflows.packages import adf, dirac, dftb, orca, cp2k
from scm.plams import Molecule

# Define molecule
mol = Molecule("water.xyz")

# Create DFT calculation using CP2K
job = cp2k(
    templates.singlepoint,
    mol,
    job_name="water_sp"
)

# Run workflow
result = run(job)
print(result.energy)
```

# Key Capabilities

## Input Generation
- Automatic input file generation for quantum packages
- Supports CP2K, ORCA, ADF, DFTB, DIRAC
- Standardized interfaces across packages

## Workflow Management
- Task dependencies via Noodles framework
- Parallel execution support
- Efficient job scheduling on HPC clusters

## Failure Recovery
- Automatic job failure detection
- Recovery strategies and retry mechanisms
- Robust error handling

## Data Storage
- HDF5 (h5py) for numerical results
- Efficient data retrieval across runs
- Integration with molecular databases

# Common Use Cases

```python
from qmflows import templates, run
from qmflows.packages import cp2k
from scm.plams import Molecule

# Geometry optimization workflow
mol = Molecule("molecule.xyz")
opt_job = cp2k(
    templates.geometry,
    mol,
    job_name="optimization"
)

# Chain calculations
single_point = cp2k(
    templates.singlepoint,
    opt_job.molecule,
    job_name="sp_on_optimized"
)

results = run(single_point)

# High-throughput calculations
molecules = [Molecule(f"mol_{i}.xyz") for i in range(100)]
jobs = [cp2k(templates.singlepoint, m, job_name=f"job_{i}")
        for i, m in enumerate(molecules)]
results = run(jobs)
```

# Supported Packages

- CP2K: DFT and molecular dynamics
- ORCA: Quantum chemistry
- ADF: Amsterdam Density Functional
- DFTB: Density functional tight binding
- DIRAC: Relativistic calculations

# When to Use This Skill

- Building automated quantum chemistry workflows
- Generating input files for CP2K, ORCA, ADF, DFTB, DIRAC
- Running high-throughput calculations on HPC clusters
- Chaining geometry optimization with property calculations
- Managing task dependencies with Noodles framework

# Best Practices

- Use templates for standardized input generation
- Chain calculations by passing `job.molecule` between jobs
- Leverage Noodles for parallel execution on clusters
- Store results in HDF5 for efficient data retrieval
- Configure retry mechanisms for robust job execution

# Resources

- GitHub: https://github.com/SCM-NV/qmflows
- Documentation: https://qmflows.readthedocs.io
- Tutorial: https://github.com/SCM-NV/qmflows/tree/master/jupyterNotebooks