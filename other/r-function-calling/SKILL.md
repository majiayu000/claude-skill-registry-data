---
name: r-function-calling
description: Use when after AutoTuner has completed peak identification (TIC analysis),
  peak isolation, and EIC parameter extraction on at least 3 raw mass spectrometry
  samples (qTOF, orbitrap, or FTICR formats converted to mzML/mzXML/CDF), and you
  need to export the tuned parameters in a format ready for XCMS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Autotuner
  - XCMS
  - MZmine2
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/812370
  title: AutoTuner parameter selection
evidence_spans:
- knitr::rmarkdown
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_autotuner_parameter_selection_cq
    doi: 10.1101/812370
    title: AutoTuner parameter selection
  dedup_kept_from: coll_autotuner_parameter_selection_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/812370
  all_source_dois:
  - 10.1101/812370
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Extract parameter estimates via R function call

## Summary

Call the returnParams R function on an AutoTuner object to extract nine optimized parameter estimates for direct input into XCMS or other metabolomics processing software. This skill bridges AutoTuner's statistical parameter inference with downstream tool configuration.

## When to use

After AutoTuner has completed peak identification (TIC analysis), peak isolation, and EIC parameter extraction on at least 3 raw mass spectrometry samples (qTOF, orbitrap, or FTICR formats converted to mzML/mzXML/CDF), and you need to export the tuned parameters in a format ready for XCMS processing of untargeted metabolomics data.

## When NOT to use

- AutoTuner has not yet completed EICparams extraction — call EICparams() and isolatePeaks() first.
- Your input data consists of fewer than 3 raw samples — AutoTuner requires at least 3 samples for robust parameter estimation.
- You are working with targeted metabolomics or already have manually tuned parameters — returnParams is designed for untargeted parameter discovery, not refinement of existing parameter sets.

## Inputs

- AutoTuner object (R) with completed EICparams and peak isolation results
- Raw mass spectrometry data files (mzML, mzXML, or CDF format) used to generate the AutoTuner object

## Outputs

- Parameter estimate table (nine distinct parameters)
- Structured parameter file (CSV or TSV) formatted for XCMS input
- Parameter vector suitable for direct entry into xcmsSet() or related XCMS functions

## How to apply

Load the AutoTuner object containing completed EICparams results into an R session (R ≥ 3.6). Call the returnParams function on the AutoTuner object; this extracts the nine distinct parameter estimates produced by statistical inference from the sliding-window TIC analysis and EIC bounds expansion. Format the returned parameter table as a structured file (CSV or TSV) suitable for direct ingestion by XCMS or MZmine2. The output parameters encapsulate peak detection thresholds, mass error bounds, and chromatographic feature definitions learned from your specific dataset and instrument, eliminating manual trial-and-error tuning.

## Related tools

- **Autotuner** (Source object containing parameter estimates; returnParams is an Autotuner class method) — https://github.com/KujawinskiLaboratory/Autotuner
- **XCMS** (Downstream consumer of the nine returned parameter estimates for peak detection and feature alignment in untargeted metabolomics)
- **MZmine2** (Alternative downstream consumer of AutoTuner parameter estimates for metabolomics data processing)
- **R** (Runtime environment for loading AutoTuner and executing returnParams function call)

## Examples

```
# Load AutoTuner library and object, then call returnParams
library(Autotuner)
params <- returnParams(autotuner_object)
write.csv(params, file='autotuner_xcms_params.csv', row.names=FALSE)
```

## Evaluation signals

- returnParams returns exactly nine parameter estimates (no more, no fewer) that match the documented AutoTuner output schema.
- Returned parameter values are numeric, within expected ranges for mass error (typically < 50 ppm), retention time windows (seconds), and peak width bounds (in scan units or seconds depending on instrument).
- Exported CSV/TSV file can be read back and successfully passed to XCMS::xcmsSet() or equivalent function without format errors.
- Parameter estimates are consistent with the input dataset's instrument type (qTOF, orbitrap, or FTICR) and are more permissive/accurate than generic defaults used without AutoTuner.
- The nine parameters include representatives of mass accuracy, peak width, peak intensity threshold, and retention time clustering parameters documented in AutoTuner publication.

## Limitations

- AutoTuner requires R ≥ 3.6; older versions are not supported.
- Input raw data must be in open formats (mzML, mzXML, CDF) — proprietary instrument formats (e.g., .raw, .d) must be converted via MSconvert first.
- AutoTuner has been tested on qTOF, orbitrap, and FTICR instruments; performance on other mass analyzer types is unknown.
- A metadata spreadsheet with sample names and experimental factor assignments must be prepared separately; returnParams alone does not infer experimental design.
- No changelog is available in the repository, making it difficult to track version-specific changes to the returnParams output schema.

## Evidence

- [other] The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS to process raw untargeted metabolomics data.: "The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS"
- [intro] Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters.: "Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters."
- [intro] AutoTuner is a parameter tuning algorithm for XCMS, MZmine2, and other metabolomics data processing softwares.: "AutoTuner is a parameter tuning algorithm for XCMS, MZmine2, and other metabolomics data processing softwares."
- [readme] For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)"
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
