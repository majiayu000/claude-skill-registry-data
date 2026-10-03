---
name: output-grounding
description: Use when when developing or extending mass spectrometry data processing workflows (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
  tools:
  - OpenMS
  - KNIME
  - Python
  - GitHub
  - pyOpenMS
  - TOPPView
  - nextflow
  - Galaxy
  - MZmine 2
  - mzmine2
  - MZmine
  - mzmine
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - ZODIAC
derived_from:
- doi: 10.1074/mcp.M113.031278
  title: featurefindermetab
- doi: 10.1186/1471-2105-11-395
  title: ''
- doi: 10.1038/s41592-019-0344-8
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bindiscover
    doi: 10.1186/s13321-023-00734-8
    title: bindiscover
  - build: coll_featurefindermetab
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_mzmine2
    doi: 10.1186/1471-2105-11-395
    title: mzmine2
  - build: coll_sirius
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  dedup_kept_from: coll_featurefindermetab
schema_version: 0.2.0
---

# output_grounding

## Summary

Validate and document the origin, format, and reproducibility of computational outputs by grounding them in standardized file formats, version-controlled source code, and documented parameter provenance. This skill ensures that mass spectrometry data processing pipelines produce outputs traceable to specific tool versions and input configurations.

## When to use

When developing or extending mass spectrometry data processing workflows (e.g., proteomics quantitation, metabolomics identification) where outputs must be reproducible across platforms and versions, or when integrating OpenMS tools into orchestration engines (KNIME, Galaxy, nextflow, TOPPAS) that require unified parameter handling and schema validation.

## When NOT to use

- When input data is already in a proprietary binary format with no open conversion path to PSI standards.
- When the analysis requires custom algorithmic modifications not yet exposed through the unified CTD or Python API.
- When integrating non-OpenMS tools that do not support standardized parameter interchange or output schema validation.

## Inputs

- Raw LC-MS data files (mzML, mzXML formats)
- Parameter configuration (CTD scheme or command-line arguments)
- Tool version identifier
- Input dataset metadata (e.g., quantitation protocol: label-free, SILAC, iTRAQ, TMT, SRM, SWATH)

## Outputs

- Standardized output files (mzML, mzXML, mzIdentXML, pepXML, mzTab)
- Tool provenance metadata (version, parameters used, timestamp)
- Unit and functional test results
- Workflow definition (compatible with KNIME, Galaxy, nextflow, TOPPAS)
- Python bindings documentation (pyOpenMS API reference)

## How to apply

Ground outputs in OpenMS's Common Tool Description (CTD) scheme to document tool versions, input parameters, and expected output formats (mzML, mzXML, mzIdentXML, pepXML, mzTab, etc.). Verify that Python bindings (pyOpenMS) expose the same API surface as the C++ core, ensuring parameter consistency across language boundaries. Establish coding conventions and unit/functional test coverage for any new data processing step before integrating into workflow engines; validate that output schemas conform to Proteomics Standards Initiative (PSI) formats. Use version control (GitHub) to track parameter changes and enable reproducibility across different machine configurations (Windows, macOS, Linux).

## Related tools

- **OpenMS** (Core C++ library providing 150+ TOPP Tools for LC-MS data processing and standardized CTD parameter schema) — https://github.com/OpenMS/OpenMS
- **pyOpenMS** (Python bindings to the OpenMS C++ API for rapid algorithm development and parameter consistency validation)
- **KNIME** (Workflow orchestration engine that integrates OpenMS TOPP Tools via unified parameter handling)
- **TOPPView** (Visualization tool (1D, 2D, 3D) for validating processed LC-MS outputs)
- **nextflow** (Pipeline engine for integrating OpenMS TOPP Tools with version-tracked parameter definitions)
- **Galaxy** (Workflow platform supporting OpenMS tool integration via CTD-based parameter exchange)

## Evaluation signals

- Output files conform to PSI formats (mzML, mzIdentXML, mzTab) and validate against schema validators.
- CTD parameter definitions match the actual command-line arguments and Python API signatures used; no parameter mismatches across C++/Python.
- Unit tests and functional tests pass for all pre-processing, identification, and quantitation workflows on test datasets.
- Outputs from the same input data are byte-identical (or numerically equivalent within machine precision) when run on different platforms (Windows, macOS, Linux) with the same tool version.
- Workflow definition (KNIME, Galaxy, nextflow) executes successfully and produces outputs with the same file format and structure as documented in README.

## Limitations

- No changelog found in the provided documentation, making it difficult to track parameter or output schema changes across versions.
- The finding regarding severity assignment was unconfirmed by expert review, indicating potential gaps in automated validation of output provenance.
- Python bindings are partial (not all of the C++ API is exposed); outputs from purely Python workflows may not be grounded to the same level as C++ equivalents.
- Output format validation depends on external PSI standards; changes to those standards require corresponding updates to CTD definitions and tests.

## Evidence

- [readme] It comes with a vast variety of pre-built and ready-to-use tools for proteomics and metabolomics data analysis (TOPPTools) as well as powerful 1D, 2D and 3D visualization (TOPPView).: "It comes with a vast variety of pre-built and ready-to-use tools for proteomics and metabolomics data analysis (TOPPTools) as well as powerful 1D, 2D and 3D visualization (TOPPView)."
- [readme] OpenMS supports the Proteomics Standard Initiative (PSI) formats for MS data.: "OpenMS supports the Proteomics Standard Initiative (PSI) formats for MS data."
- [readme] It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept and a unified parameter handling via a 'common tool description' (CTD) scheme.: "It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept and a unified parameter handling via a 'common tool"
- [readme] With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development.: "With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development."
- [methods] have [unit tests and functional tests]: "have [unit tests and functional tests]"
- [methods] have [proper documentation]: "have [proper documentation]"
