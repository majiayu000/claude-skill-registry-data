---
name: rseng-workflows
description: >-
  Covers building, choosing, discovering, describing, and sharing
  computational workflows with workflow management systems - when to move off
  ad-hoc scripts onto a WMS, how to make workflows FAIR, and where to find or
  register them. Use when the user asks how to automate a multi-step data
  pipeline, mentions Snakemake, Nextflow, CWL, WDL, Galaxy, Apache Airflow,
  Parsl, nf-core, or WorkflowHub, wants to pick a workflow engine, package a
  workflow with RO-Crate metadata, or make an analysis pipeline reproducible
  and reusable.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Computational workflows

Use this skill when a user is automating a multi-step, often multi-tool
data analysis or data-handling pipeline and wants it to be reproducible,
scalable, and shareable. A computational workflow is a special kind of
software that describes *what* should be done - a series of actions and the
data flowing between them - and hands the *how* (scheduling, resource
management, provenance tracking) to a workflow management system. Steer toward this approach when
automation would boost efficiency, when analyses must be re-run across many
datasets, or when infrastructures need integrating without reworking
existing processes.

## When to adopt a workflow manager

Treat these as triggers to move a user off ad-hoc glue and onto a WMS:

- The pipeline chains multiple tools/scripts and is run repeatedly, on new
  data, or by other people.
- Steps must run on an HPC cluster or cloud, or need parallelism the laptop
  cannot provide.
- Reproducibility, provenance, or transparent documentation is a
  requirement (publication, review, regulatory, or "future self" reruns).
- A hand-written Bash script or a notebook full of ordered cells has become
  hard to maintain, extend, or share - the classic failure mode of the
  manual "set of instructions" approach.

Recognise the spectrum, and place the user on it rather than forcing a jump:

- General-purpose scripting (Bash) - lowest ceremony, hardest to maintain
  and share at scale.
- Electronic research notebooks (Jupyter, RStudio, Apache Zeppelin) -
  ordered stages, good for exploration, still manual plumbing.
- Dedicated WMS - highest automation, reproducibility, and scalability
  because it separates inputs from data flow and abstracts the run
  mechanics behind a high-level definition language.

In practice these combine: a WMS can chain simple scripts, launched from a
notebook. Do not oversell a WMS for a
one-off, single-step script.

## Choose a workflow system

There is no universal best engine; the choice is driven by community,
facility, and environment. Work through
these factors with the user before naming a tool:

- Domain and community - scientific communities standardise around
  particular systems (e.g. REANA for particle physics; Galaxy, Snakemake,
  and Nextflow with deep roots in the life sciences). Matching the
  community buys shared workflows, documentation, and support.
- Facility and computing infrastructure - the target cluster or cloud may
  only support or optimise certain engines; this matters most when scaling.
- Availability of ready-made workflows, docs, and user support in that
  domain.

Common systems and their definition languages (pair the engine with its
language when advising):

- Nextflow - Nextflow DSL.
- Snakemake - Snakefile.
- Galaxy - browser-based, workflow repository and ToolShed.
- Apache Airflow - Airflow DAGs (Python).
- Parsl - Python-native parallel workflows.
- Cross-engine definition standards worth knowing: Common Workflow Language
  (CWL) and Workflow Description Language (WDL), which several registries
  and engines accept.

For a rigorous comparison, point users to "A Terminology for Scientific
Workflow Systems", which classifies 23 WMSs by composition, orchestration,
data management, and metadata capture, and to the domain review papers for
life-sciences engine choice.

## Discover before you build

Reusing an existing workflow beats writing one from scratch - it saves
time, avoids duplication, and inherits peer-reviewed, validated building
blocks, which raises trust in results and aids reproducibility. Advise users to search registries first,
then register their own so others can reuse them.

Point to the right registry for the context:

- WorkflowHub - cross-discipline FAIR workflow registry, strong life-science
  uptake; auto-registers nf-core workflows.
- nf-core - curated, community-reviewed Nextflow pipelines.
- Dockstore - registry supporting CWL, WDL, Nextflow, and Galaxy.
- Galaxy ToolShed / Galaxy workflow repository - Galaxy-compatible tools and
  workflows.
- REANA - reusable, reproducible analyses in particle physics and related
  fields.
- GESIS Methods Hub - emerging hub for social-science and digital
  behavioural workflows.
- GitHub / GitLab - general-purpose sharing alongside code and docs; note
  that GitHub search treats some workflow languages (e.g. CWL) as a
  searchable *Language*.

## Describe workflows with metadata

A workflow definition tells a WMS *how* to execute; workflow *metadata*
describes the workflow so humans and machines can understand, manage, and
discover it - purpose, inputs/outputs, dependencies, authorship, and
provenance. Both are needed; do not
conflate them.

- Recommend Workflow RO-Crate for packaging: it bundles the workflow
  definition (CWL, Nextflow DSL, Snakefile, etc.) with contextual metadata
  in a FAIR-compliant crate. It is the standard used by WorkflowHub and the
  LifeMonitor service.
- It builds on the RO-Crate standard and extends the schemas.science
  ComputationalWorkflow profile (from Bioschemas), using FormalParameter to
  describe inputs/outputs.
- Payoff to state: more discoverable, portable and reproducible workflows,
  especially when published alongside datasets or in a registry.

## Make workflows FAIR

Workflows are digital objects to be shared, discovered, and reused, so
apply the FAIR principles - both the general FAIR-for-research-software
recommendations and the dedicated FAIR recommendations for workflows. Concretely, when reviewing or authoring
a workflow, check that it is:

- Findable - registered with rich metadata and a persistent identifier
  (e.g. deposited in WorkflowHub with a DOI).
- Accessible - retrievable via its identifier, with the definition and
  metadata openly available.
- Interoperable - written in a recognised definition language and packaged
  with standard metadata (Workflow RO-Crate) so other tools can consume it.
- Reusable - clearly licensed, documented, versioned, and modular, with the
  computational environment pinned (see reproducible software environments,
  a closely related concern).

Point users at the Workflows Community Initiative FAIR Workflows Working
Group (WCI-FW) as the authoritative, cross-domain community effort on
applying FAIR data and software principles to workflows.

## Benefits to name when advocating

When a user is undecided, ground the pitch in concrete gains: reproducibility (each step, tool,
parameter, and environment is formalised and rerunnable); automation and
scaling (run unattended across datasets, distribute over HPC/cloud);
transparency and provenance (living documentation of the method); and
modularity, reuse, collaboration, and sharing (swap components, run the
same process across systems and teams).

## Working with this skill

The generated references.md beside this file lists the source
material and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://snakemake.readthedocs.io - Snakemake workflow
    management system
  - https://docs.seqera.io/nextflow/ - Nextflow documentation
  - https://www.commonwl.org - Common Workflow Language standard
  - https://workflowhub.eu - registry for computational workflows
  - https://doi.org/10.1038/s41597-025-04451-9 - applying FAIR
    principles to computational workflows


<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-big-data-processing - scaling pipelines across many datasets
- rseng-discovery - finding reusable workflows in registries
- rseng-fair-software - FAIR principles applied to workflows
- rseng-hpc-computing - running stages on clusters
- rseng-provenance - engine logs are provenance capture
- rseng-reproducible-environments - per-step pinned environments

<!-- related-skills:end -->
