---
name: tobias-footprint-bindetect
description: "TOBIAS pseudobulk TF footprinting and pairwise differential binding (ATACorrect, ScoreBigwig, TFBScan, BINDetect, PlotAggregate). Use for quantitative TF occupancy on pseudobulked ATAC BAMs, condition-vs-condition contrasts with p-values, and bias-corrected footprint bigwigs. For multi-condition heatmaps use hint-atac-differential-footprint."
license: MIT
---

# TOBIAS Footprinting & BINDetect Differential Binding

## Purpose

TOBIAS detects physical TF occupancy from Tn5 protection patterns on pseudobulked ATAC BAMs, then computes differential binding between two conditions via BINDetect.

**Use when:**
- Quantitative differential TF binding (WT vs KO, treated vs control)
- Validating ChromVAR accessibility hits with occupancy evidence
- Producing bias-corrected footprint bigwigs
- Per-TF bound/unbound site BEDs with p-values

**Upstream:** Peak calling (MACS2/MACS3), pseudobulk BAM generation (ArchR/Signac)
**Downstream:** Aggregate plots (PlotAggregate), quadrant analysis with ChromVAR

## Installation

```bash
python3.10 -m venv /opt/venvs/tobias
source /opt/venvs/tobias/bin/activate
pip install tobias
TOBIAS --version
```

## Workflow

```
BAM + Peaks → ATACorrect → ScoreBigwig → TFBScan → BINDetect → PlotAggregate
```

### Step 1: Tn5 Bias Correction (ATACorrect)

```bash
TOBIAS ATACorrect \
  --bam ${CELLTYPE}_${CONDITION}.bam \
  --genome mm10.fa \
  --peaks consensus_peaks.bed \
  --blacklist mm10-blacklist.v2.bed \
  --outdir ./corrected/ \
  --cores 16

# Outputs:
# - *_corrected.bw    (bias-corrected signal — USE THIS)
# - *_uncorrected.bw  (raw signal)
# - *_expected.bw     (expected Tn5 bias)
# - *_bias.bw         (estimated bias)
```

**Critical parameters:**
- `--blacklist`: ENCODE mm10 blacklist v2 (ENCFF547MET). **Mandatory** — footprinting finds "perfect" footprints in artifact regions.
- `--genome`: Must match alignment build exactly. Chromosome naming (`chr1` vs `1`) is the #1 cause of failures.
- Do NOT pre-shift reads — TOBIAS applies the +4/-5 bp Tn5 shift internally.

### Step 2: Footprint Scoring (ScoreBigwig)

```bash
TOBIAS ScoreBigwig \
  --signal ./corrected/${CELLTYPE}_${CONDITION}_corrected.bw \
  --regions consensus_peaks.bed \
  --output ./scores/${CELLTYPE}_${CONDITION}_footprints.bw \
  --cores 16
```

### Step 3: Motif Scanning (TFBScan)

```bash
TOBIAS TFBScan \
  --motifs motifs.jaspar \
  --fasta mm10.fa \
  --regions consensus_peaks.bed \
  --outdir ./motif_hits/ \
  --cores 16
```

**Motif format:** JASPAR `.jaspar` or MEME `.meme`. JASPAR 2024 Core Vertebrates recommended for mouse.

### Step 4: Differential Binding (BINDetect)

```bash
TOBIAS BINDetect \
  --motifs motifs.jaspar \
  --signals ./scores/cDC1_WT_footprints.bw ./scores/cDC1_Batf3KO_footprints.bw \
  --genome mm10.fa \
  --peaks consensus_peaks.bed \
  --outdir ./differential/cDC1_WT_vs_KO/ \
  --cond_names WT Batf3_KO \
  --cores 16

# Outputs:
# - bindetect_results.txt   (per-TF differential binding scores + p-values)
# - bindetect_results.xlsx
# - <TF_name>/              (per-TF BED files of bound/unbound sites)
# - volcano plot PDF
```

**Key output columns in `bindetect_results.txt`:**
- `<cond1>_mean_score` / `<cond2>_mean_score`: Average footprint score per condition
- `<cond1>_<cond2>_change`: Differential binding score (positive = more bound in cond1)
- `<cond1>_<cond2>_pvalue`: Statistical significance

