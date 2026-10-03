---
name: mwtab-file-parsing
description: Use when you have mwTab format files (Mass Spectrometry or Nuclear Magnetic
  Resonance experimental data from Metabolomics Workbench) that need to be loaded
  into Python for downstream analysis, validation, conversion to JSON, or programmatic
  manipulation of metadata and data sections.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mwtab
  - jsonschema
  - Python
  - pandas
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
evidence_spans:
- The ``mwtab`` package is a Python library that facilitates reading and writing files
  in
- jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema
- The ``mwtab`` package is a Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwtab_python_library_for_restful_access_cq
    doi: 10.3390/metabo11030163
    title: mwtab Python Library for RESTful Access
  dedup_kept_from: coll_mwtab_python_library_for_restful_access_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11030163
  all_source_dois:
  - 10.3390/metabo11030163
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mwtab-file-parsing

## Summary

Parse mwTab-formatted files into structured Python objects to extract metadata and tabular data sections for MS and NMR experiments. This skill enables programmatic access to mass spectrometry and nuclear magnetic resonance experimental data archived in the Metabolomics Workbench using the mwtab library.

## When to use

You have mwTab format files (Mass Spectrometry or Nuclear Magnetic Resonance experimental data from Metabolomics Workbench) that need to be loaded into Python for downstream analysis, validation, conversion to JSON, or programmatic manipulation of metadata and data sections.

## When NOT to use

- Input is already a JSON representation or equivalent structured object (use JSON direct ingestion instead)
- File is in NetCDF, mzML, or other non-mwTab metabolomics formats (use format-specific parsers)
- Task requires only metadata extraction without touching tabular data (consider lightweight regex parsing)

## Inputs

- mwTab-formatted text file (local path or remote ANALYSIS_ID)
- File handle or string path to .txt mwTab file
- ANALYSIS_ID string for remote Metabolomics Workbench fetch

## Outputs

- MWTabFile instance (generator-yielded or list collected)
- Dictionary of named data blocks (metadata and tabular sections)
- Structured metadata (STUDY_ID, ANALYSIS_ID, SOURCE, instrument parameters)
- Tabular data sections (accessible via block keys and pandas conversion)

## How to apply

Use the mwtab library's MWTabFile parser to load mwTab files, either from local disk or by ANALYSIS_ID from the Metabolomics Workbench remote service. The parser yields MWTabFile instances that provide dictionary-like access to named data blocks (metadata sections and tabular data). Extract study identifiers (STUDY_ID, ANALYSIS_ID), source metadata, and tabular blocks by iterating over the generator or accessing keys on each instance. The parser handles the mwTab text format specification internally, normalizing metadata key–value pairs and structuring tabular sections for downstream access via pandas DataFrames or direct inspection.

## Related tools

- **mwtab** (Core library for reading, writing, and parsing mwTab format files into Python MWTabFile objects) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **jsonschema** (Validates parsed mwTab data against JSON schema definitions after file parsing, enabling conformance checking)
- **pandas** (Converts mwTab tabular data sections into DataFrames for analysis and manipulation)

## Examples

```
import mwtab
for mwfile in mwtab.read_files("1", "2"):
    print("STUDY_ID:", mwfile.study_id)
    print("ANALYSIS_ID:", mwfile.analysis_id)
    print("Blocks:", list(mwfile.keys()))
```

## Evaluation signals

- MWTabFile instance is successfully created without parse errors or exceptions
- STUDY_ID and ANALYSIS_ID are non-null and match expected identifiers from input file or remote source
- Named blocks (keys) from mwTab file are accessible via dict-like interface on MWTabFile instance
- Metadata key–value pairs are correctly normalized and present in extracted metadata dictionary
- Tabular data sections (e.g., Sample data, Raw data) can be retrieved and have expected column counts

## Limitations

- Parser assumes valid mwTab format syntax; malformed files will raise exceptions and require manual repair
- Remote fetch via ANALYSIS_ID requires network access to Metabolomics Workbench API and valid credentials if applicable
- Large mwTab files with many samples or high-dimensional raw data may consume significant memory when fully loaded into memory

## Evidence

- [readme] The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear Magnetic Resonance (NMR) experimental data.: "The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear"
- [other] Create the :class:`~mwtab.mwtab.MWTabFile` generator function that will generate (yield) a single :class:`~mwtab.mwtab.MWTabFile` instance at a time.: "Create the :class:`~mwtab.mwtab.MWTabFile` generator function that will generate (yield) a single :class:`~mwtab.mwtab.MWTabFile` instance at a time."
- [other] Process each :class:`~mwtab.mwtab.MWTabFile` instance: Process ``mwTab`` files in a for-loop, one file at a time.: "Process each :class:`~mwtab.mwtab.MWTabFile` instance: Process ``mwTab`` files in a for-loop, one file at a time."
- [readme] As a library for accessing and manipulating data stored in ``mwTab`` format files.: "As a library for accessing and manipulating data stored in ``mwTab`` format files."
- [readme] Here we use ANALYSIS_ID of file to fetch data from URL: "Here we use ANALYSIS_ID of file to fetch data from URL"
