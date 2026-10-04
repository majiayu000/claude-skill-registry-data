---
name: rseng-documentation
description: >-
  Covers how to document research software at every level: writing a README,
  code-level docs (comments, docstrings, API and CLI help), project docs
  (INSTALL, CONTRIBUTING, LICENSE, CITATION, changelog), publishing hosted
  documentation with Read the Docs, and capturing a Research Software Story.
  Use when the user asks how to write or improve a README, decide what
  documentation their project needs, add docstrings or inline comments,
  document an API or CLI, set up Sphinx/MkDocs/Doxygen, host
  docs on Read the Docs, structure a docs site, or write the narrative context
  and history behind a project. For outward-facing papers, talks and
  announcements see rseng-science-communication; for public and citizen-science
  narrative see rseng-storytelling.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Documenting research software

Use this skill when creating or improving any documentation for research
software: a README, in-code comments and docstrings, API/CLI references,
project files like CONTRIBUTING or CHANGELOG, a hosted documentation site,
or a narrative Research Software Story. Good documentation makes software
understandable, reusable, and sustainable - it tells others (and your
future self) what the software does, how to use it, and how to contribute.

## Separate the two levels first

Decide which level the user needs before writing, because audience and
content differ:

- Project documentation - the software as a whole: purpose, audience,
  installation, usage, licensing, contribution. Lives in README, INSTALL,
  CONTRIBUTING, LICENSE, CITATION. Helps people use and adopt the software.
- Code documentation - how the code works internally: comments, docstrings,
  architecture notes, API references. Helps people develop, deploy, and
  sustain it.

Both matter; keep them consistent. Installation and usage often straddle
the line and serve users and developers alike, so link between the two
rather than duplicating.

Cross-cutting rules for all documentation:

- Keep it accessible, clear, consistent, and regularly updated; cover all
  key aspects and invite feedback. Outdated docs can be worse than none.
- Generate it automatically where possible and use standard formats:
  Markdown, reStructuredText, HTML, PDF, or a wiki.
- Store documentation in the repository and version-control it alongside
  the code so it moves through the same review workflow.

## Write a good README

The README is the entry point and the project's homepage on GitHub or
GitLab. Place it in the project root as plain text or Markdown so it ships
with the code. Aim for three qualities: understandability, usability, and
attribution.

Include these sections, adapting depth to the audience:

- Description - purpose and features of the software.
- Requirements - software and hardware needs (OS, interpreter version,
  extra services, infrastructure). Skip low-level library dependencies;
  express those through the language's own mechanism (e.g. requirements.txt).
- Installation - exhaustive, copy-pasteable commands assuming no prior
  knowledge; cover multiple install paths (library, Docker, script) if they
  exist, and link out for heavyweight prerequisites.
- Configuration - config-file fields and how to set them, when needed.
- Usage - every parameter/subcommand with worked examples; link to tutorials
  in other formats (video, notebook, PDF).
- Contribution - how to propose changes (pull requests, issues, standards).
- Acknowledgements - funders and contributors, per each institution's policy.
- Citation - how to cite, ideally mirroring a CITATION.cff file (e.g. BibTeX).
- License - state it explicitly; unlicensed software cannot legally be reused.

For research software also document how to reproduce or replicate the
experiments, add citation information, and describe links to related
publications and datasets.

Extra tactics: add badges for at-a-glance status (see the howfairis list);
run SOMEF to detect missing README parts (it flags gaps, it does not grade).
If AI assists in drafting a README, hold it to the same accuracy bar -
verify every command, requirement, and citation before publishing.

## Document the code

Match documentation type to purpose and audience - user, developer, and
deployment documentation each target different readers, so tailor content
accordingly; personas help.

Document as you code:

- Comments live in the source for people modifying the code; docstrings are
  visible to the outside world for people using it. Use both.
- Write comments and docstrings while coding so they stay current. Explain
  *why* and *how*, not a restatement of *what*. If code needs heavy
  commenting to be understood, rewrite the code instead.
- Lean on IDEs and extensions (autoDocstring, JSDoc) to scaffold docstrings.

Write meaningful error messages that state when and where the error
happened, what went wrong, the software state, and how to fix it or where
to look.

Include usage examples, a quickstart for a fast path to experimentation,
and a fuller step-by-step tutorial. Move examples to a dedicated section if
they clutter the main docs.

Document any CLI or API: describe usage, subcommands, options, arguments,
and environment variables with examples. Implement a `help` command so users
succeed without external docs. Tools: Click for Python CLIs, the OpenAPI
Specification and Swagger for REST APIs.

Automate generation from annotated source where you can:

- Sphinx (Python and more), Doxygen (C++ and more), Roxygen (R), JSDoc
  (JavaScript), Documenter.jl (Julia) extract docs from code comments into
  HTML/PDF.
- MkDocs builds Markdown documentation sites.
- Wire doc builds into CI (GitHub Actions, GitLab CI/CD) to publish updates
  automatically; Zenodo can archive docs with each release.

## Document the software project

Beyond the README, a well-documented project provides these root-level
files or clearly linked pointers:

- INSTALL - download and run steps (or a README section).
- LICENSE - legal conditions for use (see the licensing skill).
- CITATION - a CFF or text file stating how to cite (see the citation skill).
- CONTRIBUTING - how to get involved and submit changes.
- CODE_OF_CONDUCT - the collaboration norms for the community.
- AUTHORS/CONTRIBUTORS - who built it, inline or in a separate file.
- Pointers to deeper technical docs (API, deployment, architecture).
- Roadmap - current and planned work, or a link to the issue tracker.
- Changelog / release notes - notable changes between versions.

