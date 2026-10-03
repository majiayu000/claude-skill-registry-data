---
name: batch-timing-analysis
description: Use when when evaluating whether a new or candidate mass spectrometry
  processing library (e.g., spectrum_utils) offers faster spectrum processing throughput
  than established alternatives (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - pymzML
  - pyOpenMS
  - Python
  - seaborn
  - NumPy
  - pyteomics
  - spectrum_utils
  - pyteomics.mgf
  - matplotlib
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- pymzML (version 2.5.2)
- pyOpenMS (version 2.7.0)
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
- import seaborn as sns
- Spectrum processing in spectrum_utils has been optimized for computational efficiency
  using [NumPy](https://www.numpy.org/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
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

# batch-timing-analysis

## Summary

Quantify the per-spectrum processing throughput of mass spectrometry data processing libraries by timing standardized workflow operations on a representative batch of valid spectra. This enables objective comparison of computational efficiency across competing tools and identification of performance bottlenecks.

## When to use

When evaluating whether a new or candidate mass spectrometry processing library (e.g., spectrum_utils) offers faster spectrum processing throughput than established alternatives (e.g., pymzML, pyOpenMS), or when benchmarking a library's performance across different versions, parameter configurations, or hardware platforms. Triggered by a research question about relative computational speed or by a need to justify tool adoption based on empirical timing data.

## When NOT to use

- Input is a small test dataset (< 100 spectra) that may not reveal statistically meaningful differences due to startup overhead and noise.
- Processing parameters differ significantly between libraries, making direct comparison invalid; all libraries must apply identical filtering thresholds and transformations.
- Goal is to profile code execution at fine granularity (e.g., per-function bottlenecks); use a dedicated profiler (cProfile, line_profiler) instead of end-to-end timing.
- Libraries are running on different hardware or with different resource constraints; timing comparisons require identical execution environment.

## Inputs

- Mass spectrometry data file in MGF format (or other supported spectrum format)
- Specification of valid spectrum criteria (minimum peak count, required metadata fields)
- Processing parameter configuration (m/z range, precursor tolerance, intensity threshold, peak limit, scaling method)

## Outputs

- Per-spectrum processing time measurements (seconds) for each library
- Summary statistics (median, quartiles, min, max processing time per library)
- Boxplot or comparative visualization showing timing distribution across libraries
- Library ranking by median throughput (spectra per second)

## How to apply

Load a representative mass spectrometry data file (e.g., MGF format) and parse all spectra using a neutral parser (e.g., pyteomics.mgf). Filter to valid spectra meeting minimal quality criteria (e.g., ≥10 peaks, charge state present). For each library under comparison, apply an identical standardized processing workflow: restrict m/z range (e.g., 100–1400), remove precursor peak (with consistent tolerance, e.g., 0.02 Da), filter low-intensity noise (e.g., retain only peaks ≥5% of base peak intensity), cap peak count (e.g., max 150 peaks), and apply intensity scaling (e.g., square root). Time each library's execution on all valid spectra using Python's timing utilities. Collect per-spectrum processing times and compute summary statistics (median, quartiles). Visualize results as a boxplot or violin plot on log scale to show distribution and relative performance. Correctness is confirmed by verifying that all libraries produce identical or nearly identical processed spectra when given the same inputs and parameters.

## Related tools

- **spectrum_utils** (Primary candidate library under evaluation; implements optimized spectrum processing using NumPy and Numba) — https://github.com/bittremieux/spectrum_utils
- **pymzML** (Reference comparison library; alternative mass spectrometry data processing tool) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Reference comparison library; alternative mass spectrometry data processing tool)
- **pyteomics.mgf** (Neutral spectrum file parser used to load and validate input data before library-specific processing)
- **matplotlib** (Visualization of timing results as boxplots or comparative plots)
- **NumPy** (Underlying efficient array operations; used by spectrum_utils for optimization)
- **seaborn** (Optional statistical visualization library for enhanced boxplot styling and interpretation)

## Examples

```
import pyteomics.mgf; import spectrum_utils.spectrum as sus; spectra = [s for s in pyteomics.mgf.read('iPRG2012.mgf') if len(s['m/z array']) >= 10 and 'charge' in s['params']]; import time; times = []; [times.append(time.time()) or (lambda spec: (spec.set_mz_range(100, 1400), spec.remove_precursor_peak(0.02, 'Da'), spec.filter_intensity(0.05, 150), spec.scale_intensity('root'), time.time() - times[-1]))(sus.Spectrum(mz=s['m/z array'], intensity=s['intensity array'], precursor_mz=s['params']['precursor_mz'][0], precursor_charge=s['params']['charge'][0])) for s in spectra]
```

## Evaluation signals

- All libraries process the same set of valid spectra (vetted by peak count and metadata presence) with identical parameter inputs (m/z range, precursor tolerance, intensity threshold, peak cap, scaling method).
- Timing measurements are reproducible and consistent across multiple runs on the same input batch, with coefficient of variation < 10% for median times.
- Processed spectra from each library are identical or nearly identical in m/z values, intensities, and peak ordering, confirming that timing differences reflect computational efficiency, not algorithmic differences.
- Per-spectrum timing distributions show expected behavior: median times are in reasonable range (e.g., 1–100 ms per spectrum depending on dataset size and complexity), with outliers plausibly explained by system load or peak density variation.
- Boxplot or statistical summary clearly shows the library ranking by throughput (spectra per second), with confidence intervals or error bars that reflect measurement variability.

## Limitations

- Timing results are sensitive to hardware (CPU, RAM, disk I/O) and system state (background processes, OS scheduler); comparisons should be conducted under controlled conditions and repeated to verify reproducibility.
- Startup overhead (library import, initialization) is typically amortized in batch timing but may dominate on very small batches; timing methodology must be transparent about what is and is not included.
- Different libraries may have different memory usage profiles or cache behavior; a library that is slower per-spectrum might be preferred if it has lower peak memory or better scaling with dataset size.
- Parameter configurations may not be perfectly equivalent across libraries (e.g., precursor tolerance units, intensity scaling algorithms); timing results are only valid when parameters are genuinely identical.
- Performance may vary significantly with spectrum complexity (peak density, m/z range); a single batch may not represent diverse real-world usage patterns.

## Evidence

- [other] spectrum_utils version 0.4.0 is reported to be faster than alternative libraries pymzML version 2.5.2 and pyOpenMS version 2.7.0.: "spectrum_utils (version 0.4.0) is faster than alternative libraries, such as [pymzML](https://github.com/pymzml/pymzML/) (version 2.5.2) and [pyOpenMS](https://pyopenms.readthedocs.io/) (version"
- [other] Spectrum processing in spectrum_utils is optimized for computational efficiency using NumPy and Numba.: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)"
- [other] Workflow involves loading an MGF file, parsing spectra, filtering by quality, timing standardized processing operations, and generating comparative boxplot.: "Load MGF file (iPRG2012.mgf) and parse spectra using pyteomics.mgf. 2. Filter valid spectra (≥10 peaks, charge state present). 3. Time spectrum_utils processing: set m/z range to 100–1400, remove"
- [intro] Common spectrum processing operations are optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
