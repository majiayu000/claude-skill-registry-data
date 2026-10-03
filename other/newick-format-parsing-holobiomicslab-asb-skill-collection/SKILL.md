---
name: newick-format-parsing
description: Use when you have a Chemical Feature Tree artifact (phylogeny) output
  from q2-qemistree's make-hierarchy method and need to verify its structural validity,
  count nodes (leaves and internal nodes), measure tree depth, and assess branching
  patterns before using it for alpha- or beta-diversity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0567
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3172
  tools:
  - q2-qemistree
  - QIIME 2 artifact inspection tools
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41589-020-00677-3
  title: qemistree
evidence_spans:
- A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed
  comparison of untargeted metabolomic profiles.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qemistree
    doi: 10.1038/s41589-020-00677-3
    title: qemistree
  dedup_kept_from: coll_qemistree
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00677-3
  all_source_dois:
  - 10.1038/s41589-020-00677-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# newick-format-parsing

## Summary

Parse and validate Newick-format phylogenetic trees to extract structural properties (node count, tree depth, branching statistics) for chemically-informed metabolomic trees. This skill is essential when inspecting Chemical Feature Tree artifacts produced by q2-qemistree to ensure data integrity before downstream phylogenetic diversity analysis.

## When to use

You have a Chemical Feature Tree artifact (phylogeny) output from q2-qemistree's make-hierarchy method and need to verify its structural validity, count nodes (leaves and internal nodes), measure tree depth, and assess branching patterns before using it for alpha- or beta-diversity calculations or meta-analyses.

## When NOT to use

- Input is already in a validated, parsed tree object (e.g., skytree or dendropy Python object); parsing is redundant.
- Tree file is in a non-Newick format (e.g., Nexus, PhyloXML) without prior conversion.
- Your goal is to perform diversity analysis directly; use QIIME 2 diversity methods on the artifact without intermediate parsing unless structural inspection is required for quality control.

## Inputs

- Phylogeny[Rooted] artifact (qemistree.qza output from make-hierarchy)
- QIIME 2 artifact (.qza file)

## Outputs

- Parsed tree structure (nodes, edges, labels)
- Node count report (leaves, internal nodes, total)
- Tree depth and branching statistics
- Validation report (connectivity, malformation checks)

## How to apply

Load the Chemical Feature Tree artifact using QIIME 2 artifact inspection tools and validate the file format as Newick or QIIME 2 serialized object. Parse the tree structure to count total nodes (both leaf and internal), verify tree connectivity to ensure absence of malformed or orphaned branches, and compute structural metrics including tree depth and branching statistics. Report node labels and topology to confirm chemical feature hierarchy was correctly built from molecular substructure fingerprints (2936 or filtered to 489 PubChem positions). Cross-check that feature count in the tree matches the feature table after filtering out MS1 features without predicted fingerprints (typically 70–90% coverage).

## Related tools

- **q2-qemistree** (Generates the Chemical Feature Tree (Phylogeny[Rooted] artifact) from molecular substructure predictions via CSI:FingerID and MS2 spectral matches; tree is input to this parsing skill.) — https://github.com/biocore/q2-qemistree
- **QIIME 2 artifact inspection tools** (Load and extract serialized tree objects from .qza artifacts for parsing and validation.)

## Evaluation signals

- Total node count (leaves + internal nodes) is consistent and non-zero; node count ≤ 2× feature count in the input feature table (after filtering features without fingerprints).
- Tree is connected: all internal nodes have exactly 2 or more children, root node exists, no orphaned branches.
- All leaf nodes correspond to MS1 features in the input feature table; all feature identifiers in feature-data.qza are represented in the tree.
- Tree depth and branching statistics are reasonable (depth typically 5–30 for metabolomic datasets; branching factor indicates hierarchy built on 2936 or 489 molecular properties).
- No malformed branch structures (e.g., nodes with zero children, circular references, duplicate identifiers).

## Limitations

- Newick format does not store bootstrap values or edge weights by default; chemical distance metrics from fingerprint similarity are implicit in tree topology, not explicit in the format.
- SIRIUS predicts molecular substructures for only 70–90% of MS1 features; features without fingerprints are excluded from the tree, so tree node count < input feature table row count.
- Tree structure depends on quality of MS2 spectra and user-defined tolerances (ppm-max, zodiac-threshold); poor MS2 quality or overly stringent thresholds reduce the number of features with predictions and thus tree density.
- Newick parsing assumes well-formed input; validation must check for malformed syntax before proceeding.

## Evidence

- [other] Validate file format as either Newick or QIIME 2 serialized object.: "Validate file format as either Newick or QIIME 2 serialized object."
- [other] Parse tree structure and count total nodes (leaves + internal nodes).: "Parse tree structure and count total nodes (leaves + internal nodes)."
- [other] Verify tree connectivity and absence of malformed branches.: "Verify tree connectivity and absence of malformed branches."
- [readme] MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features): "MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1"
- [readme] A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`.: "A tree relating the MS1 features in these data based on molecular substructures predicted for MS1 features. This is of type `Phylogeny[Rooted]`."
