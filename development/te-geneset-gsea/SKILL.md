---
name: te-geneset-gsea
description: "TE-aware GSEA — runs clusterProfiler::GSEA on TE subfamily-ranked DE lists using the family/class GMTs produced by annotate-bulk-rnaseq-data (TE path). Use when running GSEA on TE subfamily ranks, where GMT gene_symbol holds subfamily IDs rather than Ensembl symbols. For gene or MSigDB GSEA use bulk-rnaseq-gsea."
license: MIT
---

# TE Geneset GSEA (TE Family/Class GMT)

## Overview

This skill covers GSEA on transposable-element expression data using the family/class GMT files produced by the `annotate-bulk-rnaseq-data` TE path. The ID space is TE **subfamily** (the `gene_symbol` column in the GMT), not Ensembl gene symbols — this is the critical distinction from `bulk-rnaseq-gsea`. The `clusterProfiler::GSEA()` machinery is shared at the algorithm level, but the T2G/T2N column names and the `@geneSets` slot fix differ (TE GMTs use `gs_name`/`gene_symbol`; bulk uses `term`/`gene`).

**When to use this skill:**
- Running GSEA against TE family or class gene sets from limma-voom DE results on the combined gene+TE DGEList
- The ranked list uses TE **subfamily** IDs as names (matching the GMT `gene_symbol` column)
- Family GMT (`<id>_TE_family.gmt`) or class GMT (`<id>_TE_class.gmt`) is available from the annotate step

**When NOT to use this skill:**
- Gene-symbol or MSigDB GSEA (Hallmark, KEGG, Reactome, GO) → use `bulk-rnaseq-gsea`
- You have Ensembl IDs as rownames → convert to subfamily IDs first (via `build_te_annotation`)

---

## Decision Tree

```
Running GSEA on TE expression data?
|
+-- Ranked list has TE subfamily IDs as names
|   AND GMT is a TE family/class GMT from annotate-bulk-rnaseq-data?
|   --> use this skill (te-geneset-gsea)
|       |
|       +-- Family-level sets (dozens of families)?
|       |   --> load <id>_TE_family.gmt  (gs_name = family, gene_symbol = subfamily)
|       |
|       +-- Class-level sets (~6 classes, very few sets)?
|           --> load <id>_TE_class.gmt   (gs_name = class, gene_symbol = subfamily)
|               NOTE: use relaxed min_size (e.g. 3) — default 5 drops most class sets
|
+-- Ranked list has gene symbols (Il2ra, Cd3e, ...)?
    --> use bulk-rnaseq-gsea (MSigDB / custom-db path)
```

---

## Quick Start

Minimal working example — family-level TE GSEA from limma-voom DE results.

```r
library(clusterProfiler)
library(data.table)

# --- 1. Load GMT (gs_name = TE family, gene_symbol = TE subfamily) -----------
gmt_path <- "03_results/objects/EXP001_TE_family.gmt"
T2G <- fread(gmt_path, header = FALSE, col.names = c("gs_name", "gs_description", "gene_symbol"))
T2N <- unique(T2G[, .(gs_name, gs_description)])

# --- 2. Build ranked list (TE subfamilies as names, t-statistic as value) -----
de_te  <- readRDS("03_results/objects/EXP001_combined_DGEList.rds")
# de_te$table must have is_te == TRUE rows; subfamily IDs are rownames
ranked <- sort(setNames(de_te$table$t[de_te$table$is_te], rownames(de_te$table)[de_te$table$is_te]),
               decreasing = TRUE)

# --- 3. Overlap sanity check BEFORE running GSEA ----------------------------
overlap <- sum(T2G$gene_symbol %in% names(ranked))
message("Overlap: ", overlap, " / ", length(unique(T2G$gene_symbol)))
# If overlap < 30% of the GMT members, ID spaces don't match -> stop and debug

# --- 4. Run GSEA -------------------------------------------------------------
gsea_fam <- clusterProfiler::GSEA(
    geneList     = ranked,
    TERM2GENE    = T2G[, .(gs_name, gene_symbol)],
    TERM2NAME    = T2N,
    pvalueCutoff = 1.0,
    minGSSize    = 5,
    maxGSSize    = 500,
    seed         = 123,
    eps          = 0
)

# --- 5. Fix @geneSets slot for enrichplot compatibility ----------------------
gsea_fam@geneSets <- split(T2G$gene_symbol, T2G$gs_name)

stopifnot(is(gsea_fam, "gseaResult"))
message("TE family GSEA: ", nrow(gsea_fam@result), " sets returned")
```

**Verify it worked:**

```r
# ID-space check
stopifnot(sum(T2G$gene_symbol %in% names(ranked)) / length(unique(T2G$gene_symbol)) > 0.3)
# Non-empty result
stopifnot(nrow(gsea_fam@result) > 0)
# @geneSets slot populated (required for enrichplot::gseaplot2)
stopifnot(length(gsea_fam@geneSets) > 0)
```

---

## Progressive Depth

### Basic Usage

Load the GMT with `fread` or `read.gmt`. The three-column format is `gs_name \t gs_description \t gene_symbol` (one row per subfamily member). Use `TERM2GENE = T2G[, .(gs_name, gene_symbol)]` and `TERM2NAME = T2N`. Always run the overlap check before GSEA — if `sum(T2G$gene_symbol %in% names(ranked)) == 0` the result is silently empty.

