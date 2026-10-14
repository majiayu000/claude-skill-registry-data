---
name: e10-sep
description: "Use when you must produce or maintain the System Engineering Plan (SEP) for a European space project per ECSS-E-ST-10C: decide when a lifecycle event forces the SEP to be revised, check that lower-level plans (product assurance, AIV, risk management, configuration management, software management) stay baseline-consistent with the SEP, and assemble the SEP-derived support package the SE function hands the project manager (PM) at each review gate. Produces the maintenance-trigger verdict, the per-plan consistency verdict, and the review support package. Trigger: ecss sep, system engineering plan, sep baseline, sep maintenance, lower-level plan consistency, review support package, e-st-10c 5.1."
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
  tags: [ecss, e-st-10c, sep, system-engineering-plan, plan-consistency, review-support]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS System Engineering Plan (space-systems/ecss/e10-sep)

Use when the task is ECSS-E-ST-10C clause 5.1 system engineering
planning: keeping the SEP current, checking lower-level plans against
its baseline, and preparing the SEP-derived package that backs the PM
at project reviews.

## Domain quick reference

- ECSS-E-ST-10C §5.1 requires the SEP to be produced early in the
  project and then maintained: it is revised and rebaselined whenever
  the lifecycle event demands it, not written once and left static.
- Typical maintenance triggers: a phase transition, a requirements
  baseline change, an approaching review gate, or a change to the
  project organisation. Routine status reporting alone does not force
  a revision.
- Lower-level plans (product assurance, AIV, risk management,
  configuration management, software management) each derive from the
  SEP; every one of them must carry a baseline tag consistent with the
  SEP's current baseline, or it is flagged for update.
- The SE function supports the PM at every project review gate (MDR,
  PRR, SRR, PDR, CDR, QR, AR, FRR, CRR, ER) with a package drawn from
  the SEP: task status, WBS/schedule status, risk status, and
  organisation/interface status, plus items specific to the gate (for
  example design-baseline consistency at PDR/CDR, verification closure
  at QR/AR/FRR).

## Workflow

1. Evaluate each pending lifecycle event with
   sep_maintenance_trigger and revise/rebaseline the SEP before any
   event that returns True.
2. Collect the current baseline tag for the SEP and for each
   lower-level plan (product assurance, AIV, risk management,
   configuration management, software management).
3. Check each lower-level plan for consistency with the SEP baseline
   using lower_plan_consistency; update any plan flagged
   inconsistent-update-required.
4. Assemble the review support package for the upcoming gate with
   review_support_package.
5. Combine steps 3 and 4 with sep_status_verdict to confirm the SEP is
   consistent and the PM's support package is ready before the review.

## Pitfalls

- Treating the SEP as a one-time deliverable instead of a maintained
  plan revised at phase transitions and baseline changes.
- Letting a lower-level plan (especially the AIV or risk management
  plan) drift onto an older baseline than the SEP.
- Handing the PM a generic status pack instead of the gate-specific
  items (for example skipping verification closure status ahead of
  QR/AR/FRR).
- Confusing plan production (writing the SEP once) with plan
  maintenance (keeping it and its dependents baseline-consistent).

## Behavior contract (gate 3)

The maintenance-trigger, plan-consistency, and review-support-package
logic is exercised by the gate 3 contract test:
scripts/test_e10_sep.py against scripts/e10_sep_logic.py (stdlib
unittest, offline). Run:
python3 scripts/test_e10_sep.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
