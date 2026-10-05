---
name: annotate-bulk-rnaseq-data
description: "Router for annotating bulk RNA-seq featureCounts matrices before edgeR/limma DE — gene symbols via bulkiRNA annotate_genes(), and transposable-element IDs parsed into Subfamily:Family:Class. R-based; annotate before filtering. For upstream STAR/featureCounts TE prep use star-te-preprocessing; for single-cell matrices use single-cell-rna-qc."
license: MIT
---

# Annotate RNAseq Data (Genes + TEs)

## Overview

This skill annotates already-counted bulk RNA-seq matrices (featureCounts outputs) and assembles edgeR `DGEList` objects for downstream limma/edgeR DE. It is one logical step **between counting and DE**, and it splits into two paths:

- **Gene-symbol annotation (the usual case)** — every preprocessed dataset needs this: map Ensembl IDs to gene symbols via Ensembl/biomaRt and build the gene `DGEList`.
- **Transposable-element annotation (the rare case)** — parse TE IDs into `Subfamily:Family:Class`, build the TE `DGEList`, and optionally row-bind genes + TEs into a unified annotated matrix.

A gene-only agent reads this router plus `references/gene-annotation.md` and stops there; it never has to read TE-specific material.

**When to use this skill:**
- Annotate Ensembl IDs with gene symbols before filtering (gene path)
- Process transposable-element count matrices into family/subfamily annotations (TE path)
- Build gene and/or TE `DGEList` objects for downstream DE
- Combine gene + TE counts into a unified annotated matrix

**When NOT to use this skill:**
- Single-cell scRNA-seq count matrices → use `single-cell-rna-qc`
- Generating the count matrices themselves (STAR alignment, SAF building, featureCounts) → use `star-te-preprocessing`

---

## Decision Tree / Routing

```
Annotating a bulk RNA-seq count matrix?
│
├─ Annotating regular gene symbols (the usual case)?
│     →  references/gene-annotation.md
│        Ensembl→Symbol via biomaRt/org.db, gene DGEList assembly.
│
├─ Annotating transposable elements?
│     →  references/te-annotation.md
│        Parse TE IDs (Subfamily:Family:Class), TE annotation, TE DGEList.
│
└─ Both, for a combined gene+TE matrix?
      →  read BOTH references/gene-annotation.md and references/te-annotation.md
         (gene + TE blocks are row-bound into one annotated matrix).
```

---

## Shared Principle

**Always annotate BEFORE filtering.** Never drop low-count rows first — filtering before annotation loses Ensembl/TE IDs irreversibly, and the mapping back to symbols/families cannot be recovered. This rule holds on both paths.

## Joint gene+TE matrix — analysis caveats (read before combined-mode DE)

A row-bound gene+TE matrix is valid only because exonic TE loci were subtracted upstream (no double-counting) — but mutual exclusivity is **necessary, not sufficient**. When you take a combined matrix into joint normalization/DE, the rules below are load-bearing — but they are **graded options, not mandates** (grade scale + key claims + gaps live in `te-gene-featurecounts/SKILL.md` "Evidence & open questions", authoritative source: the evidence-graded reconciliation, note 13). The *joint matrix itself* is a reviewed construct (**grade A**).

- **Size factors from genes ONLY — grade B / CONTESTED.** Estimate DESeq2 size factors on the gene submatrix (`estimateSizeFactors(dds, controlGenes = which(feature_type == "gene"))`). TE-Seq advocates this (the long-tailed, multimapper-inflated (`-M`) TE minority can violate the "most features unchanged" assumption and drag *gene* fold-changes); but the dominant tool **TEtranscripts pools** genes+TEs. Reasonable, not universal — sanity-check against pooled size factors and confirm gene LFCs are stable.
- **Within-feature-type, across-sample DE ONLY — grade C / inference.** The combined object is valid for gene-vs-sample and TE-vs-sample comparison; the per-sample basis offset and multimapper bias cancel across samples within a feature type. Sound mechanistic inference, not stated in a TE primary source.
- **NEVER compare gene-vs-TE magnitude within a sample — grade C / inference.** Genes (unique-only, possibly Salmon/EM/length-modeled) and TEs (`-M` integer, no length model, possibly `-s 0` both-strand) sit on different measurement bases. "This TE is expressed like that gene" and "TE % of transcriptome" are not interpretable as biology.
- **No TPM/FPKM for TE meta-features — grade C / inference.** A summed multi-locus subfamily has no single length, so length-normalized units are undefined. Use model-normalized counts / logCPM / DESeq2 LFCs only.

If TE rows were counted stranded with a sense/antisense split upstream (`--te-strand sense_antisense`), keep sense and antisense as **separate** TE features — the more principled best-practice (**grade B / SQuIRE-specific**) for preserving bidirectional TE biology on a stranded library without breaking gene-comparability. The field is split (TEtranscripts defaults `--stranded no`); `-s 0` standalone matrices remain a valid choice, and mode-switching is not required.

---

## Prerequisites

- **Gene path detail:** `references/gene-annotation.md`
- **TE path detail:** `references/te-annotation.md`
- **Gene helpers:** the installed `bulkiRNA` package — `library(bulkiRNA)`; skill `bulkirna` holds the recipe
- **TE helpers:** TE-RNAseq-toolkit **v2.0.3** — `R/te_utils.R`, `R/validate_te_input.R`, `R/create_combined_dge.R`, `R/create_te_genesets.R`

---

## When not to use

- Do not filter low-count rows before annotation — you lose Ensembl IDs irreversibly.
- Do not use for single-cell scRNA-seq. Use single-cell-rna-qc and scanpy/Seurat workflows instead.

---

## See also

The canonical handoff chain is `star-te-preprocessing → annotate-bulk-rnaseq-data → bulk-rnaseq-gsea` (gene path) or `→ te-geneset-gsea` (TE path).

- `star-te-preprocessing` — Prerequisite; produces the integer TE + gene count matrices this skill annotates
- `single-cell-rna-qc` — Alternative for single-cell scRNA-seq QC and annotation (different modality)
- `bulk-rnaseq-gsea` — Next step; downstream DE → GSEA on the annotated DGEList
- `te-geneset-gsea` — Next step (TE path); GSEA on TE family/class gene-sets produced here
