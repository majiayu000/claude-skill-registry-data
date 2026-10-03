---
name: evidence-linking
description: Use when when evaluating a scientific manuscript that describes a computational analysis (e.g., a normalization or transformation pipeline), use this skill to trace each claimed finding to its source code, data, or prior publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3361
  tools:
  - GitHub
  - sctransform
  - Seurat
  - GitHub issue tracker
  - WGCNA
derived_from:
- doi: 10.1186/s13059-019-1874-1
  title: sctransform
- doi: 10.1186/1471-2105-9-559
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_sctransform
    doi: 10.1186/s13059-019-1874-1
    title: sctransform
  - build: coll_wgcna
    doi: 10.1186/1471-2105-9-559
    title: wgcna
  dedup_kept_from: coll_sctransform
schema_version: 0.2.0
---

# evidence_linking

## Summary

Link scientific claims and computational outputs back to source materials (code repositories, data artifacts, publications) to establish reproducibility context and identify missing information. This skill surfaces the concrete evidence chain—which tools were used, which parameters were applied, which results are traceable—essential for assessing whether a computational finding can be independently verified.

## When to use

When evaluating a scientific manuscript that describes a computational analysis (e.g., a normalization or transformation pipeline), use this skill to trace each claimed finding to its source code, data, or prior publication. Trigger conditions: (1) the article describes outputs of an algorithmic procedure (e.g., normalized data, transformed matrices, differential results); (2) the authors cite code repositories or reference an earlier method paper; (3) you need to determine whether the analysis is reproducible or identify gaps (missing code, no changelog, undocumented parameter choices).

## When NOT to use

- The article is purely theoretical (no code repositories or computational artifacts mentioned).
- The task is to evaluate statistical significance or experimental design validity—use domain-specific critical appraisal instead.
- Input is a repository README with no accompanying article claims to link—the skill requires bidirectional tracing from claims to code.

## Inputs

- Article text or abstract describing a computational method or analysis
- Tool/repository citations (GitHub URLs, R package names, DOIs)
- Repository README or documentation
- Supplementary materials, vignettes, or issue trackers

## Outputs

- Indexed map of tools and repositories used
- Trace of claims to source code and documentation
- List of missing signals (e.g., no changelog, undocumented parameters)
- Reproducibility assessment (e.g., 'strong evidence linking', 'gaps identified')

## How to apply

Begin by indexing all cited tools and repositories mentioned in the article text (e.g., GitHub URLs, R package names, method citations). For each major claim or result, traverse from the claim backward to: (1) the source code repository where the algorithm is implemented; (2) the README, documentation, or vignettes that describe usage and parameters; (3) linked or cited publications that establish the theoretical basis; (4) any supplementary materials or issue trackers that record known limitations or recent changes. Document what is present (e.g., installation instructions, example invocations, published validation) and what is absent (e.g., no changelog, missing parameter documentation, unlinked intermediate files). Record the section of the article and the specific evidence span that anchors each connection. Use this map to assess reproducibility: strong evidence linking means claims are traceable to versioned code and documented examples; weak or broken links (missing repos, no vignettes, no changelog) indicate reproducibility risks.

## Related tools

- **sctransform** (Source repository containing the implementation of normalization and variance stabilization methods; indexed to trace article claims about VST regularization flavor and output formats) — https://github.com/satijalab/sctransform
- **Seurat** (Downstream R package integrating sctransform functionality; linked to demonstrate how the method is deployed in a QC and analysis workflow) — https://satijalab.org/seurat/
- **GitHub issue tracker** (Used to record and resolve reproducibility concerns (e.g., undocumented parameters, missing materials)) — https://github.com/satijalab/sctransform/issues

## Examples

```
# Install sctransform and index its documentation
install.packages('sctransform')
?sctransform::vst
# Trace article claim: 'normalized_data <- sctransform::vst(umi_count_matrix)$y' to source repo and vignettes
```

## Evaluation signals

- All major algorithmic claims in the article are traceable to a specific function, parameter, or vignette in the indexed repository.
- Installation and example invocation instructions from the README or documentation can be executed without ambiguity (e.g., `install.packages('sctransform')` and `sctransform::vst(umi_count_matrix)` are both present).
- Version-specific behavior (e.g., 'v1 regularization' vs. v2) is documented and linked to changelog entries or published revisions (e.g., Choudhary & Satija 2022).
- Missing signals are explicitly recorded (e.g., 'No changelog found', 'no parameter documentation for vst.flavor').
- Each indexed repository has a publicly accessible README or documentation page that explains its role in the analysis pipeline.

## Limitations

- The skill depends on the completeness of article citations; if repositories or prior publications are not mentioned, they cannot be indexed.
- Repository READMEs may be outdated or incomplete; absence of documentation does not prove the code is invalid, only that reproducibility cannot be independently verified from available signals.
- Some parameters or design choices may be implicit in code rather than documented; the skill surfaces gaps but does not resolve them without expert review.
- The MVP described in the source material does not execute workflows automatically; evidence linking is a manual indexing and mapping task.

## Evidence

- [other] Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information.: "Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information."
- [readme] The sctransform package was developed by Christoph Hafemeister in Rahul Satija's lab at the New York Genome Center and described in Hafemeister and Satija, Genome Biology 2019.: "The sctransform package was developed by Christoph Hafemeister in Rahul Satija's lab at the New York Genome Center and described in Hafemeister and Satija, Genome Biology 2019."
- [readme] Core functionality of this package has been integrated into Seurat, an R package designed for QC, analysis, and exploration of single cell RNA-seq data.: "Core functionality of this package has been integrated into Seurat, an R package designed for QC, analysis, and exploration of single cell RNA-seq data."
- [readme] For usage examples see vignettes in inst/doc or use the built-in help after installation `?sctransform::vst`: "For usage examples see vignettes in inst/doc or use the built-in help after installation"
