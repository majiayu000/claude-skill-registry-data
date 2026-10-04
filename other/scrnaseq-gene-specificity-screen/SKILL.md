---
name: scrnaseq-gene-specificity-screen
description: Determine whether a set of genes is specifically highly expressed in particular cell types or tissues using the Human Protein Atlas (HPA) public API. Downloads the RNA expression matrices for 154 cell types (nCPM) and 51 tissues (nTPM), screens for genes whose peak falls inside a user-defined cell-type group (such as the megakaryocytic lineage or hematopoietic cells), and outputs per-cell-type / per-tissue bar charts plus Excel/TSV results. Use it to judge the cell-type or tissue specificity of a gene list, to annotate any gene list or cNMF/GEP gene module for expression specificity, or to find lineage-specific candidate genes with unknown function. Requires a gene list from the user (CSV/TSV/XLSX with a gene or symbol column) and target cell-type group definitions.
---

# HPA gene expression specificity screening

Determine whether the genes in a list are specifically highly expressed in particular cell types
or tissues. All data come from the Human Protein Atlas public API; no registration is required.

## Workflow

Input: a gene list (CSV/TSV/XLSX; the `gene` / `symbol` / `query_gene` column is recognized;
grouping columns such as `GEP` are optional).

1. **Download the expression matrices** (resumable, cached in `cache/`):

```bash
python scripts/step1_fetch_hpa.py --gene-list genes.xlsx --output-dir out/ --config config.json
```

Outputs `HPA_RNA_expression.xlsx` (two sheets: RNA_Cell_Types, 154 cell types nCPM;
RNA_Tissues, 51 tissues nTPM) plus `validation_step1.json`. For HPA endpoint behaviour and
pitfalls see [references/hpa-api.md](references/hpa-api.md).

2. **Plot** (two bar charts per gene: per cell type, per tissue):

```bash
python scripts/step2_plot_and_merge.py --gene-list genes.xlsx --hpa-excel out/HPA_RNA_expression.xlsx \
    --output-dir out/ --config config.json --workers 4
```

Outputs `gene_plots/<gene>/` (or subdirectories per grouping column) plus the final Excel with
the grouping information merged in.
Large gene lists produce a great many images (4,110 genes ≈ 8,200+ PNGs, roughly 10 minutes) —
always use `--workers`.

3. **Specificity screening**:

```bash
python scripts/screen_specificity.py --hpa-excel out/HPA_RNA_expression.xlsx \
    --config config.json --out-dir out/ [--membership gene_groups.tsv]
```

Outputs `selected_genes.tsv` (the `driver` column records which target group drove the
selection) and `screening_summary.json` (including the borderline gene list).

The rule in one sentence: **a gene is selected when its cell-type peak falls inside a target
group; tissue information is annotation only and never filters**.
For the rationale behind the rule and its tuning (priority order, borderline threshold) see
[references/specificity-rules.md](references/specificity-rules.md) — required reading before
changing the rule.

## Configuration

Copy `assets/config.example.json` and edit it. Key fields:

- `specificity_groups`: the ordered target cell-type groups (dict order = priority; put narrow
  lineages first). The example defines the megakaryocytic lineage + other hematopoietic cells;
  switching to any other lineage only means changing these two cell-type name lists.
  Cell-type names must match the HPA column names exactly (case-sensitive); check them against
  the header of the Excel produced by step 1.
- `reference_tissue`: an additional tissue for annotation (e.g. "bone marrow"); it does not take
  part in screening.
- The remaining fields are download/plot parameters; the defaults are verified and normally need
  no changes.

## Dependencies and runtime environment

`pip install -r requirements.txt` (requests, openpyxl, Pillow; plotting uses Pillow and does not
depend on matplotlib). Access to www.proteinatlas.org is required.

## Known limitations

- Genes with several same-name Ensembl entries (observed in practice for MATR3, POLR2J3) are
  listed as warnings during validation and need a manual decision on which entry to use.
- About 0.4% of gene symbols are not found in HPA; the row is left blank and listed under
  `missing_genes` in the metadata.
- The optional follow-up analyses (STRING networks, per-gene PubMed literature research, review
  slide decks) are not part of this skill; run them on the screening results with the appropriate
  tools.
