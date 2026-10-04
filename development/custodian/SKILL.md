---
name: custodian
description: Just-in-time job management framework for handling and correcting errors in computational jobs. Use when running long DFT or quantum chemistry calculations that need automatic error recovery.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

Custodian is a Python framework for managing computational jobs with automatic error detection, correction, and recovery. Essential for high-throughput DFT and quantum chemistry calculations where error rates become problematic at scale. Maintained by the Materials Project.

# Installation

```bash
pip install custodian
```

For VASP/NwChem/QChem plugins, also install pymatgen:
```bash
pip install pymatgen
```

# Quick Start

## Basic Usage

```python
from custodian.custodian import Custodian
from custodian.vasp.handlers import VaspErrorHandler, UnconvergedErrorHandler
from custodian.vasp.jobs import VaspJob

handlers = [VaspErrorHandler(), UnconvergedErrorHandler()]
jobs = VaspJob.double_relaxation_run(["mpirun", "-np", "4", "vasp_std"])
c = Custodian(handlers, jobs, max_errors=10)
c.run()
```

## Custom Job and Handler

```python
from custodian.custodian import Job, ErrorHandler

class MyJob(Job):
    def setup(self):
        pass
    def run(self):
        pass
    def postprocess(self):
        pass

class MyHandler(ErrorHandler):
    def check(self):
        return False
    def correct(self):
        return {"errors": "none", "actions": "none"}
```

# When to Use This Skill

- Running long VASP, Q-Chem, NWChem, CP2K, or FEFF calculations
- Implementing automatic error recovery for DFT jobs
- High-throughput computational materials science workflows
- Detecting and correcting SCF convergence failures
- Managing k-point mesh symmetry issues
- Handling aliasing and tetrahedron errors in VASP
- Running convergence studies (energy cutoff, k-points)
- Building custom job management workflows

# Key Features

## Error Handlers

### VASP Error Handlers

| Handler | Purpose | Common Corrections |
|---------|---------|-------------------|
| `VaspErrorHandler` | General VASP errors | Adjusts INCAR settings |
| `UnconvergedErrorHandler` | SCF convergence failures | Modifies ALGO, ISMEAR |
| `AliasingErrorHandler` | Aliasing errors | Adjusts ENCUT, PREC |
| `MeshSymmetryErrorHandler` | K-point mesh issues | Modifies KPOINTS |
| `DriftErrorHandler` | Large drift forces | Sets ISIF, EDIFFG |
| `FrozenJobErrorHandler` | Job appears frozen | Restarts with new params |
| `IncorrectSmearingHandler` | Incorrect smearing | Changes ISMEAR, SIGMA |
| `LrfCommutatorHandler` | LRF commutator issues | Adjusts LPEAD |
| `MaxForceErrorHandler` | Force issues | Adjusts POTIM |
| `NonConvergingErrorHandler` | Non-converging runs | Adjusts mixing params |
| `PositiveEnergyErrorHandler` | Positive energy errors | Adjusts ALGO, LREAL |
| `PotimErrorHandler` | POTIM issues | Adjusts ionic steps |
| `StdErrHandler` | Standard error handling | Logs and corrects |

### Q-Chem Error Handlers

| Handler | Purpose |
|---------|---------|
| `QChemErrorHandler` | General Q-Chem errors |
| `QChemNMRHandler` | NMR-specific errors |

### CP2K Error Handlers

| Handler | Purpose |
|---------|---------|
| `Cp2kErrorHandler` | General CP2K errors |

### Lobster Error Handlers

| Handler | Purpose |
|---------|---------|
| `LobsterErrorHandler` | Lobster calculation errors |

## Supported Codes

- VASP (comprehensive handlers)
- Q-Chem
- NWChem
- CP2K
- FEFF
- Lobster

## Job Types

- Single job execution
- Double relaxation runs
- Convergence studies (k-points, energy cutoff)

# Common Use Cases

## VASP Relaxation with Error Recovery
```python
from custodian.vasp.jobs import VaspJob
jobs = VaspJob.double_relaxation_run("vasp_std")
c = Custodian([VaspErrorHandler()], jobs)
c.run()
```

## YAML-Based Job Control
```bash
cstdn run job_spec.yaml
```

## Complete VASP Handler Setup
```python
from custodian.custodian import Custodian
from custodian.vasp.handlers import (
    VaspErrorHandler, UnconvergedErrorHandler,
    AliasingErrorHandler, MeshSymmetryErrorHandler
)
from custodian.vasp.jobs import VaspJob

handlers = [
    VaspErrorHandler(),
    UnconvergedErrorHandler(),
    AliasingErrorHandler(),
    MeshSymmetryErrorHandler()
]
jobs = [VaspJob("vasp_std")]
c = Custodian(handlers, jobs, max_errors_per_job=10)
c.run()
```

# Best Practices

- Always set `max_errors` to prevent infinite loops
- Use `VaspJob.double_relaxation_run()` for structure relaxations
- Place most likely handlers first for faster error detection
- Use `gzip_output=True` to save disk space
- Set `scratch_dir` for temporary files
- Enable `checkpoint` for job recovery after crashes
- Monitor `custodian.json` for error patterns
- Test handlers locally before production runs

```python
# Recommended VASP setup
c = Custodian(
    handlers=[VaspErrorHandler(), UnconvergedErrorHandler()],
    jobs=[VaspJob("vasp_std")],
    max_errors=10,
    gzipped_output=True,
    checkpoint=True,
    scratch_dir="/tmp/scratch"
)
```

# Troubleshooting

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Job keeps restarting | Handler not correcting | Check `custodian.json` for corrections |
| Max errors exceeded | Persistent error | Review error logs; adjust INCAR manually |
| Handler not triggering | Error pattern not matched | Create custom ErrorHandler subclass |
| Memory errors | Large scratch files | Set `scratch_dir` to partition with space |
| Job hangs | Frozen job not detected | Add `FrozenJobErrorHandler` with timeout |

## Debugging Workflow

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check custodian output
c = Custodian(handlers, jobs)
c.run()
print(c.run_log)  # Review job history
```

## Creating Custom Handlers

```python
from custodian.custodian import ErrorHandler

class MyCustomHandler(ErrorHandler):
    def __init__(self):
        self.is_monitor = False  # Run at job end only

    def check(self):
        # Return True if error detected
        with open("OUTCAR", "r") as f:
            return "MY_ERROR_STRING" in f.read()

    def correct(self):
        # Return dict with errors and actions taken
        return {"errors": ["my_error"], "actions": ["fixed"]}
```

# CLI Commands

```bash
cstdn run <yaml_file>    # Run job from YAML specification
custodian --help         # Show help
```

# Metadata

| Property | Value |
|----------|-------|
| License | MIT |
| Language | Python 3.8+ |
| Maintainer | Materials Project |
| Dependencies | Optional: pymatgen |

# Resources

- GitHub: https://github.com/materialsproject/custodian
- Documentation: https://materialsproject.github.io/custodian
- Citation: Ong et al., Comput. Mater. Sci. 68, 314-319 (2013)