---
name: bigwig-signal-processing
description: Use when after bias correction of ATAC-seq reads (via ATACorrect) when you have a bias-corrected bigWig file and need to measure transcription factor footprint strength within defined accessible regions (peaks, motif sites, or called footprint boundaries).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0654
  tools:
  - TOBIAS
  - ATACorrect
  - ScoreBigwig
  - BINDetect
  - PlotAggregate
derived_from:
- doi: 10.1038/s41467-020-18035-1
  title: tobias
evidence_spans:
- '**TOBIAS** is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tobias
    doi: 10.1038/s41467-020-18035-1
    title: tobias
  dedup_kept_from: coll_tobias
schema_version: 0.2.0
---

# bigwig-signal-processing

## Summary

Convert bias-corrected ATAC-seq cutsite signal into per-base footprint scores by measuring insertion depletion patterns within accessible chromatin regions using bigWig format. This skill quantifies transcription factor occupancy by computing the magnitude of Tn5 insertion depletion at each genomic position.

## When to use

Apply this skill after bias correction of ATAC-seq reads (via ATACorrect) when you have a bias-corrected bigWig file and need to measure transcription factor footprint strength within defined accessible regions (peaks, motif sites, or called footprint boundaries). Use it as the intermediate step between bias-corrected signal and downstream binding site detection or visualization.

## When NOT to use

- Input bigWig file has not been bias-corrected for Tn5 transposase sequence preference—raw or only-quantile-normalized ATAC-seq signal will produce misleading footprint scores.
- No defined set of accessible regions is available; ScoreBigwig requires a BED file of boundaries and cannot discover footprints de novo.
- The analysis goal is only visualization or aggregate signal inspection—simpler tools like PlotAggregate may be more direct without computing per-base scores.

## Inputs

- bias-corrected bigWig file (*.bw)
- accessible chromatin regions in BED format (peaks, motifs, or footprint regions)

## Outputs

- footprint score bigWig file (*.bw) with per-base depletion magnitude scores

## How to apply

Load the bias-corrected bigWig file (output from ATACorrect, typically named *_corrected.bw) and provide a set of accessible genomic regions in BED format (ATAC-seq peaks, motif regions, or previously defined footprint boundaries). Use TOBIAS ScoreBigwig to compute footprint scores by measuring signal depletion—the tool aggregates the corrected insertion signal within each region and outputs a new bigWig file where each position's value reflects the magnitude of the local depletion pattern characteristic of protein-DNA binding. Validate the output bigWig for correct format (proper header, coordinate system consistency) and non-empty score distributions across regions; scores should show characteristic troughs at true binding sites and elevated signal in flanking regions.

## Related tools

- **ATACorrect** (upstream bias-correction step that produces the bias-corrected bigWig input required by ScoreBigwig) — https://github.com/loosolab/TOBIAS/wiki/ATACorrect
- **ScoreBigwig** (core TOBIAS tool that performs footprint score calculation from corrected cutsites) — https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig
- **BINDetect** (downstream tool for differential binding estimation using the computed footprint scores) — https://github.com/loosolab/TOBIAS/wiki/BINDetect
- **PlotAggregate** (visualization tool to validate footprint scores by plotting aggregated signal across regions) — https://github.com/loosolab/TOBIAS/wiki/PlotAggregate

## Examples

```
TOBIAS ScoreBigwig --signal corrected.bw --regions peaks.bed --output footprint_scores.bw
```

## Evaluation signals

- Output bigWig file is valid format (proper UCSC bigWig header, correct chromosome/coordinate system) and is non-empty across all input regions.
- Score distribution shows expected depletion pattern: characteristic troughs (negative or reduced values) at known transcription factor binding sites and elevated signal flanking those sites.
- Per-base scores are numerical and span a consistent range; extreme outliers or NaN values suggest malformed input regions or empty signal regions.
- Aggregate footprint plots (via PlotAggregate) show clear asymmetric depletion patterns centered on motif positions, indicating scores capture genuine protein-induced signal depletion.
- Scores correlate with transcription factor binding status in downstream BINDetect analysis (bound sites show stronger depletion scores than unbound sites).

## Limitations

- ScoreBigwig requires pre-defined region boundaries (BED file); it cannot discover footprints de novo and will produce scores only within provided regions.
- Quality of footprint scores depends critically on upstream bias correction quality; insufficient or incorrect ATACorrect output will propagate errors into score calculation.
- The method assumes a characteristic depletion signature around binding sites; weak or absent footprints (e.g., in low-accessibility regions or with transient binding) may not produce interpretable scores.
- TOBIAS was originally developed for bulk ATAC-seq; application to single-cell data requires pseudobulk aggregation by cell type, and quality of clusters and cell counts significantly affect footprint clarity.

## Evidence

- [other] Apply ScoreBigwig (part of TOBIAS) to compute footprint scores by measuring signal depletion within each region, generating a bigWig output where each position reflects the magnitude of the observed insertion depletion pattern.: "Apply ScoreBigwig (part of TOBIAS) to compute footprint scores by measuring signal depletion within each region, generating a bigWig output where each position reflects the magnitude of the observed"
- [intro] The local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as footprints: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [readme] ScoreBigwig: Calculate footprint scores from corrected cutsites: "ScoreBigwig: Calculate footprint scores from corrected cutsites"
- [readme] Correction of Tn5 insertion bias, Calculation of footprint scores within regulatory regions: "Correction of Tn5 insertion bias
- Calculation of footprint scores within regulatory regions"
- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase.: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase."
