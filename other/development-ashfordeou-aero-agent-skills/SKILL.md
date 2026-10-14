---
name: development
description: "Use when you must develop DO-178C airborne software lifecycle data for avionics items: capture high-level and low-level requirements, maintain bidirectional requirement-to-code trace links, identify derived requirements, and apply design/coding standards scaled to software level. Produce development-phase artifacts (requirements, design, code, trace matrix) for verification, with traceability closure and independent review at levels A and B. Ensure protection and safety assurance trace from top-level system protection needs down to low-level implementation and code, and maintain full coverage of verification results against each requirement and design element. Track verification coverage depth linking each test, analysis, or review outcome to originating requirements. Trigger: DO-178C development, requirements traceability, protection trace, protection assurance, safety assurance trace, verification coverage, derived requirements, low-level requirements, coding standards, software design, lifecycle data."
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
  tags: [do-178c, requirements, traceability, derived, development, lifecycle-data]
  version: 0.1.0
  author: Aero Agent Skills
---

# DO-178C Development (avionics/do178c/development)

Use when the task is DO-178C development-phase work: turning requirements
into verification-ready source code with complete traceability.

## Domain quick reference

- Development process (DO-178C): high-level requirements -> low-level
  requirements -> source code -> object code, with derived requirements
  identified at each step.
- Bidirectional traceability is required at every software level (A-E):
  high-level requirements to low-level requirements, low-level
  requirements to source code, source code to object code.
- Derived requirements: requirements added during development (design
  decisions, safety analysis output) with no direct higher-level source;
  they must be identified and justified.
- Design and coding standards are project-defined; the process must
  produce the data the standards demand.
- Levels A and B require independent review of development data,
  including the trace matrix.

## Workflow

1. Confirm the software level (DAL) from the planning phase.
2. Capture high-level requirements with unique identifiers; each must be
   verifiable and testable.
3. Derive low-level requirements from the high-level set; flag derived
   items explicitly.
4. Implement source code against the low-level requirements under the
   project coding standard.
5. Build the trace matrix across levels; identify orphans and derived
   items.
6. Gate on traceability closure; levels A/B add independent review.

## Pitfalls

- Derived requirements left unidentified (silent orphans).
- One-way traceability (requirements to code without code to
  requirements).
- Non-verifiable requirements that fail later at verification.
- No coding standard defined before code is written.

## Behavior contract (gate 3)

The traceability-completeness logic is exercised by the gate 3 contract
test: scripts/test_development.py against scripts/development_logic.py
(stdlib unittest, offline). Run: python3 scripts/test_development.py

## Compliance

- Standards referenced, not reproduced: DO-178C / ARP4754A / ARP4761A text
  is proprietary (RTCA/SAE); summary-only per standards-map.yaml and brief 06.
- Revision note: ARP4754B (2023) supersedes ARP4754A; this skill keys to
  ARP4754A as the certification-baseline revision (FAA AC 20-174 cites A);
  see standards-map.yaml arp4754a.revision_decision.
- compliance: STANDARDS-REF, gated: false.
