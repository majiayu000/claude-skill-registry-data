---
name: nist-ai-rmf
description: "Knowledge base from NIST AI Risk Management Framework 1.0 (NIST AI 100-1). Use for AI risk management, trustworthiness characteristics, GOVERN/MAP/MEASURE/MANAGE functions, bias management, AI actor roles, TEVV, AI RMF profiles, and socio-technical risk framing. Does not cover sector-specific regulations, EU AI Act, ISO 42001 in depth, or the AI RMF Playbook tactical detail."
---

<!-- argument-hint: [topic, function, or chapter number] -->

# NIST AI Risk Management Framework 1.0 (NIST AI 100-1)
**Source**: NIST (US Government work, public domain) | **Chapters**: 8

## When to use
Reach for this pack when designing, evaluating, or governing an AI system and needing a structured, standards-grounded approach to risk. Use it to select the right GOVERN/MAP/MEASURE/MANAGE activities for a given lifecycle stage, to understand trustworthiness tradeoffs, or to frame a conversation with leadership about AI risk posture. It is also useful when mapping organisational roles and responsibilities across an AI programme or when setting up a risk profiling exercise.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below.
- **With a topic** — ask about trustworthiness characteristics, bias categories, TEVV, third-party risk, AI actor roles, or risk profiles; I read the relevant chapter.
- **With a chapter** — ask for `ch04` (GOVERN), `ch05` (MAP), `ch06` (MEASURE), `ch07` (MANAGE), etc.

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

## Core Frameworks & Mental Models

### The Four Functions (AI RMF Core)

The AI RMF Core organises AI risk management into four functions. GOVERN is the cross-cutting foundation; MAP, MEASURE, and MANAGE operate on specific systems in sequence and iteratively.

```
GOVERN (cross-cutting, always on)
  └── MAP (context & risk identification)
        └── MEASURE (quantify & evaluate)
              └── MANAGE (respond, monitor, improve)
```

**GOVERN** establishes organisational culture, policies, accountability structures, workforce requirements, and third-party governance. Its six categories cover: (1) policies and legal/regulatory compliance, (2) accountability and training, (3) team diversity and human-AI configuration, (4) safety-first risk culture, (5) external stakeholder feedback, (6) third-party and supply chain risk. GOVERN must be in place before MAP activities are meaningful.

**MAP** establishes the contextual knowledge needed to frame risks: intended purposes, deployment setting, legal norms, stakeholder population, system capabilities, cost-benefit analysis, third-party components, and societal impacts. MAP 1–5 categories build from context (MAP 1) through impact characterisation (MAP 5). MAP outputs enable the go/no-go decision and are direct inputs to MEASURE.

**MEASURE** applies quantitative, qualitative, or mixed-method tools to evaluate trustworthiness characteristics. Its thirteen MEASURE 2.x subcategories map one-to-one to the trustworthiness characteristics plus environmental impact and TEVV effectiveness. Key structural requirement: assessors must be independent from builders (MEASURE 1.3). All measurement must be documented, including risks that cannot currently be measured.

**MANAGE** allocates resources to prioritised risks, executes risk treatment plans (mitigate / transfer / avoid / accept — MANAGE 1.3), documents residual risks for downstream parties (MANAGE 1.4), monitors deployed systems (MANAGE 4.1), and communicates incidents to affected communities (MANAGE 4.3). A deactivation mechanism (MANAGE 2.4) must be in place before deployment.

### Seven Trustworthiness Characteristics

Valid and Reliable is the necessary base; without it, no other characteristic can be meaningfully claimed. Accountable and Transparent is cross-cutting and applies to all others.

1. **Valid & Reliable** — system performs as required, confirmed by objective evidence, across its intended lifecycle.
2. **Safe** — no conditions under which life, health, property, or environment is endangered.
3. **Secure & Resilient** — withstands attacks and adverse events; degrades gracefully.
4. **Accountable & Transparent** — information available to those interacting with the system; enables redress.
5. **Explainable & Interpretable** — mechanisms of operation described ("how"); output meaning communicated ("why").
6. **Privacy-Enhanced** — autonomy, identity, and dignity protected through design choices.
7. **Fair / Bias Managed** — equality and equity addressed; three bias categories managed (systemic, computational/statistical, human-cognitive).

Tradeoffs among characteristics are normal and require documented, contextual human judgement — the framework does not resolve them algorithmically.

### Risk Framing
- **Risk = probability × magnitude of harm** (ISO 31000:2018 / OMB A-130:2016)
- Risk tolerance is contextual and organisation-specific; the AI RMF does not prescribe it.
- Residual risk must be documented and disclosed to downstream acquirers and end users.
- When risk is unacceptable (severe harm imminent), halt development or deployment until it can be managed.

