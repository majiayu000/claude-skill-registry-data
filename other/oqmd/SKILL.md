---
name: oqmd
description: Use this skill when accessing OQMD for open quantum materials data, phase stability, or DFT formation energies.
metadata:
    skill-author: MindSpore Science Team
---
## Overview
Open Quantum Materials Database (OQMD) provides DFT calculations for known and hypothetical compounds with focus on phase stability. Developed by the Wolverton Research Group at Northwestern University.

## When to Use This Skill

Use this skill when you need to:

1. **Query phase stability data** - Formation energies and convex hull distances
2. **Access hypothetical compounds** - Decorated prototype structures for materials discovery
3. **Generate phase diagrams** - Built-in phase diagram calculations
4. **Screen for stable materials** - Filter by energy above hull
5. **Compare formation energies** - Consistent PBE functional across all calculations
6. **Access ICSD structures** - Experimental structures also included
7. **Study thermodynamic stability** - Comprehensive energy data for screening
8. **Machine learning datasets** - Download bulk data for ML applications

## Data Types
- Formation energies
- Phase diagrams
- Crystal structures (ICSD and hypothetical)
- Band gaps and electronic properties
- Stability and convex hull data

## API Access

### REST API

#### Base URL
```
http://oqmd.org/api/
```

### Query Examples

#### Search Materials
```python
import requests

BASE_URL = "http://oqmd.org/api"

# Search by composition
response = requests.get(f"{BASE_URL}/composition", params={"name": "LiFePO4"})
data = response.json()

print(f"Found {data['meta']['total_count']} entries")
for entry in data['data'][:5]:
    print(f"ID: {entry['entry_id']}, Formation: {entry['delta_e']} eV/atom")
```

#### Get Material by ID
```python
import requests

# Get specific material
material_id = 12345
response = requests.get(f"http://oqmd.org/api/materials/{material_id}")
material = response.json()

print(f"Formula: {material['composition']}")
print(f"Formation energy: {material['delta_e']} eV/atom")
print(f"Band gap: {material.get('band_gap', 'N/A')} eV")
```

#### Query with Filters
```python
import requests

# Search with multiple filters
params = {
    "element": "Li,Fe,O",
    "delta_e__lt": 0.0,
    "band_gap__gt": 0.5,
    "limit": 10
}

response = requests.get("http://oqmd.org/api/composition", params=params)
data = response.json()

for entry in data['data']:
    print(f"{entry['name']}: E_f = {entry['delta_e']} eV/atom")
```

#### Get Phase Diagram Data
```python
import requests

# Get phase diagram data for a system
elements = "Li-Fe-O"
response = requests.get(f"http://oqmd.org/api/phasediagram/{elements}")
phase_data = response.json()

for entry in phase_data.get('stable', []):
    print(f"Stable: {entry['composition']}")
```

### Python Client (qmpy)

#### Installation
```bash
pip install qmpy
```

#### Basic Usage
```python
from qmpy import *

# Connect to OQMD database
# Note: Requires database access or REST API fallback

# Search entries
entries = Element.objects.filter(name="Si")
print(f"Silicon entries: {entries.count()}")

# Get formation energies
for entry in entries[:5]:
    calc = entry.calculation_set.first()
    if calc:
        print(f"Structure: {entry.name}")
        print(f"Formation energy: {calc.delta_e} eV/atom")
```

#### Using REST API from Python
```python
import requests
import json

class OQMDClient:
    def __init__(self):
        self.base_url = "http://oqmd.org/api"

    def search_composition(self, formula, limit=100):
        """Search by chemical formula"""
        params = {"name": formula, "limit": limit}
        response = requests.get(f"{self.base_url}/composition", params=params)
        return response.json()

    def get_material(self, entry_id):
        """Get material by OQMD ID"""
        response = requests.get(f"{self.base_url}/materials/{entry_id}")
        return response.json()

    def search_by_elements(self, elements, **kwargs):
        """Search by elements"""
        params = {"element": ",".join(elements), **kwargs}
        response = requests.get(f"{self.base_url}/composition", params=params)
        return response.json()

    def get_formation_energy(self, formula):
        """Get formation energy for a formula"""
        data = self.search_composition(formula)
        if data['data']:
            return data['data'][0]['delta_e']
        return None

# Usage
client = OQMDClient()

# Search for battery materials
results = client.search_by_elements(
    ["Li", "Co", "O"],
    delta_e__lt=0.0,
    limit=20
)

for entry in results['data'][:5]:
    print(f"{entry['name']}: {entry['delta_e']} eV/atom")
```

#### Get Structure Data
```python
import requests

def get_structure(entry_id):
    """Get crystal structure for an OQMD entry"""
    # Get material data
    response = requests.get(f"http://oqmd.org/api/materials/{entry_id}")
    material = response.json()

    # Structure is typically in the 'structure' field
    if 'structure' in material:
        return material['structure']

    # Alternative: get CIF format
    cif_url = f"http://oqmd.org/materials/{entry_id}/structure.cif"
    cif_response = requests.get(cif_url)
    return cif_response.text

# Usage
structure = get_structure(12345)
print(structure[:200])
```

### Available Properties

