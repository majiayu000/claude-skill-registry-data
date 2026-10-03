---
skill_id: cobit
name: COBIT
version: 1.0.0
category: enterprise-architecture
type: framework
frameworks: []
triggers:
  - apply cobit
  - use cobit framework
  - cobit analysis
collaborates_with:
  - governance-specialist
  - compliance-officer
  - enterprise-architect
  - infrastructure-maintainer
ethics_required: false
priority: medium
tags: [enterprise-architecture, framework]
created: 2026-03-14
updated: 2026-03-14
---

# COBIT

## Purpose
Apply COBIT to design scalable, maintainable, and interoperable enterprise systems and solutions.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `cobit` |
| Category | Enterprise Architecture |
| Version | 1.0.0 |
| Owner | ISACA |
| Maturity | Established (1996, COBIT 2019) |
| Primary References | Control Objectives for Information and Related Technologies |

## Prompt Template
```
You are applying the COBIT framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: enterprise architecture
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Identify**: What aspect of COBIT applies to this situation?
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
□ All recommendations align with COBIT principles
□ Ethical considerations have been evaluated
□ Stakeholder impacts have been considered
□ Next steps are clear and actionable
```

## Core Principles
- **Foundation**: COBIT provides structured approach to enterprise architecture
- **Application**: Use when facing decisions requiring enterprise architecture guidance
- **Adaptation**: Customize application to specific context while maintaining core integrity
- **Documentation**: Record how framework was applied and outcomes achieved

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|----------------|
| Strategic Planning | Apply COBIT to structure analysis | Clearer priorities and rationale |
| Problem Solving | Use framework to break down complex issues | Systematic approach to solutions |
| Team Alignment | Share framework language with stakeholders | Common understanding and vocabulary |
| Documentation | Record framework application in decisions | Audit trail and knowledge transfer |

## Reference Materials
- [Control Objectives for Information and Related Technologies](https://www.isaca.org/cobit) - ISACA

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
- ALWAYS consider long-term maintainability and technical debt
- NEVER recommend vendor lock-in without clear justification
- ALWAYS document architectural decisions and tradeoffs

## Success Metrics
- **Clarity**: Framework application produces clearer decision rationale
- **Consistency**: Similar situations receive similar framework-guided analysis
- **Stakeholder Alignment**: Framework language improves cross-functional understanding
- **Outcome Quality**: Decisions show improved consideration of relevant factors
- **Learning**: Framework application generates insights for future improvement

## Related Skills
- *No directly related skills defined*

## Testing Strategy
- Validate that recommendations clearly map back to COBIT principles
- Review one real example and one edge case before adopting the output
- Confirm stakeholder, ethical, and operational constraints were considered
- Document adjustments made when the framework needed adaptation for context

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
