---
name: bgc-mf-link-scoring
description: Use when you have preprocessed GCF-MF link pairs from paired genomics–metabolomics
  datasets (antiSMASH-detected BGCs clustered into GCFs, and GNPS spectra grouped
  into MFs) and need to rank them by likelihood of representing true natural product–biosynthetic
  gene associations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0204
  - http://edamontology.org/topic_3373
  tools:
  - NPLinker
  - antiSMASH
  - BiG-SCAPE
  - MIBiG
  - GNPS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set, maintaining
  the hierarchical relationship between them
- Finally, we present NPLinker, a software framework to link genomic and metabolomic
  data
- After downloading the strain assemblies and metabolomics data, the genomes were
  run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE clusters the BGCs separately by product type
- antiSMASH to score the correspondence between the MIBiG entries and the detected
  BGCs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# BGC-MF link scoring

## Summary

Compute complementary scoring functions (strain correlation and IOKR) to rank potential links between bacterial gene cluster families (GCFs) and metabolomic features (MFs), enabling prioritization of validated natural product–BGC associations. Combining both scores significantly enriches for true links compared to either score alone.

## When to use

You have preprocessed GCF-MF link pairs from paired genomics–metabolomics datasets (antiSMASH-detected BGCs clustered into GCFs, and GNPS spectra grouped into MFs) and need to rank them by likelihood of representing true natural product–biosynthetic gene associations. Use this skill when you have both genomic and metabolomic data from the same microbial strains and want to overcome limitations of correlation-based scoring alone (inability to compare scores across links with different strain patterns).

## When NOT to use

- Input spectra are not from the same microbial strains as the genomic BGCs; strain correlation will be uninformative.
- BGCs have no detectable MIBiG homology; IOKR scoring will be unavailable or unreliable.
- You only have one scoring method available (e.g., only strain correlation); complementarity is lost and enrichment diminishes.
- Validation ground truth is unavailable and you cannot assess whether the top-scoring links are correct.

## Inputs

- GCF-MF link pairs (edges between gene cluster families and metabolomic features)
- Strain presence/absence vectors (binary matrix: strains × GCFs, strains × MFs)
- BGC–MIBiG homology assignments (for IOKR molecular fingerprint assignment)
- MS/MS spectra (GNPS format; used by IOKR to compute spectral features)
- Validation ground truth (optional; list of experimentally confirmed GCF-MF pairs)

## Outputs

- Standardized strain correlation scores (per-link, mean ≈ 0, SD ≈ 1 within dataset)
- Standardized IOKR scores (per-link, comparable across links)
- Ranked GCF-MF link list (sorted by combined score or dual-score category)
- Percentile-based link categories (dual-score ≥90th, correlation-only ≥90th, IOKR-only ≥90th, both <90th)
- Validation enrichment statistics (proportion validated per category, Fisher exact test p-values)

## How to apply

Apply two independent scoring methods to each GCF-MF pair: (1) Strain correlation—compute Pearson correlation between the binary presence/absence vector of strains in the GCF and the vector for the MF, then standardize by subtracting the per-GCF or per-MF mean and dividing by standard deviation to make scores comparable across links. (2) IOKR (in silico metabolite–spectrum matching)—assign molecular fingerprints to BGCs via MIBiG homology, compute kernel-based spectral–fingerprint similarity, and standardize in the same manner. Independently calculate the 90th percentile threshold for each score within each dataset. Links exceeding the 90th percentile on both standardized scores are significantly enriched for validated links (p < 0.01). Optionally combine the two standardized scores using an ℓ_p norm (e.g., ℓ_1/2: s_sum = sgn(s_corr)|s_corr|^0.5 + sgn(s_IOKR)|s_IOKR|^0.5) to create a single ranking when dual-score filtering alone is insufficient.

## Related tools

- **NPLinker** (Framework integrating genomic and metabolomic data; implements strain correlation and IOKR scoring, link ranking, and validation enrichment analysis.) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects BGCs from microbial genomes; output used as genomic input to NPLinker.)
- **BiG-SCAPE** (Clusters BGCs into GCFs (gene cluster families) for coarse-grained linking to metabolomic features.)
- **GNPS** (Public metabolomics database; provides MS/MS spectra and spectral libraries for IOKR kernel training and scoring.)
- **MIBiG** (Reference database of characterized BGCs; IOKR relies on MIBiG homology to assign molecular fingerprints to query BGCs.)

## Evaluation signals

- Standardized scores have mean ≈ 0 and SD ≈ 1 within each dataset (check histogram of residuals).
- Raw strain correlation scores are non-informative (mean ≈ 83.5 for all links, ≈ 14.7 for validated), but standardized scores show strong separation (mean ≈ 3.67 for validated vs. ≈ −0.006 for all; p < 10^−60).
- Links in the dual-score (≥90th percentile on both metrics) category show significantly higher proportion of validated links than single-score categories (Fisher exact test p < 0.05).
- IOKR top-1 and top-5 accuracy exceed random baseline (12.08% vs. 0% and 17.08% vs. 0.14%, respectively).
- Combining both scores recovers true links at better ranks than either score alone in ≥50% of validated link cases.

## Limitations

- Raw strain correlation scores cannot reliably be compared across links (same pattern of presence/absence produces identical correlation even for unrelated GCF-MF pairs), motivating standardization but still limiting interpretability.
- IOKR relies on detectable MIBiG homology to assign molecular structures to BGCs; cannot score links for BGCs with no homologous reference, restricting applicability to well-characterized product classes.
- IOKR performance is highly sensitive to kernel function and parameters (especially molecular fingerprint substructure definitions); no principled tuning guidance provided.
- Test set sizes are insufficient to reliably break down IOKR performance by natural product type, limiting ability to detect product-class-specific biases.
- Strain correlation and IOKR are trained on different data distributions (MIBiG includes non-microbial metabolites); combining scores may conflate unrelated scoring artifacts.

## Evidence

- [methods] strain correlation-based approaches, where similarities in sets of strains on one hand, and specific spectra on the other hand, are used to evaluate the links between BGCs and spectra: "strain correlation-based approaches, where similarities in sets of strains on one hand, and specific spectra on the other hand, are used to evaluate the links between BGCs and spectra"
- [methods] we introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class: "we introduce a new feature-based analysis method which, unlike most such methods, does not directly depend on the natural product compound class"
- [results] Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [results] the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208: "the set of links scoring above the 90th percentile on both scores is significantly enriched compared to the set that exceed either of the individual scores (p-value of 2.633 × 10−4 and 0.0208"
- [abstract] using multiple link-scoring functions together makes it easier to prioritise true links relative to others: "using multiple link-scoring functions together makes it easier to prioritise true links relative to others"
- [abstract] the most popular strain correlation score [17] has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF): "the most popular strain correlation score [17] has properties that make it impossible to reliably compare score values across links (even links from the same GCF or MF)"
- [discussion] A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint: "A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures: "IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures"
