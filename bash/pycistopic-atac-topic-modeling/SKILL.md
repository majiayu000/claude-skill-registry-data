---
name: pycistopic-atac-topic-modeling
description: "MALLET collapsed-Gibbs LDA topic modeling on scATAC fragment counts via pycisTopic, identifying co-accessible region programs and candidate enhancer sets. Use as the upstream step of SCENIC+: pseudobulk, peak calling, consensus peaks, LDA, topic binarization, DAR detection. For downstream motif enrichment use pycistarget-motif-enrichment."
license: MIT
---

# pycisTopic Skill

## Purpose

Topic modeling on scATAC-seq data using LDA to identify co-accessible regulatory programs. Part of SCENIC+ ecosystem.

**Downstream:**
- [pycistarget](../pycistarget-motif-enrichment/SKILL.md) for motif enrichment + cistrome analysis
- [SCENIC+ GRN inference](../scenic-grn-inference/SKILL.md) for TF regulatory networks

## Data Flow: pycisTopic → pycistarget → SCENIC+

```
scATAC fragments → pycisTopic → cistopic_obj.pkl + region_sets/*.bed
                                          ↓
                                    pycistarget (motif enrichment)
                                          ↓
scRNA AnnData  →  →  →  →  →  →  → SCENIC+ → eRegulons (TF→region→gene)
```

## Installation

```bash
pip install pycisTopic
# MALLET (required for LDA)
wget https://github.com/mimno/Mallet/releases/download/v202108/Mallet-202108-bin.tar.gz
tar -xzf Mallet-202108-bin.tar.gz
export MALLET_PATH="$(pwd)/Mallet-202108/bin/mallet"
```

## Workflow Summary

| Stage | Function | Time |
|-------|----------|------|
| 1. QC | `pycistopic qc` CLI | ~5 min |
| 2. Pseudobulk | `export_pseudobulk()` | ~10 min |
| 3. Peaks | `peak_calling()` → `get_consensus_peaks()` | ~15 min |
| 4. Object | `create_cistopic_object_from_fragments()` | ~10 min |
| 5. LDA | `run_cgs_models_mallet()` | ~2-4 hr |
| 6. Analysis | Binarization, DARs, gene activity | ~30 min |

---

## Stage 1: QC (CLI - v2.0+)

```bash
# Get TSS annotations
pycistopic tss get_tss --output tss.bed --name "mmusculus_gene_ensembl" \
    --to-chrom-source ucsc --ucsc mm10

# Run QC (auto-thresholds via Otsu)
pycistopic qc --fragments fragments.tsv.gz \
    --regions consensus_peaks.bed --tss tss.bed --output qc/sample
```

**QC Thresholds (auto-detected):** TSS >7, unique frags >1500, FRIP >0.3

**Python QC Alternative:**
```python
from pycisTopic.qc import compute_qc_stats, get_barcodes_passing_qc_for_sample

(frag_stats, insert_dist, tss_norm, tss_per_cb) = compute_qc_stats(
    fragments_df_pl, regions_df_pl, tss_annotation,
    min_fragments_per_cb=10, collapse_duplicates=True)

cbs_passing, thresholds = get_barcodes_passing_qc_for_sample(
    sample_id, pycistopic_qc_output_dir, use_automatic_thresholds=True)
```

---

## Stage 2-3: Pseudobulk Peaks

```python
from pycisTopic.pseudobulk_peak_calling import export_pseudobulk, peak_calling
from pycisTopic.iterative_peak_calling import get_consensus_peaks

# 1. Pseudobulk by cell type
bw_paths, bed_paths = export_pseudobulk(
    input_data=cell_data, variable="cell_type", sample_id_col="sample_id",
    chromsizes=chromsizes, path_to_fragments=fragments_dict, n_cpu=10)

# 2. MACS peak calling (use macs3, not macs2)
narrow_peaks = peak_calling(
    macs_path="macs3", bed_paths=bed_paths, outdir="macs_out",
    genome_size='mm', input_format='BEDPE', n_cpu=10)

# 3. Consensus peaks (TCGA iterative filtering)
consensus = get_consensus_peaks(narrow_peaks, peak_half_width=250,
    chromsizes=chromsizes, path_to_blacklist=blacklist_bed)
consensus.to_bed("consensus_peaks.bed")
```

---

## Stage 4: Create cisTopic Object

