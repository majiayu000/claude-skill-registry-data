---
name: iterative-peak-merging
description: "Iterative overlap merging builds an optimal fixed-width 501bp merged peak set across ATAC-seq samples (Corces 2018), avoiding daisy-chaining and preserving cell-type-specific peaks. Use when consolidating per-cluster MACS2 peaks into a unified set, or when bedtools merge produces artificially wide peaks. For peak calling use MACS3 (external tool)."
license: MIT
---

# ATAC-seq Iterative Overlap Peak Merging Skill

## Overview
Iterative overlap peak merging creates optimal merged peak sets for ATAC-seq experiments by avoiding daisy-chaining and preserving cell type-specific peaks. Uses **fixed-width 501bp peaks** centered on summits. Originally described in Corces & Granja et al., Science 2018.

## Why This Method?

### Problem with Alternative Approaches

**bedtools merge** (Raw Overlap):
- ❌ Daisy-chaining: Non-overlapping peaks get merged via intermediate peaks
- ❌ Summit ambiguity: Must pick one summit or track multiple per peak
- ❌ Creates artificially wide peaks

**bedtools cluster** (Clustered Overlap):
- ❌ Under-calls peaks: Only keeps most significant per cluster
- ❌ Misses nearby peaks: Small peaks near large ones get excluded

**Iterative Overlap** (This Method):
- ✅ Ranks peaks by significance
- ✅ Iteratively keeps most significant, removes overlaps
- ✅ No daisy-chaining
- ✅ Fixed-width 501bp peaks
- ✅ Preserves cell type-specific peaks via tiered merging

## Local Script Location
```bash
<project-root>/01_scripts/R_scripts/createIterativeOverlapPeakSet.R
```

## Requirements

### R Packages (Must Be Installed)
```r
# Core packages
install.packages(c("optparse", "dplyr", "yaml", "readr"))

# Bioconductor packages
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c(
    "rtracklayer",
    "Biostrings", 
    "SummarizedExperiment",
    "GenomeInfoDb",
    "GenomicRanges",  # Must be version >1.44.0
    "edgeR",
    "BSgenome"
))

# Genome-specific BSgenome package
BiocManager::install("BSgenome.Hsapiens.UCSC.hg38")  # For human hg38
# OR
BiocManager::install("BSgenome.Mmusculus.UCSC.mm10")  # For mouse mm10
```

### Software Prerequisites
- MACS2 (for peak calling)
- Unix-based system (Linux/Mac)
- R with Bioconductor

### System Compatibility
⚠️ **IMPORTANT**: Script assumes human or mouse genomes. Other organisms may encounter issues due to chromosome naming conventions and BSgenome assumptions.

## Critical MACS2 Preprocessing

### Tn5 Offset Adjustment (MANDATORY)
Before running MACS2, BAM files **must** be adjusted for Tn5 offset as described in Buenrostro et al., Nature Protocols 2015.

### MACS2 Peak Calling Parameters (EXACT)
```bash
# Use EXACTLY these parameters for compatibility
macs2 callpeak \
  -t sample.bam \
  -f BAMPE \
  -n sample_prefix \
  --outdir /path/to/macs2/output/ \
  --shift -75 \
  --extsize 150 \
  --nomodel \
  --call-summits \
  --nolambda \
  --keep-dup all \
  -p 0.01
```

**Critical Flags**:
- `--call-summits`: Generates `*_summits.bed` files required by script
- `--shift -75`: Tn5 offset for ATAC-seq
- `--extsize 150`: ATAC-seq fragment size
- `-p 0.01`: P-value cutoff (adjust based on needs)

## Input Files

### 1. MACS2 Summit Files
- **Format**: `prefix_summits.bed` from MACS2 `--call-summits`
- **Location**: All summit files in **same directory**
- **Naming**: Consistent prefix + suffix pattern
  - Example: `CellTypeA_Rep1_summits.bed`
  - Prefix: `CellTypeA_Rep1`
  - Suffix: `_summits.bed`

### 2. Metadata File (TAB-DELIMITED)
**Format Requirements**:
- **Column 1**: Sample prefix (file name minus suffix)
- **Column 2**: Group identifier (MUST be named "Group" - case sensitive)
- **First line**: Header row
- **No duplicate** sample names
- **Tab-delimited** (not spaces)

**Example** (`metadata.txt`):
```tsv
Sample	Group
CellTypeA_Rep1	CellTypeA
CellTypeA_Rep2	CellTypeA
CellTypeA_Rep3	CellTypeA
CellTypeB_Rep1	CellTypeB
CellTypeB_Rep2	CellTypeB
CellTypeB_Rep3	CellTypeB
CellTypeC_Rep1	CellTypeC
CellTypeC_Rep2	CellTypeC
CellTypeC_Rep3	CellTypeC
```

