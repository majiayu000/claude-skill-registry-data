---
name: starsolo-spliced-unspliced
description: "Quantifies spliced, unspliced, and ambiguous count matrices from 10x FASTQs using STARsolo's Velocyto mode — a faster drop-in replacement for velocyto.py plus CellRanger. Use when preparing upstream inputs for RNA velocity from raw reads. For downstream velocity modeling on the resulting layers use rna-velocity-trajectory."
license: MIT
---

# STARsolo: Spliced/Unspliced Count Quantification

**Purpose:** Generate spliced, unspliced, and ambiguous count matrices from FASTQ files using STARsolo's Velocyto mode — a drop-in replacement for velocyto.py that is ~10x faster than CellRanger.

---

## When to Use

- You need spliced/unspliced/ambiguous layers for RNA velocity (scVelo, CellRank, Chronocell)
- Starting from FASTQ files (not BAMs) — STARsolo maps + quantifies in one pass
- Replacing a velocyto.py + CellRanger pipeline with a single STAR run
- Need CellRanger-compatible output format with velocity layers added

**Not for:** If you only have BAMs (no FASTQs), use velocyto.py directly or STARsolo's BAM-input mode.

---

## Key Concept: soloFeatures Velocyto

The critical parameter is:

```bash
--soloFeatures Gene Velocyto
```

This calculates **Spliced**, **Unspliced**, and **Ambiguous** counts per cell per gene, similar to velocyto.py (La Manno et al.). `Gene` is required alongside `Velocyto`.

For maximum information, request all features in one run:

```bash
--soloFeatures Gene GeneFull SJ Velocyto
```

---

## Quick Start: 10X Chromium V3

### 1. Build Genome Index (one-time)

```bash
STAR --runMode genomeGenerate \
  --runThreadN 32 \
  --genomeDir /path/to/star_index \
  --genomeFastaFiles /path/to/genome.fa \
  --sjdbGTFfile /path/to/genes.gtf
```

Use CellRanger-filtered GTF for best concordance with CellRanger counts. Add `--genomeSAsparseD 3` to reduce RAM to ~16GB (at 30-50% speed cost).

### 2. Run STARsolo with Velocyto

```bash
STAR \
  --genomeDir /path/to/star_index \
  --readFilesIn Read2.fastq.gz Read1.fastq.gz \
  --readFilesCommand zcat \
  --runThreadN 32 \
  --soloType CB_UMI_Simple \
  --soloCBwhitelist /path/to/3M-february-2018.txt \
  --soloCBstart 1 --soloCBlen 16 \
  --soloUMIstart 17 --soloUMIlen 12 \
  --soloFeatures Gene Velocyto \
  --soloCBmatchWLtype 1MM_multi_Nbase_pseudocounts \
  --soloUMIfiltering MultiGeneUMI_CR \
  --soloUMIdedup 1MM_CR \
  --clipAdapterType CellRanger4 \
  --outFilterScoreMin 30 \
  --soloCellFilter EmptyDrops_CR \
  --outSAMtype BAM SortedByCoordinate \
  --outSAMattributes NH HI nM AS CR UR CY UY CB UB \
  --outFileNamePrefix /path/to/output/sample1_
```

**Critical read order:** `--readFilesIn cDNA_Read2 Barcode_Read1` (Read2 first for 10X).

For multiple lanes:
```bash
--readFilesIn R2_L1.fq.gz,R2_L2.fq.gz  R1_L1.fq.gz,R1_L2.fq.gz
```

### 3. Output Structure

```
sample1_Solo.out/
  Gene/
    raw/          # Unfiltered: barcodes.tsv, features.tsv, matrix.mtx
    filtered/     # Cell-called: barcodes.tsv, features.tsv, matrix.mtx
  Velocyto/
    raw/
      spliced.mtx       # Exonic reads
      unspliced.mtx     # Intronic reads
      ambiguous.mtx     # Reads overlapping exon-intron boundaries
      barcodes.tsv
      features.tsv
    filtered/
      spliced.mtx
      unspliced.mtx
      ambiguous.mtx
      barcodes.tsv
      features.tsv
```

---

## Load into Python (scVelo / Scanpy)

