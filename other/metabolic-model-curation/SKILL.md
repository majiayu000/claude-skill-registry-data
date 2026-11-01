---
name: metabolic-model-curation
description: Use when you have generated consensus metabolic reconstructions for multiple members of a microbial community (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3837
  edam_topics:
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_2259
  tools:
  - COMMIT
derived_from:
- doi: 10.1371/journal.pcbi.1009906
  title: COMMIT
evidence_spans:
- community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_commit
    doi: 10.1371/journal.pcbi.1009906
    title: COMMIT
  dedup_kept_from: coll_commit
schema_version: 0.2.0
---

# metabolic-model-curation

## Summary

Curate and complete consensus metabolic reconstructions for microbial community members by leveraging community-dependent metabolic context to identify and fill gaps in individual models. This skill reconciles metabolic gaps across a community using shared biochemical dependencies and exchange requirements.

## When to use

Apply this skill when you have generated consensus metabolic reconstructions for multiple members of a microbial community (e.g., from Arabidopsis thaliana leaf or root samples) and need to resolve metabolic gaps—missing reactions or pathways—by exploiting metabolic interdependencies and shared biochemical context across community members rather than curating each model in isolation.

## When NOT to use

- Community members have no metabolic interdependencies or shared biochemical context—use single-model gap-filling (e.g., constraint-based flux balance analysis on individual models) instead.
- Input consensus reconstructions have not been validated or contain systematic annotation errors—resolve quality issues before community curation.
- The ecological or metabolic context of the community is unknown or poorly characterized—gap-filling will be unreliable without knowledge of community structure and function.

## Inputs

- consensus metabolic reconstructions for all community members (metabolic model format, e.g. JSON, SBML)
- specification of metabolic gaps to address across the community member set
- reference biochemical database or known plant metabolism pathways

## Outputs

- gap-filled metabolic models for each community member
- annotations linking filled reactions to their source and confidence score
- validation report confirming consistency with known plant metabolism and inter-member exchange

## How to apply

Load the consensus metabolic reconstructions for all community members generated from prior assembly or annotation steps. Initialize the COMMIT gap-filling module with the full community context, specifying which metabolic gaps to address across the member set. Execute the community-dependent gap-filling algorithm, which leverages metabolic overlap and dependencies (e.g., shared substrates, cofactor requirements, cross-feeding potential) between community members to propose reactions filling identified gaps. Validate proposed filled gaps by checking consistency with known plant metabolism (Arabidopsis thaliana in this example) and inter-member nutrient exchange requirements. Output gap-filled metabolic models for each community member with annotations indicating the source (which community member(s) informed the gap-fill) and confidence score of filled reactions.

## Related tools

- **COMMIT** (Executes community-dependent gap-filling module that leverages metabolic context from multiple community members to identify and fill metabolic gaps in consensus reconstructions) — https://zenodo.org/record/363932874

## Evaluation signals

- Gap-filled reactions pass consistency checks against known Arabidopsis thaliana metabolic pathways and do not contradict plant physiology.
- Filled reactions are annotated with source community member(s) and confidence score; reactions with lower confidence are flagged for manual review.
- Inter-member metabolic exchange requirements (cross-feeding, shared cofactor synthesis) are satisfied after gap-filling; test with community flux balance simulations.
- Gap-filled models are semantically valid (proper metabolite and reaction naming, balanced stoichiometry, no orphan metabolites).
- Comparison of individual model gaps before and after community curation shows that community-shared metabolic context resolves gaps that would remain unresolved in single-model curation.

## Limitations

- Gap-filling accuracy depends on the completeness and correctness of input consensus reconstructions; errors or missing pathways in the starting models propagate into filled models.
- Community-dependent gap-filling may artificially resolve gaps if community members are incorrectly assembled or if inter-member metabolic dependencies are over-inferred from limited data.
- Filled reactions are inferred, not experimentally validated; high-confidence gap-fills require downstream biochemical or genomic evidence.
- The skill assumes community members share sufficient metabolic context; highly specialized or isolated community members may not benefit from cross-member gap-filling.

## Evidence

- [other] COMMIT implements community-dependent gap-filling as a module that operates on consensus metabolic reconstructions generated for community members, leveraging shared metabolic context across the community to identify and fill metabolic gaps.: "COMMIT implements community-dependent gap-filling as a module that operates on consensus metabolic reconstructions generated for community members, leveraging shared metabolic context across the"
- [other] Execute community-dependent gap-filling algorithm that leverages metabolic overlap and dependencies between community members to propose reactions filling identified gaps.: "Execute community-dependent gap-filling algorithm that leverages metabolic overlap and dependencies between community members to propose reactions filling identified gaps."
- [other] Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements.: "Validate filled gaps by checking consistency with known plant (Arabidopsis thaliana) metabolism and inter-member exchange requirements."
- [other] Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions.: "Output gap-filled metabolic models for each community member with annotations indicating source and confidence of filled reactions."
- [intro] community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana: "community-dependent gap-filling using COMMIT for communites sampled from Arabidopsis thaliana"
