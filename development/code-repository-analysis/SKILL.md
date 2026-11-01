---
name: code-repository-analysis
description: Use when you have a published research article describing a new FT-ICR MS analysis tool and need to verify which analytical and visualization features are actually implemented (not just claimed).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDirect
  - UltraMassExplorer
  - FREDA
  - MetaboAnalyst
  - DropMS
  - i-van Krevelen
  - vegan
  - SYNCSA
  - pmartR
  - KEGGREST
  - py4cytoscape
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- web-based applications such as UltraMassExplorer (UME)
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28]
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst [29]
- web-based applications such as UltraMassExplorer (UME) [27], FREDA [28], MetaboAnalyst [29], and DropMS [30]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
---

# code-repository-analysis

## Summary

Systematically extract and cross-reference implementation details from a software repository's source code, dependency declarations, and documentation to construct a comprehensive feature inventory and comparative analysis table. This skill is essential when assessing the analytical capabilities of a bioinformatics pipeline against peer tools.

## When to use

You have a published research article describing a new FT-ICR MS analysis tool and need to verify which analytical and visualization features are actually implemented (not just claimed). You want to construct a side-by-side comparison table of feature support across multiple competing tools. The article claims novel capabilities (e.g., 'uniquely able to automatically generate biochemical transformation networks') and you need to confirm these claims by tracing code and dependency references.

## When NOT to use

- The software is closed-source or source code is not publicly available — code inspection is not possible.
- You only need to report the author's claimed capabilities without independent verification — skip this skill and rely on the paper's methods section alone.
- The comparison tools' documentation is proprietary or unavailable — you cannot construct a complete peer comparison matrix.

## Inputs

- GitHub repository URL
- Published article describing the pipeline
- README and setup.py/requirements.txt from source repository
- ReadTheDocs documentation or supplementary methods tables
- Published documentation or repositories of peer comparison tools

## Outputs

- Structured feature comparison table (tools × analytical/visualization features)
- Binary feature matrix (✔/✖ entries)
- Enumerated list of implemented normalization methods
- Enumerated list of supported statistical tests and indices
- Dependency inventory mapped to specific analytical capabilities

## How to apply

Clone the source repository and inspect the main pipeline code structure, function signatures, and command-line argument definitions to enumerate implemented features. Cross-reference the declared dependencies (in README or setup.py) against the article's methods section: for example, the presence of R packages 'vegan', 'SYNCSA', 'pmartR', and 'KEGGREST' confirms implementation of multivariate statistics (PERMANOVA, NMDS, PCA) and KEGG pathway mapping. Parse the ReadTheDocs documentation and supplementary tables to extract the complete list of supported parameters (normalization methods, filtering thresholds, indices). For each comparison tool, consult published documentation or repository READMEs to systematically record feature support (✔/✖) across a uniform set of dimensions: m/z filtering, isotopic filtering, formula error filtering (0.5 ppm threshold), compound class assignment, peak normalization methods (max, minmax, mean, median, total sum, z-score), Van Krevelen diagrams, thermodynamic indices (NOSC, GFE, AImod, DBE), statistical tests (PERMANOVA, NMDS, PCA), chemodiversity metrics (Shannon, Gini-Simpson, Chao1, Rao's), and transformation network generation. Construct a binary comparison matrix with rows as tools and columns as features. Validate the matrix by spot-checking feature claims against source code presence of corresponding functions or dependency imports.

## Related tools

- **MetaboDirect** (The subject pipeline whose code repository is inspected to extract implemented features and dependencies) — https://github.com/Coayala/MetaboDirect
- **vegan** (R package providing multivariate statistical methods (PERMANOVA, NMDS) — presence in dependencies confirms these features are implemented)
- **SYNCSA** (R package providing multivariate community ecology statistics — confirmed by dependency declaration)
- **pmartR** (R package used for normalization testing and validation — confirms normalization feature implementation)
- **KEGGREST** (R package enabling KEGG database queries for pathway and transformation network mapping)
- **py4cytoscape** (Python package enabling Cytoscape integration for transformation network visualization)
- **UltraMassExplorer** (Web-based comparison tool for FT-ICR MS analysis — feature support assessed via published documentation)
- **FREDA** (Web-based comparison tool for FT-ICR MS analysis — feature support assessed via published documentation)
- **MetaboAnalyst** (Web-based comparison tool for metabolomics analysis — feature support assessed via published documentation)
- **DropMS** (Web-based comparison tool for FT-ICR MS analysis — feature support assessed via published documentation)
- **i-van Krevelen** (Visualization tool for Van Krevelen diagrams — feature support assessed via published documentation)

## Examples

```
git clone https://github.com/Coayala/MetaboDirect.git && cd MetaboDirect && grep -E '(vegan|SYNCSA|pmartR|KEGGREST|py4cytoscape)' setup.py README.md && python -c "import metabodirect; help(metabodirect)" | grep -E '(PERMANOVA|NMDS|PCA|transformation|chemodiversity)'"
```

## Evaluation signals

- Dependency declarations (setup.py, requirements.txt, README) explicitly list packages corresponding to each claimed analytical feature (e.g., 'vegan' for PERMANOVA/NMDS, 'KEGGREST' for transformation networks).
- Source code inspection reveals function definitions or class methods implementing each claimed analysis (e.g., find Python/R code calling vegan::adonis for PERMANOVA).
- The comparison table is complete and internally consistent: no blank cells without documented justification; feature definitions are uniform across rows.
- Cross-referencing confirms absence claims: the article states 'MetaboDirect does not provide raw spectra data preprocessing' — verify this is not contradicted by presence of a preprocessing module or dependency like xcms or CoreMS.
- The binary matrix aligns with the article's main findings: the finding states MetaboDirect 'performs all analyses offered by other available software...except raw spectra processing and molecular formula assignment' — verify this pattern is reflected in the comparison table.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing, so feature comparison is limited to downstream analysis; peer tools offering raw spectra processing cannot be directly equated on that dimension.
- Feature support in peer tools is assessed via public documentation; if documentation is outdated or incomplete, feature support may be misattributed.
- The comparison is snapshot-based: repository code and peer tool versions change over time, so the feature table requires periodic refresh.
- Web-based GUI tools like UltraMassExplorer and FREDA may not fully expose all underlying capabilities in their user interface, making feature inventory from documentation potentially incomplete.
- Discussion section limitations or known issues not explicitly mentioned in the article text cannot be evaluated against the code.

## Evidence

- [readme] Dependency inventory from README: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above) with the following libraries/modules: [Python: argparse, numpy, pandas, seaborn, more-itertools,"
- [methods] Feature comparison workflow and scope: "For each of the five comparison tools (UltraMassExplorer, FREDA, MetaboAnalyst, DropMS, i-van Krevelen), consult their published documentation or repository READMEs to determine feature support for:"
- [abstract] Novel feature claim requiring verification: "MetaboDirect is also uniquely able to automatically generate biochemical transformation networks (ab initio) based on mass differences (mass difference network‑based approach)"
- [abstract] Analytical features implemented: "develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics), visualization"
- [methods] Scope limitation confirming absence of raw spectra processing: "MetaboDirect does not provide raw spectra data preprocessing"
- [methods] Feature inventory from source code inspection approach: "Cross-reference MetaboDirect source code for the vegan, SYNCSA, pmartR, KEGGREST, and py4cytoscape dependencies to confirm implementation of each feature"