### Step 5: Aggregate Visualization (PlotAggregate)

```bash
TOBIAS PlotAggregate \
  --TFBS ./differential/cDC1_WT_vs_KO/IRF8/beds/IRF8_cDC1_WT_bound.bed \
  --signals ./corrected/cDC1_WT_corrected.bw ./corrected/cDC1_Batf3KO_corrected.bw \
  --output IRF8_aggregate.pdf \
  --share_y both \
  --plot_boundaries \
  --signal-on-x
```

## Batch Processing (All Contrasts)

```bash
#!/bin/bash
GENOME="mm10.fa"
PEAKS="consensus_peaks.bed"
BLACKLIST="mm10-blacklist.v2.bed"
MOTIFS="motifs.jaspar"
CORES=16

declare -A CONTRASTS=(
  ["I3"]="cDC1A_WT:cDC1B_WT"
  ["P1"]="cDC1_WT:cDC1_WTplusIL12"
  ["P4"]="cDC1_WT:cDC1_Batf3KO"
  ["I1"]="DC_WT:Mac_WT"
)

# Steps 1-2: Correct and score each BAM once
for bam in ./bams/*.bam; do
  prefix=$(basename "$bam" .bam)
  TOBIAS ATACorrect --bam "$bam" --genome "$GENOME" --peaks "$PEAKS" \
    --blacklist "$BLACKLIST" --outdir ./corrected/ --cores "$CORES"
  TOBIAS ScoreBigwig --signal "./corrected/${prefix}_corrected.bw" \
    --regions "$PEAKS" --output "./scores/${prefix}_footprints.bw" --cores "$CORES"
done

# Step 4: Differential binding per contrast
for contrast_id in "${!CONTRASTS[@]}"; do
  IFS=':' read -r cond1 cond2 <<< "${CONTRASTS[$contrast_id]}"
  TOBIAS BINDetect --motifs "$MOTIFS" \
    --signals "./scores/${cond1}_footprints.bw" "./scores/${cond2}_footprints.bw" \
    --genome "$GENOME" --peaks "$PEAKS" \
    --outdir "./differential/${contrast_id}_${cond1}_vs_${cond2}/" \
    --cond_names "$cond1" "$cond2" --cores "$CORES"
done
```

## Output Interpretation

- **Differential binding score > 0**: More binding in condition 1 (first `--signals`)
- **Differential binding score < 0**: More binding in condition 2
- **p-value**: From background distribution of all binding sites for that TF
- **Bound/unbound BEDs**: Per-site classification under `<TF_name>/beds/`

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Zero footprints found | Chromosome naming mismatch (`chr1` vs `1`) | Match BAM/FASTA/peaks naming |
| Spurious "perfect" footprints | Missing blacklist filter | Always pass `--blacklist` |
| All TFs differential | Pre-shifted BAMs + TOBIAS internal shift | Do NOT pre-shift reads |
| Memory errors in ATACorrect | Whole-genome correction at once | Use `--split` or per-chromosome |
| Low footprint signal | Insufficient pseudobulk depth | Pool more cells per condition; check `.info` read counts |

## Performance Tips

- ATACorrect is the slowest step (~30–60 min per BAM)
- Run Steps 1–2 once per BAM, reuse for all pairwise contrasts
- Use `--cores` aggressively on all stages

## Resources

- **Publication**: Bentsen et al., Nature Communications 2020 ([DOI: 10.1038/s41467-020-18035-1](https://doi.org/10.1038/s41467-020-18035-1))
- **GitHub**: https://github.com/loosolab/TOBIAS
- **Wiki**: https://github.com/loosolab/TOBIAS/wiki
- **sc-framework**: https://github.com/loosolab/SC-Framework

---

## When not to use

- Do not use for single-cell TF activity — TOBIAS requires pseudobulk BAMs.
- Do not use for >2-condition overview heatmaps — use hint-atac-differential-footprint.

---

## See also

- `hint-atac-differential-footprint`
- `signac-footprint-visualization`
- `chromvar-motif-accessibility`
