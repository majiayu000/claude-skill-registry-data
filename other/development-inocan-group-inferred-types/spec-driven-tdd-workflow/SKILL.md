---
name: spec-driven-tdd-workflow
description: A workflow that drives development from requirements refined into observable behaviors (AC/EC) through requirement definition → design → implementation planning → TDD (Red/Green/Refactor) implementation → reporting → commit. Apply to tasks that execute based on `.spec-dock/current/*.md`.
---

# Spec-driven TDD Workflow

- Open `.spec-dock/docs/spec-dock-guide.md` first, and follow it for the rest of the workflow.
- Create/update `.spec-dock/current/requirement.md`, `.spec-dock/current/design.md`, `.spec-dock/current/plan.md`, and `.spec-dock/current/report.md` to maintain traceability from requirements → design → plan → implementation.
- Put investigation/interview materials in `.spec-dock/current/discussions/` (prefer Markdown; embed diagrams with PlantUML; organize freely).
- Keep user interviews/questions short and prioritized. For each question, include answer candidates (options) and your recommended choice based on analysis/simulation to reduce cognitive load.
- Implement each step in `.spec-dock/current/plan.md` as one observable behavior via TDD (Red → Green → Refactor).
- Record commands/results/changes/decisions in `.spec-dock/current/report.md` per session, and `git commit` at the end of the phase.
