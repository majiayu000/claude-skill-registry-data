---
name: genome-identifier-lookup
description: Use when a paired omics project JSON document contains genome identifiers (e.g. IMG IDs, NCBI accessions) but lacks corresponding organism names.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3672
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0080
  tools:
  - npm
  - redis queue
  - NCBI Taxonomy / IMG
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla
schema_version: 0.2.0
---

# genome-identifier-lookup

## Summary

Enriches paired omics project JSON documents by querying external genome registries (e.g. NCBI Taxonomy, IMG) to retrieve organism names from genome identifiers, then injecting the retrieved names back into the project record. This links MS/MS mass spectra with genomic context for downstream biosynthetic discovery.

## When to use

A paired omics project JSON document contains genome identifiers (e.g. IMG IDs, NCBI accessions) but lacks corresponding organism names. The enrichment is necessary when the project will be stored, searched, or linked to biosynthetic gene clusters and you need human-readable organism context alongside the spectral data.

## When NOT to use

- The genome identifier is invalid, malformed, or not present in the external registry (lookup will fail or return null; validation will catch this)
- The project JSON already contains a populated organism name field (enrichment would be redundant)
- Offline mode or disconnected operation where external registry access is unavailable

## Inputs

- Project JSON document with genome identifier field
- Genome identifier (e.g. IMG genome ID, NCBI RefSeq accession)

## Outputs

- Enriched project JSON document with organism name field populated
- Updated project file written to disk with linked genomic metadata

## How to apply

Parse the input project JSON document to extract the genome identifier field. Query an external genome registry (e.g. NCBI Taxonomy or IMG) using the genome identifier to retrieve the organism name. Inject the retrieved organism name into the project JSON document as a new or updated field. Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name. Write the enriched project JSON to the output file. The platform uses a redis queue to schedule these lookup jobs asynchronously, allowing batch enrichment of projects without blocking the web service.

## Related tools

- **npm** (Build and test framework for running the enrichment pipeline within the Node.js web service)
- **redis queue** (Asynchronous job scheduler that queues genome identifier lookups to fetch organism names and enrich projects)
- **NCBI Taxonomy / IMG** (External genome registry queried by the enrichment step to retrieve organism names from genome identifiers)

## Evaluation signals

- Enriched JSON validates against the JSON schema (app/public/schema.json) and is well-formed
- Both the original genome identifier and the newly populated organism name field are present in the enriched document
- The retrieved organism name matches expected nomenclature from the external registry (e.g. binomial species name format)
- Existing npm tests still pass after enrichment (run `npm run test` in api/ directory)
- Project file is successfully written to output with no truncation or encoding errors

## Limitations

- External registry query may fail or timeout if the registry is unavailable or the network connection is poor
- Genome identifier may not be found in the external registry, resulting in a null or empty organism name that fails validation
- Registry data may be incomplete, outdated, or use non-standard nomenclature for organism names, requiring manual curation
- Links to GNPS task identifiers were reported as broken in the platform documentation

## Evidence

- [readme] The platform links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method: "Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method"
- [readme] The web service uses a redis queue to schedule jobs to fetch more information about public identifiers, such as fetching the scientific species name from GenBank using genome identifiers: "The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific"
- [other] Parse input JSON, query external registry using genome identifier, inject organism name, validate enriched JSON, and write to output: "1. Parse the input project JSON document to extract the genome identifier field. 2. Query an external genome registry (e.g. NCBI Taxonomy, IMG, or equivalent) using the genome identifier to retrieve"
- [readme] The JSON schema describes the format of a project and is used for validation: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
