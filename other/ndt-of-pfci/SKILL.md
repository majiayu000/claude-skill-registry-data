---
name: ndt-of-pfci
description: "Use when determine the appropriate NDT category for each potentially fracture critical item (PFCI) under ECSS-E-ST-32C: select the NDT method whose minimum detectable crack size is at or below the initial assumed crack size for the item, verify that each inspection record carries full traceability to the PFCI identification, lot, and procedure reference, and handle any detected defect through the disposition protocol linked to ECSS-Q-ST-70-15. Trigger: ecss, e-st-32-structures-scope, ndt, fracture-critical, pfci, initial-crack-size, q-st-70-15, defect-disposition, traceability."
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
  tags: [ecss, e-st-32-structures-scope, ndt, fracture-critical, pfci, initial-crack-size, q-st-70-15, defect-disposition, traceability]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Structures — NDT of Potentially Fracture Critical Items (space-systems/ecss/ndt-of-pfci)

Use when the task is selecting and applying non-destructive testing (NDT)
to potentially fracture critical items (PFCIs) per ECSS-E-ST-32C fracture
control requirements — confirming that the chosen NDT method can resolve
cracks at or below the assumed initial crack size, verifying inspection
traceability, and applying the defect-disposition protocol that interfaces
with ECSS-Q-ST-70-15.

## Domain quick reference

- An NDT method is adequate for a PFCI when its minimum detectable crack
  size is at or below the assumed initial crack size (a_i) set for that
  item. If the detection threshold exceeds a_i, the inspection provides
  no assurance and must not be accepted. NDT methods are categorized by
  the defect locations they cover (surface/near-surface or volumetric)
  and the materials they are compatible with.
- Commonly applied NDT methods and their scope: fluorescent penetrant
  inspection (FPI) and magnetic particle inspection (MPI) cover surface
  and near-surface cracks; eddy current (EC) offers finer resolution for
  conductive materials at surface and near-surface locations; ultrasonic
  testing (UT) and radiographic testing (RT) resolve volumetric defects.
  Visual testing (VT) alone is insufficient for fracture control except
  as a preliminary screen because its detection threshold is too coarse
  for typical PFCI crack sizes.
- Each PFCI inspection record must carry full traceability: item
  identifier, lot reference, inspection date, NDT method used, procedure
  document reference, operator identity, operator qualification level
  (L1/L2/L3), and inspection result. A record missing any mandatory field
  is incomplete and must not be accepted as evidence of conformance.
- The Q-ST-70-15 interface governs what happens when a defect is found.
  Defect size below the critical crack size triggers rework and mandatory
  re-inspection before the item returns to service. Defect size at or
  above the critical crack size triggers rejection and quarantine, with a
  non-conformance report raised under the Q-ST-70-15 process.

## Workflow

1. For each PFCI, confirm the material type and the location of the
   assumed crack (surface, near-surface, or volumetric), then select an
   NDT method that is both compatible with that material and covers that
   location. Reject any method that does not satisfy both conditions before
   the inspection begins.
2. Confirm that the selected method's minimum detectable crack size is at
   or below the assumed initial crack size a_i for the item. If the
   method's threshold exceeds a_i, it cannot bound the assumed crack and
   a more sensitive method must be selected; document the rejection and the
   reason before proceeding.
3. Conduct the inspection and immediately record results with full
   traceability (item ID, lot, procedure reference, operator ID, operator
   qualification level, date, and result). Verify all mandatory fields are
   populated and that the qualification level and result values are from
   the permitted sets before the record is accepted.
4. If no defect is detected: confirm the record is complete and accept the
   item for fracture control purposes, with the initial crack size formally
   set to the NDT detection threshold of the method applied.
5. If a defect is detected: measure or bound the defect size and compare
   it to the critical crack size for the item. If below critical, quarantine
   the item, perform rework, and re-inspect under the same or more sensitive
   NDT method before return to service. If at or above critical, reject and
   quarantine the item and raise a non-conformance report per the Q-ST-70-15
   interface.
6. Aggregate findings across all PFCIs; a PFCI is conformant only when
   its NDT adequacy check passes, its traceability record is complete, and
   no unresolved defect remains open.

## Pitfalls

- Selecting an NDT method without checking material compatibility: MPI
  applied to a composite or non-ferromagnetic item yields no indication
  of defects and cannot be accepted as evidence of conformance.
- Accepting an inspection whose detection threshold exceeds the assumed
  initial crack size: if the method cannot resolve cracks as small as a_i,
  the inspection is silent on the very cracks the fracture control programme
  assumes exist, making the record misleading rather than assuring.
- Treating an incomplete traceability record as a minor administrative
  gap: each mandatory field is a verifiable link in the chain of evidence;
  a missing field means the inspection cannot be traced and the record is
  void for fracture control purposes.
- Reading defect-not-found as automatically passing when the NDT adequacy
  check was never done: a clean inspection result from an inadequate method
  is not a clean result — the method never had the resolving power to find
  the assumed crack.
- Applying defect disposition without reference to the critical crack size:
  all detected defects must be sized and compared; disposition is determined
  by that comparison, not by engineering judgement alone.

## Behavior contract (gate 3)

The NDT adequacy, traceability verification, defect disposition, and full
PFCI assessment logic is exercised by the gate 3 contract test:
scripts/test_ndt_of_pfci.py against scripts/ndt_of_pfci_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_ndt_of_pfci.py

## Compliance

- ECSS-E-ST-32C and ECSS-Q-ST-70-15 are freely downloadable (ESA); cite
  the source and paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
