---
name: rseng-open-science-practices
description: >-
  Covers the researcher-facing open science workflow: setting up OSF projects
  that link materials, data, code and registrations, preregistering studies
  and analysis plans, depositing preprints and linking them to published
  versions, participating in open peer review, and choosing openness levels
  honestly. Use when the user mentions open science, OSF, preregistration,
  registered reports or preprints, wants their research process (not just the
  software) open, asks where to preregister or preprint, or when a project's
  openness claims should become verifiable practice.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Open science practices

Open science extends what this pack does for software to the whole
research workflow: materials, data, analysis plans, manuscripts
and reviews, open by default and closed only with reasons. For an
agent the job is concrete plumbing, not advocacy: set up the
platforms, wire the links between artifacts, and make each
openness claim verifiable. The payoff structure is worth stating
when relevant: preregistration protects claims from hindsight,
preprints establish priority and speed feedback, open materials
earn reuse and citations - openness is self-interest aligned with
integrity.

## The OSF project as the hub

The Open Science Framework (osf.io, run by the Center for Open
Science) is the general-purpose spine for open projects:

- Structure: one OSF project per study, with components for
  materials, data, analysis code and preregistration; connect the
  code repository rather than copying it (OSF links forges;
  the repository stays the working home -
  rseng-version-control-review).
- Every component gets a persistent identifier and citation; wire
  these into the paper and the repository README so artifacts
  reference each other both ways (the same both-ways discipline
  as rseng-archiving).
- Access control is per-component: public materials next to
  embargoed data next to private drafts is a normal shape - "as
  open as possible, as closed as necessary", with reasons stated
  (rseng-regulatory-compliance governs the closed parts).
- OSF has a REST API; bulk setup and link auditing are
  scriptable when a lab runs many projects.

## Preregistration

A preregistration is a frozen, timestamped analysis plan filed
BEFORE the data is seen - the strongest cheap defense against
hindsight bias, and increasingly expected in several fields:

- File it on OSF's registration system (or a domain registry);
  once registered it is immutable - that is the point.
- The plan should be code-shaped where possible: hypotheses,
  exact variables, exclusion rules, models and inference criteria
  - ideally with the analysis script itself attached, run on
  simulated or pilot data (rseng-reproducibility's discipline
  applied before data collection; power-analysis code belongs
  here too).
- Deviations happen legitimately: the practice is to REPORT them
  as deviations with reasons, not to hide them - preregistration
  separates confirmatory from exploratory, it does not forbid
  exploration.
- Registered Reports go further: peer review of the plan before
  results exist, with in-principle acceptance - suggest the
  format when the field's journals offer it.

## Preprints

- Deposit at submission time (arXiv-class or domain servers;
  ASAPbio documents the landscape and journal policies) - a DOI'd
  preprint establishes priority and makes the work citable
  months or years early.
- Check the target journal's preprint policy first (most allow
  it; a few constrain versions) and use the journal's own
  checking where unsure.
- Link the chain: preprint to published version (servers support
  the link; OpenAlex tracks it - rseng-citation-hygiene uses this
  when verifying references), and both to the OSF project, data
  and code DOIs. The linked cluster IS the open research object.
- Versioned preprints are normal; update after major revisions
  so readers land on current claims.

## Open peer review and open participation

- When venues offer open review, the practices from
  rseng-software-peer-review transfer: constructive, specific,
  evidence-based - with a name on it.
- Review artifacts too: data and code review during peer review
  (CODECHECK-style execution) is open science applied to the
  evidence layer (rseng-software-peer-review,
  rseng-research-integrity).
- Community review of preprints (public comments, review
  platforms) counts as scholarly contribution; encourage
  recording it (ORCID records review activity).

## Keeping openness claims honest

Before submission or reporting, audit the claims: "data available
at X" resolves and matches (rseng-archiving's verify step),
"preregistered" links to the actual registration and deviations
are reported, "code available" points at a tagged, licensed,
citable release (rseng-publishing-releasing, rseng-licensing,
rseng-citation-metadata). The open-science story is the sum of
verifiable links - and AI contributions to any of it are declared
in aidecl.yaml (rseng-ai-declaration).

## Working with this skill

This skill is source-independent: its authority is the OSF and
Center for Open Science documentation and ASAPbio resources linked
below. It is the
researcher-workflow face of what rseng-fair-software,
rseng-reproducibility and rseng-archiving provide at the artifact
level.

Learn more (verified):
  - https://osf.io - Open Science Framework
  - https://www.cos.io - Center for Open Science
  - https://www.cos.io/initiatives/prereg - preregistration
    guidance
  - https://asapbio.org - ASAPbio preprint resources
  - https://orcid.org - ORCID researcher identifiers

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - both-ways artifact linking discipline
- rseng-citation-hygiene - preprint-to-published version drift
- rseng-publishing-releasing - citable code release behind claims
- rseng-regulatory-compliance - governs the closed components
- rseng-research-integrity - preregistration deviations reported honestly
- rseng-software-peer-review - open review practices transfer

<!-- related-skills:end -->
