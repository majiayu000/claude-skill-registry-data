---
name: q1009-capa
description: "Define the corrective and preventive actions a nonconformance owes under ECSS-Q-ST-10-09C clause 5.3. Use when a proposed action set has to be judged against the root causes it claims to remove, when containment is being offered as the fix, or when a recurring or systemic cause needs prevention as well as correction: rank the control each action installs, check that every cause carries a corrective action stronger than added inspection, demand prevention wherever the mechanism reaches further hardware, and record the rationale behind each choice. Trigger: ecss, q-st-10-09c, corrective-action-selection, preventive-action-selection, root-cause-coverage, recurrence-prevention, containment-versus-correction, capa-rationale-record."
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
  tags: [ecss, q-st-10-09c-nonconformance-scope, q1009-capa, corrective-action-selection, preventive-action-selection, root-cause-coverage, recurrence-prevention, containment-versus-correction, capa-rationale-record]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Nonconformance Control — Corrective and Preventive Action (space-systems/ecss/q1009-capa)

Use when the task is the action-definition step of ECSS-Q-ST-10-09C
clause 5.3 — deciding which actions a nonconformance actually earns,
whether they reach its root causes, and whether recurrence has been
stopped rather than merely detected next time.

## Domain quick reference

- Three kinds of action follow a nonconformance and only two of them
  are what the clause asks for. Containment stops the escape now:
  segregate, impound, screen the built stock. Corrective action removes
  a cause that has already produced a nonconformance. Preventive action
  removes a cause before it produces one, wherever the same mechanism
  can reach.
- Containment is not correction. An action set made only of containment
  holds the escape and leaves every cause in place, so it closes
  nothing.
- An action is worth the control it installs. Eliminating the
  possibility outranks a substitution, which outranks an engineering
  control, which outranks a written procedure or a training session,
  which outranks an added inspection. Added inspection detects the
  defect again; it has not removed the cause, so it never closes one on
  its own.
- Some causes reach further than the item in hand. A design, process,
  procedure, training or supplier cause is systemic by nature, and a
  cause that has now occurred more than once has demonstrated it, so
  both owe a preventive action as well as a corrective one.
- Every cause needs evidence behind it. A cause asserted from opinion
  gives the action set nothing to be effective against, and the
  effectiveness check downstream has nothing to measure.
- The rationale is part of the record. An action chosen without a
  stated reason cannot be re-argued when it fails to hold, and the next
  occurrence starts the same investigation from nothing.

## Workflow

1. Take the root causes with their categories, occurrence counts and
   supporting evidence; reject an empty or duplicated cause set rather
   than proceeding against an unknown target.
2. Mark the causes that owe prevention: every systemic category, plus
   any cause whose occurrence count has reached the recurrence
   threshold the programme declares.
3. Validate each proposed action — identifier, type, the control it
   installs, the cause it addresses and its rationale. A corrective or
   preventive action pointing at a cause outside the set is an input
   error, not a weak action.
4. Map corrective actions onto causes and keep the strongest control
   per cause. Name any cause with no corrective action at all, and any
   cause whose only cover is added detection.
5. Compare the preventive actions against the causes that owe one and
   report the gaps by cause, not as a single count.
6. Report the weakest corrective control in the set: it is the action
   most likely to be the one that fails the effectiveness check later.
7. Close with an adequacy verdict and the named gaps, so the
   implementation step downstream tracks actions that are worth
   tracking.

## Pitfalls

- Recording a screening campaign as the corrective action. Screening is
  containment; it finds the units already affected and changes nothing
  about why they were affected.
- Adding an inspection step and calling the cause closed. The
  inspection detects the same defect on the next unit, so the cause is
  still producing nonconformances and the only change is that the
  programme pays to find them.
- Writing one action against several causes and counting it once per
  cause. Coverage is per cause, and an action that removes one
  mechanism does not remove the others because it was listed against
  them.
- Answering a second occurrence with the same one-off correction. A
  repeat is evidence that the cause is systemic, and what it owes is a
  preventive action across the family, not a second repair.
- Assigning training as the standing answer to a workmanship cause.
  Training is a weak control by rank; where a fixture, a tool change or
  a design change can remove the possibility, the stronger control is
  the one the clause is asking for.
- Leaving the rationale out because the action is obvious. Obvious
  actions are exactly the ones that get reversed quietly later, with
  nothing in the record to say what they were for.

## Behavior contract (gate 3)

The cause validation, recurrence marking, action validation, coverage
mapping, preventive-gap detection and adequacy verdict are exercised by
the gate 3 contract test: scripts/test_q1009_capa.py against
scripts/q1009_capa_logic.py (stdlib unittest, offline).
Run: python3 scripts/test_q1009_capa.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
