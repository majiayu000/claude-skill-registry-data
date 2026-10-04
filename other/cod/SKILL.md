---
name: cod
description: Use this skill when accessing Crystallography Open Database for crystal structures, CIF files, or open crystallographic data.
metadata:
    skill-author: MindSpore Science Team
---
## Overview
Crystallography Open Database (COD) is an open-access collection of crystal structures of small molecules and organic, metal-organic, and inorganic compounds. It contains experimentally determined structures from X-ray and neutron diffraction.

## When to Use This Skill

Use this skill when you need to:

1. **Access experimental crystal structures** - Verified structures from peer-reviewed publications
2. **Download CIF files** - Standard crystallographic information file format
3. **Search by chemical formula** - Find all polymorphs of a compound
4. **Query by elements** - Find structures containing specific elements
5. **Get bibliographic data** - Publication DOI, authors, and references
6. **Access via OPTIMADE** - Standardized API across databases
7. **Find structure prototypes** - Identify common structure types
8. **Validate computed structures** - Compare DFT results with experiment

## Data Types
- Crystal structures in CIF format
- Small molecules and extended structures
- Powder diffraction patterns
- Experimental structure data
- Bibliographic references

## API Access

### REST API

#### Base URL
```
http://www.crystallography.net/cod/
```

### Query Examples

#### Search by Formula
```python
import requests

BASE_URL = "http://www.crystallography.net/cod"

# Search by chemical formula
params = {
    "format": "json",
    "filter": "formula LIKE '%LiFePO4%'"
}

response = requests.get(f"{BASE_URL}/result.php", params=params)
data = response.json()

for entry in data[:5]:
    print(f"COD ID: {entry['file']}")
    print(f"Formula: {entry['formula']}")
```

#### Get CIF by ID
```python
import requests

def get_cif(cod_id):
    """Download CIF file for a COD entry"""
    url = f"http://www.crystallography.net/cod/{cod_id}.cif"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    return None

# Usage
cif_content = get_cif(1000000)
if cif_content:
    print(cif_content[:500])
```

#### Search with Multiple Filters
```python
import requests

BASE_URL = "http://www.crystallography.net/cod"

params = {
    "format": "json",
    "filter": "elements LIKE '%Si%' AND elements LIKE '%O%'"
}

response = requests.get(f"{BASE_URL}/result.php", params=params)
data = response.json()

print(f"Found {len(data)} Si-O compounds")

for entry in data[:5]:
    print(f"COD {entry['file']}: {entry['formula']}")
```

#### Search by Element
```python
import requests

def search_by_elements(elements, max_results=100):
    """Search compounds containing specific elements"""
    element_filter = " AND ".join([f"elements LIKE '%{el}%'" for el in elements])

    params = {
        "format": "json",
        "filter": element_filter
    }

    response = requests.get("http://www.crystallography.net/cod/result.php", params=params)
    return response.json()

# Usage
results = search_by_elements(["Ti", "O"])
print(f"Found {len(results)} Ti-O compounds")
```

### COD MySQL Query Interface

```python
import requests

# Direct MySQL-like queries
query_url = "http://www.crystallography.net/cod/result.php"

# Search by space group
params = {
    "format": "json",
    "filter": "sg = 'P1'"
}

response = requests.get(query_url, params=params)
data = response.json()

for entry in data[:5]:
    print(f"{entry['file']}: {entry['formula']} (SG: {entry['sg']})")
```

### Available Fields

| Field | Description | Example |
|-------|-------------|---------|
| `file` | COD ID | `1000000` |
| `formula` | Chemical formula | `Fe2 O3` |
| `formula_html` | HTML formatted formula | `Fe<sub>2</sub>O<sub>3</sub>` |
| `elements` | Element symbols | `Fe O` |
| `sg` | Space group | `Pnma` |
| `sg_number` | Space group number | `62` |
| `a`, `b`, `c` | Lattice parameters (A) | `5.038` |
| `alpha`, `beta`, `gamma` | Cell angles (deg) | `90` |
| `cell_temp` | Temperature (K) | `293` |
| `vol` | Cell volume (A3) | `262.4` |
| `Z` | Number of formula units | `4` |
| `title` | Publication title | `Crystal structure of...` |
| `doi` | DOI of publication | `10.1107/...` |

### Advanced Query Examples

#### Search by Cell Parameters
```python
import requests

# Find structures with specific cell dimensions
params = {
    "format": "json",
    "filter": "a BETWEEN 4 AND 5 AND b BETWEEN 4 AND 5 AND c BETWEEN 4 AND 5"
}

response = requests.get("http://www.crystallography.net/cod/result.php", params=params)
data = response.json()

print(f"Found {len(data)} structures with a,b,c in 4-5 A range")
```

#### Search by Publication
```python
import requests

# Search by DOI or journal
params = {
    "format": "json",
    "filter": "doi LIKE '%10.1107%'"
}

response = requests.get("http://www.crystallography.net/cod/result.php", params=params)
data = response.json()

print(f"Found {len(data)} structures from Acta Crystallographica")
```

### Using pymatgen with COD

```python
from pymatgen.core import Structure
import requests

def get_structure_from_cod(cod_id):
    """Get pymatgen Structure from COD entry"""
    url = f"http://www.crystallography.net/cod/{cod_id}.cif"
    response = requests.get(url)

    if response.status_code == 200:
        structure = Structure.from_str(response.text, fmt="cif")
        return structure
    return None

# Usage
structure = get_structure_from_cod(1000000)
if structure:
    print(f"Formula: {structure.formula}")
    print(f"Lattice: {structure.lattice}")
    print(f"Number of sites: {len(structure)}")
```

