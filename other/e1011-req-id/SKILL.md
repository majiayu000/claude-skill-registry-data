---
name: e1011-req-id
description: "Use when identify HFE requirements from mission-phase and operator-role analysis and capture them into the Technical Specification (TS) under ECSS-E-ST-10-11C §4.3.7: enumerate every applicable mission phase, assign the operator roles active in each phase, map each phase-role pair to the relevant HFE driver categories (workload, habitability, anthropometry, visibility, reachability, cognitive, communication, safety), generate a structured requirement ID for each identified driver, verify that every phase carries at least the mandatory safety and workload requirements, and confirm that all generated IDs are unique and correctly formatted before the TS baseline is closed. Trigger: ecss, e-st-10-system-scope, hfe-requirements, mission-phase, operator-role, human-factors, requirement-identification, technical-specification."
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
  tags: [ecss, e-st-10-system-scope, hfe-requirements, mission-phase, operator-role, human-factors, requirement-identification, technical-specification]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Human Factors Engineering — HFE Requirement Identification (space-systems/ecss/e1011-req-id)

Use when the task is to identify and capture Human Factors Engineering (HFE)
requirements into the Technical Specification (TS) following ECSS-E-ST-10-11C
§4.3.7 — deriving requirements from mission-phase analysis, operator-role
assignment, and HFE driver categorization, then verifying completeness and
uniqueness before TS baseline closure.

## Domain quick reference

- ECSS-E-ST-10-11C §4.3.7 establishes that HFE requirements must be derived
  systematically from three inputs: the enumerated mission phases (e.g. launch,
  ascent, orbit, re-entry, landing, maintenance, contingency), the operator
  roles active in each phase (e.g. crew, commander, ground control, maintainer),
  and the applicable HFE driver categories for each phase-role pair.
- Eight HFE driver categories apply across a crewed or human-tended space
  programme: workload (cognitive and physical task demand), habitability
  (living and working environment quality), anthropometry (dimensional
  clearances and reach envelopes), visibility (direct and display-mediated
  situational awareness), reachability (access to controls and interfaces),
  cognitive (information processing and decision support), communication
  (crew-crew and crew-ground voice/data exchange), and safety (emergency,
  escape, and rescue procedures).
- Two drivers — safety and workload — are mandatory in every mission phase;
  a phase that reaches TS without at least one requirement covering each of
  these is a completeness gap.
- Each identified requirement is assigned a structured ID of the form
  `HFE-<PHASE_CODE>-<ROLE_CODE>-<DRIVER_CODE>-<SEQ>` (e.g.
  `HFE-ORB-CRW-WKL-001`). IDs must be unique across the TS requirement set.

## Workflow

1. Enumerate mission phases from the mission analysis and confirm the phase
   list against the programme's operations concept. Reject any phase token not
   drawn from the agreed controlled vocabulary before continuing.
2. For each phase, identify which operator roles are active. Reject any role
   token not in the controlled vocabulary. At least one role must be active in
   each phase; a phase with no assigned role is a configuration error.
3. For each phase-role pair, determine which of the eight HFE driver categories
   apply. Apply the mandatory set (safety, workload) unconditionally; apply
   the remaining six based on the human-system interface present in that phase
   and role context. Reject any driver token not in the controlled vocabulary.
4. Generate a requirement ID for each phase-role-driver combination using the
   structured scheme. Format: `HFE-<PHASE_CODE>-<ROLE_CODE>-<DRIVER_CODE>-<SEQ>`
   where SEQ is a zero-padded three-digit integer incremented within each
   phase-role-driver group. Validate the format of every generated ID.
5. Perform the completeness check: confirm that for every phase in the mission
   scope, at least one requirement exists for the safety driver and at least one
   for the workload driver. Collect any phase that fails either check as a gap.
6. Perform the uniqueness check: confirm that no two requirements share the
   same ID. Duplicate IDs are a structural error regardless of content.
7. Compile the gap list (from step 5) and the duplicate list (from step 6).
   A requirement set is ready for TS insertion only when both lists are empty.
   Return the full requirement set together with the gap and duplicate reports.

## Pitfalls

- Skipping the mandatory-driver check and relying on the analyst to remember
  which drivers apply — safety and workload are non-negotiable in every phase
  and must be enforced programmatically, not by convention.
- Allowing free-text phase or role tokens without validation against the
  controlled vocabulary — uncontrolled tokens prevent consistent ID generation
  and break downstream traceability.
- Treating a phase-role-driver triplet as a complete requirement without
  assigning a structured ID — unstructured entries cannot be traced to TS
  paragraphs or verification evidence.
- Accepting duplicate IDs silently — two requirements sharing an ID will cause
  silent collisions in the TS and render verification mapping ambiguous.
- Closing the TS baseline before running both the completeness and uniqueness
  checks — late discovery of gaps or duplicates after baseline costs a formal
  change record.

## Behavior contract (gate 3)

The phase-validation, role-validation, driver-validation, ID-generation,
completeness-check, and uniqueness-check logic is exercised by the gate 3
contract test: scripts/test_e1011_req_id.py against
scripts/e1011_req_id_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1011_req_id.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