```python
import scanpy as sc
import scvelo as scv
from scipy.io import mmread
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix

def load_starsolo_velocity(solo_out_dir, use_filtered=True):
    """Load STARsolo Velocyto output into AnnData with spliced/unspliced layers."""
    subdir = "filtered" if use_filtered else "raw"

    # Load standard gene counts
    gene_dir = f"{solo_out_dir}/Gene/{subdir}"
    adata = sc.read_mtx(f"{gene_dir}/matrix.mtx").T
    adata.obs_names = pd.read_csv(f"{gene_dir}/barcodes.tsv", header=None)[0].values
    features = pd.read_csv(f"{gene_dir}/features.tsv", sep="\t", header=None)
    adata.var_names = features[0].values
    if features.shape[1] > 1:
        adata.var["gene_name"] = features[1].values

    # Load velocity layers
    velo_dir = f"{solo_out_dir}/Velocyto/{subdir}"
    barcodes_velo = pd.read_csv(f"{velo_dir}/barcodes.tsv", header=None)[0].values

    # Ensure barcode order matches
    assert np.array_equal(adata.obs_names, barcodes_velo), \
        "Barcode mismatch between Gene and Velocyto outputs"

    adata.layers["spliced"] = csr_matrix(mmread(f"{velo_dir}/spliced.mtx").T)
    adata.layers["unspliced"] = csr_matrix(mmread(f"{velo_dir}/unspliced.mtx").T)
    adata.layers["ambiguous"] = csr_matrix(mmread(f"{velo_dir}/ambiguous.mtx").T)

    return adata


# Usage
adata = load_starsolo_velocity("/path/to/sample1_Solo.out")

# Verify layers
print(f"Spliced:   {adata.layers['spliced'].sum():.0f} counts")
print(f"Unspliced: {adata.layers['unspliced'].sum():.0f} counts")
print(f"Ambiguous: {adata.layers['ambiguous'].sum():.0f} counts")

# Proceed with scVelo
scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
scv.tl.velocity(adata, mode="dynamical")
scv.tl.velocity_graph(adata)
```

---

## Assay-Specific Presets

### 10X Chromium V3 (default)
```bash
--soloCBstart 1 --soloCBlen 16 --soloUMIstart 17 --soloUMIlen 12
--soloCBwhitelist 3M-february-2018.txt
```

### 10X Chromium V2
```bash
--soloCBstart 1 --soloCBlen 16 --soloUMIstart 17 --soloUMIlen 10
--soloCBwhitelist 737K-august-2016.txt
```

### 10X 5' (R2 only)
```bash
--soloCBstart 1 --soloCBlen 16 --soloUMIstart 17 --soloUMIlen 10
--soloStrand Reverse
--soloCBwhitelist 737K-august-2016.txt
```

### 10X 5' Paired-End (R1 longer than 39nt)
```bash
--soloBarcodeMate 1 --clip5pNbases 39 0
--soloCBstart 1 --soloCBlen 16 --soloUMIstart 17 --soloUMIlen 10
```

### 10X Multiome (Gene Expression)
Same as V3 but use the ARC Multiome whitelist.

### Drop-seq / SeqWell
```bash
--soloCBstart 1 --soloCBlen 12 --soloUMIstart 13 --soloUMIlen 8
```

### SHARE-seq
```bash
--soloCBstart 1 --soloCBlen 24 --soloUMIstart 25 --soloUMIlen 10
```

---

## Matching CellRanger Versions

### CellRanger >= 4.x (recommended)
```bash
--clipAdapterType CellRanger4 \
--outFilterScoreMin 30 \
--soloCBmatchWLtype 1MM_multi_Nbase_pseudocounts \
--soloUMIfiltering MultiGeneUMI_CR \
--soloUMIdedup 1MM_CR
```

### CellRanger 3.x
```bash
--soloCBmatchWLtype 1MM_multi_Nbase_pseudocounts \
--soloUMIfiltering MultiGeneUMI_CR \
--soloUMIdedup 1MM_CR
```

### CellRanger 2.x (STAR defaults)
No extra flags needed.

---

## Cell Filtering Options

### EmptyDrops (CellRanger 3+ style, recommended)
```bash
--soloCellFilter EmptyDrops_CR
```
Parameters: `nExpectedCells maxPercentile maxMinRatio indMin indMax umiMin umiMinFracMedian candMaxN FDR simN`
Defaults: `3000 0.99 10 45000 90000 500 0.01 20000 0.01 10000`

### Knee filtering (CellRanger 2 style)
```bash
--soloCellFilter CellRanger2.2 3000 0.99 10
```

### No filtering (get raw, filter yourself)
```bash
--soloCellFilter None
```

### Re-filter existing raw matrix (no re-mapping)
```bash
STAR --runMode soloCellFiltering \
  /path/to/Solo.out/Gene/raw/ \
  /path/to/output_prefix \
  --soloCellFilter EmptyDrops_CR
```

---

## Multi-Gene Read Handling

For genes with overlapping loci or paralog families:

```bash
--soloMultiMappers EM           # Maximum Likelihood (best accuracy)
--soloMultiMappers Uniform      # Simple fractional assignment
--soloMultiMappers Rescue       # First EM iteration
--soloMultiMappers PropUnique   # Proportional to unique mappers
```

Output: `UniqueAndMult-EM.mtx` etc. alongside standard `matrix.mtx` (unique only).

---

## BAM Input Mode

If starting from existing BAM files (e.g., CellRanger output):

```bash
STAR \
  --genomeDir /path/to/star_index \
  --readFilesIn input.bam \
  --readFilesType SAM SE \
  --readFilesCommand samtools view -F 0x100 \
  --soloType CB_UMI_Simple \
  --soloInputSAMattrBarcodeSeq CR UR \
  --soloInputSAMattrBarcodeQual CY UY \
  --soloCBwhitelist /path/to/whitelist.txt \
  --soloFeatures Gene Velocyto \
  --outSAMtype BAM SortedByCoordinate \
  --outSAMattributes NH HI nM AS CR UR CY UY CB UB
```

