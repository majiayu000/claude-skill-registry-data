---
name: bam-to-bigwig-conversion
description: Use when after running TOBIAS ATACorrect to generate bias-corrected signal tracks from aligned ATAC-seq reads. Use this skill when you have corrected cutsite signal (as .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - bedtools genomecov / bedGraphToBigWig
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

# BAM-to-BigWig conversion

## Summary

Convert bias-corrected ATAC-seq signal data from BAM format to BigWig format for visualization and downstream footprinting analysis. This transformation enables efficient storage, scalable genome browser display, and preparation for footprint scoring.

## When to use

After running TOBIAS ATACorrect to generate bias-corrected signal tracks from aligned ATAC-seq reads. Use this skill when you have corrected cutsite signal (as .bw or equivalent intermediate format) that must be visualized across the genome or fed into footprint scoring tools like ScoreBigwig.

## When NOT to use

- Input is already in BigWig format—no conversion needed.
- Analysis goal is to call peaks or identify open chromatin regions; use peak-calling tools (e.g., MACS2) directly on aligned BAM instead.
- Working with raw, uncorrected ATAC-seq cutsite data for motif discovery without bias correction; apply ATACorrect first.

## Inputs

- Bias-corrected ATAC-seq signal data (as .bw output from TOBIAS ATACorrect, or intermediate cutsite BAM/bedGraph)
- Reference genome index or chrom.sizes file (for bedGraph-to-bigWig conversion if needed)

## Outputs

- BigWig (.bw) file containing bias-corrected signal track
- IGV/genome-browser compatible signal visualization

## How to apply

Following TOBIAS ATACorrect bias correction, the corrected signal output (stored initially as a bigWig file by ATACorrect itself) is ready for visualization and downstream analysis. ATACorrect natively outputs bias-corrected signal as a .bw file alongside uncorrected, bias model, and expected signal tracks. No additional conversion step is strictly required—ATACorrect produces the BigWig directly. However, if working with intermediate cutsite signals or custom corrected BAM files, conversion to BigWig can be achieved through standard genomic tools (e.g., bedtools, deeptools, or UCSC tools) that bin aligned reads into fixed-width windows and store normalized signal values. The resulting BigWig tracks preserve positional cutsite resolution while enabling rapid querying by genome browsers and footprinting downstream tools.

## Related tools

- **TOBIAS ATACorrect** (Produces bias-corrected signal as primary bigWig output; generates _corrected.bw file from aligned BAM and reference genome) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Consumes corrected bigWig tracks to calculate footprint scores within regulatory regions) — https://github.com/loosolab/TOBIAS
- **bedtools genomecov / bedGraphToBigWig** (Alternative tools for converting intermediate bedGraph or BAM-derived signal to bigWig if not using TOBIAS ATACorrect directly)

## Examples

```
TOBIAS ATACorrect --bam reads.bam --genome genome.fa --peaks peaks.bed --outdir ./corrected_tracks
```

## Evaluation signals

- Output file exists and is valid bigWig format (check header and chrom extent with `bigWigInfo` or similar utility).
- BigWig signal values align with corrected cutsite positions from the source BAM or intermediate track—spot-check a known footprint region.
- BigWig can be loaded into a genome browser (IGV, UCSC) without errors and displays expected ATAC-seq signal distribution.
- Downstream footprinting tools (TOBIAS ScoreBigwig, PlotAggregate, PlotHeatmap) successfully ingest the BigWig without format errors.
- Signal magnitude and range are consistent with the bias-corrected BAM read depth—no anomalous scaling artifacts.

## Limitations

- BigWig is a lossy format for some use cases; exact per-base read counts may be lost if binned at low resolution. For precise analysis, retain the original BAM.
- Conversion does not add new biological information—it is purely a format transformation for visualization and downstream tool compatibility.
- TOBIAS ATACorrect outputs multiple bigWig files (_uncorrected.bw, _bias.bw, _expected.bw, _corrected.bw); ensure you use the _corrected.bw for downstream footprinting, not the uncorrected or bias tracks.
- Single-cell ATAC-seq analysis requires pseudobulk aggregation (via SC-Framework) before conversion, as individual cell BAMs lack sufficient coverage for meaningful footprinting.

## Evidence

- [readme] Output files: - <outdir>/<prefix>_uncorrected.bw - <outdir>/<prefix>_bias.bw - <outdir>/<prefix>_expected.bw - <outdir>/<prefix>_corrected.bw: "Output files:
- <outdir>/<prefix>_uncorrected.bw
- <outdir>/<prefix>_bias.bw
- <outdir>/<prefix>_expected.bw
- <outdir>/<prefix>_corrected.bw"
- [other] Convert corrected signal to bigWig format for visualization and downstream footprinting analysis.: "Convert corrected signal to bigWig format for visualization and downstream footprinting analysis."
- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase.: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase."
- [intro] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
