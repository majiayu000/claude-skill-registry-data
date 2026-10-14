---
name: e10-se-mgmt
description: "Use when manage the system engineering activities, responsibilities and interfaces of the SE function as defined in the System Engineering Plan (SEP) under ECSS-E-ST-10C clause 5.6.1: categorize each SE activity by kind, determine its assigned responsible role against the SEP responsibility assignment, verify each activity's required interfaces to other project functions (project management, product assurance, engineering disciplines, customer) are on record, and track activity status so a blocked activity carries a reason and a completed activity has no open prerequisite. Trigger: ecss, e-st-10-system-scope, se management, sep, responsibility assignment, interface control, system engineering plan, e-st-10c 5.6.1."
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
  tags: [ecss, e-st-10-system-scope, se-mgmt, sep, responsibility-assignment, interface-control]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering — SE Management (space-systems/ecss/e10-se-mgmt)

Use when the task is managing the system engineering (SE) activities,
responsibilities and interfaces of the SE function as defined in the
System Engineering Plan (SEP), per ECSS-E-ST-10C clause 5.6.1 --
categorizing each SE activity, checking that its SEP responsibility
assignment and required interfaces to other project functions are on
record, and checking that its status is internally consistent.

## Domain quick reference

- Clause 5.6.1 requires the SE function to manage its own activities,
  responsibilities and interfaces as laid down in the SEP. This leaf
  treats an SE activity as one of a fixed set of kinds: technical
  management, requirements engineering, analysis, design definition,
  verification, product-assurance interface, or risk management. Each
  activity is categorized into exactly one kind before the rest of the
  review runs.
- Every activity must have exactly one responsible role drawn from the
  SEP's role list (SE manager, lead engineer, subsystem engineer,
  product assurance engineer, project manager, customer
  representative). An activity with no owner recorded is flagged as
  unassigned; an owner outside the recognized role list is rejected
  outright, since it signals the SEP role list itself was not consulted.
- Each activity kind carries a fixed set of external project functions
  it must interface with under the SEP (e.g. verification must
  interface with product assurance; technical management and risk
  management must interface with project management; requirements
  engineering must interface with the customer). A recorded interface
  names its counterpart function; a required counterpart missing from
  the activity's recorded interfaces is flagged.
- Each activity also carries a status: planned, in progress, complete,
  or blocked. A blocked activity must record why (a blocking reason);
  a completed activity must not depend on another activity that has
  not itself reached complete -- an open prerequisite behind a
  "complete" activity is a management-control gap, not a technical one.

## Workflow

1. Inventory every SE activity under the SEP and categorize each one
   by kind. Reject an unrecognized activity kind before it enters the
   review.
2. For each activity, check the SEP responsibility assignment: flag a
   missing owner; reject an owner that is not a recognized SEP role.
3. For each activity, determine its required interface set from its
   kind and check it against the activity's recorded interfaces; flag
   each required counterpart that has no recorded interface. Reject an
   interface naming an unrecognized counterpart function.
4. For each activity, check status consistency: flag a blocked
   activity with no recorded reason, and flag a complete activity that
   depends on another activity not itself complete. Reject an
   unrecognized status or a dependency id that does not resolve to a
   known activity.
5. Aggregate the responsibility, interface and status findings per
   activity; the activity is not under SE management control until all
   three lists are empty.
6. Roll the per-activity reviews up to a program-level verdict; the
   program is not compliant until every activity in it is compliant.

## Pitfalls

- Treating an unassigned owner and an unrecognized owner the same way
  -- a missing owner is a findable gap in the SEP responsibility
  assignment, but a role outside the recognized SEP role list means
  the assignment itself is malformed and must be rejected, not
  silently logged as a finding.
- Skipping the required-interface check for an activity kind with no
  recorded interfaces at all -- the check is driven by the activity's
  kind, not by whether any interfaces happen to be present; an
  activity that never records an interface it is required to have is
  still a finding.
- Reading a "complete" status at face value without checking its
  dependencies -- a completed activity that still depends on an
  incomplete one is not actually under control, even though its own
  status field says otherwise.
- Conflating a blocked activity that records a reason with one that
  does not -- only the absence of a recorded reason is the finding;
  a blocked activity with a documented reason is a normal, trackable
  state, not a violation.

## Behavior contract (gate 3)

The activity-kind categorization, responsibility-assignment,
interface-coverage, and status-consistency logic is exercised by the
gate 3 contract test: scripts/test_e10_se_mgmt.py against
scripts/e10_se_mgmt_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e10_se_mgmt.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
