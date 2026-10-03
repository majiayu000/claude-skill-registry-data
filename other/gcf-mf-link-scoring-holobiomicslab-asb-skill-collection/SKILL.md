---
name: gcf-mf-link-scoring
description: Use when after BGC detection and clustering (producing GCFs) and metabolomics profiling (producing MFs with MS/MS spectra), when you have paired genomic and metabolomic data from the same microbial strains and need to rank which GCF–MF pairs are likely to represent true biosynthetic relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3365
  tools:
  - antiSMASH
  - BiG-SCAPE
  - GNPS
  - MIBiG
  - NPLinker
derived_from:
- doi: 10.1371/journal.pcbi.1008920
  title: NPLinker
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1371/journal.pcbi.1008920
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
---

# GCF-MF Link Scoring

## Summary

Rank potential links between genomic clusters of biosynthetic gene clusters (GCFs) and metabolomic features (MFs) using standardised strain correlation and Input-Output Kernel Regression (IOKR) scores. This skill enables prioritisation of true natural product–BGC associations from large numbers of hypothetical pairings by combining complementary scoring functions.

## When to use

After BGC detection and clustering (producing GCFs) and metabolomics profiling (producing MFs with MS/MS spectra), when you have paired genomic and metabolomic data from the same microbial strains and need to rank which GCF–MF pairs are likely to represent true biosynthetic relationships rather than co-occurrence by chance. Particularly useful when working with large datasets where manual validation is infeasible and you need a data-driven ranking to focus downstream investigation.

## When NOT to use

- When you lack paired genomic and metabolomic data from the same microbial strains; the strain correlation score depends entirely on strain co-occurrence.
- When BGCs lack considerable homology to MIBiG entries; IOKR is restricted to BGCs with structural homology to the training database and cannot predict fingerprints de novo.
- When the input spectra are predominantly from non-microbial sources or from organisms without associated genomic data, as the training set for IOKR includes metabolites from sources other than microbes, limiting specificity.

## Inputs

- Raw strain correlation scores for all GCF–MF pairs with GCF sizes (#G), MF sizes (#m), overlap sizes (#(G∩M)), and population size (#N)
- MS/MS spectra in machine-readable format (e.g., from GNPS)
- BGC sequences or GCF cluster assignments from BiG-SCAPE
- Molecular fingerprint training data and kernel function parameters (for IOKR)
- Candidate structure set with MIBiG homology assignments (for IOKR scoring)

## Outputs

- Standardised strain correlation scores (numeric, typically centred near 0 for all links, elevated for validated links)
- IOKR scores (numeric, 0–1 range, higher for true matches)
- Combined ranking scores (ℓp-norm combination of standardised strain and IOKR)
- Ranked list of GCF–MF pairs sorted by combined score
- Score distributions and enrichment statistics (means, p-values, percentile cutoffs)

## How to apply

Apply two complementary scoring schemes in sequence. First, compute the standardised strain correlation score by calculating the hypergeometric expectation and variance of raw overlap counts across GCF and MF populations, then standardise as s*_corr = (σ_corr(M,G) − E[σ_corr(M,G)]) / √Var[σ_corr(M,G)]; this correction enables fair comparison across links with different GCF and MF sizes. Second, compute an IOKR score that ranks spectra against candidate BGC structures using a molecular fingerprint kernel, filtering spectra to include only peaks in the training data and applying denoising to reduce computational cost. Combine both standardised scores using an ℓp-norm with sign adjustment: s'1/2 = sgn(s'_corr)|s'_corr|^1/2 + sgn(s'_IOKR)|s'_IOKR|^1/2. The combination leverages complementary signals: strain correlation captures co-occurrence patterns while IOKR captures chemical-structural likelihood, improving separation of validated links (mean ~3.67 for standardised strain score) from all hypothetical links (mean ~−0.006).

## Related tools

- **antiSMASH** (BGC detection and prediction in microbial genomes; input to GCF clustering)
- **BiG-SCAPE** (Clustering predicted BGCs into GCFs; output provides groupings for strain correlation and structural scoring)
- **GNPS** (Source of metabolomic MS/MS spectra and spectral library; provides MF identities and spectra for IOKR scoring)
- **MIBiG** (Reference database of experimentally validated BGC structures; used to assign structure candidates and train IOKR molecular fingerprint kernel)
- **NPLinker** (Integrated framework implementing both standardised strain correlation and IOKR scoring and combination) — https://github.com/sdrogers/nplinker

## Evaluation signals

- Standardised strain correlation scores for all links should centre near 0 (mean −0.0060 observed); validated links should show significantly elevated mean (e.g. 3.6717, p < 1e−60), indicating successful standardisation and separation.
- IOKR scores for validated links should be significantly enriched relative to all links (p < 1e−8 observed in the article), with top-n accuracy metrics (top-1, top-5, top-10, top-20) substantially exceeding random baseline (0.1208 vs 0 at top-1).
- Combined scoring function should show additive or synergistic improvement: validated links should rank higher when both scores are combined compared to either score alone, with enrichment p-value at 90th percentile < 0.05.
- Score distributions should show clear bimodal or right-skewed pattern for all links and left-skewed/elevated pattern for validated links (visualised via histograms and boxplots).
- Manual spot-checking of high-scoring links (e.g. top 5–10) should reveal MS/MS fragmentation patterns consistent with predicted molecular structures from MIBiG homology.

## Limitations

- Strain correlation score is only applicable when input genomes and metabolomics are paired from identical or very closely related microbial strains; it cannot detect links across unrelated organisms or environmental samples.
- IOKR is restricted to BGCs showing considerable homology with MIBiG entries; it cannot predict fingerprints for novel or highly divergent BGCs, limiting applicability to discovery-driven metabologenomics.
- IOKR performance is highly dependent on the choice of kernel function (e.g. Probability Product Kernel) and molecular fingerprint representation; suboptimal kernel design can severely reduce ranking accuracy.
- Test set sizes in published validations are insufficient to break down performance by product class (e.g. PKS vs NRPS vs RiPP), so compound class-specific predictive power remains uncharacterised.
- The combined scoring function requires both strain correlation (paired metadata) and IOKR (MIBiG homology); datasets lacking either component cannot benefit from the full complementarity of the approach.

## Evidence

- [results] standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64): "standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively"
- [results] standardisation successfully enables comparison across links with different GCF and MF sizes: "demonstrating that standardisation successfully enables comparison across links with different GCF and MF sizes"
- [abstract] GCF and spectrum pairs are then scored based upon their shared strains: "GCF and spectrum pairs are then scored based upon their shared strains"
- [abstract] they are in fact complementary, and show a way to combine them to improve their performance: "we demonstrate that they are in fact complementary, and show a way to combine them to improve their performance"
- [results] compute expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] using hypergeometric distribution over all possible overlap sizes: "For each GCF-MF pair, compute expected value E[σ_corr(M,G)] and variance Var[σ_corr(M,G)] using hypergeometric distribution over all possible overlap sizes k"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints"
- [discussion] restricts its use to those BGCs which show considerable homology with MIBiG entries: "restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden"
- [discussion] due to insufficient test set size, breaking down performance by product type to verify this is currently difficult: "While it is not theoretically dependent on product type, due to insufficient test set size, breaking down performance by product type to verify this is currently difficult"
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data"
