---
name: workflow-reconstruction
description: Use when when you have a partially documented or undocumented MS analysis pipeline and need to verify its correctness, trace data provenance through multiple processing stages, integrate tools via unified parameter handling (CTD scheme), or ensure the workflow adheres to community standards for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - OpenMS
  - KNIME
  - Python
  - GitHub
  - Galaxy
  - nextflow
  - TOPPAS
  - pyOpenMS
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  - MSNovelist
  - ZODIAC
derived_from:
- doi: 10.1074/mcp.M113.031278
  title: featurefindermetab
- doi: 10.1038/s41592-019-0344-8
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_featurefindermetab
    doi: 10.1074/mcp.M113.031278
    title: featurefindermetab
  - build: coll_sirius
    doi: 10.1038/s41592-019-0344-8
    title: sirius
  dedup_kept_from: coll_featurefindermetab
schema_version: 0.2.0
---

# Workflow Reconstruction

## Summary

Reconstruct and validate mass spectrometry analysis workflows by identifying tool chains, parameter flows, and data transformations across proteomics and metabolomics pipelines. This skill ensures reproducibility by documenting how raw LC-MS data flows through integrated tools like OpenMS, KNIME, and Galaxy.

## When to use

When you have a partially documented or undocumented MS analysis pipeline and need to verify its correctness, trace data provenance through multiple processing stages, integrate tools via unified parameter handling (CTD scheme), or ensure the workflow adheres to community standards for proteomics/metabolomics (PSI formats, TOPP Tools concept).

## When NOT to use

- Input data is already fully processed (e.g., a quantitation feature table or identification result file) — reconstruction applies to raw or intermediate-stage data.
- The workflow targets non-MS data types (genomics, imaging, etc.) — OpenMS is LC-MS/proteomics-specific.
- No access to tool parameter configurations or source code — reconstruction requires visibility into CTD definitions and tool integration points.

## Inputs

- Raw LC-MS data files (mzML, mzXML, NetCDF formats)
- Proteomics/metabolomics sample metadata
- Tool configuration and parameter templates (CTD files)
- Reference databases (for identification workflows)
- Existing workflow descriptions or partial documentation

## Outputs

- Validated workflow description (CTD-based or tool-chain documentation)
- Processed MS data files (mzML, mzTab, or quantitation matrices)
- Identification and quantification results
- 2D/3D visualizations (TOPPView output)
- Unit and functional test results confirming each stage

## How to apply

Begin by identifying the input data format (mzML, mzXML, pepXML, mzIdentXML, mzTab) and the final output requirement (quantitation table, identification results, visualizations). Map intermediate tools using the OpenMS TOPPTools concept and unified CTD (common tool description) parameter scheme to enforce consistent tool composition. Verify adherence to coding conventions, include unit and functional tests for each workflow stage, and ensure proper documentation of parameter choices. Validate against PSI standards and confirm integration compatibility with workflow engines (nextflow, KNIME, Galaxy, TOPPAS). Use pyOpenMS Python bindings for algorithm verification and rapid prototyping of custom workflow steps when needed.

## Related tools

- **OpenMS** (Core C++ library providing 150+ TOPP Tools for LC-MS data processing, parameter handling via CTD scheme, and unified workflow orchestration.) — https://github.com/OpenMS/OpenMS
- **KNIME** (Workflow engine for visual composition and execution of OpenMS tools; used to build and validate integrated pipelines.)
- **Galaxy** (Community workflow platform supporting OpenMS tool integration via TOPPTools concept for automated, reproducible MS analysis.)
- **nextflow** (Workflow orchestration framework for containerized OpenMS tool chains, enabling portable and scalable MS data processing.)
- **TOPPAS** (OpenMS-native workflow editor and execution environment for graphical composition of TOPP Tools.)
- **pyOpenMS** (Python bindings to OpenMS API, enabling rapid prototyping and integration testing of custom workflow stages.) — https://github.com/OpenMS/OpenMS

## Evaluation signals

- All intermediate data files conform to PSI-standardized formats (mzML, mzXML, mzIdentXML, mzTab, pepXML) and pass schema validation.
- Workflow tool chain passes unit tests and functional tests for each stage; parameter files follow OpenMS CTD specification.
- Data provenance is traceable: raw input → tool1 → intermediate1 → tool2 → … → final output, with no gaps or undocumented transformations.
- Workflow is executable and produces consistent results when re-run on the same input with identical CTD parameters across KNIME, Galaxy, nextflow, or TOPPAS engines.
- Documentation matches implemented workflow: coding conventions are met, all parameter choices are justified, and integration requirements (e.g., KNIME version compatibility) are verified.

## Limitations

- Workflow severity and internal bug triage assignments are maintained by OpenMS maintainers and may not be publicly visible; review with the maintainer community to confirm blockers for releases.
- Changelog and version-specific parameter changes may not be documented for all releases; consult the release notes and API documentation endpoints (nightly vs. release/latest vs. release/{version}) for version-dependent workflow validation.
- Integration with external tools (Comet, etc.) requires adapter configuration and compatibility testing; mismatches in input/output format can break workflow composition.
- Python bindings (pyOpenMS) cover only a subset of the C++ API; workflows requiring advanced C++ features may not be prototypable in Python and require full C++ compilation.

## Evidence

- [readme] It offers an infrastructure for rapid development of mass spectrometry-related software.: "It offers an infrastructure for rapid development of mass spectrometry-related software."
- [readme] It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept and a unified parameter handling via a 'common tool description' (CTD) scheme.: "It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept and a unified parameter handling via a 'common tool"
- [readme] OpenMS supports the Proteomics Standard Initiative (PSI) formats for MS data.: "OpenMS supports the Proteomics Standard Initiative (PSI) formats for MS data."
- [methods] Before you open the pull request, make sure you adhere to [our coding conventions]: "adhere to [our coding conventions]"
- [methods] have [unit tests and functional tests]: "have [unit tests and functional tests]"
- [readme] With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development.: "With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development."
