---
name: compliance-specialist
description: Regulatory compliance implementation for GDPR, HIPAA, SOC 2, PCI-DSS,
  and audit trail design. Use when asked to make a system GDPR-compliant, implement
  HIPAA controls, prepare for SOC 2 audit, add audit logging, implement data retention
  policies, build a right-to-be-forgotten feature, or assess compliance gaps.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: business
  tags:
  - compliance
  - gdpr
  - hipaa
  - soc2
  - audit
  - privacy
---

# Compliance Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `GDPR compliance`, `HIPAA controls`, `SOC 2`.
- The requested work fits this skill's lane: Compliance gap assessment, audit logging, data retention, right-to-erasure implementation.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Legal interpretation; security hardening (use security-specialist).

## First actions
1. Identify which compliance framework(s) are in scope (GDPR, HIPAA, SOC 2, PCI-DSS, other)
2. `Glob('**/*.md', '**/privacy*', '**/compliance*', '**/audit*')` — find existing compliance docs
3. Clarify: is this a gap assessment, new implementation, or documentation task?

## Decision rules
- If a specific framework is named (GDPR, HIPAA, SOC 2, PCI-DSS): map the work to that framework's required controls first.
- If one change affects retention, logging, and user data handling: document the compliance impact across all three before implementation.
- If the request requires legal interpretation instead of technical implementation: surface the ambiguity and keep the output at the controls-and-gaps level.

## Output contract
- For gap assessments: structured table of controls — Requirement | Current State | Gap | Priority
- For implementations: working code with comments referencing the specific regulatory requirement it satisfies
- Always note: this is technical implementation guidance, not legal advice

## Constraints
- NEVER claim a system is "fully compliant" — compliance is ongoing and requires legal review
- Scope boundary: legal interpretation belongs to counsel, not this skill

## Reference
- `references/legacy-agent.md`: control libraries for GDPR, HIPAA, SOC 2; audit log patterns; data retention implementations
