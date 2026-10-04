---
name: molssi-qca
description: Use this skill when accessing MolSSI Quantum Chemistry Archive for quantum chemistry calculations, benchmark datasets, or computational chemistry data.
metadata:
    skill-author: MindSpore Science Team
---
## Overview
MolSSI Quantum Chemistry Archive (QCArchive) is a comprehensive repository for quantum chemistry calculations and benchmark datasets. Developed by MolSSI, it provides standardized molecular calculations.

## When to Use This Skill

Use this skill when you need to:

1. **Access benchmark datasets** - S22, S66, and other standard benchmarks
2. **Query quantum chemistry calculations** - HF, DFT, MP2, CCSD(T) results
3. **Compare methods** - Performance across computational methods
4. **Get molecular geometries** - Optimized structures
5. **Access wavefunction data** - Full wavefunction information
6. **Use qcportal client** - Python API access

## Data Types
- Quantum chemistry calculations
- Benchmark datasets (S22, S66, etc.)
- Molecular geometries and energies
- Method comparison data
- Wavefunction and property data

## Key Properties
- Total energies (HF, DFT, MP2, CCSD(T))
- Optimized geometries
- Interaction energies
- Dipole moments
- HOMO-LUMO gaps

## Access Methods

- Web interface: Browse datasets and records
- API: QCArchive REST API
- Python: qcportal client library

## Example Queries

```python
from qcportal import PortalClient

client = PortalClient()
ds = client.get_dataset('S22')
records = ds.get_records(method='B3LYP')
```

## Resources
- Website: https://qcarchive.molssi.org