### Using ASE with COD

```python
from ase.io import read
from ase.db import connect
import requests
import io

def get_atoms_from_cod(cod_id):
    """Get ASE Atoms object from COD entry"""
    url = f"http://www.crystallography.net/cod/{cod_id}.cif"
    response = requests.get(url)

    if response.status_code == 200:
        atoms = read(io.StringIO(response.text), format="cif")
        return atoms
    return None

# Usage
atoms = get_atoms_from_cod(1000000)
if atoms:
    print(f"Formula: {atoms.get_chemical_formula()}")
    print(f"Number of atoms: {len(atoms)}")
```

### OPTIMADE Access to COD

```python
import requests

# COD provides OPTIMADE interface
OPTIMADE_URL = "https://www.crystallography.net/cod/optimade/v1"

# Get structures
params = {
    "filter": 'elements HAS "Si"',
    "page_limit": 10
}

response = requests.get(f"{OPTIMADE_URL}/structures", params=params)
data = response.json()

for entry in data.get('data', [])[:5]:
    print(f"COD ID: {entry['id']}")
    print(f"Formula: {entry['attributes']['chemical_formula']}")
```

### Bulk Download

```python
import requests
from concurrent.futures import ThreadPoolExecutor
import os

def download_cif(cod_id, output_dir="cod_cifs"):
    """Download a single CIF file"""
    os.makedirs(output_dir, exist_ok=True)
    url = f"http://www.crystallography.net/cod/{cod_id}.cif"

    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(output_dir, f"{cod_id}.cif")
        with open(filepath, "w") as f:
            f.write(response.text)
        return cod_id
    return None

def bulk_download(cod_ids, max_workers=10):
    """Download multiple CIF files in parallel"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(download_cif, cod_ids))

    successful = [r for r in results if r is not None]
    print(f"Downloaded {len(successful)}/{len(cod_ids)} CIF files")
    return successful

# Usage
params = {"format": "json", "filter": "elements LIKE '%Li%'" }
response = requests.get("http://www.crystallography.net/cod/result.php", params=params)
data = response.json()
cod_ids = [entry['file'] for entry in data[:50]]

bulk_download(cod_ids)
```

### Complete Structure Retrieval Pipeline

```python
import requests
from pymatgen.core import Structure
import json

def search_and_analyze(formula_pattern, max_results=10):
    """Search COD and analyze structures"""
    params = {
        "format": "json",
        "filter": f"formula LIKE '%{formula_pattern}%'"
    }

    response = requests.get("http://www.crystallography.net/cod/result.php", params=params)
    entries = response.json()[:max_results]

    results = []
    for entry in entries:
        cod_id = entry['file']

        # Download CIF
        cif_url = f"http://www.crystallography.net/cod/{cod_id}.cif"
        cif_response = requests.get(cif_url)

        if cif_response.status_code == 200:
            try:
                structure = Structure.from_str(cif_response.text, fmt="cif")
                results.append({
                    'cod_id': cod_id,
                    'formula': structure.formula,
                    'space_group': structure.get_space_group_info()[0],
                    'volume': structure.volume,
                    'num_sites': len(structure)
                })
            except Exception as e:
                print(f"Error parsing {cod_id}: {e}")

    return results

# Usage
results = search_and_analyze("Fe2O3")
for r in results:
    print(f"COD {r['cod_id']}: {r['formula']} ({r['space_group']})")
```

## Best Practices

### API Usage
- **Use JSON format**: Always set `format=json` for programmatic access
- **Rate limiting**: Add delays between requests for bulk downloads
- **Filter early**: Use SQL filters to reduce data transfer
- **Cache results**: Store downloaded CIFs locally

### Query Optimization
```python
# Efficient: Filter on server side
params = {
    "format": "json",
    "filter": "elements LIKE '%Li%' AND sg = 'Fm-3m'"
}

# Inefficient: Download all and filter locally
```

### Data Quality
```python
# Filter for high-quality data
params = {
    "format": "json",
    "filter": "Rfactor < 0.05 AND status = 'finished'"
}
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `HTTP 404` | Verify COD ID exists (7-digit number) |
| `Empty results` | Check filter syntax, try broader search |
| `Connection refused` | COD server may be down, try mirror |
| `CIF parse error` | Some entries may have formatting issues |
| `Slow queries` | Add more specific filters |

### Alternative Mirrors
```python
# Use HTTPS mirror if HTTP fails
MIRRORS = [
    "http://www.crystallography.net/cod",
    "https://www.crystallography.net/cod"
]

def get_cif_with_fallback(cod_id):
    for mirror in MIRRORS:
        try:
            url = f"{mirror}/{cod_id}.cif"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
        except:
            continue
    return None
```

### CIF Parsing Issues
```python
# Handle malformed CIFs
from pymatgen.core import Structure

def safe_parse_cif(cif_text):
    try:
        return Structure.from_str(cif_text, fmt="cif")
    except Exception as e:
        print(f"CIF parse error: {e}")
        # Try alternative parsing
        try:
            from ase.io import read
            import io
            atoms = read(io.StringIO(cif_text), format="cif")
            return atoms
        except:
            return None
```

## Resources
- Website: https://www.crystallography.net
- API Docs: https://www.crystallography.net/cod/result.php
- OPTIMADE: https://www.crystallography.net/cod/optimade
- Paper: https://doi.org/10.1107/S0021889808016439