### From Fragments (Standard)
```python
from pycisTopic.cistopic_class import create_cistopic_object_from_fragments

cistopic_obj = create_cistopic_object_from_fragments(
    path_to_fragments=fragments_dict, path_to_regions="consensus_peaks.bed",
    path_to_blacklist=blacklist_bed, valid_bc=barcodes_passing_qc)
cistopic_obj.add_cell_data(cell_metadata)
```

### From Count Matrix (Signac/ArchR Import)
```python
from pycisTopic.cistopic_class import create_cistopic_object
cistopic_obj = create_cistopic_object(fragment_matrix=count_matrix,
    cell_names=cell_names, region_names=region_names,
    tag_cells=False, project="my_project")
```

**Export from Signac (Seurat v5):**
```r
# Seurat v5 uses layer=, not slot= (v4 used slot="counts")
DefaultAssay(obj) <- "peaks_hub_filtered"
peak_matrix <- GetAssayData(obj, layer = "counts")
region_names <- paste0(seqnames(granges(obj[["peaks_hub_filtered"]])), ":",
    start(granges(obj[["peaks_hub_filtered"]])), "-",
    end(granges(obj[["peaks_hub_filtered"]])))
```

For complete R → Python handoff patterns (h5ad export, fragment harmonization, metadata), see [scenic-r-python-interop](../scenic-r-python-interop/SKILL.md).

---

## Starting with an Existing Peak Atlas

If you already have a consensus peak set (e.g., from ArchR, a published atlas, or a prior analysis), skip Stages 2-3 entirely:

```python
from pycisTopic.cistopic_class import create_cistopic_object_from_fragments

# Use existing peaks — no pseudobulk or MACS needed
cistopic_obj = create_cistopic_object_from_fragments(
    path_to_fragments=fragments_dict,
    path_to_regions="peak_atlas.bed",        # Your pre-built consensus peaks
    path_to_blacklist="mm10_blacklist.bed",
    valid_bc=barcodes_passing_qc
)
```

Alternatively, if you've already counted peaks in R (e.g., via Signac), use `create_cistopic_object()` with the pre-counted matrix — see [scenic-r-python-interop](../scenic-r-python-interop/SKILL.md) Scenario A and D.

Proceed directly to Stage 5 (LDA Topic Modeling).

---

## Stage 5: LDA Topic Modeling

```python
from pycisTopic.lda_models import run_cgs_models_mallet, evaluate_models
import os
os.environ['MALLET_MEMORY'] = '200G'

models = run_cgs_models_mallet(
    cistopic_obj, mallet_path="Mallet-202108/bin/mallet",
    n_topics=[10, 20, 30, 40, 50], n_cpu=12, n_iter=500,
    alpha=50, alpha_by_topic=True, eta=0.1,
    tmp_path="/tmp/mallet", save_path="models/")

model = evaluate_models(models, return_model=True)
cistopic_obj.add_LDA_model(model)
```

**Model Selection:**
| Metric | Better | Notes |
|--------|--------|-------|
| Coherence (Mimno) | Higher | Topics have co-accessible regions |
| Log-likelihood | Higher | Model fits data |
| Arun_2010 | Lower | Inverted in plots |

---

## Stage 6: Downstream Analysis

### Topic Binarization

`binarize_topics()` returns a **single dict** per call (not a tuple). Call separately for region and cell targets:

```python
from pycisTopic.topic_binarization import binarize_topics

# Region binarization (default target='region')
region_topics = binarize_topics(cistopic_obj, method='otsu')      # returns dict
# Cell binarization (separate call)
cell_topics = binarize_topics(cistopic_obj, target='cell', method='li')  # returns dict
```

### Differential Accessibility
```python
from pycisTopic.diff_features import impute_accessibility, find_diff_features
import numpy as np

imputed = impute_accessibility(cistopic_obj, scale_factor=10**6)
markers = find_diff_features(cistopic_obj, imputed, variable='cell_type',
    adjpval_thr=0.05, log2fc_thr=np.log2(1.5), n_cpu=5)
```

### Gene Activity + Label Transfer
```python
from pycisTopic.gene_activity import get_gene_activity
from pycisTopic.label_transfer import label_transfer

gene_act, weights = get_gene_activity(imputed, pr_annotation, chromsizes,
    use_gene_boundaries=True, upstream=[1000,100000], downstream=[1000,100000],
    distance_weight=True, gini_weight=True)

labels = label_transfer(rna_adata, atac_adata, labels_to_transfer=['cell_type'],
    methods=['harmony', 'scanorama'])  # Best performers
```

