---
name: fleet-sprint
description: How to manage a sprint lifecycle — load, track, report
user-invocable: true
---

# Fleet Sprint Skill

## Load a Sprint
```bash
fleet sprint load config/sprints/{plan}.yaml
```

## Check Sprint Status
```bash
fleet sprint status {plan-id}
```

## Sprint Lifecycle
1. **Plan**: PM breaks down epic into tasks with dependencies
2. **Load**: Sprint YAML loaded into MC with dependency chains
3. **Dispatch**: Orchestrator auto-dispatches unblocked tasks
4. **Work**: Agents execute, commit, complete
5. **Review**: fleet-ops reviews via review chain
6. **Done**: Tasks transition, dependencies unblock, next dispatched
7. **Complete**: All tasks done → parent epic to review
8. **Retro**: PM reports velocity, agent performance, lessons

## Sprint YAML Format
```yaml
sprint:
  id: project-s1
  name: "Sprint 1: Description"
  start_date: 2026-04-01
  end_date: 2026-04-14

tasks:
  - id: s1-epic
    title: "Sprint epic title"
    type: epic
    priority: high

  - id: s1-task-1
    title: "First task"
    type: task
    parent: s1-epic
    agent: software-engineer
    story_points: 3

  - id: s1-task-2
    title: "Depends on task 1"
    depends_on: [s1-task-1]
    agent: qa-engineer
    story_points: 2
```