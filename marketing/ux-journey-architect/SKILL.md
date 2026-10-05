---
name: ux-journey-architect
description: Map user journeys, onboarding paths, entry points, first actions, trust points, accessibility risks, and SEO/LLM handoffs for public websites without redesigning the visual system. Use this skill when the user asks how new readers, returning users, project reviewers, community members, buyers, or AI agents should move through a site and what each page must make clear before layout implementation.
---

# UX Journey Architect

Use this skill after the site goal, primary audience, and rough URL structure are known.

Read [references/journey-workflow.md](references/journey-workflow.md) before producing a full journey map.

## Owns

- user journey maps;
- onboarding paths;
- entry point and first-action design;
- CTA hierarchy by intent;
- trust points and credibility signals;
- accessibility and mobile journey risks;
- UX handoff requirements for SEO/LLM page roles.

## Does Not Own

- final visual design;
- component implementation;
- browser rendering tests;
- SEO schema or canonical decisions;
- live site code changes;
- conversion instrumentation implementation.

## Workflow

1. Identify audience segments and entry sources.
2. Map what each segment needs to understand in the first viewport and first scroll.
3. Define the primary action, secondary actions, and proof needed for trust.
4. Map the path from entry page to next useful page.
5. Check that the journey does not hide SEO/LLM-critical content or break the content model.
6. Identify mobile, accessibility, and cognitive-load risks.
7. Produce a journey map using [assets/journey-map.template.md](assets/journey-map.template.md).
8. Defer visual layout validation, retention systems, and onboarding implementation to the backlog when needed.

## Non-Negotiables

- Do not propose generic landing-page filler.
- Do not hide actual content behind oversized decoration.
- Do not add CTAs that have no user intent.
- Do not weaken the declared SEO/LLM content model.
- Do not replace short news and longform pages with a marketing funnel unless the site goal changed.
- Do not claim conversion uplift without measurement.

## Safety And Privacy Boundaries

- Do not include private analytics rows, raw IP logs, account identifiers, session recordings, or private user data in public journey artifacts.
- Do not recommend dark patterns, forced subscriptions, misleading urgency, fake social proof, or inaccessible interactions.
- Do not request credentials unless the user explicitly asks for a credentialed analytics task and a privacy policy exists.

## Journey Types

### New Reader

Needs fast positioning, why this source is different, where to start, and how to follow updates.

### Returning Reader

Needs freshness signals, clear latest content, saved mental model, and quick route to news or explainers.

### Project Reviewer

Needs proof of work, repository or artifact links, project status, and relation to site expertise.

### Community Member

Needs public social links, Telegram/community routes, and expectation-setting about what happens there.

### AI Agent Or Researcher

Needs crawlable static content, clear page roles, source trails, entity pages, and low ambiguity.

## Output Shape

Return:

1. Audience segments and entry sources.
2. Journey map table.
3. First viewport requirements.
4. CTA hierarchy and labels.
5. Trust and proof points.
6. Accessibility/mobile risks.
7. SEO/LLM handoff notes.
8. Backlog items for layout validation, retention, conversion, and onboarding.

## Validation

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/ux-journey-architect
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).
