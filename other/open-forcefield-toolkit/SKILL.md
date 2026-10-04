---
name: open-forcefield-toolkit
description: Use when developing molecular mechanics force fields, implementing SMIRNOFF force field format, or building interoperable molecular simulation workflows.
metadata:
    skill-author: MindSpore Science Team
---

## When to Use This Skill

Use this skill when:
- Developing molecular mechanics force fields
- Applying SMIRNOFF force fields to molecular systems
- Building interoperable molecular simulation workflows
- Converting between force field formats (AMBER, GROMACS, LAMMPS)
- Parameterizing molecules for MD simulations
- Fitting force field parameters to QM data

## Overview

The Open Forcefield Toolkit provides specifications and tools for encoding molecular mechanics force fields. The SMIRNOFF format enables portable, extensible force field definitions.

## Format Specification

- **Format**: XML with hierarchical structure
- **Pattern Matching**: SMIRKS for atom typing
- **Parameters**: Bonds, angles, torsions, impropers, vdW, electrostatics
- **Inheritance**: Force field extension via parent references
- **Versioning**: Explicit version in header

## Key Elements

| Element | Description |
|---------|-------------|
| `<ForceField>` | Root element |
| `<vdW>` | Lennard-Jones parameters |
| `<Bonds>` | Bond stretch terms |
| `<Angles>` | Angle bend terms |
| `<ProperTorsions>` | Dihedral terms |
| `<ImproperTorsions>` | Out-of-plane terms |
| `<Electrostatics>` | Charge method |
| `<ToolkitAM1BCC>` | AM1-BCC charges |

## Example Snippet

```xml
<ForceField name="openff-2.0.0" version="2.0">
  <vdW potential="Lennard-Jones-12-6">
    <Atom smirks="[#6:1]" sigma="0.33996695" epsilon="0.359824"/>
    <Atom smirks="[#1:1]-[#6]" sigma="0.260362" epsilon="0.065688"/>
  </vdW>
  <Bonds potential="harmonic">
    <Bond smirks="[#6:1]-[#6:2]" k="437.233" length="0.1529"/>
  </Bonds>
  <ProperTorsions potential="k torsion">
    <Proper smirks="[*:1]-[#6:2]-[#6:3]-[*:4]"
            k1="0.0" periodicity1="1" phase1="0.0"/>
  </ProperTorsions>
</ForceField>
```

## Force Field Specification

The SMIRNOFF (SMIRKS Native Open Force Field) format uses SMIRKS patterns for atom typing:

### SMIRKS Pattern Matching

| Pattern | Matches |
|---------|---------|
| `[#6:1]` | Any carbon |
| `[#6:1]=[#8]` | Carbonyl carbon |
| `[#7:1](-[#1])(-[#1])` | Primary amine nitrogen |
| `[#6:1](-[#7])(-[#8])` | Carbon bonded to N and O |
| `[*:1]-[#6:2]-[*:3]` | Any central carbon bond |

### Force Field Sections

| Section | Description | Parameters |
|---------|-------------|------------|
| `<vdW>` | van der Waals | sigma, epsilon |
| `<Bonds>` | Bond stretching | k, length |
| `<Angles>` | Angle bending | k, angle |
| `<ProperTorsions>` | Dihedral rotation | k, periodicity, phase |
| `<ImproperTorsions>` | Out-of-plane | k, periodicity, phase |
| `<Electrostatics>` | Charge method | method, scale |
| `<LibraryCharges>` | Fixed charges | charge |
| `<ToolkitAM1BCC>` | AM1-BCC charges | - |

## Tools

| Tool | Purpose |
|------|---------|
| openff-toolkit | Core Python package |
| openff-forcefields | Force field files |
| openff-interchange | System export |
| forcebalance | Force field fitting |
| smirnoff-plugins | Custom handlers |

## Usage Examples

### Apply Force Field to Molecule

```python
from openff.toolkit.topology import Molecule, Topology
from openff.toolkit.typing.engines.smirnoff import ForceField

# Load molecule from SMILES
molecule = Molecule.from_smiles("CCO")

# Load force field
forcefield = ForceField("openff-2.0.0.offxml")

# Create topology
topology = molecule.to_topology()

# Parameterize
interchange = forcefield.create_interchange(topology)

# Get system for simulation
system = interchange.to_openmm_system()
```

### Create Molecule from File

```python
from openff.toolkit.topology import Molecule

# From SDF file
molecule = Molecule.from_file("molecule.sdf")

# From PDB (with connectivity)
molecule = Molecule.from_pdb("protein.pdb")

# From SMILES with 3D geometry
molecule = Molecule.from_smiles("c1ccccc1")
molecule.generate_conformers(n_conformers=1)
```

### Export to MD Formats

```python
from openff.interchange import Interchange
from openff.toolkit.topology import Molecule
from openff.toolkit.typing.engines.smirnoff import ForceField

# Create parameterized system
molecule = Molecule.from_smiles("CCCC")
molecule.generate_conformers()
forcefield = ForceField("openff-2.0.0.offxml")
interchange = forcefield.create_interchange(molecule.to_topology())

# Export to GROMACS
interchange.to_gromacs("butane")

# Export to LAMMPS
interchange.to_lammps("butane")

# Export to AMBER
interchange.to_amber("butane")
```

### Inspect Force Field Parameters

```python
from openff.toolkit.typing.engines.smirnoff import ForceField

ff = ForceField("openff-2.0.0.offxml")

# List vdW parameters
for param in ff["vdW"]:
    print(f"SMIRKS: {param.smirks}")
    print(f"  sigma: {param.sigma}")
    print(f"  epsilon: {param.epsilon}")

# Get parameter for specific atom
molecule = Molecule.from_smiles("CCO")
labels = ff.label_molecules(molecule.to_topology())[0]

for atom_idx, atom_label in labels["vdW"].items():
    print(f"Atom {atom_idx}: {atom_label}")
```

### Create Custom Force Field

```python
from openff.toolkit.typing.engines.smirnoff import ForceField

# Start from existing
ff = ForceField("openff-2.0.0.offxml")

# Add custom parameter
ff["vdW"].add_parameter({
    "smirks": "[#6:1]-[#8]",
    "sigma": "0.35*angstrom",
    "epsilon": "0.3*kilocalorie/mole"
})

# Save custom force field
ff.to_file("custom-forcefield.offxml")
```

### Partial Charge Assignment

```python
from openff.toolkit.topology import Molecule
from openff.toolkit.typing.engines.smirnoff import ForceField

molecule = Molecule.from_smiles("CCO")

# AM1-BCC charges (default)
molecule.assign_partial_charges(partial_charge_method="am1bcc")

# Other methods
molecule.assign_partial_charges(partial_charge_method="mmff94")
molecule.assign_partial_charges(partial_charge_method="gasteiger")

# Access charges
for atom, charge in zip(molecule.atoms, molecule.partial_charges):
    print(f"{atom.symbol}: {charge}")
```

## Resources

- Website: https://openforcefield.org
- Docs: https://open-forcefield-toolkit.readthedocs.io