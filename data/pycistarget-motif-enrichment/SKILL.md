---
name: pycistarget-motif-enrichment
description: "TF motif ENRICHMENT on scATAC region SETS (topics, DARs, peak clusters) via pycistarget's cisTarget and DEM, extracting cistromes for SCENIC+. Use when annotating topics or DAR sets with enriched motifs, or querying Aertslab feather databases. It aggregates over a region set — for per-cell TF activity use chromvar-motif-accessibility."
license: MIT
---

# pycistarget Motif Enrichment Skill

## Purpose

Motif enrichment analysis on scATAC-seq region sets to identify transcription factor binding sites. Derives **cistromes** (TF-bound region sets) for downstream GRN inference.

**Position in SCENIC+ ecosystem:**
```
pycisTopic (regions) → pycistarget (motifs) → SCENIC+ (GRN)
        ↓                      ↓                    ↓
  topic_regions.bed    TF-motif enrichment    eRegulons (TF→region→gene)
  DARs.bed             cistromes
```

**Upstream:** [pycisTopic skill](../pycistopic-atac-topic-modeling/SKILL.md) provides region sets
**Downstream:** [SCENIC+ skill](../scenic-grn-inference/SKILL.md) uses motif enrichment for GRN

## Installation

```bash
git clone https://github.com/aertslab/pycistarget.git
cd pycistarget
pip install -e .
```

```python
import pycistarget
pycistarget.__version__
```

## Two Approaches: cisTarget vs DEM

| Approach | Database | Method | Best For |
|----------|----------|--------|----------|
| **cisTarget** | `.rankings.feather` | NES (recovery curves) | Large region sets, robust rankings |
| **DEM** | `.scores.feather` | Wilcoxon test | Differential enrichment, contrast analysis |

**Recommendation:** Run BOTH approaches, then merge results for comprehensive coverage.

## Database Requirements

### Pre-computed Databases (Aertslab)
Download from: https://resources.aertslab.org/cistarget/

| Species | Genome | Rankings DB | Scores DB |
|---------|--------|-------------|-----------|
| Human | hg38 | `*.rankings.feather` | `*.scores.feather` |
| Mouse | mm10 | `*.rankings.feather` | `*.scores.feather` |

### Custom Database (2-3x better recovery)
```bash
# Download cluster-buster
wget https://resources.aertslab.org/cistarget/programs/cbust

# Create FASTA from peaks (1kb padding)
create_fasta_with_padded_bg_from_bed.sh ${GENOME} ${CHROMSIZES} peaks.bed out.fa 1000 yes

# Build both database types
create_cistarget_motif_databases.py -f out.fa -M motifs/ -o db_prefix \
    --bgpadding 1000 -t 20
# Outputs: db_prefix.rankings.feather, db_prefix.scores.feather
```

## Prepare Region Sets

### From pycisTopic Topics
```python
import pickle
import pyranges as pr
from pycistarget.utils import region_names_to_coordinates

# Load binarized topics
with open('binarized_topics.pkl', 'rb') as f:
    topics_dict = pickle.load(f)

# Convert to PyRanges (required input format)
region_sets = {
    topic: pr.PyRanges(region_names_to_coordinates(topics_dict[topic].index.tolist()))
    for topic in topics_dict.keys()
}
```

### From DARs (Differential Accessible Regions)
```python
with open('DARs.pkl', 'rb') as f:
    DARs_dict = pickle.load(f)

region_sets = {
    key: pr.PyRanges(region_names_to_coordinates(DARs_dict[key].index.tolist()))
    for key in DARs_dict.keys()
}
```

---

## Method 1: cisTarget (NES-based)

Uses ranking database to compute Normalized Enrichment Scores via recovery curves.

