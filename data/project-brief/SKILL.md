---
name: project-brief
description: Turn ideas/brain dumps into a structured project brief (problem, goals, scope, milestones, success criteria). Use when starting a project.
triggers:
  - create brief
  - new project
  - define project
  - יש לי רעיון לפרויקט
  - project idea
---

# Project Brief Skill

Transform project ideas and brain dumps into structured project definitions with clear scope, goals, and success criteria.

## Purpose

This skill helps transform raw ideas, brain dumps, and unstructured thoughts into well-organized project briefs. It extracts key elements, structures them into a standard template, and iterates with the user until the brief is complete.

## Inputs

**Required:**
- `project_idea`: Raw description or brain dump of the project concept

**Optional:**
- `constraints`: Time, budget, or resource limitations
- `stakeholders`: Who is involved or affected
- `existing_docs`: Related materials or references

## Workflow

### Step 1: Extract Key Elements

Parse the brain dump to identify:
- **Core idea**: What is the fundamental concept?
- **Implicit goals**: What outcomes are implied?
- **Mentioned constraints**: What limitations exist?
- **Success indicators**: How will success be measured?

### Step 2: Structure into Template

Organize extracted elements into the brief template (see `resources/brief_template.md`):

```markdown
# Project Brief: {project_name}

## Overview
**Created:** {date}
**Status:** Active
**Owner:** Omer

## Problem Statement
{what_problem_does_this_solve}

## Goals
1. {primary_goal}
2. {secondary_goals}

## Scope
### In Scope
- {included_items}

### Out of Scope
- {excluded_items}

## Milestones
| Milestone | Target Date | Status |
|-----------|-------------|--------|
| {milestone_1} | {date} | Not Started |

## Deliverables
- {deliverable_1}

## Success Criteria
- {criterion_1}

## Constraints & Risks
- {constraint_or_risk}

## Notes
{additional_context}
```

### Step 3: Interactive Refinement

**CHECKPOINT:** Present draft brief to user

Ask clarifying questions:
- "Is the problem statement accurate?"
- "Are there additional goals I should include?"
- "What's the target timeline?"
- "Who are the key stakeholders?"

Iterate until user approves the brief.

### Step 4: Save and Notify

- Save as `{project}_brief.md` in project location
- Suggest next step: "Create task breakdown using task-engine"

## Output Format

The brief follows the template in `resources/brief_template.md` with all placeholders replaced with project-specific content.

## Example Interaction

**User Input:**
> "יש לי רעיון לפרויקט חדש - לבנות framework לאסטרטגיית AI לפקולטה למשפטים. רוצה להציע את זה לדיקן."

**Skill Response:**
1. **Extracts**: AI strategy, Law Faculty, presentation to Dean
2. **Asks**: "What's the timeline for the Dean presentation?"
3. **Drafts**: Brief with goals, scope, milestones
4. **Checkpoints**: "Does this capture your vision?"
5. **Saves**: `ai_strategy_law_faculty_brief.md`

## Cross-Interface Notes

- **Claude AI**: Template is read from skill's resources/ folder
- **Claude Code**: Template is read from filesystem path

