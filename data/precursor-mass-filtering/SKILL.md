---
name: precursor-mass-filtering
description: Use when after retrieving top-scoring library candidates from a full MS2Deepscore comparison, but before or during final re-ranking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2Query
  - MS2Deepscore
  - MZMine
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
---

# precursor-mass-filtering

## Summary

Filter MS/MS spectral library matches by precursor mass tolerance to distinguish exact matches from structural analogues and reduce false positives. This skill is essential when ranking candidate library spectra retrieved via MS2Deepscore similarity to ensure only plausible precursor mass assignments are retained.

## When to use

Apply this skill after retrieving top-scoring library candidates from a full MS2Deepscore comparison, but before or during final re-ranking. Use it when you need to separate exact-match candidate matches (precursor m/z difference near zero) from structural analogue matches, or when your research goal requires high specificity and you want to filter out matches with large precursor mass deviations that are unlikely to represent the true compound class.

## When NOT to use

- Input spectra lack precursor m/z annotation or are already de-isotoped and consolidated; precursor mass filtering assumes each query spectrum has a single, reliable precursor m/z value.
- Your research goal is to discover structural analogues across a wide chemical space and you intentionally want to ignore mass tolerance constraints; the MS2Query workflow is designed for both analogue and exact-match search, but removing precursor filtering may introduce spurious matches.
- Library spectra have not been indexed by precursor m/z in the SQLite database; filtering requires that candidate retrieval or ranking includes precursor m/z metadata.

## Inputs

- Query spectrum (MS/MS spectrum with precursor m/z and intensity pairs in MGF, mzML, mzXML, JSON, or MSP format)
- Library spectrum candidates (ranked list with precursor m/z annotations from SQLite library store)
- Precursor m/z tolerance threshold (instrument-dependent, typically ±0.05–0.1 Da)

## Outputs

- Filtered candidate list (library spectra within precursor mass tolerance window)
- Precursor m/z difference values (for downstream re-ranking and post-hoc interpretation)
- Match results CSV with precursor_mz_difference column for separating exact matches from analogues

## How to apply

After MS2Deepscore ranks the top ~2000 library spectra by similarity score, apply a precursor mass tolerance filter on the m/z difference between query spectrum and each library candidate. The MS2Query random forest re-ranker accepts precursor m/z difference as one of five input features and uses it to optimize candidate ranking. Compute the absolute difference between query precursor m/z and each library candidate's precursor m/z. Candidates exceeding your chosen tolerance window (e.g., ±0.05 Da for high-resolution instruments, or ±0.1 Da for lower-resolution data) can be flagged or removed before re-ranking, or retained but downweighted by the model. The precursor m/z column in the results CSV can be used post-hoc to separate exact matches (near-zero difference) from analogues for interpretation.

## Related tools

- **MS2Query** (Host tool that integrates precursor mass filtering as a feature input to its random forest re-ranker, and outputs precursor m/z differences in results CSV) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Upstream spectral similarity scorer that provides top candidates before precursor mass filtering is applied in the MS2Query workflow)
- **MZMine** (Recommended preprocessing tool for peak picking and feature clustering of MS2 spectra prior to MS2Query input; output MGF files retain precursor m/z annotations) — https://mzmine.github.io/mzmine_documentation/index.html

## Examples

```
ms2query --spectra ./query_spectra.mgf --library ./ms2query_library_files --ionmode positive
```

## Evaluation signals

- Verify that the precursor_mz_difference column in the output CSV contains values consistent with instrument mass accuracy (e.g., typically < ±0.1 Da for high-resolution MS for exact matches).
- Check that exact matches (true positives with known library compound identity) cluster near zero in the precursor m/z difference distribution, while structural analogues show larger deviations.
- Confirm that filtering out candidates beyond your chosen tolerance threshold reduces the proportion of low-confidence matches (MS2Query model prediction score < 0.6) in the final results.
- Validate that the separation of results into exact-match (|Δm/z| ≈ 0) and analogue (|Δm/z| > tolerance) subsets aligns with expected chemical structure similarities or experimental design constraints.
- Compare hit rates and match quality metrics before and after applying precursor mass filtering to benchmark the effect on both recall and precision relative to your validation set.

## Limitations

- MS2Query does not perform preselection on precursor m/z during the initial MS2Deepscore comparison, so all top 2000 similarity-ranked candidates are considered regardless of mass; precursor filtering must be applied as a secondary constraint and is most effective when integrated into the re-ranking model rather than as a hard cutoff.
- Precursor mass tolerance is instrument-dependent and must be tuned based on your MS instrument's mass accuracy; the article does not specify exact default tolerances, and user judgment is required.
- The workflow requires that library spectra are annotated with accurate precursor m/z values; poorly curated or mislabeled library entries with incorrect precursor masses will not be filtered correctly and may introduce false candidates.
- No peak picking or clustering of similar MS2 spectra is performed by MS2Query itself; if your input files contain many redundant MS/MS spectra per feature, preprocessing with MZMine or similar tools is advised to avoid inflated candidate lists.

## Evidence

- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
- [readme] The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed."
- [readme] If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference.: "If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since"
- [other] Rank candidates by precursor mass tolerance and spectral feature overlap.: "Rank candidates by precursor mass tolerance and spectral feature overlap."