```python
from pycistarget.motif_enrichment_cistarget import cisTargetDatabase, run_cistarget

# Preload database (recommended for parameter testing)
db_path = 'regions_vs_motifs.rankings.feather'
ctx_db = cisTargetDatabase(db_path, region_sets)

# Optional: Remove dbcorr motifs
ctx_db.db_rankings = ctx_db.db_rankings[~ctx_db.db_rankings.index.str.contains("dbcorr")]

# Run cisTarget
cistarget_dict = run_cistarget(
    ctx_db=ctx_db,
    region_sets=region_sets,
    specie='mus_musculus',              # or 'homo_sapiens', 'drosophila_melanogaster'
    annotation_version='v10nr_clust',   # Motif annotation version
    path_to_motif_annotations='motifs-v10-nr.mmus-m0.001-o0.0.tbl',
    auc_threshold=0.005,                # AUC threshold for recovery
    nes_threshold=3.0,                  # NES cutoff (default: 3.0)
    rank_threshold=0.05,                # Top 5% of rankings
    annotation=['Direct_annot', 'Orthology_annot'],
    n_cpu=10,
    _temp_dir='/tmp/ray_spill'
)
```

### cisTarget Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `auc_threshold` | 0.005 | AUC threshold for recovery curve |
| `nes_threshold` | 3.0 | Minimum NES to consider enriched |
| `rank_threshold` | 0.05 | Fraction of top rankings to use |
| `annotation` | Direct + Ortho | TF annotation sources |

### View Results
```python
from pycistarget.motif_enrichment_cistarget import cisTarget_results

# Display enrichment table for a topic
cisTarget_results(cistarget_dict, name='Topic21')

# Export to HTML
for key in cistarget_dict.keys():
    cistarget_dict[key].motif_enrichment.to_html(
        open(f'cistarget_{key}.html', 'w'), escape=False, col_space=80
    )
```

### Save/Load Results
```python
import pickle

# Save
with open('cistarget_dict.pkl', 'wb') as f:
    pickle.dump(cistarget_dict, f)

# Load
with open('cistarget_dict.pkl', 'rb') as f:
    cistarget_dict = pickle.load(f)
```

---

## Method 2: DEM (Differential Enrichment of Motifs)

Uses scores database with Wilcoxon tests for differential motif enrichment.

```python
from pycistarget.motif_enrichment_dem import DEMDatabase, DEM

# Preload scores database
db_path = 'regions_vs_motifs.scores.feather'
dem_db = DEMDatabase(db_path, region_sets)

# Run DEM
DEM_dict = DEM(
    dem_db=dem_db,
    region_sets=region_sets,
    specie='mus_musculus',
    contrasts='Other',                  # 'Other', 'Shuffle', or custom list
    name='DEM',
    fraction_overlap=0.4,               # Min overlap to map regions
    max_bg_regions=500,                 # Max background regions
    adjpval_thr=0.05,                   # FDR threshold
    log2fc_thr=0.25,                    # Min log2FC (use 1.0 for stringent)
    mean_fg_thr=0,                      # Min foreground mean
    motif_hit_thr=None,                 # Auto-calculate optimal threshold
    annotation=['Direct_annot', 'Motif_similarity_annot',
                'Orthology_annot', 'Motif_similarity_and_Orthology_annot'],
    n_cpu=10,
    tmp_dir='/tmp/pycistarget'
)
```

### DEM Contrast Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `'Other'` | Background = other region sets | Compare topics/cell types |
| `'Shuffle'` | Background = shuffled sequences | De novo motif analysis |
| Custom list | Explicit contrasts | Specific comparisons |

**For 'Shuffle' mode** (requires cluster-buster):
```python
DEM_dict = DEM(
    dem_db=dem_db,
    region_sets=region_sets,
    specie='mus_musculus',
    contrasts='Shuffle',
    cluster_buster_path='/path/to/cbust',
    path_to_genome_fasta='mm10.fa',
    path_to_motifs='/path/to/motifs/',
    ...
)
```

### DEM Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `fraction_overlap` | 0.4 | Min overlap to map regions to DB |
| `max_bg_regions` | None | Limit background (None = all) |
| `adjpval_thr` | 0.05 | FDR threshold |
| `log2fc_thr` | 1.0 | Min log2 fold change |
| `mean_fg_thr` | 0 | Min mean CRM in foreground |
| `motif_hit_thr` | None | Auto-calculate per motif |

### View DEM Results
```python
from pycistarget.motif_enrichment_dem import DEM_results

# Display enrichment for a topic
DEM_dict.DEM_results('Topic8')

# Export to HTML
for key in DEM_dict.motif_enrichment.keys():
    DEM_dict.motif_enrichment[key].to_html(
        open(f'DEM_{key}.html', 'w'), escape=False, col_space=80
    )
```

---

## Extract Cistromes