Organize it for the reader: identify the audience, state the purpose,
structure information logically, keep it current, make it easy to find and
navigate (e.g. GitHub Pages), and include enough detail - environment,
data, example workflows - for others to reproduce results.

A build story (docs/BUILD-STORY.md - the choices behind the project,
written as teaching material for new developers) rounds out the
developer docs from tier 2 up; rseng-trainer carries the practice.

Architecture, API and data-flow diagrams belong in the developer
docs as diagrams-as-code (Mermaid renders inline on forges and doc
sites; sources committed, exports regenerated) - what to draw and
how to keep it honest is rseng-software-design's diagram practice.

## Publish hosted documentation with Read the Docs

When a project needs a browsable docs site, generate static pages with
Sphinx or MkDocs and publish them. Read the Docs is a common host that
integrates with GitHub/GitLab and rebuilds via CI:

1. Create the source (`sphinx-quickstart` or `mkdocs new`) and push it
   with the code.
2. Import the repo on Read the Docs and add a `.readthedocs.yaml`
   (config version 2) at the repo root declaring the Python
   environment and the builder.
3. Wire webhooks/CI so pushes and pull requests trigger rebuilds;
   check build logs; docs appear at
   `https://<your-project>.readthedocs.io/`.

## Write a Research Software Story

A Research Software Story captures the context around a project rather than
how to run it: the scientific problem, the community, and the practices and
tools that sustain it - the who, what, why, where, when, and how. It helps
onboard newcomers, explains the project to leaders and funders, and, through
the act of writing, surfaces gaps the team had not noticed.

Guide the user through the template sections - the problem addressed, the
communities involved, the technical nature, dependencies, development
practices, onboarding, tooling, documentation/FAIR/openness, and
sustainability/governance. Emphasise clarity over technical depth; a reader
should grasp the project without reading the code. Any version-zero
draft counts - two or three sentences per section, written directly,
drawn out by interviewing a teammate through the template, or drafted
via interviewer-mode LLM prompting that prefers the interviewee's own
words and never invents missing facts. Refine afterward, checking that
processes are captured and linked tools and tutorials exist and work.

## Descriptive completeness: the full picture a stranger needs

Good project documentation answers every question a newcomer,
reviewer or future maintainer brings - check for ALL of these and
flag the gaps, proportionate to tier:

- Background and motivation: the research problem and statement of
  need in domain language - why anyone should care.
- Usage, end to end: install from clean environment, a quickstart
  that runs, worked examples on realistic data, configuration
  reference, troubleshooting, and stated limitations - what the
  software does NOT do is documentation too.
- Developer notes: architecture and key decisions (link ADRs), dev
  environment setup, running tests, release runbook, where help is
  wanted - the onboarding path from user to contributor.
- Alternatives: name neighboring tools and how this one differs or
  interoperates; "when NOT to use this, use X instead" earns more
  trust than silence about competitors.
- Provenance and status: citation, license, AI involvement
  disclosure, maintenance status and support expectations.

## Standards adherence for code and developer docs

Follow the ecosystem's documentation standard rather than
inventing style:

- Docstrings per the community convention: numpydoc or Google
  style in scientific Python (pick ONE and enforce it with the
  linter's docstring rules), roxygen2 in R, Doxygen conventions
  in C/C++ - the standard is what makes docs render correctly in
  the ecosystem's tooling and read familiarly to contributors.
- Structure the documentation set by function: the Diataxis
  framework's four quadrants - tutorials (learning), how-to
  guides (tasks), reference (information), explanation
  (understanding) - prevent the classic failure of one document
  trying to be all four and serving none. Label sections by
  quadrant when organizing or reviewing docs.
- Keep documented and actual behavior locked together: examples
  that run as tests (doctest-style or executable snippets in
  CI), API reference generated from the docstrings rather than
  maintained in parallel, and versioned docs matching released
  versions.

## Measuring documentation coverage

Documentation completeness can be measured, not just felt: docstring
coverage tools (interrogate for Python and equivalents elsewhere)
report the fraction of public functions, classes and modules that
carry documentation, and documentation coverage against community
conventions is an explicit quality indicator. Run it read-only
first, set a ratchet at the current value in CI so coverage cannot
regress, and target the PUBLIC surface - private helpers earn
docstrings when non-obvious, not by quota. The number locates gaps;
whether a given docstring actually helps remains a human judgment
(rseng-software-metrics covers the measurement discipline and its
gaming hazards).

## Working with this skill

The generated references.md beside this file lists the source material
and pointers.

Learn more (verified):
  - https://www.writethedocs.org/guide/ - Write the Docs
    documentation guide
  - https://diataxis.fr - Diataxis documentation framework
  - https://www.sphinx-doc.org - Sphinx documentation generator
  - https://www.mkdocs.org - MkDocs project documentation tool
  - https://docs.readthedocs.com - Read the Docs user documentation


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-citation-metadata - CITATION.cff beside the README
- rseng-licensing - LICENSE file guidance
- rseng-science-communication - outward papers and announcements
- rseng-storytelling - narrative for broad audiences
- rseng-user-support - recurring questions become docs
- rseng-ux-accessibility - docs readability and accessibility

<!-- related-skills:end -->
