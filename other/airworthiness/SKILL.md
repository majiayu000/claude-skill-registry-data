---
name: airworthiness
description: "Use when scoping transport-category airworthiness certification: determine the certification basis (FAR-25 for FAA programs, CS-25 for EASA programs), decide whether a system needs the 25.1309 safety assessment from its failure-condition severity, select a means of compliance (analysis, test, inspection, similarity), and sequence a type-certification program from application to issue. The mapped scope is transport-category; other categories must be re-scoped. Trigger: FAR-25, CS-25, airworthiness certification, certification basis, means of compliance, type certification, 25.1309 safety assessment, transport category."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
  - id: cs-25
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: far-cs25
  tags: [far-25, cs-25, airworthiness, certification, means-of-compliance, type-certificate]
  version: 0.1.0
  author: Aero Agent Skills
---

# FAR/CS-25 Airworthiness (avionics/far-cs25/airworthiness)

Use when the task is transport-category airworthiness certification:
certification basis, safety assessment applicability, means of
compliance, and type-certification sequencing.

## Domain quick reference

- 14 CFR Part 25 (FAR-25) is the US transport-category airworthiness
  regulation; CS-25 is the EASA certification specification for large
  aeroplanes and mirrors FAR-25 with EU amendments (AMC-25 acceptable
  means of compliance).
- The certification basis names the regulation plus program-specific
  amendments and special conditions.
- 25.1309 requires the safety assessment of systems whose failure
  conditions are catastrophic, hazardous, or major.
- Means of compliance: analysis, test (ground and flight),
  inspection, similarity, and certification-program demonstrations.

## Workflow

1. Identify the airplane category and operating jurisdiction.
2. Determine the certification basis (regulation + amendments +
   special conditions) with the certification authority.
3. For each system, classify failure-condition severity and decide
   whether the 25.1309 safety assessment applies.
4. Agree the means of compliance per area.
5. Sequence the program: application, basis, means of compliance,
   compliance demonstration, issue.

## Pitfalls

- Applying FAR-25/CS-25 outside transport category (re-scope).
- Skipping the safety assessment for a major-or-worse failure
  condition.
- A means of compliance agreed without the certification authority.
- Treating the basis as fixed before amendments and special
  conditions are negotiated.

## Behavior contract (gate 3)

The certification-basis, safety-assessment, and program logic is
exercised by the gate 3 contract test: scripts/test_airworthiness.py
against scripts/airworthiness_logic.py (stdlib unittest, offline).
Run: python3 scripts/test_airworthiness.py

## Compliance

- FAR-25 is US government work (17 U.S.C. 105), quotable with
  citation; CS-25 reproduction authorised with source acknowledged
  (EASA). Paraphrase preferred per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
