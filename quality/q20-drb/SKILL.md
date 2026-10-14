---
name: q20-drb
description: "Run the delivery review board that decides whether a finished item may leave, under ECSS-Q-ST-20C clause 5.7.3: test the roster for the functions that must sit on it and for the independence the quality seat needs, name the end-item data package documents the board was never given, take every open nonconformance and every waiver to its own disposition instead of one verdict, and return deliver, deliver-with-reservation or hold with the minute fields the record owes. Use when a board has to convene, reach a defensible decision and leave a record of it. Trigger: ecss, q-st-20c-clause-5-7-3, delivery-review-board, drb-membership-quorum, eidp-completeness-at-delivery, open-nonconformance-disposition, waiver-carried-to-delivery, delivery-board-record."
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
  tags: [ecss, q-st-20c-quality-assurance-scope, q20-drb, delivery-review-board, drb-membership-quorum, eidp-completeness-at-delivery, open-nonconformance-disposition, waiver-carried-to-delivery, delivery-board-record]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Delivery Review Board (space-systems/ecss/q20-drb)

Use when the task is the clause 5.7.3 delivery review of ECSS-Q-ST-20C: a
finished item is ready to leave the supplier, a board has to convene on it, and
the question is whether it may be delivered, with what reservations, and what
the board record has to say afterwards.

## Domain quick reference

- The board is the last point at which the delivery can be stopped by the
  organisation that built the item. After it, the item is the customer's
  problem, so the board's authority comes from who sits on it: quality
  assurance, project management, engineering, configuration management and the
  customer's representative each hold a veto the others cannot exercise.
- The quality seat is only a check if it is independent of the organisation
  that built the item. A quality member reporting into production can attend a
  board and still not be able to stop it.
- The board reviews a fixed input set, not a narrative: the end-item data
  package, the open nonconformance log, and the deviations and waivers offered
  against the delivery. A document said to be following on has not arrived.
- A disposition is per finding. A major nonconformance carried on use-as-is or
  repair leaves the deviation inside the delivered item, so it needs the
  customer's agreement; a rework or scrap disposition removes it and needs only
  the closure evidence.
- A waiver that was never approved, or that lapsed before the delivery date, is
  not a reservation on the delivery — it is the absence of one.
- The record is a deliverable in its own right. Date, chair, attendance, the
  inputs reviewed, the decision and the actions are what makes the decision
  defensible when the item is opened months later.

## Workflow

1. Validate the roster: normalise each function name, refuse the same function
   seated twice, and separate a function nobody holds from one whose holder did
   not attend.
2. Compute the quorum ratio over the required functions and compare it with the
   required value through a named tolerance, so a ratio landing a few ULPs short
   of unity is not read as a short board.
3. Raise a dependent quality seat as its own finding rather than folding it into
   attendance.
4. Reconcile the data package presented with the one the delivery owes, matching
   document names without regard to case or separator, and name each gap.
5. Take each open nonconformance to a disposition, grouping the result as
   blocking or as a reservation the delivery carries.
6. Take each deviation and waiver to its approval and validity state on the
   delivery date, and raise an unapproved or lapsed one as blocking.
7. Check the minute fields, then combine everything: any blocking finding is a
   hold, reservations alone are a delivery with reservation, neither is a clean
   delivery.

## Pitfalls

- Treating a quorum as a headcount. Five people in the room is not five
  functions represented, and the function nobody holds is the one whose
  objection never gets made.
- Reading a reservation as a hold. An approved, in-date waiver is exactly the
  mechanism that lets a known deviation be delivered; refusing it makes the
  board a rubber stamp in the other direction.
- Accepting a major use-as-is on the supplier's signature alone. Use-as-is and
  repair both leave the deviation in the hardware, and only the customer can
  agree to receive it.
- Stopping at the first blocking finding. The board convenes once, so the
  record has to carry every gap found in that sitting, not the first one.
- Leaving the minutes for later. An undated record with no attendance cannot
  show which functions agreed, and the decision becomes unreconstructable.

## Behavior contract (gate 3)

The roster validation, quorum ratio, independence and attendance findings, data
package reconciliation, nonconformance and waiver dispositions, minute-field
check and the combined delivery decision are exercised by the gate 3 contract
test: scripts/test_q20_drb.py against scripts/q20_drb_logic.py (stdlib
unittest, offline). Run:
python3 scripts/test_q20_drb.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
