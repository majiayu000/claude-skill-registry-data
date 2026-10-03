---
name: tabular-data-cleaning
description: Use when you have a CSV or table-format spectral peak list (with chemical
  shift, intensity, and metadata columns) destined for NMRformer or similar peak-to-metabolite
  assignment models, and you need to exclude low-quality peaks that would otherwise
  harm prediction accuracy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Pandas
  - NumPy
  - SciPy
  - NMRformer
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c05632
  title: NMRformer
evidence_spans:
- pip install pandas==1.5.1
- pip install numpy==1.26.4
- pip install scipy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmrformer_cq
    doi: 10.1021/acs.analchem.4c05632
    title: NMRformer
  dedup_kept_from: coll_nmrformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05632
  all_source_dois:
  - 10.1021/acs.analchem.4c05632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tabular-data-cleaning

## Summary

Remove noisy and unrecognized peaks from spectral peak lists in tabular format (CSV/table) before input to NMR analysis models. This preprocessing step is essential because unrecognized or noisy peaks degrade model output quality in downstream metabolite identification tasks.

## When to use

Apply this skill when you have a CSV or table-format spectral peak list (with chemical shift, intensity, and metadata columns) destined for NMRformer or similar peak-to-metabolite assignment models, and you need to exclude low-quality peaks that would otherwise harm prediction accuracy. Specifically, use it when peaks fall below a signal-to-noise ratio (SNR) threshold or cannot be matched to a reference spectral library.

## When NOT to use

- Input is a pre-processed spectrum (1D 1H NMR spectrum intensity array) rather than a peak list — use spectrum-to-peak-extraction instead.
- Peak list has already been validated and filtered by expert manual review — skip this step to avoid over-filtering.
- You lack a reference spectral library or SNR thresholds defined for your instrument/sample — proceed with caution and document assumptions.

## Inputs

- CSV file with chemical shift (column 1) and peak intensity (column 2)
- Peak list in table format with chemical shift, intensity, and metadata
- Reference spectral library or chemical shift database for cross-reference validation

## Outputs

- Filtered CSV file with cleaned peak list (unrecognized and low-SNR peaks removed)
- Peak list compatible with NMRformer model input

## How to apply

Load the input peak list (CSV format with chemical shift and intensity columns) using Pandas. Apply signal-to-noise ratio (SNR) filtering via NumPy/SciPy to exclude peaks below a quality threshold. Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify and flag unrecognized peaks. Remove both low-SNR and unrecognized peaks from the list. Export the cleaned peak list as a CSV file compatible with NMRformer input requirements. The rationale is that filtering before model input prevents noisy or spurious peaks from confounding peak assignment and metabolite identification.

## Related tools

- **Pandas** (Load, filter, and export tabular peak list data)
- **NumPy** (Compute signal-to-noise ratio thresholds and array operations for SNR filtering)
- **SciPy** (Apply statistical signal processing and SNR filtering algorithms)
- **NMRformer** (Downstream model that consumes the cleaned peak list for metabolite assignment) — github.com/zza1211/NMRformer

## Examples

```
import pandas as pd; peaks = pd.read_csv('input_peaks.csv', names=['chemical_shift', 'intensity']); snr_threshold = 5; peaks_filtered = peaks[peaks['intensity'] > snr_threshold]; peaks_filtered.to_csv('filtered_peaks.csv', index=False)
```

## Evaluation signals

- Output CSV has the same schema (chemical shift, intensity columns) as input but with fewer rows; verify no valid peaks were erroneously removed by spot-checking high-intensity peaks.
- All remaining peaks in the output file have SNR values above the defined threshold; verify SNR computation and threshold logic in code.
- All remaining peaks cross-reference successfully to the reference spectral library (or all unrecognized peaks are explicitly marked/removed); check against library records.
- NMRformer model run on filtered output produces stable, interpretable metabolite assignments without spurious low-confidence predictions from noise.
- Before-and-after row counts and summary statistics (mean intensity, intensity distribution) show reasonable reduction without data loss; document filtering rationale in a summary report.

## Limitations

- The specific SNR filtering criteria and thresholds are not detailed in the NMRformer documentation; users must define or calibrate SNR thresholds for their own instrument and sample matrix.
- Reference spectral library availability and completeness vary by metabolomics platform and NMR field strength; incomplete libraries may incorrectly flag true peaks as unrecognized.
- Filtering logic may conflict with rare or novel metabolites whose peaks are not in the reference library; manual curation is recommended for high-stakes applications.
- The README does not provide example threshold values, code snippets, or a pre-built filtering script; implementation details must be reverse-engineered or custom-coded.

## Evidence

- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible.: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [other] The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output.: "The NMRformer workflow requires manual or automated filtering of the input spectral peak list to exclude unrecognized or noisy peaks, since such peaks degrade model output"
- [other] Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy.: "Apply signal-to-noise ratio (SNR) filtering to exclude peaks below a quality threshold using NumPy and SciPy."
- [other] Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas.: "Load the input spectral peak list (CSV or table format containing peak chemical shifts, intensities, and metadata) using Pandas."
- [other] Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify and mark unrecognized peaks.: "Cross-reference remaining peaks against a reference spectral library or chemical shift database to identify and mark unrecognized peaks."
