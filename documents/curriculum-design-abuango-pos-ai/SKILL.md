---
name: curriculum-design
description: Learning Coach skill for creating structured learning curricula. Use when designing study plans, certification prep paths, or skill development programs. Triggers on phrases like "create curriculum", "study plan for", "learn X", "certification prep", or "design learning path".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Curriculum Design

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Create structured learning curricula with modules, resources, and assessments.

## Commands

- `@coach curriculum` - List active curricula
- `@coach create` - Create new curriculum
- `@coach update [id]` - Modify curriculum
- `@coach resources [id]` - Manage resources
- `@coach progress` - Show progress summary

## Directory Layout

```
contexts/personal/learning/
├── goals.yaml
├── curriculum/active/    # In progress
├── curriculum/completed/
├── progress/             # Weekly logs
└── resources/
```

## Design Process

1. **Gather Requirements:** learning goal (cert/skill/project), target date, hours/week, current level, focus areas
2. **Research:** official syllabus, best practices, resource availability
3. **Structure Modules:** topics, estimated hours, resources, assessments, dependencies per module
4. **Create Schedule:** map modules to weeks, add review time and buffer
5. **Curate Resources:** docs, courses, books, labs, practice exams (up to date, well-reviewed, accessible)
6. **Design Assessments:** quizzes (knowledge), labs (practical), projects (synthesis), mock exams (readiness)

## Curriculum YAML Schema

Save to `contexts/personal/learning/curriculum/active/{id}.yaml`:

```yaml
id: {topic-id}
title: "{title}"
target_date: "YYYY-MM-DD"
schedule:
  weekly_hours: 5
  total_weeks: 20
progress:
  overall_percent: 0
  current_module: {first-module}
modules:
  - id: {module-id}
    title: "{title}"
    weight: 19  # % of exam if cert
    status: not_started
    estimated_hours: 15
    topics: [...]
    resources:
      - type: documentation | course | book | lab
        title: "{title}"
        url: "{url}"
    assessments:
      - type: quiz | lab | project | mock_exam
        title: "{title}"
```

## Output

```
## New Curriculum: [Title]
**Goal:** [cert/skill] | **Target:** [date] | **Schedule:** [hours/week] x [weeks]

### Modules
| # | Module | Weight | Hours | Status |
|---|--------|--------|-------|--------|

**Saved to:** `contexts/personal/learning/curriculum/active/[id].yaml`
```

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
