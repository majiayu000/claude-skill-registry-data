---
skill_id: sox
name: SOX (Sarbanes-Oxley Act)
version: 1.0.0
category: security-compliance
type: framework
frameworks: []
triggers:
  - apply sox
  - use sox framework
  - sarbanes-oxley compliance analysis
  - itgc audit
collaborates_with:
  - security-analyst
  - compliance-orchestrator
  - governance-specialist
  - security-auditor
  - data-architect
ethics_required: true
priority: high
tags: [security-compliance, framework]
created: 2026-07-08
updated: 2026-07-08
---

# SOX (Sarbanes-Oxley Act)

## Purpose
Apply the Sarbanes-Oxley Act to safeguard financial-reporting integrity and IT general controls for public companies — mapping executive certification, internal-control assessment, and IT control areas to auditable evidence.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `sox` |
| Category | Security & Compliance |
| Version | 1.0.0 |
| Owner | U.S. Congress / SEC / PCAOB |
| Maturity | Established (2002) |
| Primary References | Financial reporting integrity and IT controls for public companies |

## Key Sections
| Section | Description |
|---------|-------------|
| Section 302 | CEO/CFO personal certification of financial reports |
| Section 404 | Management assessment of internal controls (ICFR) |
| Section 409 | Real-time disclosure of material events |
| Section 802 | Records retention and destruction penalties |

## IT Controls (ITGC)
| Control Area | Description |
|--------------|-------------|
| Access Controls | Who can access financial systems |
| Change Management | IT system change documentation |
| Computer Operations | Backup, recovery, batch processing |
| Data Center Security | Physical and logical data security |

## Prompt Template
```
You are applying the SOX (Sarbanes-Oxley Act) framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: security & compliance
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Identify**: Which SOX section(s) (302 / 404 / 409 / 802) apply to this situation?
2. **Analyze**: Assess against ITGC control areas:
   - Access controls, change management, computer operations, data center security
3. **Synthesize**: Combine findings into a controls assessment or remediation plan
4. **Validate**: Check against ICFR expectations and records-retention duties

OUTPUT STRUCTURE:
- Framework Application: Which sections and controls were used and why
- Analysis: Control-by-control assessment
- Recommendations: Prioritized remediation actions
- Limitations: Assumptions and scope boundaries

QUALITY CHECKS:
□ Section mapping is complete and defensible
□ ITGC control areas are assessed
□ Ethical considerations have been evaluated
□ Audit trail supports the conclusions
```

## Core Principles
- **Foundation**: SOX ties financial-reporting integrity to demonstrable IT general controls.
- **Application**: Use when assessing controls over financial systems and reporting for public companies.
- **Adaptation**: Scope controls to the systems that affect financial reporting (ICFR boundary).
- **Documentation**: Maintain evidence, change records, and retention logs as audit-ready artifacts.

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|------------------|
| SOX compliance management | Map processes to Sections 302/404/409/802 | Audit-ready compliance posture |
| Regulatory review | Cross-check disclosures and certifications | Reduced regulatory exposure |
| IT governance controls | Operationalize ITGC control areas | Governed financial-system access |
| ITGC audit | Assess access, change, operations, security | Defensible control evidence |
| Financial data integrity | Protect data feeding financial reports | Trustworthy reporting pipeline |

## Reference Materials
- [Sarbanes-Oxley Act of 2002 (SEC)](https://www.sec.gov/about/laws/soa2002.pdf) — U.S. Congress / SEC / PCAOB

## Usage Guidelines
- **Start with scope**: Establish the ICFR boundary before assessing controls.
- **Adapt, don't adopt**: Apply controls proportionate to financial-reporting impact.
- **Document decisions**: Record section mapping and control test results.
- **Review outcomes**: Re-test ITGC on the audit cadence and after material changes.
- **Share learnings**: Feed control findings back into governance improvement.

## Collaboration Protocol
- Apply independently unless a task explicitly requires another skill or framework.
- Use structured handoff format: [Context] -> [Framework Applied] -> [Open Questions] -> [Next Action]
- Auto-loop the security-analyst (CSO) on any financial-systems or ITGC task.

## Ethical Guidelines
- ALWAYS prioritize accurate, honest financial disclosure.
- NEVER weaken or bypass internal controls for convenience.
- ALWAYS preserve records per retention and destruction rules.

## Success Metrics
- **Clarity**: Section and control mapping produces a defensible rationale.
- **Consistency**: Similar systems receive similar control treatment.
- **Stakeholder Alignment**: Framework language improves cross-functional understanding.
- **Outcome Quality**: Decisions show improved control discipline and audit readiness.
- **Learning**: Audits generate reusable controls insight.

## Related Skills
- `compliance` (Maxim compliance skill layer)
- `security` (Security & Threat Intelligence)

## Testing Strategy
- Validate that recommendations clearly map back to SOX sections and ITGC control areas.
- Review one real example and one edge case before adopting the output.
- Confirm stakeholder, ethical, and audit-evidence constraints were considered.
- Document adjustments made when the framework needed adaptation for context.

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
