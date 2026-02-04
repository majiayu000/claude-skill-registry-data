---
name: skill-authoring
description: Create or update project-specific skills in this repo. Use when asked to make new skills, modularize workflows, or build skill packs for this codebase.
---

# Skill Authoring

## Overview
Create concise, modular skills stored under `skills/` in this repo.

## Workflow
1. Define triggers and scope with concrete user examples.
2. Choose a short skill name (lowercase, hyphen).
3. Initialize with `init_skill.py` from the system skill-creator.
4. Write SKILL.md in imperative form and keep it lean.
5. Add scripts or references only when they save repeated work.
6. Package with `package_skill.py` only when requested.
7. Run the QA harness to generate matrices and results templates.

## References
- Skill template: `references/skill_template.md`
- QA checklist: `references/qa_checklist.md`
- QA matrix template: `references/qa_matrix_template.md`

## QA Harness
- Generate QA artifacts: `python3 scripts/skill_qa_harness.py`
- Overwrite existing outputs: `python3 scripts/skill_qa_harness.py --force`

## Local Conventions
- Prefer small, single-purpose skills plus an orchestrator.
- Put reusable commands in scripts; keep references one hop from SKILL.md.
- Avoid extra docs (README, changelog, etc.).
- Add honesty guardrails when a skill can produce overconfident outputs.
- Add acceptance criteria sections so QA can be objective.
- Use repo-relative paths in skill lists (AGENTS.md) for portability.