### Signature Enrichment (AUCell)
```python
from pycisTopic.signature_enrichment import signature_enrichment

rankings = imputed.make_rankings()
auc_scores = signature_enrichment(rankings, region_signatures,
    enrichment_type='region', auc_threshold=0.05)
```

### pyGREAT Functional Enrichment
```python
from pycisTopic.pyGREAT import pyGREAT

great_results = pyGREAT(region_topics, species='mm10', n_cpu=10)
# Returns dict of DataFrames with GO/pathway enrichments
```

---

## SCENIC+ Export (Required Files)

```python
import pickle
from pycisTopic.utils import region_names_to_coordinates
import os

# 1. cisTopic object
pickle.dump(cistopic_obj, open('cistopic_obj.pkl', 'wb'))

# 2. Region sets as BED files
os.makedirs('region_sets', exist_ok=True)
for topic in region_topics:
    region_names_to_coordinates(region_topics[topic].index).to_csv(
        f'region_sets/{topic}.bed', sep='\t', header=False, index=False)

# 3. (For unpaired) Ensure cell_type labels match RNA vocabulary
cistopic_obj.cell_data['cell_type'] = ...  # Must match scRNA labels exactly
```

**Handoff Checklist for SCENIC+:**
- [ ] `cistopic_obj.pkl` saved with model attached
- [ ] `region_sets/*.bed` files created (one per topic + DARs)
- [ ] Cell metadata includes matching annotations
- [ ] (Unpaired only) ≥50 cells per group

---

## Loom Export (SCope Visualization)

```python
from pycisTopic.loom import export_region_accessibility_to_loom

export_region_accessibility_to_loom(
    accessibility_matrix=imputed, cistopic_obj=cistopic_obj,
    binarized_topic_region=region_topics, binarized_cell_topic=cell_topics,
    out_fname='accessibility.loom', cluster_annotation=['cell_type'],
    tree_structure=('project', 'pycisTopic', 'ATAC'), nomenclature='mm10')
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MALLET memory error | Set `MALLET_MEMORY='200G'`; reduce n_topics |
| TabixFile error | Ensure `.tbi` index exists: `tabix -p bed fragments.tsv.gz` |
| No peaks found | Check genome version matches chromsizes |
| Model convergence | Increase `n_iter` to 1000 |
| Ray parallelism fails | Set `_temp_dir` to local SSD path |
| Barcode mismatch | Check `split_pattern` matches your format |
| Empty markers | Lower `adjpval_thr`, check cell counts per group |
| Label transfer fails | Ensure matching genes between RNA/ATAC |

---

## Performance Tips

- **Memory:** `MALLET_MEMORY='200G'` for large datasets
- **Parallel:** `n_cpu=20` in peak_calling, find_diff_features
- **Binarization:** `ntop=3000` for balanced region sets (vs variable otsu)
- **Imputation:** Use `chunk_size=20000` to control memory
- **Ray:** Set `_temp_dir` to fast local storage

---

## Quick Reference

```python
# Minimal workflow
from pycisTopic.cistopic_class import create_cistopic_object_from_fragments
from pycisTopic.lda_models import run_cgs_models_mallet, evaluate_models
from pycisTopic.topic_binarization import binarize_topics
from pycisTopic.diff_features import impute_accessibility

cistopic_obj = create_cistopic_object_from_fragments(path_to_fragments, path_to_regions)
models = run_cgs_models_mallet(cistopic_obj, n_topics=[20,30,40], n_cpu=12)
cistopic_obj.add_LDA_model(evaluate_models(models, return_model=True))
topics = binarize_topics(cistopic_obj, method='otsu')
imputed = impute_accessibility(cistopic_obj)
```

## API Reference

Full documentation: https://pycistopic.readthedocs.io/en/latest/api.html

---

## When not to use

- Do not use for cell-type clustering of scATAC. Use scvi-peakvi or ArchR/Signac workflows.
- Do not use in isolation for TF inference. Requires downstream pycistarget + SCENIC+.

---

## See also

- `pycistarget-motif-enrichment` — Motif enrichment on binarized topics
- `scenic-grn-inference` — SCENIC+ eRegulon inference (downstream)
- `iterative-peak-merging`
- `chromvar-motif-accessibility`
- `scenic-r-python-interop` — R → Python data handoff (Signac, ArchR, cisTopic R bridge)
