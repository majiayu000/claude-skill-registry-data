---
name: cellranger-arc-multiome
description: "Cell Ranger ARC processes 10x Single Cell Multiome ATAC+GEX via mkfastq, count, aggr, and reanalyze, producing paired ATAC fragments and gene expression from the same cells. Use for primary processing of multiome FASTQs, including single-indexed ATAC demultiplexing and the libraries CSV. For scRNA-only use plain Cell Ranger (external), not ARC."
license: MIT
---

# Cell Ranger ARC - 10x Multiome ATAC+GEX Pipeline

## Purpose
Processes Chromium Epi Multiome data containing **paired** ATAC and Gene Expression from the same cells. **CRITICAL**: Cannot analyze ATAC or GEX alone - both modalities required for all pipelines.

## Core Workflow
1. `mkfastq`: Demultiplex BCL → FASTQ (separate runs for ATAC/GEX flow cells)
2. `count`: Align, quantify, call cells, perform joint analysis (requires both modalities)
3. `aggr`: Merge multiple samples with normalization
4. `reanalyze`: Re-run secondary analysis with different parameters

## Critical Index Structure Differences

**ATAC Libraries (Single-Indexed)**:
- Each sample index = 4 separate oligo sequences (e.g., SI-NA-A1 → 4 oligos)
- bcl2fastq creates 4 separate sample folders per biological sample
- **Must merge all 4** in libraries CSV or get 1/4th expected reads
- Read structure: I1 (opt) / R1 / R2 (i5 index) / R3 **OR** I1 / R1 / I2 (index) / R2

**GEX Libraries (Dual-Indexed)**:
- Single sample index = unique i7 + i5 pair (e.g., SI-TT-A1)
- Standard dual-index structure: I1 (i7) / I2 (i5) / R1 / R2

## Libraries CSV Format

```csv
fastqs,sample,library_type
/path/to/gex/fastqs,sample_name,Gene Expression
/path/to/atac/fastqs,sample_name,Chromatin Accessibility
```

**Critical Rules**:
- `library_type` is case-sensitive: exactly `Gene Expression` or `Chromatin Accessibility`
- Both modalities required (cannot omit either row)
- For split ATAC oligos, add 4 rows with same library_type, different sample names (SI-NA-A1_1, _2, _3, _4)

## FASTQ Naming Convention

**Must follow bcl2fastq standard**: `[Sample]_S[N]_L00[Lane]_[Read]_001.fastq.gz`

GEX reads: R1 (cDNA), R2 (UMI+barcode), I1/I2 (optional indices)
ATAC reads: R1 (genomic), R2 or I2 (barcode), R3 or R2 (genomic), I1 (optional)

**Files not matching this pattern will fail** - rename before running count.

## BCL Convert Critical Parameters

**For ATAC libraries**, must specify:
```bash
OverrideCycles,Y50;I8;U24;Y49  # Outputs UMI to FASTQ
CreateFastqForIndexReads,1     # Required for ATAC
TrimUMI,0                       # Critical: preserve UMI
```

**Never include adapter trimming settings** (`Adapter`, `AdapterRead1`, `AdapterRead2` in `[Settings]`) - damages barcodes/UMIs causing pipeline failure.

## Common Pitfalls

**ATAC 4-oligo problem**: If mkfastq/bcl2fastq created folders like `SI-NA-A1_1`, `SI-NA-A1_2`, `SI-NA-A1_3`, `SI-NA-A1_4`, you MUST list all 4 in libraries CSV:
```csv
fastqs,sample,library_type
/path,SI-NA-A1_1,Chromatin Accessibility
/path,SI-NA-A1_2,Chromatin Accessibility
/path,SI-NA-A1_3,Chromatin Accessibility
/path,SI-NA-A1_4,Chromatin Accessibility
```
Omitting any = 25% data loss per missing oligo.

**Cannot process modalities separately**: Running count with only GEX or only ATAC will fail. Use Cell Ranger (GEX) or Cell Ranger ATAC (ATAC) for single-modality analysis.

**Cell calling overrides**: `--min-atac-count` and `--min-gex-count` must be specified **together** (both or neither). Review default web_summary first before overriding.

## Key Output Files

- `filtered_feature_bc_matrix.h5`: Concatenated gene+peak counts (cells only)
- `atac_fragments.tsv.gz`: Per-fragment info (critical for downstream peak analysis)
- `analysis/feature_linkage/`: Peak-gene regulatory linkages
- `cloupe.cloupe`: Loupe Browser file (joint ATAC+GEX visualization)
- Separate BAMs: `atac_possorted_bam.bam`, `gex_possorted_bam.bam`

## Integration Notes

**For downstream analysis**:
- Use `filtered_feature_bc_matrix.h5` for Seurat/Signac (contains both modalities)
- ArchR/SnapATAC2 can import `atac_fragments.tsv.gz` directly
- Peak-gene linkages in `feature_linkage.bedpe` inform regulatory network inference
- Feature matrix rows = genes + peaks concatenated (check `features.tsv.gz` for boundaries)

---

**Installation**: Save to `/mnt/skills/user/cellranger_arc.md`  
**Test**: `cellranger-arc count --help | grep libraries`  
**Token count**: ~580 tokens

---

## When not to use

- Do not use for scRNA-only 3'/5' data. Use Cell Ranger (non-ARC) instead.
- Do not use for scATAC-only libraries. Use Cell Ranger ATAC.
- Cannot analyze ATAC or GEX modality alone; both modalities are required for all ARC pipelines.

---

## See also

- `scvi-multivi`
- `scglue-unpaired-multiomics-integration`
- `iterative-peak-merging`
- `pycistopic-atac-topic-modeling`

Upstream docs: https://www.10xgenomics.com/support/software/cell-ranger-arc
