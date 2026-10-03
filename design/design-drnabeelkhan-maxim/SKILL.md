---
skill_id: design
name: Design
description: "UX and interaction design — UI, interface, wireframe, mockup, prototype, user experience, user journey, usability, accessibility audit, onboarding flow. The \"how users think and move through it\" domain."
version: 1.0.0
category: design
office: CPO
lead_agent: product-strategist
triggers:
  - design
  - UI
  - UX
  - interface
  - wireframe
  - mockup
  - prototype
  - user experience
  - user journey
  - usability
  - accessibility
  - onboarding flow
  - visual design
  - information architecture
  - WCAG
collaborates_with:
  - ui-designer
  - ux-researcher
  - behavioral-designer
  - accessibility-auditor
  - design-system
  - ui-styling
  - ui-ux-pro-max
---

# Design -- Domain Dispatcher

> Office: CPO | Lead: product-strategist
> Sub-skills: 5 | Frameworks: Atomic Design, Double Diamond, Nielsen Heuristics, Gestalt Principles

## Purpose

UX design, interaction design, user journeys, accessibility auditing, onboarding flows, and visual design execution. This is the "how users think and flow through an interface" domain -- distinct from design-system (tokens/components) and ui-styling (CSS implementation). Every design output is validated against behavioral science triggers and WCAG 2.1 AA as the minimum accessibility baseline.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| UI design, visual design, component design, visual storytelling | ui-designer | ui-designer/SKILL.md |
| UX research, user journey mapping, usability testing, generative research | ux-researcher | ux-researcher/SKILL.md |
| onboarding flow, first-run experience, activation journey | onboarding-designer | (routed via design domain) |
| WCAG audit, inclusive design, screen reader, assistive technology | accessibility-auditor | (routed via design domain) |
| delight, whimsy, micro-interactions, personality in UI | Whimsy Layer (mode) | whimsy-injector/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-design`
- Task contains keywords: design, UI, UX, interface, wireframe, mockup, prototype, user experience, user journey, usability, accessibility, onboarding flow, visual design, WCAG, information architecture
- Executive router detects design, user experience, or interface signals
- Escalates to `ui-ux-pro-max` skill when task spans multiple design sub-domains simultaneously

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Frameworks: Atomic Design, Double Diamond, Nielsen Heuristics (10 usability heuristics), Gestalt Principles, Fitts's Law, Hick's Law, Jakob's Law
- Auto-loops: behavior-science-persuasion (UX behavioral triggers), design-system (token/component governance), ui-styling (CSS/Tailwind implementation), accessibility-auditor (WCAG compliance on all UI outputs)
- Compliance auto-loop: compliance skill triggered when design decisions involve user data collection

## External Sources

- Primary: community-packs/claude-skills-library/product-team/ (UX research templates, user journey frameworks, accessibility audit patterns)
- Secondary: community-packs/ui-ux-pro-max/.claude/skills/design/ (advanced UI/UX execution patterns, interaction design references)
- VoltAgent: community-packs/voltagent-subagents/ (design specialists)
- Conflict resolution: Maxim ALWAYS WINS

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
