---
name: e1011-safety
description: "Use when assess HFE safety requirements for a spacecraft operations
  catalogue under ECSS-E-ST-10-11C §4.6.3: categorize each operation by hazard
  criticality (critical, high, medium, low), verify that human-error prevention
  measures — confirmation steps, interlocks, reversibility checks, crew notification,
  dual verification — are present at the level each criticality demands, check that
  irreversible high-consequence operations carry maximum protection, confirm
  safety-critical operator interfaces provide clear state cues and go/no-go criteria,
  and flag every operation whose protection set falls below the minimum for its level.
  Trigger: ecss, e-st-10-system-scope, hfe, human-factors, safety-critical-operations,
  human-error-prevention, interlock, crew-notification."
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
  tags: [ecss, e-st-10-system-scope, hfe, human-factors, safety-critical-operations, human-error-prevention, interlock]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Human Factors Engineering — HFE Safety Requirements (space-systems/ecss/e1011-safety)

Use when the task is to assess whether human-factors engineering (HFE)
safety requirements have been applied to a spacecraft operations
catalogue per ECSS-E-ST-10-11C §4.6.3 — categorizing operations by
hazard criticality, checking that the required human-error prevention
measures are present at each level, and verifying that safety-critical
operator interfaces meet minimum safeguard provisions.

## Domain quick reference

- ECSS-E-ST-10-11C §4.6.3 requires every operation in a catalogue to
  carry a hazard criticality designation and a matched set of
  human-error prevention measures. Four levels are defined: CRITICAL
  (consequence is loss of life or mission-ending, typically
  irreversible), HIGH (major subsystem damage, potentially
  irreversible), MEDIUM (recoverable damage, reversible), and LOW (no
  significant safety consequence). Each operation is placed in exactly
  one level before its required measures are checked.
- Required protection measures scale with criticality. A CRITICAL
  operation demands all five: confirmation step, interlock,
  reversibility check, crew notification, and dual verification. A
  HIGH operation requires the first four (confirmation step, interlock,
  reversibility check, crew notification) but not dual verification. A
  MEDIUM operation requires confirmation step and reversibility check
  only. LOW operations have no mandatory measures under this clause.
- An irreversible operation at HIGH or CRITICAL level is subject to
  the CRITICAL protection set regardless of its nominal criticality
  designation, because the consequence of an error cannot be undone.
  This is a separate check from the nominal measures check; an
  irreversible HIGH operation that satisfies HIGH-level measures may
  still be underprotected.
- Safety-critical operator interfaces (CRITICAL and HIGH operations)
  must additionally provide clear system-state cues (visual or auditory
  indication of hazardous states) and documented go/no-go criteria.
  Absence of either is a distinct finding type, independent of the
  protection-set check.

## Workflow

1. Inventory every operation in the catalogue and assign it a hazard
   criticality level (CRITICAL, HIGH, MEDIUM, or LOW) based on
   consequence severity and reversibility. Any operation without a
   valid criticality designation must be rejected before the assessment
   proceeds; it cannot be treated as LOW by default.
2. For each operation, retrieve the set of human-error prevention
   measures on record and compare it against the minimum set required
   for its criticality level. Record each absent measure as a finding
   of type MISSING_MEASURE, naming the specific measure and the level
   that requires it.
3. For each CRITICAL or HIGH operation, verify the operator interface
   carries clear system-state cues and documented go/no-go criteria.
   Absence of state cues generates a MISSING_STATE_CUES finding;
   absence of go/no-go criteria generates a MISSING_GO_NOGO finding.
   These two findings are independent and must both be checked.
4. For every irreversible CRITICAL or HIGH operation, confirm the full
   CRITICAL-level protection set is present. Record any gap as an
   IRREVERSIBLE_UNDERPROTECTED finding; this supplements any
   MISSING_MEASURE findings from step 2 and is not merged with them.
5. Aggregate all findings per operation. An operation is HFE-safety-
   compliant only when all four finding types — MISSING_MEASURE,
   MISSING_STATE_CUES, MISSING_GO_NOGO, IRREVERSIBLE_UNDERPROTECTED
   — are absent.
6. Report the catalogue-level summary: number of operations per
   criticality level, total findings per type, and the list of
   non-compliant operations with their open findings.

## Pitfalls

- Collapsing "no finding at its nominal criticality" into compliance
  for an irreversible HIGH operation — the irreversibility check in
  step 4 is separate from the nominal measures check and catches
  cases where a HIGH operation satisfies all HIGH-level measures but
  still lacks the full CRITICAL-level protection that irreversibility
  demands.
- Treating a MISSING_GO_NOGO finding as redundant when a MISSING_MEASURE
  finding is already raised for the same operation — the interface
  requirements (step 3) are independent of the protection-set check
  (step 2) and both must be reported.
- Assigning a LOW criticality level to an irreversible operation to
  avoid the CRITICAL protection requirements — criticality must reflect
  actual consequence severity; a HIGH or CRITICAL consequence that is
  also irreversible does not become LOW by re-labelling.
- Reading an empty findings list as "assessed and compliant" when the
  operation record carries no criticality designation — an operation
  without a level must be flagged as unassessable, not silently treated
  as passing.

## Behavior contract (gate 3)

The criticality categorization, required-measures check, interface
requirements check, and irreversibility protection check are exercised
by the gate 3 contract test: scripts/test_e1011_safety.py against
scripts/e1011_safety_logic.py (stdlib unittest, offline). Run:

    python3 scripts/test_e1011_safety.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
