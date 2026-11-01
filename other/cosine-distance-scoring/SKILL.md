---
name: cosine-distance-scoring
description: Use when when you have preprocessed mass spectra (peak-filtered, metadata-cleaned) in supported formats (mzML, mzXML, msp, MGF, JSON) and need to compare all or many pairs of spectra to identify similar compounds, search spectral libraries, or build a similarity network for spectral clustering or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - Python
  - Spec2Vec
  - MS2DeepScore
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

# cosine-distance-scoring

## Summary

Compute pairwise cosine similarity scores across preprocessed mass spectra using matchms to quantify spectral similarity. This produces a scored matrix enabling downstream selection of related or similar spectra/compounds.

## When to use

When you have preprocessed mass spectra (peak-filtered, metadata-cleaned) in supported formats (mzML, mzXML, msp, MGF, JSON) and need to compare all or many pairs of spectra to identify similar compounds, search spectral libraries, or build a similarity network for spectral clustering or annotation.

## When NOT to use

- Input spectra are not yet preprocessed (raw, uncleaned peaks, unvalidated metadata) — apply peak filtering and metadata cleaning first
- You need similarity measures other than cosine (e.g., fingerprint-based or metadata-only) — matchms supports multiple measures; select the appropriate one for your research question
- Memory or time constraints are severe and you need only top-k similar spectra, not all pairwise scores — consider using faster pre-selection measures first

## Inputs

- Preprocessed mass spectra in mzML, mzXML, msp, metabolomics-USI, MGF, or JSON format
- Peak-filtered and metadata-cleaned spectral data
- List or collection of Spectrum objects from matchms

## Outputs

- Pairwise cosine similarity scores matrix (spectrum-by-spectrum)
- Sparse or dense score array in CSV or pickle format
- Similarity network or ranked list of related spectra

## How to apply

Load preprocessed spectra from input files using matchms loaders. Apply the matchms cosine similarity measure, which compares peak m/z and intensity patterns between all spectrum pairs. The cosine metric treats each spectrum as a vector of intensities at corresponding m/z values, computing dot-product similarity normalized by vector magnitudes. Construct a scores matrix with spectrum identifiers as row and column labels. For large-scale comparisons (hundreds of thousands of spectra), matchms uses sparse data formats to store only computed non-null scores, reducing memory footprint. Save the results matrix to a structured output format (CSV or pickle) for downstream filtering, clustering, or library search.

## Related tools

- **matchms** (Core library for loading spectra, applying cosine similarity computation, and constructing/exporting scores matrices) — https://github.com/matchms/matchms
- **Python** (Runtime environment and scripting language for matchms workflows)
- **Spec2Vec** (Optional extensible similarity measure built on matchms for alternative spectrum comparisons) — https://github.com/iomega/spec2vec
- **MS2DeepScore** (Optional extensible deep-learning-based similarity measure for matchms) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms import Spectrum, calculate_scores
from matchms.similarity import CosineGreedy
spectra = [load_spectrum(f) for f in spectrum_files]
scores = calculate_scores(spectra, spectra, CosineGreedy())
scores.to_csv('pairwise_cosine_scores.csv')
```

## Evaluation signals

- Scores matrix has expected dimensions (num_spectra × num_spectra) and all identifiers match input spectrum list
- Cosine scores are bounded in range [0, 1] (or [−1, 1] for some cosine variants); diagonal is 1.0 (self-similarity) or close to 1.0
- Matrix is symmetric (score(A, B) ≈ score(B, A)) confirming pairwise symmetry
- Non-null entries in sparse format match actual spectrum pairs computed; zero-padded dense format matches sparse non-zeros
- Output file (CSV or pickle) loads without error and round-trip deserialization preserves all scores within floating-point tolerance

## Limitations

- Cosine similarity is computed in m/z–intensity space and is sensitive to peak picking artifacts, noise, and preprocessing choices; results depend critically on prior cleaning and filtering steps
- Large-scale comparisons (hundreds of thousands of spectra) require sparse storage and efficient indexing; dense matrices become memory-prohibitive
- Cosine measure does not account for metadata (e.g., molecular weight, compound class) — matchms offers separate metadata-related assessments for those; cosine is purely spectral-peak-based
- Comparison is pairwise and treats all peaks equally; no weighting by peak intensity variance or chemical relevance unless custom preprocessing is applied

## Evidence

- [other] Matchms applies various pairwise similarity measures for comparing spectra, including common Cosine-related scores among other approaches such as molecular fingerprint-based comparisons and metadata-related assessments.: "Matchms applies various pairwise similarity measures for comparing spectra, including common Cosine-related scores but also molecular fingerprint-based comparisons and other metadata-related"
- [other] Load preprocessed spectra from the input file (peak-filtered spectra or reference spectral library) using matchms. Apply the cosine similarity measure to compute pairwise scores between all spectrum pairs. Construct a scores matrix with spectrum identifiers as row and column labels.: "Load preprocessed spectra from the input file (peak-filtered spectra or reference spectral library) using matchms. Apply the cosine similarity measure to compute pairwise scores between all spectrum"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] We realized that many matchms-based workflows aim to compare many-to-many spectra whereby not all pairs and scores are equally important. For this reason, we now shifted to a sparse handling of scores in matchms (that means: only storing actually computed, non-null values).: "We now shifted to a sparse handling of scores in matchms (that means: only storing actually computed, non-null values)"
- [readme] It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data, and enabling large-scale spectral similarity comparisons.: "enabling large-scale spectral similarity comparisons"
