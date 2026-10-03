---
skill_id: security
name: Security & Threat Intelligence
description: "Security review and threat work — threat modeling, vulnerability assessment, penetration test, incident response, OWASP Top 10, LLM Top 10, API Top 10, CVE triage, STRIDE, NIST CSF, SBOM. Auto-loops on any task touching PII, auth, payments or regulated data."
version: 1.0.0
category: security
office: CSO
lead_agent: security-analyst
triggers:
  - security
  - threat
  - vulnerability
  - penetration test
  - audit
  - incident
  - OWASP
  - CVE
  - threat modeling
  - security review
  - risk assessment
  - compliance assessment
  - data breach
  - encryption
  - authentication
  - authorization
  - PII
collaborates_with:
  - compliance-officer
  - data-privacy-officer
  - ai-ethics-reviewer
  - incident-responder
  - enterprise-architect
  - implementer
  - backend-architect
---

# Security & Threat Intelligence -- Domain Dispatcher

> Office: CSO | Lead: security-analyst
> Sub-skills: 8 | Frameworks: OWASP Top 10, NIST CSF, Zero Trust, STRIDE, DREAD

## Purpose

The CSO auto-loop domain -- activates automatically on any task containing security, compliance, PII, or regulated industry signals. This skill provides security analysis, threat modeling, penetration testing, incident response, vulnerability scanning, and security architecture design. Unlike raw external security tools, Maxim applies behavioral science to security culture, proactively routes to the right specialist agent, and tags every output with confidence and risk signals.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| regulatory compliance, audit prep, policy enforcement | compliance-officer | compliance-officer/SKILL.md |
| ethical hacking, bug bounty, vulnerability exploitation | ethical-hacker | ethical-hacker/SKILL.md |
| incident management, containment, post-incident review | incident-responder | incident-responder/SKILL.md |
| penetration testing, offensive security, vulnerability testing | penetration-tester | penetration-tester/SKILL.md |
| secure system design, zero trust architecture, encryption design | security-architect | security-architect/SKILL.md |
| security audit, risk assessment, controls validation | security-auditor | security-auditor/SKILL.md |
| threat analysis, threat intelligence, attack pattern mapping | threat-analyst | threat-analyst/SKILL.md |
| vulnerability scan, CVE monitoring, dependency check | vulnerability-scanner | vulnerability-scanner/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-security` or `/mxm-cso`
- Task contains keywords: security, threat, vulnerability, penetration test, audit, incident, OWASP, CVE, encryption, authentication, authorization, PII, data breach, risk assessment
- CSO auto-loop triggers: any task containing security, compliance, PII, or regulated industry signals -- no explicit request needed
- Other Maxim skills proactively loop here: engineering (code security review), testing (security testing), compliance (security dimension of violations), studio-operations (infrastructure security)

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Ethics gate: `ethics_required: true` on `penetration-tester` and `ai-ethics-reviewer` -- engagement authorization required before offensive testing; AI outputs require ethics review before deployment
- Frameworks: OWASP Top 10, NIST Cybersecurity Framework, Zero Trust Architecture, STRIDE (threat modeling), DREAD (risk scoring), ISO 27001, MITRE ATT&CK

## External Sources

- Primary: community-packs/claude-skills-library/engineering-team/senior-security (security architecture, threat modeling, compliance)
- Secondary: community-packs/claude-skills-library/engineering-team/senior-secops (incident response, SecOps)
- Secondary: community-packs/claude-skills-library/engineering-team/incident-commander (incident management)
- Secondary: community-packs/claude-skills-library/ra-qm-team/ (ISMS, ISO 27001, risk management, audit frameworks)
- Conflict resolution: Maxim ALWAYS WINS

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
