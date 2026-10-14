---
name: e1002-vcb
description: "Use when establish or operate a Verification Control Board (VCB) under ECSS-E-ST-10-02C §5.4.2: validate the board composition carries at least one customer representative and one supplier representative, confirm quorum is met before deliberation, categorize each agenda item by the decision authority it requires, evaluate whether attending members hold sufficient authority for each item, record each decision with rationale, and assess overall meeting compliance. Trigger: ecss, e-st-10-02c, verification-control-board, vcb, verification-governance, quorum, decision-authority, closeout-approval."
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
  tags: [ecss, e-st-10-system-scope, verification-control-board, vcb, verification-governance, quorum, decision-authority, closeout-approval]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Verification — Verification Control Board (space-systems/ecss/e1002-vcb)

Use when the task is to establish or operate a Verification Control Board
(VCB) per ECSS-E-ST-10-02C §5.4.2 — validating board composition,
confirming quorum before deliberation, categorizing agenda items by the
decision authority they require, evaluating whether attending members hold
sufficient authority, recording decisions with rationale, and checking
overall meeting compliance.

## Domain quick reference

- The VCB must include at least one customer representative and at least
  one supplier representative. Technical experts are co-opted as needed for
  domain coverage. Observers may attend but do not fill either required
  role and do not count toward quorum.
- Quorum is satisfied when both a customer representative and a supplier
  representative are present at the meeting. A VCB meeting must confirm
  quorum before recording any binding decision.
- Agenda items fall into two authority categories. Elevated-authority items
  (closeout approval, exception approval, discrepancy waiver) require both
  customer and supplier present to decide. Routine items (verification
  status change, action item review) require at least one of the two
  required roles present.
- Every decision must carry a rationale entry. Rationale ties the decision
  to the verification record and is mandatory for auditability; a decision
  with a missing or empty rationale is rejected before it is recorded.
- Valid decision outcomes are: approved, rejected, deferred, and
  conditionally approved. A deferred item has no binding outcome and must
  return to a future VCB meeting.

## Workflow

1. Check the VCB composition before convening. The board record must list
   at least one member with the customer role and at least one with the
   supplier role. Flag each missing required role as a composition finding.
   An observer-only or technical-expert-only board is not a valid VCB.
2. At meeting start, verify quorum by confirming that at least one customer
   representative and at least one supplier representative are marked as
   present. Record a quorum finding if either required role is absent; do
   not proceed to deliberation.
3. Categorize each agenda item as elevated-authority (closeout approval,
   exception approval, discrepancy waiver) or routine (verification status
   change, action item review). Reject an item type that is not in the
   recognised set before it enters the agenda.
4. For each agenda item, evaluate whether the roles present at the meeting
   satisfy the authority requirement for that item's category. Elevated
   items require both customer and supplier; routine items require at least
   one. Record an authority finding for items where attending roles fall
   short.
5. Record each decision with item identifier, item type, outcome
   (approved/rejected/deferred/conditionally approved), the roles present,
   and a rationale. Raise an error for an unrecognised item type,
   unrecognised outcome, or missing rationale before the record is written.
6. Aggregate composition, quorum, and decision-authority findings. The
   meeting is VCB-compliant when all three finding lists are empty.

## Pitfalls

- Proceeding to deliberation without confirming quorum: decisions recorded
  without both required roles present carry no binding authority under the
  VCB governance structure and must be voided.
- Treating observer or technical expert attendance as satisfying a required
  role: only the customer and supplier roles count toward quorum and
  decision authority; all other roles are supplementary.
- Recording a decision without rationale: an empty or missing rationale
  is not a minor omission — it breaks traceability to the verification
  record and must be rejected before the record is accepted.
- Applying routine authority to elevated-authority items: closeout
  approvals and exception approvals require both customer and supplier
  present; a meeting with only one of the two cannot decide these items
  regardless of how many technical experts attend.
- Treating a deferred decision as an approval: deferral means no binding
  outcome has been reached; the item must be re-tabled at the next
  meeting with quorum, not treated as passing by default.

## Behavior contract (gate 3)

The VCB composition validation, quorum check, agenda-item authority
categorization, decision recording, and full meeting review logic is
exercised by the gate 3 contract test:
scripts/test_e1002_vcb.py against scripts/e1002_vcb_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1002_vcb.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
