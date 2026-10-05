---
name: pybigwig
description: Fast Python I/O for BigWig (continuous genome signal) and BigBed (interval annotation) files via libBigWig. Use for random-access signal queries at specific genomic coordinates (bw.values, bw.stats), computing per-region summary statistics (mean/max/coverage) over a BED file of regions, writing custom BigWig tracks from numpy arrays, and loading ChIP-seq/ATAC-seq/RNA-seq/methylation coverage tracks (e.g. produced by deeptools bamCoverage) into pandas/numpy for downstream analysis or ML feature extraction. Complements deeptools (which generates BigWig files) and chip-seq/atac-seq workflows.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
compatibility: Requires Python 3.9+ and pyBigWig 0.3.x (current 0.3.25). This is a C extension over libBigWig — bioconda ships prebuilt packages for linux-64, linux-aarch64, osx-64 and osx-arm64, while PyPI ships manylinux x86_64 wheels only, so `pip install pyBigWig` builds from source on macOS; that build needs libcurl and zlib headers (`curl-config` on PATH), which macOS supplies in the SDK.
metadata: {"version": "1.0", "skill-author": "community"}
---

# pyBigWig

## Overview

BigWig files are the standard binary format for genome-wide continuous signal (read depth, fold enrichment, log2 ratio, per-CpG methylation) — the typical output of `deeptools bamCoverage`/`bamCompare`. BigBed files store interval annotations (peaks, genes) with optional scores in the same indexed binary family. pyBigWig is a thin, fast C-extension wrapper around `libBigWig` that gives you random access to either format: fetch signal for an arbitrary region in milliseconds without loading the whole (often multi-GB) file into memory.

Use it whenever an analysis needs to go *beyond* what deeptools' CLI already covers — pulling signal at custom coordinates for a model, correlating ChIP enrichment with expression at specific genes, or building a signal-aggregation plot with your own binning logic.

## Installation

```bash
uv pip install pyBigWig
# or, to skip the libcurl/zlib build requirement entirely:
conda install -c bioconda -c conda-forge pybigwig
```

Import as `import pyBigWig` (mixed-case module name, despite the lowercase PyPI/conda package listing `pybigwig`).

## When to Use

- Extracting signal values at specific genomic coordinates for downstream ML feature vectors (e.g., ATAC-seq accessibility at a set of candidate enhancers).
- Computing summary statistics (mean/max/coverage) over a custom BED of regions — differential peaks, gene bodies, TSS windows — without going back through the deeptools CLI.
- Writing a BigWig track from a numpy array or custom per-base signal you've computed in Python.
- Streaming through a BigWig/BigBed without materializing the whole file (chromosome-by-chromosome iteration).
- Opening a BigWig directly from an HTTPS/FTP URL (e.g., a public ENCODE or UCSC track) without downloading it first.

## Opening a File

```python
import pyBigWig

bw = pyBigWig.open("sample.bw")            # read mode (default)
bw_remote = pyBigWig.open("https://.../track.bw")   # remote access works transparently
bwrite = pyBigWig.open("output.bw", "w")   # write mode — can ONLY be written to, not queried
```

`pyBigWig.open()` raises `RuntimeError: Received an error during file opening!` if the file doesn't exist, isn't a valid BigWig/BigBed, or is an unreachable URL — it never returns `None`, so wrap it in `try`/`except RuntimeError` rather than testing the handle.

## Reading: Header and Chromosomes

```python
print(bw.isBigWig(), bw.isBigBed())
print(bw.chroms())          # {'chr1': 248956422, 'chr2': 242193529, ...}
print(bw.chroms("chr1"))    # 248956422
print(bw.header())          # nBasesCovered, minVal, maxVal, sumData, sumSquared, etc.
```

## Per-Base Values

```python
# 0-based, half-open interval [start, end) — same convention as BED
values = bw.values("chr1", 1000, 2000)     # list of floats, one per base; nan where no data
```

For large regions, prefer `bw.stats(..., exact=False)` (bin-level, uses precomputed zoom levels — fast) over pulling every base with `bw.values` and reducing in Python.

## Bin-Level Statistics

```python
# Mean signal in 100 equal-width bins across the region — fast, uses zoom levels
means = bw.stats("chr1", 0, 10000, type="mean", nBins=100)

# Single summary value for the whole region
mean_val = bw.stats("chr1", 0, 10000, type="mean")[0]
max_val = bw.stats("chr1", 0, 10000, type="max")[0]
coverage = bw.stats("chr1", 0, 10000, type="coverage")[0]   # fraction of bases with data

# Exact (base-pair-precise) instead of zoom-level-approximated — slower, use for small/critical regions
exact_mean = bw.stats("chr1", 0, 10000, type="mean", exact=True)[0]
```

