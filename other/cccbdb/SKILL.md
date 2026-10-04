---
name: cccbdb
description: Use this skill when accessing CCCBDB for computational chemistry benchmarks, spectroscopic data, or validating quantum chemistry calculations.
metadata:
    skill-author: MindSpore Science Team
---
## Overview
Computational Chemistry Comparison and Benchmark Database (CCCBDB) from NIST provides experimental and computed thermochemical and spectroscopic data for benchmarking quantum chemistry methods.

## When to Use This Skill

Use this skill when you need to:

1. **Benchmark quantum chemistry methods** - Compare computed vs experimental values
2. **Access thermochemical data** - Enthalpies, free energies, heat capacities
3. **Get vibrational frequencies** - IR and Raman frequencies
4. **Validate calculations** - Compare your DFT/ab initio results with reference
5. **Compare methods** - B3LYP vs CCSD(T) vs HF performance
6. **Access molecular geometries** - Experimental and computed structures

## Data Types
- Thermochemical data (enthalpies, free energies, heat capacities)
- Vibrational frequencies
- Molecular geometries (experimental and computed)
- Spectroscopic constants
- Computational method comparisons

## Key Properties
- Enthalpy of formation
- Ionization energy
- Electron affinity
- Vibrational frequencies (IR, Raman)
- Rotational constants

## Access Methods

- Web interface: Search by molecule name or formula
- Download: Text files, HTML tables
- No public API

## Example Queries

```
Web: Molecule "water" -> View all computed vs experimental data
Web: Compare methods "B3LYP vs CCSD(T)" for property "bond length"
Web: Property "vibrational frequencies" for "CH4"
```

## Resources
- Website: http://cccbdb.nist.gov