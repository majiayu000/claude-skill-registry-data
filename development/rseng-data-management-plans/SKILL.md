---
name: rseng-data-management-plans
description: >-
  Covers data management plans (DMPs) for research projects: what funders
  require, drafting a DMP from the project's actual data reality (types,
  volumes, storage, sharing, preservation, responsibilities, costs),
  machine-actionable DMPs (RDA common standard, Data Stewardship Wizard,
  DMPonline funder templates), and keeping the plan synchronized with
  practice. Use when a proposal or project needs a DMP, when the user mentions
  data management plans, maDMPs, DS-Wizard or DMPonline, when funder or
  institutional data policy applies, or when the existing DMP has drifted from
  what the project actually does with its data. (Day-to-day data practice is
  rseng-data-management; the software management plan twin is
  rseng-management-planning.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Data management plans

A DMP answers, before the data exists, the questions that hurt
when answered too late: what data will the project produce, where
will it live, who may see it, what does that cost, and what
survives the grant. Funders require one with most proposals; the
useful version is not the compliance document but the honest
operating plan - and because it describes practices this pack
already engineers, most of a good DMP can be drafted from, and
checked against, the project itself. The software counterpart
(rseng-management-planning's SMP practice) shares this design; write the two
consistently and cross-reference them.

## What a plan covers

The standard sections, each answered from project reality:

1. Data description: types, formats, expected volumes, sources -
   name open formats deliberately (rseng-scientific-file-formats)
   and reused third-party datasets with their licenses and terms.
2. Documentation and metadata: data dictionaries, READMEs,
   community metadata standards for the domain
   (rseng-data-management owns the practice; the DMP states which).
3. Storage and backup during the project: where working data
   lives, replication, who administers it - institutional storage
   beats lab improvisation; sensitive data goes where the
   steward says (rseng-regulatory-compliance).
4. Access, sharing and legal: who can access what and when, embargo
   plans, consent and GDPR constraints, anonymization strategy -
   with honest limits stated (rseng-regulatory-compliance); "as open
   as possible, as closed as necessary" is the working frame.
5. Preservation and sharing after the project: which data is
   deposited, where (domain repository first, Zenodo-class
   otherwise - rseng-archiving), with what identifiers and licenses
   (rseng-licensing for data licenses), and what is deliberately
   discarded (retention has costs; keeping everything is not a
   plan).
6. Responsibilities and resources: named roles (who curates, who
   deposits), storage and curation costs as budget lines - data
   work is fundable work; say so in the proposal.

Proportionality: a simulation project with regenerable outputs
needs a lean DMP centered on code and configs
(rseng-reproducibility); a project collecting human-subject data
needs the full treatment. Match depth honestly.

## Machine-actionable DMPs

DMPs are becoming structured data, not prose PDFs:

- The RDA DMP Common Standard defines the maDMP schema - a JSON
  model of datasets, distributions, hosts, licenses and costs
  that tools exchange.
- The Data Stewardship Wizard (DS-Wizard) builds DMPs from
  questionnaire knowledge models and exports funder formats plus
  maDMP JSON; DMPonline carries the major funder templates.
  When the user's institution runs one of these, draft THERE (or
  produce content ready to paste), so the plan lands in the
  system reviewers and stewards actually use.
- The agent-friendly consequence: a structured DMP is checkable -
  datasets listed in the plan can be diffed against datasets the
  project actually has, licenses in the plan against LICENSE
  files, deposit promises against archive records
  (rseng-archiving).

## The DMP as a living document

Plans drift: new instruments, bigger volumes, a dataset that
cannot be shared after all. Treat the DMP like the SMP:

- Version it with the project (repository or the DMP platform's
  versioning); update at milestones, reporting deadlines and
  whenever data reality changes - a plan contradicted by practice
  is a liability at review and audit time
  (rseng-management-planning owns the cadence).
- Run a drift check when revisiting: promised repositories vs
  actual deposits, promised metadata vs delivered, promised
  retention vs disk reality. Report gaps as actions with owners.
- Record AI assistance in drafting or revising the plan in
  aidecl.yaml (rseng-ai-declaration).

## Working with this skill

This skill is source-independent: its authority is the RDA common
standard, the platform documentation and the RDMkit guidance
linked below. It is the data twin of
the SMP practice in rseng-management-planning; rseng-data-management holds the
underlying practice.

Learn more (verified):
  - https://rdmkit.elixir-europe.org/data_management_plan - RDMkit
    on data management plans
  - https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard -
    RDA maDMP common standard
  - https://ds-wizard.org - Data Stewardship Wizard
  - https://dmponline.dcc.ac.uk - DMPonline funder templates

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - deposit and preservation promises
- rseng-data-management - the practice the plan describes
- rseng-licensing - data license choices in the plan
- rseng-management-planning - SMP twin, shared drafting cadence
- rseng-regulatory-compliance - GDPR, consent and anonymization sections
- rseng-scientific-file-formats - naming open formats deliberately

<!-- related-skills:end -->
