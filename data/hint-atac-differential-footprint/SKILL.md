---
name: hint-atac-differential-footprint
description: "HINT-ATAC (rgt-hint) HMM-based TF footprint detection and multi-condition differential footprinting. Use when comparing TF activity across 3+ conditions at once and you want overview heatmaps from one command. For pairwise contrasts with p-values use tobias-footprint-bindetect; for figures use signac-footprint-visualization."
license: MIT
---

# HINT-ATAC Multi-Condition Differential Footprinting

## Purpose

HINT-ATAC (part of the RGT suite) uses an HMM to learn footprint states from ATAC-seq Tn5 cuts and supports multi-condition differential footprinting in a single command — its main advantage over TOBIAS BINDetect, which is pairwise only.

**Use when:**
- Comparing TF binding across 3+ cell types or conditions simultaneously
- Producing overview heatmaps of TF activity dynamics
- Bias-corrected bigwig tracks for genome browsers (`rgt-hint tracks`)

**Upstream:** Peak calling (MACS2/MACS3), pseudobulk BAM generation
**Downstream:** Multi-condition activity heatmaps, scatter plots of TF dynamics

## Installation

```bash
python3.9 -m venv /opt/venvs/rgt
source /opt/venvs/rgt/bin/activate
pip install rgt

# Download genome data (REQUIRED for bias correction)
python -c "from rgt.helper import download_genome; download_genome('mm10')"

rgt-hint footprinting --help
```

## Workflow

```
BAM + Peaks → footprinting → motifanalysis matching → differential → heatmaps
```

### Step 1: Footprint Calling

```bash
# Per celltype pseudobulk BAM
rgt-hint footprinting \
  --atac-seq \
  --paired-end \
  --organism=mm10 \
  --output-location=./footprints/ \
  --output-prefix=${CELLTYPE} \
  ${CELLTYPE}.bam ${CELLTYPE}_peaks.narrowPeak
```

**Critical:** `--organism=mm10` requires RGT genome data downloaded first (see Installation).

### Step 2: Motif Matching

```bash
rgt-motifanalysis matching \
  --organism=mm10 \
  --output-location=./motif_matching/ \
  --input-files ./footprints/${CELLTYPE}.bed
```

### Step 3: Differential Footprinting (Multi-Condition)

```bash
# Compare multiple cell types in one run
rgt-hint differential \
  --organism=mm10 \
  --bc \
  --nc 64 \
  --mpbs-files=./motif_matching/cDC1_mpbs.bed,./motif_matching/cDC2_mpbs.bed,./motif_matching/Mac_mpbs.bed \
  --reads-files=cDC1.bam,cDC2.bam,Mac.bam \
  --conditions=cDC1,cDC2,Mac \
  --output-location=./diff_footprints/ \
  --output-prefix=celltype_comparison
```

**Outputs:**
- `*_statistics.txt`: Tag count and protection score per condition per TF
- `Lineplots/`: ATAC-seq profiles per TF per condition
- Scatter plot of TF activity dynamics across conditions

### Step 4: Bias-Corrected Tracks (Genome Browser)

```bash
rgt-hint tracks \
  --bc \
  --bigWig \
  --organism=mm10 \
  ${CELLTYPE}.bam ${CELLTYPE}_peaks.narrowPeak \
  --output-prefix=${CELLTYPE}_BC
```

## Output Interpretation

- **Protection score**: Higher = stronger footprint (more TF occupancy)
- **Tag count score**: Reads around motif sites (library-size dependent — normalize before comparing libraries)
- **Statistics file**: Per-TF activity scores across all conditions; suitable for heatmap input
- **Activity scatter**: TFs with high condition-specific activity appear as outliers

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `--organism=mm10` errors | Genome data not downloaded | `python -c "from rgt.helper import download_genome; download_genome('mm10')"` |
| Library-size confounds activity | Tag count not normalized | Compare protection scores, or downsample BAMs to matched depth |
| Slow `differential` step | Single-threaded by default | Set `--nc 64` to parallelize |
| Motif name mismatch with TOBIAS/ChromVAR | Different PWM sets | Use a shared motif database across tools |

## Performance Tips

- `--nc` controls parallelism in `rgt-hint differential` — use it
- For >5 conditions, expect heavy memory use; split into thematic groups if needed
- Pre-compute motif matching once per peak set, reuse across condition combinations

## Resources

- **Publication**: Li et al., Genome Biology 2019 ([DOI: 10.1186/s13059-019-1642-2](https://doi.org/10.1186/s13059-019-1642-2))
- **RGT Suite docs**: https://reg-gen.readthedocs.io/
- **HINT-ATAC tutorial (DC specification)**: https://reg-gen.readthedocs.io/en/latest/hint/tutorial_DC.html

---

## When not to use

- Do not use for single-cell TF activity — HINT-ATAC requires pseudobulk BAMs.
- Do not use for quantitative pairwise contrasts — use tobias-footprint-bindetect.

---

## See also

- `tobias-footprint-bindetect`
- `signac-footprint-visualization`
- `chromvar-motif-accessibility`
