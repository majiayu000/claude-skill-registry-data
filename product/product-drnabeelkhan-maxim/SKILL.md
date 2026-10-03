---
skill_id: product
name: Product Strategy
description: "Decide what to build — product strategy, roadmap, feature prioritization, product-market fit, pricing model, backlog, sprint planning, product vision, RICE, JTBD, OKRs. Distinct from designing or building it."
version: 1.0.0
category: product
office: CPO
lead_agent: product-strategist
triggers:
  - product strategy
  - roadmap
  - feature prioritization
  - product-market fit
  - pricing model
  - backlog prioritization
  - sprint planning
  - product vision
  - go-to-market
  - RICE
  - WSJF
  - north star metric
collaborates_with:
  - feedback-synthesizer
  - trend-researcher
  - pricing-strategist
  - sprint-prioritizer
  - product-manager
  - product-development-research
  - security-analyst
---

# Product Strategy -- Domain Dispatcher

> Office: CPO | Lead: product-strategist
> Sub-skills: 2 | Frameworks: Kano Model, Jobs-to-be-Done, Product-Market Fit Canvas

## Purpose

Strategic product decisions, pricing strategy, backlog prioritisation, and trend intelligence. The "deciding what to build" domain -- distinct from product-development-research (which handles discovering and validating what to build). When product decisions involve user behavioral data or PII, the compliance skill is auto-looped via the CSO auto-loop rule.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| User feedback synthesis, NPS data, product signals | feedback-synthesizer | product/feedback-synthesizer/SKILL.md |
| Market trend intelligence, emerging signal detection | trend-researcher | product/trend-researcher/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-cpo`
- Task contains keywords: product strategy, roadmap, feature prioritization, product-market fit, pricing model, backlog prioritization, sprint planning, product vision, go-to-market, RICE, WSJF, ICE scoring, OKRs, north star metric, product KPIs, user feedback, NPS

## Behavioral Layer

- Confidence: 🟢 HIGH
- Compliance: reads project-manifest.json
- Handoff: writes .mxm-skills/agents-handoff.md
- Frameworks: Kano Model, Jobs-to-be-Done, Product-Market Fit Canvas, RICE, WSJF, ICE

## External Sources

- Primary: community-packs/claude-skills-library/product-team/
- Merge rule: Maxim ALWAYS WINS -- behavioral science + proactive triggers + confidence tagging non-negotiable

---
*Maxim Product Strategy Skill -- Version 1.0.0*
*Maxim behavioral layer: ACTIVE | External merge: product-team ABSORBED | Confidence: 🟢 HIGH*

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
