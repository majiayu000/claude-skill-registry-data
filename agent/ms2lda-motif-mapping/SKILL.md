---
name: ms2lda-motif-mapping
description: Use when you have a GNPS-generated molecular network (either classical
  or feature-based) and corresponding MS2LDA experiment output containing Mass2Motif-to-spectrum
  assignments, and you want to visualize which substructural motifs are shared across
  clusters or features and how they distribute.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyMolNetEnhancer
  - Python
  - MS2LDA
  - RMolNetEnhancer
  - GNPS
  - Cytoscape
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure
  information
- pyMolNetEnhancer is a python module
- Map MS2LDA substructural information to mass spectral molecular networks
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnetenhancer_cq
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo9070144
  all_source_dois:
  - 10.3390/metabo9070144
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms2lda-motif-mapping

## Summary

Map MS2LDA Mass2Motif substructural information onto GNPS molecular networks (classical or feature-based) to annotate network nodes and edges with discovered mass spectral motifs and shared substructural features. This skill integrates probabilistic substructure discovery with network topology to enable motif-driven chemical class interpretation.

## When to use

You have a GNPS-generated molecular network (either classical or feature-based) and corresponding MS2LDA experiment output containing Mass2Motif-to-spectrum assignments, and you want to visualize which substructural motifs are shared across clusters or features and how they distribute through the network.

## When NOT to use

- MS2LDA experiment has not been run or motif assignments are unavailable; the module requires pre-computed Mass2Motif output.
- GNPS network is not from a known source (madeleineernst tools assume classical or feature-based GNPS workflows); custom network formats may not parse correctly.
- You only have unannotated spectra and no pre-existing MS2LDA or GNPS results; this skill is a post-hoc integration step, not a discovery method.

## Inputs

- GNPS molecular network file (classical network format or feature-based variant)
- MS2LDA job summary table with motif-document assignments and probability/overlap scores
- GNPS job ID (to fetch network metadata if using online retrieval)

## Outputs

- Mass2Motifs_Nodes_*.tsv (node table with motif annotations and TopSharedMotifs per family)
- Mass2Motifs_Edges_*.tsv (edge table with shared motif interaction labels)
- Annotated .graphml file for Cytoscape visualization

## How to apply

Load the GNPS network file (in classical or feature-based format) and the MS2LDA job summary table containing motif probability and overlap scores. Apply pyMolNetEnhancer or RMolNetEnhancer's feature-based or classical mapping function, specifying filtering thresholds: minimum probability score (default 0.01) to exclude low-confidence motif assignments, minimum overlap score (default 0.3) to ensure meaningful motif-spectrum overlap, and top-k parameter (default 5) to limit the most shared motifs reported per molecular family (network component). The module matches nodes by cluster ID (classical) or feature identifier (feature-based) and outputs annotated edge and node tables with motif labels and interaction types, plus a .graphml file for network visualization in Cytoscape. The rationale is that filtering by probability and overlap removes spurious low-signal motifs, while top-k focuses interpretation on the dominant substructural signatures within each network family.

## Related tools

- **pyMolNetEnhancer** (Python module that executes feature-based and classical motif-to-network mapping, filtering by probability/overlap thresholds, and outputs annotated TSV and .graphml files) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing identical motif-to-network mapping functionality for users preferring R workflows) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform that generates the input molecular networks) — https://gnps.ucsd.edu/
- **MS2LDA** (Latent Dirichlet allocation tool that discovers Mass2Motifs from MS/MS spectra; generates the motif assignments and probability/overlap scores consumed by MolNetEnhancer) — http://ms2lda.org/
- **Cytoscape** (Network visualization software used to import the .graphml output and color nodes/edges by motif labels) — https://cytoscape.org/

## Evaluation signals

- Output TSV files are non-empty and contain expected columns (CLUSTERID1, CLUSTERID2, interact for edges; CLUSTER_INDEX, TopSharedMotifs for nodes)
- The .graphml file parses without error in Cytoscape and displays network structure with node and edge attributes
- Motif probability and overlap values in the output respect the applied thresholds (no motif with prob < threshold or overlap < threshold is present unless manually overridden)
- TopSharedMotifs per node lists ≤ k motifs (where k is the 'top' parameter), confirming that limiting logic was applied
- Edge interaction labels match motif identifiers in the MS2LDA output, confirming correct motif-to-node matching

## Limitations

- Server connection timeouts may occur if the MS2LDA summary file is large; manual download from ms2lda.org is recommended as a workaround.
- Probability and overlap thresholds set in the ms2lda.org web app (Experimental Options) are applied during LDA inference; the summary table already contains filtered motif-document relations, so the tool's prob and overlap parameters act as secondary filters on an already-filtered result.
- The tool is specific to GNPS classical and feature-based network formats; custom or non-GNPS network formats are not supported without reformatting.
- No changelog is available, limiting visibility into version history and breaking changes.

## Evidence

- [intro] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [readme] Feature-based mapping matches nodes by feature identifier: "In order to map substructural information to a mass spectral molecular network created through the feature based workflow you need to: [Create a feature based molecular network] through the Global"
- [readme] Filtering parameters control motif inclusion: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] Top-k parameter limits motifs per molecular family: "top: This parameter specifies how many most shared motifs per molecular family (network component index) should be shown. Default is 5."
- [readme] Output formats include TSV and .graphml: "To visualize results import the .graphml output file into Cytoscape... Alternatively the edges and nodes output files can also be loaded separately into Cytoscape. To this end import the"
- [readme] Thresholds are applied post-LDA in web app, then again in the tool: "The probability and overlap thresholds can be set within the ms2lda.org app as well under the Experimental Options tab... Importantly, the summary table contains filtered motif-document relations"
- [readme] Server timeout risk on large files: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
