---
name: bedgraph-file-export
description: Use when after computing per-bin coverage depth using cooltools.coverage() on a loaded cooler object, when you need to (1) share the coverage track with non-Python tools, (2) visualize it in a genome browser, or (3) integrate it with downstream analyses that expect bedGraph or tabular input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_0092
  tools:
  - cooltools
  - cooler
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- cooltools provides a suite of computational tools with a paired python API
- cooltools leverages this format to enable flexible and reproducible analysis of high-resolution data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# bedgraph-file-export

## Summary

Export per-bin sequencing depth (coverage) computed from cooler Hi-C files to bedGraph or tabular (CSV/TSV) format for downstream visualization and analysis. This skill bridges in-memory coverage track objects to portable, coordinate-annotated text formats.

## When to use

After computing per-bin coverage depth using cooltools.coverage() on a loaded cooler object, when you need to (1) share the coverage track with non-Python tools, (2) visualize it in a genome browser, or (3) integrate it with downstream analyses that expect bedGraph or tabular input. Use this when your analysis requires bin coordinates alongside coverage values in a human-readable or browser-compatible format.

## When NOT to use

- Input is already a bedGraph or coordinate-annotated tabular file; use direct format conversion instead.
- Coverage has not been computed or cooler object is not loaded; compute coverage first using cooltools.coverage().
- Analysis requires in-memory array operations or sparse matrix format; keep coverage as a Python object rather than exporting to disk.

## Inputs

- cooler file (.cool or .mcool HDF5 format)
- coverage track object (output from cooltools.coverage())
- bin table with genomic coordinates (chrom, start, end)

## Outputs

- bedGraph file (4-column: chrom, start, end, coverage)
- CSV or TSV table with bin coordinates and coverage values

## How to apply

Following cooltools.coverage() computation, the resulting coverage track object contains per-bin sequencing depth values indexed by bin coordinates. Export this to bedGraph format (with columns: chromosome, start, end, coverage value) or tabular format (CSV/TSV with bin metadata and coverage) by iterating over bins, retrieving their genomic coordinates from the cooler file's bin table, pairing them with coverage values, and writing to file. Validate the output by checking (a) row count matches the number of bins in the cooler, (b) coordinate ranges are contiguous and non-overlapping, and (c) coverage values are numeric and within expected range (non-negative, typically matching total contact counts per bin).

## Related tools

- **cooltools** (Computes per-bin sequencing depth (coverage) from cooler files via cooltools.coverage() function) — https://github.com/open2c/cooltools
- **cooler** (Loads and provides access to Hi-C cooler file format, including bin table with genomic coordinates) — https://github.com/open2c/cooler
- **Python** (Programming language for iterating over coverage tracks and writing formatted output)

## Examples

```
import cooltools; import cooler; c = cooler.Cooler('sample.cool'); cov = cooltools.coverage(c); import pandas as pd; bins = c.bins[:]; cov_df = pd.DataFrame({'chrom': bins['chrom'], 'start': bins['start'], 'end': bins['end'], 'value': cov}); cov_df.to_csv('coverage.bedgraph', sep='\t', header=False, index=False)
```

## Evaluation signals

- Output file row count equals total number of bins in the cooler (excluding any filtered/masked bins if applicable).
- bedGraph coordinates (chrom, start, end) match bin table entries from the cooler; no gaps or overlaps between consecutive bins.
- Coverage values are numeric, non-negative, and sum/distribution is consistent with total contact counts per bin in the original cooler.
- File format is valid bedGraph (4 tab-separated columns) or TSV/CSV (header row, consistent column count, proper delimiters).
- bedGraph can be successfully parsed and visualized by genome browsers (e.g. UCSC Genome Browser, IGV) without format errors.

## Limitations

- bedGraph export requires explicit iteration over bins; for very large coolers (>1M bins), file I/O and memory may become a bottleneck.
- Output file size can be substantial; a large cooler at fine resolution (e.g. 1 kb bins) may produce multi-GB bedGraph files.
- cooler file must contain a valid bin table; corrupted or incomplete coolers will produce invalid coordinate output.
- Coverage values are tied to the bin resolution of the source cooler; changing resolution requires recomputing coverage, not re-exporting.

## Evidence

- [other] Call cooltools.coverage() on the loaded cooler object to compute per-bin sequencing depth, optionally specifying whether to store total cis counts in the cooler as indicated in the function signature.: "Call cooltools.coverage() on the loaded cooler object to compute per-bin sequencing depth, optionally specifying whether to store total cis counts in the cooler"
- [other] Export the resulting coverage track to bedGraph or tabular format (CSV/TSV) containing bin coordinates and coverage values.: "Export the resulting coverage track to bedGraph or tabular format (CSV/TSV) containing bin coordinates and coverage values."
- [other] Validate the output file format and row counts match expected documentation.: "Validate the output file format and row counts match expected documentation."
- [intro] The recently-introduced cooler format readily handles storage of high-resolution datasets: "The recently-introduced cooler format readily handles storage of high-resolution datasets"
