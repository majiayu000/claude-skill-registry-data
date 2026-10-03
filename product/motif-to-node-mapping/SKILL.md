---
name: motif-to-node-mapping
description: Use when you have a GNPS-generated classical or feature-based mass spectral molecular network (graphml or JSON format) and a corresponding MS2LDA experiment with Mass2Motif assignments on the same spectra, and you want to visualize and quantify which structural motifs are shared within and across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - pyMolNetEnhancer
  - Python
  - RMolNetEnhancer
  - GNPS
  - ms2lda.org
  - Cytoscape
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure information
- pyMolNetEnhancer is a python module
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnetenhancer
    doi: 10.3390/metabo9070144
    title: molnetenhancer
  dedup_kept_from: coll_molnetenhancer
schema_version: 0.2.0
---

# motif-to-node-mapping

## Summary

Map MS2LDA-derived Mass2Motif substructural information onto nodes in GNPS mass spectral molecular networks (classical or feature-based mode) to annotate network components with discovered structural motifs. This enables visual and quantitative exploration of shared chemical substructures across networked spectra.

## When to use

You have a GNPS-generated classical or feature-based mass spectral molecular network (graphml or JSON format) and a corresponding MS2LDA experiment with Mass2Motif assignments on the same spectra, and you want to visualize and quantify which structural motifs are shared within and across molecular families (network components).

## When NOT to use

- Your molecular network was not created through the GNPS platform or uses a non-standard network format incompatible with graphml/JSON input.
- You do not have a corresponding MS2LDA experiment on the same clustered spectra used to build your GNPS network.
- Your analysis goal is to identify novel chemical structures de novo rather than to map known/discovered motifs onto an existing network.

## Inputs

- GNPS classical molecular network file (graphml or JSON format)
- MS2LDA Mass2Motif output data (motif-document relations with probability and overlap scores)
- GNPS job ID
- MS2LDA job ID

## Outputs

- Annotated molecular network file (graphml or JSON) with motif metadata embedded in node attributes
- Mass2Motifs_Nodes_Classical.tsv or Mass2Motifs_Nodes_FeatureBased.tsv (node table with motif assignments)
- Mass2Motifs_Edges_Classical.tsv or Mass2Motifs_Edges_FeatureBased.tsv (edge table with shared motif interactions)

## How to apply

Retrieve your GNPS job ID and MS2LDA job ID (or manually download the MS2LDA summary table if server timeout occurs). Load the GNPS network file and MS2LDA motif-document relations into pyMolNetEnhancer or RMolNetEnhancer. Set filtering thresholds: minimal probability score (default 0.01) and minimal overlap score (default 0.3) for motif inclusion, and specify the number of top shared motifs per network component to display (default 5). The tool aligns motif identifiers to network nodes based on precursor m/z and spectral similarity, embeds motif metadata in node attributes, and exports an annotated graphml or JSON file with node and edge tables (TSV format) indicating shared motifs. Visualize the enhanced network in Cytoscape by mapping 'interaction' column to edge stroke color and 'TopSharedMotifs' to node charts.

## Related tools

- **pyMolNetEnhancer** (Python module that performs MS2LDA motif-to-node alignment and network annotation in classical and feature-based modes) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (Analogous R package providing identical motif-to-node mapping functionality as pyMolNetEnhancer) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Global Natural Products Social Molecular Networking platform that generates the input mass spectral molecular networks) — https://gnps.ucsd.edu/
- **ms2lda.org** (Web application for Latent Dirichlet Allocation analysis that generates Mass2Motif substructural assignments on MS2 spectra) — http://ms2lda.org/
- **Cytoscape** (Network visualization tool used to display and annotate the enhanced molecular networks with motif information) — https://cytoscape.org/

## Evaluation signals

- The output graphml or JSON file contains new node attributes populated with motif IDs and confidence scores; nodes without assigned motifs should have empty or null values, not errors.
- The Mass2Motifs_Nodes output table has a row for each cluster ID in the original network, with motif columns respecting the prob and overlap thresholds specified (e.g., no motifs with prob < 0.01 or overlap < 0.3).
- The Mass2Motifs_Edges output table correctly identifies pairs of nodes (CLUSTERID1, CLUSTERID2) that share at least one motif, with the 'interact' column listing the shared motif ID(s).
- When imported into Cytoscape, edges colored by motif interaction and nodes colored by TopSharedMotifs display visually coherent groups (e.g., nodes in the same molecular family share the same dominant motifs).
- The number of unique motifs shown per network component does not exceed the 'top' parameter value (default 5) specified at runtime.

## Limitations

- Server connection timeout may occur when retrieving large MS2LDA summary files; manual download from http://ms2lda.org/ is recommended as a fallback.
- Mapping accuracy depends on consistent precursor m/z and spectral similarity matching between the GNPS network and MS2LDA assignments; discrepancies in data preprocessing or clustering parameters between platforms can introduce misalignments.
- The tool requires user-defined filtering thresholds (prob, overlap, top) which may need empirical tuning per dataset; the README notes that these thresholds should ideally match those set in the ms2lda.org web app interface.
- No changelog is available to track breaking changes or deprecated features between software versions.

## Evidence

- [intro] pyMolNetEnhancer integrates chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks"
- [other] MS2LDA motifs are mapped to network nodes via alignment of precursor m/z and spectral similarity: "align MS2LDA motif identifiers to corresponding nodes in the molecular network based on precursor m/z and spectral similarity"
- [readme] The workflow requires GNPS classical mode network, MS2LDA motif assignments, and produces annotated graphml output: "Create a molecular network through the Global Natural Products Social Molecular Networking (GNPS) platform. Create an LDA experiment on http://ms2lda.org/"
- [readme] Probability and overlap are the primary filtering thresholds for motif inclusion in the network: "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3."
- [readme] Output includes TSV edge and node tables in addition to graphml for alternative Cytoscape import workflow: "Alternatively the edges and nodes output files can also be loaded separately into Cytoscape. To this end import the 'Mass2Motifs_Edges_Classical.tsv' output file as network into Cytoscape"
- [readme] Server connection timeout may require manual file download from ms2lda.org: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