**Grouping Logic**:
- Samples with same "Group" value are merged first
- Creates group-specific peak sets before final merge
- Use groups to represent: cell types, conditions, batches

### 3. Blacklist File
- **Download from**: [Boyle Lab Blacklists](https://github.com/Boyle-Lab/Blacklist)
- **Format**: Uncompressed BED file (gunzip if downloaded as .bed.gz)
- **Purpose**: Removes anomalous high-signal regions

**Available blacklists**:
- hg38: `hg38-blacklist.v2.bed`
- mm10: `mm10-blacklist.v2.bed`
- hg19: `hg19-blacklist.v2.bed`

## Running the Script

### Basic Command Structure
```bash
Rscript <project-root>/01_scripts/R_scripts/createIterativeOverlapPeakSet.R \
  --metadata /path/to/metadata.txt \
  --macs2dir /path/to/macs2/output/ \
  --outdir /path/to/output/ \
  --suffix _summits.bed \
  --blacklist /path/to/blacklist.bed \
  --genome hg38 \
  --spm 5 \
  --rule "(n+1)/2" \
  --extend 250
```

### Parameters Explained

#### Required Parameters (No Defaults)

**`--metadata`**: Path to metadata file
```bash
--metadata /data/atac_project/metadata.txt
```

**`--macs2dir`**: Directory containing summit files (must end with `/`)
```bash
--macs2dir /data/atac_project/macs2_peaks/
```

**`--outdir`**: Output directory (must end with `/`)
```bash
--outdir /data/atac_project/merged_peaks/
```

**`--suffix`**: Summit file suffix (typically `_summits.bed`)
```bash
--suffix _summits.bed
```

**`--blacklist`**: Path to uncompressed blacklist BED file
```bash
--blacklist /data/references/hg38-blacklist.v2.bed
```

**`--genome`**: BSgenome shorthand (e.g., `hg38`, `mm10`)
```bash
--genome hg38

# Find genome names:
# In R: BSgenome::available.genomes(splitNameParts=TRUE)
# Use "provider_version" column value
```

#### Optional Parameters (With Defaults)

**`--spm`**: Score-per-million cutoff (default: 5)
- **Higher** = More stringent (fewer, more significant peaks)
- **Lower** = More permissive (more peaks, some may be noise)
- **Recommended**: 2-5 for most experiments
```bash
--spm 5  # Standard stringency
--spm 2  # More permissive
--spm 10 # Very stringent
```

**`--rule`**: Reproducibility rule (default: 2)
- **Numeric**: Minimum number of samples with overlapping peak
- **Formula**: Dynamic based on sample count (use quotes)
- **Examples**:
  - `"2"`: At least 2 samples (fixed)
  - `"(n+1)/2"`: Majority of samples (50%+1)
  - `"n/2"`: At least half of samples
```bash
--rule "2"        # Fixed: 2+ samples required
--rule "(n+1)/2"  # Majority: >50% samples required
--rule "n"        # All samples (very stringent)
```

**Rule Interpretation by Group Size**:
| Rule | 2 reps | 3 reps | 4 reps | 5 reps |
|------|--------|--------|--------|--------|
| `"2"` | 2 | 2 | 2 | 2 |
| `"(n+1)/2"` | 2 | 2 | 3 | 3 |
| `"n/2"` | 1 | 2 | 2 | 3 |

**`--extend`**: Base pairs to extend from summit (default: 250)
- Creates peaks of width `(2 × extend) + 1`
- **Default 250** → 501bp peaks
- **Example 200** → 401bp peaks
```bash
--extend 250  # 501bp peaks (recommended)
--extend 200  # 401bp peaks
```

## Complete Working Example

### Setup
```bash
# Directory structure
/data/atac_project/
├── bams/                    # Tn5-adjusted BAM files
├── macs2_peaks/            # MACS2 output
│   ├── CellA_R1_summits.bed
│   ├── CellA_R2_summits.bed
│   ├── CellA_R3_summits.bed
│   ├── CellB_R1_summits.bed
│   ├── CellB_R2_summits.bed
│   └── CellB_R3_summits.bed
├── metadata.txt            # Sample metadata
└── merged_peaks/           # Output directory (create first)

/references/
└── hg38-blacklist.v2.bed
```

### Create Metadata
```bash
cat > /data/atac_project/metadata.txt << 'EOF'
Sample	Group
CellA_R1	CellTypeA
CellA_R2	CellTypeA
CellA_R3	CellTypeA
CellB_R1	CellTypeB
CellB_R2	CellTypeB
CellB_R3	CellTypeB
EOF
```

### Run Peak Merging
```bash
Rscript <project-root>/01_scripts/R_scripts/createIterativeOverlapPeakSet.R \
  --metadata /data/atac_project/metadata.txt \
  --macs2dir /data/atac_project/macs2_peaks/ \
  --outdir /data/atac_project/merged_peaks/ \
  --suffix _summits.bed \
  --blacklist /references/hg38-blacklist.v2.bed \
  --genome hg38 \
  --spm 5 \
  --rule "(n+1)/2" \
  --extend 250
```

## Output Files

### Generated Files
```
/data/atac_project/merged_peaks/
├── CellTypeA-reproduciblePeaks.bed    # Group A merged peaks
├── CellTypeB-reproduciblePeaks.bed    # Group B merged peaks
└── AllGroups-reproduciblePeaks.bed    # Final merged peak set
```

### Output Format
Standard BED format (0-indexed):
```
chr1    1000    1501    peak_1    score
chr1    5000    5501    peak_2    score
```
- **Width**: Always 501bp (with default extend=250)
- **Centered**: Peak summit is center position
- **Sorted**: By chromosome and position

## The Tiered Merging Process

### How It Works (Step-by-Step)

**Tier 1: Within-Group Merging**
1. Rank all peaks within group by significance
2. Keep most significant peak
3. Remove any peaks overlapping with it (≥1bp overlap)
4. Repeat for remaining peaks until none left
5. Filter by reproducibility rule (e.g., present in 2+ replicates)
6. Output: One merged peak set per group

**Tier 2: Across-Group Merging**
1. Combine all group peak sets
2. Re-normalize significance across groups (CRITICAL)
3. Perform iterative overlap removal again
4. Output: Single final merged peak set

### Why Tiered?
- **Preserves cell type-specific peaks**: Weak peaks in rare cell types not lost to strong peaks in abundant cell types
- **Fair comparison**: Re-normalization ensures groups with more reads don't dominate

## Automatic Filtering Steps

The script automatically performs these QC steps:

1. **Significance Filter**: Removes peaks below `spm` threshold
2. **Chromosome Clipping**: Removes peaks extending past chromosome ends
3. **chrY Removal**: Removes peaks mapping to Y chromosome
4. **N-base Filter**: Removes peaks spanning unknown bases (N) in reference
5. **Blacklist Filter**: Removes peaks overlapping blacklist regions

## Parameter Selection Guidelines

### Choosing SPM Threshold
| Data Type | Recommended SPM |
|-----------|----------------|
| High-quality, deep sequencing | 5-10 |
| Standard ATAC-seq | 3-5 |
| Low-depth or degraded | 2-3 |

**Diagnostic**: If output has very few peaks, lower SPM. If too many noisy peaks, raise SPM.

### Choosing Reproducibility Rule
| Scenario | Recommended Rule |
|----------|-----------------|
| 2-3 replicates | `"2"` or `"(n+1)/2"` |
| 4+ replicates | `"(n+1)/2"` or `"n/2"` |
| High variability | `"(n+1)/2"` (majority) |
| Low variability | Lower thresholds OK |

**Diagnostic**: Compare group peak counts. If a group has very few peaks, that group may have low reproducibility.

## Common Pitfalls

### File Format Issues
- ❌ **Space-delimited metadata** → Must be tab-delimited
- ❌ **Wrong column name** → Second column must be exactly "Group"
- ❌ **Inconsistent suffix** → All files must have same suffix
- ❌ **Compressed blacklist** → Uncompress .bed.gz files first
- ❌ **Missing trailing slash** → `--macs2dir` and `--outdir` must end with `/`

### MACS2 Parameter Issues
- ❌ **No `--call-summits`** → Script requires `*_summits.bed` files
- ❌ **Wrong MACS2 params** → Use exact parameters listed above
- ❌ **No Tn5 adjustment** → BAMs must be Tn5-offset corrected first

### Metadata Issues
- ❌ **Duplicate sample names** → Each sample must be unique
- ❌ **Wrong prefix** → Must exactly match filename minus suffix
- ❌ **Missing samples** → All summit files need metadata entry

### Genome Issues
- ❌ **BSgenome not installed** → Install genome-specific BSgenome package
- ❌ **Wrong genome name** → Use exact BSgenome "provider_version" value
- ❌ **Non-human/mouse genome** → May have chromosome naming issues

### Path Issues
- ❌ **Relative paths** → Use absolute paths for all arguments
- ❌ **Spaces in paths** → Avoid or quote properly
- ❌ **Missing directories** → Create output directory before running

## Troubleshooting

### No Output Files Generated
**Check**:
1. Did all summit files load correctly? (Check console output)
2. Are there any peaks passing `spm` filter?
3. Is reproducibility rule too stringent?

**Fix**: Lower `--spm` or relax `--rule`

### Very Few Peaks in Output
**Causes**:
- SPM threshold too high
- Reproducibility rule too stringent
- Poor sample quality

**Fix**: 
```bash
# Try more permissive settings
--spm 2 --rule "2"
```

### Script Crashes During Execution
**Common causes**:
1. Missing R packages
2. Wrong genome name
3. Corrupted summit files
4. Insufficient memory

**Diagnostic**:
```bash
# Test R package installation
Rscript -e "library(GenomicRanges); packageVersion('GenomicRanges')"

# Verify GenomicRanges version >1.44.0
```

### Different Peak Counts Per Group
**This is expected** - Different cell types have different numbers of accessible regions. Large differences may indicate:
- Quality differences between samples
- Biological differences (expected)
- Reproducibility issues within group

## Integration with Downstream Analysis

### Using Merged Peaks with ArchR
```r
# If using ArchR for scATAC-seq, you can provide custom peak set
library(ArchR)

# Read merged peaks
peaks <- rtracklayer::import("AllGroups-reproduciblePeaks.bed")

# Add to ArchR project
projATAC <- addPeakSet(
    ArchRProj = projATAC,
    peakSet = peaks,
    force = TRUE
)
```

### Using with Other Tools
The output BED file is compatible with:
- **HOMER**: Motif enrichment
- **DESeq2/edgeR**: Differential accessibility
- **chromVAR**: TF activity analysis
- **GREAT**: Regulatory region analysis
- **bedtools**: Further processing

## Best Practices

1. **Always use Tn5-adjusted BAMs** for MACS2
2. **Use exact MACS2 parameters** specified above
3. **Group samples logically** (by cell type, condition, etc.)
4. **Check group peak counts** to assess reproducibility
5. **Start with default parameters** (spm=5, rule="(n+1)/2")
6. **Compare multiple parameter sets** if unsure
7. **Document parameters used** for reproducibility

## Quick Reference

### Minimal Command
```bash
Rscript <project-root>/01_scripts/R_scripts/createIterativeOverlapPeakSet.R \
  --metadata metadata.txt \
  --macs2dir ./macs2_peaks/ \
  --outdir ./merged_peaks/ \
  --suffix _summits.bed \
  --blacklist hg38-blacklist.v2.bed \
  --genome hg38
```

### Typical Command (with all common options)
```bash
Rscript <project-root>/01_scripts/R_scripts/createIterativeOverlapPeakSet.R \
  --metadata /path/to/metadata.txt \
  --macs2dir /path/to/macs2/ \
  --outdir /path/to/output/ \
  --suffix _summits.bed \
  --blacklist /path/to/blacklist.bed \
  --genome hg38 \
  --spm 5 \
  --rule "(n+1)/2" \
  --extend 250
```

## When NOT to Use This Script

- ✅ **Use for**: Bulk ATAC-seq, pseudo-bulk ATAC-seq
- ❌ **Don't use for**: scATAC-seq (use ArchR's `addReproduciblePeakSet()` instead)
- ❌ **Don't use for**: ChIP-seq (different biology, use appropriate tools)
- ❌ **Don't use for**: Non-MACS2 peak calls (expects MACS2 summit format)

