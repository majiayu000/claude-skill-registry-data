---
name: materials-project
description: Use this skill when accessing Materials Project for computed materials properties, phase diagrams, battery materials, or DFT data.
metadata:
    skill-author: MindSpore Science Team
---
## Overview
Materials Project provides computed information on known and predicted materials using high-throughput DFT, enabling materials design and discovery.

## When to Use This Skill

Use this skill when you need to:

1. **Query computed materials properties** - Formation energies, band gaps, elastic constants, dielectric constants, piezoelectric tensors
2. **Build phase diagrams** - Generate binary, ternary, and quaternary phase diagrams for stability analysis
3. **Search for battery materials** - Access electrode data, voltage profiles, capacity predictions for Li-ion and other batteries
4. **Filter materials by properties** - Find materials matching specific property criteria (band gap range, stability, elements)
5. **Retrieve crystal structures** - Get optimized structures in various formats for further calculations
6. **Access electronic structure** - Download band structures, density of states, and charge densities
7. **Explore Pourbaix diagrams** - Aqueous stability analysis for electrochemical applications
8. **Machine learning datasets** - Download curated datasets for training ML models

## Data Types
- Formation energies and stability
- Band gaps and electronic structure
- Elastic and mechanical properties
- Phase diagrams and Pourbaix diagrams
- Battery materials and electrode data

## API Access

### Authentication
- Register at https://materialsproject.org to get API key
- API key required for all requests
- Set via environment variable `MP_API_KEY` or pass directly

### Python API (mp-api)

#### Installation
```bash
pip install mp-api
```

#### Basic Setup
```python
from mp_api.client import MPRester

# Using environment variable MP_API_KEY
with MPRester() as mpr:
    pass

# Or pass API key directly
with MPRester("YOUR_API_KEY") as mpr:
    pass
```

### Query Examples

#### Search by Formula
```python
from mp_api.client import MPRester

with MPRester() as mpr:
    # Search for materials by formula
    docs = mpr.materials.summary.search(formula="LiFePO4")

    # Get first result
    doc = docs[0]
    print(f"Material ID: {doc.material_id}")
    print(f"Formula: {doc.formula_pretty}")
    print(f"Band gap: {doc.band_gap} eV")
    print(f"Formation energy: {doc.formation_energy_per_atom} eV/atom")
```

#### Search by Properties
```python
with MPRester() as mpr:
    # Search by band gap range
    docs = mpr.materials.summary.search(
        band_gap=(0.5, 2.0),
        elements=["Li", "Co", "O"],
        formula="Li*O*",
    )

    for doc in docs[:5]:
        print(f"{doc.formula_pretty}: E_g = {doc.band_gap} eV")
```

#### Get Material by ID
```python
with MPRester() as mpr:
    # Get specific material
    doc = mpr.materials.summary.get_data_by_id("mp-149")

    # This is silicon
    print(f"Formula: {doc.formula_pretty}")
    print(f"Band gap: {doc.band_gap} eV")
    print(f"Crystal system: {doc.symmetry.crystal_system}")
```

#### Retrieve Structure
```python
from pymatgen.core import Structure

with MPRester() as mpr:
    # Get structure as pymatgen object
    structure = mpr.get_structure_by_material_id("mp-149")

    # Or from summary document
    doc = mpr.materials.summary.get_data_by_id("mp-149")
    structure = doc.structure

    print(f"Lattice: {structure.lattice}")
    print(f"Number of sites: {len(structure)}")
```

#### Get Electronic Structure
```python
with MPRester() as mpr:
    # Get band structure
    bs = mpr.get_bandstructure_by_material_id("mp-149")

    # Get density of states
    dos = mpr.get_dos_by_material_id("mp-149")

    # Band gap info
    print(f"Band gap: {bs.get_band_gap()}")
```

#### Get Phase Diagram
```python
with MPRester() as mpr:
    # Get entries for phase diagram
    entries = mpr.get_entries_in_chemsys(["Li", "Fe", "O"])

    from pymatgen.analysis.phase_diagram import PhaseDiagram
    pd = PhaseDiagram(entries)
```

#### Elastic Properties
```python
with MPRester() as mpr:
    # Get elastic tensor
    elastic_doc = mpr.materials.elasticity.get_data_by_id("mp-149")

    if elastic_doc:
        print(f"K_VRH: {elastic_doc.k_vrh} GPa")
        print(f"G_VRH: {elastic_doc.g_vrh} GPa")
```

#### Battery Materials
```python
with MPRester() as mpr:
    # Search battery materials
    battery_docs = mpr.materials.battery.search(
        working_voltage=(3.0, 4.5)
    )

    for doc in battery_docs[:5]:
        print(f"{doc.formula_pretty}: V = {doc.average_voltage} V")
```

