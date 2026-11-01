---
name: build-system-monitoring
description: Use when when you need to capture a snapshot of a research software project's health metrics from multiple CI/CD and repository services (Travis CI, Landscape.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
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
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
- doi: 10.5281/zenodo.1043226
  title: ''
- doi: 10.5281/zenodo.1043226.svg
  title: ''
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma
schema_version: 0.2.0
---

# build-system-monitoring

## Summary

Retrieves and tabulates the current status of project health indicators (build, code quality, test coverage, deployment, and archival badges) from live CI/CD and service endpoints embedded in a repository README. This skill enables reproducible documentation of project status at a point in time.

## When to use

When you need to capture a snapshot of a research software project's health metrics from multiple CI/CD and repository services (Travis CI, Landscape.io, Coveralls, Docker Hub, Zenodo), either to validate claims in documentation or to establish a baseline for monitoring project maintenance state over time.

## When NOT to use

- Project repositories do not embed CI/CD or service badges in their README.
- Endpoints are behind authentication walls or have no public API response format.
- You only need real-time monitoring (not a one-time snapshot); use the service dashboards directly instead.

## Inputs

- GitHub repository URL
- README file content containing embedded badge image URLs and target endpoint links

## Outputs

- Structured status table with columns: badge name, endpoint URL, status value, timestamp
- CSV or tabular format suitable for archival and time-series comparison

## How to apply

Locate the README file in the target repository (e.g., https://github.com/NLeSC/MAGMa) and identify all badge image URLs and their target endpoints. For each badge, extract the endpoint URL (Travis CI build status, Landscape.io code health, Coveralls test coverage, Docker Hub container readiness, Zenodo DOI archival). Retrieve the current status value by accessing each endpoint URL and parsing the response for the status field (pass/fail for build, numerical score for code quality, percentage for coverage, version string for Docker, or DOI metadata for Zenodo). Record each result with badge name, endpoint URL, retrieved status value, and retrieval timestamp. Tabulate results in a structured format (CSV or table) to enable time-series comparison and validation against README claims.

## Related tools

- **Travis CI** (Source of build status badge and live CI/CD status endpoint) — https://travis-ci.org/NLeSC/MAGMa
- **Landscape.io** (Source of code health/quality badge endpoint) — https://landscape.io/github/NLeSC/MAGMa/master
- **Coveralls** (Source of test coverage percentage badge endpoint) — https://coveralls.io/r/NLeSC/MAGMa?branch=master
- **Docker Hub** (Source of container image readiness badge endpoint) — https://hub.docker.com/r/nlesc/magma
- **Zenodo** (Source of DOI and archival badge endpoint) — https://doi.org/10.5281/zenodo.1043226

## Evaluation signals

- All five badge endpoints (Travis CI, Landscape.io, Coveralls, Docker Hub, Zenodo) are successfully retrieved and return parseable status values.
- Tabulated status values match the live badge display shown in the GitHub README when compared at the same timestamp.
- Each row in the output table contains non-empty values for badge name, endpoint URL, status value, and retrieval timestamp.
- Status values conform to expected formats (e.g., 'passing'/'failing' for build, 0–100 for coverage percentage, semantic version for Docker).
- Retrieval timestamps are recorded within the same minute to ensure synchrony across endpoints.

## Limitations

- Badge endpoints may be temporarily offline or deprecated, causing retrieval failures.
- Some endpoints may return HTML badge images rather than machine-readable JSON/XML, requiring additional parsing logic.
- Status values are a snapshot and do not capture historical trends; repeated runs are needed for time-series analysis.
- Docker Hub and Zenodo badges in the MAGMa README use generic or static badge SVGs that may not reflect real-time changes in the underlying services.

## Evidence

- [other] Five badge endpoints referenced in task_002: "Five badge endpoints are embedded in the MAGMa README: Travis CI (build status), Landscape.io (code health), Coveralls (test coverage), Docker Hub (container readiness), and Zenodo (DOI archival)"
- [other] Workflow for badge endpoint retrieval: "For each badge endpoint, retrieve the current status value by accessing the endpoint URL and parsing the response (status field, numerical score, or version string as applicable)"
- [readme] README contains live badge links: ".. image:: https://travis-ci.org/NLeSC/MAGMa.svg?branch=master
    :target: https://travis-ci.org/NLeSC/MAGMa"
- [readme] Zenodo DOI badge in README: ".. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1043226.svg
   :target: https://doi.org/10.5281/zenodo.1043226"
- [other] Expected output structure: "Tabulate the results in a structured table with columns for badge name, endpoint URL, retrieved status value, and timestamp of retrieval"
