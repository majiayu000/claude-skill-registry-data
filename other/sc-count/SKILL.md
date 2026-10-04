---
# AUTO-GENERATED header from skill.yaml — do not edit by hand.
# Edit skill.yaml, then run: python scripts/generate_skill_md.py <skill_dir>
name: sc-count
description: Load when turning scRNA FASTQ (or existing CellRanger/STARsolo/SimpleAF/kb-python output)
  into a downstream-ready AnnData. Skip when reads are already counted into AnnData (use sc-standardize-input);
  raw quality assessment only (use sc-fastq-qc).
version: 0.3.0
author: OmicsClaw
license: MIT
emoji: 🧬
tags:
- singlecell
- scrna
- counting
- cellranger
- starsolo
- simpleaf
- kb-python
requires:
- anndata
- matplotlib
- numpy
- pandas
- scanpy
- scipy
- seaborn
---

# sc-count

## When to use

The user has FASTQ files (or pre-existing tool output directories) and
wants per-cell counts in OmicsClaw's canonical AnnData contract.  Four
backends share one CLI: `cellranger`, `starsolo`, `simpleaf`,
`kb-python`.  When passed an already-counted directory the skill
re-canonicalises rather than re-counts.  Pairs with `sc-fastq-qc`
upstream (read QC) and `sc-multi-count` downstream (merging multiple
samples).

## Inputs & Outputs

<!-- AUTO-GENERATED from skill.yaml (interface) — do not edit by hand. Regenerate: python scripts/generate_skill_md.py <skill_dir> -->

**Inputs**

- Input kinds: `file`, `directory`
- Modalities: scrna
- File types: `.fastq`, `.fq`, `.h5ad`
- FASTQ structure: valid first record; `paired` layout
- Directory layouts (any): `paired-fastq`, `tenx-matrix`, `cellranger-output`, `starsolo-output`, `pseudoalign-output`

**Outputs**

- `tables/Summary.csv`
- `tables/backend_summary.csv`
- `tables/barcode_metrics.csv`
- `tables/barcodes.tsv`
- `tables/cell_metadata.csv`
- `tables/count_summary.csv`
- `tables/features.tsv`
- `tables/genes.tsv`
- `tables/metrics_summary.csv`
- `tables/simpleaf_t2g.tsv`
- `figures/barcode_rank.png`
- `figures/count_complexity_scatter.png`
- `figures/count_distributions.png`
- `3M-february-2018.txt`
- `737K-august-2016.txt`
- `Aligned.sortedByCoord.out.bam`
- `analysis_summary.txt`
- `cells_x_genes.barcodes.txt`
- `cells_x_genes.genes.txt`
- `multiqc_report.html`
- `possorted_genome_bam.bam`
- `processed.h5ad`
- `quants_mat_cols.txt`
- `quants_mat_rows.txt`
- `simpleaf_index.json`
- `standardized_input.h5ad`
- `web_summary.html`
- `report.md`
- `result.json`
- Processed AnnData (`saves_h5ad`)

## Flow

1. Resolve `--input`; if it's an existing CellRanger / STARsolo / SimpleAF / kb-python output dir, re-canonicalise instead of running the backend.
2. Otherwise validate backend prerequisites (chemistry, reference, t2g for kb-python, whitelist for STARsolo).
3. Run the chosen backend against the FASTQ (and `--read2` if explicit).
4. Load the resulting matrix into AnnData; canonicalise (`layers["counts"]`, `adata.raw`, gene-name harmonisation).
5. Render barcode-rank + count-distribution figures.
6. Emit `processed.h5ad` + `report.md` + `result.json`.

## Gotchas

- **Missing input path → hard fail.** `sc_count.py:356` raises `FileNotFoundError(f"Input path not found: {input_path}")`.  Common when the FASTQ dir is on a network mount that has not been resolved at run time.
- **STARsolo requires explicit chemistry.** `sc_count.py:420` raises `ValueError("STARsolo runs require an explicit `--chemistry` value such as `10xv3`.")` when chemistry is left at the `auto` default.  STARsolo currently supports `10xv2`, `10xv3`, and `10xv4`; pass one of those.
- **Backend prerequisites are validated up front.** `sc_count.py:401`, `:423`, `:451` raise `ValueError` for missing `--reference` (CellRanger/STARsolo/simpleaf), missing `--t2g` (kb-python), or unsupported `--chemistry` for STARsolo.  No silent fallback to a different backend — pick a feasible one before invoking.
- **Re-canonicalising-existing-output is detected by directory shape, not a flag.** If `--input` points at a CellRanger output dir (e.g. one with `outs/raw_feature_bc_matrix/`), the skill skips counting and just imports the matrix.  No flag separates the two paths; verify by inspecting `result.json["data"]["execution"]` (empty list = re-canonicalise; populated = backend invoked) or by reading `tables/backend_summary.csv` (lists the backend metrics only when the backend ran).

## Key CLI

```bash
# Demo (synthetic FASTQ + CellRanger-shaped output)
python omicsclaw.py run sc-count --demo --output /tmp/sc_count_demo

# CellRanger over FASTQ
python omicsclaw.py run sc-count \
  --input fastq_dir/ --output results/ \
  --reference cellranger_transcriptome --threads 16

# STARsolo (requires explicit chemistry)
python omicsclaw.py run sc-count \
  --input fastq_dir/ --output results/ \
  --reference star_genome_dir --chemistry 10xv3 --whitelist barcodes.tsv

# Re-canonicalise an existing CellRanger output directory
python omicsclaw.py run sc-count \
  --input cellranger_output_dir/ --output results/
```

## See also

- `references/parameters.md` — every CLI flag and per-backend prerequisite
- `references/methodology.md` — backend selection guide, re-canonicalise vs re-run logic
- `references/output_contract.md` — `processed.h5ad` schema + table layouts
- Adjacent skills: `sc-fastq-qc` (upstream — read-quality check before counting), `sc-multi-count` (downstream — merge multiple sample outputs), `sc-standardize-input` (parallel — for AnnData from outside OmicsClaw)
