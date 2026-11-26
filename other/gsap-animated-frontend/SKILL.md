---
name: gsap-animated-frontend
always: true
description: Persistent, recoverable GSAP workflow for coding agents. Use when the user wants to animate a new page or section, or improve an existing page/component with GSAP. Route new/greenfield work to gsap-new and existing-code improvement work to gsap-refactor. Always use .gsap artifacts as the source of truth so any fresh agent session can resume without chat history.
triggers:
  - gsap animated frontend
  - gsap
  - persistent
  - recoverable

---

# GSAP Animated Frontend

Use this skill as the root router for a model-agnostic GSAP workflow.

## Public Workflow Surface

Expose only two primary workflows:

- `gsap-new`
- `gsap-refactor`

Do not present scan, audit, recipes, doctor, validate, or similar helpers as primary user-facing workflows.

## Source Of Truth

Always read and update these project artifacts first:

- `.gsap/animation-spec.md`
- `.gsap/animation-plan.md`
- `.gsap/audit-report.md`
- `.gsap/pages/*.animation.md`

Never rely on chat history as the workflow memory.

## Workflow Routing

For new pages, new sections, or first-time motion systems:

- read `subskills/gsap-new/SKILL.md`

For existing pages/components that need improvement:

- read `subskills/gsap-refactor/SKILL.md`

## Internal Helpers

Use internal scripts and templates for support work:

- `scripts/gsap_workflow.py`
- `scripts/brand_extractor.py`
- `scripts/structure_search.py`
- `scripts/interview_generator.py`
- `scripts/phase_planner.py`
- `templates/animation-spec.md`
- `templates/animation-plan.md`
- `templates/audit-report.md`
- `templates/animation-tasks.md`
- `templates/page-animation.md`
- `templates/phase.md`

Use references only as needed:

- `references/gsap-core-patterns.md`
- `references/scroll-trigger-patterns.md`
- `references/animation-recipes.md`
- `references/performance-guide.md`

## Non-Negotiables

1. Persist decisions back into `.gsap`.
2. Ask questions only when required by missing artifact data.
3. Read current code before planning refactors.
4. Include reduced-motion and mobile downgrade rules in every plan.
5. Keep helper commands internal; the visible experience stays centered on `gsap-new` and `gsap-refactor`.
6. Let the workflow script inspect framework, packages, page structure, design signals, and existing motion before asking questions.
7. Do not implement an entire page in one pass; generate phased artifacts and execute one major section per phase.
8. Keep `.gsap/tasks/*.md` and `.gsap/phases/**/*.md` current so a fresh agent can resume safely.
