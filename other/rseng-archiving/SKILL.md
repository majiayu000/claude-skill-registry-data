---
name: rseng-archiving
description: >-
  Covers long-term archiving of research software and data: Software Heritage
  save requests and SWHID persistent identifiers, Zenodo deposits with
  versioned DOIs and forge integration, choosing domain and institutional
  repositories, deciding what to archive (code, data, environments,
  documentation) and when, and archiving at project retirement. Use when the
  user wants software or data preserved beyond the life of a forge account,
  grant or lab, mentions Software Heritage, SWHIDs, Zenodo deposits or
  archiving, retires or hands over a project, prepares artifacts that must
  stay resolvable for a paper, or when funder policy requires long-term
  preservation. (Cutting the release itself is rseng-publishing-releasing;
  day-to-day data storage and repository choice is rseng-data-management.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Archiving research software and data

A git forge is a workspace, not an archive: repositories get
renamed, deleted, force-pushed and orphaned, and a URL in a paper
has a half-life. Archiving puts an immutable, independently hosted,
persistently identified copy of the work somewhere designed to
outlive projects, labs and platforms. It is cheap (minutes per
release), and it is what makes "the code is available" true in ten
years. Distinct roles: rseng-publishing-releasing covers making
releases; this skill covers making them permanent.

## The two-pillar default

For any research software worth citing, do both - they solve
different problems:

- Software Heritage archives the SOURCE HISTORY: submit a save
  request for the repository (web form or API - no account needed)
  and the full history is preserved in the universal archive.
  Every commit, directory and file gets an intrinsic SWHID
  (persistent, content-derived, verifiable) that resolves at
  archive.softwareheritage.org regardless of what happens to the
  forge. Re-save at releases; heavily referenced repos are also
  crawled automatically, but an explicit save is a guarantee.
- Zenodo archives the RELEASE ARTIFACT with a citable DOI: deposit
  the release tarball (the forge integration can do this
  automatically per release), get a version DOI plus a concept DOI
  covering all versions, and wire the DOI back into
  CITATION.cff and the README (rseng-citation-metadata). Zenodo is
  CERN-backed and free for research outputs.

SWHID vs DOI in one line: the SWHID identifies the exact source
content (verifiable by hash), the DOI identifies the published
release object (citable in references) - papers benefit from both.

## What to archive

An archive that cannot be understood is storage, not preservation.
Per archived release:

- The source at the released tag (both pillars above).
- The data needed to reproduce headline results, or scripted
  retrieval with checksums when data lives in its own repository
  (rseng-data-management owns data-repository choice; deposit data
  in domain archives where one exists, Zenodo otherwise).
- The environment specification - lockfiles, container recipe -
  and where feasible a container image; bytes rot slower than
  dependency graphs (rseng-reproducible-environments).
- README, license, citation metadata and a manifest tying it
  together (the research-compendium shape from
  rseng-reproducibility maps directly onto a good deposit).
- Rich deposit metadata: creators with ORCIDs, description,
  keywords, related identifiers (paper DOI, software DOI, SWHID) -
  metadata is what makes the archive findable
  (rseng-fair-software).

## When to archive

- At every citable release: automate it (forge-to-Zenodo webhook +
  a save request in the release pipeline - rseng-ci-cd makes both a
  release-time step).
- Before things end: grant end, maintainer departure, lab closure,
  platform migration - archive FIRST, then wind down
  (rseng-legacy-code's retire path and
  rseng-maintenance-sustainability's succession planning both
  terminate here).
- Before risky history operations: a save request costs nothing
  and preserves the pre-rewrite state.
- On publication: the artifact a paper cites must be the archived,
  DOI'd version, not a branch (rseng-reproducibility's replication
  packages; journals' availability policies increasingly require
  archival deposit explicitly).

## Choosing repositories beyond the default

- Domain repositories first for DATA when the field has one -
  community metadata standards and audiences live there; registries
  like the ones rseng-fair-software points to list them.
- Institutional repositories: use when policy requires; check they
  issue persistent identifiers and have a preservation commitment.
- Trust marks: CoreTrustSeal certification signals a repository
  with audited preservation practices - prefer certified archives
  for irreplaceable data.
- What NOT to trust as an archive: forge releases alone, lab web
  servers, cloud buckets on a grant credit card, supplementary-
  material ZIPs at publishers.

## Verify the archive

Archiving unverified is hoping: resolve the DOI and the SWHID,
download the deposit fresh, and check the artifact matches the
release (checksums). Record identifiers in the repository (README
badges, CITATION.cff, aidecl.yaml provenance where AI contributed -
rseng-ai-declaration) so the archived and living copies point at each
other.

## Working with this skill

This skill is source-independent: its authority is the Software
Heritage, SWHID and Zenodo documentation linked below. It is the
preservation end of the publishing chain
(rseng-publishing-releasing -> rseng-archiving).

Learn more (verified):
  - https://archive.softwareheritage.org - Software Heritage
    archive (save code, browse, SWHID resolution)
  - https://www.swhid.org - SWHID identifier specification
  - https://zenodo.org - Zenodo
  - https://help.zenodo.org - Zenodo documentation (deposits,
    forge integration, versioned DOIs)
  - https://www.coretrustseal.org - CoreTrustSeal certified
    repositories
    task page on archiving software

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-citation-metadata - wire DOIs into citation files
- rseng-data-management - domain data repository choice
- rseng-legacy-code - retire path terminates in archive
- rseng-maintenance-sustainability - succession and wind-down archiving
- rseng-publishing-releasing - archive every citable release
- rseng-reproducible-environments - environment capture inside deposits

<!-- related-skills:end -->
