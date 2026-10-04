---
name: cif
description: Use when working with crystallographic data, parsing structure files from databases, or implementing crystal structure visualization and analysis tools.
metadata:
    skill-author: MindSpore Science Team
---

## When to Use This Skill

Use this skill when:
- Parsing or generating CIF files from crystallographic databases (COD, ICSD, Materials Project)
- Validating crystal structure data for publication or submission
- Converting between CIF and other structure formats (POSCAR, XYZ, PDB)
- Extracting atomic coordinates, unit cell parameters, or symmetry information
- Implementing crystallographic software or visualization tools
- Processing Powder Diffraction File (PDF) data

## Overview

The Crystallographic Information File (CIF) is the IUCr standard for representing crystallographic information. It is the universal format for exchanging crystal structure data.

## Format Specification

- **Encoding**: ASCII text, case-insensitive tags
- **Structure**: Data blocks starting with `data_` declarations
- **Syntax**: Tag-value pairs, loops for tabular data
- **Comments**: Lines beginning with `#`
- **Strings**: Quoted with `'` or `"` or delimited by `;` for multiline

## Key Elements

| Element | Description |
|---------|-------------|
| `_cell_length_a/b/c` | Unit cell dimensions |
| `_cell_angle_alpha/beta/gamma` | Unit cell angles |
| `_atom_site_label` | Atom identifier |
| `_atom_site_fract_x/y/z` | Fractional coordinates |
| `_atom_site_occupancy` | Site occupancy factor |
| `_symmetry_equiv_pos_as_xyz` | Symmetry operations |
| `_atom_site_type_symbol` | Element symbol |

## Example Snippet

```cif
data_NaCl
_cell_length_a   5.6402
_cell_length_b   5.6402
_cell_length_c   5.6402
_cell_angle_alpha 90
_cell_angle_beta  90
_cell_angle_gamma 90
_space_group_name_H-M 'F m -3 m'

loop_
_atom_site_label
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
Na1  0.0000  0.0000  0.0000
Cl1  0.5000  0.5000  0.5000
```

## Format Validation Tools

| Tool | Purpose |
|------|---------|
| checkCIF | IUCr online validation service (https://checkcif.iucr.org/) |
| PLATON | Structure validation and analysis |
| Gemmi validate | Command-line validation |
| PyCIFRW validation | Programmatic validation |

## Tools

| Tool | Purpose |
|------|---------|
| PyCIFRW | Python parser/writer |
| Gemmi | C++ library with Python bindings |
| Cif2Cell | Convert to computational codes |
| checkCIF | IUCr validation service |
| pycifstar | Modern Python CIF library |

## Usage Examples

### Parse CIF with PyCIFRW

```python
from CifFile import ReadCif

# Read a CIF file
cif = ReadCif("structure.cif")

# Access data blocks
for block_name in cif.keys():
    block = cif[block_name]
    print(f"Block: {block_name}")

    # Get cell parameters
    a = block.get('_cell_length_a')
    b = block.get('_cell_length_b')
    c = block.get('_cell_length_c')
    print(f"Cell: {a} x {b} x {c}")

    # Get atom sites
    labels = block.get('_atom_site_label')
    x = block.get('_atom_site_fract_x')
    y = block.get('_atom_site_fract_y')
    z = block.get('_atom_site_fract_z')
```

### Parse CIF with Gemmi

```python
import gemmi

# Read CIF file
doc = gemmi.cif.read_file("structure.cif")
block = doc.sole_block()

# Extract unit cell
cell = gemmi.UnitCell()
cell.set_from_block(block)
print(f"Cell volume: {cell.volume}")

# Convert to structure
structure = gemmi.make_structure_from_block(block)
print(f"Formula: {structure[0].formula}")
```

### Write CIF File

```python
from CifFile import CifFile, CifBlock

# Create new CIF
cif = CifFile()
block = CifBlock("my_structure")

# Add cell parameters
block['_cell_length_a'] = '5.0'
block['_cell_length_b'] = '5.0'
block['_cell_length_c'] = '5.0'
block['_cell_angle_alpha'] = '90'
block['_cell_angle_beta'] = '90'
block['_cell_angle_gamma'] = '90'

# Add atom data using loops
block.AddLoopItem(('_atom_site_label', ['Si1', 'O1']))
block.AddLoopItem(('_atom_site_fract_x', ['0.0', '0.5']))

cif['my_structure'] = block
cif.write_file("output.cif")
```

## Resources

- Website: https://www.iucr.org/resources/cif