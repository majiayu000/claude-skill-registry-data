---
name: saas-team-growth
description: "Orchestrate the growth & acquisition team — growth-engineer, seo-strategist, copywriter, frontend-engineer, analytics-engineer — landing page, SEO, tracking, and viral loops."
argument-hint: "[growth initiative description] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/saas-team-growth/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation`

Resolved above — use as-is; `--review` overrides `review_mode` for this run.

# Team Growth & Acquisition

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Orchestrate the growth engineering team to build high-converting landing pages, programmatic SEO,
analytics instrumentation, lead capture, and referral loops.

**Argument check:** If no growth initiative description is provided, output:
> "Usage: `/saas-team-growth [initiative description] [--review full|lean|solo]` — Describe the acquisition or conversion feature you want to build (e.g. Landing Page redesign, Onboarding funnel optimization, Referral invite loop, Programmatic SEO directory)."

When this skill is invoked with a valid argument, orchestrate the team:

1. **Strategy & Copy Phase**:
   - `growth-engineer`: Map conversion funnel (Visitor → Lead → Signup → Activated User)
   - `copywriter`: High-converting headlines, value proposition hooks, social proof, and primary CTAs
   - `seo-strategist`: Keyword architecture, metadata, OpenGraph tags, JSON-LD schema, and sitemap plan

2. **Frontend & Interactive Experience**:
   - `frontend-engineer`: Implement responsive landing page, interactive product demo, newsletter/signup form
   - Optimize Core Web Vitals (LCP < 2.5s, CLS = 0, FID/INP < 100ms)

3. **Analytics & Instrumentation**:
   - `analytics-engineer`: Instrument tracking events (PostHog, Segment, Mixpanel, GA4)
   - Track key conversion milestones: page view, CTA click, signup started, signup completed

4. **Review & Validation**:
   - Verify lighthouse performance score (>90), mobile responsiveness, and form submission reliability.

5. **Verdict**:
   - Output: **COMPLETE** — growth initiative designed, implemented, and tracked.