`type` accepts `"mean"`, `"max"`, `"min"`, `"std"`, `"coverage"`, or `"sum"`. Bins with no data return `None` in the result list — handle that explicitly (see pitfalls).

## Iterating Intervals

```python
for start, end, value in bw.intervals("chr1"):     # every stored interval on chr1
    ...

for start, end, value in bw.intervals("chr1", 1000, 5000):   # restricted to a region
    ...
```

## BigBed Entries

```python
bb = pyBigWig.open("peaks.bb")
for start, end, rest in bb.entries("chr1", 0, 1000000):
    # `rest` is a tab-separated string of any extra BED columns (name, score, strand, ...)
    name, score, strand = rest.split("\t")[:3]
```

## Region-Based Signal Extraction (BED → DataFrame)

The most common real-world pattern — mean signal per region from a BED file:

```python
import pandas as pd
import pyBigWig

bw = pyBigWig.open("H3K27ac.bw")
regions = pd.read_csv("peaks.bed", sep="\t", header=None,
                       names=["chrom", "start", "end", "name"])

def mean_signal(row):
    val = bw.stats(row.chrom, row.start, row.end, type="mean")[0]
    return val if val is not None else 0.0

regions["mean_signal"] = regions.apply(mean_signal, axis=1)
bw.close()
```

For thousands of regions, batching by chromosome and using `bw.stats(..., nBins=1)` per region is still the bottleneck-free approach — pyBigWig's `stats` call is C-level and fast per call, but calling it hundreds of thousands of times in a tight Python loop still dominates wall-clock time; vectorize with multiprocessing across chromosomes if this becomes a bottleneck.

## Writing a BigWig File

```python
import pyBigWig

bw = pyBigWig.open("custom_signal.bw", "w")
bw.addHeader([("chr1", 248956422), ("chr2", 242193529)])   # must be called before addEntries
bw.addEntries(
    ["chr1", "chr1", "chr1"],
    [0, 100, 200],
    ends=[100, 200, 300],
    values=[1.5, 2.7, 0.3],
)
bw.close()   # required — data isn't flushed to disk until close()
```

`addEntries` also accepts a single-chromosome + span/step form (`bw.addEntries("chr1", 0, values=[...], span=10, step=10)`) for fixed-interval tracks. `addEntries` accepts numpy arrays for `chroms`/`starts`/`ends`/`values` directly — no flag is needed — provided pyBigWig was compiled with numpy available; check with `pyBigWig.numpy == 1`. (There is no `numpy` keyword on `open()` or `addEntries()`. The `numpy=True` keyword is real but belongs to the read side, on `values()` and `stats()`, where it returns a numpy array instead of a Python list.)

## Common Pitfalls

- **`bw.stats()` returns `None` for empty bins, not `0` or `nan`.** Code that does arithmetic on the raw result list will crash or silently propagate `None`; explicitly substitute `0.0` (no signal) or `float("nan")` (missing data) depending on what's semantically correct for your analysis.
- **`exact=True` on huge regions is slow.** It re-reads every base rather than using precomputed zoom-level summaries; only use it when you need base-pair precision (e.g., very small windows or footprinting), not for genome-wide scans.
- **Files opened `"w"` cannot be queried.** A write-mode handle can only be written to (`addHeader`/`addEntries`) — open a second, separate read-mode handle if you need to verify what you just wrote.
- **Forgetting `bw.close()` after writing.** BigWig writes are buffered; skipping `close()` (or crashing before it) leaves a truncated/invalid file.
- **Coordinate convention mismatch.** pyBigWig follows BED's 0-based, half-open convention (`values("chr1", 1000, 2000)` covers positions 1000-1999). If you're cross-referencing 1-based coordinates from a VCF or GFF, convert (`start - 1`) before querying.
- **Remote file latency.** Opening a BigWig over HTTPS/FTP works but each `stats`/`values` call may trigger a range request; for repeated heavy querying, download the file locally first.
- **Missing libcurl/zlib when building from source.** If a prebuilt wheel isn't available for your platform, `pip install pyBigWig` fails with a linker error unless `curl-config` and zlib headers are installed — switch to the conda-forge/bioconda build instead of chasing system headers.

## Resources

- Docs / README: https://github.com/deeptools/pyBigWig#readme
- Source: https://github.com/deeptools/pyBigWig
- Underlying C library: https://github.com/dpryan79/libBigWig
