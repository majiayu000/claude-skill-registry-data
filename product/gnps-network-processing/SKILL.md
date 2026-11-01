---
name: gnps-network-processing
description: Use when you have generated a GNPS mass spectral molecular network (in classical or feature-based mode) and want to annotate network nodes with substructural motifs from MS2LDA or chemical class information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - pyMolNetEnhancer
  - GNPS
  - Python
  - RMolNetEnhancer
  - MS2LDA (ms2lda.org)
  - Cytoscape
derived_from:
- doi: 10.3390/metabo9070144
  title: molnetenhancer
evidence_spans:
- pyMolNetEnhancer is a python module integrating chemical class and substructure information
- mass spectral molecular networks created through the Global Natural Products Social Molecular Networking (GNPS) platform
- mass spectral molecular networks created through the Global Natural Products Social Molecular Networking (GNPS)
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

# Map Substructural and Chemical Class Information to GNPS Molecular Networks

## Summary

This skill integrates MS2LDA-derived Mass2Motif substructural information and chemical class annotations onto mass spectral molecular networks created through the GNPS platform, supporting both classical and feature-based network modes. It enables structural interpretation of molecular families by mapping motif probabilities and chemical class labels to network nodes and edges.

## When to use

You have generated a GNPS mass spectral molecular network (in classical or feature-based mode) and want to annotate network nodes with substructural motifs from MS2LDA or chemical class information. Use this skill when you need to understand which structural motifs are shared within molecular families or relate spectral similarity patterns to known chemical scaffolds.

## When NOT to use

- Your molecular network was not generated through GNPS or uses a non-standard format incompatible with GraphML/JSON.
- You have not created an MS2LDA LDA experiment using clustered spectra from your GNPS job; motif mapping requires MS2LDA output.
- Your analysis goal is only network topology or spectral clustering; chemical class or motif annotation is not relevant to your research question.

## Inputs

- GNPS molecular network file (GraphML or JSON format, from classical or feature-based workflow)
- MS2LDA Mass2Motif summary output (TSV or downloaded from ms2lda.org)
- GNPS job ID (for direct server retrieval of network and motif data)
- MS2LDA job ID (for retrieval of motif assignments)

## Outputs

- Annotated molecular network file (GraphML format) with motif IDs and confidence scores embedded in node attributes
- Mass2Motifs_Edges_Classical.tsv or equivalent (interaction type, shared motif labels, confidence metrics)
- Mass2Motifs_Nodes_Classical.tsv or equivalent (node cluster IDs, assigned motif labels, TopSharedMotifs per molecular family)
- Cytoscape-compatible network visualization with colored edges and nodes reflecting motif sharing patterns

## How to apply

Load the GNPS-generated molecular network file (GraphML or JSON format) and MS2LDA Mass2Motif output data containing substructural assignments and probability scores. Apply pyMolNetEnhancer (or RMolNetEnhancer for R users) with user-defined thresholds: a minimal probability score (default 0.01) and overlap score (default 0.3) to filter low-confidence motif-document relations. Optionally specify a `top` parameter (default 5) to limit display to the most shared motifs per molecular family (network component index). Execute the mapping function appropriate to your network type (classical or feature-based), which aligns motif identifiers to corresponding nodes via precursor m/z and spectral similarity. Export the annotated network as GraphML with motif metadata and confidence scores embedded in node and edge attributes. Visualize in Cytoscape by mapping `interaction` attribute to edge stroke color and `TopSharedMotifs` to node chart/image properties.

## Related tools

- **pyMolNetEnhancer** (Python module that executes the mapping of MS2LDA motifs and chemical classes onto GNPS network nodes and edges) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package providing equivalent functionality to pyMolNetEnhancer for network annotation) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Generates the classical or feature-based mass spectral molecular network (GraphML/JSON) that serves as input) — https://gnps.ucsd.edu/
- **MS2LDA (ms2lda.org)** (Performs Latent Dirichlet Allocation on clustered spectra to derive Mass2Motif substructural assignments with probability and overlap scores) — http://ms2lda.org/
- **Cytoscape** (Desktop visualization tool for importing annotated network GraphML files and applying discrete/continuous color mapping to nodes and edges) — https://cytoscape.org/

