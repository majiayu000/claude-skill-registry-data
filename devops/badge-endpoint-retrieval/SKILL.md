---
name: badge-endpoint-retrieval
description: Use when when you need to verify the current operational status of a software project across multiple dimensions (CI/CD, code quality, test coverage, containerization, archival) and those status indicators are exposed as badge endpoints in the project's README.
license: CC-BY-4.0
metadata:
  edam_topics: []
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

# badge-endpoint-retrieval

## Summary

Retrieve and parse live status indicators from badge endpoints embedded in a project README to obtain current build, code quality, test coverage, deployment, and archival status. This skill enables reproducible capture of project health metrics at a specific point in time.

## When to use

When you need to verify the current operational status of a software project across multiple dimensions (CI/CD, code quality, test coverage, containerization, archival) and those status indicators are exposed as badge endpoints in the project's README. Use this skill when creating a snapshot of project health metrics or auditing the availability and correctness of status reporting infrastructure.

## When NOT to use

- When the project README contains no embedded badges or status endpoint references.
- When you require historical badge status data; badge endpoints report only current state, not time-series history.
- When the project's status infrastructure is known to be deprecated or the badges are stale placeholders not actively maintained.

## Inputs

- GitHub repository URL (e.g., https://github.com/NLeSC/MAGMa)
- Project README file (reStructuredText or Markdown format)
- Badge endpoint URLs embedded in README (Travis CI, Landscape.io, Coveralls, Docker Hub, Zenodo)

## Outputs

- Structured table with columns: badge name, endpoint URL, retrieved status value, retrieval timestamp
- JSON or CSV record of live badge status snapshot
- Validation report indicating which badge endpoints are responsive and which are unavailable

## How to apply

Locate the target repository's README file and identify all badge image URLs and their corresponding target links (typically embedded as reStructuredText or Markdown image syntax). For each badge endpoint—such as Travis CI build status, Landscape.io code quality, Coveralls test coverage, Docker Hub container readiness, and Zenodo DOI archival—construct an HTTP request to retrieve the badge endpoint URL. Parse the response to extract the status value (e.g., 'passing' or 'failing' for CI badges, numerical health scores for code quality, version strings for archival badges). Record each retrieval result with its endpoint URL, parsed status value, and timestamp. The rationale is that badges are live indicators pointing to authoritative status pages; by querying the endpoint directly rather than relying on cached or displayed values, you obtain the most current state of the project's operational health across its full technology stack.

## Related tools

- **Travis CI** (Provides build status badge endpoint for continuous integration) — https://travis-ci.org/NLeSC/MAGMa
- **Landscape.io** (Provides code health and quality badge endpoint) — https://landscape.io/github/NLeSC/MAGMa/master
- **Coveralls** (Provides test coverage badge endpoint) — https://coveralls.io/r/NLeSC/MAGMa
- **Docker Hub** (Provides container readiness status badge) — https://hub.docker.com/r/nlesc/magma
- **Zenodo** (Provides DOI archival badge endpoint with version metadata) — https://zenodo.org/badge/DOI/10.5281/zenodo.1043226.svg

## Examples

```
curl -s https://travis-ci.org/NLeSC/MAGMa.svg?branch=master | grep -oP '(?<=<text.*?>)[^<]+' | head -1
```

## Evaluation signals

- All badge endpoint URLs identified in the README are successfully retrieved (HTTP 200 or 304 response) and not broken links.
- Each badge endpoint response contains a parseable status field or numerical value matching the expected badge type (e.g., 'passing'/'failing' for CI, health score 0–10 for code quality, percentage for coverage).
- Timestamps recorded for each retrieval fall within a narrow window (seconds to minutes apart), confirming a synchronized snapshot capture.
- Status values retrieved from badge endpoints are consistent with the live status pages they link to (e.g., Travis CI badge status matches the repository's Travis CI page).
- Tabulated results include all five badge types documented in the README (Travis CI, Landscape.io, Coveralls, Docker Hub, Zenodo) or explicitly justify any omissions.

## Limitations

- Badge endpoints may rate-limit or block automated requests; retrieval may fail if called too frequently without appropriate delays or user-agent headers.
- Some badge providers return SVG images rather than machine-readable JSON; parsing requires image metadata extraction or follow-through to the linked status page.
- Badge endpoints reflect only the most recent build or quality scan; they do not provide historical trends or explain *why* a status changed.
- The MAGMa README contains no changelog documentation, limiting context for interpreting sudden status changes across badge endpoints.

## Evidence

- [other] Five badge endpoints are embedded in the MAGMa README: Travis CI (build status), Landscape.io (code health), Coveralls (test coverage), Docker Hub (container readiness), and Zenodo (DOI archival), each linking to live project status pages.: "Five badge endpoints are embedded in the MAGMa README: Travis CI (build status), Landscape.io (code health), Coveralls (test coverage), Docker Hub (container readiness), and Zenodo (DOI archival),"
- [other] For each badge endpoint, retrieve the current status value by accessing the endpoint URL and parsing the response (status field, numerical score, or version string as applicable).: "For each badge endpoint, retrieve the current status value by accessing the endpoint URL and parsing the response (status field, numerical score, or version string as applicable)."
- [other] Identify all badge endpoint URLs embedded in or referenced by the README (Travis CI build status, Coveralls code coverage, Landscape.io code quality, Docker Hub image status, Zenodo DOI badge).: "Identify all badge endpoint URLs embedded in or referenced by the README (Travis CI build status, Coveralls code coverage, Landscape.io code quality, Docker Hub image status, Zenodo DOI badge)."
- [other] Tabulate the results in a structured table with columns for badge name, endpoint URL, retrieved status value, and timestamp of retrieval.: "Tabulate the results in a structured table with columns for badge name, endpoint URL, retrieved status value, and timestamp of retrieval."
- [readme] image:: https://travis-ci.org/NLeSC/MAGMa.svg?branch=master: "image:: https://travis-ci.org/NLeSC/MAGMa.svg?branch=master"
- [readme] image:: https://landscape.io/github/NLeSC/MAGMa/master/landscape.svg?style=flat: "image:: https://landscape.io/github/NLeSC/MAGMa/master/landscape.svg?style=flat"
- [readme] image:: https://coveralls.io/repos/NLeSC/MAGMa/badge.svg?branch=master: "image:: https://coveralls.io/repos/NLeSC/MAGMa/badge.svg?branch=master"
- [readme] image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1043226.svg: "image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1043226.svg"