### Intermediate Usage

**Class-level GMT — relaxed `min_size`:** The class GMT contains only ~6 sets (LINE, SINE, LTR, DNA, Simple_repeat, Low_complexity). The default `minGSSize = 5` will retain the larger classes but drop small ones. Use `minGSSize = 3` to keep all non-trivial class sets. Verify with `nrow(gsea_fam@result)` before reporting.

**Normalizing results to CSV:** run TE sets through bulkiRNA `gs_test()` and `gs_to_master()` (skill `bulk-rnaseq-gsea`). Label the provider `"TE_FAMILY"` or `"TE_CLASS"` with `gsdb_register(database = )` so rows are distinguishable in the master table. Prefix pathway IDs with `TE_FAMILY_` / `TE_CLASS_` (SCREAMING_SNAKE) to avoid collisions with MSigDB IDs.

### Advanced Usage

**Combining TE and gene GSEA in one master table:** Run `bulk-rnaseq-gsea` for gene pathways and `te-geneset-gsea` for TE sets, then idempotently append TE rows to `master_gsea_table.csv`. Use the `filter(database != "TE_FAMILY") |> bind_rows(...)` pattern from `bulk-rnaseq-gsea` references/master-tables.md — the 13-column schema is shared.

For the full GMT column contract and annotated code walkthroughs → see `references/te-gsea.md`.

---

## Verification Checklist

After running this skill, confirm:

- [ ] **Overlap check passed:** `sum(T2G$gene_symbol %in% names(ranked)) / length(unique(T2G$gene_symbol)) > 0.3`
- [ ] **Non-empty result:** `nrow(gsea_fam@result) > 0`
- [ ] **@geneSets slot fixed:** `length(gsea_fam@geneSets) == length(unique(T2G$gs_name))`
- [ ] **ID prefix applied:** pathway IDs in master table start with `TE_FAMILY_` or `TE_CLASS_`
- [ ] **Biological plausibility:** LINE/SINE enrichment direction consistent with known TE derepression phenotype if applicable

---

## Common Pitfalls

### Pitfall: Wrong ID space — 0 results

- **Symptom:** `nrow(gsea_fam@result) == 0`; overlap check shows `0` or near-zero.
- **Cause:** Ranked list uses Ensembl gene IDs or gene symbols instead of TE subfamily IDs. The GMT `gene_symbol` column contains subfamily names (e.g. `HAL1`, `L1Md_T`, `B1_Mm`) — these must match the rownames of the ranked list.
- **Fix:** Extract TE rows from the combined DGEList using `is_te == TRUE` and confirm rownames are subfamily IDs. Re-run `build_te_annotation(rownames(mat_te))` if `$gene_symbol` is missing from the annotation.

### Pitfall: Empty @geneSets slot breaks enrichplot

- **Symptom:** `enrichplot::gseaplot2()` errors or produces blank plots.
- **Cause:** `clusterProfiler::GSEA()` does not always populate the `@geneSets` slot from custom TERM2GENE inputs.
- **Fix:** Always add after GSEA: `gsea_result@geneSets <- split(T2G$gene_symbol, T2G$gs_name)`. Use `T2G$gene_symbol` and `T2G$gs_name` — NOT `T2G$gene`/`T2G$term` (those columns do not exist in TE GMTs).

### Pitfall: Class GMT drops all sets with default min_size

- **Symptom:** `nrow(gsea_class@result) == 0` when using the class GMT; no error.
- **Cause:** The class GMT has only ~6 gene sets. With the default `minGSSize = 5`, sets with fewer than 5 member subfamilies are silently excluded.
- **Fix:** Set `minGSSize = 3` for class-level GSEA. Verify which sets survive with `unique(gsea_class@result$ID)`.

### Pitfall: Overlap check passes but results are biologically unexpected

- **Symptom:** GSEA runs, results non-empty, but enrichment is flat or reversed.
- **Cause:** The t-statistic ranking is on the combined gene+TE DGEList, but size factors may have been estimated from genes only. TE DE effect sizes relative to genes may be miscalibrated.
- **Fix:** Confirm size factors used in the combined DGEList came from the gene-only subset (this is the documented behavior of `create_combined_dge`). Compare TE log-fold changes to standalone TE-only edgeR results as a sanity check.

---

## Prerequisites

The TE path requires the project-vendored **TE-RNAseq-toolkit v2.0.3** and an
`analysis_config.yaml`-based analysis layout.

## Resources

- **clusterProfiler:** https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html
- **TE-RNAseq-toolkit v2.0.3:** `01_modules/TE-RNAseq-toolkit/` — `R/create_te_genesets.R`, `R/te_utils.R`
- **Deeper reference (load on demand):** `references/te-gsea.md` — full GMT column contract, `gs_name`/`gene_symbol` vs `term`/`gene` distinction, annotated GSEA code, overlap-check pattern, class-GMT min_size guidance

---

## When not to use

- Do not use for gene-symbol or MSigDB GSEA. Use bulk-rnaseq-gsea instead.

---

## See also

- `annotate-bulk-rnaseq-data` — Prerequisite (TE path); build the TE family/class GMTs and combined DGEList
- `bulk-rnaseq-gsea` — Alternative; gene-symbol or MSigDB GSEA (Hallmark/KEGG/Reactome), shares clusterProfiler machinery
