---
name: bedpe-format-handling
description: Use when your ChIP-Seq input is paired-end sequencing data stored in BEDPE format (e.g., CTCF_PE_ChIP_chr22_50k.bedpe.gz), and you need to estimate fragment length and call peaks while respecting the paired nature of the reads rather than treating them as independent single-end alignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - macs3 predictd
  - macs3 callpeak
  - macs3 pileup
derived_from:
- doi: 10.1186/gb-2008-9-9-r137
  title: macs
evidence_spans: []
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

# bedpe-format-handling

## Summary

Handle paired-end ChIP-Seq data in BEDPE format to preserve fragment pairing information through peak-calling workflows. BEDPE format encodes both read pairs as six-column tab-separated coordinates, enabling proper fragment length estimation and paired-end-aware pileup.

## When to use

Your ChIP-Seq input is paired-end sequencing data stored in BEDPE format (e.g., CTCF_PE_ChIP_chr22_50k.bedpe.gz), and you need to estimate fragment length and call peaks while respecting the paired nature of the reads rather than treating them as independent single-end alignments.

## When NOT to use

- Input is single-end ChIP-Seq data (use BED format instead with manual fragment length specification via --extsize)
- Fragment length is already known and fixed across the experiment (use -f BED with explicit --extsize parameter for faster processing)
- BEDPE file contains singletons or unpaired reads (filter or convert to BED first)

## Inputs

- BEDPE-format paired-end ChIP-Seq alignment file (gzip-compressed, e.g., .bedpe.gz)
- Control (input) sample in BEDPE format (optional but recommended for peak calling)

## Outputs

- Fragment length estimate (d) in base pairs
- narrowPeak file with peak coordinates and summit positions
- bedGraph intermediate pileup tracks

## How to apply

Pass the BEDPE file to macs3 predictd with the -f BEDPE flag to estimate average insertion length (fragment length d), which should be reported in base pairs (e.g., ~253 bp for the CTCF test data). Then run macs3 callpeak with -f BEDPE on the ChIP sample without specifying --extsize, allowing the pileup function to automatically handle paired-end fragment extent. Verify that the narrowPeak output file is generated with proper peak coordinates and summit positions. This workflow respects the original fragment boundaries encoded in the BEDPE coordinate pairs rather than requiring manual extension parameters.

## Related tools

- **macs3 predictd** (Estimate average insertion length (fragment length d) from paired-end ChIP sample) — https://github.com/macs3-project/MACS
- **macs3 callpeak** (Call peaks on paired-end ChIP-Seq data using BEDPE format to automatically extend fragments) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Generate pileup track for paired-end ChIP sample, handling fragment extent from BEDPE coordinates) — https://github.com/macs3-project/MACS

## Examples

```
macs3 predictd -i CTCF_PE_ChIP_chr22_50k.bedpe.gz -f BEDPE -g hs && macs3 callpeak -t CTCF_PE_ChIP_chr22_50k.bedpe.gz -c CTCF_Control_200K.bedpe.gz -f BEDPE -n ctcf_pe_peaks -g hs
```

## Evaluation signals

- macs3 predictd reports a fragment length estimate consistent with the expected insert size for the library preparation protocol (e.g., ~253 bp for standard CTCF ChIP)
- narrowPeak output file is generated with non-empty peak calls and summit coordinates within the peak regions
- bedGraph pileup tracks reflect fragment-aware coverage (peaks are broader and smoothed compared to single-end processing)
- No manual --extsize parameter was required in callpeak invocation, confirming automatic paired-end handling
- Peak positions and counts are reproducible and do not change when re-running on the same BEDPE input

## Limitations

- BEDPE format assumes all reads are properly paired; unpaired or singleton reads will be ignored or cause parsing errors
- Fragment length estimation (predictd) requires sufficient read depth in enriched regions; sparse or low-coverage data may yield unreliable d estimates
- BEDPE coordinate encoding depends on correct SAM-to-BEDPE conversion; downstream analysis quality is sensitive to conversion artifacts
- The paired-end aware pileup does not account for insert size variation beyond the point estimate of d; high variance in fragment length may reduce peak resolution

## Evidence

- [methods] if you run this on the `CTCF_PE_ChIP_chr22_50k.bedpe.gz` file in the test directory: "if you run this on the `CTCF_PE_ChIP_chr22_50k.bedpe.gz` file in the test directory"
- [other] Run macs3 predictd on the paired-end input file with -f BEDPE flag to estimate average insertion length (fragment length d), which should be reported as ~253 bp.: "Run macs3 predictd on the paired-end input file with -f BEDPE flag to estimate average insertion length (fragment length d), which should be reported as ~253 bp."
- [other] Run macs3 callpeak with -f BEDPE flag on the paired-end ChIP sample without specifying --extsize (pileup automatically handles paired-end fragment extent) to generate peak calls and intermediate bedGraph tracks.: "Run macs3 callpeak with -f BEDPE flag on the paired-end ChIP sample without specifying --extsize (pileup automatically handles paired-end fragment extent) to generate peak calls and intermediate"
- [other] Verify the narrowPeak output file is generated with proper peak coordinates and summit positions.: "Verify the narrowPeak output file is generated with proper peak coordinates and summit positions."
- [methods] This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data: "This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data"
