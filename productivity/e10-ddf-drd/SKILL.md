---
name: e10-ddf-drd
description: "Use when validating or generating a Design Definition File
  (DDF) against the ECSS-E-ST-10 Annex G document requirements definition
  (DRD): identify the content blocks (introduction, applicable and reference
  documents, terms/definitions/abbreviations, design overview, per-item
  design solution, budgets and margins, interface definition, design
  justification, open-points register, supporting annexes) that are
  mandatory at the current review milestone (SRR, PDR, CDR, AR), classify
  each block as present or missing, verify its reported maturity (draft,
  consolidated, final) meets the milestone's minimum, and confirm the
  open-points register carries zero unresolved TBD/TBC items by acceptance
  review. Trigger: ecss, e-st-10-system-scope, ddf, design definition file,
  annex g, drd, review milestone, tbd tbc closure."
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
  tags: [ecss, e-st-10-system-scope, ddf, design-definition-file, annex-g, drd, review-milestone]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Design Definition File DRD (space-systems/ecss/e10-ddf-drd)

Use when the task is producing or checking a Design Definition File (DDF)
against the ECSS-E-ST-10 Annex G document requirements definition -- the
DDF's content-block structure, and the maturity each block must reach at
a given project review milestone, rather than the design content itself.

## Domain quick reference

- Annex G defines a fixed content-block list for the DDF: introduction;
  applicable and reference documents; terms, definitions and abbreviated
  terms; design overview (functional and physical architecture); design
  solution per configuration item; engineering budgets and margins;
  interface definition; design justification and trade-off rationale;
  an open-points register (TBD/TBC list with a closure plan); and
  supporting annexes (drawings, ICDs, budget sheets). A block outside
  this list is not part of the DRD structure.
- The DDF is not produced once -- it is re-issued with growing maturity
  at each project review milestone (SRR, PDR, CDR, AR, in that order).
  Each content block becomes mandatory from a specific milestone
  onward: the introduction, reference documents, terms, design overview
  and open-points register are mandatory from SRR; per-item design
  solution, budgets/margins and interfaces are added at PDR; design
  justification and supporting annexes are added at CDR. A block
  mandatory from an earlier milestone stays mandatory at every later
  one.
- Each present block also carries a maturity level -- draft,
  consolidated, or final -- and the DRD expects a minimum maturity per
  milestone: draft at SRR, consolidated at PDR, final at CDR and AR. A
  mandatory block present below the milestone's minimum maturity is a
  finding, not a pass.
- The open-points register tracks TBD (to be determined) and TBC (to be
  confirmed) items against the design. It is allowed to be non-empty
  through SRR/PDR/CDR, but by the acceptance review (AR) milestone --
  the DDF's closure point -- every open item must be resolved; a
  nonzero count at AR is itself a finding.

## Workflow

1. Determine the current review milestone (SRR, PDR, CDR, or AR) that
   the DDF is being assessed against. Reject an unrecognized milestone
   before proceeding.
2. Derive the set of content blocks mandatory at or before that
   milestone from the Annex G content-block catalogue.
3. For each reported content block, classify it against the catalogue:
   flag a block id that is not part of the DRD structure as
   unrecognized rather than silently accepting it.
4. For each mandatory block, verify it is present; a missing mandatory
   block is a finding.
5. For each present mandatory block, verify its reported maturity meets
   or exceeds the milestone's minimum (draft at SRR, consolidated at
   PDR, final at CDR/AR); an unreported or insufficient maturity is a
   finding.
6. At the AR milestone only, verify the open-points register reports
   zero unresolved TBD/TBC items; a nonzero count is a finding.
7. Aggregate every finding category; the DDF is not compliant at this
   milestone until missing blocks, unrecognized blocks, insufficient
   maturity, and (at AR) unresolved open items are all empty.

## Pitfalls

- Treating a block that is optional at SRR/PDR but appears early as a
  problem -- the DRD sets a floor (mandatory from a milestone onward),
  not a ceiling; early inclusion of a later-mandatory block is not a
  finding.
- Accepting a mandatory block as compliant because it is present,
  without checking its maturity -- a design-overview block still
  marked "draft" at CDR has not met the DRD's minimum for that
  milestone even though the block itself exists.
- Reading an empty open-points register at SRR or PDR as evidence of a
  mature design -- the register is expected to carry live TBD/TBC
  items at earlier milestones; the empty-register requirement applies
  only at AR closure.
- Silently ignoring a content-block id absent from the Annex G
  catalogue -- an unrecognized block name is a structure error (wrong
  id, typo, or a block the DRD does not define), not a harmless extra.

## Behavior contract (gate 3)

The milestone-derived mandatory-block set, block classification,
maturity check, and AR open-points closure logic is exercised by the
gate 3 contract test: scripts/test_e10_ddf_drd.py against
scripts/e10_ddf_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e10_ddf_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
