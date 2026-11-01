---
name: macs3-subcommand-chaining
description: Use when when you have aligned ChIP-Seq reads (BED or BEDPE format) and a corresponding control sample, and you need explicit control over peak-calling parameters—including fragment-length prediction, local bias windows (d, slocal=1kb, llocal=10kb), background scaling, and score-cutoff.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - macs3 filterdup
  - macs3 predictd
  - macs3 pileup
  - macs3 bdgcmp
  - macs3 bdgopt
  - macs3 bdgpeakcall
derived_from:
- doi: 10.1186/gb-2008-9-9-r137
  title: macs
evidence_spans:
- we'll explain how you can accomplish this using the `filterdup` subcommand
- This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data
- generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand
- using the `bdgcmp` module, which outputs a score for each base pair in the genome
- apply the `bdgopt` subcommand
- identify regions that surpass a specific score cutoff using the `bdgpeakcall` function for narrow peak calling
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_macs
    doi: 10.1186/gb-2008-9-9-r137
    title: macs
  dedup_kept_from: coll_macs
schema_version: 0.2.0
---

# macs3-subcommand-chaining

## Summary

Reconstruct the MACS3 callpeak peak-calling pipeline by chaining individual subcommands (filterdup, predictd, pileup, bdgcmp, bdgopt, bdgpeakcall) to progressively transform ChIP-Seq BED/BEDPE reads into narrow peak calls. This skill enables fine-grained control over each step of duplicate filtering, fragment-length estimation, coverage pileup, local-background bias modeling, and statistical scoring.

## When to use

When you have aligned ChIP-Seq reads (BED or BEDPE format) and a corresponding control sample, and you need explicit control over peak-calling parameters—including fragment-length prediction, local bias windows (d, slocal=1kb, llocal=10kb), background scaling, and score-cutoff thresholds—rather than using the monolithic macs3 callpeak wrapper.

## When NOT to use

- You only have a single replicate and no control sample; local-bias modeling requires control data.
- Your input is already a peak file (BED, narrowPeak, or broadPeak); this skill is for generating peaks from raw reads.
- You are analyzing broad histone marks (e.g., H3K27me3); use macs3 bdgbroadcall instead of bdgpeakcall for the final step.
- Your reads are in formats other than BED/BEDPE (e.g., BAM); convert or use macs3 callpeak wrapper instead.

## Inputs

- ChIP-Seq aligned reads in BED format (e.g., CTCF_ChIP_200K.bed.gz)
- Control sample aligned reads in BED format (e.g., CTCF_Control_200K.bed.gz)
- Genome size (human: 2.7e9 bp, or -g hs flag)
- Fragment-length search range (e.g., -m 5 50 for 5–50 bp)

## Outputs

- Duplicate-filtered ChIP BED file with final read count
- Duplicate-filtered control BED file with final read count
- Predicted fragment length d (integer)
- ChIP pileup BEDGRAPH track (coverage at fragment-length extension)
- Control d-background BEDGRAPH (d-extended control pileup)
- Control slocal-background BEDGRAPH (1 kb local window)
- Control llocal-background BEDGRAPH (10 kb local window)
- Normalized slocal BEDGRAPH (d/slocal-scaled)
- Normalized llocal BEDGRAPH (d/llocal-scaled)
- Combined maximum-bias BEDGRAPH (max of d, slocal, llocal)
- Scaled local-lambda BEDGRAPH (lambda scaled to ChIP sequencing depth)
- Score BEDGRAPH (q-value or p-value track from bdgcmp)
- Narrow peaks BED file (regions above score cutoff)

## How to apply

Begin by filtering duplicate reads from both ChIP and control BED files using macs3 filterdup with --keep-dup=1 to record final read counts. Estimate fragment length d from the filtered ChIP sample using macs3 predictd with genome size (-g hs) and d-range parameters (-m 5 50). Generate ChIP pileup by extending reads to the predicted fragment length using macs3 pileup with --extsize. Build local bias by creating three background tracks from control: d-extension (direct), slocal (1 kb window), and llocal (10 kb window), each generated via macs3 pileup -B with corresponding --extsize values, then normalize slocal and llocal using macs3 bdgopt multiply with scaling factors (d/slocal and d/llocal). Combine backgrounds by computing the maximum across the three tracks using sequential macs3 bdgcmp -m max operations, then add genome-wide background (control_reads × d / genome_size) via macs3 bdgopt. Scale the local lambda bias to match ChIP sequencing depth using macs3 bdgopt multiply with the ratio of final ChIP to control read counts. Compare ChIP pileup against scaled lambda using macs3 bdgcmp with -m qpois (for q-values) or -m ppois (for p-values) to generate score BEDGRAPH. Finally, call narrow peaks from the score track using macs3 bdgpeakcall with a score cutoff (e.g., -c 1.301 for q-value 0.05), minimum peak length -l set to d, and gap parameter -g set to the read length.

## Related tools

