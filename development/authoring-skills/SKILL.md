---
name: authoring-skills
description: MUST BE USED when creating, improving, or reviewing Skills. Use PROACTIVELY when user mentions "create a skill", "new skill", "write a skill", "improve skill", "skill description", or "progressive disclosure". Guides through specification-compliant skill design with three-level progressive disclosure.
metadata:
  category: meta
  keywords: skill, create, authoring, develop, progressive-disclosure, compliance
---

# Skill Development

Guides effective Skill creation following the Universal Skills Specification.

## Overview

Skills enable agents to work autonomously without human intervention. This skill provides the methodology for creating specification-compliant skills using progressive disclosure, robust scripting, and agentic patterns.

## When to Use

- User mentions "create a skill", "new skill", "write a skill", "improve skill"
- Reviewing or auditing existing skills for compliance
- Designing skill architecture with proper agentic patterns

## Workflow

<workflow>
1. **Analyze & Plan**:
   - Determine Degrees of Freedom (Fragile vs Creative) using `references/agentic-patterns.md`.
   - Define Security Scope using `references/security-best-practices.md`.
   - Create `evaluation_plan.md` from `assets/templates/evaluation_plan.md`.

2. **Draft Content**:
   - Use `assets/templates/skill_structure.md` for `SKILL.md`.
   - Use `assets/templates/robust_script.py` for any Python scripts.
   - Write frontmatter using `references/description-templates.md` (CRITICAL).

3. **Verify & Refine**:
   - Validate against `references/compliance-checklist.md`.
   - Ensure all paths are relative to project root.
   - Verify that instructions use imperative, third-person language (no "you").
</workflow>

## Critical Rules

<rules>
- **Frontmatter**: MUST use directive language (MUST BE USED, Use PROACTIVELY) in `description`.
- **Language**: NEVER use second person ("You should"). Use imperative ("Do X").
- **Structure**: Keep `SKILL.md` body under 500 lines. Move details to `references/`.
- **Pathing**: ALWAYS use project-root relative paths.
- **Verification**: workflows MUST include self-correction loops.
</rules>

## Resources

- **Core Principles**: `references/core-principles.md` (Philosophy, Directory Structure, Detailed Workflow)
- **Templates**:
  - Description: `references/description-templates.md`
  - Structure: `assets/templates/skill_structure.md`
  - Script: `assets/templates/robust_script.py`
  - Evaluation: `assets/templates/evaluation_plan.md`
- **Guides**:
  - `references/compliance-checklist.md`
  - `references/agentic-patterns.md`
  - `references/security-best-practices.md`
  - `references/progressive-disclosure.md`
