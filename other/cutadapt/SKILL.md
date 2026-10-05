---
name: cutadapt
description: Adapter, primer, and poly-A/T trimming for high-throughput sequencing reads (FASTQ/FASTA). Use for ATAC-seq (Nextera adapter removal), ChIP-seq/CUT&RUN, small RNA-seq (preserving reads as short as ~18 nt), and amplicon/primer trimming where exact or linked adapter sequences matter more than fastp's heuristic auto-detection. Covers 3'/5'/linked adapters, IUPAC wildcards, paired-end synchronization, quality/length filtering, and demultiplexing by barcode.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
compatibility: Requires Python 3.10+ and cutadapt 5.x (current 5.2; Python 3.9 support was dropped in 5.2, released 2025-10-23). Depends on dnaio>=1.2.3 and xopen>=1.6.0, installed automatically via pip/conda; bioconda provides prebuilt binaries including ARM64 macOS.
metadata: {"version": "1.0", "skill-author": "community"}
---

# Cutadapt

## Overview

Cutadapt finds and removes adapter sequences, primers, poly-A tails, and other unwanted sequence from sequencing reads in an error-tolerant way (configurable mismatch/indel rate), and can filter, trim by quality/length, or demultiplex reads at the same time. It differs from heuristic auto-detecting trimmers (e.g. `fastp`) by requiring you to specify the adapter/primer sequence(s) — which makes it the right tool whenever the adapter is known and exact matching matters: Nextera adapters in ATAC-seq, 3' adapters in small-RNA-seq, PCR primers in amplicon sequencing, or barcodes for demultiplexing.

## Installation

```bash
uv pip install cutadapt
# or
conda install -c bioconda cutadapt
```

Check version: `cutadapt --version` (targets the 5.x series; flag behavior below matches 5.0+ — see pitfalls for what changed at the 5.0 major bump).

## When to Use vs. fastp

| | cutadapt | fastp |
|---|---|---|
| Adapter specification | Explicit sequence(s), IUPAC wildcards, linked adapters | Auto-detected (overlap analysis) or explicit |
| Best for | ATAC-seq Nextera, small-RNA 3' adapters, amplicon primers, barcode demultiplexing | General-purpose QC + trim in one pass, unknown/mixed adapters |
| Paired-end adapter correction | Yes (`--pair-filter`, linked adapters spanning both reads) | Yes, via overlap detection |

Use both in the same pipeline if useful: `fastp` for general QC/deduplication, `cutadapt` for precise, sequence-specific adapter/primer removal.

## Adapter Types

- `-a ADAPTER` — 3' adapter (trims the adapter and everything after it).
- `-g ADAPTER` — 5' adapter (trims the adapter and everything before it).
- `-b ADAPTER` — either end (searches both).
- Anchored: `-g ^ADAPTER` (must be at the very start) / `-a ADAPTER$` (must be at the very end) — much faster and less error-prone for known-position primers/barcodes.
- Linked adapters (both ends of a fragment, e.g., amplicon primers): `-g ^PRIMER1...PRIMER2$` or via `--pair-adapters`.
- IUPAC wildcards are supported in adapter sequences (`N`, `R`, `Y`, etc.).
- Multiple adapters: repeat `-a`/`-g` — cutadapt tries all and reports which one matched (used for demultiplexing).

## Quick Start: Single-End

```bash
cutadapt \
  -a AGATCGGAAGAGC \
  -o trimmed.fastq.gz \
  input.fastq.gz \
  > report.txt
```

## Paired-End

```bash
cutadapt \
  -a AGATCGGAAGAGC -A AGATCGGAAGAGC \
  -o trimmed_R1.fastq.gz -p trimmed_R2.fastq.gz \
  input_R1.fastq.gz input_R2.fastq.gz
```

Lowercase flags (`-a`, `-g`, `-b`, `-q`) apply to R1; uppercase (`-A`, `-G`, `-B`, `-Q`) apply to R2. Cutadapt keeps R1/R2 synchronized automatically — never trim the two files independently with separate commands, or read order/pairing breaks.

