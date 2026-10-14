---
name: e10-sep-drd
description: "Use when you must generate or validate a System Engineering Plan (SEP) document against its document-requirements-definition (DRD) per ECSS-E-ST-10C Annex D: check the document carries every mandatory content block (introduction, applicable/reference documents, SE organisation, SE processes, SE tasks, DRD linkage), that every organisation interface (product assurance, AIV, risk management, configuration management, software engineering) is covered by an assigned role, that every task has a known owner, and that every document the SEP claims to plan or control exists in the project's master document list. This checks the SEP document's DRD content shape; see the sibling e10-sep leaf for SEP maintenance and baseline-consistency logic. Trigger: sep drd, system engineering plan drd, ecss annex d, sep content, sep document requirements, e-st-10c annex d."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-10c, annex-d, sep, drd, document-check, system-engineering-plan]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering Plan DRD Check (space-systems/ecss/e10-sep-drd)

Use when the task is generating or validating a System Engineering Plan
(SEP) document against ECSS-E-ST-10C Annex D's document-requirements-
definition (DRD): confirm the document carries every mandatory content
block, that the organisation section covers every required interface,
that every task has a known owner, and that the document's claimed
links into the project's document tree resolve.

## Domain quick reference

- ECSS-E-ST-10C Annex D fixes the DRD content list for the SEP: an
  introduction and applicable/reference documents section, the
  project's SE organisation and its interfaces to other project
  functions, the SE process description, the SE task list, and the
  SEP's linkage to the other documents it plans or controls in the
  project's document tree.
- The SE organisation section must show, for every project function
  the SEP interfaces with -- product assurance, AIV, risk management,
  configuration management, software engineering -- at least one
  assigned role responsible for that interface.
- Every task in the SEP task list must be owned by a role defined in
  the SE organisation section; a task with no matching role is a DRD
  gap, not just a scheduling detail.
- The SEP's DRD-linkage section names the other project documents it
  plans or controls; every name there must resolve to an entry in the
  project's master document list (e.g. the Annex A delivery schedule),
  or the link is dangling.
- This leaf checks the SEP document's DRD content shape at a point in
  time. It does not evaluate whether the SEP is due for revision or
  whether lower-level plans remain baseline-consistent with it -- that
  is the sibling e10-sep leaf's scope.

## Workflow

1. Assemble the candidate SEP document as section key -> content and
   run missing_sections against it for the six mandatory Annex D
   content blocks (REQUIRED_SEP_SECTIONS).
2. List the SE organisation's roles and their declared interfaces, and
   run missing_organisation_interfaces to confirm every required
   interface (product-assurance, aiv, risk-management,
   configuration-management, software-engineering) is covered.
3. List the SE task list and run unowned_tasks against the roles from
   step 2 to catch any task without a matching owner.
4. List the documents the SEP's DRD-linkage section claims to plan or
   control and run dangling_drd_links against the project's master
   document list.
5. Combine steps 1-4 with sep_drd_compliance; the SEP is DRD-compliant
   only when every violation list it returns is empty.

## Pitfalls

- Treating the SE organisation section as an org chart only, without
  naming which role owns each required interface (product assurance,
  AIV, risk management, configuration management, software
  engineering).
- Adding a task to the SE task list under a role that was never
  defined in the organisation section (or was renamed since).
- Letting the DRD-linkage section reference a document that was
  dropped from, or never added to, the project's master document
  list.
- Confusing this DRD content-shape check with the sibling e10-sep
  leaf's maintenance-trigger and baseline-consistency logic -- a
  document can be DRD-compliant in shape yet still be on a stale
  baseline.

## Behavior contract (gate 3)

The required-section, organisation-interface, task-ownership, and
DRD-linkage logic is exercised by the gate 3 contract test:
scripts/test_e10_sep_drd.py against scripts/e10_sep_drd_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e10_sep_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
