---
name: status-value-parsing
description: Use when when a project README or documentation embeds badge endpoints
  that report real-time status (e.g., Travis CI build, Landscape.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MAGMa
  - Travis CI
  - Landscape.io
  - Coveralls
  - Docker Hub
  - Zenodo
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
- doi: 10.5281/zenodo.1043226
  title: ''
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  - 10.5281/zenodo.1043226
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# status-value-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and tabulate current status values from live project status badge endpoints (CI/CD, code quality, coverage, container, archival) by retrieving and parsing endpoint responses. This skill enables reproducible monitoring of multi-faceted project health indicators embedded in repository documentation.

## When to use

When a project README or documentation embeds badge endpoints that report real-time status (e.g., Travis CI build, Landscape.io code health, Coveralls test coverage, Docker Hub readiness, Zenodo DOI archival) and you need to retrieve, parse, and record the current status values alongside timestamps for comparison, auditing, or dashboard purposes.

## When NOT to use

- Endpoint URLs are not publicly accessible or require authentication beyond simple HTTP GET.
- Status endpoints are known to be deprecated, offline, or non-functional (e.g., Travis CI sunset, Landscape.io discontinuation).
- The goal is to retrieve historical status data; live endpoint parsing only captures present state, not time-series history.

## Inputs

- Repository README file or badge reference documentation (text, Markdown, or reStructuredText)
- Set of badge endpoint URLs (from Travis CI, Landscape.io, Coveralls, Docker Hub, Zenodo, or equivalent)
- HTTP client capable of GET requests and response parsing (requests library, curl, or similar)

## Outputs

- Structured table (CSV, TSV, or JSON) with columns: badge_name, endpoint_url, status_value, retrieval_timestamp
- Optionally: parsed response objects or raw endpoint payloads for archival or further analysis

## How to apply

Locate all badge endpoint URLs in the target repository README (search for common CI/CD, coverage, and archival badge services). For each badge, construct a request to the endpoint URL and parse the response to extract the status field, numerical score, or version string as applicable. Store results in a structured table with columns for badge name, endpoint URL, retrieved status value, and retrieval timestamp. Validate that endpoint responses are well-formed and non-empty before tabulation. Use consistent timestamp format (ISO 8601 recommended) to enable temporal comparison across multiple retrieval cycles.

## Related tools

- **Travis CI** (Provides build status badge endpoint reporting pass/fail CI pipeline status) — https://travis-ci.org/NLeSC/MAGMa
- **Landscape.io** (Provides code health/quality score badge endpoint reporting static analysis results) — https://landscape.io/github/NLeSC/MAGMa/master
- **Coveralls** (Provides test coverage percentage badge endpoint reporting unit test coverage metrics) — https://coveralls.io/r/NLeSC/MAGMa?branch=master
- **Docker Hub** (Provides container image readiness badge endpoint reporting image availability) — https://hub.docker.com/r/nlesc/magma
- **Zenodo** (Provides DOI archival badge endpoint reporting persistent identifier and archival status) — https://doi.org/10.5281/zenodo.1043226

## Evaluation signals

- All badge endpoint URLs from the README are successfully retrieved (HTTP 200 or expected status code returned).
- Parsed status values are non-null and match the documented format for each badge service (e.g., 'passing'/'failing' for Travis CI, numerical score for Landscape.io, percentage for Coveralls).
- Retrieval timestamps are recorded in ISO 8601 format and are consistent and sequential across all badges in a single retrieval cycle.
- Tabulated results include all five badge types mentioned in the README (Travis CI, Landscape.io, Coveralls, Docker Hub, Zenodo) with no missing entries.
- Status values are consistent with live project status pages when independently verified through browser inspection or API documentation.

## Limitations

- Badge endpoint availability and response format may change without notice (e.g., service deprecation, API versioning).
- Some badge services (e.g., Landscape.io) may be deprecated or transitioned to alternative providers, rendering endpoints inaccessible.
- Parsing logic must be adapted per badge service, as response formats vary (SVG, JSON, plain text) and may not be machine-parseable by simple text extraction.
- Timestamps reflect only the moment of retrieval; they do not represent the time at which the underlying status was last updated by the badge service, which may introduce temporal misalignment.
- Rate limiting or IP-based blocking by badge endpoints may prevent frequent retrieval cycles or large-scale batch monitoring.

## Evidence

- [other] Five badge endpoints are identified in the MAGMa README: "Five badge endpoints are embedded in the MAGMa README: Travis CI (build status), Landscape.io (code health), Coveralls (test coverage), Docker Hub (container readiness), and Zenodo (DOI archival)"
- [readme] Badge URLs are embedded in reStructuredText README with live service links: ".. image:: https://travis-ci.org/NLeSC/MAGMa.svg?branch=master
    :target: https://travis-ci.org/NLeSC/MAGMa"
- [other] Workflow includes parsing and tabulation of endpoint responses: "For each badge endpoint, retrieve the current status value by accessing the endpoint URL and parsing the response (status field, numerical score, or version string as applicable). Tabulate the"
- [readme] Multiple badge services with distinct response types are used: ".. image:: https://landscape.io/github/NLeSC/MAGMa/master/landscape.svg?style=flat
    :target: https://landscape.io/github/NLeSC/MAGMa/master"
