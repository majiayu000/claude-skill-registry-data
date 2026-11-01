---
name: smiles-notation-parsing
description: Use when when processing downloaded mass spectral libraries (particularly MoNA EI or MS2 libraries) where SMILES information exists but is embedded in unstructured Comment fields rather than a dedicated SMILES field, or when assigning SMILES from external structure databases (SDF files) to library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3370
  tools:
  - mspcompiler
  - R
  - MoNA
  - ChemmineR
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- The MassBank of North America (MoNA) has an EI library available
- The MoNA MS2 libraries can be downloaded from https://mona.fiehnlab.ucdavis.edu/downloads
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler
schema_version: 0.2.0
---

# SMILES Notation Parsing

## Summary

Extract and standardize SMILES (Simplified Molecular Input Line Entry System) strings from mass spectral library records, typically sourced from Comment fields or structure databases. This skill reorganizes molecular structure information into a dedicated SMILES field required by downstream mass spectral analysis pipelines.

## When to use

When processing downloaded mass spectral libraries (particularly MoNA EI or MS2 libraries) where SMILES information exists but is embedded in unstructured Comment fields rather than a dedicated SMILES field, or when assigning SMILES from external structure databases (SDF files) to library records that lack molecular structure annotation.

## When NOT to use

- Library records already have SMILES in a dedicated SMILES field and the field is validated; use this skill only if SMILES is missing or incorrectly structured.
- Input file format is not MSP (e.g., MGF format for GNPS requires different parsing; use complete_mgf() instead).
- SMILES information is not available in any form (Comment field, MOL files, or external structure database); the library cannot be augmented with structure data.

## Inputs

- MSP file (EI or MS2 library format) with embedded or missing SMILES
- SDF file (structure database from combined MOL files)
- Structure annotation table (text file output from extract_structure)

## Outputs

- R list object representing the mass spectral library with SMILES field populated
- Updated library object ready for downstream processing (polarity separation, RI assignment, output writing)

## How to apply

Load the msp library file into R using read_lib() with the appropriate type parameter (type='EI' or type='MS2'). If SMILES is embedded in the Comment field (as in MoNA libraries), apply reorganize_mona() to extract SMILES strings and populate them into the dedicated SMILES field. Alternatively, if SMILES must be derived from structure files, first extract structures from MOL or SDF files using extract_structure(), then use assign_smiles() with a matching strategy (match='name' for name-based matching, or match='inchikey' on Linux/Mac when InChIKey is available) to populate SMILES fields. Verify that the output object contains a populated SMILES field and that record counts match the input library.

## Related tools

- **mspcompiler** (Core R package providing reorganize_mona(), assign_smiles(), extract_structure(), and related functions for SMILES parsing and library reorganization) — https://github.com/QizhiSu/mspcompiler
- **ChemmineR** (Bioconductor package used by mspcompiler for structure matching and SMILES manipulation)
- **R** (Runtime environment for executing mspcompiler functions and library manipulation)

## Examples

```
mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type = "EI"); mona_ei <- reorganize_mona(mona_ei)
```

## Evaluation signals

- Output library object contains a non-empty SMILES field for all or most records (check with summary() or length(unique(library$SMILES)))
- Record count (nrow or list length) is identical before and after SMILES parsing, confirming no records were dropped
- SMILES strings follow valid SMILES syntax (e.g., start with element symbols, contain valid bond/ring notations)
- For reorganize_mona(): SMILES values match the structure originally in the Comment field (spot-check a subset of records)
- For assign_smiles(): SMILES assignments correspond to the correct compound name/InChIKey, verified by comparing library$Name with structure annotation table

## Limitations

- reorganize_mona() is specific to MoNA library format; other library sources (NIST, RIKEN) may require different parsing logic or external structure enrichment via assign_smiles().
- assign_smiles() matching accuracy depends on the chosen strategy: match='name' can fail if compound names differ between library and structure file; match='inchikey' is more robust but requires InChIKey presence in both sources.
- Large SDF files (hundreds of thousands of MOL records) can be time-consuming to process; parallel computing is recommended but requires additional setup (future, future.apply, parallel packages).
- SMILES extraction from Comment fields is text-based and may fail if Comment field format is non-standard or SMILES strings are malformed in the source library.

## Evidence

- [readme] MoNA EI library SMILES extraction rationale: "This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field by the reorganize_mona function."
- [readme] reorganize_mona() function application: "mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type = "EI")
mona_ei <- reorganize_mona(mona_ei)"
- [readme] assign_smiles() matching strategy and rationale: "Assign SMILES to the library. If you are working with Linux-based or Mac OS, please use "match = "inchikey". nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = "name")"
- [other] SMILES field population task definition: "Apply reorganize_mona() function to extract SMILES information from the Comment field and populate the SMILES field in the library object."
- [other] Verification of SMILES parsing output: "Verify the output object contains the expected field structure (SMILES field populated) and that row count matches the input."
