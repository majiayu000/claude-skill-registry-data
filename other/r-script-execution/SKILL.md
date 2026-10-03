---
name: r-script-execution
description: Use when you have located example R scripts in a version-controlled repository
  (e.g., Codes-Explained folder), a Read-Me.txt file documents the purpose and parameters
  of each script, and you need to reconstruct or validate a simulation procedure for
  a specific data sub-sample scenario.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3071
  tools:
  - R
  - DisCoPad
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo15010028
  title: DisCo P-ad
evidence_spans:
- example R and MATLAB codes (for one data sub-sample scenario) used for the simulation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_disco_p_ad_cq
    doi: 10.3390/metabo15010028
    title: DisCo P-ad
  dedup_kept_from: coll_disco_p_ad_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo15010028
  all_source_dois:
  - 10.3390/metabo15010028
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# r-script-execution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute R scripts in sequence from a documented simulation workflow, monitoring console output and intermediate file writes to verify correctness. This skill is essential for reproducing computational analyses where R code implements critical steps in a multi-language (R + MATLAB) pipeline.

## When to use

You have located example R scripts in a version-controlled repository (e.g., Codes-Explained folder), a Read-Me.txt file documents the purpose and parameters of each script, and you need to reconstruct or validate a simulation procedure for a specific data sub-sample scenario. Use this skill when the workflow requires sequential R execution with intermediate verification before proceeding to downstream steps (e.g., MATLAB scripts).

## When NOT to use

- Input data objects are not yet available or have not been downloaded from the link-to-codes-and-data-objects file.
- The R scripts are part of a parallel execution workflow where order independence is assumed; in such cases, concurrent execution may be preferred.
- You are validating only the MATLAB component of the pipeline and do not need R results as inputs to MATLAB stages.

## Inputs

- R script files (.R) from Codes-Explained folder
- Sub-sample data objects (.RData, .rds, or text-based formats referenced in link-to-codes-and-data-objects file
- Read-Me.txt documentation file
- Parameter and configuration settings specified in Read-Me.txt

## Outputs

- Console output (diagnostic messages, warnings, model summaries)
- Intermediate files (tables in .csv or .txt format, figures in .pdf or .png format)
- R model objects (saved as .RData or .rds files)
- Simulation results tables and figures matching documented format in Read-Me.txt

## How to apply

First, consult the Read-Me.txt file to identify which R scripts correspond to your sub-sample simulation and understand their documented purpose and parameters. Second, load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using R's standard data import functions (e.g., load(), read.csv(), readRDS()). Third, execute the R scripts in the documented sequence, capturing and inspecting console output for errors, warnings, and expected diagnostic messages. Fourth, verify that intermediate file writes (e.g., saved tables, figures, model objects) are created in the expected locations with correct dimensions and data types. Compare outputs against the format and structure described in Read-Me.txt to confirm correctness before advancing to subsequent scripts or tools.

## Related tools

- **R** (Language and runtime for executing example scripts implementing the simulation procedure on sub-sample data)
- **DisCoPad** (Repository containing codes, data objects, and documentation (Read-Me.txt, link-to-codes-and-data-objects file, Codes-Explained folder) that support R script execution and validation) — https://github.com/KechrisLab/DisCoPad

## Examples

```
source('Codes-Explained/example_script_1.R'); load('data_objects/subsample_1.RData'); # Check console output and ls() for expected objects; verify output files written to disk
```

## Evaluation signals

- Console output contains no fatal errors and includes expected diagnostic messages or model summaries as documented in Read-Me.txt.
- All intermediate files (tables, figures, model objects) are written to their expected locations with correct file names and formats.
- Dimensions and data types of saved tables and model objects match the structure described in Read-Me.txt documentation.
- Figures render without missing data or formatting errors and contain expected plot elements (axes labels, legends, statistical annotations).
- Sequential execution of multiple R scripts produces no dependency errors (i.e., downstream scripts successfully load outputs from upstream scripts).

## Limitations

- The skill assumes Read-Me.txt fully documents the purpose, parameters, and expected outputs of each R script; incomplete or outdated documentation may lead to misinterpretation of results.
- Example scripts are provided for only a single data sub-sample scenario; scaling or extending the workflow to other sub-samples or data types may require code modification not covered by the documented example.
- Console output and intermediate file monitoring are manual tasks; automated logging or validation is not explicitly described in the README.

## Evidence

- [other] Access the DisCoPad repository and navigate to the Codes-Explained folder to locate the example R and MATLAB scripts for the single documented sub-sample scenario.: "Check out "Codes-Explained" folder to find all the example R and MATLAB codes (for one data sub-sample scenario) used for the simulation."
- [readme] Consult the Read-Me.txt file to identify which script(s) correspond to the sub-sample simulation and understand the documented purpose and parameters of each.: "Refer to the "Read-Me.txt" file to understand what each script accomplishes."
- [other] Load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using the appropriate language (R or MATLAB).: "Click on the "link-to-codes-and-data-objects" file to access all codes and related items."
- [other] Execute the R script(s) in sequence, monitoring console output and intermediate file writes for correctness.: "Execute the R script(s) in sequence, monitoring console output and intermediate file writes for correctness."
- [other] Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt.: "Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt."
