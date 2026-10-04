---
name: rseng-management-planning
description: >-
  Covers planning research software work: writing and maintaining a Software
  Management Plan (SMP), and choosing programming languages, tools, and
  infrastructures for a project. Use when the user wants to write or review an
  SMP, plan how software will be developed, maintained, shared, and preserved,
  needs the software sections of a proposal or funder template, wants to
  decide which language or framework to start a project in (Python, C++, R,
  Julia, Rust, Fortran, JavaScript), pick a project template or boilerplate,
  or weigh reuse, sustainability, and funder requirements at the start of a
  project. (Data management plans, maDMPs, DS-Wizard and DMPonline are
  rseng-data-management-plans; interactive new-project setup is
  rseng-project-kickoff; week-to-week task tracking is rseng-project-tracking.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Planning research software: management plans and technology choice

Use this skill at the start of a research software project, or whenever a
project's direction needs to be captured or revisited: drafting a Software
Management Plan (SMP), reviewing one against community standards, or choosing
the language, frameworks, and infrastructures to build on. It covers management
planning and technology choice.
Tailor the rigor to the software's type and intended lifespan - do not push a
throwaway prototype through the full governance apparatus of long-lived
infrastructure.

## What a Software Management Plan is

An SMP is a living document that plans how software will be developed,
maintained, shared, and preserved, capturing key decisions early and updating
them as the project evolves. Frame it
to the user as guidance embedded in the process, not a one-off deliverable.

It exists to serve five concerns; name the ones that matter for the project:

- Reproducibility and reusability: the software can be reliably reproduced,
  verified, and reused by others.
- Funding and milestones: funders can see the development strategy and track
  progress against it.
- Community standards and best practices: code review, continuous
  integration, testing, documentation standards, and FAIR4RS principles are
  planned in, not bolted on.
- Accessibility: the software is discoverable, accessible, and usable by the
  wider research community.
- Credit and impact: how contributors are acknowledged (citation files,
  ORCID, authorship), how usage is tracked, and how impact is evaluated.

## Tailor the SMP to the software (do this first)

Not all software is created equal.
Before drafting sections, classify the software and set its priorities:

- Place it on the pack's three-tier view: exploratory analysis code, reusable
  research software, or long-lived research software infrastructure. Higher
  tiers warrant more rigor, formality, and investment.
- Set the primary quality goals from the tier. For analysis code, prioritise
  reproducibility, transparency, and provenance. For infrastructure,
  prioritise robustness, scalability, security, and long-term maintenance.
- Make these priorities explicit in the plan so the team spends effort where
  it delivers the most value, rather than applying every practice uniformly.
- Check for external constraints early: institutional policy, national
  guidelines, or funder requirements often dictate the required level of
  detail and may mandate open release.

## SMP section checklist

A plan should systematically cover these foundational aspects. Walk them in order when drafting or
reviewing, and record decisions rather than intentions:

1. General information: what the software does, who owns it, its scope and
   intended longevity.
2. Collaboration and licensing: contribution model, governance, and license
   choice (defer license specifics to the licensing skill).
3. Analysis: requirements and the problem the software addresses.
4. Design: architecture and key technical decisions.
5. Implementation: coding standards, secure development workflow, and the
   languages and tools chosen (see the technology-choice rules below).
6. Testing and quality assurance: automated testing, continuous integration,
   and code review.
7. Deployment and delivery: how the software reaches its users.
8. Versioning and releases: versioning scheme, release cadence, archiving.
9. Long-term maintenance: resource needs, governance model, and contingency
   plans - succession of maintainers, deprecation and end-of-life strategy.
10. Credit, accessibility, and impact: citation, discoverability, registries,
    and how impact is measured and communicated.

Two cross-cutting checks:

- Engage all relevant stakeholders - architects, developers, researchers,
  legal advisors, community managers - so responsibilities are shared and
  understood and the plan is actually adopted. Consider user support,
  documentation, community contributions, onboarding, and governance.
- Plan for integration with development platforms (GitHub, GitLab) and
  research registries and archives (Software Heritage, Zenodo, bio.tools,
  OpenEBench) so the plan is straightforward to put into practice.

## Keep the SMP alive

Treat the SMP as a living document, not a start-of-project formality:

- Revisit it at lifecycle transitions and whenever a major decision changes.
- Prefer a tool that produces both human-readable output (for stakeholders
  and reviewers) and machine-actionable output (for automated workflows,
  metadata extraction, or compliance checks) when the project needs it.
- Build on established templates and checklists rather than inventing a
  format - the ELIXIR SMP template and the Software Management Wizard offer
  guided, low-barrier starting points; the SSI checklist helps evaluate
  coverage. See references.md for the vetted set.

## Machine-actionable SMPs and platform workflows

SMPs are becoming structured data, not prose PDFs. When the user's
institution runs a planning platform, draft THERE (or produce
paste-ready content): the Data Stewardship Wizard builds plans from
questionnaire knowledge models and exports funder formats plus
machine-actionable output; DMPonline carries the major funder
templates whose software sections an SMP feeds. A structured plan is
checkable - promised repositories can be diffed against actual
deposits, promised licenses against LICENSE files, promised archiving
against archive records (rseng-archiving).

Drafting workflow for an agent: for an existing project, read the
repository first - license, CI, tests, CITATION.cff, README - and
write the plan that is TRUE, flagging gaps as planned improvements
with owners rather than papering over them. For a new proposal,
draft from intended practices with this pack's standards as the
default, concrete over aspirational ("unit tests in CI on every
merge", not "high quality standards"). Version the plan in the
repository so changes are reviewable history; revisit at releases
and reporting deadlines, and run a drift check - a plan that says
"Zenodo archiving" while nothing is archived is a liability at
review time. The data twin is rseng-data-management-plans; write the
two consistently and cross-reference them. Record AI assistance in
drafting in aidecl.yaml (rseng-ai-declaration).

## Choosing languages, tools, and infrastructures

Distinguish the three kinds of choice before advising: the programming *language* (the
main medium, affecting functionality, readability, and pace); *tools and
frameworks* (reusable abstraction layers for a domain, e.g. web, ML,
workflows); and *infrastructures* (broader knowledge-oriented techniques such
as databases, GPU/FPGA programming, or ML). The considerations below apply to
all three unless noted.

### Decision rules

Weigh social factors alongside technical ones - technical merit alone does
not predict a project's success:

- People and community: prefer what is already used widely in the field, for
  interoperability and reusability (the I and R in FAIR). Draw on existing
  practices, and on expertise available at your institute - a nearby expert
  who can coach you is invaluable.
- Personal and team expertise: account for what the team already knows and
  prefers; factor in project partners' preferences, not just your own.
- Language and ecosystem fit: does it offer the features and frameworks you
  need and save time; is it expressive enough for the design; is it not
  overkill or too complicated for the purpose?
- Deferring the choice: if undecided, design modularly and hide a choice
  behind an abstraction layer so the rest of the application is not tied to
  its specifics and the decision can change later.

### Match the choice to the lifecycle stage

Three situations impose different constraints:

- Rapid prototyping: personal preference weighs most - use something you know
  or want to try. If you know no language yet, Python is a good default.
- Starting a new development project: apply the full set of considerations
  above, balancing feature, social, and personal factors.
- Joining an existing project: you are usually constrained by the existing
  languages and frameworks; switching either is a big, infrequent decision.
  New technology may be exactly why you were brought in - social
  considerations still apply within those constraints.

### Good default languages

Opinionated but proven starting points:

- Python: prototyping, gluing code together, data analysis, ML; easy to start
  and widely adopted across scientific communities.
- C++: high performance, compiled, strongly typed, multi-paradigm.
- JavaScript/TypeScript: anything with a serious web component, and UI for
  non-web applications.
- R: statistical analysis, especially social sciences and medical research.
- Fortran: computationally intensive numerical simulation and HPC.
- Modern, smaller-ecosystem choices: Julia (mathematical modelling, elegant
  semantics, JIT-compiled) and Rust (high performance, safety-first).
- Special purpose: CUDA/OpenCL for GPU programming; shell scripting (Bash,
  PowerShell) for text processing, environment setup, and simple pipelines.

### Get off to a flying start with templates

After choosing, do not scaffold by hand - reach for community-curated
templates:

- Templates bundle current best practices ready to use, and contributing back
  multiplies the effort for future users. Prefer research-software-specific
  boilerplate, which covers aspects generic tools miss.
- Concrete starting points: the Netherlands eScience Center Python template,
  BestieTemplate.jl for Julia, and usethis for R packages.
- IDE snippets and AI assistants offer lighter-weight help (inline templates,
  autocompletion) and are worth using, but full project generators give a
  stronger, best-practice-aligned starting structure.

## Working with this skill

The generated references.md beside this file lists the source material
and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://www.software.ac.uk/guide/writing-and-using-software-management-plan -
    SSI guide to software management plans
  - https://doi.org/10.5281/zenodo.7038280 - practical guide to
    Software Management Plans
  - https://dmponline.dcc.ac.uk - DMPonline planning tool
  - https://book.the-turing-way.org/project-design/project-design/ -
    Turing Way guide for project design


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - preservation promises need archiving mechanics
- rseng-data-management-plans - drafting the data twin plan
- rseng-licensing - plan's licensing section needs specifics
- rseng-maintenance-sustainability - planning the long-term maintenance section
- rseng-project-kickoff - brand-new project starts with interview
- rseng-project-scaffolding - template kickstart after language choice

<!-- related-skills:end -->
