---
name: spectral-peak-filtering
description: Use when you have imported raw mass spectrometry data in formats such as MGF, MSP, mzML, or mzXML and need to clean the spectral data prior to similarity comparisons, metadata validation, or export.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - Python
derived_from:
- doi: 10.21105/joss.02411
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.21105/joss.02411
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
---

# spectral-peak-filtering

## Summary

Remove low-intensity and irrelevant peaks from mass spectrometry spectral data to ensure data accuracy and integrity before downstream similarity comparisons or analysis. This filtering step is essential in preprocessing workflows that transform raw spectral files into cleaned datasets suitable for large-scale spectral comparisons.

## When to use

Apply this skill when you have imported raw mass spectrometry data in formats such as MGF, MSP, mzML, or mzXML and need to clean the spectral data prior to similarity comparisons, metadata validation, or export. Use it as the first major processing step after data import to remove noise and irrelevant low-intensity peaks that would otherwise compromise spectral similarity scoring or introduce spurious matches.

## When NOT to use

- Input spectra have already been filtered by an upstream preprocessing tool or vendor software — refiltering may remove legitimate low-abundance peaks needed for downstream analysis.
- Your analysis goal requires retention of all peaks including noise for diagnostic or exploratory purposes — filtering is irreversible and will remove data.
- You are working with very low-abundance compounds or isotope patterns where all peaks, including weak ones, carry biological or diagnostic significance.

## Inputs

- Raw spectral data file (MGF, MSP, mzML, mzXML, or JSON format)
- Spectrum objects or spectrum collection from matchms import
- Peak intensity threshold parameter(s) for filtering decisions

## Outputs

- Filtered spectrum objects or spectrum collection
- Cleaned spectral data file in original or compatible format (MGF, MSP, mzML, or JSON)

## How to apply

Load spectral data from your file using matchms import functions appropriate to your format (MGF, MSP, mzML, mzXML, or JSON). Apply matchms peak filtering functions to remove low-intensity peaks below a defined threshold and irrelevant peaks that do not contribute to spectral characterization. The filtering step operates on individual spectrum objects or spectrum collections, iteratively removing peaks that fall below intensity thresholds or do not meet quality criteria. After filtering, export the cleaned spectrum collection back to a compatible spectral format (MGF, MSP, mzML, or JSON) for downstream use. The rationale is that mass spectrometry spectra contain instrumental noise and chemical background; filtering ensures that only meaningful peaks are retained for reproducible and accurate spectral similarity evaluation.

## Related tools

- **matchms** (Provides peak filtering functions and spectral data import/export for MGF, MSP, mzML, mzXML, and JSON formats; core tool for applying filtering to spectrum objects and collections.) — https://github.com/matchms/matchms
- **Python** (Programming language in which matchms is implemented; required for scripting and executing peak filtering workflows.)

## Evaluation signals

- Verify that peak count per spectrum decreases after filtering; compare spectrum.peaks before and after filtering to confirm low-intensity peaks are removed.
- Check that total ion current (TIC) or sum of peak intensities is preserved or only slightly reduced for high-quality spectra, indicating selective removal of noise rather than loss of signal.
- Confirm that filtered spectra retain characteristic peaks relevant to the analyte mass and fragmentation pattern (e.g., molecular ion, major fragment peaks).
- Export filtered spectra to output format and validate file integrity by re-importing and verifying spectrum metadata and peak counts match the expected filtered output.
- Compare spectral similarity scores (e.g., cosine similarity) before and after filtering; expect improved or stable scores when comparing against reference spectra, indicating noise reduction improves signal-to-noise ratio.

## Limitations

- Peak filtering is data-dependent; the choice of intensity threshold and filtering criteria must be tuned for the specific mass spectrometry platform, ionization method, and analyte class. Threshold values that work for high-abundance metabolites may be inappropriate for low-abundance compounds.
- Filtering is irreversible; peaks removed during this step cannot be recovered. Over-aggressive filtering may remove legitimate low-abundance fragment peaks or isotope patterns critical for compound identification.
- Matchms provides 'basic' peak filtering; the filtering implementation may not support all advanced filtering strategies (e.g., adaptive thresholding based on local noise, mass window-specific thresholding) that specialized MS vendor software offers.
- Filtering operates on individual spectra independently; it does not consider spectral alignment or consensus patterns across a cohort, which may limit ability to distinguish compound-specific peaks from systematic noise in large datasets.

## Evidence

- [other] Matchms provides basic peak filtering tools as part of its data processing workflow to ensure data accuracy and integrity in spectral datasets.: "Apply matchms peak filtering functions to remove low-intensity peaks and irrelevant peaks to ensure data accuracy and integrity."
- [readme] Supported input and output formats for peak filtering workflow.: "Load spectral data from a file (MGF, MSP, or mzML format) using matchms import functions. Apply matchms peak filtering functions to remove low-intensity peaks. Export the filtered spectrum collection"
- [readme] Matchms is designed to transform raw spectral data through preprocessing steps.: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [readme] Basic peak filtering is a core data quality assurance capability.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
- [readme] Matchms supports multiple relevant spectral formats for input and output.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