## Quality, Length, and N Filtering

```bash
# -q 20,20    trim low-quality bases from both ends (Phred cutoff)
# -m 20       discard reads shorter than 20nt after trimming
# --max-n 0.1 discard reads with too many Ns
cutadapt \
  -a AGATCGGAAGAGC \
  -q 20,20 \
  -m 20 \
  --max-n 0.1 \
  -o trimmed.fastq.gz input.fastq.gz
```

Common companions: `--discard-untrimmed` (keep only reads where the adapter was actually found — useful for amplicon primer confirmation), `--trim-n` (strip trailing Ns), `-u 10` (unconditionally cut 10 bases from the 5' end, e.g. a fixed UMI/spacer).

## Demultiplexing

```bash
cutadapt \
  -g file:barcodes.fasta \
  -o "trimmed-{name}.fastq.gz" \
  input.fastq.gz
```

`barcodes.fasta` holds one named barcode sequence per record; cutadapt writes a separate output file per matched barcode (`{name}` is substituted), plus an `unknown` bucket for unmatched reads.

## Small RNA / Poly-A Specifics

```bash
# Small RNA: keep short reads, trim the 3' adapter, discard anything too short to be biological signal
cutadapt -a TGGAATTCTCGGGTGCCAAGG -m 18 -M 30 -o trimmed.fastq.gz input.fastq.gz

# Poly-A tail removal (RNA-seq) — --poly-a supersedes the older `-a "A{100}"` recipe
cutadapt --poly-a -o trimmed.fastq.gz input.fastq.gz
```

## Multi-Core and Reports

```bash
cutadapt -j 8 -a AGATCGGAAGAGC -o trimmed.fastq.gz input.fastq.gz   # -j 0 = auto-detect cores
cutadapt --json=report.json -a AGATCGGAAGAGC -o trimmed.fastq.gz input.fastq.gz
```

`--json` reports (adapter match counts, length histograms) feed cleanly into MultiQC. `--info-file=info.txt` (and `--info-file-paired` for R2) writes one line per read documenting exactly what was trimmed — useful for debugging unexpected trimming behavior.

## Common Pitfalls

- **Version 5.0 changed default compression and demux behavior.** Since 5.0, default gzip compression level dropped from 5 to 1 (faster, larger intermediate files — fine since they're usually deleted downstream; use `--compression-level=5` to match pre-5.0 output size). Also since 5.0, multi-adapter/barcode matches that are *ambiguous* between two adapters are no longer arbitrarily assigned to one — they go to `unknown` instead, which can silently increase your "unmatched" bucket size if you're comparing against older-cutadapt pipelines.
- **Running R1/R2 through separate invocations.** Always trim paired files together with `-o`/`-p` in one command; separate commands can desynchronize which reads survive filtering in each file.
- **Not anchoring adapters that are always at a fixed position.** Un-anchored search is slower and occasionally matches spuriously in the middle of a read; use `^`/`$` anchoring for primers/barcodes you know are at the read boundary.
- **Confusing `-a`/`-g` orientation.** `-a` trims the adapter *and everything after*; `-g` trims the adapter *and everything before*. Getting this backwards silently drops the biologically relevant part of the read instead of the adapter.
- **Forgetting `--discard-untrimmed` for amplicon work.** Without it, reads where the primer wasn't found are kept untrimmed rather than removed, which can leak primer-less off-target reads into downstream analysis.
- **Python floor.** cutadapt 5.2 dropped Python 3.9; pin `cutadapt<5.2` if you must run on 3.9, or upgrade the environment.

## Resources

- Docs: https://cutadapt.readthedocs.io/
- Changelog: https://cutadapt.readthedocs.io/en/stable/changes.html
- Source: https://github.com/marcelm/cutadapt
- Citation: Martin, M. (2011). Cutadapt removes adapter sequences from high-throughput sequencing reads. *EMBnet.journal*, 17(1), 10-12. DOI: 10.14806/ej.17.1.200
