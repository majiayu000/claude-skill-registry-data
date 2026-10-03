---
name: api-data-retrieval
description: Use when you need to obtain all project JSON documents currently deposited
  in a data platform (such as the Paired Omics Data Platform) to validate their structure
  against a JSON Schema specification, or when you require a complete snapshot of
  published records for quality assurance, data migration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0091
  tools:
  - npm
  - OpenAPI specification
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or
  `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00724-z
  all_source_dois:
  - 10.1038/s41589-020-00724-z
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# api-data-retrieval

## Summary

Retrieve complete sets of JSON documents from a web API endpoint to obtain all currently published records for downstream validation or analysis. This skill is essential when you need to audit data conformance against a schema or perform bulk operations on a platform's full dataset.

## When to use

Apply this skill when you need to obtain all project JSON documents currently deposited in a data platform (such as the Paired Omics Data Platform) to validate their structure against a JSON Schema specification, or when you require a complete snapshot of published records for quality assurance, data migration, or bulk analysis workflows.

## When NOT to use

- If you only need a subset of records (e.g., a single project ID or records matching a filter) — use targeted API queries instead.
- If the platform does not expose an API endpoint for bulk retrieval — fall back to web scraping or manual export mechanisms.
- If your workflow requires real-time streaming data rather than a static snapshot — use event-based subscriptions or webhooks instead.

## Inputs

- API endpoint URL (platform-specific)
- Authentication credentials or access tokens (if required)
- Query parameters specifying scope (e.g., all projects, published projects only)

## Outputs

- Complete set of project JSON documents
- API response metadata (status codes, pagination info)
- Local cache or data store of retrieved records

## How to apply

Query the data platform's API or web interface to retrieve the complete set of project JSON documents currently published. Use the platform's OpenAPI specification (if available) to understand authentication requirements, pagination, and response formats. Retrieve documents in a format suitable for downstream processing (typically JSON). Store the retrieved documents locally or in memory for iteration in subsequent workflow steps (e.g., schema validation). Verify retrieval completeness by checking response status codes, comparing document counts against known platform metrics, and ensuring no pagination tokens remain unprocessed.

## Related tools

- **npm** (Run test suites and manage Node.js dependencies for API client scripts and validation pipelines)
- **OpenAPI specification** (Document API endpoints, authentication schemes, request/response schemas, and pagination rules for programmatic data retrieval)

## Evaluation signals

- HTTP response status code is 200 OK (or other success code) with no connection errors or timeouts.
- Retrieved JSON documents parse without syntax errors and conform to expected top-level schema structure.
- Document count matches or exceeds the platform's known published project count; pagination is fully traversed.
- All required fields present in each document (e.g., project identifier, metadata); no truncated or malformed records.
- Timestamps or version metadata in retrieved documents are recent and consistent with platform state at retrieval time.

## Limitations

- API rate limits or throttling may prevent retrieval of very large datasets in a single batch; implement exponential backoff and pagination handling.
- Authentication credentials or access tokens may expire during long-running bulk retrievals; implement token refresh logic.
- Platform changes to API version, endpoint structure, or response format may break existing retrieval scripts; monitor API deprecation notices.
- Network interruptions or platform unavailability may cause incomplete or failed retrievals; implement retry logic and idempotency checks.

## Evidence

- [other] Query the Paired Omics Data Platform API or web interface to retrieve the complete set of project JSON documents currently published.: "Query the Paired Omics Data Platform API or web interface to retrieve the complete set of project JSON documents currently published."
- [readme] The web service has an OpenAPI (v3.0.3) specification which can be used to submit and retrieve projects in a programmatic manner.: "The web service has an OpenAPI (v3.0.3) specification which can be used to submit and retrieve projects in a programmatic manner."
- [other] Iterate over each retrieved project JSON document and validate its structure and field types against the schema using a JSON Schema validator.: "Iterate over each retrieved project JSON document and validate its structure and field types against the schema using a JSON Schema validator."
