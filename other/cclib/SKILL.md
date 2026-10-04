---
name: cclib
description: Parser and interpreter for computational chemistry package outputs. Use when extracting molecular properties, orbital information, or calculation results from quantum chemistry software outputs.
metadata:
    skill-author: MindSpore Science Team
---

# Overview

cclib is a Python library for parsing output files from computational chemistry packages (Gaussian, ORCA, Q-Chem, ADF, GAMESS, NWChem, PSI4) into standardized Python data structures.

# Installation

```bash
pip install cclib
```

# Quick Start

```python
import cclib

# Parse a quantum chemistry output file
data = cclib.parser.parse("output.log")

# Access parsed properties
print(f"Number of atoms: {data.natom}")
print(f"Atomic numbers: {data.atomnos}")
print(f"Molecular orbitals: {data.moenergies}")
print(f"Vibrational frequencies: {data.vibfreqs}")

# Specific parser selection
from cclib.parser import Gaussian, ORCA, QChem
parser = Gaussian("gaussian.log")
data = parser.parse()
```

# Key Features

## Supported Packages
- Gaussian, ORCA, Q-Chem, ADF, GAMESS, NWChem, PSI4, Molpro, Jaguar

## Extracted Properties
- `atomnos`, `atomcoords`: Atomic numbers and coordinates
- `moenergies`, `mooccs`: Molecular orbital energies and occupations
- `vibfreqs`, `vibirs`: Vibrational frequencies and intensities
- `scfenergies`, `scfvalues`: SCF energies and convergence
- `atomcharges`: Atomic charge analyses (Mulliken, ESP, etc.)
- `dipole`, `moments`: Dipole and multipole moments
- `homos`: HOMO indices
- `etenergies`, `etsecs`: Electronic transition energies

## Algorithms Module
```python
from cclib.method import population, MPA
pop = population.MPA(data)
pop.calculate()
print(pop.aonames)  # Atomic orbital names
```

# Common Use Cases

## Automated Analysis Pipeline
```python
import cclib
from pathlib import Path

for log_file in Path("calculations/").glob("*.log"):
    data = cclib.parser.parse(str(log_file))
    energies = data.scfenergies[-1]  # Final SCF energy
```

## ML Dataset Creation
```python
import numpy as np

structures = []
for log_file in log_files:
    data = cclib.parser.parse(log_file)
    structures.append({
        "coords": data.atomcoords[-1],
        "energy": data.scfenergies[-1],
        "charges": data.atomcharges.get("mulliken")
    })
```

## Comparing Methods
```python
gaussian_data = cclib.parser.parse("gaussian.log")
orca_data = cclib.parser.parse("orca.log")
print(f"Gaussian energy: {gaussian_data.scfenergies[-1]}")
print(f"ORCA energy: {orca_data.scfenergies[-1]}")
```

# Bridge Interfaces
```python
# Convert to ASE Atoms
from cclib.bridge import ase
atoms = ase.makease(data)

# Convert to pymatgen Structure
from cclib.bridge import pymatgen
struct = pymatgen.makestructure(data)
```

# When to Use This Skill

- Parsing quantum chemistry output files from Gaussian, ORCA, Q-Chem, ADF, GAMESS, NWChem, PSI4
- Extracting molecular properties (energies, orbitals, frequencies) into Python data structures
- Building automated analysis pipelines for computational chemistry results
- Converting parsed data to ASE Atoms or pymatgen Structures for further analysis
- Creating ML-ready datasets from quantum chemistry calculations

# Best Practices

- Always specify the parser explicitly if auto-detection fails
- Use `data.scfenergies[-1]` for final SCF energy in converged calculations
- Validate parsed data with `data.metadata` for calculation parameters
- Leverage bridge interfaces for seamless integration with ASE/pymatgen
- Check convergence flags before using extracted energies

# Resources

- GitHub: https://github.com/cclib/cclib
- Docs: https://cclib.github.io
- PyPI: https://pypi.org/project/cclib