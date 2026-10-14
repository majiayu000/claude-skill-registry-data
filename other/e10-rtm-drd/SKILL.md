---
name: e10-rtm-drd
description: "Use when build or audit a requirements traceability matrix against the ECSS-E-ST-10C Annex N Document Requirements Definition: confirm every row carries its DRD fields, trace each derived requirement upward to a parent that exists in the matrix, trace each requirement that must flow down to at least one child, detect parent-pointer cycles, and confirm each allocation names a real product-tree element and each verification method is one of the four recognized ones. Trigger: ecss, e-st-10-system-scope, traceability-matrix, annex-n-drd, upward-trace, downward-trace, requirement-allocation, trace-coverage."
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
  tags: [ecss, e-st-10-system-scope, traceability-matrix, annex-n-drd, upward-trace, downward-trace, requirement-allocation]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — Requirements Traceability Matrix DRD (space-systems/ecss/e10-rtm-drd)

Use when the task is to build or audit a Requirements Traceability Matrix
against the Document Requirements Definition of ECSS-E-ST-10C Annex N --
the per-row trace fields, and the two directions of coverage the matrix
exists to prove.

## Domain quick reference

- Traceability runs in two directions and each finds a different defect.
  Upward: a derived requirement that reaches no parent came from
  nowhere. Downward: a requirement that must flow down but has no child
  was accepted and never allocated onward. Neither check substitutes for
  the other.
- A top-level requirement is *declared*, not inferred from a blank
  parent field. That distinction is the point: if absence of a parent
  meant "root", every forgotten link would silently become a new root
  and the upward check would find nothing.
- The two declarations are cross-checked both ways. A row declared
  top-level that also names a parent is as much a finding as a derived
  row with no parent -- the matrix is contradicting itself.
- A parent that is not itself a row in the matrix is a dangling trace:
  it looks traced, and it leads out of the document.
- Parent pointers can close into a cycle, which makes the upward walk
  non-terminating. Cycles are found explicitly rather than by letting a
  traversal run away.
- Allocation is checked against the product tree, not merely for
  presence. A row allocated to an element that does not exist is
  untraceable in exactly the way the matrix is meant to prevent.
- A blank verification method and an unrecognized one are separate
  findings, raised by separate checks, so one row never double-reports.

## Workflow

1. Confirm every row has a requirement identifier and that identifiers
   are unique; stop if not, since an ambiguous key makes tracing
   meaningless.
2. Check each row for its required DRD fields.
3. Run the upward trace: top-level rows must name no parent, derived
   rows must name one, and every named parent must exist.
4. Run the downward trace: each row expecting flow-down must have at
   least one child.
5. Detect parent-pointer cycles and report every requirement on one.
6. Check each allocation against the product-tree element set, and each
   verification method against the recognized four.
7. The matrix is Annex N complete only when the finding list is empty.

## Pitfalls

- Inferring "top level" from a blank parent field, which converts every
  dropped link into a spurious root and empties the upward check of
  meaning.
- Checking the upward trace only. Coverage of the parent requirements
  is the half that proves nothing was accepted and forgotten.
- Walking parent pointers without a cycle guard, which hangs on exactly
  the malformed matrix the audit is supposed to catch.
- Accepting an allocation string because it is non-empty. A typo names
  a product element that does not exist and still looks allocated.
- Reporting a blank verification method twice, once as a missing field
  and once as an unrecognized method. It is one defect.
- Reading a high percentage of traced rows as a pass. Annex N coverage
  is all-or-nothing; the untraced remainder is where the risk sits.

## Behavior contract (gate 3)

The row-uniqueness, DRD-field, upward-trace, downward-trace,
cycle-detection, allocation and verification-method logic is exercised
by the gate 3 contract test: scripts/test_e10_rtm_drd.py against
scripts/e10_rtm_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e10_rtm_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
