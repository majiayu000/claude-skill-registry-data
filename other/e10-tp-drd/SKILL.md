---
name: e10-tp-drd
description: "Use when you must generate or validate the Technology Plan (TP) for a European space project per ECSS-E-ST-10C Annex E: check the draft TP against the required DRD content blocks, assess each critical/enabling technology's TRL entry (current vs. target TRL, assessment-due date vs. need-by date), roll up the technology development schedule, and decide whether the TP is ready to submit or needs revision. Produces the completeness verdict, per-technology TRL/schedule verdicts, and the overall TP status. Trigger: ecss technology plan, tp drd, trl assessment plan, technology development schedule, technology schedule risk, e-st-10c annex e."
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
  tags: [ecss, e-st-10c, technology-plan, tp-drd, trl-assessment, annex-e]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Technology Plan per DRD (space-systems/ecss/e10-tp-drd)

Use when the task is ECSS-E-ST-10C Annex E: generating or validating a
project's Technology Plan (TP) against its normative DRD content and
checking that the technology maturation schedule it commits to is
internally consistent.

## Domain quick reference

- ECSS-E-ST-10C Annex E is the normative DRD for the Technology Plan:
  it fixes the content blocks the document must carry, not just its
  general topic.
- A TP is only complete once it contains: purpose and scope,
  applicable/reference documents, the critical/enabling technology
  list, the TRL assessment plan and methodology, the technology
  development/maturation schedule, the technology risk assessment,
  backup/alternative solutions for each critical technology, and the
  cross-reference to the technology matrix (Annex F). Missing any of
  these makes the TP incomplete, not merely thin.
- TRL is scored 1-9 per the E-AS-11 (ISO 16290) scale. A technology's
  target TRL for a project gate must be at or above its current TRL —
  a target below the current level is a data error, not a real
  maturation goal.
- Each critical technology's TRL assessment must be due on or before
  the date the design needs its result (typically ahead of PDR or
  CDR). An assessment scheduled to complete after its need-by date is
  a schedule risk that must be flagged before the TP is approved.

## Workflow

1. List the content sections present in the draft TP and check them
   against the DRD with tp_completeness_check; add any section it
   reports missing before proceeding.
2. For each critical/enabling technology, build an entry with
   trl_assessment_entry (technology name, current TRL, target TRL,
   assessment-due date, need-by date) and read its status.
3. Roll up all entries with technology_schedule_verdict to see which
   technologies are on-track versus at risk (TRL regression or
   schedule slip).
4. Combine steps 1 and 3 with tp_status_verdict to get the overall TP
   status before it is submitted at the owning review gate.

## Pitfalls

- Treating the technology matrix cross-reference (Annex F) as
  optional — Annex E requires the TP to point to it explicitly.
- Entering a target TRL lower than the current TRL for a technology;
  that is a data-entry error, not a valid maturation target.
- Scheduling a technology's TRL assessment to complete after the
  milestone that needs its result (e.g. due after PDR) and treating
  the plan as on-track anyway.
- Submitting a TP that is missing a required section (for example, no
  backup/alternative-solutions block) as though it were complete.

## Behavior contract (gate 3)

The completeness, TRL-assessment, and schedule-verdict logic is
exercised by the gate 3 contract test: scripts/test_e10_tp_drd.py
against scripts/e10_tp_drd_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e10_tp_drd.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
