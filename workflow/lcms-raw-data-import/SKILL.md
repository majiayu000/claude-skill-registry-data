---
name: lcms-raw-data-import
description: Use when you have raw LC/MS data in mzML or mzXML format and need to
  initiate untargeted metabolomics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - mzEmbed
  - mzLearn
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.01.26.634927v3
  title: mzLearn
evidence_spans:
- mzEmbed, a framework for developing pre-trained generative models and fine-tuning
  them for specific tasks for untargeted metabolomics datasets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzlearn_cq
    doi: 10.1101/2025.01.26.634927v3
    title: mzLearn
  dedup_kept_from: coll_mzlearn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.01.26.634927v3
  all_source_dois:
  - 10.1101/2025.01.26.634927v3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-raw-data-import

## Summary

Import and parse raw LC/MS data files (mzML or mzXML format) into a signal detection pipeline without requiring manual parameter tuning. This skill enables the first step of untargeted metabolomics analysis by loading vendor-agnostic, open-source LC/MS data formats directly into data-driven signal detection workflows.

## When to use

You have raw LC/MS data in mzML or mzXML format and need to initiate untargeted metabolomics analysis. Use this skill when you want to avoid manual parameter optimization and instead apply a data-driven signal detection algorithm (such as mzLearn) that autonomously learns signal characteristics from the raw input.

## When NOT to use

- Input is already a processed feature table or peak list; mzLearn is designed for raw, vendor-neutral LC/MS data files only.
- You require targeted metabolite detection with predefined m/z and retention time windows; mzLearn is designed for untargeted metabolomics discovery.
- You have proprietary vendor formats (e.g., .raw, .d) that have not been converted to mzML or mzXML.

## Inputs

- Raw LC/MS data file in mzML format
- Raw LC/MS data file in mzXML format
- Single or multiple LC/MS sample files organized in a directory

## Outputs

- Two-dimensional feature abundance table (CSV or mzTab format)
- Feature table with columns: m/z values, retention times (rt), normalized intensities across samples

## How to apply

Load raw LC/MS data files in mzML or mzXML format into the mzLearn signal detector component within the mzEmbed framework. The data-driven algorithm iteratively learns signal characteristics across mass-to-charge (m/z) and retention time (rt) dimensions without requiring prior knowledge or QC samples. The algorithm autonomously corrects for retention time and intensity drifts caused by batch effects and run order, then outputs a two-dimensional feature table with median rt, m/z values, and normalized intensities. Process all samples in a single run if possible to enable batch-effect correction across the full cohort (the framework is capable of handling large-scale datasets, e.g., 2,075 files in a single run).

## Related tools

- **mzEmbed** (Framework that contains the mzLearn signal detector and orchestrates raw data import, signal detection, and downstream generative model development) — https://github.com/ReviveMed/mzEmbed
- **mzLearn** (Data-driven LC/MS signal detection algorithm that processes imported raw data and autonomously detects metabolite signals without parameter tuning) — http://mzlearn.com/

## Examples

```
```python
from mz_embed.signal_detection import mzLearn
detector = mzLearn()
feature_table = detector.detect_signals(
    data_files='/path/to/raw_lcms_data/',
    format='mzML',
    output_path='/path/to/output_features.csv'
)
```
```

## Evaluation signals

- Raw data file is successfully parsed and loaded into memory without format errors or missing required mzML/mzXML schema fields.
- Output feature table has exactly 3+ columns (m/z, retention time, intensity) and row count equals the number of detected features across all samples.
- Feature abundance values are normalized and consistent across all samples in the cohort; no missing values in the intensity matrix.
- Retention time and intensity drifts are corrected (compare median rt and intensity distributions before and after import across sample batches).
- Output file can be read by downstream tools in the mzEmbed framework (e.g., VAE pretraining) without schema mismatches.

## Limitations

- Only mzML and mzXML open-source formats are supported; proprietary vendor formats must be converted first.
- The algorithm requires data to be loaded as a cohort to enable batch-effect and run-order correction; processing single samples limits drift correction.
- Zero-parameter design assumes that raw data quality is adequate; poor-quality or contaminated samples may produce spurious features.
- The robust feature set output is standardized to 2,736 features (as mentioned in the README); custom feature sets or lower-dimensional outputs require downstream filtering.

## Evidence

- [other] Load raw LC/MS data (mzML or mzXML format) into the mzLearn signal detector: "Load raw LC/MS data (mzML or mzXML format) into the mzLearn signal detector."
- [readme] mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user: "mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user."
- [readme] The algorithm processes raw LC/MS data files in the open-source mzML format, iteratively learning signal characteristics to ensure high-quality signal detection: "The algorithm processes raw LC/MS data files in the open-source mzML format, iteratively learning signal characteristics to ensure high-quality signal detection."
- [readme] A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples: "A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples."
- [readme] mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order: "mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order."
- [readme] Capable of handling large-scale datasets (e.g., 2,075 files in a single run): "Capable of handling large-scale datasets (e.g., 2,075 files in a single run)."
- [readme] No prior knowledge or QC samples are required: "No prior knowledge or QC samples are required."