### AI RMF Profiles
Current Profile (existing state) → Gap Analysis → Target Profile (desired state) → Action Plan. This is the mechanism for turning the generic framework into organisation-specific improvement programmes. Cross-sectoral profiles address capabilities (e.g., LLMs) used across multiple sectors.

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-framing-ai-risk.md) | Framing AI Risk | Risk definition, risk tolerance, risk prioritisation, socio-technical risk, measurement challenges |
| [ch02](chapters/ch02-audience-and-ai-actors.md) | Audience and AI Actors | AI actors, OECD lifecycle dimensions, TEVV, diverse teams, affected communities |
| [ch03](chapters/ch03-trustworthiness-characteristics.md) | Trustworthiness Characteristics | All seven characteristics, three bias categories, tradeoff analysis, measurement obligations |
| [ch04](chapters/ch04-govern-function.md) | GOVERN Function | GOVERN 1–6, risk culture, accountability, diversity, third-party governance, decommissioning |
| [ch05](chapters/ch05-map-function.md) | MAP Function | MAP 1–5, context establishment, system categorisation, impact characterisation, go/no-go |
| [ch06](chapters/ch06-measure-function.md) | MEASURE Function | MEASURE 1–4, TEVV, independent assessment, MEASURE 2.1–2.13 subcategory details |
| [ch07](chapters/ch07-manage-function.md) | MANAGE Function | MANAGE 1–4, risk response options, residual risk, deactivation, incident communication |
| [ch08](chapters/ch08-profiles-and-use.md) | Profiles and Use | Current/Target profiles, gap analysis, cross-sectoral profiles, AI RMF Playbook, living document |

## Topic Index

- **Accountability** → ch03, ch04 (GOVERN 2)
- **Bias (three categories)** → ch03, ch06 (MEASURE 2.11)
- **Decommissioning** → ch04 (GOVERN 1.7), ch07 (MANAGE 4.1)
- **Deactivation mechanism** → ch07 (MANAGE 2.4)
- **Diverse teams** → ch02, ch04 (GOVERN 3), ch05 (MAP 1.2)
- **Environmental impact** → ch06 (MEASURE 2.12)
- **Explainability / Interpretability** → ch03, ch06 (MEASURE 2.9)
- **Fairness** → ch03, ch06 (MEASURE 2.11)
- **Go/no-go decision** → ch05 (MAP), ch07 (MANAGE 1.1)
- **GOVERN categories** → ch04
- **Human-AI interaction** → ch02, ch04 (GOVERN 3.2), ch05 (MAP 3.5)
- **Incident response** → ch07 (MANAGE 4.3)
- **MAP categories** → ch05
- **MANAGE categories** → ch07
- **MEASURE subcategories** → ch06
- **Privacy** → ch03, ch06 (MEASURE 2.10)
- **Profiles (Current/Target)** → ch08
- **Residual risk** → ch01, ch07 (MANAGE 1.4)
- **Risk measurement challenges** → ch01
- **Risk tolerance** → ch01, ch04 (GOVERN 1.3), ch05 (MAP 1.5)
- **Robustness / generalizability** → ch03
- **Safety** → ch03, ch06 (MEASURE 2.6)
- **Security and resilience** → ch03, ch06 (MEASURE 2.7)
- **Socio-technical risk** → ch01, ch02
- **TEVV** → ch02, ch06 (MEASURE 1.3, MEASURE 2.1–2.2)
- **Third-party risk** → ch01, ch04 (GOVERN 6), ch05 (MAP 4), ch07 (MANAGE 3)
- **Transparency** → ch03, ch06 (MEASURE 2.8)
- **Trustworthiness characteristics** → ch03
- **Valid and Reliable** → ch03, ch06 (MEASURE 2.5)

## Supporting Files
- [glossary.md](glossary.md) — ~45 terms with chapter references, alphabetical.
- [patterns.md](patterns.md) — 13 actionable patterns with when-to-use and trade-offs.
- [cheatsheet.md](cheatsheet.md) — decision rules, function quick-reference table, trustworthiness characteristic table, tells and smells.

---

## Scope & Limits

This pack covers the NIST AI RMF 1.0 (NIST AI 100-1, January 2023) in full: foundational framing, audience, trustworthiness characteristics, all four Core functions and their categories/subcategories, and profiles. It is a US Government publication and is public domain. This pack does not cover: the AI RMF Playbook's tactical subcategory suggestions (separate online resource), the EU AI Act, ISO/IEC 42001 in depth, sector-specific regulations, or post-1.0 NIST AI RMF updates. For security and privacy implementation detail, consult the NIST Cybersecurity Framework and NIST Privacy Framework packs directly.
