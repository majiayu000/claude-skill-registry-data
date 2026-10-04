---
name: fleet-plan
description: How to break down an epic into sprint tasks with dependencies
user-invocable: false
---

# Fleet Planning Skill

You are breaking down work into a structured sprint plan.

## 1. Analyze the Epic/Request
- What are the requirements?
- What components are involved?
- What are the dependencies?
- What are the risks?

## 2. Break Down into Tasks

For each task, define:
- **Title**: Clear, actionable (start with verb)
- **Type**: epic/story/task/subtask
- **Agent**: Who should do this (use routing: architect for design, sw-eng for code, etc.)
- **Story Points**: 1/2/3/5/8/13 (complexity estimate)
- **Dependencies**: What must complete first
- **Priority**: urgent/high/medium/low

## 3. Create Tasks with Dependencies

```
# First task (no dependencies)
fleet_task_create(
  title="Design auth architecture",
  agent_name="architect",
  task_type="story",
  story_points=5,
  priority="high",
  parent_task="{epic_id}"
)

# Dependent task
fleet_task_create(
  title="Implement auth middleware",
  agent_name="software-engineer",
  depends_on=["{design_task_id}"],
  task_type="task",
  story_points=5,
  parent_task="{epic_id}"
)
```

## 4. Verify the Plan
- All tasks have agents assigned
- Dependencies form a DAG (no circular)
- Critical path identified (longest dependency chain)
- Story points total is reasonable
- Blockers and risks identified