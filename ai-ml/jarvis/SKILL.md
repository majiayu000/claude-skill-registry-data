---
name: jarvis
description: Use this skill when accessing JARVIS for computed materials properties, 2D materials data, or NIST materials datasets.
metadata:
    skill-author: MindSpore Science Team
---
## Overview
Joint Automated Repository for Various Integrated Simulations (JARVIS) is NIST's database of computed materials properties including 2D materials, bulk solids, and molecules. Established in 2017, it contains 80,000+ materials with 1 million+ properties.

## When to Use This Skill

Use this skill when you need to:

1. **Access 2D materials data** - Comprehensive 2D materials database with exfoliation energies
2. **Use free, open data** - No API key required, public domain data from NIST
3. **Query semiconductor properties** - Band gaps (mBJ), dielectric functions, effective masses
4. **Access ML-ready datasets** - Pre-formatted data for machine learning applications
5. **Find superconductor candidates** - Dedicated superconductor database
6. **Study solar cell materials** - Solar efficiency (SLME) calculations
7. **Get elastic properties** - Full elastic tensors and mechanical properties
8. **Use ALIGNN models** - Pre-trained graph neural network models for property prediction

## Data Types
- DFT and classical MD calculations
- 2D materials properties
- Elastic, electronic, optical properties
- Machine learning models and data
- Defect and surface calculations

## API Access

### Python API (jarvis-tools)

#### Installation
```bash
pip install jarvis-tools
```

#### Basic Setup
```python
from jarvis.db.figshare import data
from jarvis.db.jsonutils import loadjson

# No API key required - open access
```

### Query Examples

#### Get 3D Materials Database
```python
from jarvis.db.figshare import data

# Load 3D bulk materials database
dft_3d = data("dft_3d")

print(f"Total materials: {len(dft_3d)}")

# Access properties for a material
mat = dft_3d[0]
print(f"JARVIS ID: {mat['jid']}")
print(f"Formula: {mat['formula']}")
print(f"Formation energy: {mat['formation_energy_peratom']} eV/atom")
print(f"Band gap: {mat['gap mbj']} eV")
```

#### Get 2D Materials Database
```python
from jarvis.db.figshare import data

# Load 2D materials database
dft_2d = data("dft_2d")

print(f"Total 2D materials: {len(dft_2d)}")

for mat in dft_2d[:5]:
    print(f"{mat['formula']}: Eg = {mat.get('gap mbj', 'N/A')} eV")
```

#### Search by Formula
```python
from jarvis.db.figshare import data

dft_3d = data("dft_3d")

# Find specific formula
si_materials = [m for m in dft_3d if m['formula'] == 'Si']
for mat in si_materials:
    print(f"JID: {mat['jid']}, Eg: {mat['gap mbj']} eV")

# Or search by pattern
li_materials = [m for m in dft_3d if 'Li' in m['formula']]
print(f"Materials containing Li: {len(li_materials)}")
```

#### Get Crystal Structure
```python
from jarvis.core.atoms import Atoms

dft_3d = data("dft_3d")
mat = dft_3d[0]

# Convert to JARVIS Atoms object
atoms = Atoms.from_dict(mat['atoms'])

print(f"Formula: {atoms.composition.formula}")
print(f"Lattice: {atoms.lattice}")
print(f"Number of atoms: {len(atoms.elements)}")

# Export to other formats
poscar_str = atoms.to_poscar()
print(poscar_str[:200])
```

#### Get Electronic Properties
```python
from jarvis.db.figshare import data

dft_3d = data("dft_3d")

for mat in dft_3d[:5]:
    jid = mat['jid']
    gap = mat.get('gap mbj', 'N/A')
    eform = mat.get('formation_energy_peratom', 'N/A')

    print(f"{mat['formula']} ({jid}):")
    print(f"  Band gap: {gap} eV")
    print(f"  Formation energy: {eform} eV/atom")
```

#### Elastic Properties
```python
from jarvis.db.figshare import data

dft_3d = data("dft_3d")

# Get elastic properties
for mat in dft_3d[:5]:
    elastic_tensor = mat.get('elastic_tensor')
    if elastic_tensor:
        print(f"{mat['formula']}: Elastic tensor available")
```

#### Download Specific Property Data
```python
from jarvis.db.figshare import get_ff_id_from_jid, get_dft_data

# Get data for specific JARVIS ID
jid = "JVASP-1002"

# Access raw data
dft_3d = data("dft_3d")
mat = next((m for m in dft_3d if m['jid'] == jid), None)
if mat:
    print(mat.keys())
```

### Available Databases

| Database | Function Call | Description | Size |
|----------|---------------|-------------|------|
| dft_3d | `data("dft_3d")` | 3D bulk materials | 77,096 |
| dft_2d | `data("dft_2d")` | 2D materials | ~1,000 |
| dft_3d_2 | `data("dft_3d_2")` | Additional 3D data (PBEsol) | 800,000+ |
| supercon_3d | `data("supercon_3d")` | Superconductor data | - |
| solar_3d | `data("solar_3d")` | Solar cell materials | 8,614 |
| dielectric_3d | `data("dielectric_3d")` | Dielectric materials | 15,860 |
| surface | `data("surface")` | Surface calculations | - |
| defect | `data("defect")` | Defect calculations | - |