## Examples

```
pip install pyMolNetEnhancer; then in Python: `from pyMolNetEnhancer import classical_mode; classical_mode(gnps_job_id='1234567890', ms2lda_job_id='abcd', prob=0.01, overlap=0.3, top=5)` to generate annotated GraphML and TSV outputs.
```

## Evaluation signals

- Verify that all nodes in the output network have non-null motif ID and confidence score attributes; nodes with zero motifs should be explicitly marked or excluded depending on parameter thresholds.
- Check that probability and overlap values in output TSV files respect the specified thresholds (default prob ≥ 0.01, overlap ≥ 0.3); any relation below threshold should be absent from the annotated network.
- Confirm that TopSharedMotifs list per molecular family (network component index) contains at most `top` motifs (default 5) and is sorted by frequency or confidence in descending order.
- Validate that edge attributes correctly reflect shared motif labels between connected nodes; visualized edge colors should be discrete and correspond to unique interaction (motif) labels.
- Cross-check MS2LDA summary table (from ms2lda.org web app) against output node/edge TSV files to ensure motif-document and motif-cluster relations are consistently represented after thresholding.

## Limitations

- Mapping accuracy depends on the quality and overlap of GNPS spectral clustering and MS2LDA motif assignments; poor spectral similarity within clusters or low-confidence motif probabilities reduce annotation reliability.
- MS2LDA server connection timeouts may occur for large MGF files; manual download from ms2lda.org is an alternative but requires user intervention.
- The `prob` and `overlap` thresholds set in the ms2lda.org web app Experimental Options tab override or interact with thresholds set during pyMolNetEnhancer/RMolNetEnhancer execution; coordination between these two systems is required for reproducible filtering.
- Feature-based networks require MS2LDA input generated from the MZmine-derived MGF file (not the GNPS-clustered MGF), introducing an additional preprocessing dependency.
- Chemical class mapping relies on availability of class metadata in the GNPS public library; compounds not in this library will lack chemical class annotations.
- Visualization of complex networks (>1000 nodes) in Cytoscape may become computationally expensive; node filtering or layout optimization may be necessary for interpretability.

## Evidence

- [intro] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the GNPS platform: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [other] Load the GNPS-generated classical molecular network file and use pyMolNetEnhancer's classical-mode mapping function to align MS2LDA motif identifiers to corresponding nodes: "Load the GNPS-generated classical molecular network file (graphml or JSON format) and MS2LDA Mass2Motif output data containing substructural motif assignments. 2. Use pyMolNetEnhancer's"
- [readme] User-defined parameters include prob (minimal probability score, default 0.01), overlap (minimal overlap score, default 0.3), and top (how many most shared motifs per molecular family to show, default 5): "prob: minimal probability score for a Mass2Motif to be included. Default is 0.01. overlap: minimal overlap score for a Mass2Motif to be included. Default is 0.3. top: This parameter specifies how"
- [readme] To visualize results import the .graphml output file into Cytoscape and color edges based on shared Mass2Motifs or nodes by TopSharedMotifs: "To visualize results import the .graphml output file into Cytoscape. To color edges based on shared Mass2Motifs in between nodes select 'Stroke Color' in the 'Edge' tab to the left and choose"
- [readme] Feature-based networks require MS2LDA input generated from the MZmine MGF file, not the GNPS-clustered MGF: "Create an LDA experiment on http://ms2lda.org/ using the MGF file created within MZmine"
- [readme] Server connection timeouts may occur for large MS2LDA files; manual download from ms2lda.org is an alternative: "Depending on the size of this file, a server connection timeout may occur. Alternatively, you may download the file manually at http://ms2lda.org/"
