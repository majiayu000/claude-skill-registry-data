---
skill_id: ceo-automation
name: CEO Automation
description: "Founder and CEO automation — morning standup, overnight cycle, burn rate, runway, pipeline review, investor and fundraising prep, executive summary, daily digest. Operates on the .mxm-executive-summary context."
version: 1.0.0
category: ceo-automation
office: CEO
lead_agent: enterprise-architect
triggers:
  - CEO
  - startup
  - investor
  - fundraising
  - morning standup
  - overnight
  - burn rate
  - pipeline
  - executive summary
  - daily digest
  - metrics review
  - OKR review
  - board prep
  - cap table
  - content calendar
collaborates_with:
  - financial-modeler
  - investor-pitch-writer
  - business-architect
  - content-strategist
  - seo-specialist
  - product-strategist
  - security-analyst
---

# CEO Automation -- Domain Dispatcher

> Office: CEO | Lead: enterprise-architect
> Sub-skills: 5 | Frameworks: OKR, RICE, Lean Startup, Business Model Canvas

## Purpose

Cross-functional startup automation spanning strategy, metrics, pipeline, marketing, sales, launch, and social media. Operates on the `.mxm-executive-summary/` knowledge base per project, providing 160+ prompts across CEO tasks, marketing automation, sales automation, product launch readiness, and social media management. When `.mxm-executive-summary/` exists in a project root, this skill auto-activates alongside enterprise-architecture.

## Sub-Skill Routing

| Task Signal | Routes To | SKILL.md Path |
|---|---|---|
| strategy, metrics, team, investors, decisions, comms | CEO Tasks | ceo-tasks/SKILL.md |
| content, email, SEO, growth, brand, analytics | Marketing | marketing/SKILL.md |
| pipeline, prospecting, closing, proposals, retention | Sales | sales/SKILL.md |
| launch readiness, roadmap, code quality, docs, feedback | Launch/Product | launch-product/SKILL.md |
| Facebook, X/Twitter, LinkedIn, cross-platform social | Social Media | social-media/SKILL.md |

## Activation

This domain activates when:
- User invokes `/mxm-ceo`, `/mxm-ceo-morning`, `/mxm-ceo-overnight`, `/mxm-ceo-setup`
- Task contains keywords: CEO, startup, investor, fundraising, burn rate, pipeline, daily digest, metrics review, OKR, board prep, content calendar, sales automation
- Executive router detects strategy, executive, or startup operations signals
- `.mxm-executive-summary/` directory exists in project root (auto-activation)

## Behavioral Layer

- Confidence: 🟢 HIGH (Maxim skill + external knowledge merged)
- Compliance: reads project-manifest.json before decisions
- Handoff: writes .mxm-skills/agents-handoff.md on completion
- Session continuity: writes to .mxm-executive-summary/sessions/
- Frameworks: OKR, RICE, Lean Startup, Business Model Canvas, Porter's Five Forces, Blue Ocean, Jobs-to-be-Done, SPIN Selling, Challenger Sale, MEDDIC, AIDA, PAS, StoryBrand, SaaS Unit Economics
- Mandatory behavioral science: Fogg Behavior Model, COM-B, EAST Framework, Hook Model, Loss Aversion (Kahneman)

## External Sources

- Primary: community-packs/claude-skills-library/c-level-advisor/ (executive strategy, C-suite advisory patterns)
- Reference library: ceo-automation-prompts.md (2,441 lines, 160+ prompts)
- VoltAgent: community-packs/voltagent-subagents/ (cross-category specialists)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
