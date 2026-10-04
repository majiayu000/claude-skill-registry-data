---
name: atb
description: Use this skill when accessing the Automated Topology Builder for molecular force field parameters, topology files, or molecular simulation data.
metadata:
    skill-author: MindSpore Science Team
---
## Overview
Automated Topology Builder (ATB) and Repository provides molecular topology files and force field parameters for biomolecular simulations. Developed at University of Queensland, it uses the GROMOS 54A7 force field and provides ready-to-use simulation inputs.

## When to Use This Skill

Use this skill when you need to:

1. **Get GROMACS topology files** - Ready-to-use .top and .itp files for MD simulations
2. **Generate force field parameters** - GROMOS 54A7 parameters for new molecules
3. **Access optimized geometries** - 3D structures with energy-minimized coordinates
4. **Build simulation systems** - Pre-solvated and membrane-inserted systems
5. **Obtain partial charges** - Quantum-derived atomic charges for simulations
6. **Find molecular topologies** - Search by name, SMILES, or structure drawing
7. **Set up biomolecular simulations** - Ligands, drug molecules, small compounds
8. **Compare with experimental data** - Validation against known molecular properties

## Data Types
- Molecular topologies and force field parameters (GROMOS 54A7)
- 3D molecular structures (optimized geometries)
- Partial atomic charges
- GROMACS topology files (.top, .itp)
- Solvated systems and membrane inserts

## Key Properties
- Molecular weight, formula, charge
- Bonded and non-bonded parameters
- Energy minimization results
- RMSD from initial geometry
- Solvation free energy estimates

## Access Methods

### Web Interface

- **Search**: Search by molecule name, SMILES, or IUPAC name
- **Draw**: Use JSME molecular editor to draw structure
- **Upload**: Upload MOL2 or PDB file for topology generation

### API Access

```python
import requests

BASE_URL = "https://atb.uq.edu.au/api/v1"

# Search for molecules
response = requests.get(f"{BASE_URL}/molecules", params={"name": "paracetamol"})
data = response.json()

for mol in data.get('results', [])[:5]:
    print(f"Molecule ID: {mol['molid']}")
    print(f"Name: {mol['name']}")
    print(f"Formula: {mol['formula']}")
```

### Download Topology Files

```python
import requests

def download_topology(molid, output_dir="atb_files"):
    """Download GROMACS topology files from ATB"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Download topology
    url = f"https://atb.uq.edu.au/molecule/{molid}/topology"
    response = requests.get(url)

    if response.status_code == 200:
        filepath = os.path.join(output_dir, f"{molid}.top")
        with open(filepath, "w") as f:
            f.write(response.text)
        return filepath
    return None

# Usage
topology_file = download_topology(12345)
```

### Example Queries

```python
# Web interface queries
# 1. Search: "acetaminophen" -> Download topology files
# 2. SMILES: "CC(=O)NC1=CC=C(O)C=C1" -> Generate topology
# 3. Draw: JSME editor -> Submit for parameterization

# API queries
import requests

# Search by SMILES
smiles = "CCO"  # ethanol
response = requests.get(f"https://atb.uq.edu.au/api/v1/molecules", params={"smiles": smiles})
data = response.json()

if data.get('results'):
    mol = data['results'][0]
    print(f"Molecule: {mol['name']}")
    print(f"Topology available: {mol.get('topology_available', False)}")
```

### Quality Levels

ATB provides different quality levels for topologies:

| Level | Description | Use Case |
|-------|-------------|----------|
| **Level 0** | Basic topology | Quick screening |
| **Level 1** | Optimized geometry | Standard simulations |
| **Level 2a** | Full charges, partial validation | Production runs |
| **Level 2b** | Full validation against experiment | High-accuracy needs |

```python
# Request specific quality level
response = requests.get(f"https://atb.uq.edu.au/api/v1/molecules/{molid}", params={"level": "2a"})
```

## Best Practices

### Topology Selection
- **Use Level 2a or 2b** for production simulations
- **Validate charges** against quantum calculations for critical molecules
- **Check atom types** match your simulation needs
- **Compare geometry** with experimental structures

### Integration with GROMACS
```python
# After downloading topology
# 1. Include in GROMACS topology file
# 2. Add to system topology with #include statement
# 3. Verify atom naming consistency

# Example GROMACS usage:
# gmx grompp -f ions.mdp -c system.gro -p topol.top -o ions.tpr
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Molecule not found` | Try alternative names or draw structure |
| `Topology incomplete` | Request higher quality level |
| `Charge mismatch` | Validate with quantum calculations |
| `Atom type error` | Check GROMOS 54A7 compatibility |
| `API timeout` | Large molecules take longer to process |

## Resources
- Website: https://atb.uq.edu.au
- Documentation: https://atb.uq.edu.au/docs
- Paper: https://doi.org/10.1021/ci100438p
- GROMOS Force Field: https://gromos.org