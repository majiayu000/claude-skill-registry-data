---
name: e50-outputs
description: "Verify the outputs a communication system engineering step is required to produce under ECSS-E-ST-50C clause 5.2.1.3, where the step is finished when its outputs exist rather than when its activities stop. Evaluate a declared output set for the three ways a claimed output turns out not to be one: absent entirely, present but carrying no identifier anyone can call for, and present but produced by no activity of the step. Grade duplicated names separately, and report completion as a fraction rather than a yes. Use when closing or reviewing a communication system engineering step. Trigger: ecss, e-st-50-communications, communication-system-engineering-outputs, communication-process-output-completeness, output-producer-traceability, unidentified-process-output, communication-design-deliverables."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
clauses:
  - standard: ECSS-E-ST-50C Rev.2
    clause: 5.2.1.3
    items: [a]
    relation: verifies
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-50-communications, e50-outputs, communication-system-engineering-outputs, communication-process-output-completeness, output-producer-traceability, unidentified-process-output, communication-design-deliverables]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Communications — Engineering Process Outputs (space-systems/ecss/e50-outputs)

Use when a communication system engineering step is being closed or reviewed,
per ECSS-E-ST-50C clause 5.2.1.3 — what the step is required to hand on, and
whether the things on the closure list qualify.

## Domain quick reference

- The clause fixes what the step produces. Completion is a property of
  the outputs, not of the activities: a step whose work is finished and
  whose outputs are not is not finished.
- A claimed output fails in three distinguishable ways, and they need
  different fixes. Absent: nobody produced it. Unidentified: it exists
  but has no identifier, so the next step cannot call for it and a
  review cannot cite it. Untraced: it exists but no activity of this
  step produced it, so it came from outside the step's control.
- Untraced is the one that survives reviews. A document with the right
  title is in the folder, everyone assumes it was written here, and the
  step inherits a deliverable it cannot maintain or justify.
- A duplicated output name is its own finding, not a tidiness problem.
  Two entries under one name mean nobody can say which copy is the
  deliverable, and downstream will pick whichever it found first.
- Completion is a fraction. Reporting it as a yes or no throws away the
  only number that tells a programme how far off it is, and invites a
  yes on the strength of the outputs that are present.

## Workflow

1. List the required outputs of the step before opening the closure
   list, so the review is driven by what is owed rather than by what
   was submitted. Where the step is the requirements engineering one,
   the list carries the requirements specification for the
   communication system: the customer owes it, and it is written to
   the document definition the standard's annex sets out for that
   deliverable.
2. Normalise each declared output into name, identifier and producing
   activity. Accept a missing identifier or producer rather than
   rejecting the record — those are the findings, not input errors.
3. Compare names against the required set and take completion as a
   fraction of it, keeping anything undeclared in its own list.
4. Flag every output with no identifier, naming it, because an output
   nobody can reference is an output nobody will find.
5. Resolve each producing activity against the step's own activity set,
   and flag both the outputs naming nothing and the outputs naming an
   activity that belongs to some other step.
6. Count repeated names and report each with its count.
7. Report the step complete only when nothing is missing, unidentified,
   untraced or duplicated — and report the fraction either way.

## Obligations

| Item | Step |
|---|---|
| ECSS-E-ST-50C Rev.2 5.2.1.3a | 1 |

## Pitfalls

- Closing a step on activity completion. The activities finishing is
  what makes the outputs possible, not what makes them exist.
- Accepting a title as an identifier. Titles collide across steps and
  get edited; the identifier is what survives being moved into a
  different folder by someone in a hurry.
- Letting an output name an activity from another step as its producer.
  It reads as traceability and is the opposite: this step is claiming
  credit for work it does not control and cannot maintain.
- Merging duplicate entries to clear the finding. The duplication is
  evidence that two versions are in circulation, and merging the list
  entries does not merge the documents.
- Reporting completion as a percentage of what was submitted rather than
  of what was required. Submitting one output and nothing else scores
  full marks under that arithmetic.

## Behavior contract (gate 3)

Output normalisation with absent identifiers and producers preserved,
the completion fraction with undeclared outputs held separate, the
unidentified and untraced findings, and duplicate-name counting are
exercised by the gate 3 contract test:
scripts/test_e50_outputs.py against
scripts/e50_outputs_logic.py (stdlib unittest, offline).
Run:
python3 scripts/test_e50_outputs.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
