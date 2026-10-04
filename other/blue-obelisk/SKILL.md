---
name: blue-obelisk
description: Use when implementing open data standards in chemistry/materials science, ensuring reproducibility through open source tools, or establishing interoperability between computational chemistry software.
metadata:
    skill-author: MindSpore Science Team
---

## Overview

The Blue Obelisk is a movement promoting open data, open source software, and open standards in computational chemistry and materials science. It fosters collaboration and reproducibility across the community.

## Format Specification

- **Open Standards**: Community-developed file formats and APIs
- **Algorithm Dictionary**: Standardized algorithm definitions
- **Data Dictionary**: Common data types and structures
- **License**: Open licenses for all outputs
- **Versioning**: Stable, versioned releases

## Key Standards

| Standard | Description |
|----------|-------------|
| InChI | IUPAC International Chemical Identifier |
| CML | Chemical Markup Language |
| CDK Notation | Canonical SMILES extensions |
| BO Algorithm Dictionary | Standard algorithm descriptions |
| BO Data Dictionary | Common data type definitions |

## Example Algorithm Entry

```xml
<entry id="bo:charge-gasteiger" term="Gasteiger Charges">
  <definition>
    Iterative partial equalization of orbital electronegativity
  </definition>
  <relatedEntry type="is-a" term="partial charge method"/>
  <isClassifiedAs>
    <Descriptor value="iterative"/>
    <Descriptor value="empirical"/>
  </isClassifiedAs>
</entry>
```

## Example Data Dictionary Entry

```xml
<entry id="bo:bond-order" term="Bond Order">
  <definition>
    The bond order between two atoms, as a floating point number
  </definition>
  <dataType>float</dataType>
  <units>dimensionless</units>
  <relatedEntry type="is-a" term="bond property"/>
</entry>
```

## Tools

| Tool | Purpose |
|------|---------|
| OpenBabel | Format conversion hub |
| RDKit | Cheminformatics toolkit |
| CDK | Chemistry Development Kit |
| Avogadro | Molecular editor |
| JChemPaint | Structure drawing |

## Resources

- Website: https://blueobelisk.github.io
- Dictionary: https://github.com/blueobelisk/dictionary