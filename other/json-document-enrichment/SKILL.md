---
name: json-document-enrichment
description: Use when when your project JSON document contains public identifiers (genome IDs, biosample accessions, etc.) that lack human-readable or linked metadata, and you need to populate those fields programmatically before storage or publication to enable full-text search, validation, or cross-linking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0157
  tools:
  - npm
  - paired-data-form (iomega)
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

# json-document-enrichment

## Summary

Augment a project JSON document by querying external registries (e.g., genome identifier → organism name) and injecting retrieved metadata as new fields, enabling integrated multi-omics data representation. This skill bridges standalone identifiers with curated biological information for downstream analysis.

## When to use

When your project JSON document contains public identifiers (genome IDs, biosample accessions, etc.) that lack human-readable or linked metadata, and you need to populate those fields programmatically before storage or publication to enable full-text search, validation, or cross-linking with other omics data types (MS/MS spectra, gene clusters).

## When NOT to use

- Input project JSON already contains all required organism or metadata fields and no external lookup is needed.
- External registry is unavailable, unreliable, or does not support querying by the identifier type present in your document.
- The identifier is already a free-text organism name or a non-resolvable/proprietary identifier without a public registry.

## Inputs

- project JSON document (as file or object) containing at least one public genome/sample identifier field

## Outputs

- enriched project JSON document with new or updated metadata field (e.g., organism name)
- validation report confirming schema conformance and presence of both original and enriched fields

## How to apply

Parse the input project JSON document to extract the identifier field of interest (e.g., genome identifier). Query an external genome registry—such as NCBI Taxonomy, IMG, or GenBank—using that identifier to retrieve the corresponding organism name or other linked metadata. Inject the retrieved value into the project JSON as a new or updated field. Validate that the enriched JSON is well-formed and conforms to the project schema, ensuring both the original identifier and the newly populated field are present and correctly typed. Write the enriched document to the output file. Use npm-based test suites (e.g., `npm run test`) to verify that enrichment logic preserves all existing fields and does not break downstream search or upload workflows.

## Related tools

- **npm** (run test suites to verify enrichment logic preserves schema validity and does not break downstream workflows) — https://www.npmjs.com
- **paired-data-form (iomega)** (web application and API that stores project JSON documents and uses redis queue to schedule enrichment jobs fetching organism names from GenBank identifiers) — https://github.com/iomega/paired-data-form

## Evaluation signals

- Enriched JSON parses without syntax errors and validates against the project schema (app/public/schema.json).
- Original identifier field is preserved unchanged in the output document.
- New metadata field is present and populated with a non-empty value retrieved from the external registry (not null, not empty string).
- Downstream workflows (full-text search, upload to Zenodo, API retrieval) operate on the enriched document without errors.
- npm test suite passes after enrichment logic is added, confirming no regression in existing functionality.

## Limitations

- Registry queries may fail or return incomplete results if the identifier is malformed, deprecated, or not present in the external database; error handling and fallback strategies are essential.
- Enrichment latency scales with registry response time and network reliability; consider asynchronous/queued processing (as implemented via redis in the paired-data-form platform) for large document batches.
- Some organisms or identifiers may map to multiple registry entries or ambiguous results, requiring manual curation or conflict resolution logic.
- Spaces and special characters in URLs must be properly encoded to avoid breaking registry queries; documented issues (#75) note that unencoded spaces cause failures.

## Evidence

- [other] Parse the input project JSON document to extract the genome identifier field. Query an external genome registry (e.g. NCBI Taxonomy, IMG, or equivalent) using the genome identifier to retrieve the organism name. Inject the retrieved organism name into the project JSON document as a new or updated field. Validate that the enriched JSON is well-formed and contains both the original genome identifier and the newly populated organism name. Write the enriched project JSON to the output file.: "Parse the input project JSON document to extract the genome identifier field. Query an external genome registry (e.g. NCBI Taxonomy, IMG, or equivalent) using the genome identifier to retrieve the"
- [readme] The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific species name is fetched from GenBank using the public genome identifiers in the project.: "The web service uses a redis queue (v5.0.5) to schedule jobs to fetch more information about the public identifiers and to upload the projects to Zenodo each month. For example, the scientific"
- [intro] Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method: "Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method"
- [other] make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory: "make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory"
- [discussion] Warning to not include spaces in urls ([#75]: "Warning to not include spaces in urls ([#75]"
