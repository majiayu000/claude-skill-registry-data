---
name: kegg-api-querying
description: Use when after metabolite KEGG identifiers and hierarchy metadata have
  been assigned (via assign_hierarchy with 'KEGG' identifier) and you need to enrich
  your metabolomics count data frame with functional orthology and associated gene
  information from KEGG.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - KEGGREST
  - R
  - Omu
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1128/mra.00129-19
  title: omu metabolomics count data tool
evidence_spans:
- which retrieves data from the KEGG API using the function ```keggGet``` from the
  package KEGGREST
- Omu is an R package that enables rapid analysis of Metabolomics data sets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
  dedup_kept_from: coll_omu_metabolomics_count_data_tool_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00129-19
  all_source_dois:
  - 10.1128/mra.00129-19
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# kegg-api-querying

## Summary

Query the KEGG API via the KEGGREST package to retrieve functional orthology (KO numbers) and gene names for metabolite-annotated data frames. This skill integrates KEGG functional data into metabolomics count tables, enabling orthology-based downstream analysis.

## When to use

Apply this skill after metabolite KEGG identifiers and hierarchy metadata have been assigned (via assign_hierarchy with 'KEGG' identifier) and you need to enrich your metabolomics count data frame with functional orthology and associated gene information from KEGG. This is necessary when performing metabolite-to-function mapping or when linking metabolic features to prokaryotic/eukaryotic gene families.

## When NOT to use

- Your metabolite identifiers are not KEGG compound IDs (use a different identifier type or mapping)
- You lack internet access to query the live KEGG API
- Your data frame has not yet been assigned hierarchy metadata via assign_hierarchy

## Inputs

- metabolomics count data frame with KEGG compound identifiers
- hierarchy metadata columns from assign_hierarchy output

## Outputs

- augmented data frame with new functional orthology (KO) columns
- augmented data frame with gene name columns

## How to apply

Call the KEGG_gather S3 method on your metabolite-annotated data frame; the method automatically dispatches based on the data frame's class metadata. For each metabolite's KEGG ID, KEGG_gather invokes keggGet from the KEGGREST package to query the KEGG API and retrieve the corresponding functional orthology and gene records. The returned KEGG records are parsed and cleaned using the internal make_omelette function to extract KO identifiers and gene names into a structured format. The cleaned data is then formatted using the plate_omelette S3 method and bound as new columns to the input data frame. Ensure your input data frame carries the proper S3 class (determined by existing hierarchy metadata columns) so that dispatch and formatting proceed correctly.

## Related tools

- **KEGGREST** (R package providing keggGet function to query the KEGG API and retrieve KO and gene data)
- **R** (Statistical computing environment in which Omu and KEGGREST operate)
- **Omu** (Metabolomics analysis R package providing KEGG_gather S3 method wrapper) — github.com/connor-reid-tiffany/Omu

## Examples

```
KEGG_gather(metabolite_df)
```

## Evaluation signals

- Output data frame has new columns containing KO identifiers (e.g., 'K00001', 'K02288') with no missing values for valid KEGG compounds
- Output data frame has gene name columns with associated gene symbols and descriptions parsed from KEGG records
- Row count of output equals input; no metabolites were dropped during API querying
- All original metabolite identifiers and hierarchy metadata columns are preserved in the output
- API call latency is reasonable (seconds to minutes depending on number of metabolites); failures should be logged with specific KEGG IDs that failed

## Limitations

- Requires live internet connectivity to the KEGG API; offline operation is not supported
- KEGG API may rate-limit or temporarily unavail; no built-in retry or caching logic is mentioned
- Metabolites without valid KEGG compound IDs will not retrieve data; data quality depends on upstream assignment accuracy
- The internal make_omelette and plate_omelette functions are not documented in the article; their behavior and parsing rules are opaque to end users

## Evidence

- [other] keggGet retrieves functional orthology (KO numbers) and associated gene information: "invoke keggGet from KEGGREST package to query the KEGG API and retrieve functional orthology (KO numbers) and associated gene information"
- [other] KEGG_gather is an S3 method that dispatches on data frame class: "Call KEGG_gather on the data frame, which dispatches based on the S3 class determined by existing metadata columns"
- [other] make_omelette parses and cleans KEGG records: "Parse and clean the returned KEGG records using the internal make_omelette function to extract KO identifiers and gene names into a structured format"
- [other] KEGG_gather requires KEGG compound identifiers and hierarchy metadata as input: "Load a metabolomics count data frame with KEGG compound identifiers and hierarchy metadata (output from assign_hierarchy)"
- [other] Omu uses KEGG_gather S3 method to retrieve data from KEGG API: "To gather functional orthology and gene data, Omu uses an S3 method called ```KEGG_gather```, which retrieves data from the KEGG API"
