---
name: chemical-class-mapping
description: Use when you have a GNPS molecular network (GML or GraphML format) and
  wish to annotate network nodes with chemical class labels to support metabolite
  family interpretation. Use it specifically when you need to overlay chemical classification
  schemes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - pyMolNetEnhancer
  - Python
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

# chemical-class-mapping

## Summary

Map chemical class annotations onto mass spectral molecular network nodes to enable semantic enrichment and interpretation of metabolite clusters. This skill integrates standardized chemical taxonomy with GNPS-generated network topology, revealing the structural and pharmacological families present in complex natural product mixtures.

## When to use

Apply this skill when you have a GNPS molecular network (GML or GraphML format) and wish to annotate network nodes with chemical class labels to support metabolite family interpretation. Use it specifically when you need to overlay chemical classification schemes (e.g., natural product classes, chemical ontologies) onto an existing mass spectral molecular network to identify which structural classes cluster together and to facilitate comparative analysis across datasets.

## When NOT to use

- Input network is not in GML/GraphML format or lacks valid cluster identifiers that match the chemical class table
- Chemical class mapping is incomplete or inconsistent (e.g., > 20% of clusters lack class assignments) — reconcile mapping table before proceeding
- Goal is to perform *de novo* chemical class prediction rather than integrate pre-computed classifications — use MS2LDA or other discovery methods instead

## Inputs

- GNPS molecular network (GML or GraphML format)
- Chemical class mapping table (CSV or TSV with cluster IDs and class labels)
- Node attribute metadata (optional, for merging with existing annotations)

## Outputs

- Class-annotated molecular network (GraphML format)
- Node attribute table with integrated chemical class labels (CSV format)
- Edge list with class-based interaction annotations (TSV format, optional)

## How to apply

Load the GNPS molecular network in GML or GraphML format along with a chemical class mapping table (typically a CSV or TSV with cluster IDs and corresponding chemical class assignments). Use pyMolNetEnhancer's chemical class integration functions to map these class labels to network nodes by matching cluster identifiers. Merge the chemical class annotations into unified node attribute tables, ensuring that each node receives appropriate class labels without overwriting existing attributes. Export the annotated network in GraphML format and the node attribute table in CSV format for visualization in Cytoscape or downstream analysis. Set any filtering parameters (e.g., confidence thresholds) before mapping to control annotation stringency.

## Related tools

- **pyMolNetEnhancer** (Python module that performs chemical class mapping to network nodes and merges annotations into unified node attributes) — https://github.com/madeleineernst/pyMolNetEnhancer
- **RMolNetEnhancer** (R package equivalent for chemical class mapping to mass spectral molecular networks) — https://github.com/madeleineernst/RMolNetEnhancer
- **GNPS** (Source platform for generating the molecular network topology in GML/GraphML format) — https://gnps.ucsd.edu/
- **Cytoscape** (Visualization tool for importing and rendering the class-annotated GraphML network with node/edge styling) — https://cytoscape.org/

## Examples

```
pip install pyMolNetEnhancer; python -c "from pyMolNetEnhancer import *; map_chemical_classes('network.graphml', 'chemical_classes.csv', output_prefix='annotated')"
```

## Evaluation signals

- All network nodes have non-null chemical class attributes in the output CSV; verify no nodes are orphaned during the merge
- GraphML output retains the original network topology (node count and edge count unchanged) while adding class labels to node attributes
- Chemical class distribution in the annotated network matches the expected ratio from the input mapping table (±5%); spot-check 10–20 nodes visually in Cytoscape
- Node attribute table can be successfully imported into Cytoscape and used for discrete mapping to node color or shape without errors
- Export files conform to standard formats: GraphML is valid XML, CSV is properly delimited with no malformed rows

## Limitations

- Mapping accuracy is contingent on cluster ID matching between the GNPS network and the chemical class table; inconsistent nomenclature or missing IDs will result in unmapped nodes
- Chemical class annotations are only as reliable as the source classification scheme; no de novo validation is performed by the tool
- Large networks (>5000 nodes) may experience performance delays during merging depending on system memory; test on a subset first if using this skill on very large datasets
- The tool does not handle hierarchical or multi-level chemical class assignments natively; flattening or reformatting may be required if your classification scheme has multiple inheritance levels

## Evidence

- [other] pyMolNetEnhancer maps chemical class information to mass spectral molecular networks, enabling annotation of network nodes with chemical class labels.: "pyMolNetEnhancer maps chemical class information to mass spectral molecular networks, enabling annotation of network nodes with chemical class labels."
- [other] Load the GNPS molecular network (GML or GraphML format) and MS2LDA substructural feature assignments into pyMolNetEnhancer. Map chemical class information to network nodes using the module's chemical class integration functions.: "Load the GNPS molecular network (GML or GraphML format) and MS2LDA substructural feature assignments into pyMolNetEnhancer. Map chemical class information to network nodes using the module's chemical"
- [other] Merge chemical class and MS2LDA annotations into unified node attributes. Export the class-annotated network and node attribute table in standard formats (GML/GraphML and CSV).: "Merge chemical class and MS2LDA annotations into unified node attributes. Export the class-annotated network and node attribute table in standard formats (GML/GraphML and CSV)."
- [readme] pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular Networking (GNPS) platform.: "pyMolNetEnhancer is a python module integrating chemical class and substructure information within mass spectral molecular networks created through the Global Natural Products Social Molecular"
- [readme] Map chemical class information to mass spectral molecular networks: "Map chemical class information to mass spectral molecular networks"
