---
name: rseng-software-publishing
description: >-
  Covers publishing research software through its distribution channels:
  packaging for and releasing on package indexes (PyPI, conda-forge, CRAN and
  ecosystem equivalents), registering in research software registries,
  submitting to software journals (JOSS-style), and choosing the channel mix
  for a project's audience. Use when the user wants their software installable
  by others, asks how to publish on PyPI, CRAN or conda-forge, wants the
  software listed where researchers search, or when a mature project is only
  obtainable by cloning its repository. (Cutting versioned releases and DOIs:
  rseng-publishing-releasing; the JOSS review process: rseng-software-peer-review;
  preservation: rseng-archiving.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Publishing research software

"Available on request" and "clone the repo" are not distribution.
Publishing puts software where its users already look - the package
index they install from, the registry they search, the journal that
tells them it was reviewed - and each channel has its own rules.
The neighboring skills own the mechanics this skill orchestrates:
rseng-publishing-releasing (versioned releases, changelogs, DOIs),
rseng-project-scaffolding (installable package structure),
rseng-software-peer-review (the JOSS process itself),
rseng-archiving (preservation). This skill is the channel strategy
and the index-specific craft.

## Choose the channel mix by audience

- Users who pip/conda/install: a package index is non-negotiable -
  it is the difference between a dependency and a science project.
- Researchers who search by domain: a Research Software Directory
  instance and domain registries (rseng-software-reuse lists them) -
  where discovery happens for people who do not know the package
  name.
- Reviewers, citers, funders: a software journal entry (JOSS-class)
  plus the archived, DOI'd release (rseng-archiving).

A healthy mature project typically has all three; a young one
starts with the index and adds the rest at first stable release.
State the recommended mix and why, then build it channel by
channel.

## Package indexes: the craft per ecosystem

Common core across ecosystems: complete metadata (description,
license, URLs, authors - the index page IS a landing page:
rseng-fair-software's findability applied), semantic versioning
(rseng-publishing-releasing), and automated publication from CI with
provenance rather than laptop uploads
(rseng-ci-cd, rseng-security's trusted-publishing staircase).

- PyPI (Python): modern pyproject.toml packaging per the PyPA
  guide (rseng-project-scaffolding's template does this); test on
  TestPyPI first; use trusted publishing from CI; wheels plus
  sdist; never delete released versions - yank instead.
- conda-forge: the community channel for the scientific stack and
  the path when binaries/native deps matter (rseng-hpc-computing
  users often live here); publication is a recipe PR to
  staged-recipes, then a feedstock you maintain - it is a
  community process with reviewers, not an upload.
- CRAN (R): the strictest gate - read the repository policies
  before submitting; R CMD check --as-cran must pass cleanly on
  multiple platforms, submissions are human-reviewed, and policy
  violations get packages archived. rOpenSci's guide (and its
  review - rseng-software-peer-review) is the community on-ramp.
- Other ecosystems follow the same shape (npm, crates.io, Julia
  General registry): find the community's packaging guide, meet
  its gate, automate the release.

Version-support policy belongs to publishing: which language/
dependency versions you support, tested in CI matrices, stated in
metadata (rseng-maintenance-sustainability owns the deprecation
half).

## Registries: be found by field, not name

Register at first citable release, and keep entries alive:

- RSD instances harvest most metadata from the repository when
  CITATION.cff and codemeta.json exist (rseng-citation-metadata) -
  the entry is cheap if the metadata hygiene is there.
- Update triggers: new major release, changed maintainership,
  publication of the software paper - a stale registry entry
  pointing at a moved repository is worse than none.
- Link everything: registry entry <-> index page <-> repository <->
  paper DOI <-> archive - the same both-ways discipline as
  rseng-archiving and rseng-open-science-practices.

## The publication checklist

Before announcing any channel as live, verify as a user would:

1. Fresh-environment install from the index succeeds
   (rseng-reproducible-environments provides the clean room).
2. Index page renders correctly - description, links, license,
   badges.
3. Import/run smoke test passes on the installed (not cloned)
   artifact.
4. Citation instructions resolve (CITATION.cff shipped, DOI live).
5. The announcement is drafted (rseng-science-communication) and the
   aidecl.yaml reflects AI involvement in the release
   (rseng-ai-declaration).

## Working with this skill

This skill is source-independent: its authority is the packaging
guides and index policies linked below. It orchestrates the
channel-specific end of the publishing chain.

Learn more (verified):
  - https://packaging.python.org - Python Packaging User Guide
  - https://pypi.org - PyPI
  - https://conda-forge.org - conda-forge
  - https://cran.r-project.org/web/packages/policies.html - CRAN
    repository policies
  - https://devguide.ropensci.org - rOpenSci packaging guide
  - https://joss.theoj.org - Journal of Open Source Software
  - https://research-software-directory.org - Research Software
    Directory

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ci-cd - trusted publishing from CI
- rseng-citation-metadata - registries harvest CITATION.cff/codemeta
- rseng-project-scaffolding - installable package structure
- rseng-publishing-releasing - release mechanics behind each channel
- rseng-reproducible-environments - fresh-install verification clean room
- rseng-software-peer-review - JOSS submission pathway

<!-- related-skills:end -->