| Property | Field | Description |
|----------|-------|-------------|
| Entry ID | `entry_id` | OQMD unique identifier |
| Composition | `composition`, `name` | Chemical formula |
| Formation Energy | `delta_e` | Formation energy (eV/atom) |
| Band Gap | `band_gap` | Band gap (eV) |
| Volume | `volume` | Unit cell volume (A3) |
| Energy Above Hull | `stability` | Distance from hull (eV/atom) |
| Space Group | `spacegroup` | Space group number |

### Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `element` | Filter by elements | `Li,Co,O` |
| `name` | Filter by composition | `LiCoO2` |
| `delta_e__lt` | Formation energy less than | `-0.1` |
| `delta_e__gt` | Formation energy greater than | `-2.0` |
| `band_gap__gt` | Band gap greater than | `0.5` |
| `stability__lt` | Energy above hull less than | `0.05` |
| `limit` | Number of results | `100` |
| `offset` | Pagination offset | `50` |

### Phase Diagram Queries

```python
import requests

def get_stable_compounds(elements):
    """Get all stable compounds in a chemical system"""
    system = "-".join(elements)
    url = f"http://oqmd.org/api/phasediagram/{system}"

    response = requests.get(url)
    data = response.json()

    stable = data.get('stable', [])
    unstable = data.get('unstable', [])

    print(f"Stable compounds in {system}:")
    for compound in stable:
        print(f"  {compound['composition']}: {compound['delta_e']} eV/atom")

    return stable, unstable

# Usage
stable, unstable = get_stable_compounds(["Li", "Fe", "O"])
```

### Convex Hull Analysis

```python
import requests
import json

def get_convex_hull_data(elements):
    """Download convex hull data for visualization"""
    system = "-".join(elements)

    # Get all entries in the system
    params = {
        "element": ",".join(elements),
        "limit": 1000
    }

    response = requests.get("http://oqmd.org/api/composition", params=params)
    data = response.json()

    # Sort by formation energy
    entries = sorted(data['data'], key=lambda x: x['delta_e'])

    # Find hull entries (most negative formation energies)
    hull_entries = [e for e in entries if e.get('stability', 999) == 0]

    return {
        'all_entries': entries,
        'hull_entries': hull_entries
    }

# Usage
hull_data = get_convex_hull_data(["Li", "Co", "O"])
print(f"Hull entries: {len(hull_data['hull_entries'])}")
```

### Bulk Download

```python
import requests
import pandas as pd

def download_oqmd_dataset(nspecies_max=3, limit=10000):
    """Download OQMD dataset as DataFrame"""
    all_data = []
    offset = 0
    batch_size = 500

    while len(all_data) < limit:
        params = {
            "nspecies__lte": nspecies_max,
            "delta_e__lt": 0.1,
            "limit": batch_size,
            "offset": offset
        }

        response = requests.get("http://oqmd.org/api/composition", params=params)
        data = response.json()

        if not data['data']:
            break

        all_data.extend(data['data'])
        offset += batch_size

        if len(data['data']) < batch_size:
            break

    df = pd.DataFrame(all_data)
    return df

# Usage
df = download_oqmd_dataset(nspecies_max=4, limit=5000)
df.to_csv("oqmd_data.csv", index=False)
print(f"Downloaded {len(df)} entries")
```

## Best Practices

### API Usage
- **Use limit parameter**: Always set reasonable limits to avoid timeouts
- **Filter at source**: Use query parameters to reduce data transfer
- **Batch large queries**: Use pagination with offset parameter
- **Cache results**: Store query results locally

### Data Quality
```python
# Filter for stable compounds
params = {
    "stability__lt": 0.025,  # Within 25 meV/atom of hull
    "delta_e__lt": 0.0,       # Negative formation energy
    "limit": 1000
}

response = requests.get("http://oqmd.org/api/composition", params=params)
stable_compounds = response.json()['data']
```

### Query Optimization
```python
# Efficient: Use filters to reduce response size
params = {
    "element": "Li,Co,O",
    "stability__lt": 0.05,
    "fields": "entry_id,name,delta_e,stability"  # Request only needed fields
}

# Inefficient: Download all and filter locally
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Connection refused` | OQMD server may be down, try later |
| `Empty results` | Check filter syntax, verify element names |
| `Timeout` | Reduce limit parameter, use pagination |
| `Invalid parameter` | Check parameter names match API docs |
| `Missing field` | Not all entries have all properties; use `.get()` |

### Server Availability
```python
import requests

def check_oqmd_status():
    """Check if OQMD API is responding"""
    try:
        response = requests.get("http://oqmd.org/api/composition",
                                params={"limit": 1}, timeout=10)
        return response.status_code == 200
    except:
        return False

if not check_oqmd_status():
    print("OQMD API not responding")
```

### Missing Properties
```python
# Handle missing properties safely
entry = data['data'][0]

band_gap = entry.get('band_gap', None)
if band_gap is None:
    print("Band gap not available for this entry")
```

## Resources
- Website: http://oqmd.org
- API Docs: http://oqmd.org/api/docs
- GitHub: https://github.com/wolverton-research-group/qmpy
- Paper: https://doi.org/10.1007/s11837-013-0755-4