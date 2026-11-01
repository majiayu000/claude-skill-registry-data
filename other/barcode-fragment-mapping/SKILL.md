---
name: barcode-fragment-mapping
description: Use when you have a coordinate-sorted BAM file from a single-cell ATAC-seq experiment (especially 10X Genomics platforms) and need to extract per-fragment information including cell barcodes, fragment coordinates, and quality metrics for downstream analysis in SnapATAC2 or compatible tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3199
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_3169
  tools:
  - SnapATAC2
  - Python
  - Rust
  - precellar
  - samtools
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_snapatac2
    doi: 10.1038/s41592-023-02139-9
    title: snapatac2
  dedup_kept_from: coll_snapatac2
schema_version: 0.2.0
---

# barcode-fragment-mapping

## Summary

Convert coordinate-sorted BAM files into compressed fragment files with cell barcode and quality annotations using SnapATAC2's pp.make_fragment_file. This preprocessing step is essential for single-cell ATAC-seq analysis, enabling efficient storage and downstream processing of chromatin accessibility data.

## When to use

You have a coordinate-sorted BAM file from a single-cell ATAC-seq experiment (especially 10X Genomics platforms) and need to extract per-fragment information including cell barcodes, fragment coordinates, and quality metrics for downstream analysis in SnapATAC2 or compatible tools.

## When NOT to use

- Input BAM file is not coordinate-sorted; use samtools sort to order by chromosome and position first.
- Fragment file already exists in validated BED.gz or zst format; re-processing is redundant.
- Data source is unstranded or non-ATAC-seq (e.g., whole-genome bisulfite sequencing); barcode-fragment mapping assumes paired-end ATAC-seq reads with valid cell barcodes.

## Inputs

- coordinate-sorted BAM file
- 10X Genomics BAM file (optional source specification)

## Outputs

- compressed fragment file (BED.gz or .zst format)
- fragment metadata with barcode annotations
- QC metrics (duplication rate, read count)

## How to apply

Load the coordinate-sorted BAM file and invoke pp.make_fragment_file with source='10x' if processing 10X BAM input, or with default settings for standard BAM files. The function generates a compressed fragment file (BED.gz or zst format) containing canonical BED fields (chrom, start, end) plus barcode and count columns. After execution, validate output file integrity by confirming non-empty content, verifying BED format compliance, and checking that QC metrics (duplication rate, read counts) are computed and accessible via the output metadata. The compressed output enables scalable processing of large cell numbers while preserving fragment-level information needed for tile matrix construction and peak calling.

## Related tools

- **SnapATAC2** (Python/Rust package providing pp.make_fragment_file for BAM-to-fragment conversion and downstream single-cell ATAC-seq analysis) — https://github.com/scverse/SnapATAC2
- **precellar** (Universal preprocessing pipeline for generating fragment files (.tsv.zst) from raw FASTQ for multiple single-cell ATAC-seq platforms) — https://github.com/regulatory-genomics/precellar
- **samtools** (Utilities for BAM sorting and validation prior to fragment file conversion)

## Examples

```
import snapatac2 as snap; snap.pp.make_fragment_file(bam='sample.bam', output='fragments.tsv.zst', source='10x')
```

## Evaluation signals

- Output fragment file is non-empty and has file size proportional to input BAM complexity.
- Fragment file header and all rows conform to BED format (chrom, start, end as tab-separated columns; start and end are numeric; coordinates in [0, chromosome_length)).
- Barcode column contains valid cell identifiers present in the BAM header.
- Count column contains positive integers reflecting fragment observation frequency.
- QC metrics (computed duplication rate, read count totals) are logically consistent with input BAM statistics and are accessible via file metadata or log output.

## Limitations

- Requires input BAM to be coordinate-sorted; unsorted input will produce incorrect or incomplete fragment files.
- Cell barcode extraction assumes barcodes are properly encoded in BAM tags (typically CB or CR field); malformed or missing barcodes will result in loss of barcode information.
- Compression format (BED.gz vs. zst) must match downstream tool expectations; incompatible format can prevent downstream import.
- Quality metrics are computed during conversion; re-running on the same input BAM will not update metrics if the tool caches outputs.

## Evidence

- [intro] BAM-to-fragment files conversion: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
- [methods] pp.make_fragment_file function and workflow: "BAM/Fragment file processing with pp.make_fragment_file, pp.import_fragments"
- [other] Fragment file format and content: "Generate fragment file output in compressed format (BED.gz or zst) containing fragment coordinates, cell barcodes, and quality metrics."
- [other] Validation and QC verification: "Verify output file integrity and confirm QC metrics (duplication rate, read counts) are computed and accessible."
- [other] 10X BAM source support: "Invoke pp.make_fragment_file with source='10x' if the input is a 10X BAM file, or with default settings for standard BAM inputs."
- [readme] Multi-platform support via precellar: "This tool is an automated pipeline for preprocessing single-cell genomics data. It is designed to take raw data (fastq files) from a variety of single-cell genomics platforms and a seqspec file as"
