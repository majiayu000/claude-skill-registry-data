---
skill_id: enterprise-architecture
name: Enterprise Architecture
description: "Enterprise and solution architecture — system design, scalability, cloud strategy, digital transformation, data architecture, governance, technology strategy. Practitioner-level TOGAF, C4, ArchiMate, Zachman, Wardley mapping and ADR authoring."
version: 1.0.0
category: enterprise-architecture
office: CEO
lead_agent: enterprise-architect
triggers:
  - architecture
  - system design
  - enterprise
  - scalability
  - cloud
  - infrastructure strategy
  - digital transformation
  - TOGAF
  - Zachman
  - solution design
  - data platform
  - technology strategy
  - governance framework
collaborates_with:
  - business-architect
  - data-architect
  - solution-architect
  - technology-architect
  - governance-specialist
  - implementer
  - security-analyst
---

# Enterprise Architecture -- Domain Dispatcher

> Office: CEO | Lead: enterprise-architect
> Sub-skills: 6 | Frameworks: TOGAF, Zachman, C4 Model, Well-Architected Framework

## Purpose

Enterprise systems design, business architecture, solution architecture, data architecture, governance, and technology strategy. The CEO office's primary technical domain -- resolves strategic conflicts between all other offices. When architecture decisions involve PII data flows or regulated industries, the compliance skill is auto-looped via the CSO auto-loop rule.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| Enterprise architecture strategy, digital transformation, IT roadmap | enterprise-architect | enterprise-architecture/enterprise-architect/SKILL.md |
| Business capability modeling, value chain, operating model | business-architect | enterprise-architecture/business-architect/SKILL.md |
| Data platform design, data governance, data modeling, DMBOK | data-architect | enterprise-architecture/data-architect/SKILL.md |
| IT governance, COBIT, RoPA maintenance, audit trail management | governance-specialist | enterprise-architecture/governance-specialist/SKILL.md |
| End-to-end solution design, cloud architecture, system integration | solution-architect | enterprise-architecture/solution-architect/SKILL.md |
| Technology strategy, tech stack evaluation, platform decisions | technology-architect | enterprise-architecture/technology-architect/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-ceo`
- Task contains keywords: architecture, system design, enterprise, scalability, cloud, infrastructure strategy, digital transformation, TOGAF, Zachman, solution design, data platform, technology strategy, governance framework, microservices, API gateway, COBIT, ITIL

## Behavioral Layer

- Confidence: 🟢 HIGH
- Compliance: reads project-manifest.json
- Handoff: writes .mxm-skills/agents-handoff.md
- Frameworks: TOGAF, Zachman, C4 Model, AWS Well-Architected Framework, COBIT, ITIL

## External Sources

- Primary: community-packs/claude-skills-library/c-level-advisor/
- Secondary: community-packs/claude-skills-library/engineering-team/senior-architect
- Secondary: community-packs/claude-skills-library/engineering-team/aws-solution-architect
- Secondary: community-packs/claude-skills-library/orchestration/
- Merge rule: Maxim ALWAYS WINS -- behavioral science + proactive triggers + confidence tagging non-negotiable

---
*Maxim Enterprise Architecture Skill -- Version 1.0.0*
*Maxim behavioral layer: ACTIVE | External merge: c-level-advisor + engineering-team ABSORBED | Confidence: 🟢 HIGH*

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
