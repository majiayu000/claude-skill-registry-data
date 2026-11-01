---
name: metabolite-set-analysis
description: Use when you have a metabolite intensity matrix (rows=metabolites or peaks, columns=samples) paired with metabolite-to-pathway or metabolite-to-feature-group annotations, and you want to score activity levels across pathways or metabolite groupings in a way that tolerates missing peaks and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals
schema_version: 0.2.0
---

# Metabolite-Set Analysis via PLAGE Decomposition

## Summary

Decompose metabolite intensity data across predefined metabolite sets (pathways, molecular families, or mass2motifs) using singular value decomposition (SVD) to extract pathway activity level scores that rank biological processes by their magnitude and statistical significance. This approach is more robust to noise and missing peaks than enrichment-based alternatives (ORA, GSEA), making it suitable for metabolomics data with sparse or noisy measurements.

## When to use

Apply this skill when you have a metabolite intensity matrix (rows=metabolites or peaks, columns=samples) paired with metabolite-to-pathway or metabolite-to-feature-group annotations, and you want to score activity levels across pathways or metabolite groupings in a way that tolerates missing peaks and measurement noise. Use PLAGE decomposition when you prioritize robustness to incomplete data and need ranked pathway results for downstream interpretation or biomarker discovery.

## When NOT to use

- Your metabolite data are already summarized at the pathway level (e.g., input is already a pathway-level feature table or activity matrix). PLAGE decomposes individual metabolite intensity data; if aggregation has already occurred, re-decomposition will not recover lost information.
- You require transcript-level or gene-level results from genomics data without prior conversion to metabolite annotations. PLAGE in PALS is optimized for metabolomics; equivalent decomposition for transcriptomics uses gene sets, not metabolite sets.
- You have very few metabolites per pathway (< 3 members). SVD requires sufficient samples to extract a meaningful principal component; pathways with few metabolites may yield unstable or uninformative scores.

## Inputs

- Metabolite intensity matrix (CSV or pandas DataFrame): rows=peak/metabolite features with identifiers, columns=individual samples or replicates
- Metabolite annotations table (CSV or DataFrame): two-column format mapping peak IDs to metabolite database IDs (KEGG compound IDs, ChEBI IDs, etc.)
- Pathway or metabolite-set definitions (database or list): groupings of metabolites or compounds assigned to pathways, molecular families, or mass2motifs
- Experimental design specification: sample groupings and case-vs-control comparisons

## Outputs

- Pathway activity ranking table (CSV or DataFrame): columns include pathway identifier, activity score, p-value, and coverage metrics (e.g., fraction of pathway metabolites detected in dataset)
- Ranked pathway results sorted by activity magnitude or statistical significance
- Per-pathway first principal component (activity score vector) for downstream interpretation

## How to apply

Load the intensity matrix and pathway/metabolite-set database, then for each pathway or metabolite set, subset the intensity data to only those metabolites assigned to that set. Apply singular value decomposition (SVD) to each subset and extract the first principal component (largest singular vector) as the pathway activity score. Log-transform intensities to base 2 and standardize (zero mean, unit variance) before SVD. Rank pathways by the magnitude of their activity scores and compute statistical significance metrics (p-values) for each ranked result. The first principal component captures the dominant mode of co-variation within each metabolite set, making it robust to individual missing values or measurement noise in single metabolites.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Complete implementation of metabolite-set decomposition and ranking; performs database queries, PLAGE decomposition, and result presentation) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web-based interface for running PALS and inspecting ranked pathway results; enables visualization of activity levels and comparison across samples) — https://pals.glasgowcompbio.org/app/
- **ORA (Over-Representation Analysis)** (Alternative pathway ranking method included in PALS for comparison; does not use decomposition and is more sensitive to noise and missing peaks)
- **GSEA (Gene Set Enrichment Analysis)** (Alternative pathway ranking method included in PALS for comparison; does not use decomposition and is more sensitive to noise and missing peaks)
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of molecular family definitions that can be analyzed as metabolite sets in PALS) — http://gnps.ucsd.edu/
- **MS2LDA** (Source of mass2motif definitions that can be analyzed as metabolite sets in PALS) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Output pathway ranking table has consistent column structure with pathway identifiers, numeric activity scores, p-values, and coverage metrics (e.g., tot_ds_F, unq_pw_F, F_coverage). Verify no missing or NaN values in ranked results.
- Principal components extracted from pathway subsets are orthogonal to those of other pathways (SVD decomposition property); confirm by checking that pathway scores are uncorrelated.
- Pathways with higher coverage (more of the pathway's metabolites detected in the dataset) produce more statistically significant results; check that p-value trends inversely with coverage for high-activity pathways.
- Intensity preprocessing produces standardized data (mean ~0, variance ~1) before SVD; verify by computing summary statistics on log-transformed, standardized matrix.
- Robustness check: replicate analysis with random subsampling of metabolites or samples; PLAGE scores should remain relatively stable, with rank correlation of pathway results > 0.8 compared to full dataset.

## Limitations

- SVD-based principal component extraction assumes that the dominant mode of co-variation within a metabolite set is biologically meaningful; in pathways with heterogeneous metabolite roles or regulation, the first principal component may not reflect true pathway activity.
- Missing data imputation (replacement of zero/missing intensities with minimum or mean values) can introduce bias if missingness is non-random; the method is more robust than ORA/GSEA to missing peaks, but does not recover truly undetected metabolites.
- Pathway definitions are static (loaded from KEGG, Reactome, or user-supplied lists); changes in pathway membership or addition of newly discovered metabolite associations are not automatically incorporated.
- The method is sensitive to the choice of intensity preprocessing parameters (e.g., min_replace threshold for data imputation). Different imputation cutoffs or log-transformation bases can alter pathway rankings.
- Statistical significance (p-values) requires definition of experimental comparisons (case vs. control groups); results are specific to the stated comparisons and cannot be directly applied to other study designs without recomputation.

## Evidence

- [other] For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway. Extract the first principal component (singular vector) from each pathway's SVD as the pathway activity score.: "For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway. 3. Extract the"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks"
- [readme] The decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways.: "the [decomposition approach] in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] Data is transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance"
- [readme] If all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value; if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values"
