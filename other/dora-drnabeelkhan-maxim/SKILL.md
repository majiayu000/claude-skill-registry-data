---
skill_id: dora
name: DORA (Digital Operational Resilience Act)
version: 1.0.0
category: security-compliance
type: framework
frameworks: []
triggers:
  - apply dora
  - use dora framework
  - dora analysis
collaborates_with:
  - compliance-officer
  - security-architect
  - incident-responder
  - penetration-tester
  - legal-compliance-checker
ethics_required: true
priority: medium
tags: [security-compliance, framework]
created: 2026-07-08
updated: 2026-07-08
---

# DORA (Digital Operational Resilience Act)

## Purpose
Apply DORA to manage ICT risk and operational resilience for EU financial entities, covering governance, incident reporting, resilience testing, third-party risk, and threat intelligence sharing.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `dora` |
| Category | Security & Compliance |
| Version | 1.0.0 |
| Owner | European Union |
| Maturity | Active (Effective January 2025) |
| Primary References | Digital Operational Resilience Act |

## Prompt Template
```
You are applying the DORA (Digital Operational Resilience Act) framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: security & compliance
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Identify**: What aspect of DORA applies to this situation?
2. **Analyze**: Break down the problem using framework principles:
   - Apply relevant framework principles to the context
3. **Synthesize**: Combine insights into actionable recommendations
4. **Validate**: Check recommendations against framework guidelines

OUTPUT STRUCTURE:
- Framework Application: Which principles were used and why
- Analysis: Step-by-step application to the specific context
- Recommendations: Prioritized actions based on framework guidance
- Limitations: Any constraints or assumptions in the application

QUALITY CHECKS:
□ All recommendations align with DORA principles
□ Ethical considerations have been evaluated
□ Stakeholder impacts have been considered
□ Next steps are clear and actionable
```

## Core Principles
DORA rests on five pillars:
- **ICT Risk Management**: Governance frameworks and risk strategies
- **ICT Incident Reporting**: Classification and mandatory reporting of incidents
- **Digital Operational Resilience Testing**: Threat-Led Penetration Testing (TLPT)
- **ICT Third-Party Risk**: Contractual requirements for critical ICT providers
- **Information Sharing**: Threat intelligence sharing between financial entities

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|----------------|
| ICT Risk Management | Establish governance frameworks and risk strategies | Structured, board-accountable risk posture |
| ICT Incident Reporting | Classify and report incidents on mandatory timelines | Regulator-ready incident notifications |
| Resilience Testing | Run Threat-Led Penetration Testing (TLPT) exercises | Evidence of tested operational resilience |
| Third-Party Risk | Review contracts for critical ICT providers | Compliant provider agreements and exit plans |

## Reference Materials
- [Digital Operational Resilience Act](https://www.digital-operational-resilience-act.com/) - European Union

## Usage Guidelines
- **Start with context**: Clearly define the problem space before applying framework
- **Adapt, don't adopt**: Customize framework application to your specific situation
- **Document decisions**: Record how and why framework principles were applied
- **Review outcomes**: Evaluate results to improve future framework application
- **Share learnings**: Contribute insights back to team knowledge base

## Collaboration Protocol
- Apply independently unless a task explicitly requires another skill or framework
- Use structured handoff format: [Context] -> [Framework Applied] -> [Open Questions] -> [Next Action]

## Ethical Guidelines
- ALWAYS apply principle of least privilege
- NEVER store sensitive data in plaintext or logs
- ALWAYS follow responsible disclosure practices

## Success Metrics
- **Clarity**: Framework application produces clearer decision rationale
- **Consistency**: Similar situations receive similar framework-guided analysis
- **Stakeholder Alignment**: Framework language improves cross-functional understanding
- **Outcome Quality**: Decisions show improved consideration of relevant factors
- **Learning**: Framework application generates insights for future improvement

## Related Skills
- *No directly related skills defined*

## Testing Strategy
- Validate that recommendations clearly map back to DORA principles
- Review one real example and one edge case before adopting the output
- Confirm stakeholder, ethical, and operational constraints were considered
- Document adjustments made when the framework needed adaptation for context

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
