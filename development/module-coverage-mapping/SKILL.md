---
name: module-coverage-mapping
description: Use when evaluating whether a mass spectrometry data analysis platform (such as mzmine) provides complete module coverage across all advertised separation and ionisation techniques.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mzmine
derived_from:
- doi: 10.1038/s41587-023-01690-2
  title: mzmine3
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzmine3
    doi: 10.1038/s41587-023-01690-2
    title: mzmine3
  dedup_kept_from: coll_mzmine3
schema_version: 0.2.0
---

# module-coverage-mapping

## Summary

Systematically inventory all processing modules in a mass spectrometry software suite and cross-reference them against supported separation/ionisation techniques (LC, GC, IMS, MS imaging) to verify complete workflow coverage. This skill ensures that every supported instrument type and analysis modality has at least one corresponding processing module in the software architecture.

## When to use

Apply this skill when evaluating whether a mass spectrometry data analysis platform (such as mzmine) provides complete module coverage across all advertised separation and ionisation techniques. Use it to answer questions like: 'Does every supported LC/GC/IMS/MS imaging input type have at least one dedicated processing module?' or 'What gaps exist in the module inventory for specific instrument types?'

## When NOT to use

- When evaluating only a single module's capability rather than the completeness of the entire suite—use module-specific documentation review instead.
- When the software does not explicitly advertise support for multiple separation/ionisation techniques—matrix-based coverage analysis is unnecessary if only one technique is supported.
- When module responsibilities overlap or are poorly documented—coverage mapping requires clear separation of concerns and accessible module documentation to be reliable.

## Inputs

- software repository source tree (mzmine codebase)
- module documentation (README files, inline code comments, API docs)
- list of advertised separation/ionisation techniques (from software README or marketing materials)

## Outputs

- module inventory (enumerated list of all processing modules with primary function classification)
- module-technique coverage matrix (rows: separation/ionisation types; columns: module categories or individual modules; cells: boolean or support level)
- coverage verification report (text or structured summary confirming every advertised technique has ≥1 corresponding module)

## How to apply

Access the software repository (e.g. github.com/mzmine/mzmine) and retrieve the complete list of processing modules from the codebase structure and documentation. Categorise each module by its primary function (import, preprocessing, alignment, identification, visualisation, etc.) using source code inspection or architectural documentation. Cross-reference module documentation or source code comments to identify which separation/ionisation types each module explicitly supports (LC, GC, IMS, MS Imaging). Build a coverage matrix mapping each separation/ionisation type as rows and module categories as columns, marking which modules support which techniques. Verify that every advertised technique (e.g. LC, GC, IMS, MALDI MS imaging) appears in at least one column per module category. Document the module inventory, support attributes, and coverage verification results in a structured report (e.g. table or matrix) to enable future maintainers to identify gaps.

## Related tools

- **mzmine** (mass spectrometry data processing platform whose module inventory and technique support coverage is being mapped) — https://github.com/mzmine/mzmine

## Evaluation signals

- Every row in the coverage matrix (each advertised separation/ionisation type: LC, GC, IMS, MS imaging) has at least one module marked as supporting it.
- The module inventory list is exhaustive and accounts for all source directories and documented processing steps in the codebase (spot-check: review README and /src/main/java module structure for consistency).
- Module categorisations are mutually exclusive and logically consistent (e.g. each module has exactly one primary function; no module is categorised simultaneously as 'import' and 'preprocessing' without justification).
- Cross-references between modules and techniques are traceable to source code or documentation (i.e. each claim 'module X supports technique Y' is linked to a code comment, README section, or class name indicating this support).
- No advertised technique is completely absent from the module inventory (spot-check: if the README states 'Support includes LC, GC, IMS, and MS imaging', verify that the coverage matrix has non-empty entries for all four).

## Limitations

- Module coverage mapping reflects only the presence of modules, not their maturity, completeness, or correctness—a module may be listed but poorly implemented or rarely maintained.
- Documentation quality varies; some modules may lack clear documentation of which techniques they support, requiring inference from code or examples rather than explicit statements.
- Coverage mapping is a snapshot in time and becomes outdated as new modules are added or existing modules deprecate support for certain techniques—periodic re-verification is necessary.
- The skill does not evaluate module interoperability or workflow completeness; a technique may have a module but lack integration with upstream import or downstream identification modules needed for a full analytical workflow.

## Evidence

- [other] mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments.: "mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS"
- [other] Access the mzmine repository (github.com/mzmine/mzmine) and retrieve the complete list of processing modules from the codebase structure or documentation. Categorise each module by its primary function (e.g., import, preprocessing, alignment, identification, visualisation). Cross-reference module documentation or source code to identify which separation/ionisation types each module supports (LC, GC, IMS, MS Imaging). Build a coverage matrix mapping separation/ionisation types to modules.: "Access the mzmine repository (github.com/mzmine/mzmine) and retrieve the complete list of processing modules from the codebase structure or documentation. Categorise each module by its primary"
- [other] Verify that every supported type (LC, GC, IMS, MS Imaging) is covered by at least one module in the workflow. Document the module inventory and coverage verification in a structured report.: "Verify that every supported type (LC, GC, IMS, MS Imaging) is covered by at least one module in the workflow. Document the module inventory and coverage verification in a structured report"
- [readme] provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow: "provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow"
