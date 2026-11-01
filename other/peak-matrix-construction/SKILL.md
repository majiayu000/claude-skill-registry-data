---
name: peak-matrix-construction
description: Use when when you have raw mzML files and a corresponding feature table (CSV format, e.g., from mzmine) and need to generate peak matrices with fixed dimensions (e.g., 2 × 120) that encode margin vs. peak signal regions for training a neural network classifier to filter false positive LCMS peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
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

# peak-matrix-construction

## Summary

Construct 2D peak matrices from LCMS raw data and feature tables using NeatMS's neural network handler, encoding margin and peak signal regions for automated classification of true vs. false positive MS1 peaks. This skill produces normalized batch arrays suitable for neural network training and validation.

## When to use

When you have raw mzML files and a corresponding feature table (CSV format, e.g., from mzmine) and need to generate peak matrices with fixed dimensions (e.g., 2 × 120) that encode margin vs. peak signal regions for training a neural network classifier to filter false positive LCMS peaks.

## When NOT to use

- Input feature table is already in a non-CSV or incompatible format (e.g., mzTab, SQLite database) without prior conversion to mzmine CSV.
- Raw mzML files are missing or corrupted; peak matrix construction requires valid LC–MS/MS signal intensity profiles.
- Expected peaks have fewer scans than min_scan_num; these will be filtered out and should be handled separately or min_scan_num should be lowered with justification.

## Inputs

- raw mzML files (untargeted LCMS data)
- feature table (CSV, mzmine format or compatible)
- Experiment object (NeatMS-instantiated from mzML and feature table)

## Outputs

- peak matrix batches (training, test, validation splits)
- batch arrays with shape (N_peaks, 2, matrice_size)
- binary-encoded margin and peak signal labels (0 for margin, 1 for peak)

## How to apply

Load raw mzML files and the feature table (in mzmine or compatible format) into a NeatMS Experiment object. Instantiate a NN_handler (Neural Network Handler) with desired batch-creation parameters: matrice_size (default 120, the 1D signal length), margin (default 1, padding around the peak center), and min_scan_num (default 5, minimum scans to define a peak). Call create_batches() with train/test/validation split ratios (default 80/10/10) and normalise_class=False to generate peak matrix batches. Inspect the resulting arrays to verify shape (2 × matrice_size per peak) and binary encoding: the first and last `margin × scan_width` values encode margin (label 0), the middle values encode peak signal (label 1). Validate that margin and peak regions match the documented result_matrix_shape before passing to model training.

## Related tools

- **NeatMS** (Provides Experiment and NN_handler classes for loading raw LCMS data, feature tables, and constructing peak matrices with neural-network-ready batch splits and normalization.) — https://github.com/bihealth/NeatMS
- **NumPy** (Underlying array manipulation for batch creation, shape validation, and matrix inspection.)
- **pandas** (Feature table I/O and preprocessing (CSV reading, filtering).)
- **Python** (Language in which NeatMS and all downstream processing is implemented.)

## Examples

```
from neatms import Experiment, NN_handler
exp = Experiment(raw_data_path='./mzml_files/', feature_table_path='./feature_table.csv', peak_detection='mzmine')
nn_handler = NN_handler(exp, matrice_size=120, margin=1, min_scan_num=5)
training_batches, test_batches, validation_batches = nn_handler.create_batches(training_split=0.8, test_split=0.1, val_split=0.1, normalise_class=False)
```

## Evaluation signals

- Peak matrix shape matches expected result_matrix_shape (2 × matrice_size) for all peaks in all batch splits.
- Binary encoding is correct: first and last `margin × scan_width` values are 0 (margin), middle values are 1 (peak signal); sum of 1-labels equals peak region length.
- Batch split counts match specified ratios (e.g., 80% training, 10% test, 10% validation).
- All peaks with scans < min_scan_num are excluded from batches; remaining peaks have ≥ min_scan_num valid scan points.
- Peaks are successfully loaded from the feature table and matched to raw mzML data with no missing or unmatched entries in the resulting batch arrays.

## Limitations

- Peak matrix construction is sensitive to min_scan_num: too high a value filters out genuine peaks; too low risks including noise. NeatMS recommends min_scan_num=5, but users must validate for their LC protocol.
- Feature table format must be compatible with mzmine CSV output; other peak-picking formats (OpenMS, XCMS) may require manual reformatting.
- The margin and matrice_size parameters are fixed during batch creation; post-hoc resizing of peak matrices is not supported by the documented API.
- No changelog is available for NeatMS; backward compatibility of the Experiment and NN_handler APIs across versions is not documented.

## Evidence

- [intro] NeatMS is an open source python package for untargeted LCMS signal labelling and filtering that enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS is an open source python package for untargeted LCMS signal labelling and filtering that enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing"
- [methods] Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as 'mzmine'.: "Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as"
- [methods] Instantiate a NN_handler (Neural Network Handler) object with the experiment and default batch-creation parameters (matrice_size=120, margin=1, min_scan_num=5).: "Instantiate a NN_handler (Neural Network Handler) object with the experiment and default batch-creation parameters (matrice_size=120, margin=1, min_scan_num=5)."
- [methods] Call create_batches() with default split ratios (80% training, 10% test, 10% validation) and normalise_class=False to generate peak matrix batches.: "Call create_batches() with default split ratios (80% training, 10% test, 10% validation) and normalise_class=False to generate peak matrix batches."
- [methods] Validate that the first and last 40 values correspond to margin portions and the middle 40 values correspond to peak signal, matching the documented result_matrix_shape.: "Validate that the first and last 40 values correspond to margin portions and the middle 40 values correspond to peak signal, matching the documented result_matrix_shape."