### Available Properties

| Property | Key | Description |
|----------|-----|-------------|
| JARVIS ID | `jid` | Unique identifier (JVASP-XXXXX) |
| Formula | `formula` | Chemical formula |
| Formation Energy | `formation_energy_peratom` | eV/atom |
| Band Gap (mBJ) | `gap mbj` | Band gap from mBJ calculation |
| Band Gap (OPT) | `gap opt` | Optical gap |
| Total Energy | `total energy` | Total energy (eV) |
| Structure | `atoms` | Crystal structure dict |
| Elastic Tensor | `elastic_tensor` | 6x6 elastic tensor |
| Effective Mass | `effective_mass` | Carrier effective mass |
| Exfoliation Energy | `exfoliation_en` | 2D exfoliation energy (meV/atom) |
| Seebeck Coefficient | `seebeck` | Seebeck coefficient |
| Piezoelectric Tensor | `piezoelectric` | Piezoelectric tensor |

### REST API Access

```python
import requests

# Base URL for JARVIS API
BASE_URL = "https://jarvis.nist.gov/rest"

# Get list of databases
response = requests.get(f"{BASE_URL}/datasets/")
datasets = response.json()

# Query specific material
jid = "JVASP-1002"
response = requests.get(f"{BASE_URL}/material/{jid}/")
material = response.json()
```

### Bulk Data Download

```python
from jarvis.db.figshare import data
import pandas as pd

# Load and convert to DataFrame
dft_3d = data("dft_3d")

df = pd.DataFrame(dft_3d)
print(df.columns.tolist())

# Filter and save
stable_materials = df[df['formation_energy_peratom'] < 0.1]
stable_materials.to_csv("stable_materials.csv", index=False)
```

### Machine Learning Data

```python
from jarvis.db.figshare import data

# Get ML-ready data
dft_3d = data("dft_3d")

# Common ML features available
features = []
for mat in dft_3d[:5]:
    feature_dict = {
        'jid': mat['jid'],
        'formula': mat['formula'],
        'formation_energy': mat.get('formation_energy_peratom'),
        'band_gap': mat.get('gap mbj'),
        'gap_opt': mat.get('gap opt'),
    }
    features.append(feature_dict)

print(f"Extracted {len(features)} feature vectors")
```

## Best Practices

### API Usage
- **Use local caching**: Datasets are downloaded once and cached locally
- **Batch operations**: Load entire dataset then filter in memory
- **Use Figshare**: Direct download from NIST Figshare for large datasets
- **Check data availability**: Not all properties are available for all materials

### Data Quality
```python
# Filter for high-quality data
dft_3d = data("dft_3d")

# Remove entries with missing critical properties
valid_entries = [
    m for m in dft_3d
    if m.get('gap mbj') is not None
    and m.get('formation_energy_peratom') is not None
]

# Filter by formation energy for stable materials
stable = [m for m in valid_entries if m['formation_energy_peratom'] < 0]
```

### Using with pymatgen
```python
from jarvis.core.atoms import Atoms
from pymatgen.core import Structure

def jarvis_to_pymatgen(jarvis_atoms):
    """Convert JARVIS Atoms to pymatgen Structure"""
    poscar = jarvis_atoms.to_poscar()
    return Structure.from_str(poscar, fmt="poscar")

dft_3d = data("dft_3d")
jarvis_atoms = Atoms.from_dict(dft_3d[0]['atoms'])
pmg_struct = jarvis_to_pymatgen(jarvis_atoms)
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ConnectionError` on `data()` | Check internet connection, Figshare may be temporarily down |
| `KeyError` for properties | Use `.get('property', default)` to handle missing data |
| Slow first load | Dataset downloaded to cache (~500MB), subsequent loads are fast |
| `ImportError: jarvis` | `pip install jarvis-tools --upgrade` |
| Missing entries | Some entries lack certain properties; filter with `.get()` |

### Cache Location
```python
from jarvis.db.figshare import data
import os

# Default cache location
cache_dir = os.path.expanduser("~/.jarvis/")
print(f"JARVIS cache: {cache_dir}")
```

### Large Dataset Handling
```python
# Process large datasets in chunks
from jarvis.db.figshare import data

dft_3d = data("dft_3d")
chunk_size = 1000

for i in range(0, len(dft_3d), chunk_size):
    chunk = dft_3d[i:i + chunk_size]
    # Process chunk
    pass
```

## Resources
- Website: https://jarvis.nist.gov
- Documentation: https://jarvis-tools.readthedocs.io
- GitHub: https://github.com/usnistgov/jarvis
- Publications: https://pages.nist.gov/jarvis/publications/