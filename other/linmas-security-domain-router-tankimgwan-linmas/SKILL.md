---
name: linmas-security-domain-router
description: Security domain routing skill for choosing the right specialist workflow across secure coding, architecture, response, operations, cloud, threat, blockchain, and compliance work.
triggers:
  - security router
  - choose security skill
  - security domain
---
# Security Domain Router

## Best fit

Use this skill when the user needs help choosing the right security specialist workflow, or when the request spans more than one security domain.

## Use another skill when

Do not use this skill when a request clearly belongs to one specialist skill such as `linmas-secure-code-reviewer` or `linmas-incident-triage-lead`.

## Operating guardrails

- Authorized security testing only.
- Defensive security, incident response, research, and authorized CTF contexts are in scope.
- Do not help with destructive attacks, denial-of-service, stealth for malicious use, mass exploitation, or supply chain compromise.

## Intake checklist

Before routing, confirm:
- whether the task is code review, architecture, cloud, incident, detection, intelligence, compliance, blockchain, or exploit validation
- whether the user already named the environment, target, or framework
- whether the request spans one domain or multiple domains
- whether the user needs a specialist response or just help picking the right specialist

## Output contract

Default response shape:
1. Best-fit skill recommendation
2. Why it fits
3. Alternate skill if scope changes
4. Missing inputs to ask for next

## Routing heuristics

- Route directly when the user clearly names one domain and one objective.
- Offer one alternate skill when the scope could plausibly shift.
- Keep multi-domain requests narrow by identifying the first specialist that should lead.
- Ask for environment, target, or framework details when those affect skill choice.

## Next questions to ask

- What system, environment, or codebase is in scope?
- Is the need mainly review, design, incident handling, detection, or validation?
- Does the request stay within one domain or cross into another specialist area?

## Routing guide

Choose `linmas-secure-code-reviewer` for secure SDLC, threat modeling, secure review, scanner tuning, and developer enablement.
Choose `linmas-secure-systems-architect` for cross-system security design and control boundaries.
Choose `linmas-smart-contract-reviewer` for blockchain, smart contract, and Web3 security review.
Choose `linmas-cloud-hardening-architect` for cloud IAM, network, platform, and landing-zone security design.
Choose `linmas-controls-compliance-reviewer` for control mapping, audit preparation, and evidence-based compliance work.
Choose `linmas-incident-triage-lead` for breach triage, containment, eradication, and recovery workflows.
Choose `linmas-exploit-validation-specialist` for authorized exploit-path validation.
Choose `linmas-security-operations-lead` for operational security monitoring and response readiness.
Choose `linmas-detection-rules-engineer` for alerting logic, SIEM rules, and detection content engineering.
Choose `linmas-threat-research-analyst` for adversary tracking, IOC analysis, and threat reporting.
