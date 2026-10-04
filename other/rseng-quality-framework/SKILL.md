---
name: rseng-quality-framework
description: >-
  The entry point and router for this pack: explains the research software
  quality framework - community-standard quality dimensions, measurable
  indicators and the three-tier model (analysis code, prototype tools,
  infrastructure) - and routes to the right companion rseng-* skill. Use
  PROACTIVELY at the start of any research software task to classify the
  software's tier and select which practices apply, and whenever the user asks
  what research software quality means, mentions quality dimensions,
  indicators or the three-tier model, wants a quality assessment or
  improvement plan for research software, or is unsure which quality practice
  to start with.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Research software quality framework

This skill is the entry point to the pack. It explains a community-standard
framing of research software quality and points to the specialised
sibling skills for concrete tasks. Ground every quality discussion in two
questions: what tier of software is this, and which quality dimensions
matter for it right now.

## The three-tier view

Classify the software before recommending practices; expectations scale
with intent, not with code size.

- Tier 1, analysis code: scripts and notebooks capturing a computational
  method for a paper or dataset, often single-author. Quality floor:
  version control, a README stating purpose and how to run, a pinned
  environment, a license, and a citation entry.
- Tier 2, prototype tools: software demonstrating a method for use beyond
  its origin project, multiple users or contributors. Add: tests with CI,
  structured documentation, releases with versioning, contribution notes.
- Tier 3, research software infrastructure: services, libraries and
  frameworks that communities depend on. Add: governance, review process,
  security and maintenance policy, sustainability planning, archiving.

Software moves between tiers; when analysis code starts being reused,
recommend upgrading its practices tier by tier rather than all at once.

## Quality dimensions

