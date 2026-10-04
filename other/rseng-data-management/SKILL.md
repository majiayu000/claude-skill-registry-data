---
name: rseng-data-management
description: >-
  Covers research data management around software: organizing and documenting
  datasets (layout, data dictionaries), keeping data out of git while
  versioning it properly (DVC, git-annex, DataLad), FAIR data and metadata
  standards, depositing data with DOIs in repositories such as Zenodo,
  licensing data, and handling sensitive or personal data. Use PROACTIVELY
  when a project reads or produces datasets, when the user asks where to put
  data, how to version or share large files, how to document a dataset, which
  data license or repository to use, or when data files are about to be
  committed to a code repository. (Format engineering - HDF5, NetCDF, Parquet,
  chunking - is rseng-scientific-file-formats; funder data management plans are
  rseng-data-management-plans.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Research data management for software projects

Most research software exists to turn input data into output data,
yet data is routinely the least managed part of the project: undocu-
mented CSVs, 2GB files in git, results nobody can regenerate. Treat
data as a first-class research output with the same care as code -
versioned, documented, licensed and citable. FAIR applies to data
even more directly than to software (rseng-fair-software covers the
software side; the principles at go-fair.org are the shared root).

## Project layout and the data/code boundary

- Separate raw, intermediate and final data explicitly - e.g.
  data/raw/, data/processed/, results/ - and treat raw data as
  READ-ONLY: nothing ever edits a raw file in place; all cleaning is
  scripted so the pipeline can regenerate everything downstream
  (rseng-workflows).
- Keep the mapping from data to code explicit: which script produces
  which file, recorded in the workflow or a Makefile, not in memory.
- Configuration, not hard-coded paths: data locations belong in a
  config file or environment variable so the project runs outside
  its author's laptop (rseng-reproducible-environments).

## Keeping data out of git - but versioned

Git is for text; repositories bloat permanently with every committed
binary revision. Before a large or binary data file lands in git,
intervene:

- Small, stable reference data (kilobytes, test fixtures) may live in
  the repository - that is fine and convenient.
- For everything else use a data versioning layer: DVC or git-annex
  track content by hash in git while the bytes live in ordinary
  storage; DataLad builds full dataset management on git-annex and is
  widespread in neuroscience and beyond. All three keep code and data
  revisions linked, which is the actual requirement: "which data did
  commit X use?" must have an answer.
- Published, frozen inputs are often best NOT copied at all: record
  the DOI or URL plus a checksum, and fetch in a scripted step.
- Git LFS exists but suits media assets better than evolving research
  data; hosting quotas bite and history stays coupled to one forge.

## Documenting a dataset

A dataset without documentation is a puzzle, not a resource. Minimum
per dataset:

- A README (or datasheet) stating: what the data is, how it was
  collected or generated, its units, coordinate systems and
  conventions, known limitations, license, and how to cite it.
- A data dictionary for tabular data: every column's name, type,
  units, allowed values and meaning. Generate it from the data where
  possible so it cannot drift silently.
- Formats: prefer open, well-specified formats (CSV with a stated
  dialect, Parquet, HDF5, NetCDF, domain standards) over proprietary
  ones; for domain metadata standards and format registries, point
  users to FAIRsharing and the ELIXIR RDMkit rather than inventing a
  schema ad hoc.

## Depositing, DOIs and citation

Data that supports a publication belongs in a data repository, not in
supplementary ZIPs or the code repo:

- Zenodo is the general-purpose default (free, DOI per version,
  versioned records); domain repositories are better when one exists -
  RDMkit and FAIRsharing list them per field.
- Give the dataset its own DOI and its own citation entry; link data
  DOI and software DOI both ways so each cites the other
  (rseng-citation-metadata, rseng-publishing-releasing).
- License the data explicitly - and note that code licenses do not
  fit data well: CC0 or CC-BY are the common choices for open data,
  while ODbL and domain-specific terms exist for databases
  (rseng-licensing). "No license" means "all rights reserved", for data
  exactly as for code.

## Sensitive and personal data

When data involves people, patients, protected locations or
commercial restrictions:

- Never commit sensitive data, even briefly - git history is forever
  and forges cache aggressively. Add ignore rules and pre-commit
  guards BEFORE the first sensitive file exists in the project.
- Keep sensitive data in the access-controlled storage the
  institution provides; the repository carries only synthetic or
  anonymized samples plus the code that ran on the real thing.
- Anonymization is a research task, not a rename: removing names is
  not de-identification. Route the user to their data steward or
  ethics board rather than improvising GDPR compliance.
- A data management plan (DMP) may already govern the project - ask;
  when one exists it decides storage, retention and sharing, and the
  software should implement it rather than contradict it. Writing and
  maintaining DMPs is rseng-data-management-plans.

## Records and transparency

When AI assistance produced or transformed datasets, record it in the
project's AI declaration - dataset entries are a supported content
type in aidecl.yaml (rseng-ai-declaration). Data provenance and AI
provenance are the same habit applied to different artifacts.

## Working with this skill

This skill is source-independent: its authority is the FAIR data
principles and the community resources linked below.

Learn more (verified):
  - https://www.gofair.foundation/fair-principles - the FAIR principles
  - https://rdmkit.elixir-europe.org - ELIXIR RDMkit, per-domain and
    per-task RDM guidance
  - https://fairsharing.org - registry of metadata standards and
    data repositories
  - https://zenodo.org - general-purpose data repository with DOIs
  - https://dvc.org - Data Version Control
  - https://www.datalad.org - DataLad dataset management

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - long-term data deposit
- rseng-citation-metadata - data DOIs and two-way citation
- rseng-data-management-plans - funder plan over the practice
- rseng-regulatory-compliance - sensitive and personal data obligations
- rseng-scientific-file-formats - choosing and engineering the format
- rseng-workflows - scripted regeneration of derived data

<!-- related-skills:end -->