### Available Properties

| Property | Field Name | Description |
|----------|-----------|-------------|
| Material ID | `material_id` | Unique identifier (mp-XXXXX) |
| Formula | `formula_pretty` | Reduced formula |
| Band Gap | `band_gap` | Band gap in eV |
| Formation Energy | `formation_energy_per_atom` | eV/atom |
| Energy Above Hull | `energy_above_hull` | Stability metric (eV/atom) |
| Crystal System | `symmetry.crystal_system` | Crystal structure type |
| Density | `density` | g/cm3 |
| Volume | `volume` | Unit cell volume (A3) |
| NSites | `nsites` | Number of atoms in cell |

### REST API Endpoints

Base URL: `https://api.materialsproject.org`

```
GET /materials/summary/
GET /materials/{material_id}
GET /materials/{material_id}/structure
GET /materials/{material_id}/bandstructure
GET /materials/{material_id}/dos
GET /materials/{material_id}/elasticity
GET /materials/{material_id}/thermo
```

### Bulk Download

```python
# Download all materials with specific properties
with MPRester() as mpr:
    docs = mpr.materials.summary.search(
        fields=["material_id", "formula_pretty", "band_gap",
                "formation_energy_per_atom", "energy_above_hull"]
    )

    # Convert to DataFrame
    import pandas as pd
    df = pd.DataFrame([d.dict() for d in docs])
    df.to_csv("materials_data.csv", index=False)
```

### Query Filters

```python
# Common filter operations
docs = mpr.materials.summary.search(
    # Numerical comparisons
    band_gap=(0.5, 3.0),  # Range
    energy_above_hull=(None, 0.05),  # Less than 0.05 eV/atom

    # Element filters
    elements=["Si", "O"],  # Contains both Si and O
    nelements=(2, 4),  # 2-4 elements

    # Formula patterns
    formula="ABO3",  # Perovskite formula

    # Crystal system
    crystal_system="cubic",

    # Stability
    is_stable=True,
    thelectric=True,  # Theoretical materials

    # Sorting and limiting
    sort_fields=["formation_energy_per_atom"],
    num_sites=(2, 50),
)
```

## Best Practices

### API Usage
- **Use environment variables** for API keys: `export MP_API_KEY=your_key`
- **Batch queries** when retrieving multiple materials to reduce API calls
- **Specify fields** to reduce response size: `fields=["material_id", "band_gap"]`
- **Use pagination** for large queries: `num_chunks` parameter in search methods
- **Cache results locally** to avoid repeated queries for the same data

### Rate Limits
- Default: 5000 requests per hour per user
- Implement exponential backoff for retries
- Use bulk endpoints instead of individual material queries
- Check rate limit headers in API responses

### Caching
```python
# Cache results to avoid repeated API calls
import json
from pathlib import Path

def get_material_cached(mpr, mp_id, cache_dir="mp_cache"):
    cache_path = Path(cache_dir) / f"{mp_id}.json"

    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    doc = mpr.materials.summary.get_data_by_id(mp_id)
    data = doc.dict()

    cache_path.parent.mkdir(exist_ok=True)
    with open(cache_path, "w") as f:
        json.dump(data, f)

    return data
```

### Data Quality
- Filter by `energy_above_hull < 0.05` eV/atom for stable materials
- Check `is_stable` flag for thermodynamic stability
- Verify calculation type (GGA, GGA+U, SCAN) for property accuracy
- Use `theoretical=False` for experimentally observed materials only

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` | Check API key is valid and properly set |
| `429 Too Many Requests` | Reduce request rate, implement backoff |
| `404 Not Found` | Verify material_id format (mp-XXXXX) |
| `Empty results` | Check query syntax, filters may be too restrictive |
| `Timeout errors` | Reduce batch size, use async requests |
| `Import error: mp_api` | `pip install mp-api --upgrade` |

### Connection Issues
```python
import time
from mp_api.client import MPRester

def robust_query(mpr, query_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return query_func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1}/{max_retries} in {wait_time}s")
            time.sleep(wait_time)
```

### API Key Issues
```python
import os

# Verify API key is set
api_key = os.environ.get("MP_API_KEY")
if not api_key:
    raise ValueError("Set MP_API_KEY environment variable")

# Alternative: use dotenv
from dotenv import load_dotenv
load_dotenv()
```

## Resources
- Website: https://materialsproject.org
- API Docs: https://api.materialsproject.org/docs
- mp-api: https://github.com/materialsproject/api