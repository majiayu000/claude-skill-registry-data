---
name: tabular-data-export
description: Use when you have extracted MS1 or MS2 peak lists and scan headers from
  Thermo Fisher RAW files using MetaXtract and need to load them into pandas, NumPy,
  or external analysis tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaXtract
  - Python (pandas, NumPy, PyArrow)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.11.12.687968v1
  title: MetaXtract
evidence_spans:
- MetaXtract is a hybrid tool for extracting, analysing, and visualising data from
  **Thermo Fisher RAW** mass spectrometry files.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaxtract_cq
    doi: 10.1101/2025.11.12.687968v1
    title: MetaXtract
  dedup_kept_from: coll_metaxtract_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.11.12.687968v1
  all_source_dois:
  - 10.1101/2025.11.12.687968v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tabular-data-export

## Summary

Export mass spectrometry peak lists and scan metadata from Thermo Fisher RAW files into tabular formats (CSV, TSV, Parquet) for downstream computational analysis. This skill bridges native binary RAW file data and standard data science pipelines by converting complex nested scan structures into flat, queryable tables.

## When to use

You have extracted MS1 or MS2 peak lists and scan headers from Thermo Fisher RAW files using MetaXtract and need to load them into pandas, NumPy, or external analysis tools. Use this skill when your downstream workflow requires tabular data with one row per scan and array-valued columns (m/z, intensity, resolution, noise, baseline, charge) that can be iterated or sliced by scan number.

## When NOT to use

- Input is already a pandas DataFrame or pre-exported CSV/TSV table (tabular data is already in memory; re-export would duplicate work)
- You need to modify RAW file content (export is read-only; writing back to RAW requires different tools)
- Analysis requires real-time streaming access to raw detector signal during acquisition (export creates static snapshots post-acquisition)

## Inputs

- Thermo Fisher RAW mass spectrometry file (native binary format)
- MetaXtract object initialized with path to RAW file
- Scan number range or selection criteria (optional)

## Outputs

- CSV or TSV table of scan headers (MS1 and/or MS2) with instrument metadata, retention time, TIC, scan mode
- Parquet file of MS2 peak lists with columns: scan_number, mz_array, intensity_array, resolution_array, noises_array, baselines_array, charges_array
- Parquet file of MS1 peak lists with columns: scan_number, mz_array, intensity_array (with centroid/profile flag)
- Dictionary mapping scan_number → tuple of NumPy arrays (mz, intensity, [optional: resolution, noise, baseline, charge])

## How to apply

Call MetaXtract's export functions (ExportPeakList for MS2, ExportMS1PeakList for MS1) to write peak lists in Parquet or CSV format, where each row represents one scan and array columns store m/z, intensity, and optional technical arrays (resolution, noise, baseline, charge for MS2). For MS1, export includes m/z_array and intensity_array with centroid/profile flags. Separately export scan headers (MS1 and MS2) as CSV/TSV with selectable columns (Total Ion Current, Retention Time, Scan Mode, etc.). After export, validate that the output table contains the expected scan_number identifier column and non-empty array columns. Load exported Parquet files into Python using pandas.read_parquet() or the provided helper function to convert each scan row into a dictionary keyed by scan number with NumPy array tuples as values.

## Related tools

- **MetaXtract** (Primary tool for reading native Thermo Fisher RAW files and exporting peak lists and scan headers to tabular formats) — https://github.com/Rappsilber-Laboratory/MetaXtract
- **Python (pandas, NumPy, PyArrow)** (Libraries for loading exported Parquet/CSV files, parsing array columns, and converting to NumPy-backed structures for downstream analysis)

## Examples

```
from raw_parser import MetaXtract
raw = MetaXtract('path/to/file.RAW')
raw.ExportPeakList('ms2_peaklist.parquet')
raw.ExportMS1PeakList('ms1_peaklist.parquet')
raw.CloseRAWFile()
# Then load: df_ms2 = pd.read_parquet('ms2_peaklist.parquet')
```

## Evaluation signals

- Output CSV/TSV file is readable by pandas.read_csv() and contains non-empty scan metadata with expected columns (scan_number, retention_time, TIC, etc.)
- Output Parquet file is readable by pandas.read_parquet() and contains one row per scan with array-valued columns of consistent length (all m/z arrays match corresponding intensity array length)
- Scan number column is present, unique, and numeric; no NaN or duplicate scan IDs in output
- When loaded via the helper function, the returned dictionary keys match scan numbers in the Parquet file and all tuple values are NumPy arrays with dtype float64
- Row count in exported table matches the number of scans acquired (validate against CountMS2() or scan summary metadata)

## Limitations

- Parquet export of MS2 extended peak lists (resolution, noise, baseline, charge arrays) depends on Thermo RawFileReader populating those fields; some older RAW files or instrument configurations may have sparse or missing values in extended arrays.
- MS Method and LC Method extraction (GUI options) are not supported on Linux; only Parquet/CSV export of peak lists and scan headers is cross-platform.
- Array columns in Parquet are stored as nested structures; some external tools (e.g. spreadsheet software) may not render them natively; use Python or dedicated HDF5 viewers.
- Export does not include retention time alignment or intensity normalization; raw TIC and peak intensities are preserved as-recorded from the instrument.

## Evidence

- [readme] Exports data as: CSV / TSV, Parquet (peak lists), Interactive Plotly HTML reports: "Exports data as: CSV / TSV, Parquet (peak lists), Interactive Plotly HTML reports"
- [readme] MetaXtract exports MS1/MS2 peak lists as Parquet (or CSV) where each row represents one scan and stores arrays (m/z, intensities, etc.): "MetaXtract exports MS1/MS2 peak lists as **Parquet** (or CSV) where each row represents one scan and stores arrays (m/z, intensities, etc.)"
- [readme] Export MS2 extended peak list (Parquet): Per scan; mz_array, intensity_array, resolution_array, noises_array, baselines_array, charges_array: "**Export MS2 extended peak list (Parquet):** Per scan; `mz_array`, `intensity_array`, `resolution_array`, `noises_array`, `baselines_array`, `charges_array`."
- [readme] MS1 peak list with centroid/profile flag: "**Export MS1 peak list (Parquet):** Per scan; `mz_array`, `intensity_array` with centroid/profile flag."
- [readme] Writes a TSV file containing: Instrument details, Scan counts, Run statistics, Sample information: "**Writes a TSV file containing:** Instrument details, Scan counts, Run statistics, Sample information."
- [other] Convert the extracted data into a tabular format (CSV or pandas DataFrame) containing the mass-to-charge ratios, intensities, and scan metadata: "Convert the extracted data into a tabular format (CSV or pandas DataFrame) containing the mass-to-charge ratios, intensities, and scan metadata"
