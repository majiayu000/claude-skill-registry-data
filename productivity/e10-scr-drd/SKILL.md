---
name: e10-scr-drd
description: "Use when preparing a System Concept Report (SCR) for a European space project per ECSS-E-ST-10C Annex C: validate that the required sections (candidate concepts, trade summary, feasibility assessment, recommended concept) are present, that every candidate concept carries a description, that the trade summary scores every candidate against all trade criteria (technical, programmatic, cost, risk), that every candidate carries a valid feasibility verdict, and that the recommended concept is a known candidate that is not itself flagged not_feasible before the SCR is handed off at the end of phase 0/A. Trigger: scr, system concept report, annex c, e-st-10c annex c, candidate concepts, trade summary, trade-off analysis, feasibility assessment, drd, concept selection, down-select."
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
  tags: [ecss, e-st-10c, annex-c, scr, system-concept-report, drd, trade-off]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Concept Report (space-systems/ecss/e10-scr-drd)

Use when the task is producing or checking the System Concept Report
(SCR) for a European space project against the ECSS-E-ST-10C Annex C
document requirements definition (DRD), covering the candidate
concepts traded during phase 0/A and the concept recommended for
carry-forward.

## Domain quick reference

- ECSS-E-ST-10C Annex C defines the DRD for the SCR: a document
  produced during phase 0/A that captures the candidate system
  concepts developed to satisfy the mission stated in the Mission
  Description Document (see the sibling e10-mdd-drd leaf), the
  trade-off performed among them, and the concept recommended to
  carry forward into system/segment requirements (see the sibling
  e10-req-analysis leaf).
- Four content areas are mandatory: candidate concepts (the options
  developed, each with a description), the trade summary (each
  candidate scored against every trade criterion), the feasibility
  assessment (a verdict per candidate), and the recommended concept
  (the single candidate selected to carry forward).
- Trade-off scoring covers four criteria: technical, programmatic,
  cost, and risk. A candidate with no scored entry for one of these
  criteria has not been through a complete trade.
- Feasibility verdicts are one of feasible, feasible_with_risk, or
  not_feasible. A not_feasible candidate is a normal and expected
  trade outcome (it documents why a concept was screened out) - it
  only blocks the SCR if it is the concept actually recommended, or if
  a candidate has no verdict at all.
- The SCR is an input to the concept-selection milestone; an
  incomplete SCR (missing section, a candidate concept with no
  description, a trade with unscored criteria, a candidate with no or
  an invalid feasibility verdict, or a recommendation that names an
  unknown or infeasible concept) is not ready to support down-select.

## Workflow

1. Assemble the SCR as a dict with the four required sections:
   candidate_concepts, trade_summary, feasibility_assessment,
   recommended_concept.
2. Run missing_sections to confirm none of the four are absent or
   empty; resolve any gap before continuing.
3. Run incomplete_concepts against candidate_concepts to confirm every
   candidate carries a description; resolve any gap.
4. Run missing_trade_criteria against trade_summary and the candidate
   concept ids to confirm every candidate is scored against all four
   trade criteria; resolve any gap.
5. Run classify_feasibility against feasibility_assessment and the
   candidate concept ids to confirm every candidate has a valid
   verdict; resolve any invalid or missing verdict.
6. Run validate_recommendation against recommended_concept, the
   candidate concept ids, and feasibility_assessment to confirm the
   recommendation names a known, assessed candidate that is not
   not_feasible.
7. Combine steps 2-6 with build_completeness_report and read the
   verdict from drd_gate_verdict before handing the SCR to the
   concept-selection milestone.

## Pitfalls

- Listing a candidate concept without a description, which leaves the
  trade-off without a documented basis for its score.
- Scoring a candidate against only some of the four trade criteria
  (technical, programmatic, cost, risk), which makes the trade summary
  look complete while actually being partial.
- Recording a feasibility verdict outside feasible /
  feasible_with_risk / not_feasible (or inventing a fifth verdict),
  which strands the candidate outside the categories downstream
  concept selection relies on.
- Treating a not_feasible candidate anywhere in the set as an SCR
  blocker - it is only a blocker when it is the recommended concept,
  or when a candidate is missing a verdict entirely.
- Recommending a concept id that does not appear in candidate_concepts,
  or that has no feasibility assessment on record.

## Behavior contract (gate 3)

The section-completeness, candidate-concept, trade-criteria-coverage,
feasibility-classification, and recommendation-validation logic is
exercised by the gate 3 contract test: scripts/test_e10_scr_drd.py
against scripts/e10_scr_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e10_scr_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
