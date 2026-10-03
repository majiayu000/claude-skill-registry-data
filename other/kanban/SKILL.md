---
skill_id: kanban
name: Kanban
version: 1.0.0
category: project-management
type: framework
frameworks: []
triggers:
  - apply kanban
  - use kanban framework
  - kanban analysis
collaborates_with:
  - sprint-prioritizer
  - project-shipper
  - experiment-tracker
  - studio-producer
ethics_required: false
priority: medium
tags: [project-management, framework]
created: 2026-03-14
updated: 2026-03-14
---

# Kanban

## Purpose
Apply Kanban to guide decision-making, structure analysis, and improve outcomes in relevant contexts.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `kanban` |
| Category | Project Management |
| Version | 1.0.0 |
| Owner | Toyota (adapted for software) |
| Maturity | Established (1940s, software 2000s) |
| Primary References | Visual Workflow Management |

## Prompt Template
```
You are applying the Kanban framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: project management
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Identify**: What aspect of Kanban applies to this situation?
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
□ All recommendations align with Kanban principles
□ Ethical considerations have been evaluated
□ Stakeholder impacts have been considered
□ Next steps are clear and actionable
```

## Core Principles
- **Foundation**: Kanban provides structured approach to project management
- **Application**: Use when facing decisions requiring project management guidance
- **Adaptation**: Customize application to specific context while maintaining core integrity
- **Documentation**: Record how framework was applied and outcomes achieved

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|----------------|
| Strategic Planning | Apply Kanban to structure analysis | Clearer priorities and rationale |
| Problem Solving | Use framework to break down complex issues | Systematic approach to solutions |
| Team Alignment | Share framework language with stakeholders | Common understanding and vocabulary |
| Documentation | Record framework application in decisions | Audit trail and knowledge transfer |

## Reference Materials
- [Visual Workflow Management](https://kanban.zone/) - Toyota (adapted for software)

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
- ALWAYS act in the best interest of stakeholders
- NEVER misrepresent the framework's capabilities or limitations
- ALWAYS disclose when framework guidance is being applied

## Success Metrics
- **Clarity**: Framework application produces clearer decision rationale
- **Consistency**: Similar situations receive similar framework-guided analysis
- **Stakeholder Alignment**: Framework language improves cross-functional understanding
- **Outcome Quality**: Decisions show improved consideration of relevant factors
- **Learning**: Framework application generates insights for future improvement

## Related Skills
- *No directly related skills defined*

## Testing Strategy
- Validate that recommendations clearly map back to Kanban principles
- Review one real example and one edge case before adopting the output
- Confirm stakeholder, ethical, and operational constraints were considered
- Document adjustments made when the framework needed adaptation for context

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
