---
name: pygenometracks-coverage-plots
description: "pyGenomeTracks — publication-quality genome-browser-style coverage plots from bigWig / BED / GTF tracks driven by an INI config. Use when you need a static PNG/SVG of read pileup, peak calls, or gene annotations at a specific locus for a figure. For interactive browsing use IGV or UCSC."
license: MIT
---

# pyGenomeTracks Coverage Plots

## Overview

`pyGenomeTracks` produces static, figure-ready genome-browser snapshots
from a single INI config file. It is the idiomatic Python tool for the
"show me a screenshot of this locus" figure panel that almost every
chromatin paper includes. Inputs are standard bigWig / BED / GTF /
BedGraph files; output is PNG, SVG, or PDF at a chosen DPI.

**When to reach for this skill:**
- You need a figure-quality, scriptable, reproducible genome-browser
  screenshot at a specific locus.
- You want to overlay multiple tracks (ATAC bigWig, peak calls, gene
  models) in a single panel.

**Pre-reqs:**
- `pip install pygenometracks`
- bigWig files for each track (convert BAM → bigWig with `deeptools
  bamCoverage` or `bedGraphToBigWig`).

---

## Part 1 — Minimal tracks.ini

```ini
[bigwig]
file = coverage.bw
title = ATAC Coverage
height = 3
color = blue

[genes]
file = genes.gtf
title = Genes
fontsize = 10
height = 5
```

Write the INI file from Python so the entire pipeline is scriptable:

```python
tracks_config = """
[bigwig]
file = coverage.bw
title = ATAC Coverage
height = 3
color = blue

[genes]
file = genes.gtf
title = Genes
fontsize = 10
height = 5
"""

with open("tracks.ini", "w") as f:
    f.write(tracks_config)
```

---

## Part 2 — Rendering

```bash
pyGenomeTracks \
    --tracks tracks.ini \
    --region chr11:60000000-60500000 \
    -o coverage.png \
    --dpi 300
```

For multiple loci (e.g. one panel per cell-type-specific gene), wrap in
a Python loop:

```python
import subprocess
loci = {
    "MS4A1":  "chr11:60223282-60238459",
    "CD8A":   "chr2:86784710-86808558",
    "GAPDH":  "chr12:6534517-6538371",
}
for gene, region in loci.items():
    subprocess.run([
        "pyGenomeTracks",
        "--tracks", "tracks.ini",
        "--region", region,
        "-o", f"{gene}.png",
        "--dpi", "300",
    ], check=True)
```

---

## Part 3 — Multi-condition track stacks

A common multiome figure shows ATAC coverage in N cell types stacked
vertically:

```ini
[atac_Bcell]
file = atac_Bcell.bw
title = B cell
color = #1f77b4
height = 2
min_value = 0
max_value = 25

[atac_Tcell]
file = atac_Tcell.bw
title = T cell
color = #ff7f0e
height = 2
min_value = 0
max_value = 25

[atac_NK]
file = atac_NK.bw
title = NK cell
color = #2ca02c
height = 2
min_value = 0
max_value = 25

[spacer]

[peaks]
file = peaks.bed
title = Peaks
display = collapsed
color = grey
height = 1

[genes]
file = genes.gtf
title = Genes
fontsize = 8
height = 4
```

Always pin `min_value` / `max_value` so the visual scale is comparable
across conditions — otherwise pyGenomeTracks auto-scales each track
independently and makes coverage look uniform when it is not.

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| Tracks auto-scale independently → misleading | Set `min_value` / `max_value` explicitly on every bigwig track. |
| Output is rasterised at low DPI | Pass `--dpi 300` (or output SVG with `-o out.svg`). |
| Gene annotation track is empty | Ensure the GTF has a `gene` feature line, not just `exon`. |
| Region string format error | Use `chrN:start-end` exactly — no spaces, no commas, hyphen separator. |
| BigWig conversion: BAM uses different chrom naming (`1` vs `chr1`) | Reheader the BAM with `samtools view -h | sed` before `bamCoverage`. |

---

## Generating bigWigs from BAM (companion step)

```bash
# Index BAM
samtools index sample.bam

# Generate bigWig (CPM-normalised)
bamCoverage \
    --bam sample.bam \
    --outFileName sample.bw \
    --binSize 10 \
    --normalizeUsing CPM \
    --extendReads
```

---

## API quick reference

```bash
pyGenomeTracks --tracks tracks.ini --region chrN:start-end -o out.png
```

INI track types: `bigwig`, `bedgraph`, `bed`, `gtf`, `links`, `hic`,
`epilogos`, `spacer`, `x-axis`.

---

## Resources

- pyGenomeTracks docs: https://pygenometracks.readthedocs.io/
- deepTools bamCoverage: https://deeptools.readthedocs.io/
- INI track-type gallery: https://pygenometracks.readthedocs.io/en/latest/content/all_tracks.html

---

## When not to use

- Do not use for interactive genome browsing — use IGV or UCSC.
- Do not use for per-cell heatmaps of accessibility — use sc.pl.heatmap.

---

## See also

- `muon-multimodal-analysis`
- `snapatac2-atac-preprocessing`
- `signac-chromatin-analysis`
