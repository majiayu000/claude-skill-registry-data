---
name: e10-rjf-drd
description: "Use when compile or audit a Requirements Justification File against the ECSS-E-ST-10C Annex O Document Requirements Definition: validate each requirement's derivation basis, confirm a parent-derived requirement names its parent and that a top-level requirement rests on a standard or mission need instead, detect a rationale that merely restates the requirement it is meant to justify, confirm each rationale is attributed, and decide whether every requirement is justified. Trigger: ecss, e-st-10-system-scope, requirements-justification-file, rjf, annex-o-drd, derivation-basis, requirement-rationale, attribution."
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
  tags: [ecss, e-st-10-system-scope, requirements-justification-file, annex-o-drd, derivation-basis, requirement-rationale]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Requirements Justification File DRD (space-systems/ecss/e10-rjf-drd)

Use when the task is to compile or audit the Requirements Justification
File of ECSS-E-ST-10C Annex O -- the record of *why* each requirement
reads as it does, so that a later reviewer can re-derive the choice
rather than inherit it.

## Domain quick reference

- Every requirement carries three things: a derivation basis (a parent
  requirement, an analysis, an applicable standard, heritage, or a
  stated mission need), a rationale in its own words, and an attributed
  author.
- The basis and the requirement's level must agree. A requirement
  derived from a parent must name that parent. A top-level requirement
  cannot derive from one -- there is nothing above it -- so a
  parent-derived top-level row hides an unjustified requirement behind
  a trace that cannot exist.
- A top-level requirement rests on something external: an applicable
  standard or a stated mission need. Heritage is not enough at the
  apex, because "we did it this way before" explains a choice inside a
  design, not the existence of a system-level requirement.
- A parent recorded alongside a non-parent basis is fine -- an analysis
  that refined an inherited requirement legitimately has both -- so
  that combination is not a finding.
- The characteristic failure of this file is not a blank field: it is a
  rationale that restates the requirement. Every column is populated,
  nothing is explained, and a presence check passes it. A rationale
  identical to the requirement, or wholly contained in its wording,
  justifies nothing.
- Attribution matters because the file exists to be questioned later. A
  rationale nobody signed cannot be taken up with anyone.
- The file is complete only when no requirement carries a finding.

## Workflow

1. Confirm requirement identifiers are present and unique.
2. Validate each requirement's derivation basis against the recognized
   set.
3. Check the rationale: present, long enough to carry an argument, and
   not a restatement of the requirement itself. A missing rationale
   short-circuits the rest -- there is nothing to inspect.
4. Check the basis against the requirement's level: parent basis needs
   a named parent, a top-level requirement needs an external basis.
5. Confirm each rationale is attributed to an author.
6. Aggregate; a requirement is justified only when it carries no
   finding, and the file is complete only when all are.

## Pitfalls

- Grading the file on field completeness. A restating rationale fills
  every field and explains nothing, which is precisely how an RJF
  decays into a formality.
- Accepting a top-level requirement derived from a parent. The trace
  points at something that does not exist, and the requirement is
  effectively unjustified.
- Treating heritage as a sufficient basis at system level. It explains
  a design choice, not why the requirement is there at all.
- Flagging a requirement that records a parent alongside an analysis
  basis. Refining an inherited requirement legitimately has both, and
  flagging it trains reviewers to ignore findings.
- Reporting a missing rationale and a too-short rationale as two
  findings on the same row; absence is one defect, checked first.
- Leaving a rationale unattributed on the grounds that the team wrote
  it. The file's purpose is to let a later reviewer ask someone.

## Behavior contract (gate 3)

The basis validation, restatement detection, rationale, basis/level
agreement and attribution logic is exercised by the gate 3 contract
test: scripts/test_e10_rjf_drd.py against scripts/e10_rjf_drd_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e10_rjf_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
