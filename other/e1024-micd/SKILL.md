---
name: e1024-micd
description: "Use when produce mechanical interface control documents (MICDs) under ECSS-E-ST-10-24C §5.11: categorize each mechanical interface as structural, kinematic, thermal-mechanical, electrical-mechanical, fluid-mechanical, or optical-mechanical; verify the MICD carries required fields (interface identifier, provider and receiver elements, registered coordinate frame, six-component interface loads, and mass properties); validate that mass is non-negative and all six load components are numeric; flag any coordinate frame not found in the project registered-frame list; and aggregate open items to determine closure status — a MICD is closed only when all required data items are present and valid. Trigger: ecss, e-st-10-24c, micd, mechanical-interface, interface-control-document, coordinate-frame, interface-loads, mass-properties, e-st-10-system-scope."
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
  tags: [ecss, e-st-10-system-scope, e-st-10-24c, micd, mechanical-interface, interface-control-document, coordinate-frame, mass-properties]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Interface Management — MICD Production (space-systems/ecss/e1024-micd)

Use when the task is producing or reviewing a mechanical interface control
document (MICD) under ECSS-E-ST-10-24C §5.11 — confirming the interface is
categorized by type, all required data items are recorded, load components
and mass properties carry numeric values, and the referenced coordinate frame
appears in the project master registered-frame list.

## Domain quick reference

- §5.11 requires one MICD per mechanical interface between system elements.
  An interface is the physical boundary at which forces, moments, and
  kinematics are exchanged between a provider element (the hardware
  delivering the interface surface) and a receiver element (the mating
  hardware). Six mechanical interface types are recognized: structural
  (force- and moment-transmitting joints), kinematic (constrained
  degrees-of-freedom joints), thermal-mechanical (interfaces where thermal
  strain drives load), electrical-mechanical (connector or harness bracket
  interfaces), fluid-mechanical (pipe or tube attachment flanges), and
  optical-mechanical (mirror or lens mount interfaces). Each MICD records
  exactly one type; an unrecognized type is an error, not a default.
- The required data content per §5.11 is: interface identifier, provider
  element name, receiver element name, interface type, coordinate frame
  identifier (pointing to the project master frame list), the six-component
  interface load set (three orthogonal forces Fx, Fy, Fz in newtons and
  three orthogonal moments Mx, My, Mz in newton-metres, all evaluated at
  the interface plane in the reference coordinate frame), and mass
  properties of the provider-side hardware (mass in kg and
  centre-of-gravity coordinates in metres, in the same frame).
- A coordinate frame cited in a MICD must appear in the project
  registered-frame list; a frame not in that list indicates a definition
  gap in the interface management database — the MICD references geometry
  that cannot be traced to an authorised datum.
- A MICD is considered open until every required data item is present and
  each item passes its validity check (numeric load components,
  non-negative mass, registered frame). Open items are aggregated before
  the document is issued; the document is not closed with any open item
  outstanding.

## Workflow

1. Confirm the interface under assessment links exactly one provider element
   to one receiver element, and select the interface type from the recognized
   set. Reject any interface type not in the defined list before proceeding.
2. Check the MICD for required field completeness: interface identifier,
   provider element, receiver element, interface type, coordinate frame
   identifier, interface loads, and mass properties must all be present and
   non-null. Record each absent or null field as an open item.
3. Validate the coordinate frame identifier against the project
   registered-frame list. Flag any frame not found there as an open item.
4. Validate the six-component load set: confirm Fx_N, Fy_N, Fz_N, Mx_Nm,
   My_Nm, Mz_Nm are all present and carry numeric values. Flag each missing
   or non-numeric component as a separate open item.
5. Validate the mass-property block: confirm mass_kg, cg_x_m, cg_y_m,
   cg_z_m are all present and numeric, and that mass_kg is non-negative.
   Flag each missing, non-numeric, or negative-mass finding as an open item.
6. Aggregate the open items from steps 2–5. A MICD with an empty open-item
   list is ready for formal issue; otherwise return the list and resolve
   each item before closure.

## Pitfalls

- Accepting an unrecognized interface type instead of rejecting it — an
  unknown type means the interface has not been categorized under the
  standard's schema, and downstream checks (load characterization, test
  levels) will operate on an undefined interface class.
- Treating a None or absent coordinate frame field as acceptable with a
  default assumption — a MICD without a registered frame cannot be traced
  to a common geometric datum, which is an interface management gap, not
  a conservative assumption.
- Passing a MICD with a string placeholder (e.g. "TBD") for a load
  component — load values that are not numeric cannot be compared against
  a structural design limit and must be treated as missing data, not zero.
- Interpreting absence of open items as proof of physical correctness —
  the MICD closure check verifies data completeness and format; it does
  not verify that the recorded loads are within structural margins or that
  the coordinate frame orientation is correct.

## Behavior contract (gate 3)

The interface-type recognition, required-field completeness, coordinate-frame
registration, load-component validation, mass-property validation,
open-item aggregation, and closure-status logic are exercised by the gate 3
contract test: scripts/test_e1024_micd.py against scripts/e1024_micd_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1024_micd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
