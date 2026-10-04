---
name: optimade-python-tools
description: Tools for implementing and consuming OPTIMADE APIs in Python. Use when querying materials databases, implementing OPTIMADE-compliant APIs, or converting between materials data formats.
metadata:
    skill-author: MindSpore Science Team
---

## Overview

OPTIMADE Python Tools is a library for implementing and consuming OPTIMADE APIs in Python. It enables interoperability among materials databases through a unified query interface, developed by the OPTIMADE consortium. The library provides Pydantic models, filter parsers, adapters for pymatgen/ASE/CIF conversion, and server implementations.

# OPTIMADE Python Tools

Library for implementing and consuming OPTIMADE APIs. Enables interoperability among materials databases through unified query interface. Developed by the OPTIMADE consortium.

## Installation

```bash
pip install optimade
```

From source:
```bash
git clone https://github.com/Materials-Consortia/optimade-python-tools
pip install .
```

## Quick Start

### Client Usage

```python
from optimade.client import OptimadeClient

# Query multiple providers
client = OptimadeClient()
results = client.get_structures(filter='elements HAS ALL "Si","O"')

# Command-line tool
optimade-get --filter 'elements HAS "Si"' --providers mp,odbx
```

### Data Conversion

```python
from optimade.adapters import Structure

# Convert to pymatgen/ASE/CIF
optimade_structure = Structure(entry)
pmg_struct = optimade_structure.to_pymatgen()
ase_atoms = optimade_structure.to_ase()
cif_string = optimade_structure.to_cif()
```

# When to Use This Skill

- Querying multiple materials databases with a unified API
- Converting materials data between pymatgen, ASE, and CIF formats
- Implementing an OPTIMADE-compliant API server
- Validating OPTIMADE implementations
- Accessing Materials Project, COD, OQMD, and other databases uniformly
- Building materials data aggregation tools
- Developing materials discovery applications
- Creating custom OPTIMADE providers

# Key Features

- **Pydantic Models**: All OPTIMADE entry types and responses
- **Filter Parser**: Lark-based EBNF grammar for filter language
- **Adapters**: pymatgen, ASE, CIF conversion
- **Server**: MongoDB/Elasticsearch backends
- **Validator**: `optimade-validator` tool

# API Examples

## Basic Structure Queries

```python
from optimade.client import OptimadeClient

client = OptimadeClient()

# Query by elements
results = client.get_structures(filter='elements HAS ALL "Fe","O"')

# Query by formula
results = client.get_structures(filter='chemical_formula="Fe2O3"')

# Query by property
results = client.get_structures(filter='nsites < 100')

# Complex filter
results = client.get_structures(
    filter='elements HAS ALL "Ti","O" AND nsites < 50'
)
```

## Provider-Specific Queries

```python
from optimade.client import OptimadeClient

client = OptimadeClient()

# Query specific providers
results = client.get_structures(
    filter='elements HAS "Cu"',
    providers=["mp", "odbx"]  # Materials Project, odbx
)

# Get available providers
providers = client.list_providers()
```

## Data Format Conversion

```python
from optimade.adapters import Structure

# From OPTIMADE entry to various formats
structure = Structure(optimade_entry)

# Convert to pymatgen
pmg_structure = structure.to_pymatgen()

# Convert to ASE Atoms
ase_atoms = structure.to_ase()

# Convert to CIF string
cif_str = structure.to_cif()

# Convert to JSON string
json_str = structure.to_json()
```

## Server Implementation

```python
from fastapi import FastAPI
from optimade.server.main import app

# Run the reference server
# $ uvicorn optimade.server.main:app --reload

# Custom configuration
from optimade.server.config import CONFIG
CONFIG.mongo_database = "my_database"
CONFIG.collection_name = "structures"
```

## Validator Usage

```bash
# Validate an OPTIMADE provider
optimade-validator https://materialsproject.org/optimade

# Validate with specific version
optimade-validator --version 1.2.0 https://example.com/optimade
```

## Filter Examples

```python
# Filter syntax examples

# Element containment
'elements HAS "Si"'
'elements HAS ALL "Si","O"'
'elements HAS ANY "Fe","Co","Ni"'

# Numeric comparisons
'nsites < 100'
'nsites >= 50 AND nsites <= 200'

# String matching
'chemical_formula = "H2O"'
'chemical_formula CONTAINS "Fe"'

# Combined filters
'elements HAS "Fe" AND nsites < 50'
'chemical_formula CONTAINS "O" OR chemical_formula CONTAINS "N"'
```

# Common Use Cases

- Querying multiple materials databases uniformly
- Implementing OPTIMADE-compliant APIs
- Converting materials data between formats
- Validating OPTIMADE implementations

# Best Practices

- Always specify providers when querying to reduce load
- Use pagination for large result sets
- Cache results locally when doing repeated queries
- Validate your filter syntax before complex queries
- Use `client.count()` to estimate result size before full query
- Handle rate limiting for provider APIs

```python
# Pagination example
from optimade.client import OptimadeClient

client = OptimadeClient()
page = client.get_structures_page(
    filter='elements HAS "Fe"',
    page_limit=100,
    page_number=1
)

# Get total count
count = client.count_structures(filter='elements HAS "Fe"')
```

# Troubleshooting

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Provider timeout | Slow API response | Increase timeout or retry |
| Invalid filter | Syntax error | Use filter validator |
| No results | Filter too restrictive | Relax filter conditions |
| Import errors | Missing adapter | Install optional deps: `pip install optimade[pymatgen]` |
| Version mismatch | API version incompatible | Check `optimade` package version |

## Filter Debugging

```python
from optimade.filterparser import LarkParser

parser = LarkParser()
try:
    tree = parser.parse('elements HAS "Si"')
    print(tree.pretty())
except Exception as e:
    print(f"Filter error: {e}")
```

## Provider Issues

```python
# Check provider availability
from optimade.client import OptimadeClient

client = OptimadeClient()
providers = client.list_providers()

for p in providers:
    try:
        client.get_structures_page(filter='nsites > 0', providers=[p])
        print(f"{p}: OK")
    except Exception as e:
        print(f"{p}: Error - {e}")
```

# Supported OPTIMADE Versions

| OPTIMADE API Version | `optimade` Package Requirement |
|---------------------|-------------------------------|
| v1.0.0 | `optimade<=0.12.9` |
| v1.1.0 | `optimade>=0.16,<1.2` |
| v1.2.0 | `optimade>=1.2.0` |

# Metadata

| Property | Value |
|----------|-------|
| License | MIT |
| Language | Python 3.8+ |
| Maintainer | OPTIMADE Consortium |
| Dependencies | pydantic, lark, fastapi |
| Backends | MongoDB, Elasticsearch |

# Resources

- GitHub: https://github.com/Materials-Consortia/optimade-python-tools
- Docs: https://optimade.org/optimade-python-tools
- Paper: Evans et al., JOSS 6(65), 3458 (2021)
- Citation: Evans et al., Digital Discovery, 3, 1509-1533 (2024)