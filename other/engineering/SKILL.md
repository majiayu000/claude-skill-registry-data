---
skill_id: engineering
name: Engineering
description: "Build and ship software — code, implement, develop, API, backend, frontend, deploy, infrastructure, CI/CD, databases, cloud, mobile, AI/ML. The CTO office's broadest execution domain, applied with TDD discipline."
version: 1.0.0
category: engineering
office: CTO
lead_agent: implementer
triggers:
  - build
  - code
  - implement
  - develop
  - API
  - backend
  - frontend
  - deploy
  - infrastructure
  - CI/CD
  - database
  - refactor
  - debug
  - optimize
  - machine learning
  - LLM
  - performance
  - load test
collaborates_with:
  - reviewer
  - security-analyst
  - tester
  - performance-engineer
  - compliance
  - release-manager
---

# Engineering -- Domain Dispatcher

> Office: CTO | Lead: implementer
> Sub-skills: 6 (19 active agents) | Frameworks: SOLID, Clean Code, 12-Factor App, TDD, DDD

## Purpose

Software engineering across backend, frontend, AI/ML, mobile, DevOps, infrastructure, databases, APIs, and cloud. The broadest Maxim skill domain with 19 active agents spanning the full software delivery lifecycle. Every code output is reviewed against OWASP Top 10 as the minimum security baseline, with ethics gates on security-architect (auth/payment/PII paths) and ai-engineer (AI ethics compliance).

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| ML models, LLM integration, embeddings, AI features, RAG | ai-engineer | ai-engineer/SKILL.md |
| API design, database design, system scalability, microservices | backend-architect | backend-architect/SKILL.md |
| CI/CD pipelines, infrastructure automation, deployment, monitoring | devops-automator | devops-automator/SKILL.md |
| UI implementation, component development, responsive design, PWA | frontend-developer | frontend-developer/SKILL.md |
| cross-platform mobile, React Native | mobile-app-builder | mobile-app-builder/SKILL.md |
| fast iteration, MVP scaffolding, prototype builds | rapid-prototyper | rapid-prototyper/SKILL.md |
| third-party API integration, orchestration | api-integrator | (routed via engineering domain) |
| retrieval-augmented generation systems | rag-specialist | (routed via engineering domain) |
| LLM prompt design, optimization | prompt-engineer | (routed via engineering domain) |
| query optimization, schema design, indexing | database-optimizer | (routed via engineering domain) |
| package security, version management, supply chain | dependency-auditor | (routed via engineering domain) |
| ML dataset preparation, governance | training-data-curator | (routed via engineering domain) |
| automated support, chatbot systems | support-agent-builder | (routed via engineering domain) |
| benchmarking, load testing, latency optimization | performance-engineer | (routed via engineering domain) |
| cloud spend analysis, right-sizing | cloud-cost-optimizer | (routed via engineering domain) |
| auth, payment, PII code path security | security-architect | (routed via engineering domain) |
| end-to-end system integration | solution-architect | (routed via engineering domain) |
| API validation, contract testing | api-tester | (routed via engineering domain) |
| performance and stress testing | load-tester | (routed via engineering domain) |

## Activation

This domain activates when:
- User invokes `/mxm-cto`
- Task contains keywords: build, code, implement, develop, API, backend, frontend, deploy, infrastructure, CI/CD, database, refactor, debug, optimize, machine learning, LLM, performance, load test
- Executive router detects engineering, development, or infrastructure signals
- Any code generation, review, or deployment task

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Frameworks: SOLID, Clean Code, 12-Factor App, TDD, DDD, OWASP Top 10 (security baseline), REST/GraphQL conventions
- Ethics gates: security-architect (auth/payment/PII paths), ai-engineer (AI ethics compliance)
- Auto-loops: reviewer (code review on all generated code), security-analyst (CSO auto-loop on auth/payment/PII), tester (pre-deployment testing), performance-engineer (scalability signals), compliance skill (regulated industry/PII)

## External Sources

- Primary: community-packs/claude-skills-library/engineering-team/ (backend, frontend, fullstack, senior architects)
- Architects: community-packs/claude-skills-library/engineering-team/senior-architect (consumed by enterprise-architect, solution-architect, backend-architect)
- AI/ML: community-packs/claude-skills-library/engineering-team/senior-ml-engineer, senior-prompt-engineer, senior-computer-vision (consumed by ai-engineer, rag-specialist, prompt-engineer)
- Power patterns: community-packs/claude-skills-library/POWERFUL/ (power-user engineering patterns)
- VoltAgent: community-packs/voltagent-subagents/ (engineering specialists)
- Conflict resolution: Maxim ALWAYS WINS

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
