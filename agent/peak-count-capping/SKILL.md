---
name: peak-count-capping
description: Use when apply peak-count capping when preprocessing tandem mass spectrometry
  (MS/MS) spectra for peptide identification or spectral library matching, particularly
  when working with high-resolution spectra that may retain numerous low-intensity
  noise peaks after intensity filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectrum_utils
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-count-capping

## Summary

Peak-count capping limits the number of intensity peaks retained in a mass spectrum after noise filtering, improving computational efficiency while preserving the most intense fragment ions. This step is applied during spectrum preprocessing to prevent memory overhead and ensure reproducibility in downstream peptide identification or spectral matching.

## When to use

Apply peak-count capping when preprocessing tandem mass spectrometry (MS/MS) spectra for peptide identification or spectral library matching, particularly when working with high-resolution spectra that may retain numerous low-intensity noise peaks after intensity filtering. Use this skill if memory constraints, computational speed, or reproducibility across different peak-picking algorithms are concerns; the capping ensures consistent spectral dimensionality regardless of input acquisition parameters.

## When NOT to use

- Input spectrum has already been capped to a lower threshold or contains fewer peaks than max_num_peaks; re-capping adds no benefit.
- Analysis requires all peaks for isotope pattern detection or high-resolution mass accuracy calibration; capping may remove isotope satellites or calibrant ions.
- Spectrum is a library entry with manually curated fragment annotations; capping may remove annotated fragments if they fall outside the top max_num_peaks.

## Inputs

- MsmsSpectrum object with m/z and intensity arrays
- integer: max_num_peaks threshold (e.g., 50)

## Outputs

- MsmsSpectrum object with peak count capped at max_num_peaks
- integer: actual number of peaks retained (≤ max_num_peaks)

## How to apply

After applying intensity filtering (e.g., min_intensity=0.05 relative to base peak), invoke the filter_intensity method with a max_num_peaks parameter (e.g., max_num_peaks=50) to retain only the highest-intensity peaks up to the specified ceiling. The spectrum_utils implementation preserves peaks in order of decreasing intensity, effectively truncating the tail of weak peaks. Set the max_num_peaks threshold based on your analysis requirements: lower values (e.g., 20–30 peaks) reduce noise and noise-induced false matches in library searches; higher values (e.g., 100+ peaks) retain more information for de novo sequencing or complex fragmentation patterns. Always apply peak-count capping after intensity normalization (e.g., scale_intensity with mode='root') so that the ranking by intensity reflects the final spectrum representation.

## Related tools

- **spectrum_utils** (provides MsmsSpectrum.filter_intensity() method with max_num_peaks parameter for peak-count capping) — https://github.com/bittremieux/spectrum_utils/
- **Python** (host language for spectrum_utils API invocation)

## Examples

```
spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50)
```

## Evaluation signals

- Verify that the output spectrum's peak count equals min(input_peak_count, max_num_peaks).
- Confirm that retained peaks are ranked in descending order of intensity (no peak is retained unless its intensity exceeds that of any omitted peak).
- Check that m/z and intensity arrays in the output have matching length and no NaN or inf values.
- For comparative analysis: apply the same max_num_peaks threshold to library spectra and query spectra to ensure fair spectral similarity scoring (cosine, dot product).
- Validate that intensity scaling (e.g., root scaling) and peak-count capping do not interact unexpectedly; rerun with and without capping and compare search results for consistency in peptide identifications.

## Limitations

- Peak-count capping is lossy; weak but genuine fragment ions (e.g., neutral-loss peaks, diagnostic low-abundance transitions) may be discarded if they rank outside the top max_num_peaks. This can reduce sensitivity for peptides with complex or distributed fragmentation.
- The threshold max_num_peaks is dataset- and instrument-dependent; no universal optimal value is specified. Users must tune empirically for their MS/MS acquisition method (e.g., HCD, ETD).
- If multiple peaks have identical intensity (rare but possible after intensity quantization), tie-breaking behavior (which peaks are retained) may depend on internal sorting implementation and is not guaranteed to be stable across software versions.
- Peak-count capping does not account for post-translational modifications (PTMs) or cross-linked peptides, which may exhibit fragmentation patterns requiring retention of more peaks; the fixed threshold may not adapt to sequence complexity.

## Evidence

- [other] Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count.: "Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count."
- [intro] spectrum_utils provides common spectrum processing operations including precursor & noise peak removal, intensity filtering, and intensity scaling optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Filter low-intensity noise peaks with max_num_peaks parameter in filter_intensity method.: ".filter_intensity(min_intensity=0.05, max_num_peaks=50)"