- **macs3 filterdup** (Remove redundant reads at each genomic location from ChIP and control BED files) — https://github.com/macs3-project/MACS
- **macs3 predictd** (Estimate fragment length d from filtered ChIP data using cross-correlation analysis) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Generate coverage BEDGRAPH tracks by extending reads to fragment length d (ChIP) or building control backgrounds) — https://github.com/macs3-project/MACS
- **macs3 bdgcmp** (Compare ChIP pileup against local-lambda background using Poisson or q-value models to generate score tracks) — https://github.com/macs3-project/MACS
- **macs3 bdgopt** (Normalize, scale, and combine BEDGRAPH tracks (multiply, add operations) for local-bias and depth normalization) — https://github.com/macs3-project/MACS
- **macs3 bdgpeakcall** (Identify narrow peaks from score BEDGRAPH by filtering regions above a score cutoff with minimum length and gap constraints) — https://github.com/macs3-project/MACS

## Examples

```
macs3 filterdup -i CTCF_ChIP_200K.bed.gz --keep-dup=1 -o CTCF_ChIP_filtered.bed && macs3 predictd -i CTCF_ChIP_filtered.bed -g hs -m 5 50 && macs3 pileup -i CTCF_ChIP_filtered.bed --extsize 100 -o CTCF_ChIP_pileup.bedgraph && macs3 pileup -i CTCF_Control_200K.bed.gz -B --extsize 100 -o CTCF_Control_d.bedgraph && macs3 bdgcmp -t CTCF_ChIP_pileup.bedgraph -c CTCF_Control_d.bedgraph -m qpois -o CTCF_qvalue.bedgraph && macs3 bdgpeakcall -i CTCF_qvalue.bedgraph -c 1.301 -l 100 -g 50 -o CTCF_peaks.narrowPeak
```

## Evaluation signals

- Final ChIP and control read counts are equal after filtering (indicating consistent duplicate handling); record counts from macs3 filterdup output.
- Predicted fragment length d is biologically plausible (typically 100–300 bp for nucleosome-binding proteins) and matches cross-correlation peak from macs3 predictd.
- ChIP pileup BEDGRAPH spans the full genome with non-negative float values representing normalized coverage; inspect first 10 lines for valid coordinates and values.
- Local-bias BEDGRAPH files (d, slocal, llocal) have identical coordinate ranges and all values are ≥ 0 after normalization via bdgopt.
- Score BEDGRAPH (q-value or p-value) contains regions where enriched peaks show scores above the chosen cutoff (e.g., q-value < 0.05 = score > 1.301); verify histogram of scores is bimodal with a peak near zero.
- Final peak BED file has 3+ columns (chrom, start, end) with no overlapping intervals, peak widths are ≥ d (fragment length), and peak counts are reasonable (typically 1000–50000 for transcription factors like CTCF).

## Limitations

- Fragment-length prediction (macs3 predictd) requires sufficient ChIP enrichment; weak or diffuse signals may yield unreliable d estimates; cross-correlation plots should be visually inspected.
- Local-bias modeling assumes control and ChIP samples are sequenced to similar depth; large imbalances in sequencing depth require manual re-scaling before bdgopt or will skew background estimates.
- Peak-calling cutoff (-c flag in bdgpeakcall) must be manually chosen based on desired false-discovery rate (e.g., -c 1.301 for FDR q-value 0.05); no automatic cutoff selection is provided.
- The pipeline assumes single-end or properly paired-end reads; mixed or corrupted BEDPE files may cause failures in fragment-length estimation or pileup.
- Memory and runtime scale with genome size and sequencing depth; 200k reads (test data) processes in seconds, but whole-genome human ChIP-Seq (>10M reads) may require hours and several GB RAM.

## Evidence

- [other] The MACS3 callpeak pipeline operates through sequential subcommands: filterdup removes duplicate reads, predictd estimates fragment length d from ChIP data, pileup generates coverage tracks, bdgcmp compares ChIP and control signals to compute p/q-value scores, bdgopt applies optimization to score tracks, and bdgpeakcall identifies peaks by filtering regions above a score cutoff.: "The MACS3 callpeak pipeline operates through sequential subcommands: filterdup removes duplicate reads, predictd estimates fragment length d from ChIP data, pileup generates coverage tracks, bdgcmp"
- [methods] MACS3 does offer a range of subcommands that allow you to customize every step of your analysis: "MACS3 does offer a range of subcommands that allow you to customize every step of your analysis"
- [methods] In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location: "In the initial step of ChIP-Seq analysis with `callpeak`, we read both ChIP and control data and remove redundant reads from each genomic location"
- [methods] This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data: "This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data"
- [methods] By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background: "By default, the MACS3 `callpeak` function calculates local bias by considering the maximum bias from the surrounding 1kb, 10kb, the fragment length `d`, and the whole genome background"
- [methods] To ensure accurate comparison between ChIP and control signals, both must be scaled to the same sequencing depth: "To ensure accurate comparison between ChIP and control signals, both must be scaled to the same sequencing depth"
- [methods] To identify enriched regions and predict peaks, the ChIP signals and local lambda stored in the BEDGRAPH file must be compared using a statistical model: "To identify enriched regions and predict peaks, the ChIP signals and local lambda stored in the BEDGRAPH file must be compared using a statistical model"
- [methods] The final step in peak calling is to identify regions that surpass a specific score cutoff using the `bdgpeakcall` function: "The final step in peak calling is to identify regions that surpass a specific score cutoff using the `bdgpeakcall` function"
