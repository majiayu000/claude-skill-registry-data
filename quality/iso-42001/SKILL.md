---
skill_id: iso-42001
name: ISO 42001 (AI Management System)
version: 1.0.0
category: security-compliance
type: framework
frameworks: []
triggers:
  - apply iso 42001
  - use iso-42001 framework
  - ai management system audit
  - aims certification analysis
collaborates_with:
  - security-analyst
  - compliance-orchestrator
  - enterprise-architect
  - data-architect
  - governance-specialist
ethics_required: true
priority: high
tags: [security-compliance, framework]
created: 2026-07-08
updated: 2026-07-08
---

# ISO 42001 (AI Management System)

## Purpose
Apply ISO/IEC 42001 to establish, operate, and continually improve an AI Management System (AIMS) — giving an organization a certifiable, clause-based structure for governing AI across its full lifecycle.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `iso-42001` |
| Category | Security & Compliance |
| Version | 1.0.0 |
| Owner | ISO/IEC JTC 1/SC 42 |
| Maturity | Established (Published December 2023) |
| Primary References | International standard for establishing AI management systems (AIMS) |

## Key Clauses
| Clause | Area | Description |
|--------|------|-------------|
| 4 | Context of Organization | Understanding AI impact on stakeholders |
| 5 | Leadership | Top management commitment and AI policy |
| 6 | Planning | Risk and opportunity management for AI |
| 7 | Support | Resources, competence, awareness |
| 8 | Operation | AI system lifecycle controls |
| 9 | Performance Evaluation | Monitoring, measurement, audits |
| 10 | Improvement | Nonconformity and continual improvement |

## Prompt Template
```
You are applying the ISO 42001 (AI Management System) framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: security & compliance
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Identify**: Which ISO 42001 clause(s) (4–10) govern this situation?
2. **Analyze**: Assess the AIMS against clause requirements:
   - Context, leadership, planning, support, operation, performance evaluation, improvement
3. **Synthesize**: Combine findings into an AIMS establishment or audit plan
4. **Validate**: Check against certification readiness and continual-improvement expectations

OUTPUT STRUCTURE:
- Framework Application: Which clauses were used and why
- Analysis: Clause-by-clause conformity assessment
- Recommendations: Prioritized AIMS actions
- Limitations: Assumptions and scope of the management system

QUALITY CHECKS:
□ Clause mapping is complete and defensible
□ Leadership commitment and AI policy are addressed
□ Ethical considerations have been evaluated
□ Continual-improvement loop is defined
```

## Core Principles
- **Foundation**: ISO 42001 provides a certifiable, clause-based management system for AI governance.
- **Application**: Use when standing up, auditing, or certifying an organization's AI governance structure.
- **Adaptation**: Scope the AIMS to the organization's actual AI footprint and risk profile.
- **Documentation**: Maintain records, audit trail, and nonconformity logs as management-system evidence.

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|------------------|
| AI system certification | Map controls to clauses 4–10 | Certification-ready AIMS |
| AI control implementation | Operationalize lifecycle controls | Governed AI operations |
| AI governance structure | Define leadership and policy | Clear accountability model |
| AI data requirements | Align data controls to the AIMS | Defensible data posture |
| AI organizational alignment | Embed AIMS into enterprise architecture | Coherent AI operating model |

## Reference Materials
- [ISO/IEC 42001 — standard page](https://www.iso.org/standard/81230.html) — ISO/IEC JTC 1/SC 42

## Usage Guidelines
- **Start with context (Clause 4)**: Define stakeholders and AI impact before designing controls.
- **Adapt, don't adopt**: Scale the AIMS to the organization's risk and AI maturity.
- **Document decisions**: Record clause conformity and management-review outputs.
- **Review outcomes**: Run the performance-evaluation and improvement loop on a cadence.
- **Share learnings**: Feed audit findings back into continual improvement.

## Collaboration Protocol
- Apply independently unless a task explicitly requires another skill or framework.
- Use structured handoff format: [Context] -> [Framework Applied] -> [Open Questions] -> [Next Action]
- Auto-loop the security-analyst (CSO) on regulated-AI governance tasks.

## Ethical Guidelines
- ALWAYS prioritize responsible AI governance and stakeholder impact.
- NEVER treat certification as a substitute for genuine oversight.
- ALWAYS maintain a transparent audit trail for AI decisions.

## Success Metrics
- **Clarity**: Clause mapping produces a defensible governance rationale.
- **Consistency**: Similar AI systems receive similar clause-based treatment.
- **Stakeholder Alignment**: Framework language improves cross-functional understanding.
- **Outcome Quality**: Decisions show improved governance, monitoring, and improvement discipline.
- **Learning**: Audits generate reusable AIMS insight.

## Related Skills
- `compliance` (Maxim compliance skill layer)
- `enterprise-architecture` (AI organizational alignment)

## Testing Strategy
- Validate that recommendations clearly map back to ISO 42001 clauses 4–10.
- Review one real example and one edge case before adopting the output.
- Confirm stakeholder, ethical, and certification-readiness constraints were considered.
- Document adjustments made when the framework needed adaptation for context.

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
