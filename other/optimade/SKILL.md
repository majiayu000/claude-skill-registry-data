---
name: optimade
description: Use when querying multiple materials databases, building federated search tools, or implementing interoperable materials data APIs.
metadata:
    skill-author: MindSpore Science Team
---

## When to Use This Skill

Use this skill when:
- Querying multiple materials databases through a unified API
- Building federated search across crystallographic databases
- Integrating with Materials Project, COD, OQMD, NOMAD, or AFLOW
- Implementing materials data interoperability
- Developing client applications for materials databases
- Building high-throughput materials discovery workflows

## Overview

OPTIMADE (Open Databases Integration for Materials Design) is a REST API standard for materials databases. It provides unified access to crystal structures and properties across multiple databases.

## Format/Schema Details

- **RESTful API**: Standard endpoints for data access
- **Filter Syntax**: URL-based query language for complex searches
- **Entry Types**: Structures, calculations, references
- **Properties**: Standardized property names and units
- **Pagination**: Cursor-based navigation of results
- **Providers Registry**: List of OPTIMADE-compliant databases

## API Access

### Base Endpoints

| Endpoint | Description |
|----------|-------------|
| `/structures` | Crystal structures |
| `/calculations` | Calculation entries |
| `/references` | Bibliographic references |
| `/info` | API information |
| `/links` | Related resources |
| `/info/structures` | Structure properties |

### Major Providers

| Provider | Base URL |
|----------|----------|
| Materials Project | `https://api.materialsproject.org/optimade/v1` |
| COD | `https://www.crystallography.net/cod/optimade/v1` |
| OQMD | `https://oqmd.org/optimade/v1` |
| NOMAD | `https://nomad-lab.eu/prod/v1/optimade` |
| AFLOW | `https://aflow.org/api/optimade/v1` |
| JARVIS | `https://jarvis.nist.gov/optimade/v1` |

## Query Examples

### Basic Structure Query

```python
import requests

# Query Materials Project via OPTIMADE
BASE_URL = "https://api.materialsproject.org/optimade/v1"

params = {
    "filter": 'elements HAS "Si"',
    "page_limit": 10
}

response = requests.get(f"{BASE_URL}/structures", params=params)
data = response.json()

for entry in data.get('data', [])[:5]:
    print(f"ID: {entry['id']}")
    print(f"Formula: {entry['attributes']['chemical_formula']}")
    print(f"Elements: {entry['attributes']['elements']}")
```

### Query Multiple Providers

```python
import requests

PROVIDERS = {
    "Materials Project": "https://api.materialsproject.org/optimade/v1",
    "COD": "https://www.crystallography.net/cod/optimade/v1",
    "OQMD": "https://oqmd.org/optimade/v1",
}

def query_all_providers(filter_str, limit=5):
    """Query multiple OPTIMADE providers"""
    results = {}

    for name, base_url in PROVIDERS.items():
        try:
            params = {
                "filter": filter_str,
                "page_limit": limit
            }
            response = requests.get(f"{base_url}/structures", params=params)
            data = response.json()
            results[name] = data.get('data', [])
            print(f"{name}: {len(results[name])} results")
        except Exception as e:
            print(f"{name}: Error - {e}")

    return results

# Usage
results = query_all_providers('chemical_formula = "SiO2"')
```

### Python Client (optimade-python-tools)

#### Installation
```bash
pip install optimade
```

#### Basic Usage
```python
from optimade.client import OptimadeClient

# Initialize client with specific provider
client = OptimadeClient("https://api.materialsproject.org/optimade/v1")

# Query structures
structures = client.get_structures(
    filter='elements HAS "Li" AND elements HAS "Co"',
    page_limit=10
)

for struct in structures.data[:5]:
    print(f"{struct.id}: {struct.attributes.chemical_formula}")
```

#### Multi-Provider Search
```python
from optimade.client import OptimadeClient

# Query multiple providers at once
client = OptimadeClient()  # Uses all known providers

results = client.get_structures(
    filter='chemical_formula = "LiFePO4"',
    page_limit=5
)

# Results grouped by provider
for provider, structures in results.items():
    print(f"\n{provider}:")
    for struct in structures:
        print(f"  {struct.id}: {struct.attributes.chemical_formula}")
```

### Filter Syntax

| Operator | Syntax | Example |
|----------|--------|---------|
| Equals | `=` | `chemical_formula = "SiO2"` |
| Not equals | `!=` | `nelements != 1` |
| Greater than | `>` | `nsites > 10` |
| Less than | `<` | `nsites < 100` |
| Greater or equal | `>=` | `nsites >= 10` |
| Less or equal | `<=` | `nsites <= 100` |
| Contains | `HAS` | `elements HAS "Si"` |
| Contains all | `HAS ALL` | `elements HAS ALL "Si","O"` |
| Contains any | `HAS ANY` | `elements HAS ANY "Si","Ge"` |
| Starts with | `STARTS WITH` | `chemical_formula STARTS WITH "Li"` |
| Ends with | `ENDS WITH` | `chemical_formula ENDS WITH "O3"` |
| Contains string | `CONTAINS` | `chemical_formula CONTAINS "Fe"` |
| AND | `AND` | `elements HAS "Si" AND nsites > 10` |
| OR | `OR` | `elements HAS "Fe" OR elements HAS "Co"` |
| NOT | `NOT` | `NOT elements HAS "H"` |