## Alternative: ArchR for scATAC-seq

If working with **single-cell ATAC-seq**, use ArchR's built-in function:

```r
library(ArchR)

# ArchR implements the same algorithm with scATAC optimizations
projATAC <- addReproduciblePeakSet(
    ArchRProj = projATAC,
    groupBy = "Clusters",
    pathToMacs2 = "/path/to/macs2",
    reproducibility = "2",  # Same as --rule
    peakMethod = "Macs2"
)
```

ArchR handles pseudo-bulk generation, normalization, and tiered merging automatically.

## References

- **Original Method**: Corces & Granja et al., Science 2018
- **ArchR Implementation**: Granja, Corces et al., Nature Genetics 2021
- **ATAC-seq Protocol**: Buenrostro et al., Nature Protocols 2015
- **Blacklists**: Amemiya et al., Scientific Reports 2019
- **GitHub Repository**: https://github.com/corceslab/ATAC_IterativeOverlapPeakMerging

---

## When not to use

- Do not use as a substitute for peak calling. Requires MACS2/MACS3 summit files as input.
- Do not use bedtools merge or bedtools cluster for the same task — they cause daisy-chaining or undercalling.

---

## See also

- `cellranger-arc-multiome`
- `scvi-peakvi`
- `chromvar-motif-accessibility`
- `pycistopic-atac-topic-modeling`

Upstream docs: https://www.science.org/doi/10.1126/science.aav1898
