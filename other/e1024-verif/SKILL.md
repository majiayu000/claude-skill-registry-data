---
name: e1024-verif
description: "Use when verify and validate interfaces under ECSS-E-ST-10-24C §5.6:
  check each ICD record for completeness (required fields, valid interface type,
  non-self-referential subsystems), confirm every VCD entry carries an approved
  verification method per E-ST-10-02 (test, analysis, inspection, review, or
  similarity) and a recognized status, trace each interface requirement to at
  least one VCD entry to identify coverage gaps, and flag interface items with
  no verification record. Trigger: ecss, e-st-10-system-scope, e-st-10-24c,
  interface-verification, icd, vcd, verification-control-document,
  interface-compliance, coverage-trace."
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
  tags: [ecss, e-st-10-system-scope, e-st-10-24c, interface-verification, icd, vcd, verification-control-document, interface-compliance]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Interface Management — Verify and Validate Interfaces (space-systems/ecss/e1024-verif)

Use when the task is to verify and validate interface definitions under
ECSS-E-ST-10-24C §5.6 — checking ICD records for completeness, validating
VCD entries for approved methods and statuses, and tracing every interface
requirement to at least one verification activity.

## Domain quick reference

- ECSS-E-ST-10-24C §5.6 requires that every interface defined in an ICD
  is covered by a corresponding entry in the Verification Control Document
  (VCD). Each VCD entry names an approved verification method and records
  the current status of that verification activity.
- Approved verification methods (per E-ST-10-02): test, analysis,
  inspection, review, and similarity. Any other method string is not
  recognized and must be flagged before the VCD is accepted.
- Recognized VCD statuses: open, in-progress, complete, waived,
  not-applicable. A waived entry must still appear in the VCD — the
  waiver decision is evidence, not an absence of coverage.
- An ICD record must have: a unique identifier, a source subsystem, a
  destination subsystem, a recognized interface type (mechanical,
  electrical, thermal, data, rf, optical, fluid, or software), and a
  description. Source and destination must be distinct subsystems — a
  self-referential interface (source equals destination) cannot be
  verified meaningfully and is flagged.
- Coverage gap: an ICD item with no matching VCD entry (by ICD ID) is a
  gap finding. Coverage ratio = number of ICD items with at least one
  VCD entry divided by total ICD items.

## Workflow

1. Inventory all ICD records for the interface set under review. Confirm
   each record carries all required fields: id, source_subsystem,
   destination_subsystem, interface_type, and description. Flag any
   record missing a field or carrying a blank value.
2. Check each ICD record's interface_type against the recognized set.
   Flag any unrecognized type. Check that source_subsystem and
   destination_subsystem are not identical; flag any self-referential
   pair.
3. Inventory all VCD entries. Confirm each entry carries: id, icd_ref
   (pointing to the ICD record ID it covers), method, and status. Flag
   any entry with a missing or blank required field.
4. Validate each VCD entry's method against the approved set. Validate
   the status against recognized statuses. Flag any entry that fails
   either check.
5. Trace each ICD record to VCD entries: for every ICD id, check whether
   at least one VCD entry exists with a matching icd_ref. Collect ICD
   ids with no matching VCD entry as gap findings.
6. Compute the coverage ratio. Report: ICD findings, VCD findings,
   coverage gaps, coverage ratio, and overall compliance status. The
   interface set is compliant only when ICD findings, VCD findings, and
   gaps are all empty.

## Pitfalls

- Treating a waived VCD entry as a gap — a waived status still provides
  evidence of a deliberate disposition; the gap list should only include
  ICD items with no VCD entry at all.
- Accepting an unrecognized verification method without flagging it —
  a method outside the E-ST-10-02 approved set cannot be evaluated for
  rigor; it must be flagged, not silently passed.
- Reading zero findings from a short ICD list as "fully verified" before
  computing the coverage ratio — an ICD list with no VCD entries at all
  has a coverage ratio of 0.0 and is not compliant.
- Allowing a self-referential interface (source equals destination) to
  enter the coverage trace — such an entry has no meaningful bilateral
  verification context and must be flagged at the ICD validation step.

## Behavior contract (gate 3)

The ICD validation, VCD validation, trace, and coverage logic is
exercised by the gate 3 contract test:
scripts/test_e1024_verif.py against scripts/e1024_verif_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1024_verif.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