### Query Examples

#### Filter by Elements
```python
import requests

BASE_URL = "https://api.materialsproject.org/optimade/v1"

# Compounds containing Si AND O
params = {
    "filter": 'elements HAS ALL "Si","O"',
    "page_limit": 10
}

response = requests.get(f"{BASE_URL}/structures", params=params)
data = response.json()

for entry in data['data']:
    print(entry['attributes']['chemical_formula'])
```

#### Filter by Formula
```python
# Exact formula match
params = {
    "filter": 'chemical_formula = "LiFePO4"'
}

# Formula pattern
params = {
    "filter": 'chemical_formula CONTAINS "Fe"'
}

# Formula starts with
params = {
    "filter": 'chemical_formula STARTS WITH "Li"'
}
```

#### Filter by Properties
```python
import requests

BASE_URL = "https://api.materialsproject.org/optimade/v1"

# Filter by number of sites
params = {
    "filter": 'nsites >= 10 AND nsites <= 100',
    "page_limit": 10
}

# Filter by crystal system (if available)
params = {
    "filter": 'nsites > 5 AND nelements <= 3'
}
```

#### Complex Queries
```python
import requests

BASE_URL = "https://api.materialsproject.org/optimade/v1"

# Multiple conditions
filter_query = '''
    elements HAS ALL "Li","O" AND
    nelements <= 4 AND
    nsites <= 20 AND
    NOT elements HAS "H"
'''

params = {
    "filter": filter_query,
    "page_limit": 20
}

response = requests.get(f"{BASE_URL}/structures", params=params)
data = response.json()

print(f"Found {data['meta'].get('data_returned', 'unknown')} structures")
```

### Available Properties

| Property | Description | Type |
|----------|-------------|------|
| `id` | Entry identifier | string |
| `chemical_formula` | Formula | string |
| `chemical_formula_reduced` | Reduced formula | string |
| `elements` | Element symbols | list |
| `nelements` | Number of elements | integer |
| `nsites` | Number of sites | integer |
| `lattice_vectors` | Cell vectors | array |
| `cartesian_site_positions` | Atomic positions | array |
| `species_at_sites` | Species labels | list |
| `dimension_types` | Periodic directions | list |
| `nperiodic_dimensions` | Periodic dimensions | integer |

### Pagination

```python
import requests

def get_all_structures(base_url, filter_str, page_size=50):
    """Paginate through all results"""
    all_data = []
    page_offset = 0

    while True:
        params = {
            "filter": filter_str,
            "page_limit": page_size,
            "page_offset": page_offset
        }

        response = requests.get(f"{base_url}/structures", params=params)
        data = response.json()

        entries = data.get('data', [])
        all_data.extend(entries)

        # Check for more pages
        if len(entries) < page_size:
            break

        page_offset += page_size

        # Safety limit
        if page_offset > 1000:
            print("Reached pagination limit")
            break

    return all_data

# Usage
structures = get_all_structures(
    "https://api.materialsproject.org/optimade/v1",
    'elements HAS "Si"'
)
print(f"Retrieved {len(structures)} structures")
```

### Get Structure as pymatgen

```python
from pymatgen.core import Structure
import requests

def get_pymatgen_structure(base_url, entry_id):
    """Get pymatgen Structure from OPTIMADE entry"""
    response = requests.get(f"{base_url}/structures/{entry_id}")
    entry = response.json()['data']

    attrs = entry['attributes']

    # Extract structure data
    lattice_vectors = attrs['lattice_vectors']
    positions = attrs['cartesian_site_positions']
    species = attrs['species_at_sites']

    # Create pymatgen Structure
    structure = Structure(
        lattice=lattice_vectors,
        species=species,
        coords=positions,
        coords_are_cartesian=True
    )

    return structure

# Usage
structure = get_pymatgen_structure(
    "https://api.materialsproject.org/optimade/v1",
    "mp-149"
)
print(f"Formula: {structure.formula}")
print(f"Lattice: {structure.lattice}")
```

### Provider Registry

```python
import requests

# Get list of all OPTIMADE providers
response = requests.get("https://providers.optimade.org/v1/links")
providers = response.json()

print("Available OPTIMADE Providers:")
for provider in providers.get('data', []):
    attrs = provider.get('attributes', {})
    print(f"  {attrs.get('name', 'Unknown')}: {attrs.get('base_url', 'N/A')}")
```

### Response Format

```json
{
  "data": [
    {
      "id": "mp-149",
      "type": "structures",
      "attributes": {
        "chemical_formula": "Si",
        "elements": ["Si"],
        "nelements": 1,
        "nsites": 2,
        "lattice_vectors": [[5.43, 0, 0], [0, 5.43, 0], [0, 0, 5.43]],
        "cartesian_site_positions": [[0, 0, 0], [2.715, 2.715, 2.715]],
        "species_at_sites": ["Si", "Si"]
      }
    }
  ],
  "meta": {
    "data_returned": 1,
    "more_data_available": false
  }
}
```

## Resources

- Website: https://www.optimade.org
- Specification: https://github.com/Materials-Consortia/OPTIMADE
- Providers: https://providers.optimade.org
- Python Tools: https://github.com/Materials-Consortia/optimade-python-tools