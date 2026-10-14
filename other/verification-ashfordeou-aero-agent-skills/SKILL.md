---
name: verification
description: "Use when you must verify DO-178C airborne software against its requirements: review software architecture, design, and code, run requirements-based tests, and analyze structural coverage at the depth the software level demands: A requires MC/DC, B decision coverage, C statement coverage, D and E require none. Determine whether verification must be independent, which applies at levels A and B, and produce the verification results, coverage analysis, and review records the software verification process must deliver. Trigger: DO-178C verification, MC/DC coverage, decision coverage, statement coverage, structural coverage analysis, requirements-based testing, independent verification."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: do-178c
    reference-only: true
  - id: arp4754a
    reference-only: true
  - id: arp4761a
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: do178c
  tags: [do-178c, verification, coverage, independence, testing]
  version: 0.1.0
  author: Aero Agent Skills
---

# DO-178C Verification (avionics/do178c/verification)

Use when the task is DO-178C verification-phase work: proving the software
meets its requirements and analyzing structural coverage to the depth the
software level demands.

## Domain quick reference

- Verification (DO-178C): review of architecture, design, and code, plus
  requirements-based testing; every requirement is exercised.
- Structural coverage depth scales with level: A = MC/DC, B = decision,
  C = statement, D/E = none required.
- Coverage must reach 100% of the required metric for the level.
- Independence: levels A and B require independent verification; C/D/E
  allow the developer's organization to verify.
- Verification results, problem reports, and coverage analysis are the
  outputs the process must deliver.

## Workflow

1. Confirm the software level and the applicable coverage depth.
2. Review software architecture, design, and code against requirements.
3. Run requirements-based tests; confirm every requirement is exercised.
4. Analyze structural coverage at the required depth (A MC/DC, B
   decision, C statement).
5. Levels A/B: perform the independent verification activities.
6. Produce verification results, coverage analysis, and review records.

## Pitfalls

- Coverage depth mismatched to level (A requires MC/DC, not statement).
- Structural coverage below 100% of the required metric.
- Requirements-based testing without exercising every requirement.
- Missing independence at level A or B.

## Behavior contract (gate 3)

The coverage-depth and independence logic is exercised by the gate 3
contract test: scripts/test_verification.py against
scripts/verification_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_verification.py

## Compliance

- Standards referenced, not reproduced: DO-178C / ARP4754A / ARP4761A text
  is proprietary (RTCA/SAE); summary-only per standards-map.yaml and brief 06.
- Revision note: ARP4754B (2023) supersedes ARP4754A; this skill keys to
  ARP4754A as the certification-baseline revision (FAA AC 20-174 cites A);
  see standards-map.yaml arp4754a.revision_decision.
- compliance: STANDARDS-REF, gated: false.
