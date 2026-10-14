---
name: e1024-ticd
description: "Use when produce test interface control documents (TICDs) for ground test interfaces under ECSS-E-ST-10-24C §5.10: identify every electrical, mechanical, data, and power interface between the unit under test and ground support equipment, define each signal's type, direction, connector, and pin assignment, verify pin assignments are unique, confirm a ground reference signal is present, and check that all required interface categories are covered before the test campaign begins. Trigger: ecss, e-st-10-system-scope, ticd, test-interface-control-document, ground-support-equipment, gse-interface, verification, ground-test."
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
  tags: [ecss, e-st-10-system-scope, ticd, test-interface-control-document, gse-interface, verification, ground-test]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Verification — Test Interface Control Document (space-systems/ecss/e1024-ticd)

Use when the task is to produce a test interface control document (TICD)
for a ground test campaign under ECSS-E-ST-10-24C §5.10 — enumerating every
interface connection between the unit under test (UUT) and ground support
equipment (GSE), defining signal properties and pin assignments, and verifying
the interface set is complete and self-consistent before the test begins.

## Domain quick reference

- A TICD is the interface contract between the UUT and the GSE for a
  specific test configuration. It captures every signal exchanged across
  the test boundary: its type (electrical, power, data, mechanical, thermal,
  RF, optical, or ground), its direction relative to the UUT (source, sink,
  or bidirectional), and its physical location (connector identifier and pin
  number). One TICD per test configuration; a changed configuration requires
  a new or revised TICD before re-test.
- Signal types are grouped into interface categories. The set of required
  categories for a given test is specified by the test specification or the
  test procedure; the TICD must cover every required category. A TICD that
  omits an entire required category (e.g. no power signals in a powered
  functional test) is incomplete and blocks test readiness.
- Pin assignments must be unique within a connector: two signals cannot
  share the same connector/pin pair. A ground reference signal must appear
  at least once to establish the reference potential of the interface.
- Signal direction is defined relative to the UUT: source means the UUT
  drives the signal; sink means the UUT receives it; bidirectional means
  the UUT can both drive and receive on the same connection. A signal name
  that appears simultaneously as source and sink in the same TICD indicates
  a wiring conflict and must be resolved before test.

## Workflow

1. Identify the test configuration: record the TICD identifier, the UUT
   name and configuration state, and the GSE assembly being interfaced.
   A blank TICD identifier or test-item name stops the assessment —
   both fields are mandatory traceability anchors.
2. Enumerate every signal crossing the UUT/GSE boundary. For each signal
   record: signal name, signal type (from the controlled vocabulary),
   direction relative to the UUT, connector identifier, and pin number.
   Reject any record that is missing a required field or carries an
   unrecognized signal type or direction before it enters the assessment.
3. Check pin assignments for uniqueness within each connector: flag any
   connector/pin pair that is assigned to more than one signal. A conflict
   here indicates a wiring error in the TICD that must be corrected before
   the document can be baselined.
4. Check for duplicate signal names across the TICD: two distinct physical
   connections must not share the same signal name, as this makes the
   document ambiguous and traceability from the test procedure to the
   interface impossible.
5. Confirm a ground reference signal is present: at least one signal of
   type "ground" must appear in the TICD to establish the reference
   potential. Absence of a ground reference is a TICD completeness failure.
6. Compare the set of signal types present against the list of required
   interface categories for this test. Flag each required category that
   has no signal representative in the TICD.
7. Check for direction conflicts: a signal name that appears as both source
   and sink in the same TICD indicates a contradictory interface definition
   and must be resolved.
8. Aggregate all findings per step. The TICD is not ready for baseline
   until every finding is resolved and the document re-assessed clean.

## Pitfalls

- Baselineing a TICD before resolving pin conflicts — a shared connector/pin
  pair causes physical wiring ambiguity that cannot be resolved at test time
  without stopping the campaign.
- Omitting the ground reference signal on the assumption that GSE grounding
  is implied — the TICD must explicitly record the reference potential
  connection; implicit grounding is not traceable.
- Treating a TICD covering only a subset of required interface categories
  as acceptable for a full functional test — an absent category means an
  entire class of interfaces is uncontrolled, which invalidates the test
  evidence for those interfaces.
- Reusing a TICD from a prior test configuration without issuing a new
  revision when the connector pinout changes — stale TICD content silently
  breaks traceability between the test procedure steps and the physical
  interface.
- Recording a signal as bidirectional when it is in fact a fixed-direction
  line — bidirectional designation requires explicit protocol justification;
  treating every uncertain line as bidirectional inflates the interface
  ambiguity and makes verification harder.

## Behavior contract (gate 3)

The signal-record validation, pin-conflict, duplicate-name, ground-reference,
category-coverage, and direction-conflict logic is exercised by the gate 3
contract test: scripts/test_e1024_ticd.py against
scripts/e1024_ticd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1024_ticd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
