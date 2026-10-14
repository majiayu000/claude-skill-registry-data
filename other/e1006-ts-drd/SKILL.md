---
name: e1006-ts-drd
description: "Use when validate a Technical requirements specification (TS) document against the ECSS-E-ST-10C Annex A DRD: confirm all mandatory sections are present (system identification, mission context, technical performance requirements, interface requirements, environmental conditions, and verification cross-reference table), verify each requirement carries a unique identifier and an assigned verification method (test, analysis, inspection, or review of design), check that interface requirements reference a registered ICD entry, and flag any absent mandatory section or any requirement lacking a verification method. Trigger: ecss, e-st-10-system-scope, technical-specification, ts-drd, requirements-document, verification-method, interface-requirement, drd-validation."
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
  tags: [ecss, e-st-10-system-scope, technical-specification, ts-drd, requirements-document, verification-method, interface-requirement, drd-validation]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Systems Engineering — Technical Requirements Specification (TS) DRD (space-systems/ecss/e1006-ts-drd)

Use when the task is to generate or validate a Technical requirements
specification (TS) document per ECSS-E-ST-10C Annex A DRD — confirming
that all mandatory sections are present, that every requirement is properly
identified and carries a verification method, and that interface requirements
are linked to registered ICDs.

## Domain quick reference

- The TS document is the contractual statement of what a system or subsystem
  shall do, defined in ECSS-E-ST-10C Annex A as a normative Document
  Requirements Definition (DRD). Its purpose is to capture the complete,
  consistent, and verifiable set of technical requirements at a given product
  tree level before design work begins.
- Six sections are mandatory in every TS: the system identification block
  (project, item, revision), the mission and functional context, the technical
  performance requirements (TPRs), the interface requirements, the
  environmental requirements, and the verification cross-reference table that
  maps each requirement to its assigned verification method.
- Verification methods follow the four-method taxonomy: Test (T) — direct
  measurement; Analysis (A) — computation or modelling; Inspection (I) —
  visual or dimensional check; Review of Design (R) — examination of drawings
  and documents. Every requirement must be assigned at least one of these four.
- Interface requirements must reference an Interface Control Document (ICD)
  entry. A requirement that calls out an ICD not in the project's registered
  ICD list is a traceability gap and must be flagged.
- A TS is not compliant until both structural completeness and requirement
  integrity are satisfied: all sections present, all requirements identified,
  and all verification methods valid.

## Workflow

1. Confirm the document identification block is populated: project name,
   system or subsystem name, document number, revision letter, and effective
   date. Reject any TS that is missing or blank in these fields before
   proceeding.
2. Verify the mission and functional context section describes what the item
   does within its parent system, the applicable mission phases, and the key
   functional modes. The section must exist and must not be empty.
3. Inspect each requirement in the technical performance requirements,
   interface requirements, and environmental requirements sections. For each
   requirement: confirm a unique identifier is assigned (e.g. TPR-001);
   confirm the requirement text is non-empty; confirm a verification method
   is assigned and resolves to one of T, A, I, or R.
4. For every requirement of type interface, check that an ICD reference is
   present and that the referenced ICD appears in the project's registered
   ICD list. Flag any interface requirement with a missing or unregistered
   ICD reference.
5. Confirm the verification cross-reference table is present. Each row of
   the table should map a requirement identifier to one or more verification
   methods. The table need not be exhaustively checked at this step — its
   presence is the structural gate.
6. Compute the completeness score as the fraction of the six mandatory
   sections that are non-absent. Report the score alongside the findings
   list. A score of 1.0 with an empty major/critical findings list indicates
   a TS that passes the DRD gate.

## Pitfalls

- Accepting a requirement with a verification method of "TBD" or "simulation"
  as compliant — neither resolves to T, A, I, or R and must be flagged as
  an unrecognized method.
- Treating the absence of a verification cross-reference table as a minor
  issue — the table is a mandatory DRD section; its absence is a major
  structural finding that blocks DRD compliance regardless of individual
  requirement quality.
- Skipping the ICD-linkage check for interface requirements because the ICD
  "probably exists" — traceability must be verified against the actual
  registered ICD list, not assumed.
- Treating a TS with a completeness score below 1.0 as partially compliant —
  partial compliance is non-compliance at the DRD gate; every mandatory
  section must be present before the document can be submitted.

## Behavior contract (gate 3)

The structure validation, requirement integrity, interface linkage, and
completeness scoring logic is exercised by the gate 3 contract test:
scripts/test_e1006_ts_drd.py against scripts/e1006_ts_drd_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1006_ts_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
- Citation anchor: ECSS-E-ST-10C Annex A (DRD-TS).
