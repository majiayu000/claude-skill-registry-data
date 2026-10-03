---
name: s3-method-dispatch
description: Use when your metabolomics data frame has inherited or assigned class
  metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - KEGGREST
  - R
  - assign_hierarchy
  - make_omelette
  - plate_omelette
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

# s3-method-dispatch

## Summary

Use S3 method dispatch to dynamically route data-frame processing logic based on metadata class attributes, enabling flexible annotation and transformation pipelines that adapt to heterogeneous metabolomics data structures. This skill ensures that generic operations like KEGG_gather select the correct class-specific implementation (e.g., plate_omelette) without explicit conditional branching.

## When to use

Your metabolomics data frame has inherited or assigned class metadata (e.g., KEGG hierarchy class determined by assign_hierarchy) and you need to apply a generic operation—such as functional orthology retrieval or data formatting—that must behave differently depending on which classification system (KEGG, KO_Number, Prokaryote, or Eukaryote) is already present. Use this skill when a single function name should produce different outputs for different data structures without forcing the caller to specify the variant.

## When NOT to use

- Input data frame has no class attribute or metadata; dispatch will fail or fall back to default method, potentially losing desired logic.
- You need conditional branching based on user input or parameter values rather than object class; use explicit if/else instead of S3 dispatch.
- The operation should behave identically regardless of metabolite classification system; a single function is simpler and avoids dispatch overhead.

## Inputs

- metabolomics count data frame with assigned class attribute (output from assign_hierarchy)
- hierarchical metadata columns (KEGG ID, KO number, or prokaryote/eukaryote classifier)

## Outputs

- augmented data frame with class-specific formatting applied
- functional orthology and gene annotation columns (for KEGG_gather dispatch)
- formatted output structure appropriate to the dispatched class method

## How to apply

Define a generic S3 function (e.g., KEGG_gather or plate_omelette) with a default method and one or more class-specific methods. Ensure the input data frame has been assigned an appropriate class attribute via assign_hierarchy or similar prior setup. When the generic function is called on the data frame, R's method dispatch system automatically selects the matching class method. For KEGG_gather, this means the dispatcher routes to the correct keggGet invocation and parsing path; for plate_omelette, the dispatcher selects the output formatting appropriate to the current class. Verify dispatch by checking the class attribute (e.g., class(data_frame)) before calling the generic function.

## Related tools

- **KEGGREST** (dispatched to retrieve functional orthology and gene names from the KEGG API via keggGet; called within class-specific KEGG_gather method)
- **assign_hierarchy** (assigns class attributes to the input data frame before dispatch; determines which S3 method will be selected) — https://github.com/connor-reid-tiffany/Omu
- **make_omelette** (internal parsing and cleaning function called by the dispatched KEGG_gather method to extract KO identifiers and gene names) — https://github.com/connor-reid-tiffany/Omu
- **plate_omelette** (S3 method dispatched to format cleaned KEGG data into the structure appropriate to the data frame's class) — https://github.com/connor-reid-tiffany/Omu

## Examples

```
KEGG_gather(metabolite_df)  # dispatch selects the appropriate method based on class(metabolite_df), e.g., KEGG_gather.KEGG or KEGG_gather.KO_Number
```

## Evaluation signals

- Verify that class(data_frame) returns the expected class name (e.g., 'KEGG', 'KO_Number', 'Prokaryote', or 'Eukaryote') before calling the generic function.
- Check that the correct class-specific method was invoked by inspecting the function signature in the call stack or by adding a debug message to each method.
- Confirm that output columns (e.g., KO numbers and gene names from KEGG_gather) match the formatting and structure expected for that class.
- Verify that no errors or 'no applicable method' warnings are raised; if dispatch fails, the default method will execute, which may not provide the desired result.
- Compare the returned data frame structure to the output specification for the specific class method that should have been dispatched.

## Limitations

- S3 dispatch is single-dispatch (based on the class of the first argument only); if you need to dispatch on multiple object types, use S4 or R6 instead.
- If the input data frame loses its class attribute (e.g., via subsetting or transformation), dispatch will revert to the default method, potentially producing incorrect results.
- Method dispatch depends on exact class name matching; typos or class name mismatches will silently fall back to the default method rather than raising an error.
- No changelog is available for the Omu package, so version-specific behavior changes in S3 method implementations are not documented.

## Evidence

- [other] Call KEGG_gather on the data frame, which dispatches based on the S3 class determined by existing metadata columns.: "Call KEGG_gather on the data frame, which dispatches based on the S3 class determined by existing metadata columns."
- [other] To assign hierarchical class data, use the assign_hierarchy function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote": "To assign hierarchical class data, use the ```assign_hierarchy``` function and pick the correct identifier, either "KEGG", "KO_Number", "Prokaryote", or "Eukaryote""
- [other] Format the cleaned data using the plate_omelette S3 method appropriate to the data frame class.: "Format the cleaned data using the plate_omelette S3 method appropriate to the data frame class."
- [other] The KEGG_gather S3 method retrieves data from the KEGG API using the keggGet function from the KEGGREST package to obtain functional orthology and gene names for metabolite-annotated data frames.: "The KEGG_gather S3 method retrieves data from the KEGG API using the keggGet function from the KEGGREST package to obtain functional orthology and gene names for metabolite-annotated data frames."
- [other] To gather functional orthology and gene data, Omu uses an S3 method called KEGG_gather, which retrieves data from the KEGG API: "To gather functional orthology and gene data, Omu uses an S3 method called ```KEGG_gather```, which retrieves data from the KEGG API"