The framework defines 13 quality dimensions, formally published as a JSON-LD
registry (https://w3id.org/everse/rsqd). Always take names and counts from
the registry, not from page prose:

community, compatibility, FAIRness, flexibility, functional suitability,
interaction capability, maintainability, open source software, performance
efficiency, reliability, safety, security, sustainability.

Dimensions are qualitative categories, built on the ISO/IEC 25010 top-level
characteristics and extended for research software. Use them to structure
an assessment conversation, not as a scoring rubric.

## Quality indicators

Each dimension is backed by measurable indicators from the companion
registry (https://w3id.org/everse/rsqi); 47 indicators are defined at the
pinned upstream version, such as software_has_tests, has_ci-tests,
software_has_license, software_has_citation and archived_in_software_heritage.
The browsable dimension and indicator tables are published at
(https://everse.software/indicators/website/indicators.html and
.../dimensions.html). Indicators are proxies: passing them is evidence
of quality, not proof.

### Running an indicator-based assessment

When asked to "check quality" or assess a repository, run a structured
pass rather than an impression:

1. Establish the tier first (above) - roughly a third of the
   indicators are not applicable to analysis code, and reporting them
   as failures demoralizes rather than helps.
2. Walk the indicators per dimension and mark each met / unmet /
   not-applicable-for-tier, with one line of evidence per verdict
   (the file, badge, workflow or record that proves it).
3. Route every unmet indicator to the sibling skill that fixes it
   (the dimension map below); the quantitative cluster - complexity,
   duplication, cohesion/coupling, churn, maintainability index, size
   and documentation-coverage conventions - is measured by
   rseng-software-metrics.
4. Deliver as a prioritized improvement plan, cheapest-first within
   the tier's expectations, not as a scorecard - and rerun after
   fixes to report the delta (the same assess-fix-reassess loop as
   rseng-fairguard).

### Dimension-to-skill map

- Community: rseng-community-governance, rseng-science-communication
- Compatibility: rseng-scientific-file-formats,
  rseng-reproducible-environments
- FAIRness: rseng-fair-software, rseng-fairguard, rseng-citation-metadata,
  rseng-fair-ml
- Flexibility: rseng-software-design, rseng-reproducible-environments
- Functional suitability: rseng-testing, rseng-defensive-coding
- Interaction capability: rseng-ux-accessibility
- Maintainability: rseng-code-quality, rseng-software-metrics,
  rseng-software-design, rseng-maintenance-sustainability
- Open source software: rseng-licensing, rseng-license-compliance,
  rseng-community-governance
- Performance efficiency: rseng-performance-profiling,
  rseng-gpu-computing, rseng-big-data-processing
- Reliability: rseng-testing, rseng-debugging, rseng-defensive-coding
- Safety: no dedicated skill - for software whose failure can harm
  people or property, flag it and route to domain safety processes
- Security: rseng-security, rseng-agent-security,
  rseng-regulatory-compliance
- Sustainability: rseng-maintenance-sustainability, rseng-archiving,
  rseng-green-computing, rseng-management-planning

## The software life cycle

Quality practices attach to life-cycle stages: planning, development,
testing, release, maintenance, retirement. When the
user is at a specific stage, prefer stage-appropriate advice - a retirement
conversation is about archiving and handover, not about adding CI.

## Role-based entry points

Match advice to who is asking: researcher who codes (version control,
README, pinned environment, basic tests first; grow from there),
research software engineer (full engineering practice), principal
investigator (management plans, credit policy, sustainability and
staffing), project manager (milestones tied to releases, quality
gates, maintenance backlog), policy maker (software as a recognized
research output), trainer (curricula from the task pages, Carpentries
and CodeRefinery style).

## Which sibling skill to use

Route concrete tasks to the specialised skill:

<!-- skill-directory:start (generated - do not edit by hand) -->

Core engineering:
- rseng-testing: how to test research software
- rseng-ci-cd: continuous integration and delivery for research software
- rseng-code-quality: writing readable research code and structuring software projects
- rseng-software-design: designing research software
- rseng-defensive-coding: defenses against silently wrong research results
- rseng-debugging: systematic debugging of research software
- rseng-version-control-review: using version control effectively for research software and the PR-time review process
- rseng-software-metrics: measuring code health quantitatively
- rseng-pair-programming: the agent as an effective pair programmer and pull-request review buddy for research software
- rseng-code-review: reviewing existing code and whole projects, not just new diffs
- rseng-project-scaffolding: starting research software projects from maintained templates and keeping them in sync

Reproducibility and workflows:
- rseng-reproducible-environments: making research software environments reproducible
- rseng-reproducibility: end-to-end computational reproducibility
- rseng-workflows: building, choosing, discovering, describing, and sharing computational workflows with workflow management...
- rseng-provenance: capturing and packaging the provenance of software and data
- rseng-notebooks: engineering discipline for computational notebooks

Research data:
- rseng-data-management: research data management around software
- rseng-scientific-file-formats: choosing and handling scientific data formats in code
- rseng-big-data-processing: processing research data that outgrows one machine's memory
- rseng-data-management-plans: data management plans (DMPs) for research projects

Numerics and performance:
- rseng-numerical-accuracy: floating-point correctness in research code
- rseng-performance-profiling: making research code faster with evidence
- rseng-gpu-computing: GPU and accelerator programming for research software
- rseng-hpc-computing: working effectively on high-performance computing clusters

Publishing, credit and reuse:
- rseng-publishing-releasing: the release lifecycle of research software
- rseng-software-publishing: publishing research software through its distribution channels
- rseng-archiving: long-term archiving of research software and data
- rseng-citation-metadata: making research software citable and contributors credited
- rseng-citation-hygiene: verifying that every citation is real, correct and current
- rseng-licensing: how to license research software
- rseng-license-compliance: license compliance engineering
- rseng-fair-software: how to apply the FAIR principles - findable, accessible, interoperable, reusable - to research software...
- rseng-fair-ml: applying FAIR principles to machine learning artifacts
- rseng-fairguard: assessing research software against the 17 FAIR4RS principles with FAIRGuard (https://www.fairguard.org)
- rseng-software-reuse: discovering and reusing existing research software instead of rebuilding it...
- rseng-discovery: discovering the research landscape around a topic or project
- rseng-dependency-management: the full lifecycle of third-party dependencies
- rseng-software-peer-review: community peer review of research software
- rseng-open-science-practices: the researcher-facing open science workflow

Integrity, security and compliance:
- rseng-security: securing research software and its supply chain
- rseng-agent-security: operating AI coding agents securely
- rseng-regulatory-compliance: checking research code and data against data-protection and AI regulation
- rseng-research-integrity: integrity checks on research outputs before submission or release
- rseng-fact-checking: verifying facts and sources at the content level
- rseng-honesty: responding when concealment or misrepresentation is requested
- rseng-human-verification: the human's side of AI-assisted research software
- rseng-ai-declaration: declaring AI involvement with the AI Declaration Format (https://ai-declaration.org)

Community and people:
- rseng-community-governance: building and governing a community around research software
- rseng-community-metrics: measuring community health with CHAOSS-style metrics
- rseng-contributor-onboarding: turning users into contributors and contributors into regulars
- rseng-user-support: running user support as an operation for research software
- rseng-trainer: teaching research software skills while working

Communication and interfaces:
- rseng-documentation: how to document research software at every level
- rseng-science-communication: communicating research software outward to research audiences
- rseng-storytelling: telling the story of research data, software and projects to broad audiences
- rseng-ux-accessibility: user experience and accessibility for research software

Planning and operations:
- rseng-management-planning: planning research software work
- rseng-project-kickoff: starting a new research software project with a short kickoff interview
- rseng-project-tracking: the operational side of running a research software project
- rseng-lessons-learned: capturing and reusing what a project learns
- rseng-maintenance-sustainability: keeping research software alive and responsible over time
- rseng-green-computing: the environmental footprint of research computing

Specialized:
- rseng-language-guides: language-specific research software practice
- rseng-legacy-code: working safely with inherited research code
- rseng-open-source-migration: migrating research code from commercial, license-bound platforms to open source alternatives
- rseng-scientific-visualization: visualization of scientific data beyond publication figures

<!-- skill-directory:end -->
## Working with this skill

- references.md - source citations and links to the upstream framework pages

Learn more (verified):
  - https://everse.software/RSQKit/ - Research Software Quality Kit
  - https://www.bestpractices.dev - OpenSSF Best Practices badge
    program
  - https://fair-software.eu - five recommendations for FAIR software
  - https://guide.esciencecenter.nl - Netherlands eScience Center guide
  - https://book.the-turing-way.org - The Turing Way handbook

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-fair-software - FAIRness dimension practice
- rseng-fairguard - FAIR assess-fix-reassess sibling loop
- rseng-management-planning - tier drives plan rigor
- rseng-project-kickoff - new projects pair tiering with interview
- rseng-software-metrics - quantitative indicator measurement
- rseng-testing - most common first unmet indicator

<!-- related-skills:end -->
