---
name: smiles-sdf-parsing
description: Use when you have a natural product molecule or compound library provided
  as SMILES strings, InChI strings, or SDF files, and you need to convert them into
  an in-memory molecular representation (RDKit Mol object) suitable for fingerprinting,
  property prediction, or other cheminformatic operations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2814
  tools:
  - pip
  - RDKit
  - biosynfoni
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
evidence_spans:
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni_2_cq
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES/SDF Parsing

## Summary

Parse molecular structure representations in SMILES or SDF format and load them into an RDKit molecule object for downstream cheminformatic analysis. This is a foundational step for any workflow that accepts chemical structure input and needs to operate on molecular graphs.

## When to use

You have a natural product molecule or compound library provided as SMILES strings, InChI strings, or SDF files, and you need to convert them into an in-memory molecular representation (RDKit Mol object) suitable for fingerprinting, property prediction, or other cheminformatic operations.

## When NOT to use

- Input is already an RDKit Mol object or other in-memory molecular representation.
- You are working with protein sequences or genomic data rather than small-molecule chemistry.
- The molecular structure is malformed or incomplete and cannot be unambiguously interpreted as a valid chemical graph.

## Inputs

- SMILES string
- InChI string
- SDF file
- Molecule structure in chemical format

## Outputs

- RDKit Mol object
- Molecule supplier iterator (for SDF input)

## How to apply

Use RDKit's Chem module to parse the input: call Chem.MolFromSmiles() for SMILES strings or Chem.MolFromInchi() for InChI strings to produce a Mol object. For SDF files, use Chem.SDMolSupplier() to iterate over all molecules in the file. Validate that the returned Mol object is not None before proceeding; a None return indicates the parser could not interpret the structure and the input should be checked for formatting errors or chemical validity.

## Related tools

- **RDKit** (Parses SMILES, InChI, and SDF strings/files into Mol objects for cheminformatic operations) — https://www.rdkit.org
- **biosynfoni** (Accepts RDKit Mol objects parsed from SMILES/SDF and computes biosynformatic fingerprints) — https://github.com/lucinamay/biosynfoni

## Examples

```
from rdkit import Chem
smi = 'CCO'
mol = Chem.MolFromSmiles(smi)
print(mol.GetNumAtoms())
```

## Evaluation signals

- Returned RDKit Mol object is not None and has a valid atomic connectivity graph.
- Mol object has correct atom count, bond types, and stereochemistry matching the input structure.
- When iterated over an SDF file, all molecules are successfully parsed without errors.
- Round-trip conversion (SMILES → Mol → SMILES) produces chemically equivalent structures.
- No warnings or exceptions are raised during parsing of chemically valid input.

## Limitations

- Parser will return None if the input SMILES or InChI string is malformed or represents an invalid chemical structure.
- SDF files may contain metadata or properties that are not automatically extracted into the Mol object; use GetProp() or other RDKit accessors to retrieve them.
- Some stereochemical and charge specifications may be ambiguous in SMILES and require explicit annotation or validation against expected chemical rules.
- Large SDF files may require streaming (SDMolSupplier with lazy loading) to avoid memory exhaustion.

## Evidence

- [readme] Convert a SMILES string to a fingerprint: from biosynfoni import Biosynfoni from rdkit import Chem smi = <SMILES> mol = Chem.MolFromSmiles(smi): "mol = Chem.MolFromSmiles(smi)"
- [readme] Create a fingerprint from a SMILES string: biosynfoni <SMILES> Create a fingerprint from an InChI string: biosynfoni <InChI> Write the fingerprints of all molecules in an SDF file to a CSV file: biosynfoni <molecule_supplier.sdf>: "Create a fingerprint from a SMILES string: biosynfoni <SMILES> Create a fingerprint from an InChI string: biosynfoni <InChI> Write the fingerprints of all molecules in an SDF file to a CSV file:"
- [other] Load a natural-product molecule structure from SMILES or SDF input using the biosynfoni API.: "Load a natural-product molecule structure from SMILES or SDF input using the biosynfoni API"
