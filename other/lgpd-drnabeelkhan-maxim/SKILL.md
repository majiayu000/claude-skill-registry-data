---
skill_id: lgpd
name: LGPD (Lei Geral de Proteção de Dados — Brazil)
version: 1.0.0
category: security-compliance
type: framework
frameworks: []
triggers:
  - apply lgpd
  - use lgpd framework
  - lgpd analysis
collaborates_with:
  - compliance-officer
  - legal-compliance-checker
  - data-architect
  - security-architect
ethics_required: true
priority: medium
tags: [security-compliance, framework]
created: 2026-07-08
updated: 2026-07-08
---

# LGPD (Lei Geral de Proteção de Dados — Brazil)

## Purpose
Apply LGPD to govern data privacy and protection for Brazil, establishing lawful bases for processing personal data and aligning with ANPD regulatory expectations.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `lgpd` |
| Category | Security & Compliance |
| Version | 1.0.0 |
| Owner | Brazil / ANPD (Autoridade Nacional de Proteção de Dados) |
| Maturity | Established (2020) |
| Primary References | Lei Geral de Proteção de Dados |

## Prompt Template
```
You are applying the LGPD (Lei Geral de Proteção de Dados) framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: security & compliance
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Identify**: What aspect of LGPD applies to this situation?
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
□ All recommendations align with LGPD principles
□ Ethical considerations have been evaluated
□ Stakeholder impacts have been considered
□ Next steps are clear and actionable
```

## Core Principles
LGPD requires a valid legal basis for processing personal data:
- **Consent**: Explicit consent of data subject
- **Legal Obligation**: Compliance with legal or regulatory obligation
- **Public Policy**: Execution of public policies
- **Research**: Research by public body
- **Contract**: Execution of contract with data subject
- **Legitimate Interest**: Based on controller's legitimate interest

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|----------------|
| LATAM Privacy Compliance | Assess processing against LGPD legal bases | Compliant Brazilian data-handling posture |
| Regulatory Alignment | Align practices with ANPD expectations | Reduced regulatory exposure |
| Data Classification | Classify personal and sensitive data | Clear data inventory and handling rules |
| Privacy by Design | Embed privacy controls into system design | Privacy-protective architecture |

## Reference Materials
- [Lei Geral de Proteção de Dados](https://www.gov.br/anpd/pt-br) - Brazil / ANPD (Autoridade Nacional de Proteção de Dados)

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
- Validate that recommendations clearly map back to LGPD principles
- Review one real example and one edge case before adopting the output
- Confirm stakeholder, ethical, and operational constraints were considered
- Document adjustments made when the framework needed adaptation for context

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
