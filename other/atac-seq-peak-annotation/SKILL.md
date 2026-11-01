---
name: atac-seq-peak-annotation
description: Use when after differential peak analysis (tl.diff_test) has identified peaks that differ in accessibility across cell types or conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0445
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0097
  tools:
  - SnapATAC2
  - tl.diff_test
  - datasets.cis_bp
  - Python
  - tl.motif_enrichment
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- tl.marker_regions, tl.diff_test for differential analysis
- datasets.cis_bp
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

# atac-seq-peak-annotation

## Summary

Annotate differentially accessible peaks from single-cell ATAC-seq data with transcription factor motifs and regulatory elements using SnapATAC2's motif enrichment workflow. This skill identifies which regulatory motifs are overrepresented in peak regions and computes statistical significance, enabling inference of transcriptional regulators driving chromatin accessibility differences.

## When to use

Apply this skill after differential peak analysis (tl.diff_test) has identified peaks that differ in accessibility across cell types or conditions. Use it to gain mechanistic insight into which transcription factors likely regulate the differentially accessible chromatin regions, particularly when you need to map peaks to specific regulatory proteins rather than just genes.

## When NOT to use

- Input peak set is from peak calling (tl.macs3) rather than differential analysis — use for differential peaks specifically, not all peaks in a dataset
- You need to map peaks to target genes or regulatory elements by proximity — use gene annotation tools (e.g. tl.marker_regions) instead
- The motif database is organism-specific (e.g. CIS-BP is curated for specific genomes) and your species/context is not well-covered

## Inputs

- Differentially accessible peak set (GRanges or BED-like object from tl.diff_test)
- Peak genomic sequences (FASTA or in-memory)
- CIS-BP motif database (position-weight matrices and motif metadata from datasets.cis_bp)

## Outputs

- Motif enrichment table (columns: motif_id, tf_name, enrichment_score, p_value, q_value)
- Motif occurrence coordinates within peak regions (optional detailed output)
- Background model statistics used for enrichment computation

## How to apply

Load differentially accessible peaks (output from tl.diff_test) as a feature set into SnapATAC2. Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight matrices. Invoke tl.motif_enrichment on the peak set, which scans for motif occurrences within the differential regions and computes enrichment statistics against a background model. The function returns a motif enrichment table containing motif IDs, TF names, enrichment scores, and p-values. Validate that all required columns are non-null, that p-values reflect statistical significance of motif overrepresentation (typically p < 0.05), and that enrichment scores indicate direction and magnitude of motif overrepresentation relative to background.

## Related tools

- **SnapATAC2** (Core framework providing tl.motif_enrichment function, differential peak analysis (tl.diff_test), and motif database loading) — https://github.com/scverse/SnapATAC2
- **tl.motif_enrichment** (Function that scans peaks for motif occurrences and computes enrichment statistics with p-values) — https://github.com/scverse/SnapATAC2
- **tl.diff_test** (Upstream function that identifies differentially accessible peaks; output serves as input to motif enrichment) — https://github.com/scverse/SnapATAC2
- **datasets.cis_bp** (SnapATAC2 dataset loader for CIS-BP motif database containing position-weight matrices and transcription factor metadata) — https://github.com/scverse/SnapATAC2
- **Python** (Programming language for executing SnapATAC2 workflows)

## Examples

```
import snapatac2 as snap; snap.tl.motif_enrichment(adata, motif_mat=snap.datasets.cis_bp(), peaks=diff_peaks, output_prefix='motif_enrichment')
```

## Evaluation signals

- Motif enrichment table contains non-null values for all required columns (motif_id, enrichment_score, p_value)
- P-values reflect valid statistical test output (range [0,1], distribution expected under null hypothesis)
- Enrichment scores are computed against an appropriate background model (e.g. dinucleotide-shuffled sequences or genome-wide background)
- Results pass multiple-testing correction (e.g. q-value or Benjamini-Hochberg FDR < 0.05) to identify significant motifs
- Top-ranked motifs are interpretable: correspond to known transcription factors relevant to the cell type or condition under study

## Limitations

- CIS-BP database coverage is limited to well-characterized organisms and transcription factors; rare or species-specific TFs may not be represented
- Motif enrichment identifies co-occurrence of binding sites but does not prove functional binding or transcriptional activity
- Background model assumption (e.g. dinucleotide composition matching) can affect enrichment scores; results are sensitive to choice of background
- Peak sequence quality and length affect motif detection; very short peaks or low-complexity sequences reduce power to detect motifs

## Evidence

- [other] Load differentially accessible peaks (output from tl.diff_test) as a feature set into SnapATAC2. Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight matrices. Invoke tl.motif_enrichment on the peak set, scanning for motif occurrences within differential regions and computing enrichment statistics against a background model.: "Load differentially accessible peaks (output from tl.diff_test) as a feature set into SnapATAC2. Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight"
- [other] Retrieve the resulting motif enrichment table containing motif IDs, enrichment scores, and p-values. Validate that all required columns are present and non-null, and that p-values reflect the statistical significance of motif overrepresentation.: "Retrieve the resulting motif enrichment table containing motif IDs, enrichment scores, and p-values. Validate that all required columns are present and non-null, and that p-values reflect the"
- [readme] End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis, regulatory network analysis.: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis"
- [methods] tl.motif_enrichment for motif analysis: "tl.motif_enrichment for motif analysis"
- [other] SnapATAC2 includes tl.motif_enrichment for motif analysis as part of its single-cell ATAC-seq analysis pipeline.: "SnapATAC2 includes tl.motif_enrichment for motif analysis as part of its single-cell ATAC-seq analysis pipeline."
