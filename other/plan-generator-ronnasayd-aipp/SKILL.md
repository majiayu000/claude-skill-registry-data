---
name: plan-generator
description: Generate structured plans for tasks and projects, saved as date-stamped markdown files in docs/agents/plans/. Use whenever the user wants to plan a project, break down a task, create a roadmap, design a workflow, or organize phases and milestones — even if they just say "make a plan for X" or "how should I approach Y".
argument-hint: Describe the task or project. Include scope, constraints, team size, and timeline if known.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

## Overview

Creates structured, actionable plans saved to `docs/agents/plans/` with date-stamped filenames (`yyyy-mm-dd-short-description.md`).

## Instructions

1. **Understand scope**: Identify what's in/out and any constraints
2. **Define phases**: Break work into logical phases with clear boundaries and dependencies
3. **Estimate and assign**: Set realistic durations and owners per phase
4. **Define success**: Add measurable success criteria
5. **Save file**: Use format `docs/agents/plans/yyyy-mm-dd-short-description.md`
   - Example: `17-03-2026-api-migration-plan.md`

## Plan Template

```markdown
# Plan: [Title]

**Created:** DD/MM/YYYY
**Type:** Task | Project | Process | Strategy
**Status:** Draft | In Progress | Ready for Review

## Overview

[What this plan covers and why it matters]

## Objectives

- [ ] Objective 1
- [ ] Objective 2

## Scope

**Included:** item 1, item 2
**Excluded:** item 1, item 2

## Phase 1: [Name]

**Duration:** X weeks | **Owner:** [Who]
**Deliverables:** deliverable 1, deliverable 2
**Tasks:**

- [ ] Task 1
- [ ] Task 2

**Dependencies:** [None | depends on Phase X]

[Repeat for each phase]

## Timeline

| Phase   | Start | End |
| ------- | ----- | --- |
| Phase 1 | ...   | ... |

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Risks

| Risk   | Impact          | Mitigation |
| ------ | --------------- | ---------- |
| Risk 1 | High/Medium/Low | Strategy   |

## Checkpoints

- [ ] Mid-point review (Date)
- [ ] Final review (Date)
```
