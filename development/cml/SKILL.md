---
name: cml
description: Use when exchanging molecular data between tools, encoding reactions and spectra, or building interoperable chemistry workflows.
metadata:
    skill-author: MindSpore Science Team
---

## When to Use This Skill

Use this skill when:
- Exchanging molecular data between different chemistry software
- Encoding chemical reactions with stoichiometry and conditions
- Representing spectroscopic data (NMR, IR, MS)
- Building interoperable chemistry workflows
- Archiving computational chemistry results
- Creating machine-readable chemical documents

## Overview

Chemical Markup Language (CML) is an XML-based standard for representing molecules, compounds, reactions, spectra, and crystals. It provides a flexible, extensible framework for chemical data exchange.

## Format Specification

- **Encoding**: XML with namespaces
- **Namespace**: `http://www.xml-cml.org/schema`
- **Schema**: Modular XSD definitions
- **Conventions**: Standard attribute sets for coordinates, bonding
- **Validation**: XSD schema validation supported

## Key Elements

| Element | Description |
|---------|-------------|
| `<molecule>` | Root for molecular data |
| `<atomArray>` | Container for atoms |
| `<atom>` | Individual atom with id, elementType, x3, y3, z3 |
| `<bondArray>` | Container for bonds |
| `<bond>` | Bond with atomRefs2, order |
| `<crystal>` | Unit cell and symmetry |
| `<spectrum>` | Spectroscopic data |
| `<reaction>` | Chemical reaction data |
| `<property>` | Observable properties |

## Example Snippet

```xml
<molecule xmlns="http://www.xml-cml.org/schema" id="water">
  <atomArray>
    <atom id="O1" elementType="O" x3="0.0" y3="0.0" z3="0.117"/>
    <atom id="H1" elementType="H" x3="0.0" y3="0.757" z3="-0.469"/>
    <atom id="H2" elementType="H" x3="0.0" y3="-0.757" z3="-0.469"/>
  </atomArray>
  <bondArray>
    <bond atomRefs2="O1 H1" order="1"/>
    <bond atomRefs2="O1 H2" order="1"/>
  </bondArray>
</molecule>
```

## Tools Using CML

| Tool | Purpose |
|------|---------|
| OpenBabel | Conversion to/from CML, format interoperability |
| CDK (Chemistry Development Kit) | Java chemistry toolkit with CML support |
| CMLDOM | DOM-based CML parser |
| JUMBO | Java CML toolkit |
| JChemPaint | Chemical structure editor (CML-native) |
| JSpecView | Spectroscopy viewer (CML spectra) |
| Bioclipse | Integrated bio/chem platform |
| ODDT | Open drug discovery toolkit |
| PyBEL | OpenBabel Python interface |

## Usage Examples

### Create CML Molecule

```python
from openbabel import openbabel as ob

# Create molecule
mol = ob.OBMol()
mol.NewAtom()
mol.NewAtom()
mol.GetAtom(1).SetAtomicNum(8)  # Oxygen
mol.GetAtom(2).SetAtomicNum(1)  # Hydrogen

# Convert to CML
conv = ob.OBConversion()
conv.SetOutFormat("cml")
cml_output = conv.WriteString(mol)
print(cml_output)
```

### Parse CML with CDK (Java)

```java
import org.openscience.cdk.interfaces.IChemFile;
import org.openscience.cdk.io.CMLReader;

CMLReader reader = new CMLReader(new FileReader("molecule.cml"));
IChemFile chemFile = reader.read(new ChemFile());
IAtomContainer molecule = chemFile.getChemSequence(0)
                                 .getChemModel(0)
                                 .getMoleculeSet()
                                 .getAtomContainer(0);
```

### CML Reaction

```xml
<cml xmlns="http://www.xml-cml.org/schema">
  <reaction id="r1">
    <reactantList>
      <molecule id="H2">
        <atomArray>
          <atom id="H1" elementType="H"/>
          <atom id="H2" elementType="H"/>
        </atomArray>
        <bondArray>
          <bond atomRefs2="H1 H2" order="1"/>
        </bondArray>
      </molecule>
    </reactantList>
    <productList>
      <molecule id="H2O">
        <!-- water structure -->
      </molecule>
    </productList>
    <propertyList>
      <property dictRef="reaction:enthalpy">
        <scalar>-286 kJ/mol</scalar>
      </property>
    </propertyList>
  </reaction>
</cml>
```

## Resources

- Website: http://www.xml-cml.org