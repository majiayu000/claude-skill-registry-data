---
name: mass-track-clustering
description: Use when after constructing initial data bins from mzTree (indexed by
  int(mz × 1000)), determine whether a single bin contains one or multiple mass tracks.
  Apply clustering when the m/z range of points in a bin exceeds 2 × ppm tolerance
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pymzml
  - Python
  - nn_cluster_by_mz_seeds
  - get_thousandth_bins
  - asari chromatograms.extract_massTracks_
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- The default method uses `pymzml` to parse mzML files.
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-track-clustering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Partition m/z data points within a mass bin into distinct mass tracks using nearest-neighbor clustering when high mass resolution cannot resolve all peaks within the bin's m/z range. This skill determines how many independent ion species coexist in the same chromatographic bin and assigns each a consensus m/z and intensity vector.

## When to use

After constructing initial data bins from mzTree (indexed by int(mz × 1000)), determine whether a single bin contains one or multiple mass tracks. Apply clustering when the m/z range of points in a bin exceeds 2 × ppm tolerance (e.g., for 5 ppm tolerance, cluster if m/z span > 10 ppm), indicating that high mass resolution alone cannot separate all species and local structure must guide track identity.

## When NOT to use

- The m/z range of the bin is already ≤ 2 × ppm tolerance — use single-track assignment directly.
- Data points are already assigned to known reference masses or spike-in standards — use targeted assignment instead of clustering.
- The bin contains only noise or very low-intensity points below min_intensity_threshold — filter or reject the bin before clustering.

## Inputs

- data bin (set of (m/z, scan_number, intensity) tuples from mzTree keyed by thousandth-m/z)
- ppm tolerance threshold (default 5 ppm for high-resolution Orbitrap)
- m/z histogram of the bin (for seed identification)
- mz_tolerance_minimum (minimum m/z gap to define separate peaks in histogram)

## Outputs

- list of mass tracks, each a (consensus_mz, intensity_vector) tuple
- track assignments for each input point (which cluster each (m/z, scan, intensity) belongs to)

## How to apply

First, check the m/z range (max − min) of all data points in the candidate bin. If the range is ≤ 2 × ppm tolerance, assign all points to a single track with consensus m/z = mean(median_mz, mz_at_highest_intensity). Otherwise, apply nearest-neighbor clustering via nn_cluster_by_mz_seeds, using m/z histogram peaks separated by the mz_tolerance_minimum as seed points. This ensures clusters are anchored to actual density maxima in the m/z distribution rather than arbitrary boundaries. For each cluster, build a mass track as (consensus_mz, intensity_vector), using maximum intensity when multiple points exist in the same scan, and inserting zeros for missing scans across the full retention time range.

## Related tools

- **pymzml** (Parse mzML files to retrieve MS1 spectra as (m/z, scan_number, intensity) tuples for input to bin construction)
- **nn_cluster_by_mz_seeds** (Perform nearest-neighbor clustering on m/z values using histogram peaks as seeds; core algorithm for multi-track assignment) — https://github.com/shuzhao-li/asari
- **get_thousandth_bins** (Construct initial data bins from mzTree by binning on int(mz × 1000) and merging adjacent bins, prerequisite for clustering decision) — https://github.com/shuzhao-li/asari
- **asari chromatograms.extract_massTracks_** (Build final mass track objects (consensus_mz, intensity_vector) after clustering for each sample) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.chromatograms import extract_massTracks_; tracks = nn_cluster_by_mz_seeds(mz_list=bin_points, mz_tolerance_minimum=0.001, ppm=5); mass_tracks = [build_track(cluster) for cluster in tracks]
```

## Evaluation signals

- Verify cluster counts match the number of distinct m/z peaks in the bin's histogram separated by ≥ mz_tolerance_minimum.
- Check that each cluster's consensus m/z lies within the spatial bounds of its assigned points (min_mz ≤ consensus ≤ max_mz).
- Confirm intensity vectors have no gaps within single tracks — missing scans should be zero, not omitted.
- Validate that all (m/z, scan, intensity) points from the input bin are assigned to exactly one cluster (no orphans, no duplicates).
- Cross-check that single-track bins (m/z range ≤ 2 × ppm) were assigned directly without invoking nn_cluster_by_mz_seeds, avoiding unnecessary computation.

## Limitations

- Clustering sensitivity depends on mz_tolerance_minimum and histogram resolution; very low-abundance minor peaks may be missed if below noise floor or poorly resolved in histogram.
- Nearest-neighbor clustering assumes clear separation in m/z space; if multiple species have overlapping m/z ranges due to instrumental limitations, track assignment may be ambiguous and may benefit from isotope or adduct annotation (handled separately via khipu pre-annotation).
- Performance scales with bin size; bins with very high point density (e.g., from high-abundance compounds) may incur clustering overhead; asari mitigates this through maximum intensity selection per scan.
- Clustering does not use retention time information; co-eluting species at identical m/z cannot be resolved by this method alone and require MS/MS or auxiliary data.

## Evidence

- [other] if m/z range is within 2 × ppm tolerance, create one track; otherwise apply nearest-neighbor clustering via nn_cluster_by_mz_seeds using m/z histogram peaks separated by mz tolerance minimum: "if m/z range is within 2 × ppm tolerance, create one track; otherwise apply nearest-neighbor clustering via nn_cluster_by_mz_seeds using m/z histogram peaks separated by mz tolerance minimum."
- [other] Build each mass track as (consensus_mz, intensity_vector) where consensus_mz = mean(median_mz, mz_at_highest_intensity), maximum intensity is used when multiple points exist in the same scan, and zeros are inserted for missing intensity values across full RT range.: "Build each mass track as (consensus_mz, intensity_vector) where consensus_mz = mean(median_mz, mz_at_highest_intensity), maximum intensity is used when multiple points exist in the same scan, and"
- [other] Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval. 3. Create data bins from mzTree using get_thousandth_bins, filtering for minimal required scan count and merging adjacent bins separated by ≤0.001 amu or within ppm tolerance.: "Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval. 3. Create data bins from mzTree using get_thousandth_bins, filtering for minimal required scan count and"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [other] Asari builds mass tracks per data bin by leveraging high mass resolution to prioritize mass separation and alignment during the initial processing of MS1 spectra (m/z, scan number, intensity) from data files.: "Asari builds mass tracks per data bin by leveraging high mass resolution to prioritize mass separation and alignment during the initial processing of MS1 spectra (m/z, scan number, intensity) from"
