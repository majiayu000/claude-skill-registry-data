---
skill_id: fedramp
name: FedRAMP
version: 1.0.0
category: security
type: framework
frameworks: []
triggers:
  - apply fedramp
  - use fedramp framework
  - fedramp analysis
collaborates_with:
  - compliance-officer
  - security-auditor
  - infrastructure-maintainer
ethics_required: true
priority: medium
tags: [security, framework]
created: 2026-03-14
updated: 2026-03-14
---

# FedRAMP

## Purpose
Apply FedRAMP to identify, assess, and mitigate security risks in systems, processes, and data handling.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `fedramp` |
| Category | Security |
| Version | 1.0.0 |
| Owner | U.S. General Services Administration |
| Maturity | Established (2011) |
| Primary References | Federal Risk and Authorization Management Program |

## Prompt Template
```
You are applying the FedRAMP framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: security
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Identify**: What aspect of FedRAMP applies to this situation?
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
□ All recommendations align with FedRAMP principles
□ Ethical considerations have been evaluated
□ Stakeholder impacts have been considered
□ Next steps are clear and actionable
```

## Core Principles
- **Foundation**: FedRAMP provides structured approach to security
- **Application**: Use when facing decisions requiring security guidance
- **Adaptation**: Customize application to specific context while maintaining core integrity
- **Documentation**: Record how framework was applied and outcomes achieved

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|----------------|
| Strategic Planning | Apply FedRAMP to structure analysis | Clearer priorities and rationale |
| Problem Solving | Use framework to break down complex issues | Systematic approach to solutions |
| Team Alignment | Share framework language with stakeholders | Common understanding and vocabulary |
| Documentation | Record framework application in decisions | Audit trail and knowledge transfer |

## Reference Materials
- [Federal Risk and Authorization Management Program](https://www.fedramp.gov/) - U.S. General Services Administration

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
- Validate that recommendations clearly map back to FedRAMP principles
- Review one real example and one edge case before adopting the output
- Confirm stakeholder, ethical, and operational constraints were considered
- Document adjustments made when the framework needed adaptation for context

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
