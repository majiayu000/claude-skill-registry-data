---
name: lc-ms-data-preprocessing
description: 'Use when you have raw mzML files and corresponding feature tables (CSV format, mzmine-formatted) from untargeted LCMS experiments, and you need to convert them into uniformly-shaped peak matrices (2 × 120 per peak: margin + signal regions) as input for neural network classification of MS1 peak.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - NeatMS
  - Python
  - NumPy
  - pandas
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
---

# lc-ms-data-preprocessing

## Summary

Prepare untargeted liquid chromatography–mass spectrometry (LCMS) raw data and feature tables for neural network–based peak classification by converting mzML and feature table inputs into normalized peak matrices with consistent dimensionality. This skill is essential when you need to standardize heterogeneous LCMS outputs before filtering false positive MS1 peaks.

## When to use

You have raw mzML files and corresponding feature tables (CSV format, mzmine-formatted) from untargeted LCMS experiments, and you need to convert them into uniformly-shaped peak matrices (2 × 120 per peak: margin + signal regions) as input for neural network classification of MS1 peak quality. Apply this skill when peak detection pipelines (e.g., MZmine) have reported candidate peaks that require automated false-positive filtering.

## When NOT to use

- Input feature table is already in a normalized matrix format; skip to model training.
- You are analyzing targeted LCMS data with known metabolite identities; NeatMS is designed for untargeted peak filtering.
- You have fewer than ~500 peaks per class; full model training from scratch will be underpowered; consider transfer learning instead.

## Inputs

- mzML files (raw LCMS data)
- Feature table (CSV format, mzmine-formatted)
- Sample metadata (optional, for exclusion)

## Outputs

- Peak matrix batches (NumPy arrays, shape: N_peaks × 2 × 120)
- Training set (80% of peaks, shape: N_train × 2 × 120)
- Test set (10% of peaks, shape: N_test × 2 × 120)
- Validation set (10% of peaks, shape: N_val × 2 × 120)

## How to apply

Create a NeatMS Experiment object by loading raw mzML files and the feature table, specifying input_format='mzmine'. Instantiate a NN_handler (Neural Network Handler) object with the experiment and configure batch-creation parameters: matrice_size=120 (total peak matrix width), margin=1 (margin region specification), and min_scan_num=5 (minimum scan points per peak). Call create_batches() with your desired split ratios (default: 80% training, 10% test, 10% validation) and set normalise_class=False unless you require class balancing for imbalanced training sets. The resulting batch arrays encode each peak as a 2D matrix where the first 40 values and last 40 values represent margin (0) regions and the middle 40 values represent peak signal (1), forming a binary spatial encoding. Verify output shape matches expected_result_matrix_shape: 2 × 120 per peak.

## Related tools

- **NeatMS** (Core package providing Experiment and NN_handler classes for batch creation and peak matrix generation) — https://github.com/bihealth/NeatMS
- **NumPy** (Array manipulation and inspection of peak matrix shapes and binary encoding)
- **pandas** (Loading and parsing feature table (CSV) and sample metadata)
- **Python** (Language for executing NeatMS API and batch inspection)

## Examples

```
from neatms import Experiment, NN_handler
exp = Experiment(raw_data_path='path/to/mzML/', feature_table_path='features.csv', input_format='mzmine')
nn_handler = NN_handler(experiment=exp, matrice_size=120, margin=1, min_scan_num=5)
nn_handler.create_batches(train_split=0.8, test_split=0.1, val_split=0.1, normalise_class=False)
```

## Evaluation signals

- Peak matrix shape equals 2 × 120 for every peak in all batches (no ragged arrays).
- First 40 and last 40 values of the second dimension are margin-encoded (predominantly 0); middle 40 values contain peak signal (predominantly 1).
- Split ratios match requested proportions: training ≈ 80%, test ≈ 10%, validation ≈ 10% of total peaks.
- All peaks meet min_scan_num ≥ 5 criterion; no peaks with fewer than 5 scan points remain in batches.
- Batch arrays are NumPy-serializable and have consistent dtype (typically float or int); no missing or NaN values introduced by preprocessing.

## Limitations

- min_scan_num=5 (default) may filter out low-abundance or short-duration peaks; adjust if analyzing ultra-short chromatographic features.
- matrice_size=120 is fixed; peaks with fewer than 120 scan points will be zero-padded, which may bias short peaks or distort their signal morphology.
- normalise_class=False can lead to imbalanced training sets if one peak class (e.g., true positives vs. false positives) is significantly rarer; set normalise_class=True if class imbalance exceeds 1:3.
- NeatMS does not provide automatic early stopping during training; manual monitoring of validation metrics is required to prevent overfitting.
- Input format is mzmine-specific; feature tables from other peak detection tools (e.g., XCMS, MZmine3 with modified output) may require reformatting.

## Evidence

- [readme] NeatMS is an open source python package for untargeted LCMS signal labelling and filtering: "**NeatMS** is an open source python package for untargeted LCMS signal labelling and filtering."
- [readme] NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines: "**NeatMS** enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used LCMS data processing pipelines."
- [other] Create a NeatMS Experiment object by loading raw mzML files and feature table in mzmine format: "Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as"
- [other] Instantiate a NN_handler object with default batch-creation parameters: "Instantiate a NN_handler (Neural Network Handler) object with the experiment and default batch-creation parameters (matrice_size=120, margin=1, min_scan_num=5)."
- [other] Call create_batches() with default split ratios and normalise_class parameter: "Call create_batches() with default split ratios (80% training, 10% test, 10% validation) and normalise_class=False to generate peak matrix batches."
- [other] Peak matrix shape and binary encoding structure: "Validate that the first and last 40 values correspond to margin portions and the middle 40 values correspond to peak signal, matching the documented result_matrix_shape."
- [methods] min_scan_number filtering default value: "`min_scan_number` argument will filter out all peaks that have a number of point (scan) lower than this value. `5` is the default value"
- [methods] normalise_class parameter for class balancing: "The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest"
