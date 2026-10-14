---
name: e10-mdd-drd
description: "Use when generating or validating a Mission Description Document (MDD) for a European space project per ECSS-E-ST-10C Annex B: check that the required sections (objectives, mission statement, mission scenario, constraints) are present, that the mission statement carries an objective/target/timeframe, that the mission scenario phases follow the launch-to-disposal order, and that every constraint is categorised (programmatic, technical, operational, environmental) before the MDD is handed off at MDR. Trigger: mdd, mission description document, annex b, e-st-10c annex b, mission statement, mission scenario, mission constraints, drd, mission definition review, mdr package."
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
  tags: [ecss, e-st-10c, annex-b, mdd, mission-description-document, drd, mdr]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Mission Description Document (space-systems/ecss/e10-mdd-drd)

Use when the task is producing or checking the Mission Description
Document (MDD) for a European space project against the ECSS-E-ST-10C
Annex B document requirements definition (DRD), ahead of the mission
definition review (MDR).

## Domain quick reference

- ECSS-E-ST-10C Annex B defines the DRD for the MDD: a document
  produced early (phase 0) that states what the mission is for and
  under what constraints, before candidate concepts are traded in the
  System Concept Report (see the sibling e10-scr-drd leaf).
- Four content areas are mandatory: objectives (why the mission
  exists), the mission statement (a concise objective/target/timeframe
  triple), the mission scenario (the ordered operational phases from
  launch through disposal), and constraints (the boundaries the
  mission must respect).
- Mission scenario phases follow a fixed canonical order: launch,
  commissioning, operations, disposal. A phase can be omitted, but a
  later phase cannot be listed before an earlier one.
- Constraints are categorised programmatic (budget, schedule),
  technical (launcher, ground segment, interfaces), operational
  (crew, ground station availability), or environmental (orbital
  debris, planetary protection, radiation). A constraint without one
  of these categories is not usable by downstream requirement
  engineering (see the sibling e10-req-analysis leaf).
- The MDD is an input to the MDR package; an incomplete MDD (missing
  section, an unstated mission-statement field, out-of-order scenario
  phases, or an uncategorised constraint) is not ready to support the
  review.

## Workflow

1. Assemble the MDD as a dict with the four required sections:
   objectives, mission_statement, mission_scenario, constraints.
2. Run missing_sections to confirm none of the four are absent or
   empty; resolve any gap before continuing.
3. Run missing_statement_fields against mission_statement to confirm
   it carries objective, target, and timeframe; resolve any gap.
4. Run validate_scenario_order against the mission_scenario phase list
   to confirm phases are drawn from the canonical set and never regress
   to an earlier phase.
5. Run classify_constraints against the constraints list to confirm
   every constraint carries one of the four known categories; disposition
   any constraint flagged invalid before it reaches requirement analysis.
6. Combine steps 2-5 with build_completeness_report and read the
   verdict from drd_gate_verdict before handing the MDD to the MDR
   package.

## Pitfalls

- Treating the mission statement as free text instead of the
  objective/target/timeframe triple the DRD expects, which leaves
  downstream requirement analysis without a traceable source.
- Listing mission scenario phases out of launch-to-disposal order, or
  skipping straight to operations without commissioning when the
  mission actually needs it.
- Leaving a constraint uncategorised (or inventing a fifth category),
  which strands it outside the programmatic/technical/operational/
  environmental buckets requirement analysis and the SEP rely on.
- Declaring the MDD complete because prose sections exist, without
  checking the specific fields the DRD requires inside each section.

## Behavior contract (gate 3)

The section-completeness, mission-statement, scenario-order, and
constraint-classification logic is exercised by the gate 3 contract
test: scripts/test_e10_mdd_drd.py against
scripts/e10_mdd_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e10_mdd_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
