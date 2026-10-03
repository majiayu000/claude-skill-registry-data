---
skill_id: eu-ai-act
name: EU AI Act
version: 1.0.0
category: security-compliance
type: framework
frameworks: []
triggers:
  - apply eu ai act
  - use eu-ai-act framework
  - eu ai act risk classification
  - ai act compliance analysis
collaborates_with:
  - security-analyst
  - compliance-orchestrator
  - enterprise-architect
  - data-architect
  - product-strategist
ethics_required: true
priority: high
tags: [security-compliance, framework]
created: 2026-07-08
updated: 2026-07-08
---

# EU AI Act

## Purpose
Apply the EU AI Act to classify, govern, and document AI systems under the European Union's risk-based regulatory regime — ensuring products meet conformity, transparency, and human-oversight obligations before and after market entry.

## Frameworks & Standards
| Item | Value |
|------|-------|
| Framework ID | `eu-ai-act` |
| Category | Security & Compliance |
| Version | 1.0.0 |
| Owner | European Union |
| Maturity | Active (2024, enforcement phased through 2026–2027) |
| Primary References | Risk-based regulation of artificial intelligence systems |

## Risk Classification
| Risk Level | Description | Examples |
|------------|-------------|----------|
| Unacceptable | Prohibited AI practices | Social scoring, real-time biometric mass surveillance |
| High Risk | Significant conformity requirements | Medical devices, recruitment AI, credit scoring |
| Limited Risk | Transparency obligations | Chatbots, deepfakes |
| Minimal Risk | No mandatory requirements | Spam filters, AI in games |
| GPAI Models | General-purpose AI model requirements | Foundation models (GPT, Claude, etc.) |

## Compliance Requirements
| Requirement | Description |
|-------------|-------------|
| Risk Management System | Identify, analyze, and mitigate risks |
| Data Governance | Training data quality and relevance |
| Technical Documentation | Pre-market and ongoing documentation |
| Human Oversight | Ensure meaningful human control |
| Transparency | Clear disclosure when interacting with AI |
| Accuracy & Robustness | Performance metrics and cybersecurity |

## Prompt Template
```
You are applying the EU AI Act framework.

CONTEXT:
- Current task: [[task_description]]
- Domain: security & compliance
- Stakeholders: [[stakeholder_roles]]

FRAMEWORK APPLICATION:
1. **Classify**: Which EU AI Act risk level applies (Unacceptable / High / Limited / Minimal / GPAI)?
2. **Analyze**: Map the system against the compliance requirements for that risk tier:
   - Risk management, data governance, technical documentation, human oversight, transparency, accuracy & robustness
3. **Synthesize**: Combine findings into a conformity path and disclosure obligations
4. **Validate**: Check against EU AI Act enforcement timelines and prohibited-practice list

OUTPUT STRUCTURE:
- Framework Application: Risk classification and why
- Analysis: Requirement-by-requirement gap assessment
- Recommendations: Prioritized conformity actions
- Limitations: Assumptions, jurisdictional scope, phased-enforcement caveats

QUALITY CHECKS:
□ Risk classification is defensible and documented
□ Human-oversight and transparency obligations addressed
□ Ethical considerations have been evaluated
□ Next steps map to enforcement timelines
```

## Core Principles
- **Foundation**: The EU AI Act provides a risk-based structure for governing AI systems in the EU market.
- **Application**: Use when scoping, building, or auditing AI products that reach EU users or high-risk domains.
- **Adaptation**: Match obligations to the specific risk tier; do not over- or under-apply controls.
- **Documentation**: Maintain technical documentation and audit trail as first-class conformity evidence.

## Applications & Use Cases
| Use Case | Application | Expected Outcome |
|----------|-------------|------------------|
| AI product compliance | Classify system and map obligations | Clear conformity path per risk tier |
| Regulatory alignment | Cross-check against prohibited practices | Reduced enforcement exposure |
| AI risk architecture | Bake oversight + robustness into design | Governed-by-design AI system |
| Training data governance | Assess data quality and relevance | Defensible data-governance posture |
| Responsible AI product strategy | Align roadmap to transparency duties | Trust-forward product positioning |

## Reference Materials
- [EU AI Act — official portal](https://artificialintelligenceact.eu/) — European Union

## Usage Guidelines
- **Start with classification**: Determine the risk tier before assessing controls.
- **Adapt, don't adopt**: Apply only the obligations the tier actually triggers.
- **Document decisions**: Record classification rationale and requirement mapping.
- **Review outcomes**: Re-assess as enforcement phases in through 2026–2027.
- **Share learnings**: Contribute classification patterns back to team knowledge base.

## Collaboration Protocol
- Apply independently unless a task explicitly requires another skill or framework.
- Use structured handoff format: [Context] -> [Framework Applied] -> [Open Questions] -> [Next Action]
- Auto-loop the security-analyst (CSO) on any regulated-AI or PII-adjacent task.

## Ethical Guidelines
- ALWAYS prioritize meaningful human oversight and user autonomy.
- NEVER use for prohibited practices (social scoring, mass biometric surveillance).
- ALWAYS disclose clearly when a user is interacting with an AI system.

## Success Metrics
- **Clarity**: Risk classification produces a defensible conformity rationale.
- **Consistency**: Similar systems receive similar tier-based obligations.
- **Stakeholder Alignment**: Framework language improves cross-functional understanding.
- **Outcome Quality**: Decisions show improved consideration of risk, oversight, and transparency.
- **Learning**: Application generates reusable classification insight.

## Related Skills
- `compliance` (Maxim compliance skill layer)
- `security` (Security & Threat Intelligence)

## Testing Strategy
- Validate that recommendations clearly map back to the EU AI Act risk tiers.
- Review one real example and one edge case before adopting the output.
- Confirm stakeholder, ethical, and enforcement-timeline constraints were considered.
- Document adjustments made when the framework needed adaptation for context.

---
<sub>Copyright (c) 2026 iSystematic Inc. Maxim is a product of iSystematic Inc.  
SPDX-License-Identifier: BSL-1.1 (Apache-2.0 after 4 years)  
See LICENSE at repo root. Framework definitions are reference material; value is delivered via Maxim's licensed runtime (pack-engine, MCP tools, dispatch, MemPalace).</sub>