Use `--readFilesSAMattrKeep None` to avoid duplicated SAM attributes.

---

## Batch Processing Script

```bash
#!/usr/bin/env bash
# run_starsolo_batch.sh - Process multiple 10X V3 samples
set -euo pipefail

GENOME_DIR="/path/to/star_index"
WHITELIST="/path/to/3M-february-2018.txt"
OUTPUT_BASE="/path/to/results"
THREADS=32

declare -A SAMPLES=(
    ["sample1"]="/path/to/sample1_fastqs"
    ["sample2"]="/path/to/sample2_fastqs"
)

for sample in "${!SAMPLES[@]}"; do
    fastq_dir="${SAMPLES[$sample]}"
    out_dir="${OUTPUT_BASE}/${sample}"
    mkdir -p "${out_dir}"

    # Collect FASTQ files
    R1=$(ls "${fastq_dir}"/*_R1_001.fastq.gz | sort | paste -sd,)
    R2=$(ls "${fastq_dir}"/*_R2_001.fastq.gz | sort | paste -sd,)

    echo "Processing ${sample}..."
    STAR \
      --genomeDir "${GENOME_DIR}" \
      --readFilesIn "${R2}" "${R1}" \
      --readFilesCommand zcat \
      --runThreadN "${THREADS}" \
      --soloType CB_UMI_Simple \
      --soloCBwhitelist "${WHITELIST}" \
      --soloCBstart 1 --soloCBlen 16 \
      --soloUMIstart 17 --soloUMIlen 12 \
      --soloFeatures Gene GeneFull Velocyto \
      --soloCBmatchWLtype 1MM_multi_Nbase_pseudocounts \
      --soloUMIfiltering MultiGeneUMI_CR \
      --soloUMIdedup 1MM_CR \
      --clipAdapterType CellRanger4 \
      --outFilterScoreMin 30 \
      --soloCellFilter EmptyDrops_CR \
      --outSAMtype BAM SortedByCoordinate \
      --outSAMattributes NH HI nM AS CR UR CY UY CB UB \
      --outFileNamePrefix "${out_dir}/"

    echo "Done: ${sample} -> ${out_dir}/Solo.out/"
done
```

---

## Resource Requirements

| Component | Recommendation |
|-----------|---------------|
| RAM | 32-40GB (genome loading); add `--genomeSAsparseD 3` at index build to reduce to ~16GB |
| CPUs | 16-32 threads (`--runThreadN`) |
| Disk | ~500GB per sample (BAM + intermediate); output matrices are small |
| STAR version | >= 2.7.9a (Velocyto improvements); recommended 2.7.11b |
| Time | ~20-40 min per sample (vs. hours for CellRanger) |

---

## Whitelist Files

| Chemistry | Whitelist | UMI length |
|-----------|-----------|------------|
| 10X V3 / V3.1 | `3M-february-2018.txt` | 12 |
| 10X V2 | `737K-august-2016.txt` | 10 |
| 10X 5' | `737K-august-2016.txt` | 10 |
| 10X Multiome | ARC whitelist | 12 |

Download from: `https://github.com/10XGenomics/cellranger/tree/master/lib/python/cellranger/barcodes/`

---

## Prebuilt References (Cloud/Terra)

| Keyword | Description |
|---------|-------------|
| `GRCh38-2020-A` | Human (GENCODE v32/Ensembl 98) |
| `mm10-2020-A` | Mouse (GENCODE vM23/Ensembl 98) |
| `GRCh38-and-mm10-2020-A` | Human + Mouse (barnyard) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty Velocyto output | Ensure `Gene` is included: `--soloFeatures Gene Velocyto` (Velocyto requires Gene) |
| Barcode mismatch | Check read order: R2 (cDNA) first, R1 (barcode) second for 10X |
| Low unspliced fraction | Normal for mature mRNA-enriched protocols; check with `adata.layers['unspliced'].sum() / adata.layers['spliced'].sum()` — expect 5-20% for 3' protocols |
| RAM exceeded | Use sparse suffix array: `--genomeSAsparseD 3` at genome generation step |
| Slow BAM sorting | Increase `--limitBAMsortRAM` or use `--outSAMtype BAM Unsorted` if BAM not needed |
| Version mismatch counts | Match GTF exactly between STAR index and CellRanger reference |
| `soloBarcodeReadLength` error | Set `--soloBarcodeReadLength 0` to skip length check |

---

## When not to use

- Do not use if you only have BAM files — use velocyto.py or STARsolo BAM-input mode instead.
- Do not use for standard gene-only counting where velocity layers are unneeded — plain CellRanger or STARsolo Gene is lighter.

---

## See also

- `rna-velocity-trajectory`

Upstream docs: https://github.com/alexdobin/STAR/blob/master/docs/STARsolo.md