Cistromes are TF-bound region sets derived from motif enrichment.

```python
# From cisTarget results
cistromes = cistarget_dict['Topic21'].cistromes['Region_set']

# List available TFs
print(cistromes.keys())
# dict_keys(['BATF_(1914r)', 'IRF4_(1009r)', 'BATF_extended_(2216r)', ...])

# Direct annotation = exact motif match
# Extended = includes orthologs and similarity matches

# Get regions for a specific TF
batf_regions = cistromes['BATF_(1914r)']
```

### Cistrome Naming Convention
```
TF_NAME_(Xr)           # Direct annotation, X regions
TF_NAME_extended_(Xr)  # Extended annotation (orthologs + similarity)
```

---

## SCENIC+ Integration

### Within Snakemake Pipeline
SCENIC+ automatically runs pycistarget. Configure in `config.yaml`:

```yaml
params_motif_enrichment:
  dem_adj_pval_thr: 0.05      # DEM FDR threshold
  ctx_nes_threshold: 3.0      # cisTarget NES threshold
  ctx_auc_threshold: 0.005    # cisTarget AUC threshold
  ctx_rank_threshold: 0.05    # cisTarget rank threshold

cistarget_databases:
  ctx_db: "/path/to/*.rankings.feather"
  dem_db: "/path/to/*.scores.feather"
  motif_annotation: "/path/to/motifs-v10-nr.mmus.tbl"
```

### Standalone (Pre-SCENIC+)
Run pycistarget separately, then provide results to SCENIC+:

```python
# 1. Run both methods
cistarget_dict = run_cistarget(...)
DEM_dict = DEM(...)

# 2. Save for SCENIC+
pickle.dump(cistarget_dict, open('cistarget_results.pkl', 'wb'))
pickle.dump(DEM_dict, open('DEM_results.pkl', 'wb'))

# 3. Update SCENIC+ config to use pre-computed results
```

---

## Non-Multiome / Unpaired Data

For separate RNA and ATAC experiments, pycistarget analysis remains the same. The metacell approach is handled by SCENIC+, not pycistarget.

**Key requirement:** Ensure region sets (from pycisTopic) are derived from the ATAC data that will be used in SCENIC+.

See [SCENIC+ skill](../scenic-grn-inference/SKILL.md) for metacell configuration.

For R → Python data export (Signac/ArchR → pycisTopic → pycistarget), see [scenic-r-python-interop](../scenic-r-python-interop/SKILL.md).

---

## Quality Metrics

### cisTarget
| Metric | Good | Interpretation |
|--------|------|----------------|
| NES | >3.0 | Significant enrichment |
| AUC | >0.01 | Strong recovery |
| # Enriched motifs | >10 | Sufficient coverage |

### DEM
| Metric | Good | Interpretation |
|--------|------|----------------|
| adj_pval | <0.05 | Significant |
| log2FC | >1.0 | 2-fold enrichment |
| mean_fg | >0.5 | Detectable signal |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No enriched motifs | Lower NES threshold (2.5), check species match |
| Region overlap failures | Increase `fraction_overlap` or check genome version |
| Memory errors | Reduce `max_bg_regions`, process in batches |
| Slow DEM with Shuffle | Use 'Other' contrast, or reduce motif set |
| Empty cistromes | Check annotation version matches database |
| Species mismatch | Ensure DB, annotation, and data use same genome |
| Batch motif enrichment | Use `run_pycistarget` wrapper from `scenicplus.wrappers.run_pycistarget` for batch processing |

## Quick Checklist

- [ ] Database matches genome version (hg38/mm10)
- [ ] Region sets in PyRanges format
- [ ] Motif annotations match database version
- [ ] Species parameter correct
- [ ] Both cisTarget AND DEM run for comprehensive coverage
- [ ] Results saved as pickle for SCENIC+

## API Reference

Full documentation: https://pycistarget.readthedocs.io/en/latest/api.html

---

## When not to use

- Do not use for per-cell TF activity scoring. Use chromvar-motif-accessibility.
- Do not use for TF footprinting / occupancy evidence. Use tf-footprint-differential-analysis.

---

## See also

- `pycistopic-atac-topic-modeling`
- `scenic-grn-inference`
- `chromvar-motif-accessibility`
- `tf-footprint-differential-analysis`
